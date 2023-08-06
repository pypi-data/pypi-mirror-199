"""
kernel.py is part of The SimpleTap Project.
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
import pathlib
import os

from simpletap import profiles
from simpletap.apps import Call
from simpletap.resources import module_from_file

cfg = profiles.current_profile.cfg
tmp_cfg = profiles.current_profile.tmp_cfg

class Kernel:
    def __init__(self, app_mngr, server=None):
        self.server = server
        self.app_mngr = app_mngr
        if self.server == None:
            self.server = (tmp_cfg["arch"]["server_ip"],
                           tmp_cfg["arch"]["kernel_port"])
        self.extensions = {}
        self.callback_registrations = {}

    async def load_extensions(self):
        for extension in profiles.current_profile.path.glob("extensions/*"):
            if extension.name.endswith(".py"):
                extension_id = "".join(extension.name.rsplit(".py", 1))
            else:
                extension_id = extension.name
            if extension_id in cfg["extensions"]["disabled"]:
                continue
            if not os.path.exists(profiles.current_profile.path / "tmp" / extension_id):
                os.mkdir(profiles.current_profile.path / "tmp" / extension_id)
            if not os.path.exists(profiles.current_profile.path / "ext_data" / extension_id):
                os.mkdir(profiles.current_profile.path / "ext_data" / extension_id)
            extension_data = profiles.current_profile.path / "ext_data" / extension_id
            extension_dir = profiles.current_profile.path / "extensions" / extension_id
            self.extensions[extension_id] = {}
            if (profiles.current_profile.path / "extensions" / extension_id / "info.json").exists():
                with open(profiles.current_profile.path / "extensions" / extension_id / "info.json") as f:
                    self.extensions[extension_id]["info"] = json.load(f)
            else:
                self.extensions[extension_id]["info"] = {}
            if "new_process" not in self.extensions[extension_id]["info"]:
                self.extensions[extension_id]["info"]["new_process"] = False
            if self.extensions[extension_id]["info"]["new_process"] == True:
                pass
            connector = KernelExtensionConnector(extension_id, self, cfg, tmp_cfg, profiles.current_profile.path, asyncio.get_event_loop(), self.server, self.app_mngr, extension_data, extension_dir)
            self.extensions[extension_id] = {"connector": connector}
            self.extensions[extension_id]["mod"] = module_from_file(extension_id, profiles.current_profile.path / "extensions" / extension_id / "__init__.py")
            self.extensions[extension_id]["mod"].st = connector
            if hasattr(self.extensions[extension_id]["mod"], "main"):
                if asyncio.iscoroutinefunction(self.extensions[extension_id]["mod"].main):
                    self.extensions[extension_id]["main_task"] = asyncio.create_task(
                        self.extensions[extension_id]["mod"].main())
                else:
                    self.extensions[extension_id]["main_task"] = asyncio.create_task(
                        asyncio.to_thread(self.extensions[extension_id]["mod"].main))

    async def handle(self, reader, writer):
        buff = b""
        while b'\r\n' not in buff:
            data = await reader.read(100)
            buff += data
        data, sep, buff = buff.partition(b'\r\n')
        data = json.loads(data.decode())
        if data["app id"] not in self.app_mngr.apps:
            return
        if data["instance uuid"] not in self.app_mngr.apps[data["app id"]].instances:
            return
        if "extension id" in data:
            if data["extension id"] not in self.extensions:
                return
            if "func" not in data:
                return
            if data["func"] not in self.extensions[data["extension id"]]["mod"].funcs:
                return
            if asyncio.iscoroutinefunction(self.extensions[data["extension id"]]["mod"].funcs[data["func"]]):
                result = await self.extensions[data["extension id"]]["mod"].funcs[data["func"]](*data["args"], **data["kwargs"])
            else:
                result = self.extensions[data["extension id"]]["mod"].funcs[data["func"]](*data["args"], **data["kwargs"])
            try:
                result = json.dumps(result)
            except:
                result = json.dumps(str(result))
            writer.write(result.encode() + b'\r\n')
        elif "add callback" in data:
            if data["add callback"] not in self.callback_registrations:
                if data["add callback"] not in self.callback_registrations:
                    self.callback_registrations[data["add callback"]] = []
                self.callback_registrations[data["add callback"]].append(
                    (data["app id"], data["instance uuid"]))
        elif "remove callback" in data:
            if data["remove callback"] in self.callback_registrations:
                if (data["app id"], data["instance uuid"]) in self.callback_registrations[data["remove callback"]]:
                    self.callback_registrations[data["remove callback"]].remove(
                        (data["app id"], data["instance uuid"]))
        writer.close()
        await writer.wait_closed()

    async def _context_mngr_server(self):
        async with self._server:
            await self._server.serve_forever()

    async def start(self):
        await self.load_extensions()
        self._server = await asyncio.start_server(self.handle, self.server[0], self.server[1])
        addrs = ', '.join(str(sock.getsockname())
                          for sock in self._server.sockets)
        self.kernel_server_task = asyncio.create_task(
            self._context_mngr_server())
        return self


class KernelExtensionConnector:
    def __init__(self, id, kernel, cfg, tmp_cfg, profile, event_loop, server, app_mngr, ext_data, ext_dir):
        self.event_loop = event_loop
        self.server = server
        self.Call = Call
        self.id = id
        self.instance_uuid = "0"
        self.kernel = kernel
        self.cfg = cfg
        self.tmp_cfg = tmp_cfg
        self.app_manager = app_mngr
        self.profile = pathlib.Path(profile)
        self.ext_data = ext_data
        self.ext_dir = ext_dir

    async def call_callback(self, callback_name, *args, **kwargs):
        if callback_name not in self.kernel.callback_registrations:
            return
        for app_id, instance_uuid in self.kernel.callback_registrations[callback_name]:
            if app_id not in self.kernel.app_mngr.apps:
                continue
            if instance_uuid not in self.kernel.app_mngr.apps[app_id].instances:
                continue
            instance_host = self.kernel.app_mngr.apps[app_id].instances[instance_uuid].host
            instance_port = self.kernel.app_mngr.apps[app_id].instances[instance_uuid].port
            while True:
                try:
                    reader, writer = await asyncio.open_connection(instance_host, instance_port)
                    break
                except:
                    print("Connection issues")
                    await asyncio.sleep(0.1)
            writer.write(json.dumps(
                {"callback": callback_name, "args": args, "kwargs": kwargs}).encode() + b'\r\n')
            await writer.drain()
            writer.close()
            await writer.wait_closed()
