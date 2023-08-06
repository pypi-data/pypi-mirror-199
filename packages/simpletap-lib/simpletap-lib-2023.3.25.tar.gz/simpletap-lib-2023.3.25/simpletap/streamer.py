"""
streamer.py is part of The SimpleTap Project.
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
import base64
import json
import os
import traceback
import uuid

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from simpletap.exceptions.streamer import *
from simpletap.resources import find_free_port

pymongo_import_error = False
try:
    from pymongo import MongoClient
except (ImportError, ModuleNotFoundError):
    print("pymongo not installed, using in-memory hash table")
    pymongo_import_error = True

from simpletap.auth import User, Challenge

class Streamer:
    def __init__(self, reader, writer, request_key):
        self.reader = reader
        self.writer = writer
        self.request_key = request_key
        self.f = Fernet(self.request_key)
    async def __aiter__(self):
        return self
    async def __anext__(self):
        data = await self.reader.read(1024)
        if not data or data == b"END":
            raise StopAsyncIteration
        request = base64.b64decode(data)
        try:
            request = self.f.decrypt(request)
        except:
            return {"error": "Invalid request"}
        return data
    async def send(self, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        data = self.f.encrypt(data.encode())
        self.writer.write(base64.b64encode(data))
        await self.writer.drain()
    async def end(self):
        self.writer.write(b"END")
        await self.writer.drain()

class StreamerServer:
    def __init__(self, handler, host="0.0.0.0", port=6537, db=True, allow_registration=True):
        self.host = host
        self.port = port
        self.allow_registration = allow_registration
        self.users = {}
        if pymongo_import_error:
            db = False
        self.db = db
        if db:
            self.client = MongoClient()
            self.database = self.client["simpletap"]
            self.users = self.database["users"]
        self.handler = handler

    async def read(self, reader):
        buff = b""
        while b'\r\n' not in buff:
            data = await reader.read(100)
            if not data or data == b"END\r\n":
                break
            buff += data
        data, sep, buff = buff.partition(b"\r\n")
        return data

    async def auth_challenge(self, reader, writer, user):
        if self.db:
            challenge_public_key = serialization.load_pem_public_key(
                user["challenge_public_key"], backend=default_backend())
        else:
            challenge_public_key = serialization.load_pem_public_key(
                self.users[user]["challenge_public_key"], backend=default_backend())
        challenge = Challenge(challenge_public_key)
        writer.write(f"5?{challenge.generate().decode()}\r\n".encode())
        await writer.drain()
        data = await self.read(reader)
        if not data:
            return
        data = data.decode().split("?")
        if data[0] != "6":
            return
        if not challenge.verify(base64.b64decode(data[1])):
            writer.write(b"4?2?Challenge failed\r\n")
            await writer.drain()
            return False
        writer.write(b"7?Challenge passed\r\n")
        await writer.drain()
        return True

    async def _handle_client(self, reader, writer):
        data = await self.read(reader)
        if not data:
            return
        data = data.decode().split("?")
        action = data[0]
        if action == "0":
            if not self.allow_registration:
                writer.write(b"4?1?Registration not allowed\r\n")
                await writer.drain()
            else:
                request_key = rsa.generate_private_key(
                    public_exponent=65537, key_size=2048, backend=default_backend())
                response_key = rsa.generate_private_key(
                    public_exponent=65537, key_size=2048, backend=default_backend())
                request_public_key = request_key.public_key().public_bytes(encoding=serialization.Encoding.PEM,
                                                                           format=serialization.PublicFormat.SubjectPublicKeyInfo)
                request_private_key = request_key.private_bytes(
                    encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
                response_private_key = response_key.private_bytes(
                    encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
                client_uuid = str(uuid.uuid4())
                if self.db:
                    self.users.insert_one(
                        {"status": {"state": "active", "reason": ""}, "uuid": client_uuid, "request_key": request_private_key, "response_key": response_private_key, "challenge_public_key": base64.b64decode(data[1].encode())})
                else:
                    self.users[client_uuid] = {
                        "status": {"state": "active", "reason": ""}, "request_private_key": request_private_key, "response_private_key": response_private_key, "challenge_public_key": base64.b64decode(data[1].encode())}
                writer.write(
                    f"2?{client_uuid}?{request_public_key.decode()}?{response_private_key.decode()}\r\n".encode())
                await writer.drain()
        elif action == "1":
            user_uuid = data[1]
            if self.db:
                user = self.users.find_one({"uuid": user_uuid})
                if not user:
                    writer.write(b"4?1?User not found\r\n")
                    await writer.drain()
                    raise UserNotFound(user_uuid)
            else:
                if user_uuid not in self.users:
                    writer.write(b"4?1?User not found\r\n")
                    await writer.drain()
                    raise UserNotFound(user_uuid)
                user = user_uuid
            if not await self.auth_challenge(reader, writer, user):
                writer.write(b"4?2?Invalid key\r\n")
                await writer.drain()
                raise InvalidKey(user_uuid)
            if self.db:
                request_private_key = serialization.load_pem_private_key(
                    user["request_key"], password=None, backend=default_backend())
            else:
                request_private_key = serialization.load_pem_private_key(
                    self.users[user_uuid]["request_private_key"], password=None, backend=default_backend())
            try:
                request_key = request_private_key.decrypt(base64.b64decode(data[2]), padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
            except:
                writer.write(b"4?2?Invalid key\r\n")
                await writer.drain()
                raise InvalidKey(user_uuid)
            request = base64.b64decode(data[3])
            f = Fernet(request_key)
            request = f.decrypt(request)
            if data[4] == "str":
                request = request.decode()
            elif data[4] == "json":
                request = json.loads(request)
            user_obj = User(user_uuid)
            streamer = Streamer(reader, writer, request_key)
            if asyncio.iscoroutinefunction(self.handler):
                response = await self.handler(user_obj if self.db else user, request, streamer)
            else:
                response = self.handler(user_obj if self.db else user, request, streamer)
            response_key = Fernet.generate_key()
            f = Fernet(response_key)
            response_format = "bytes"
            if isinstance(response, str):
                response_format = "str"
                response = response.encode()
            elif isinstance(response, dict) or isinstance(response, list):
                response_format = "json"
                response = json.dumps(response).encode()
            elif not isinstance(response, bytes):
                raise TypeError("Response must be bytes, str or json")
            response = f.encrypt(response)
            if self.db:
                response_private_key = serialization.load_pem_private_key(
                    user["response_key"], password=None, backend=default_backend())
            else:
                response_private_key = serialization.load_pem_private_key(
                    self.users[user_uuid]["response_private_key"], password=None, backend=default_backend())
            response_key = response_private_key.public_key().encrypt(response_key, padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
            writer.write(
                f"3?{base64.b64encode(response_key).decode()}?{base64.b64encode(response).decode()}?{response_format}\r\n".encode())
            await writer.drain()

    async def handle_client(self, reader, writer):
        try:
            await self._handle_client(reader, writer)
        except Exception as e:
            print(traceback.format_exc())

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')
        async with server:
            await server.serve_forever()

class StreamerClient:
    def __init__(self, path, host="127.0.0.1", port=6537):
        self.path = path
        self.host = host
        self.port = port
        self.request_public_key = None
        self.response_private_key = None
        self.challenge_private_key = None
        self.uuid = uuid

    def load(self):
        if not os.path.exists(self.path / "uuid"):
            return False
        if not os.path.exists(self.path / "request_public_key"):
            return False
        if not os.path.exists(self.path / "response_private_key"):
            return False
        if not os.path.exists(self.path / "challenge_private_key"):
            return False
        try:
            with open(self.path / "uuid", "r") as f:
                self.uuid = f.read()
            with open(self.path / "request_public_key", "r") as f:
                self.request_public_key = f.read()
            with open(self.path / "response_private_key", "r") as f:
                self.response_private_key = f.read()
            with open(self.path / "challenge_private_key", "r") as f:
                self.challenge_private_key = f.read()
            self.request_public_key = serialization.load_pem_public_key(
                self.request_public_key.encode(), backend=default_backend())
            self.response_private_key = serialization.load_pem_private_key(
                self.response_private_key.encode(), password=None, backend=default_backend())
            self.challenge_private_key = serialization.load_pem_private_key(
                self.challenge_private_key.encode(), password=None, backend=default_backend())
        except:
            raise LocalDataCorrupted("Local data corrupted")
        return True

    async def connect(self):
        for i in range(10):
            try:
                reader, writer = await asyncio.open_connection(self.host, self.port)
                return reader, writer
            except Exception as e:
                print(f"Error connecting to server: {e}, retrying...")
                await asyncio.sleep(0.5)
        raise RepeatedConnectionFailed("Could not connect to server")