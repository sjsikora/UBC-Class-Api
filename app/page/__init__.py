from flask import Blueprint, render_template

pageBP = Blueprint('page', __name__)

@pageBP.route('/')
def home():
    return render_template('index.html')