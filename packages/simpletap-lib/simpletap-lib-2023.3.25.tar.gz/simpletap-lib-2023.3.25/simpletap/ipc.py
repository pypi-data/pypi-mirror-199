"""
ipc.py is part of The SimpleTap Project.
https://git.benmickler.com/SimpleTap/simpletap
Copyright (C) 2023  Benjamin Mickler

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import json
import uuid
import asyncio
from multiprocessing import Queue, Process, get_context
from multiprocessing.queues import Queue as MPQueue

from simpletap import resources

class AsyncMPQueue:
    def __init__(self, maxsize=0):
        self._queue = MPQueue(maxsize=maxsize, ctx=get_context())

    def init(self):
        self._loop = asyncio.get_event_loop()

    async def put(self, item):
        await self._loop.run_in_executor(None, self._queue.put, item)

    async def get(self):
        return await self._loop.run_in_executor(None, self._queue.get)

    def sync_put(self, item):
        self._queue.put(item)

    def sync_get(self):
        self._queue.get()

    def empty(self):
        return self._queue.empty()

    def full(self):
        return self._queue.full()

    def qsize(self):
        return self._queue.qsize()

    def close(self):
        self._queue.close()

    def join_thread(self):
        self._queue.join_thread()

def run_async(func, args, kwargs):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(func(*args, **kwargs))


class ProxyObject:
    def __getitem__(self, key):
        return self.__dict__[key]
    def __setitem__(self, key, value):
        self.__dict__[key] = value
    def __delitem__(self, key):
        del self.__dict__[key]
    def __iter__(self):
        return iter(self.__dict__)
    def __len__(self):
        return len(self.__dict__)

class Server:
    def __init__(self, port=None):
        self.funcs = {}
        self.port = port
        if not self.port:
            self.port = resources.find_free_port()
        self.clients = {}
    async def call_callback(self, client_uuid, func, *args, **kwargs):
        reader, writer = self.clients[client_uuid]
        writer.write(f"{json.dumps({'type': 'callback', 'func': func, 'args': args, 'kwargs': kwargs})}\r\n".encode())
    async def handle(self, reader, writer):
        client_uuid = str(uuid.uuid4())
        self.clients[client_uuid] = (reader, writer)
        writer.write(f"{json.dumps({'type': 'uuid', 'uuid': client_uuid})}\r\n".encode())
        buff = b""
        while True:
            while b'\r\n' not in buff:
                data = await reader.read(100)
                if not data or data == b"END\r\n":
                    break
                buff += data
            if not data or data == b"END\r\n":
                break
            data,sep,buff = buff.partition(b'\r\n')
            data = json.loads(data)
            if data["type"] == "call":
                if data["func"] in self.funcs:
                    if asyncio.iscoroutinefunction(self.funcs[data["func"]]):
                        task = asyncio.create_task(self.funcs[data["func"]](self, client_uuid, *data["args"], **data["kwargs"]))
                        await task
                        returndata = task.result()
                    else:
                        returndata = self.funcs[data["func"]](self, client_uuid, *data["args"], **data["kwargs"])
                else:
                    returndata = "ERROR: Function not found"
                writer.write(f"{json.dumps({'type': 'return', 'uuid': data['uuid'], 'return': returndata})}\r\n".encode())
    async def start(self):
        server = await asyncio.start_server(self.handle, '127.0.0.1', self.port)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')
        async with server:
            await server.serve_forever()

class Client:
    def __init__(self, server):
        self.server = server
        self.uuid = None
        self.callbacks = {}
        self.return_events = {}
        self.returns = {}
        self.connected = asyncio.Event()
    async def connect(self):
        for i in range(10):
            try:
                self.reader, self.writer = await asyncio.open_connection(self.server[0], self.server[1])
                self.connected.set()
                asyncio.create_task(self.listen())
                return True
            except:
                pass
        return False
    async def call(self, func, *args, **kwargs):
        if not self.connected.is_set():
            await self.connected.wait()
        call_uuid = str(uuid.uuid4())
        self.writer.write(f"{json.dumps({'uuid': call_uuid, 'type': 'call', 'func': func, 'args': args, 'kwargs': kwargs})}\r\n".encode())
        await self.writer.drain()
        self.return_events[call_uuid] = asyncio.Event()
        await self.return_events[call_uuid].wait()
        return self.returns[call_uuid]
    async def listen(self):
        buff = b""
        while True:
            while b'\r\n' not in buff:
                data = await self.reader.read(100)
                if not data or data == b"END\r\n":
                    break
                buff += data
            if not data or data == b"END\r\n":
                break
            data,sep,buff = buff.partition(b'\r\n')
            data = json.loads(data)
            if data["type"] == "uuid":
                self.uuid = data["uuid"]
            elif data["type"] == "return":
                if data["uuid"] in self.return_events:
                    self.returns[data["uuid"]] = data["return"]
                    self.return_events[data["uuid"]].set()
            elif data["type"] == "callback":
                if data["func"] in self.callbacks:
                    if asyncio.iscoroutinefunction(self.callbacks[data["func"]]):
                        asyncio.create_task(self.callbacks[data["func"]](*data["args"], **data["kwargs"]))
                    else:
                        self.callbacks[data["func"]](*data["args"], **data["kwargs"])