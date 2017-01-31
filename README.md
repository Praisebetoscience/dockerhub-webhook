[![Build Status](https://travis-ci.org/Praisebetoscience/dockerhub-webhook.svg?branch=master)](https://travis-ci.org/Praisebetoscience/dockerhub-webhook)
[![Coverage Status](https://coveralls.io/repos/github/Praisebetoscience/dockerhub-webhook/badge.svg?branch=master)](https://coveralls.io/github/Praisebetoscience/dockerhub-webhook?branch=master)
[![Code Climate](https://codeclimate.com/github/Praisebetoscience/dockerhub-webhook/badges/gpa.svg)](https://codeclimate.com/github/Praisebetoscience/dockerhub-webhook)
[![Requirements Status](https://requires.io/github/Praisebetoscience/dockerhub-webhook/requirements.svg?branch=master)](https://requires.io/github/Praisebetoscience/dockerhub-webhook/requirements/?branch=master)

# dockerhub-webhook

Automatic container deployments from Dockerhub.

dockerhub-webhook listens to HTTP POST requests from dockerhub and triggers your scripts to update when a new container is available.  

## Features

* Supports Python 3.3+ 
* Can be installed using pip
* Lightweight - built using [Flask](http://flask.pocoo.org/).
* Supports unlimited number of triggers. 
* Full logging support including script errors. 

---

## Installation (Option 1: from Git)

### Download Repository

    git clone https://github.com/Praisebetoscience/dockerhub-webhook.git


### Install dependencies

    pip install -r requirements.txt

### Create config

    cp config.py.example config.py

### Generate API token

Create a new token using openssl, pwgen or other tool

    openssl rand -base64 30 | sed 's=/=\\/=g'
    pwgen 30 1

Save this token to either the `DOCHOOK_TOKEN` environmnt variable or in `config.py` as `apikey`.  `DOCHOOK_TOKEN` overrides `config.py`.  

### Configure scripts

Add scripts to `hooks` in `config.py`

    '<repo name>' : '/path/to/script'

Note: The repository name is the name of the container excluding the namespace. (i.e. `namespace/repo` is `repo`.)

### Start a WSGI server (ex [Gunicorn](http://gunicorn.org/))

It is *highly* recommened you install a production ready WSGI server and not use the server packaged with flask (Werkzeug) because it's geared towards development.  Here's a quick example of how to start the application with Gunicorn.  Gunicorn is typically reversed proxied by nginx.  

**NOTE**:  dockerhub-webhook looks for `config.py` in the current working directory. 

    pip install gunicorn
    gunicorn dockerhook:app -w 1 -b <host_ip>:<port>

### Configure [Docker Hub](https://hub.docker.com/)

1. Go to https://hub.docker.com 
2. Click the repository you wish to autodeploy
3. Under the Webhooks tab add a webhook
4. Choose any name you please
5. For the Webhook URL use the following:

    http://<your_domain>:<port>/hubhook?key=<token>

Replace placeholders with your reverse proxy settings.

---

## Installation (Option 2: pip)

### Create project directory

    mkdir -p dockerhook/log

optional

    mkdir -p dockerhook/scripts

### create config.py

    cd dockerhook
    wget -o config.py https://raw.githubusercontent.com/Praisebetoscience/dockerhub-webhook/master/config.py.example

### Install dockerhub-webhook using pip

    pip install dockerhub-webhook

### Follow instructions from Option 1:

* [Generate API key](#generate-api-token)
* [Configure scripts](#configure-scripts)
* [Start a WSGI server](#start-a-wsgi-server-ex-gunicorn)
* [Configure Dockerhub](#configure-docker-hub) 

---

## Development 

#### Project standards

* [github-flow](https://guides.github.com/introduction/flow/) used for branching and merging. 
* [PEP8](https://www.python.org/dev/peps/pep-0008/) *mostly* followed.

#### Development server  

To start Flask's development Werkzeug server, run `run.py`

#### Testing

All tests are written using py.test.  Tests can be run by `python setup.py test`

#### Tools 

* pytest
* flake8
* pylint
