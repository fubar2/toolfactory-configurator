#!/bin/bash
# seem to need a delay here
# needs changes to base_config.yml to enable master and touch-reload on uwsgi and watchdog: auto for galaxy
/usr/bin/sleep 30s
echo "slept well.."
DONEONCE="0"
if [ -f "/export/galaxy/tools/toolfactory/ToolFactory.xml" ]; then
  DONEONCE="1"
  echo "configurator found the toolfactory already present so not installing anything"
else
  echo "configurator found no toolfactory - loading sample history and overwriting configs as needed"
  chown -R galaxy:galaxy /config
  chown -R galaxy:galaxy /tools
  chown galaxy:galaxy /welcome.html
  sudo -H -u galaxy bash -c 'cp -r /tools/* /export/galaxy/tools/'
  sudo -H -u galaxy bash -c 'cp -r /config/* /export/galaxy/config/'
  sudo -H -u galaxy bash -c 'cp /welcome.html /export/galaxy/static/welcome.html'
  sudo -H -u galaxy bash -c '. /export/galaxy/.venv/bin/activate ; python3 -m pip install -U pip; python3 -m pip install watchdog ; deactivate'
  touch /export/galaxy/config/reload_uwsgi.touchme
  chown galaxy:galaxy /export/galaxy/config/reload_uwsgi.touchme
  sleep 10s
  echo "configurator is installing the demonstration history"
  sudo -H -u galaxy bash -c '. /venv/bin/activate ; python3 /config/install-history.py ; deactivate'
fi
# run toolwatcher watchdog to trigger planemo tests when requested by toolfactory
export HOME="$PLANEMO_ROOT"
touch /export/galaxy/toolwatcher.log
chown galaxy:galaxy /export/galaxy/toolwatcher.log
cd /export/galaxy ; sudo -H -u galaxy bash -c ". /venv/bin/activate ; python3 /usr/local/bin/toolwatcher.py"
