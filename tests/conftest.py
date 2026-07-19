import os
import sys

# Make the Flask application importable from docker/app/app.py
APP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docker", "app")
sys.path.insert(0, APP_DIR)
