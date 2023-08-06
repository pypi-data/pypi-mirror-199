"""
package_manager.py is part of The SimpleTap Project.
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

import hashlib
import json
import os
import asyncio
import datetime
from simpletap import profiles

cfg = profiles.current_profile.cfg
tmp_cfg = profiles.current_profile.tmp_cfg

class PackageLists:
    def __init__(self):
        pass
    def load_package_lists(self):
        if not os.path.exists(f"{profiles.current_profile.path}/package_lists"):
            os.makedirs(f"{profiles.current_profile.path}/package_lists")
        package_lists = {}
        for file in os.listdir(f"{profiles.current_profile.path}/package_lists"):
            if file.endswith(".jsonl"):
                with open(f"{profiles.current_profile.path}/package_lists/{file}", "r") as f:
                    package_lists[file[:-5]] = {}
                    for line in f:
                        package = json.loads(line)
                        package_lists[file[:-5]][package["id"]] = package
        return package_lists
    async def update_package_lists(self):
        errors = []
        package_lists = self.load_package_lists()
        for package_list in package_lists:
            if not "__package_list__" in package_lists[package_list]:
                continue
            if not "server" in package_lists[package_list]["__package_list__"]:
                continue
            package_list_version = datetime.datetime.strptime(package_lists[package_list]["__package_list__"]["version"], "%Y-%m-%d")
            try:
                reader, writer = await asyncio.open_connection(package_lists[package_list]["__package_list__"]["server"][0], package_lists[package_list]["__package_list__"]["server"][1])
            except BaseException as e:
                errors.append(repr(e))
                continue
            writer.write('{"action": "get_package_list_version", "package_list": "%s"}\r\n' % package_list["__package_list__"]["name"])
            await writer.drain()
            buff = b''
            while b'\r\n' not in buff:
                data = await reader.read(1)
                if not data:
                    break
                buff += data
            data, sep, buff = buff.partition(b'\r\n')
            data = json.loads(data.decode())
            if data["status"] == "success":
                latest_package_list_version = datetime.datetime.strptime(data["version"], "%Y-%m-%d")
            else:
                errors.append(data["error"])
                continue
            if latest_package_list_version <= package_list_version:
                continue
            writer.write('{"action": "get_package_list", "package_list": "%s"}\r\n' % package_list)
            await writer.drain()
            buff = b''
            while b'\r\n' not in buff:
                data = await reader.read(1)
                if not data:
                    break
                buff += data
            data, sep, buff = buff.partition(b'\r\n')
            data = json.loads(data.decode())
            if data["status"] == "success":
                if os.path.exists(f"{profiles.current_profile.path}/package_lists/{package_list}.jsonl"):
                    os.rename(f"{profiles.current_profile.path}/package_lists/{package_list}.jsonl", f"{profiles.current_profile.path}/package_lists/{package_list}_{package_lists[package_list]['__package_list__']['version']}.jsonl")
                with open(f"{profiles.current_profile.path}/package_lists/{package_list}.jsonl", "w") as f:
                    for package in data["packages"]:
                        f.write(json.dumps(package) + '\n')
            else:
                errors.append(data["error"])
                continue
            sha256 = hashlib.sha256()
            with open(f"{profiles.current_profile.path}/package_lists/{package_list}.jsonl", "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256.update(chunk)
            if sha256.hexdigest() != data["hash"]:
                errors.append("Hash mismatch")
                continue
            writer.close()
        if len(errors) > 0:
            return errors
        return True