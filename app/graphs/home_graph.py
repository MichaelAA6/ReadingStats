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
    stats['Poss'] = pd.to_numeric(stats['Poss'], errors='coerce')
    stats['Attendance'] = stats['Attendance'].replace({',': ''}, regex=True).astype(int)
    stats['Date'] =pd.to_datetime(stats['Date'],errors='coerce')
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
    chart_goal_json = goal_chart.to_json()
    result_count = stats['Result'].value_counts()
    total_wins = result_count.get('W',0)
    total_draws = result_count.get('D',0)
    total_losses = result_count.get('L',0)
    results_stats = pd.DataFrame({
        'Result':["W","D","L"],
        'Total':[total_wins,total_draws,total_losses],
    })
    result_chart = alt.Chart(results_stats).mark_arc(innerRadius=50).encode(
        theta='Total:Q',
        color=alt.Color('Result:N',
            scale=alt.Scale(
                domain=['W','D','L'],
                range=['green','yellow','red']
            )
        ),
        tooltip=['Result', 'Total']
    )
    result_chart_json = result_chart.to_json()
    poss_stats = stats[['Date','Poss','Opponent']].copy()
    avg_poss = poss_stats['Poss'].mean()
    poss_stats['AvgPoss'] = avg_poss
    poss_chart = alt.Chart(poss_stats).mark_line(
        point=alt.OverlayMarkDef(color="black",opacity=0.7),
        interpolate='step-after'
    ).encode(
        x=alt.X('Date:T', title='Date'),
        y=alt.Y('Poss:Q', title='Poss',scale=alt.Scale(zero=False)),
        tooltip=['Date', 'Poss','Opponent'],
    ).properties(
        width=1000, height=500
    )
    line_poss = alt.Chart(poss_stats).mark_rule(color='red').encode(
        y='AvgPoss',
        tooltip=[
            alt.Tooltip('AvgPoss',title='Average Possession'),
        ],
    )
    poss_chart = poss_chart + line_poss
    poss_chart_json = poss_chart.to_json()
    attend_stats = stats[['Attendance','Date','Opponent','Venue']].copy()
    home_attend_stats = attend_stats[(attend_stats['Venue'] == 'Home')]
    away_attend_stats = attend_stats[(attend_stats['Venue'] == 'Away')]
    avg_home_attend = home_attend_stats['Attendance'].mean().round(0)
    home_attend_stats['AvgAttendance'] = avg_home_attend
    avg_away_attend = away_attend_stats['Attendance'].mean().round(0)
    away_attend_stats['AvgAttendance'] = avg_away_attend
    home_line = alt.Chart(home_attend_stats).mark_line(
        point=alt.OverlayMarkDef(color="black", opacity=0.7)
    ).encode(
        x=alt.X('Date:T', title='Date'),
        y=alt.Y('Attendance:Q', title='Attendance'),
        tooltip=['Date', 'Attendance','Opponent'],
    )
    away_line = alt.Chart(away_attend_stats).mark_line(
        color='red',
        point=alt.OverlayMarkDef(color="black", opacity=0.7)
    ).encode(
        x=alt.X('Date:T', title='Date'),
        y=alt.Y('Attendance:Q', title='Attendance'),
        tooltip=['Date', 'Attendance','Opponent'],
    )
    avg_home_line = alt.Chart(home_attend_stats).mark_rule(color="blue").encode(
        y='AvgAttendance',
        tooltip=[
            alt.Tooltip('AvgAttendance',title='Average Home Attendance'),
        ]
    )
    avg_away_line = alt.Chart(away_attend_stats).mark_rule(color="darkred").encode(
        y='AvgAttendance',
        tooltip=[
            alt.Tooltip('AvgAttendance',title='Average Away Attendance'),
        ]
    )

    attend_chart = (home_line + away_line + avg_home_line + avg_away_line).properties(
        width=1000, height=500
    )
    attend_chart_json = attend_chart.to_json()
    return chart_goal_json, result_chart_json,poss_chart_json,attend_chart_json