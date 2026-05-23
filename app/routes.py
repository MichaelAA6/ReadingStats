from flask import Blueprint, render_template

from app.graphs import home_graph, goalkeepers_graph

main = Blueprint('main', __name__)

#used to return homepage route and returns the html page
@main.route('/')
def home():
    #creates home page graph
    graph = home_graph()
    return render_template('home.html',graph=graph)

#used to return goalkeepers route and return the html page
@main.route('/goalkeepers')
def goalkeepers():
    apps_graph,card_graph = goalkeepers_graph()
    return render_template('goalkeepers.html',apps_graph=apps_graph,card_graph=card_graph)

@main.route('/defenders')
def defenders():
    return render_template('defenders.html')

@main.route('/midfielders')
def midfielders():
    return render_template('midfielders.html')

@main.route('/forwards')
def forwards():
    return render_template('forwards.html')