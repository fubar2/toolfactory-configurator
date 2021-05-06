# if a new ubuntu image, will need a port mapped and add some basics first
# apt update ; apt install -y python3-dev python3-venv python3-wheel nano curl wget git python3-setuptools
TARGDIR="/galaxy-central"
PDIR="/planemo"
git clone --recursive https://github.com/fubar2/planemo.git $PDIR
mkdir -p $TARGDIR
curl -L -s https://github.com/galaxyproject/galaxy/archive/dev.tar.gz | tar xzf - --strip-components=1 -C $TARGDIR
cd $PDIR
mkdir mytools
python3 -m venv .venv
. .venv/bin/activate
python3 setup.py build
python3 setup.py install
planemo conda_init --conda_prefix $PDIR/con
/planemo/con/bin/conda init
. ~/.bashrc
/planemo/con/bin/conda activate base
/planemo/con/bin/conda install -y -c bioconda -c conda-forge configparser galaxyxml
# without this, planemo does not work in docker... No clue why but planemo goes all pear shaped
# but pip reports that it's missing - installing it explicitly seems to do some kind of magic
echo "Starting first run. This takes ages and includes building the Galaxy client. Be patient. Do something else for 20 minutes"
. $PDIR/.venv/bin/activate
planemo tool_factory --galaxy_root $TARGDIR --port 9090 --host 0.0.0.0 --conda_dependency_resolution --conda_auto_install 
# planemo tool_factory --galaxy_root $TARGDIR --port 8080 --host 0.0.0.0 --conda_dependency_resolution --conda_auto_install 
#planemo tool_factory --galaxy_root $TARGDIR --conda_prefix $PDIR/con --port 9090 --host 0.0.0.0
# planemo serve --galaxy_root /galaxy-central/ --conda_prefix /planemo/con --port 8080 --host 0.0.0.0 --conda_dependency_resolution --conda_auto_install /planemo/.venv/lib/python3.8/site-packages/planemo-0.74.1-py3.8.egg/planemo_ext/tool_factory_2 
# planemo serve --galaxy_root /galaxy-central/ --port 8080 --host 0.0.0.0 --conda_dependency_resolution --conda_auto_install /planemo/.venv/lib/python3.8/site-packages/planemo-0.74.1-py3.8.egg/planemo_ext/tool_factory_2 
# planemo serve --galaxy_root $TARGDIR --port 8080 --host 0.0.0.0 --conda_dependency_resolution --conda_auto_install /usr/local/lib/python3.6/dist-packages/planemo-0.74.1-py3.6.egg/planemo_ext/tool_factory_2/

# host is needed to get -p 9090:9090 to work in docker. Default 127.0.0.1 doesn't redirect :(ls -l /tmp
