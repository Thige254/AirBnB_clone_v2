#!/usr/bin/python3
"""
Fabric script to generate a .tgz archive from the contents of web_static folder
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder
    Returns:
        Archive path if successful, None otherwise
    """
    try:
        # Create versions folder if it doesn't exist
        local("mkdir -p versions")

        # Generate archive path
        time_format = "%Y%m%d%H%M%S"
        archive_name = "web_static_{}.tgz".format(datetime.utcnow().strftime(time_format))
        archive_path = "versions/{}".format(archive_name)

        # Compress web_static folder
        local("tar -cvzf {} web_static".format(archive_path))

        return archive_path
    except Exception as e:
        return None
