pyserve
--------
Unify SocketServer Implementations based on a Session Model

### Install

```bash
pip install pyserve3
```

### Example

```python
from pyserve import *
from typing import Optional

class EchoServer(Session):
    
    def connection_made(self, addr: Address, writer: Writer):
        print('connection made!', addr, writer)
        self.addr   = addr
        self.writer = writer

    def data_recieved(self, data: bytes):
        print(f'recieved {data!r} from {self.addr}')
        self.writer.write(data)
        self.writer.close()

    def connection_lost(self, err: Optional[Exception]):
        print('connection lost!', self.addr, err)

# run sync
# listen_udp_threaded(('127.0.0.1', 8000), EchoServer)
# listen_tcp_threaded(('127.0.0.1', 8000), EchoServer)

# run async
import asyncio
# asyncio.run(listen_udp_async(('127.0.0.1', 8000), EchoServer))
asyncio.run(listen_tcp_async(('127.0.0.1', 8000), EchoServer))
```

