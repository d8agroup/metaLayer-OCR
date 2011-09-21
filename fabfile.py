from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['root@ml.stage.ocr.01']

def staging():
    with cd('/usr/local/metaLayer-ocr'):
        run("git pull")
        run("git status")
    run("service apache2 restart")