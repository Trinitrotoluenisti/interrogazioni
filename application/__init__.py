from flask import Flask
from .data import load_data


app = Flask(__name__)
app.url_map.strict_slashes = False

load_data()


from .routes import *
