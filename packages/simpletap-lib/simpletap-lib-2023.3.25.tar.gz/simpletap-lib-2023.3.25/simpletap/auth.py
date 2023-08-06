"""
auth.py is part of The SimpleTap Project.
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
import secrets
import string
import traceback
import uuid
import socket
from contextlib import closing
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve import PublicKey

from simpletap.exceptions.auth import *

# secp256k1
# https://github.com/starkbank/ecdsa-python

class ChallengeResponse:
    def __init__(self, private_key_pem):
        self.private_key = PrivateKey.fromPem(private_key_pem)
    def sign(self, challenge):
        return Ecdsa.sign(challenge, self.private_key).toBase64()

class ChallengeServer:
    def __init__(self, public_key_pem):
        self.public_key = PublicKey.fromPem(public_key_pem)
    def generate(self):
        letters = string.ascii_lowercase+string.ascii_uppercase+string.digits
        return ''.join(secrets.choice(letters) for i in range(50)).encode()
    def verify(self, challenge, signature):
        return Ecdsa.verify(challenge, signature, self.public_key)

pymongo_import_error = False
try:
    from pymongo import MongoClient
except (ImportError, ModuleNotFoundError):
    print("pymongo not installed, using in-memory hash table")
    pymongo_import_error = True

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

class User:
    def __init__(self, user_uuid):
        self.user_uuid = user_uuid
        self._db_client = MongoClient()
        self._database = self._db_client["simpletap"]
        self._users = self._database["users"]
        self.user = self._users.find_one({"uuid": self.user_uuid})
        if self.user is None:
            raise UserNotFound(self.user_uuid)
        self._attributes = []
        for attribute in self.user:
            if attribute == "_id":
                continue
            self._attributes.append(attribute)
            setattr(self, attribute, self.user[attribute])
    def delete(self):
        self.users.delete_one({"uuid": self.user_uuid})
    def save(self):
        for attribute in self._attributes:
            self.users.update_one({"uuid": self.user_uuid}, {"$set": {attribute: getattr(self, attribute)}})
    def new_attribute(self, attribute, value):
        self._attributes.append(attribute)
        setattr(self, attribute, value)
        self.users.update_one({"uuid": self.user_uuid}, {"$set": {attribute: value}})
    def delete_attribute(self, attribute):
        self._attributes.remove(attribute)
        delattr(self, attribute)
        self.users.update_one({"uuid": self.user_uuid}, {"$unset": {attribute: 1}})

class Challenge:
    def __init__(self, public_key):
        self.public_key = public_key

    def generate(self):
        letters = string.ascii_lowercase+string.ascii_uppercase+string.digits
        self.original_data = ''.join(secrets.choice(letters)
                                     for i in range(50)).encode()
        self.encrypted_data = self.public_key.encrypt(self.original_data, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        self.encrypted_data_base64 = base64.b64encode(self.encrypted_data)
        return self.encrypted_data_base64

    def verify(self, data: bytes):
        return data == self.original_data


class DirReqServer:
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
            if asyncio.iscoroutinefunction(self.handler):
                response = await self.handler(user_obj if self.db else user, request)
            else:
                response = self.handler(user_obj if self.db else user, request)
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


class DirReqClient:
    def __init__(self, path, uuid=None, host="127.0.0.1", port=6537):
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

    async def read(self, reader):
        buff = b""
        while b'\r\n' not in buff:
            data = await reader.read(100)
            if not data or data == b"END\r\n":
                break
            buff += data
        data, sep, buff = buff.partition(b'\r\n')
        return data

    async def auth_challenge(self, reader, writer):
        data = await self.read(reader)
        if not data:
            raise InvalidChallenge("No challenge received")
        data = data.split(b"?")
        if data[0] != b"5":
            raise InvalidChallenge("Invalid challenge received")
        challenge = base64.b64decode(data[1])
        challenge = self.challenge_private_key.decrypt(challenge, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        writer.write(f"6?{base64.b64encode(challenge).decode()}\r\n".encode())
        await writer.drain()
        data = await self.read(reader)
        if not data:
            raise InvalidChallenge("No challenge response received")
        data = data.split(b"?")
        if data[0] != b"7":
            raise InvalidChallenge("Invalid challenge response received")

    async def register(self):
        challenge_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend())
        challenge_public_key = challenge_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
        challenge_private_key = challenge_key.private_bytes(
            encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
        self.challenge_private_key = challenge_key
        with open(self.path / "challenge_private_key", "wb") as f:
            f.write(challenge_private_key)
        reader, writer = await self.connect()
        writer.write(
            f"0?{base64.b64encode(challenge_public_key).decode()}\r\n".encode())
        await writer.drain()
        data = await self.read(reader)
        if not data:
            return
        data = data.split(b"?")
        action = data[0]
        if action == b"2":
            self._request_public_key = data[2]
            self._response_private_key = data[3]
            self.uuid = data[1].decode()
            with open(self.path / "uuid", "w") as f:
                f.write(self.uuid)
            with open(self.path / "request_public_key", "wb") as f:
                f.write(self._request_public_key)
            with open(self.path / "response_private_key", "wb") as f:
                f.write(self._response_private_key)
            self.request_public_key = serialization.load_pem_public_key(
                self._request_public_key, backend=default_backend())
            self.response_private_key = serialization.load_pem_private_key(
                self._response_private_key, password=None, backend=default_backend())
        elif action == b"4":
            raise RequestFailed(data[2].decode())

    async def request(self, request):
        if isinstance(request, str):
            request_format = "str"
            request = request.encode()
        elif isinstance(request, dict) or isinstance(request, list):
            request_format = "json"
            request = json.dumps(request).encode()
        else:
            request_format = "bytes"
        reader, writer = await self.connect()
        request_key = Fernet.generate_key()
        f = Fernet(request_key)
        request = f.encrypt(request)
        request_key = self.request_public_key.encrypt(request_key, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        writer.write(
            f"1?{self.uuid}?{base64.b64encode(request_key).decode()}?{base64.b64encode(request).decode()}?{request_format}\r\n".encode())
        await writer.drain()
        await self.auth_challenge(reader, writer)
        data = await self.read(reader)
        if not data:
            return
        data = data.decode().split("?")
        action = data[0]
        if action == "3":
            response_key = self.response_private_key.decrypt(base64.b64decode(data[1]), padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
            f = Fernet(response_key)
            response = f.decrypt(base64.b64decode(data[2]))
            if data[3] == "str":
                response = response.decode()
            elif data[3] == "json":
                response = json.loads(response)
            return response
        else:
            raise RequestFailed(data[2])
    
    async def __call__(self, request):
        return await self.request(request)