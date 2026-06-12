"""
    home_graph.py
    Used to return the graph used on the homepage
    :return graph
"""
import os
import random
import altair as alt
import numpy as np
import pandas as pd
from flask import current_app

def home_graph(csv_name):
    #retrieves the CSV file of player data
    csv_path = os.path.join(current_app.root_path,'db', csv_name)
    #read the csv file and make sure the data retrieved is error free
    stats = pd.read_csv(csv_path)
    #specifically for minutes remove commas example 4,300 -> 4300
    stats['Min'] = stats['Min'].replace({',': ''}, regex=True).astype(float)
    stats['Gls'] = pd.to_numeric(stats['Gls'], errors='coerce')
    #create new data frame storing only player name, goals and minutes played
    goal_stats = stats[['Player', 'Gls', 'Min']].copy()
    #filter the stats for only players who have scored or played
    goal_stats = goal_stats[(goal_stats['Gls'] > 0) & (goal_stats['Min'] > 0)]
    #creates random rotation and colours for graph
    goal_stats['Rotation'] = np.random.uniform(0, 90, size=len(goal_stats))
    goal_stats['Color'] = [
        f"#{random.randint(0, 0xFFFFFF):06x}"
        for _ in range(len(goal_stats))
    ]

    #create point graph with diamond shapes with slightly less opacity
    chart = alt.Chart(goal_stats).mark_point(shape="diamond",size=4000,filled=True,opacity=0.8).encode(
        #make x and y-axis goals and minutes
        x=alt.X('Gls:Q', title='Goals'),
        y=alt.Y('Min:Q', title='Minutes'),
        #allow people to hover over and view point stats
        tooltip=['Player', 'Gls', 'Min'],
        #add the random rotation and colour from above to better separate points
        angle=alt.Angle('Rotation:Q', scale=alt.Scale(domain=[0, 90])),
        color=alt.Color('Color:N', scale=None)
    ).properties(
        width=400,  # Wider chart
        height=800  # Taller chart
    #allow people to move graph and zoom in
    ).interactive()
    #make graph json so it can be displayed on html
    chart_json = chart.to_json()
    return chart_json

def home_graph_match(csv_name):
    csv_path = os.path.join(current_app.root_path,'db', csv_name)
    stats = pd.read_csv(csv_path)
    stats['GF'] = pd.to_numeric(stats['GF'], errors='coerce')
    stats['GA'] = pd.to_numeric(stats['GA'], errors='coerce')
    stats['Result'] = pd.to_numeric(stats['Result'], errors='coerce')
    stats['Poss'] = pd.to_numeric(stats['Poss'], errors='coerce')
    stats['Attendance'] = stats['Attendance'].replace({',': ''}, regex=True).astype(int)
    goals_scored = stats['GF'].sum()
    goals_conceded = stats['GA'].sum()
    goal_difference = goals_scored - goals_conceded
    goal_stats = pd.DataFrame({
        'Type':['Goals Scored','Goals Conceded','Goals Difference'],
        'Goals':[goals_scored, goals_conceded, goal_difference]
    })
    goal_chart = alt.Chart(goal_stats).mark_bar().encode(
        x=alt.X('Type:N', title='Type',sort=None),
        y=alt.Y('Goals:Q', title='Goals'),
        tooltip=['Type', 'Goals'],
        color=alt.Color('Type:N',
            scale=alt.Scale(
                domain=['Goals Scored', 'Goals Conceded', 'Goals Difference'],
                range=['green','red','yellow']
            )
        ),
    )
    chart_json = goal_chart.to_json()
    return chart_json