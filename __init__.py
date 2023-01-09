from flask import Flask
from app import createApp

app = createApp()
app.config['SECRET_KEY'] = "secretkey123"


if __name__ == '__main__':
    app.run()
