[![Build Status](https://travis-ci.org/Praisebetoscience/dockerhub-webhook.svg?branch=master)](https://travis-ci.org/Praisebetoscience/dockerhub-webhook)
[![Coverage Status](https://coveralls.io/repos/github/Praisebetoscience/dockerhub-webhook/badge.svg?branch=master)](https://coveralls.io/github/Praisebetoscience/dockerhub-webhook?branch=master)
[![Code Climate](https://codeclimate.com/github/Praisebetoscience/dockerhub-webhook/badges/gpa.svg)](https://codeclimate.com/github/Praisebetoscience/dockerhub-webhook)
[![Requirements Status](https://requires.io/github/Praisebetoscience/dockerhub-webhook/requirements.svg?branch=master)](https://requires.io/github/Praisebetoscience/dockerhub-webhook/requirements/?branch=master)

# dockerhub-webhook

Automatic container deployments from Dockerhub.

dockerhub-webhook listens to HTTP POST requests from dockerhub and triggers your scripts to update when a new container is available.  

## Features

* Supports Python 3.3+ 
* Lightweight - built on flask and gunicorn.
* Easy installation.
* supports unlimited number of triggers. 

## Installation

### Download Repository

    git clone https://github.com/Praisebetoscience/dockerhub-webhook.git


### Install dependencies

    pip install -r requirements/production.txt 

### Create config

    cp config.json.example config.json

### Generate API token

Create a new token, using openssl, pwgen or other tool

    pwgen 30 1

Save this token to either the `DOCHOOK_TOKEN` environmnt variable or in `config.json` as `apikey`.  `DOCHOOK_TOKEN` overrides `config.json`.  

### Configure scripts

Add scripts to `hooks` in `config.json`

    '<repo name>' : '/path/to/script'

Note: The repository name is the name of the container excluding the owner. (i.e. `owner/repo` is `repo`.)

### Start gunicorn

The prefered method for a production server is to start the server with gunicorn.  Running `wsgi.py` directly is for development because the auto-reloader and debug mode are both enabled.  A proxy such as nginx is recommended.  

    gunicorn wsgi:app -w 1 -b <host_ip>:<port>

### Configure Docker Hub

1. Go to https://hub.docker.com 
2. Click the repository you wish to autodeploy
3. Under the Webhooks tab add a webhook
4. Choose any name you please
5. For the Webhook URL use the following:

    http://<your_domain>:<port>/hubhook?key=<token>

Adjust this URL if proxied, such as eliminating the port or changing the endpoint.  

## Development 

### Install development requirements.  

    pip install -r requirements/development.txt  

### Tools 

* pytest
* flake8
* pylint


