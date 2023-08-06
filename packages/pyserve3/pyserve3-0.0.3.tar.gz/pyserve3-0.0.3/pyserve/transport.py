"""
AsyncIO Implementations of session-based servers
"""
import asyncio
from dataclasses import dataclass, field
from typing import Type, Optional, Dict, Any

from .abc import RawAddr, Address, Writer, Session, modify_socket

#** Variables **#
__all__ = ['UdpProtocol', 'TcpProtocol']

#** Classes **#

@dataclass
class UdpWriter(Writer):
    addr:      Address
    transport: asyncio.DatagramTransport
    
    def write(self, data: bytes, addr: Optional[Address] = None):
        self.transport.sendto(data, addr or self.addr)

    def close(self):
        self.transport.close()

    def is_closing(self) -> bool:
        return self.transport.is_closing()

@dataclass
class BaseProtocol:
    factory:   Type[Session]
    args:      tuple           = field(default_factory=tuple)
    kwargs:    Dict[str, Any]  = field(default_factory=dict)
    timeout:   Optional[int]   = None
    interface: Optional[bytes] = None

    def test_factory(self):
        """validate session can be generated w/ args and kwargs"""
        self.factory(*self.args, **self.kwargs)

    def set_timeout(self, timeout: int, tport: asyncio.Transport):
        """implement timeout handling for async servers"""
        # generate async expiration function
        async def expire():
            await asyncio.sleep(timeout)
            if not tport.is_closing():
                tport.abort()
        # spawn future to kill transport
        loop = asyncio.get_event_loop()
        loop.create_task(expire())

class UdpProtocol(BaseProtocol, asyncio.DatagramTransport):
 
    def connection_made(self, transport: asyncio.DatagramTransport):
        """"""
        self.transport = transport
        # handle modifying socket and making changes for handling
        socket = transport.get_extra_info('socket')
        modify_socket(socket, None, self.interface)
        if self.timeout is not None:
            self.set_timeout(self.timeout, transport) #pyright: ignore
       
    def datagram_received(self, data: bytes, addr: RawAddr):
        """"""
        # generate session w/ attributes and notify on connection-made
        address      = Address(*addr)
        writer       = UdpWriter(address, self.transport)
        self.session = self.factory(*self.args, **self.kwargs)
        self.session.connection_made(address, writer)
        self.session.data_recieved(data)

    def connection_lost(self, err: Optional[Exception]):
        """"""
        self.session.connection_lost(err)

class TcpProtocol(BaseProtocol, asyncio.Protocol):
   
    def connection_made(self, transport: asyncio.Transport):
        """"""
        # collect attributes and prepare socket for session
        address = Address(*transport.get_extra_info('peername'))
        socket  = transport.get_extra_info('socket')
        # handle modifying socket and making changes for handling
        modify_socket(socket, None, self.interface)
        if self.timeout is not None:
            self.set_timeout(self.timeout, transport)
        # generate session w/ attributes and notify on connection-made
        self.session = self.factory(*self.args, **self.kwargs)
        self.session.connection_made(address, transport)

    def data_received(self, data: bytes):
        """"""
        self.session.data_recieved(data)

    def connection_lost(self, err: Optional[Exception]):
        """"""
        self.session.connection_lost(err)
