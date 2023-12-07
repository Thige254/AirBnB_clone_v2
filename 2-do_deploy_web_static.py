#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""

from fabric.api import run, put, env
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'  # I will later update with my username
env.key_filename = '/path/to/my/private/key'  # Since my laptop crashed and i
#do not have access to path, i will use fictional one.


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    Args:
        archive_path: Path to the archive file on the local machine
    Returns:
        True if successful, False otherwise
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Create the target directory
        run('mkdir -p /data/web_static/releases/{}'.format(
            archive_path.split('/')[1].split('.')[0]))

        # Uncompress the archive to the target directory
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(
            archive_path.split('/')[1], archive_path.split('/')[1].split('.')[0]))

        # Remove the uploaded archive
        run('rm /tmp/{}'.format(archive_path.split('/')[1]))

        # Move contents to proper location
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}'.format(
            archive_path.split('/')[1].split('.')[0], archive_path.split('/')[1].split('.')[0]))

        # Remove unnecessary directory
        run('rm -rf /data/web_static/releases/{}/web_static'.format(
            archive_path.split('/')[1].split('.')[0]))

        # Remove old symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{} /data/web_static/current'.format(
            archive_path.split('/')[1].split('.')[0]))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
