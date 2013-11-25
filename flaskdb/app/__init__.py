from flask import Flask

app = Flask(__name__)

from flaskdb.app import views