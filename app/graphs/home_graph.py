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
from pathlib import Path

def home_graph(csv_name,season):
    #retrieves the CSV file of player data
    root = Path(__file__).resolve().parents[1]
    csv_path = root / 'db' / csv_name
    json_output = root / 'static' / 'jsons' / 'home' / season
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
        width=1000,  # Wider chart
        height=1000  # Taller chart
    #allow people to move graph and zoom in
    ).interactive()
    #make graph json so it can be displayed on html
    chart.save(str(json_output / 'scorers.json'))

def home_graph_match(csv_name,season):
    #connect to csv file for match data and make it a frame
    root = Path(__file__).resolve().parents[1]
    csv_path = root / 'db' / csv_name
    json_output = root / 'static' / 'jsons' / 'home' / season
    stats = pd.read_csv(csv_path)
    #go throught stats and make sure all the data is error free
    stats['GF'] = pd.to_numeric(stats['GF'], errors='coerce')
    stats['GA'] = pd.to_numeric(stats['GA'], errors='coerce')
    stats['Poss'] = pd.to_numeric(stats['Poss'], errors='coerce')
    stats['Attendance'] = stats['Attendance'].replace({',': ''}, regex=True).astype(int)
    stats['Date'] =pd.to_datetime(stats['Date'],errors='coerce')

    """Goal Chart"""

    #find the total goals for and against and then find goal difference
    goals_scored = stats['GF'].sum()
    goals_conceded = stats['GA'].sum()
    goal_difference = goals_scored - goals_conceded
    #make a data frame to better format data
    goal_stats = pd.DataFrame({
        'Type':['Goals Scored','Goals Conceded','Goals Difference'],
        'Goals':[goals_scored, goals_conceded, goal_difference]
    })
    #create bar chart to display the goals
    goal_chart = alt.Chart(goal_stats).mark_bar().encode(
        #x-axis is the type, goals for against difference
        x=alt.X('Type:N', title='Type',sort=None),
        #y-axis is the goal value
        y=alt.Y('Goals:Q', title='Goals'),
        #when hovering display the type and number of goals
        tooltip=['Type', 'Goals'],
        #set colour for each column
        color=alt.Color('Type:N',
            scale=alt.Scale(
                domain=['Goals Scored', 'Goals Conceded', 'Goals Difference'],
                range=['green','red','yellow']
            )
        ),
    ).properties(height=700,width=500)
    #convert chart to json so it can be displayed on html
    goal_chart.save(str(json_output / 'goals.json'))

    """Result Chart"""

    #get all the result values and find each type total
    result_count = stats['Result'].value_counts()
    total_wins = result_count.get('W',0)
    total_draws = result_count.get('D',0)
    total_losses = result_count.get('L',0)
    #create new frame to better display the values
    results_stats = pd.DataFrame({
        'Result':["W","D","L"],
        'Total':[total_wins,total_draws,total_losses],
    })
    #create pie chart with gap in middle
    result_chart = alt.Chart(results_stats).mark_arc(innerRadius=50).encode(
        #set the angle based on the values
        theta='Total:Q',
        #set the colour mapped to the result
        color=alt.Color('Result:N',
            scale=alt.Scale(
                domain=['W','D','L'],
                range=['green','yellow','red']
            )
        ),
        tooltip=['Result', 'Total']
    ).properties(height=700,width=500)
    result_chart.save(str(json_output / 'results.json'))


    """Possession Chart"""

    #copy the stats needed for the graph
    poss_stats = stats[['Date','Poss','Opponent']].copy()
    #find the avg possesion and store it
    avg_poss = poss_stats['Poss'].mean()
    poss_stats['AvgPoss'] = avg_poss
    #create a line graph
    poss_chart = alt.Chart(poss_stats).mark_line(
        #create black points and make it a step graph
        point=alt.OverlayMarkDef(color="black",opacity=0.7),
        interpolate='step-after'
    ).encode(
        #x-axis is the date
        x=alt.X('Date:T', title='Date'),
        #y-axis is the possession value
        y=alt.Y('Poss:Q', title='Poss',scale=alt.Scale(zero=False)),
        #tool tip to view the stats
        tooltip=['Date', 'Poss','Opponent'],
    ).properties(
        #set width and height
        width=1000, height=500
    )
    #create straight line showing the average possession
    line_poss = alt.Chart(poss_stats).mark_rule(color='red').encode(
        y='AvgPoss',
        tooltip=[
            alt.Tooltip('AvgPoss',title='Average Possession'),
        ],
    )
    #combine the charts
    poss_chart = poss_chart + line_poss
    poss_chart.save(str(json_output / 'poss.json'))

    """Attendance Chart"""

    #copy the required stats for attendance
    attend_stats = stats[['Attendance','Date','Opponent','Venue']].copy()
    #find just home stats and away stats
    home_attend_stats = attend_stats[(attend_stats['Venue'] == 'Home')]
    away_attend_stats = attend_stats[(attend_stats['Venue'] == 'Away')]
    #find the home and away avg attendance and store it
    avg_home_attend = home_attend_stats['Attendance'].mean().round(0)
    home_attend_stats['AvgAttendance'] = avg_home_attend
    avg_away_attend = away_attend_stats['Attendance'].mean().round(0)
    away_attend_stats['AvgAttendance'] = avg_away_attend
    #create line graph for home attendance
    home_line = alt.Chart(home_attend_stats).mark_line(
        point=alt.OverlayMarkDef(color="black", opacity=0.7)
    ).encode(
        #x-axis is date
        x=alt.X('Date:T', title='Date'),
        #y-axis is the attendance
        y=alt.Y('Attendance:Q', title='Attendance'),
        tooltip=['Date', 'Attendance','Opponent'],
    )
    #create line graph for away attendance
    away_line = alt.Chart(away_attend_stats).mark_line(
        #make line red
        color='red',
        point=alt.OverlayMarkDef(color="black", opacity=0.7)
    ).encode(
        x=alt.X('Date:T', title='Date'),
        y=alt.Y('Attendance:Q', title='Attendance'),
        tooltip=['Date', 'Attendance','Opponent'],
    )
    #create avg home attendance line
    avg_home_line = alt.Chart(home_attend_stats).mark_rule(color="blue").encode(
        y='AvgAttendance',
        tooltip=[
            alt.Tooltip('AvgAttendance',title='Average Home Attendance'),
        ]
    )
    #create avg away attendance line
    avg_away_line = alt.Chart(away_attend_stats).mark_rule(color="darkred").encode(
        y='AvgAttendance',
        tooltip=[
            alt.Tooltip('AvgAttendance',title='Average Away Attendance'),
        ]
    )
    #combine all the lines and set the size
    attend_chart = (home_line + away_line + avg_home_line + avg_away_line).properties(
        width=1000, height=500
    )
    attend_chart.save(str(json_output / 'attend.json'))

    """Map Chart"""

    #retrieve stadium csv then merge both databases on the opponent and team
    stadium_csv = pd.read_csv(root / 'db' / 'stadiums.csv')
    stats = stats.merge(stadium_csv, left_on='Opponent',right_on='Team',how='left')
    #retreieve the map graph
    countries = alt.topo_feature('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json', 'countries')
    #set the type scale and location
    projection = dict(type='mercator', scale=7000, center=[-1.5, 52.6])
    #create map graph
    map_chart = alt.Chart(countries).mark_geoshape(fill='#e8f0e8', stroke='#b0c4b0', strokeWidth=0.5).project(**projection).properties(width=1000,height=1000)
    #add points of opposition teams
    map_points = alt.Chart(stats).mark_point(color="red",size=100,filled=True).encode(
        #get longitude value
        longitude='Lon:Q',
        #get latitude value
        latitude='Lat:Q',
        #view team and stadium name when hovering
        tooltip=[
            alt.Tooltip('Team:N',title='Team'),
            alt.Tooltip('Stadium:N',title='Stadium'),
        ]
    ).project(**projection)
    #add the stadium names to the map
    map_labels = alt.Chart(stats).mark_text(align='left', fontSize=7,dy=12).encode(
        longitude='Lon:Q',
        latitude='Lat:Q',
        text='Stadium:N',
    ).project(**projection)
    #combine all parts and configure the view
    map_chart = (map_chart + map_points + map_labels).configure_view()
    map_chart.save(str(json_output / 'map.json'))

home_graph('player_data.csv','2526')
home_graph('player_data2425.csv','2425')
home_graph_match('match_data.csv','2526')
home_graph_match('match_data2425.csv','2425')