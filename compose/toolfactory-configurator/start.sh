#!/bin/bash
/export/tool_deps/_conda/bin/galaxy-wait -g http://nginx -v --timeout 120
echo "Galaxy is up! - start post startup configuration"
. /galaxy/.venv/bin/activate
pip3 install watchdog
deactivate
python /usr/local/bin/install_history.py
touch "/galaxy/reload_uwsgi.touchme"
touch "/galaxy/config/tool_conf.xml"
