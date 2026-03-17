from flask import Flask, sessions, render_template

from app.blueprints.hangman import galgje
from app.blueprints.boter_kaas_eieren import bke
from app.blueprints.getal_rader import getal

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')
    
    app.register_blueprint(galgje.Hangman)
    app.register_blueprint(bke.bke)
    app.register_blueprint(getal.Bagel)

    return app
