"""
    midfielder_graph.py
    Used to return the midfielder graph on the website
    :returns Appearance, Goals and Assists, Cards, Crossing
"""
import os
import random

import altair as alt
import numpy as np
import pandas as pd
from flask import current_app
def midfielders_graph():
    #find the players in the database and create a pd Frame
    csv_path = os.path.join(current_app.root_path,'db', 'player_data.csv')
    stats = pd.read_csv(csv_path)
    #check all values are error free
    stats['MP'] = pd.to_numeric(stats['MP'], errors='coerce')
    stats['CrdY'] = pd.to_numeric(stats['CrdY'], errors='coerce')
    stats['CrdR'] = pd.to_numeric(stats['CrdR'], errors='coerce')
    stats['Gls'] = pd.to_numeric(stats['Gls'], errors='coerce')
    stats['Ast'] = pd.to_numeric(stats['Ast'], errors='coerce')
    stats['G+A_p90'] = pd.to_numeric(stats['G+A_p90'], errors='coerce')
    stats['Crs'] = pd.to_numeric(stats['Crs'], errors='coerce')
    #copy the stats and make sure they only show midfielders and have played a match
    midfielders_stats = stats[['Player', 'Pos', 'MP', 'Gls', 'Ast', 'G+A_p90', 'CrdY', 'CrdR','Crs']].copy()
    midfielders_stats = midfielders_stats[(midfielders_stats['Pos'] == 'MF') & (midfielders_stats['MP'] > 0)]

    """Appearance Chart"""

    #creates a chart that creates the pie chart showing the player chart
    chart_apps = alt.Chart(midfielders_stats).encode(
        #maps the appearances to the arc
        alt.Theta('MP:Q').stack(True),
        #maps colour to the player
        alt.Color('Player:N',
                  legend=alt.Legend(
                      offset=40
                  )
                  ),
        #view the name and appearances when hovering
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('MP:Q', title='Matches Played')
        ]

    )
    #create the donut shape
    c1 = chart_apps.mark_arc(innerRadius=20, stroke="#fff")
    #add the numbers to the outside of the chart
    c2 = chart_apps.mark_text(radius=168, size=20).encode(
        text=alt.Text("MP:Q")
    )
    #comboine the charts
    final_chart_apps = c1 + c2
    chart_apps_json = final_chart_apps.to_json()

    """Goals and Assists Chart"""
    #retrieve the stats needed
    ga_stats = midfielders_stats[['Player', 'Gls', 'Ast', 'G+A_p90']].copy()
    #melt the frame to better combine fields
    ga_stats = ga_stats.melt(
        id_vars=['Player', 'G+A_p90'],
        value_vars=['Gls', 'Ast'],
        var_name='Contribution Type',
        value_name='Count'
    )
    #creates base graph with players as x-axis
    base_ga = alt.Chart(ga_stats).encode(
        alt.X('Player:N'),
    )
    #find the max goals and assists by a player
    max_bar = float(ga_stats.groupby(['Player', 'Contribution Type'])['Count'].sum().max()) + 1
    #create the bar graph used to represent goals and assists
    bar_ga = base_ga.mark_bar().encode(
        #store the goals and assists of the player
        y=alt.Y('sum(Count):Q', scale=alt.Scale(domain=[0, max_bar]),
                title='Goals/Assists'),
        xOffset='Contribution Type:N',
        #create the colours for the scale including the other y graph
        color=alt.Color('Contribution Type:N',
                        scale=alt.Scale(
                            domain=['Gls', 'Ast', 'G+A_p90'],
                            range=['green', 'blue', 'red']
                        )),
        #let the user view the name and total and type when they hover over the bar
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('Contribution Type:N', title='Contribution Type'),
            alt.Tooltip('Count:Q', title='Value')
        ])
    #find the max GA per 90 value
    max_line = float(ga_stats['G+A_p90'].max()) + 0.01
    line_ga = base_ga.mark_line(
        #create red lines and black dots
        color="red",
        point=alt.OverlayMarkDef(color="black", opacity=0.2),
    ).encode(
        #add y value with line
        y=alt.Y('G+A_p90:Q', scale=alt.Scale(domain=[0, max_line]),
                title="Goals + Assists Per 90"),
        #can view player and value when hovering
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('G+A_p90:Q', title='G+A per 90')
        ]
    )
    #combine the graphs
    chart_ga = alt.layer(bar_ga, line_ga).resolve_scale(y="independent")
    chart_ga_json = chart_ga.to_json()

    """Cards Chart"""

    #only retrieve the required stats
    cards_stats = midfielders_stats[['Player', 'CrdY', 'CrdR']].copy()
    #melt the frame to combine fields to better work with graph
    cards_stats = cards_stats.melt(
        id_vars='Player',
        value_vars=['CrdY', 'CrdR'],
        var_name='CardType',
        value_name='Cards'
    )
    #rename field names for better displaying
    cards_stats['CardType'] = cards_stats['CardType'].replace({
        'CrdY': 'Yellow Cards',
        'CrdR': 'Red Cards'
    })
    chart_cards = alt.Chart(cards_stats).mark_bar().encode(
        #display player name on x-axis
        x=alt.X('Player:N'),
        #display cards on y-axis
        y=alt.Y('sum(Cards):Q', title='Cards'),
        #display bars as correct colour type
        color=alt.Color(
            'CardType:N',
            scale=alt.Scale(
                domain=['Yellow Cards', 'Red Cards'],
                range=['yellow', 'red']
            ),
            title='Card Type'
        ),
        # let them view the players name, the type of card and how many
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('CardType:N', title='Card Type'),
            alt.Tooltip('Cards:Q', title='Cards')
        ]
    )
    chart_cards_json = chart_cards.to_json()

    """Cross Graph"""

    #only retrieve required stats
    cross_stats = midfielders_stats[['Player','Crs']].copy()
    #find the average number of crosses
    avg_cross = round(float(cross_stats['Crs'].mean()))
    #store the avg cross in stats
    cross_stats['AvgCrs'] = avg_cross
    #create a frame storing the avg, highest and 0
    area_data = pd.DataFrame({
        'AvgCross':[avg_cross],
        'HighestCross':[float(cross_stats['Crs'].max()) +16],
        'Zero': [0]
    })
    #create an area below the avg
    below_avg = alt.Chart(area_data).mark_rect(opacity=0.1).encode(
        y='Zero',
        y2='AvgCross',
        color=alt.ColorValue("#FF0000")
    )
    #create an area above the avg
    above_avg = alt.Chart(area_data).mark_rect(opacity=0.1).encode(
        y='AvgCross',
        y2='HighestCross',
        color=alt.ColorValue("#10ba0d")
    )
    #create bar graph
    chart_cross = alt.Chart(cross_stats).mark_bar().encode(
        #make x-axis for the players
        x=alt.X('Player:N'),
        #make the y-axis for number of crosses
        y=alt.Y('Crs:Q', title='Crosses'),
        #set the colour of each bar to specific player
        color=alt.Color("Player:N"),
        #let user hover over bar and view the number of crosses and players
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('Crs:Q', title='Crosses')
        ]
    )
    #create a line showing the avg crosses, allowing them to view the avg number
    avg_chart = alt.Chart(cross_stats).mark_rule(color="blue").encode(
        y='AvgCrs:Q',
        tooltip=[
            alt.Tooltip('AvgCrs:N', title='Average Crosses'),
        ]
    )
    #combine the graphs and areas
    chart_cross = below_avg + above_avg + chart_cross + avg_chart
    chart_cross_json = chart_cross.to_json()
    return chart_apps_json, chart_ga_json, chart_cards_json,chart_cross_json