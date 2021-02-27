from flask import Flask
from .data import Data


app = Flask(__name__)
Data.load()

from .routes import *
