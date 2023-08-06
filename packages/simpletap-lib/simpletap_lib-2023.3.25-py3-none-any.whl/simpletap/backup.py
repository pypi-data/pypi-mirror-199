"""
backup.py is part of The SimpleTap Project.
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

import datetime
import zipfile

try:
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    from oauth2client.client import GoogleCredentials
except ImportError:
    pydrive = None
try:
    from dropbox import Dropbox
    from dropbox.files import WriteMode
except ImportError:
    dropbox = None
try:
    from mega import Mega
except ImportError:
    mega = None

from simpletap import profiles


def backup_to_disk():
    with zipfile.ZipFile(profiles.current_profile.path / "backups" / f"{profiles.current_profile.name}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.zip", "w") as z:
        for file in profiles.current_profile.path.rglob("*"):
            if file.is_file():
                z.write(file, file.relative_to(profiles.current_profile.path))
    return profiles.current_profile.path / "backups" / f"{profiles.current_profile.name}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.zip"


def backup_to_gdrive():
    if not pydrive:
        raise ImportError("pydrive is not installed")
    backup_file = backup_to_disk()
    gauth = GoogleAuth()
    gauth.credentials = GoogleCredentials(
        profiles.current_profile.config["gdrive"]["token"])
    drive = GoogleDrive(gauth)
    if not drive.ListFile({'q': "title='SimpleTap Backups' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList():
        folder = drive.CreateFile(
            {'title': 'SimpleTap Backups', 'mimeType': 'application/vnd.google-apps.folder'})
        folder.Upload()
    file = drive.CreateFile({'title': backup_file.name, 'parents': [{'id': drive.ListFile(
        {'q': "title='SimpleTap Backups' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()[0]['id']}]})
    file.SetContentFile(backup_file)
    file.Upload()
    backup_file.unlink()
    return file['id']


def backup_to_dropbox():
    if not dropbox:
        raise ImportError("dropbox is not installed")
    backup_file = backup_to_disk()
    dbx = Dropbox(profiles.current_profile.config["dropbox"]["token"])
    with open(backup_file, "rb") as f:
        dbx.files_upload(
            f.read(), f"/SimpleTap Backups/{backup_file.name}", mode=WriteMode('overwrite'))
    backup_file.unlink()
    return dbx.sharing_create_shared_link(f"/SimpleTap Backups/{backup_file.name}")['url']


def backup_to_mega():
    if not mega:
        raise ImportError("mega is not installed")
    backup_file = backup_to_disk()
    m = Mega()
    m.login(profiles.current_profile.config["mega"]["email"],
            profiles.current_profile.config["mega"]["password"])
    m.upload(backup_file)
    backup_file.unlink()
    return m.get_upload_link(backup_file.name)
