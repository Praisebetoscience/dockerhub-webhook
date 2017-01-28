#!venv/bin/python

"""dockerhub-webhook run.py"""

from app import app
app.run(debug=True)
