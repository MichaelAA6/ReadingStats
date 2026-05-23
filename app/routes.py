from flask import Blueprint, render_template

from app.graphs import home_graph

main = Blueprint('main', __name__)

@main.route('/')
def home():
    graph = home_graph()
    return render_template('home.html',graph=graph)