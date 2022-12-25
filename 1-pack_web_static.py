#!/usr/bin/python3
# This Fabric Script generates a .tgz archive.
import os
from fabric.api import local
from datetime import datetime


def do_pack():
    """This function will create a .tgz archive"""
    local("mkdir -p versions/")
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(
            datetime.utcnow().year, datetime.utcnow().month,
            datetime.utcnow().day, datetime.utcnow().hour,
            datetime.utcnow().minute, datetime.utcnow().second)
    result = local("tar -cvzf {} web_static".format(file))
    if result.failed:
        return None
    else:
        return file
