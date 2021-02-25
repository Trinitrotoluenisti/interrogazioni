from flask import Flask
from .lists import Lists


app = Flask(__name__)
Lists.load()

from .routes import *
