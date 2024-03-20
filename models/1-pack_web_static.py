#!/usr/bin/python3
"""
    Fabric script that generates a .tgz archive from the
    contents of the web_static folder
"""

from datetime import datetime
from fabric.api import local


def do_pack():
    """
        # All files in the folder web_static must be added to the final archive

        # All archives must be stored in the folder versions
         (your function should create this folder if it doesn’t exist)

        # The name of the archive created must be:
         web_static_<year><mont><day><hour><mnute><second>.tgz
    """
    date_time = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        file_name = "versions/web_static_{}.tgz".format(date_time)
        local("tar -cvzf {} web_static/".format(file_name))
        return file_name
    except TypeError:
        return None
