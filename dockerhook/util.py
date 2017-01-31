"""dockerhub-webhook util.py"""
import os

def get_app_base_path():
    """Return module directory"""
    return os.path.dirname(os.path.realpath(__file__))

def get_instance_folder_path():
    """Return working directory"""
    return os.getcwd()
