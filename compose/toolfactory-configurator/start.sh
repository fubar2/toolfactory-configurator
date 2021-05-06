#!/bin/bash
sleep 30
/galaxy/tool_deps/_conda/bin/galaxy-wait -g http://nginx -v --timeout 120
echo "Galaxy is up! - start post startup configuration"
. /export/galaxy/.venv/bin/activate
pip3 install watchdog
deactivate
python /export/galaxy/config/install_history.py
touch "/export/galaxy/config/reload_uwsgi.touchme"
touch "/export/galaxy/config/tool_conf.xml"
