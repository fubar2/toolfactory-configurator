# Galaxy Docker Compose
This setup is built on the idea to use a basic docker-compose file and extend it
for additional use cases. Therefore the `docker-compose.yml` is the base of the
whole setup.
All working data (database, virtual environment, etc.) is exported in the
`EXPORT_DIR`, which defaults to ./export.


## Usage
### First startup
When starting the setup for the first time, the Galaxy container will copy
a bunch of files into the `EXPORT_DIR`. This might take quite some time
to finish (even 20 minutes or more). Please don't interrupt the setup in
this period, as this might result in a broken state of the `EXPORT_DIR`.

### Basic setup
Simply run

> docker-compose up

to start Galaxy. In the basic setup, Galaxy together with Nginx as the proxy,
Postgres as the DB, and RabbitMQ as the message queue is run.

The default username and password is "admin", "password" (API key "fakekey").
Those credentials are set at first run and can be tweaked using the environment
variables `GALAXY_DEFAULT_ADMIN_USER`, `GALAXY_DEFAULT_ADMIN_EMAIL`,
`GALAXY_DEFAULT_ADMIN_PASSWORD`, and `GALAXY_DEFAULT_ADMIN_KEY` in the
`docker-compose.yml` file. If you want to change the email address of an admin,
remember to update the `admin_users` setting of the Galaxy config (also
see [Configuration](#configuration) to learn how to configure Galaxy).

### Running in background
If you want to run the setup in the background, use the detach option (`-d`):

> docker-compose up -d

### Upgrading to a newer Galaxy version
When not setting `IMAGE_TAG` to a specific version, Docker-Compose will always
fetch the newest image and therefore Galaxy version available. Depending
on the magnitude of the upgrade, you may need to delete the virtual
environment of Galaxy (EXPORT_PATH/galaxy/.venv) before you start the
setup again. The DB migration depends on the `database_auto_migrate`
setting for Galaxy (which is not
set on default and will therefore be `false` normally).
