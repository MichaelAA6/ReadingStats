"""
    routes.py
    used to create link between pages and also provides content to each page
    :returns home,goalkeepers,defenders,midfielders,forwards
"""
from flask import Blueprint, render_template
from app.graphs.home_graph import home_graph, home_graph_match
from app.graphs.goalkeeper_graph import goalkeepers_graph
from app.graphs.defender_graph import defenders_graph
from app.graphs.midfielder_graph import midfielders_graph
from app.graphs.forwards_graph import forwards_graph
from app.graphs.historical_graph import historical_graph

main = Blueprint('main', __name__)

#used to return homepage route and returns the html page
@main.route('/')
def home():
    return render_template('home.html',season='2526')

@main.route('/2425season')
def home_2425season():
    return render_template('home.html',season='2425')
#used to return goalkeepers route and return the html page
@main.route('/goalkeepers')
def goalkeepers():
    #creates and returns the goalkeepers graph
    return render_template('goalkeepers.html',season='2526')
@main.route('/goalkeepers/2425season')
def goalkeepers_2425season():
    return render_template('goalkeepers.html',season='2425')
@main.route('/defenders')
def defenders():
    #creates and returns defenders graph
    apps_graph, ga_graph,card_graph,defence_graph = defenders_graph('player_data.csv')
    return render_template('defenders.html',apps_graph=apps_graph,ga_graph=ga_graph,card_graph=card_graph,defence_graph=defence_graph)
@main.route('/defenders/2425season')
def defenders_2425season():
    apps_graph, ga_graph, card_graph, defence_graph = defenders_graph('player_data2425.csv')
    return render_template('defenders.html', apps_graph=apps_graph, ga_graph=ga_graph, card_graph=card_graph,defence_graph=defence_graph)
@main.route('/midfielders')
def midfielders():
    #creates and returns midfielders graph
    apps_graph, ga_graph,card_graph,cross_graph = midfielders_graph('player_data.csv')
    return render_template('midfielders.html',apps_graph=apps_graph,ga_graph=ga_graph,card_graph=card_graph,cross_graph=cross_graph)
@main.route('/midfielders/2425season')
def midfielders_2425season():
    apps_graph, ga_graph, card_graph, cross_graph = midfielders_graph('player_data2425.csv')
    return render_template('midfielders.html', apps_graph=apps_graph, ga_graph=ga_graph, card_graph=card_graph,cross_graph=cross_graph)
@main.route('/forwards')
def forwards():
    #creates and returns forwards graph
    apps_graph, ga_graph,card_graph,shots_graph,offside_graph = forwards_graph('player_data.csv')
    return render_template('forwards.html',apps_graph=apps_graph,ga_graph=ga_graph,card_graph=card_graph,shots_graph=shots_graph,offside_graph=offside_graph)
@main.route('/forwards/2425season')
def forwards_2425season():
    apps_graph, ga_graph, card_graph, shots_graph, offside_graph = forwards_graph('player_data2425.csv')
    return render_template('forwards.html', apps_graph=apps_graph, ga_graph=ga_graph, card_graph=card_graph,shots_graph=shots_graph, offside_graph=offside_graph)

#create historical page
@main.route('/history')
def history():
    position_graph,tgs_graph = historical_graph()
    return render_template('history.html',position_graph=position_graph,tgs_graph=tgs_graph)

#create about page
@main.route('/about')
def about():
    return render_template('about.html')

#create posts page
@main.route('/posts')
def posts():
    return render_template('posts.html')