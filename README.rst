dockerhub-webhook
=================
.. image:: https://img.shields.io/pypi/v/dockerhub-webhook.svg
   :alt: PyPi version
   :target: https://pypi.python.org/pypi?:action=display&name=dockerhub-webhook&version=0.2.1
.. image:: https://travis-ci.org/Praisebetoscience/dockerhub-webhook.svg?branch=master
   :alt: Travis CI Status
   :target: https://travis-ci.org/Praisebetoscience/dockerhub-webhook
.. image:: https://coveralls.io/repos/github/Praisebetoscience/dockerhub-webhook/badge.svg?branch=master
   :alt: Coveralls Coverage
   :target: https://coveralls.io/github/Praisebetoscience/dockerhub-webhook?branch=master
.. image:: https://codeclimate.com/github/Praisebetoscience/dockerhub-webhook/badges/gpa.svg
   :alt: Code Climate Rating
   :target: https://codeclimate.com/github/Praisebetoscience/dockerhub-webhook
.. image:: https://requires.io/github/Praisebetoscience/dockerhub-webhook/requirements.svg?branch=master
   :alt: Requires.io Check
   :target: https://requires.io/github/Praisebetoscience/dockerhub-webhook/requirements/?branch=master


**dockerhub-webhook** listens to HTTP POST requests from dockerhub and
triggers your scripts to update when a new container is available.

.. _Features:

Features
--------

-  Python 3.3+ support.
-  Pip installion availble
-  Lightweight - built using `Flask`_.
-  Supports unlimited number of triggers.
-  Full logging support including script errors.

--------------

.. _installation:

Installation (Option 1: from Git)
---------------------------------

Dockerhub-webhook is supported on python 3.3, 3.4, 3.5, and 3.6.  To install
from the github repository, the first step is to clone it.

.. code-block:: bash

    git clone https://github.com/Praisebetoscience/dockerhub-webhook.git

Then install dependencies.

.. code-block:: bash

    pip install -r requirements.txt

Next we need to create the config file which contains our apikey, maps scripts
to incoming repository hooks.  We can start from the example config.py and
filling in the variables listed.

.. code-block:: bash

    cp config.py.example config.py

To generate an apikey you can use tools such as openssl or pwgen.

.. code-block:: bash

    openssl rand -base64 30 | sed 's=/=\\/=g'
    pwgen 30 1

Alternatively you can set the ``$DOCKERHOOK_TOKEN`` environment variable with your
key.  This will override anything in config.py.

The ``HOOKS`` dict in config.py maps respository names to serverside deploy
scripts.  Keys are the names of repositories (no namespace), and values are
the full path to the script to be called, or a relative path to the current
working directory.

.. code-block:: python

    HOOKS = {'repo1': '/full/path/to/script.sh',
             'repo2': 'relative_path_to_script.sh'
            }


WSGI server (ex `Gunicorn`_)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is *highly* recommened you install a production ready WSGI server and
not use the server packaged with Flask (Werkzeug) because it’s geared
towards development. Here’s a quick example of how to start the
application with Gunicorn. Gunicorn is typically reversed proxied by
nginx.

**NOTE**: dockerhub-webhook looks for ``config.py`` in the current
working directory.

.. code-block:: bash

    pip install gunicorn
    gunicorn dockerhook:app -w 1 -b <host_ip>:<port>


Installation (Option 2: pip)
----------------------------

The biggest devation from installing from github is the directory stucture
where the config file, logs, and optionally scripts needs to be created

.. code-block:: bash

    mkdir -p dockerhook/log
    mkdir -p dockerhook/scripts

You create your config file just as above, but instead of coming with the
source, you have to download the example directly.

.. code-block:: bash

    cd dockerhook
    wget -o config.py https://raw.githubusercontent.com/Praisebetoscience/dockerhub-webhook/master/config.py.example

.. _DockerHubSetup:

Configure `Docker Hub`_
~~~~~~~~~~~~~~~~~~~~~~~

#. Go to https://hub.docker.com
#. Click the repository you wish to autodeploy
#. Under the Webhooks tab add a webhook
#. Choose any name you please
#. For the Webhook URL use the following:

.. code-block:: bash

    http://example.com/hubhook?key=secret

Adjust the domain and endpoint to your reverse proxy setting, and replace
``secret`` with your API key.

.. _license:

License
~~~~~~~

dockerhub-webhook source code is provided under the `Apachi 2.0 License
<http://www.apache.org/licenses/LICENSE-2.0>`_.

* Copyright (c), 2017, PrasieBeToScience.

.. _development:

Development
~~~~~~~~~~~

Webhook uses `github-flow`_ for managing branches and follows `PEP8`_ as much as
possible.

To start Flask's development Werkzeug server you can use ``run.py``.

You can run pytest unittests using ``python setup.py test``.



.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _github-flow: https://guides.github.com/introduction/flow/
.. _Flask: http://flask.pocoo.org/
.. _Gunicorn: http://gunicorn.org/
.. _Docker Hub: https://hub.docker.com/



