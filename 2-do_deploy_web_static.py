#!/usr/bin/python3
# This Fabric Script generates a .tgz archive.
import os
import sys
from fabric.api import local, env
from datetime import datetime


env.hosts = ['100.25.199.87', '54.144.223.92']
env.user = sys.argv
def do_deploy(archive_path):
    """Distributes archive to server
    Args:
        archive_path(str): path of .tgz archive
    Returns:
        True on sucess
        False on non existent file path
    """
    if os.isfile(archive_path) is False:
        return False
    split_path = archive_path.split("/")
    archive_name = split_path[-1]
    res1 = put(archive_path, "/tmp/{}".format(archive_name))
    split_arch_name = archive_name.split(".")
    name_min_exten = split_arch_name[0]
    res2 = run("tar -zxvf /tmp/{} -C /data/web_static/releases/{}/".format(archive_name, name_min_exten))
    res3 = run("rm /tmp/{}".format(archive_name))
    res4 = run("rm /data/web_static/current")
    res5 = run("ln -s -Ff /data/web_static/releases/{}/ /data/web_static/current".format(name_min_exten))
    if res1.failed:
        return False
    if res2.failed:
        return False
    if res3.failed:
        return False
    if res4.failed:
        return False
    if res5.failed:
        return False
    return True
