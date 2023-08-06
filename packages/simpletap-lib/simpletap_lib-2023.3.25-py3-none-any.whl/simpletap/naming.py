"""
naming.py is part of The SimpleTap Project.
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

import asyncio
import json

pymongo_import_error = False
try:
    from pymongo import MongoClient
except (ImportError, ModuleNotFoundError):
    print("pymongo not installed, using in-memory hash table")
    pymongo_import_error = True

class NameServer:
    def __init__(self, server):
        self.server = server
        self.names = {}
        if pymongo_import_error:
            db = False
        self.db = db
        if db:
            self.client = MongoClient()
            self.database = self.client["simpletap"]
            self.names = self.database["names"]

    async def handle(self, reader, writer):
        buff = b""
        while b'\r\n' not in buff:
            data = await reader.read(100)
            buff += data
        data, sep, buff = buff.partition(b'\r\n')
        data = json.loads(data.decode())
        if "name" not in data:
            return
        if "action" not in data:
            return
        if data["action"] == "set":
            if "value" not in data:
                return
            self.names[data["name"]] = data["value"]
        elif data["action"] == "get":
            if data["name"] in self.names:
                writer.write(self.names[data["name"]].encode() + b'\r\n')
        writer.close()
        await writer.wait_closed()

    async def _context_mngr_server(self):
        async with self._server:
            await self._server.serve_forever()

    async def start(self):
        self._server = await asyncio.start_server(self.handle, self.server[0], self.server[1])
        addrs = ', '.join(str(sock.getsockname())
                          for sock in self._server.sockets)
        self.kernel_server_task = asyncio.create_task(
            self._context_mngr_server())
        return self

class NameClient:
    def __init__(self, server):
        self.server = server

    async def _context_mngr_client(self):
        async with self._client:
            await self._client.serve_forever()

    async def start(self):
        self._client = await asyncio.start_server(self.handle, self.server[0], self.server[1])
        addrs = ', '.join(str(sock.getsockname())
                          for sock in self._client.sockets)
        self.kernel_client_task = asyncio.create_task(
            self._context_mngr_client())
        return self

    async def set(self, name, value):
        reader, writer = await asyncio.open_connection(self.server[0], self.server[1])
        writer.write(json.dumps({"name": name, "value": value, "action": "set"}).encode() + b'\r\n')
        writer.close()
        await writer.wait_closed()

    async def get(self, name):
        reader, writer = await asyncio.open_connection(self.server[0], self.server[1])
        writer.write(json.dumps({"name": name, "action": "get"}).encode() + b'\r\n')
        buff = b""
        while b'\r\n' not in buff:
            data = await reader.read(100)
            buff += data
        data, sep, buff = buff.partition(b'\r\n')
        writer.close()
        await writer.wait_closed()
        return data.decode()