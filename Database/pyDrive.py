from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import os

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

entries = os.listdir("../Tutanak/")
for entry in entries:
    if entry.endswith(".txt"):
        file = "../Tutanak/" + entry
        if os.path.getsize(file) != 0:
            f = drive.CreateFile({'title': entry})
            f.SetContentFile(os.path.join(file, entry))
            f.Upload()
            f = None
    break
