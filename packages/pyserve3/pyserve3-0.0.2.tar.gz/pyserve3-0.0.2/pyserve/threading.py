"""
Threading Implementations of session-based servers
"""
import socket
import socketserver
from ssl import SSLContext, wrap_socket
from dataclasses import dataclass, field
from typing import Type, Optional, Dict, Any, ClassVar

from .abc import RawAddr, Address, Writer, Session, modify_socket

#** Variables **#
__all__ = ['UdpThreadServer', 'TcpThreadServer']

#** Functions **#

def new_handler(
    base:      Type['BaseRequestHandler'],
    factory:   Type[Session],
    args:      tuple           = (),
    kwargs:    Dict[str, Any]  = {},
    timeout:   Optional[int]   = None,
    interface: Optional[bytes] = None,
    blocksize: int             = 8192
) -> Type['BaseRequestHandler']:
    """
    spawn new request-handler class w/ configured settings
    """
    # test factory generation
    factory(*args, **kwargs)
    # generate new request handler
    name = f'{base.__name__}Instance'
    return type(name, (base, ), dict(
        factory=factory,
        args=args,
        kwargs=kwargs,
        timeout=timeout,
        interface=interface,
        blocksize=blocksize,
    ))

#** Classes **#

@dataclass
class UdpWriter(Writer):
    addr: Address
    sock: socket.socket
    closing: bool = False
    
    def write(self, data: bytes, addr: Optional[Address] = None):
        self.sock.sendto(data, addr or self.addr)

    def close(self):
        self.sock.close()
        self.closing = True

    def is_closing(self) -> bool:
        return self.closing

@dataclass
class TcpWriter(Writer):
    sock: socket.socket
    closing: bool = False

    def write(self, data: bytes):
        self.sock.sendall(data)

    def close(self):
        self.closing = True
        self.sock.close()

    def is_closing(self) -> bool:
        return self.closing

class BaseRequestHandler(socketserver.BaseRequestHandler):
    factory:   Type[Session]
    args:      tuple           
    kwargs:    Dict[str, Any]
    timeout:   Optional[int]
    interface: Optional[bytes]
    blocksize: int

    def setup(self):
        """configure and generate session w/ information collected"""
        self.addr:   Address = Address(*self.client_address)
        self.sock:   socket.socket
        self.writer: Writer
        self.error:  Optional[Exception] = None
        modify_socket(self.sock, self.timeout, self.interface)
        # spawn session object
        self.session = self.factory(*self.args, **self.kwargs)
        self.session.connection_made(self.addr, self.writer)
    
    def finish(self):
        """notify that connection disconnected"""
        self.session.connection_lost(self.error)

class UdpHandler(BaseRequestHandler):
    
    def setup(self):
        """handle connection spawn"""
        self.addr    = Address(*self.client_address) 
        self.sock    = self.request[1]
        self.writer: UdpWriter = UdpWriter(self.addr, self.sock)
        super().setup()

    def handle(self):
        """handle single inbound udp packet"""
        try:
            data = self.request[0]
            self.session.data_recieved(data)
        except socket.error as e:
            self.error = e
            if not self.writer.closing:
                self.writer.close()

class TcpHandler(BaseRequestHandler):
    
    def setup(self):
        """handle setup of server"""
        self.sock = self.request
        self.writer: TcpWriter = TcpWriter(self.sock)
        super().setup()

    def handle(self):
        """handle subsequent reads of inbound data"""
        while not self.writer.closing:
            try:
                data = self.sock.recv(self.blocksize)
                if not data:
                    break
                self.session.data_recieved(data)
            except socket.error as e:
                self.error = e
                if not self.writer.closing:
                    self.writer.close()
                break

@dataclass
class BaseThreadServer(socketserver.ThreadingMixIn):
    server:    ClassVar[Type[socketserver.BaseServer]]
    handler:   ClassVar[Type[BaseRequestHandler]]

    address:    RawAddr
    factory:    Type[Session]
    args:       tuple           = field(default_factory=tuple)
    kwargs:     Dict[str, Any]  = field(default_factory=dict)
    timeout:    Optional[int]   = None
    interface:  Optional[bytes] = None
    reuse_port: bool            = False
    
    def __post_init__(self):
        self.allow_reuse_port = self.reuse_port
        # build handler for base init
        self.server.__init__(self, self.address, new_handler( #pyright: ignore
            base=self.handler, 
            factory=self.factory, 
            args=self.args, 
            kwargs=self.kwargs,
            timeout=self.timeout,
            interface=self.interface,
            blocksize=getattr(self, 'blocksize', 8192),
        ))
    
    def __exit__(self, *_):
        """ensure server is shutdown properly"""
        self.shutdown()

    def shutdown(self):
        raise NotImplementedError

@dataclass
class UdpThreadServer(BaseThreadServer, socketserver.UDPServer):
    server  = socketserver.UDPServer
    handler = UdpHandler

    allow_broadcast: bool = False

    def __post_init__(self):
        super().__post_init__()
        if self.allow_broadcast:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    def shutdown(self):
        """override shutdown behavior"""
        self.server.shutdown(self)
        self.socket.close()
        self.server_close()

@dataclass
class TcpThreadServer(BaseThreadServer, socketserver.TCPServer):
    server  = socketserver.TCPServer
    handler = TcpHandler

    ssl:       Optional[SSLContext] = None
    blocksize: int                  = 8192
    
    def __post_init__(self):
        super().__post_init__()
        if self.ssl:
            self.socket = wrap_socket(self.socket, server_side=True)

    def shutdown(self):
        """override shutdown behavior"""
        self.socket: socket.socket
        self.server.shutdown(self) #pyright: ignore
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        self.server_close()

