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

main = Blueprint('main', __name__)

#used to return homepage route and returns the html page
@main.route('/')
def home():
    #creates home page graph
    graph = home_graph('player_data.csv')
    goal_graph,result_graph,poss_graph,attend_graph,map_graph = home_graph_match('match_data.csv')
    return render_template('home.html',graph=graph,goal_graph=goal_graph,result_graph=result_graph,poss_graph=poss_graph,attend_graph=attend_graph,map_graph=map_graph)

@main.route('/2425season')
def home_2425season():
    graph = home_graph('player_data2425.csv')
    goal_graph,result_graph,poss_graph,attend_graph,map_graph = home_graph_match('match_data2425.csv')
    return render_template('home.html',graph=graph,goal_graph=goal_graph,result_graph=result_graph,poss_graph=poss_graph,attend_graph=attend_graph,map_graph=map_graph)
#used to return goalkeepers route and return the html page
@main.route('/goalkeepers')
def goalkeepers():
    #creates and returns the goalkeepers graph
    apps_graph,card_graph,conceded_graph,save_graph,clean_graph = goalkeepers_graph('goalkeeper_data.csv')
    return render_template('goalkeepers.html',apps_graph=apps_graph,card_graph=card_graph,conceded_graph=conceded_graph,save_graph=save_graph,clean_graph=clean_graph)
@main.route('/goalkeepers/2425season')
def goalkeepers_2425season():
    apps_graph, card_graph, conceded_graph, save_graph, clean_graph = goalkeepers_graph('goalkeeper_data2425.csv')
    return render_template('goalkeepers.html', apps_graph=apps_graph, card_graph=card_graph,conceded_graph=conceded_graph, save_graph=save_graph, clean_graph=clean_graph)
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