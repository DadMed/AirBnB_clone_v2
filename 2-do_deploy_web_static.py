#!/usr/bin/python3
# Fabfile to generates a .tgz archive from the contents of web_static.
import os.path
from datetime import datetime
from fabric.api import local, env, put, run


env.hosts = ['<IP web-01>', 'IP web-02']
env.user = '<username>'  # Replace <username> with your username


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


def do_deploy(archive_path):
    """Distribute an archive to web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        remote_path = "/tmp/{}".format(archive_name)
        release_path = "/data/web_static/releases/{}".format(
            archive_name.split('.')[0])

        put(archive_path, remote_path)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf {} -C {}".format(remote_path, release_path))
        run("rm {}".format(remote_path))
        run("mv {}/web_static/* {}".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))
        return True
    except Exception as e:
        return False

