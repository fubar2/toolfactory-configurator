
# container with planemo with a galaxy dist for it to use
# triggered by watchdog when a .testme file is written to anything in /export/galaxy/tools/*
# planemo does not play nicely when run as a tool....
ARG DOCKER_REGISTRY=quay.io
ARG DOCKER_REGISTRY_USERNAME=bgruening
ARG IMAGE_TAG=latest
FROM $DOCKER_REGISTRY/$DOCKER_REGISTRY_USERNAME/galaxy-container-base:$IMAGE_TAG as final


ARG GALAXY_RELEASE="release_21.01"
ARG GALAXY_REPO="https://github.com/galaxyproject/galaxy"
ARG GALAXY_ROOT="/galaxy-central"

ENV DEBIAN_FRONTEND noninteractive

ENV GALAXY_USER=galaxy \
    GALAXY_GROUP=galaxy \
    GALAXY_UID=1450 \
    GALAXY_GID=1450 \
    GALAXY_HOME=/home/galaxy \
    GALAXY_ROOT=/galaxy-central \
    PLANEMO_ROOT=$GALAXY_ROOT/planemo

RUN groupadd -r $GALAXY_USER -g $GALAXY_GID \
    && useradd -u $GALAXY_UID -r -g $GALAXY_USER -d $GALAXY_HOME -c "Galaxy user" --shell /bin/bash $GALAXY_USER \
    && mkdir -p $GALAXY_HOME \
    && mkdir -p $PLANEMO_ROOT \
    && apt update && apt install python3 git python3-pip python3-wheel python3-venv git nano curl sudo -y \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3 9 \
    && mkdir -p "$GALAXY_ROOT" \
    && curl -L -s $GALAXY_REPO/archive/$GALAXY_RELEASE.tar.gz | tar xzf - --strip-components=1 -C $GALAXY_ROOT



COPY ./files/toolfactory /tools/toolfactory
COPY ./files/planemo_test /tools/planemo_test
COPY ./files/tacrev /tools/tacrev
COPY ./files/install-history.py /config/
COPY ./files/datatypes_conf.xml /config/
COPY ./files/tool_conf.xml /config/
COPY ./files/toolfactory/welcome.html /welcome.html
# for galaxy container
COPY ./files/datatypes_conf.xml $GALAXY_ROOT/config/


RUN python3 -m venv $GALAXY_ROOT/.venv \
&& python3 -m venv /venv \
&& . /venv/bin/activate \
&& pip3 install -U pip \
&& pip3 install planemo bioblend ephemeris parsec requests wheel watchdog \
&& mkdir -p /export/galaxy/config \
&& touch /export/galaxy/config/reload_uwsgi.touchme \
&& export HOME="$PLANEMO_ROOT" \
&& planemo conda_init --conda_prefix $PLANEMO_ROOT/con \
&& planemo test --conda_prefix "$PLANEMO_ROOT/con" --galaxy_root $GALAXY_ROOT "/tools/tacrev/tacrev.xml" \
&& apt-get clean && apt-get purge \
&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
&& chown -R $GALAXY_USER:$GALAXY_USER $GALAXY_HOME \
&& chown -R $GALAXY_USER:$GALAXY_USER $GALAXY_ROOT

COPY ./start.sh /usr/local/bin/start_tf_config.sh
COPY ./files/toolwatcher.py /usr/local/bin/toolwatcher.py
#COPY ./files/job_conf.xml /config/
# if overwrite of default wanted?

ENTRYPOINT /usr/local/bin/start_tf_config.sh
