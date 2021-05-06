ARG DOCKER_REGISTRY=quay.io
ARG DOCKER_REGISTRY_USERNAME=bgruening
ARG IMAGE_TAG=latest

FROM buildpack-deps:20.04 as galaxy_dependencies

ENV GALAXY_ROOT=/galaxy

FROM $DOCKER_REGISTRY/$DOCKER_REGISTRY_USERNAME/galaxy-container-base:$IMAGE_TAG as final

ENV DEBIAN_FRONTEND noninteractive

ENV GALAXY_USER=galaxy \
    GALAXY_GROUP=galaxy \
    GALAXY_UID=1450 \
    GALAXY_GID=1450 \
    GALAXY_HOME=/home/galaxy \
    GALAXY_ROOT=/galaxy

RUN groupadd -r $GALAXY_USER -g $GALAXY_GID \
    && useradd -u $GALAXY_UID -r -g $GALAXY_USER -d $GALAXY_HOME -c "Galaxy user" --shell /bin/bash $GALAXY_USER \
    && mkdir $GALAXY_HOME \
    && chown -R $GALAXY_USER:$GALAXY_USER $GALAXY_HOME

ENV EXPORT_DIR=/export \
    # Setting a standard encoding. This can get important for things like the unix sort tool.
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8


RUN apt update && apt install python3 git python3-pip python3-wheel python3-venv -y \
&&  pip3 install -U pip \
&& pip3 install planemo bioblend ephemeris parsec \
&& mkdir -p /export/galaxy/config \
&& touch /export/galaxy/config/reload_uwsgi.touchme \
&& update-alternatives --install /usr/bin/python python /usr/bin/python3 9 \
&& sh /usr/bin/common_cleanup.sh

COPY ./start.sh /usr/local/bin/start_tf_config.sh
COPY ./files/toolfactory /export/galaxy/tools/
COPY ./files/planemo_test /export/galaxy/tools/
COPY ./files/install-history.py /export/galaxy/config/
COPY ./files/datatypes_conf.xml /export/galaxy/config/
COPY ./files/tool_conf.xml /export/galaxy/config/
COPY ./files/job_conf.xml /export/galaxy/config/
RUN chown -R galaxy:galaxy /export/galaxy/tools /export/galaxy/config
USER galaxy
ENTRYPOINT /usr/local/bin/start_tf_config.sh
