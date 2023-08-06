"""
profiles.py is part of The SimpleTap Project.
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
import sys
import shutil
from pathlib import Path


class Profile:
    def __init__(self, name):
        self.name = name
        self.path = Path("profiles").resolve() / name
        sys.path.append(str(self.path / "path"))
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        try:
            shutil.rmtree(self.path / "tmp")
        except:
            pass
        if not os.path.isdir(self.path / "tmp"):
            os.makedirs(self.path / "tmp")
        if not os.path.isdir(self.path / "app_data"):
            os.makedirs(self.path / "app_data")
        if not os.path.isdir(self.path / "templates"):
            os.makedirs(self.path / "templates")
        if not os.path.isdir(self.path / "config"):
            os.makedirs(self.path / "config")
        if not os.path.isdir(self.path / "id"):
            os.makedirs(self.path / "id")
        if not os.path.isfile(self.path / "config" / "main.json"):
            with open(self.path / "config" / "main.json", "w") as f:
                json.dump({}, f)
        with open(self.path / "config" / "main.json", "r") as f:
            self.cfg = json.load(f)
        if not os.path.isfile(self.path / "tmp" / "main.json"):
            with open(self.path / "tmp" / "main.json", "w") as f:
                json.dump({}, f)
        with open(self.path / "tmp" / "main.json", "r") as f:
            self.tmp_cfg = json.load(f)

    def save_cfg(self):
        with open(self.path / "config" / "main.json", "w") as f:
            json.dump(self.cfg, f)

    def save_tmp_cfg(self):
        with open(self.path / "tmp" / "main.json", "w") as f:
            json.dump(self.tmp_cfg, f)

class ID:
    def __init__(self, profile):
        self.profile = profile
        self.path = profile.path / "id"

class MirrorProfile(Profile):
    def __init__(self, name, mirror):
        super().__init__(name)
        self.mirror = mirror
        for root, dirs, files in os.walk(self.mirror.path):
            for name in files:
                if not os.path.isfile(self.path / os.path.relpath(os.path.join(root, name), self.mirror.path)):
                    shutil.copy(os.path.join(root, name), self.path /
                                os.path.relpath(os.path.join(root, name), self.mirror.path))
                else:
                    with open(os.path.join(root, name), "rb") as f:
                        checksum = hashlib.md5(f.read()).hexdigest()
                    with open(self.path / os.path.relpath(os.path.join(root, name), self.mirror.path), "rb") as f:
                        checksum2 = hashlib.md5(f.read()).hexdigest()
                    if checksum != checksum2:
                        shutil.copy(os.path.join(
                            root, name), self.path / os.path.relpath(os.path.join(root, name), self.mirror.path))
            for name in dirs:
                if not os.path.isdir(self.path / os.path.relpath(os.path.join(root, name), self.mirror.path)):
                    shutil.copytree(os.path.join(
                        root, name), self.path / os.path.relpath(os.path.join(root, name), self.mirror.path))

with open("config.json") as f:
    profile_config = json.load(f)

profiles = {}
for profile in profile_config["profiles"]:
    if profile["mirror"]:
        profiles[profile["name"]] = MirrorProfile(profile["name"], profiles[profile["mirror_name"]])
    else:
        profiles[profile["name"]] = Profile(profile["name"])

current_profile = profiles[profile_config["current"]]