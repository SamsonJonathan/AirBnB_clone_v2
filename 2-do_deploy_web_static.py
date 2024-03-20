#!/usr/bin/python3
""" distributes an archive to 2 web servers """
from fabric.api import put, run, env
from os.path import exists


env.hosts = ['	18.207.3.99', '	54.87.215.37']


def do_deploy(archive_path=None):
    """ Upload the archive to the /tmp/ directory of the web server """
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
