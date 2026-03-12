from flask import Flask, sessions, render_template

from .blueprints import main
from app.blueprints.hangman import galgje

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    app.register_blueprint(main.Home)
    app.register_blueprint(galgje.Hangman)

    return app