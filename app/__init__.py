"""
    __init__.py
    :returns app
"""
from flask import Flask
from .routes import main
def create_app():
    #creates flask application
    app = Flask(__name__)
    app.register_blueprint(main)
    return app