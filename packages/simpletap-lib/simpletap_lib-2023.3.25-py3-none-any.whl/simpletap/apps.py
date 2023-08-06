"""
apps.py is part of The SimpleTap Project.
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
import multiprocessing
import os
import sys
import traceback
import uuid
import pathlib

from simpletap import resources, profiles

cfg = profiles.current_profile.cfg
tmp_cfg = profiles.current_profile.tmp_cfg

class Call:
        def __init__(self, extension_id):
            self.extension_id = extension_id
        async def __call__(self, func, *args, **kwargs):
            args = [str(arg) if isinstance(arg, os.PathLike) else arg for arg in args]
            kwargs = {key: str(value) if isinstance(value, os.PathLike) else value for key, value in kwargs.items()}
            while True:
                try:
                    reader, writer = await asyncio.open_connection(st.server[0], st.server[1])
                    break
                except:
                    print("Retrying connection to kernel...")
                    await asyncio.sleep(0.1)
            writer.write(
                f"{json.dumps({'app id': st.id, 'instance uuid': st.instance_uuid, 'extension id': self.extension_id, 'func': func, 'args': args, 'kwargs': kwargs})}\r\n".encode())
            await writer.drain()
            buff = b""
            while b'\r\n' not in buff:
                data = await reader.read(100)
                buff += data
            data, sep, buff = buff.partition(b'\r\n')
            result = json.loads(data.decode())
            writer.close()
            await writer.wait_closed()
            return result

class _AppConnector:
    def __init__(self, id, instance_uuid, server, instance_server, _uuid, _app, _app_tmp, _app_data, _profile, _Call):
        self.Call  = _Call
        self.uuid = _uuid
        self.app = _app
        self.app_tmp = _app_tmp
        self.app_data = _app_data
        self.profile = _profile
        self.server = server
        self.id = id
        self.instance_server = instance_server
        self.instance_uuid = instance_uuid
        self.signal_callbacks = {"start": "__start__", "end": sys.exit}
        self.callbacks = {}

    async def start(self):
        event_loop.create_task(st.start_instance_server())

    async def call(self, extension_id, func, args=[], kwargs={}):
        args = [str(arg) if isinstance(arg, os.PathLike) else arg for arg in args]
        kwargs = {key: str(value) if isinstance(value, os.PathLike) else value for key, value in kwargs.items()}
        while True:
            try:
                reader, writer = await asyncio.open_connection(self.server[0], self.server[1])
                break
            except:
                await asyncio.sleep(0.1)
        writer.write(
            f"{json.dumps({'app id': self.id, 'instance uuid': self.instance_uuid, 'extension id': extension_id, 'func': func, 'args': args, 'kwargs': kwargs})}\r\n".encode())
        await writer.drain()
        buff = b""
        while b'\r\n' not in buff:
            data = await reader.read(100)
            buff += data
        data, sep, buff = buff.partition(b'\r\n')
        result = json.loads(data.decode())
        writer.close()
        await writer.wait_closed()
        return result
    
    async def add_callback(self, name, func):
        while True:
            try:
                reader, writer = await asyncio.open_connection(self.server[0], self.server[1])
                break
            except:
                await asyncio.sleep(0.1)
        try:
            writer.write(
                f"{json.dumps({'app id': self.id, 'instance uuid': self.instance_uuid, 'add callback': name})}\r\n".encode())
            await writer.drain()
        except:
            return
        self.callbacks[name] = func

    async def handle_instance_server(self, reader, writer):
        buff = b""
        while b'\r\n' not in buff:
            data = await reader.read(100)
            buff += data
        data, sep, buff = buff.partition(b'\r\n')
        data = json.loads(data.decode())
        if "action" in data:
            if data["action"] == "start":
                if isinstance(self.signal_callbacks["start"], str):
                    try:
                        self.signal_callbacks["start"] = globals(
                        )[self.signal_callbacks["start"]]
                    except:
                        print("Failed to get function")
                        traceback.print_exc()
                await self.try_call(self.signal_callbacks["start"])
            elif data["action"] == "end":
                if isinstance(self.signal_callbacks["end"], str):
                    try:
                        self.signal_callbacks["end"] = globals()[
                            self.signal_callbacks["end"]]
                    except:
                        print("Failed to get function")
                        traceback.print_exc()
                await self.try_call(self.signal_callbacks["end"])
        elif "signal" in data:
            if data["signal"] in self.signal_callbacks:
                self.signal_callbacks[data["signal"]]()
        elif "callback" in data:
            if data["callback"] in self.callbacks:
                await self.try_call(self.callbacks[data["callback"]], data["args"], data["kwargs"])
    async def try_call(self, func, args=None, kwargs=None):
        try:
            if asyncio.iscoroutinefunction(func):
                if args in ([], (), None):
                    return await func()
                elif kwargs in ({}, None):
                    return await func(*args)
                else:
                    return await func(*args, **kwargs)
            else:
                if args in ([], (), None):
                    return func()
                elif kwargs in ({}, None):
                    return func(*args)
                else:
                    return func(*args, **kwargs)
        except Exception as e:
            print(repr(e))

    async def start_instance_server(self):
        _instance_server = await asyncio.start_server(self.handle_instance_server, self.instance_server[0], self.instance_server[1])
        addrs = ', '.join(str(sock.getsockname())
                          for sock in _instance_server.sockets)
        async with _instance_server:
            await _instance_server.serve_forever()

    def set_signal_callback(self, signal, func):
        self.signal_callbacks[signal] = func


class _AppInstance:
    def __init__(self, id):
        self.id = id
        self.server = (tmp_cfg["arch"]["server_ip"],
                       tmp_cfg["arch"]["kernel_port"])
        self.instance_uuid = str(uuid.uuid4())
        tmp_cfg["instances"] = {}
        tmp_cfg["instances"][self.instance_uuid] = {}
        tmp_cfg["instances"][self.instance_uuid]["port"] = resources.find_free_port()
        self.host = tmp_cfg["arch"]["server_ip"]
        self.port = tmp_cfg["instances"][self.instance_uuid]["port"]
        with open(profiles.current_profile.path / "tmp" / "main.json", "w") as f:
            json.dump(cfg, f)

    def load(self):
        try:
            with open(f"{profiles.current_profile.path}/apps/{self.id}/__init__.py", "r") as f:
                self.code = f.read()
            self.bytecode = compile(
                self.code, f"{profiles.current_profile.path}/apps/{self.id}/__init__.py", "exec")
            if not os.path.exists(f"{profiles.current_profile.path}/tmp/apps/{self.instance_uuid}"):
                os.makedirs(
                    f"{profiles.current_profile.path}/tmp/apps/{self.instance_uuid}")
            return self
        except BaseException as e:
            print(traceback.format_exc())
            return repr(e)

    def _run(self, _bytecode, instance_uuid, _Call):
        _uuid = instance_uuid
        _app = pathlib.Path(f"{profiles.current_profile.path}/apps/{self.id}")
        _app_tmp = pathlib.Path(f"{profiles.current_profile.path}/tmp/apps/{self.instance_uuid}")
        _app_data = pathlib.Path(f"{profiles.current_profile.path}/app_data/{self.id}")
        _profile = pathlib.Path(profiles.current_profile.path)
        if not os.path.isdir(str(_app_data)):
            os.makedirs(str(_app_data))
        os.chdir(str(_app_data))
        sys.path.append(str(_app))
        global event_loop
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        global st
        st = _AppConnector(self.id, self.instance_uuid, self.server,
                           ("127.0.0.1", tmp_cfg["instances"][self.instance_uuid]["port"]), _uuid, _app, _app_tmp, _app_data, _profile, _Call)
        event_loop.create_task(st.start())
        exec(_bytecode, globals())
        event_loop.run_forever()

    async def start(self):
        while True:
            try:
                reader, writer = await asyncio.open_connection(tmp_cfg["arch"]["server_ip"], tmp_cfg["instances"][self.instance_uuid]["port"])
                writer.write('{"action": "start"}\r\n'.encode())
                await writer.drain()
                writer.close()
                break
            except:
                await asyncio.sleep(0.1)

    async def end(self):
        while True:
            try:
                reader, writer = await asyncio.open_connection(tmp_cfg["arch"]["server_ip"], tmp_cfg["instances"][self.instance_uuid]["port"])
                writer.write('{"action": "end"}\r\n'.encode())
                await writer.drain()
                writer.close()
                break
            except:
                await asyncio.sleep(0.1)

    def run(self):
        self.process = multiprocessing.Process(
            target=self._run, args=(self.bytecode, self.instance_uuid, Call))
        self.process.start()
        return self


class App:
    def __init__(self, id):
        self.id = id
        self.instances = {}
        with open(f"{profiles.current_profile.path}/apps/{self.id}/info.json", "r") as f:
            self.info = json.load(f)

    def create_new_instance(self):
        instance = _AppInstance(self.id)
        self.instances[instance.instance_uuid] = instance
        return instance

    def create_instance(self):
        if not len(self.instances) >= 1:
            return self.create_new_instance()
        return self.instances[list(self.instances.keys())[0]]

    def run_instance(self):
        return self.create_instance().load().run()

    def run_new_instance(self):
        return self.create_new_instance().load().run()

    async def end_all_instances(self):
        for instance in self.instances:
            await instance.end()
        self.instances = []


class AppManager:
    def __init__(self, server=None):
        self.server = server
        if self.server == None:
            self.server = (tmp_cfg["arch"]["server_ip"],
                           tmp_cfg["arch"]["appmanager_port"])
        self.apps = {}
        self.load_apps()

    def load_apps(self):
        for app in os.listdir(f"{profiles.current_profile.path}/apps"):
            if os.path.isdir(f"{profiles.current_profile.path}/apps/{app}"):
                self.apps[app] = App(app)
                
    async def handle(self, reader, writer):
        buff = b""
        while b'\r\n' not in buff:
            data = await reader.read(100)
            buff += data
        data, sep, buff = buff.partition(b'\r\n')
        data = json.loads(data.decode())
        if not "app" in data or "action" not in data:
            writer.write({"error": "no app or action specified"})
            await writer.drain()
            return
        result = getattr(self.apps[data["app"]], data["action"])()
        writer.write(result.id)
        await writer.drain()
    
    async def _context_mngr_server(self):
        async with self._server:
            await self._server.serve_forever()
    
    async def start_server(self):
        self._server = await asyncio.start_server(self.handle, self.server[0], self.server[1])
        addrs = ', '.join(str(sock.getsockname())
                          for sock in self._server.sockets)
        self.kernel_server_task = asyncio.create_task(
            self._context_mngr_server())
        return self