"""
    routes.py
    used to create link between pages and also provides content to each page
    :returns home,goalkeepers,defenders,midfielders,forwards
"""
from flask import Blueprint, render_template

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
    return render_template('defenders.html',season='2526')
@main.route('/defenders/2425season')
def defenders_2425season():
    return render_template('defenders.html',season='2425' )
@main.route('/midfielders')
def midfielders():
    #creates and returns midfielders graph
    return render_template('midfielders.html',season='2526')
@main.route('/midfielders/2425season')
def midfielders_2425season():
    return render_template('midfielders.html',season='2425')
@main.route('/forwards')
def forwards():
    #creates and returns forwards graph
    return render_template('forwards.html',season='2526')
@main.route('/forwards/2425season')
def forwards_2425season():
    return render_template('forwards.html',season='2425')

#create historical page
@main.route('/history')
def history():
    return render_template('history.html')

#create about page
@main.route('/about')
def about():
    return render_template('about.html')

#create posts page
@main.route('/posts')
def posts():
    return render_template('posts.html')