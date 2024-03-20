#!/usr/bin/python3
""" distributes an archive to 2 web servers """
from fabric.api import put, run, env, local
from os.path import exists
from datetime import datetime


env.hosts = ['18.207.3.99', '54.87.215.37']


def do_pack():
    """
        Generates archive file:

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


def do_deploy(archive_path=None):
    """ Upload/Deploy archive to  web servers and decompress """
    if exists(archive_path) is False:
        return False

    file_name = archive_path.split("/")[-1].split(".")[0]
    try:
        put(archive_path, "/tmp/")
        run('mkdir -p /data/web_static/releases/{}/'.format(file_name))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
            .format(file_name, file_name))
        run('rm /tmp/{}.tgz'.format(file_name))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}'.format(file_name, file_name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(file_name))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ \
            /data/web_static/current'.format(file_name))
        return True
    except TypeError:
        return False


def deploy():
    """ creates and distributes archive to servers """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
