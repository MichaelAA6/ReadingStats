from flask import Blueprint, render_template

from app.graphs import home_graph, goalkeepers_graph, defenders_graph, midfielders_graph

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
    apps_graph, ga_graph,card_graph = defenders_graph()
    return render_template('defenders.html',apps_graph=apps_graph,ga_graph=ga_graph,card_graph=card_graph)

@main.route('/midfielders')
def midfielders():
    apps_graph, ga_graph,card_graph = midfielders_graph()
    return render_template('midfielders.html',apps_graph=apps_graph,ga_graph=ga_graph,card_graph=card_graph)

@main.route('/forwards')
def forwards():
    return render_template('forwards.html')