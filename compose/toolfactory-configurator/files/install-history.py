
#!/usr/bin/python

import argparse
import os
import requests
import time

from bioblend import galaxy


def _parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--galaxy", help='URL of target galaxy', default="http://nginx")
    parser.add_argument("-k", "--key", help='Galaxy admin key', default="fakekey")
    parser.add_argument("-e", "--email", help='admin email of target galaxy', default="admin@galaxy.org")
    parser.add_argument("-p", "--password", help='Galaxy admin password', default="password")
    parser.add_argument("-i", "--history_path", help='Path to history gz files to be loaded', default="/export/galaxy/tools/toolfactory/TF_demo_history_May4.tar.gz")
    #parser.add_argument("-t", "--toolid", help='tool(s) to install dependencies', default=["rgtf2","planemo_test"], action="append")
    parser.add_argument("-t", "--toolid", help='tool(s) to install dependencies', default=[], action="append")
    return parser

import requests


def main():
    """
    load a folder of histories or a single gz
    """
    args = _parser().parse_args()
    if args.key:
        connected = False
        while not connected:
            try:
                gi = galaxy.GalaxyInstance(url=args.galaxy, key=args.key)
                connected = True
            except Exception:
                print('install-history: No gi yet...')
                time.sleep(1)
    hdir = args.history_path
    if os.path.isdir(hdir):
        for fp in os.listdir(hdir):
            hp = os.path.join(hdir,fp)
            if os.path.isfile(hp):
                x = gi.histories.import_history(file_path=hp, url=None)
                print('installed ',hp,'res=',x)
    else:
        x = gi.histories.import_history(file_path=hdir, url=None)
        print('installed',hdir,'res=',x)
    for tfid in args.toolid:
        x = gi.tools.install_dependencies(tfid)
        print('installed', tfid, 'dependencies, res=',x)


if __name__ == "__main__":
    main()

