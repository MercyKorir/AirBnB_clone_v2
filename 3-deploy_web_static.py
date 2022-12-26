#!/usr/bin/python3
# This Fabric Script generates a .tgz archive.
import os.path
import os
from fabric.api import env, run, put, local
from datetime import datetime


env.hosts = ["100.25.199.87", "54.144.223.92"]


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


def do_deploy(archive_path):
    """Distributes archive to server
    Args:
        archive_path(str): path of .tgz archive
    Returns:
        True on sucess
        False on non existent file path
    """
    if os.path.isfile(archive_path) is False:
        return False
    split_path = archive_path.split("/")
    archive_name = split_path[-1]
    res1 = put(archive_path, "/tmp/{}".format(archive_name))

    split_arch_name = archive_name.split(".")
    name_min_exten = split_arch_name[0]

    res7 = run("mkdir -p /data/web_static/releases/{}/".format(name_min_exten))

    res2 = run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
        archive_name, name_min_exten))

    res3 = run("rm /tmp/{}".format(archive_name))

    mv_file = '/data/web_static/releases/{}'.format(name_min_exten)

    res8 = run("mv {}/web_static/* {}/".format(mv_file, mv_file))

    res9 = run("rm -rf /data/web_static/releases/{}/web_static".format(
        name_min_exten))

    res4 = run("rm -rf /data/web_static/current")

    link_name = "/data/web_static/current"
    res5 = run("ln -s /data/web_static/releases/{}/ {}".format(
        name_min_exten, link_name))

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
    if res7.failed:
        return False
    if res8.failed:
        return False
    if res9.failed:
        return False
    return True


def deploy():
    """Distributes archive to server
    Returns:
        True on sucess
        False on non existent file path
    """
    arch_pathname = do_pack()
    if arch_pathname is None:
        return False
    ret_val = do_deploy(arch_pathname)
    return ret_val
