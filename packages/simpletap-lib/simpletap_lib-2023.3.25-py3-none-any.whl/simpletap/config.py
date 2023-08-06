"""
config.py is part of The SimpleTap Project.
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

import os
import json
from pathlib import Path
import datetime
import traceback
from simpletap import profiles

class config_file:
    def __init__(self, name):
        self.data = {}
        self.path = profiles.current_profile.path / "config"
        self.name = name
        if os.path.isfile(self.path / name):
            with open(self.path / name, "r") as f:
                self.data = json.load(f)
        if not os.path.isfile(self.path / "backups.json"):
            with open(self.path / "backups.json", "w+") as f:
                json.dump({}, f)
        with open(self.path / "backups.json", "r") as f:
            self.backups = json.load(f)
        if not os.path.isdir(self.path / "backups"):
            os.makedirs(self.path / "backups")
        if not name in self.backups:
            self.backups[name] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.path / "backups.json", "w+") as f:
                json.dump(self.backups, f, indent=4)
        if datetime.datetime.now() - datetime.datetime.strptime(self.backups[name], "%Y-%m-%d %H:%M:%S") > datetime.timedelta(days=0):
            with open(self.path / "backups" / f'{name}_{datetime.datetime.strptime(self.backups[name], "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d-%H%M%S")}.json', "w") as f:
                json.dump(self.data, f, indent=4)
            self.backups[name] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.path / "backups.json", "w+") as f:
                json.dump(self.backups, f, indent=4)
    def __getitem__(self, key):
        return self.data[str(key)]
    def __setitem__(self, key, value):
        self.data[str(key)] = value
        self.save()
    def __delitem__(self, key):
        del self.data[str(key)]
        self.save()
    def __iter__(self):
        return iter(self.data)
    def __len__(self):
        return len(self.data)
    def save(self):
        with open(self.path / self.name, "w") as f:
            json.dump(self.data, f, indent=4)
    def delete(self):
        os.remove(self.path)

class config:
    def __init__(self, load_all=False):
        self.path = profiles.current_profile.path / "config"
        self.cfgs = {}
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        if load_all:
            for file in os.listdir(self.path):
                if "backup" in file:
                    continue
                if os.path.isfile(self.path / file):
                    self.cfgs[file] = config_file(file)
    def save_all(self):
        for cfg in self.cfgs:
            self.cfgs[cfg].save()
    def __getitem__(self, key):
        if key not in self.cfgs:
            self.cfgs[key] = config_file(key)
        return self.cfgs[key]
    def __delitem__(self, key):
        self.cfgs[key].delete()

cfg = config(load_all=True)