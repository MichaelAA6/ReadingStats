from flask import Blueprint, render_template
from app.graphs.home_graph import home_graph
from app.graphs.goalkeeper_graph import goalkeepers_graph
from app.graphs.defender_graph import defenders_graph
from app.graphs.midfielder_graph import midfielders_graph
from app.graphs.forwards_graph import forwards_graph

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
    apps_graph,card_graph,conceded_graph,save_graph,clean_graph = goalkeepers_graph()
    return render_template('goalkeepers.html',apps_graph=apps_graph,card_graph=card_graph,conceded_graph=conceded_graph,save_graph=save_graph,clean_graph=clean_graph)

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
    apps_graph, ga_graph,card_graph,shots_graph = forwards_graph()
    return render_template('forwards.html',apps_graph=apps_graph,ga_graph=ga_graph,card_graph=card_graph,shots_graph=shots_graph)