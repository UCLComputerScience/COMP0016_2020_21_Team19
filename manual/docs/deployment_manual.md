# Deploying Activity League

These instructions should be followed on a production server.

## Install Docker and Docker Compose by following the official instructions:

- Docker: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)
- Docker Compose: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

## Starting the web app

Create a new directory called `deploy` in the `$HOME` directory.

Copy the following [`docker-compose-production-example.yml`](docker-compose-production-example.yml) into `~/deploy/`.

This file manages all the images and containers that the app requires.

```yaml
version: "3.9"

services:
  db:
    image: postgres
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: {{ POSTGRES_USER }}
      POSTGRES_PASSWORD: {{ POSTGRES_PASSWORD }}
    volumes:
      - postgres_data:/var/lib/postgresql/data/
  web:
    image: docker.pkg.github.com/uclcomputerscience/comp0016_2020_21_team19/activityleague_web:latest
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DB_USER: {{ POSTGRES_USER }}
      DB_PASSWORD: {{ POSTGRES_PASSWORD }}
      DEBUG: "False"
      EMAIL_HOST: {{ MAILSERVER.COM }}
      EMAIL_HOST_PASSWORD: {{ EMAIL_HOST_PASSWORD }}
      EMAIL_HOST_USER: {{ EMAIL_HOST_USER }}
      GOOGLE_CLIENT_ID: {{ GOOGLE_CLIENT_ID }}
      GOOGLE_SECRET: {{ GOOGLE_SECRET }}
      SECRET_KEY: {{ SECRET_KEY }}
  watchtower: # optional
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /home/host/.docker/config.json:/config.json
    command: --interval 30
volumes:
  postgres_data:
```

This is an example `docker-compose.yml` that can be used on a production server.
The environment variables defined under the `web` service are used in `ActivityLeague/settings.py` and can be configured as your deployed instance requires.

The `watchtower` service is used to continuously check GitHub Packages for a newer build of the image and if it finds one, the new image is pulled and deployed. This service is optional

## Configuring the server to run Activity League on reboot

To run Activity League on server reboot automatically, create a file called `activity_league.service` in `/etc/systemd/system` and populate it with the following:

```ini
[Unit]
Description=Activity league docker compose deployment

[Service]
User={USERNAME}
Group=docker
WorkingDirectory=/home/{USERNAME}/deploy

ExecStartPre=/usr/local/bin/docker-compose pull --quiet
ExecStart=/usr/local/bin/docker-compose up

ExecStop=/usr/local/bin/docker-compose down

ExecReload=/usr/local/bin/docker-compose pull --quiet
ExecReload=/usr/local/bin/docker-compose down
ExecReload=/usr/local/bin/docker-compose up

[Install]
WantedBy=multi-user.target
```

Change `USERNAME` to whichever user is being used to deploy Activity League.

After you've copied this, save and close the file.

- Run `sudo systemctl daemon-reload` to allow the system to recognise the new service and once you've done this.
- Run `sudo systemctl enable activity_league` to ensure that the service runs automatically at startup.
- To get it up and running now, run `sudo systemctl activity_league start`.

## Manual Deployment

The steps described above will set up a continuous deployment workflow.

If this type of deployment is undesirable, you can simply omit the `watchtower` service from the `docker.compose.yml`.

The image running on the server can then be updated only by:

- SSH-ing into the server as the user being used to deploy Activity League.
- Navigating to `~/deploy`.
- Running `docker-compose down` to stop the web app.
- Running `docker-compose build` to rebuild the containers using the latest images.
- Running `docker-compose up -d` to run the web app on port 8000 in detached mode (i.e. in the background).