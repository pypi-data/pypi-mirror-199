"""
handlers.py is part of The SimpleTap Project.
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
import copy
#from bson import json_util

class BaseHandler:
    def __call__(self, user, request):
        self.user = user
        self.request = request
        if not self.user.status["state"] == "active":
            return {"error": "user not active"}
        return self.handle(user, request)
    def handle(self, user, request):
        pass

class ModuleHandler(BaseHandler):
    def __init__(self, modules):
        self.modules = modules
    def __call__(self, user, request):
        super().__call__(user, request)
        return self._handle(user, request)
    def _handle(self, user, request):
        if not "module" in request:
            return {"error": "Module not specified"}
        else:
            return self.modules[request["module"]].handler(user, request)