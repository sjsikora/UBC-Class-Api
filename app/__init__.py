from flask import Flask
from app.api import apiBP
from app.page import pageBP

def createApp():
    app = Flask(__name__)

    app.register_blueprint(apiBP)
    app.register_blueprint(pageBP)
    return app

