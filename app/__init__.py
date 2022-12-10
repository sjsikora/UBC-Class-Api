from flask import Flask
from app.api import apiBP


def createApp():

    app = Flask(__name__)

    app.register_blueprint(apiBP)
    
    return app

