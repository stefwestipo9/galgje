from flask import Blueprint, render_template

Home = Blueprint("main", __name__)

@Home.route("/")
def home():
    return render_template("index.html")