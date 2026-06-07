"""
    defender_graph.py
    Used to return the defenders graphs used on the website
    :returns Appearances, Goals and Assists, Cards, Defensive Performances
"""
import os
import random

import altair as alt
import numpy as np
import pandas as pd
from flask import current_app

def defenders_graph():
    #find the players database and create a pd Frame
    csv_path = os.path.join(current_app.root_path,'db', 'player_data.csv')
    stats = pd.read_csv(csv_path)
    #check all the values are error free
    stats['MP'] = pd.to_numeric(stats['MP'], errors='coerce')
    stats['CrdY'] = pd.to_numeric(stats['CrdY'], errors='coerce')
    stats['CrdR'] = pd.to_numeric(stats['CrdR'], errors='coerce')
    stats['Gls'] = pd.to_numeric(stats['Gls'], errors='coerce')
    stats['Ast'] = pd.to_numeric(stats['Ast'], errors='coerce')
    stats['G+A_p90'] = pd.to_numeric(stats['G+A_p90'], errors='coerce')
    stats['Fls'] = pd.to_numeric(stats['Fls'], errors='coerce')
    stats['Int'] = pd.to_numeric(stats['Int'], errors='coerce')
    stats['TklW'] = pd.to_numeric(stats['TklW'], errors='coerce')
    #copy the stats and make suer they are only defenders who have played a match
    defender_stats = stats[['Player','Pos','MP', 'Gls','Ast','G+A_p90','CrdY','CrdR','Fls','Int','TklW']].copy()
    defender_stats = defender_stats[(defender_stats['Pos'] == 'DF') & (defender_stats['MP'] > 0)]

    """Appearance Chart"""

    #create a chart that creates the pie chart showing the player caps
    chart_apps = alt.Chart(defender_stats).encode(
        #map appearances to the arc
        alt.Theta('MP:Q').stack(True),
        #map the colour to the player
        alt.Color('Player:N',
                  legend=alt.Legend(
                    offset=40
                    )
                  ),
        #view name and mp when hovering over piece
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('MP:Q', title='Matches Played')
        ]

    )
    #creates donut shape
    c1 = chart_apps.mark_arc(innerRadius=20, stroke="#fff")
    #adds number
    c2 = chart_apps.mark_text(radius=168, size=20).encode(
        text=alt.Text("MP:Q")
    )
    #combine the graphs
    final_chart_apps = c1 + c2
    chart_apps_json = final_chart_apps.to_json()

    """Goals and Assist Chart"""

    #only retrieve the required stats for the graph
    ga_stats = defender_stats[['Player','Gls','Ast','G+A_p90']].copy()
    #melt the frame to better combine the fields
    ga_stats = ga_stats.melt(
        id_vars=['Player','G+A_p90'],
        value_vars=['Gls','Ast'],
        var_name = 'Contribution Type',
        value_name = 'Count'
    )
    #creates the base graph storing the players name
    base_ga = alt.Chart(ga_stats).encode(
        alt.X('Player:N'),
    )
    #find the max goals and assist total
    max_bar = float(ga_stats.groupby(['Player', 'Contribution Type'])['Count'].sum().max()) + 1
    #create the bar graph used to represent goals and assists
    bar_ga = base_ga.mark_bar().encode(
        #store the goals and assists of the player
        y=alt.Y('sum(Count):Q',scale=alt.Scale(domain=[0,max_bar]),
                title='Goals/Assists'),
        xOffset='Contribution Type:N',
        #create the colours for the scale including the other y graph
        color=alt.Color('Contribution Type:N',
            scale=alt.Scale(
                domain=['Gls', 'Ast', 'G+A_p90'],
                range=['green', 'blue','red']
            )),
        #let the user view the name and total and type when they hover over bar
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('Contribution Type:N', title='Contribution Type'),
            alt.Tooltip('Count:Q', title='Value')
        ])
    #find the max GA per 90 value
    max_line = float(ga_stats['G+A_p90'].max()) + 0.01
    #create teh line graph representing the goals/assist per 90
    line_ga = base_ga.mark_line(
        #create red line and add black dots
        color="red",
        point = alt.OverlayMarkDef(color="black", opacity=0.2),
        ).encode(
        #add y value with line
        y=alt.Y('G+A_p90:Q',scale=alt.Scale(domain=[0,max_line]),
                title = "Goals + Assists Per 90"),
        #can view the value and player name when hovering
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('G+A_p90:Q', title='G+A per 90')
        ]
    )
    #combine the charts
    chart_ga = alt.layer(bar_ga, line_ga).resolve_scale(y="independent")
    chart_ga_json = chart_ga.to_json()

    """Cards Chart"""

    #only retrieve the required stats
    cards_stats = defender_stats[['Player', 'CrdY', 'CrdR']].copy()
    #melt the frame to work better combining the fields
    cards_stats = cards_stats.melt(
        id_vars='Player',
        value_vars=['CrdY', 'CrdR'],
        var_name='CardType',
        value_name='Cards'
    )
    #rename the field names for better displaying
    cards_stats['CardType'] = cards_stats['CardType'].replace({
        'CrdY': 'Yellow Cards',
        'CrdR': 'Red Cards'
    })
    #creates bar chart to display the number of charts
    chart_cards = alt.Chart(cards_stats).mark_bar().encode(
        #x axis contains players
        x=alt.X('Player:N'),
        #y axis contains both red and yellow cards
        y=alt.Y('sum(Cards):Q', title='Cards'),
        #set the cards to the correct colours
        color=alt.Color(
            'CardType:N',
            scale=alt.Scale(
                domain=['Yellow Cards', 'Red Cards'],
                range=['yellow', 'red']
            ),
            title='Card Type'
        ),
        #allow them to hover over the graph and read the player name, the type of card and total
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('CardType:N', title='Card Type'),
            alt.Tooltip('Cards:Q', title='Cards')
        ]
    )
    chart_cards_json = chart_cards.to_json()

    """Defensive Performance Chart"""

    #only copy the required stats
    defence_stats = defender_stats[['Player','Fls','Int','TklW']].copy()
    #add value used to modify the shape of graph points
    defence_stats['Fouls_Size'] = defence_stats['Fls']
    #used to find the different points of graph used to create groups and names
    area_data = pd.DataFrame({
        "HlfTck":[(float(defender_stats['TklW'].max()))/2],
        "FulTck":[(float(defender_stats['TklW'].max()))+1],
        "HlfInt":[(float(defender_stats['Int'].max()))/2],
        "FulInt":[(float(defender_stats['Int'].max()))+3],
        "Zerox":[0],
        "Zeroy":[0],
        "LILT":"Low Interception, Low Tackles",
        "HILT":"High Interception, Low Tackles",
        "LIHT":"Low Interception, High Tackles",
        "HIHT":"High Interception, High Tackles",
    })
    #Creates area for Low Interceptions, Low Tackles
    LILT_area = alt.Chart(area_data).mark_rect(opacity=0.1).encode(
        x='Zerox',
        x2='HlfTck',
        y='Zeroy',
        y2='HlfInt',
        #sets colour to red
        color=alt.ColorValue("#FF0000"),
        tooltip=[
            alt.Tooltip('LILT:N', title='Type'),
        ]
    )
    #Creates area for High Interceptions Low Tackles
    HILT_area = alt.Chart(area_data).mark_rect(opacity=0.1).encode(
        x='Zerox',
        x2='HlfTck',
        y='HlfInt',
        y2='FulInt',
        #sets colour to orange
        color=alt.ColorValue("#ff6f00"),
        tooltip=[
            alt.Tooltip('HILT:N', title='Type'),
        ]

    )
    #Creates area for Low Interceptions, High Tackles
    LIHT_area = alt.Chart(area_data).mark_rect(opacity=0.1).encode(
        x='HlfTck',
        x2='FulTck',
        y='Zeroy',
        y2='HlfInt',
        #Sets colour to orange
        color=alt.ColorValue("#ff6f00"),
        tooltip=[
            alt.Tooltip('LIHT:N', title='Type'),
        ]
    )
    #Creates area for High Interceptions, High Tackles
    HIHT_area = alt.Chart(area_data).mark_rect(opacity=0.1).encode(
        x='HlfTck',
        x2='FulTck',
        y='HlfInt',
        y2='FulInt',
        #sets colour to green
        color=alt.ColorValue("#10ba0d"),
        tooltip=[
            alt.Tooltip('HIHT:N', title='Type'),
        ]
    )
    #create point graph
    defence_chart = alt.Chart(defence_stats).mark_point().encode(
        #set x-axis to tackles won
        x=alt.X('TklW:Q',title="Tackles Won"),
        #set y-axis to interceptions
        y=alt.Y('Int:Q',title="Interceptions Won"),
        #The colour is set to the number of fouls
        color=alt.Color(
            'Fls:Q',
            title='Fouls Committed',
            scale=alt.Scale(scheme='goldred'),
            legend=alt.Legend(type='gradient')
        ),
        #also sets the size of the point based on the fouls
        size=alt.Size('Fouls_Size:Q', scale=alt.Scale(range=[100, 1000]),legend=None),
        #let them view all values when they hover over the point
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('TklW:Q', title='Tackles Won'),
            alt.Tooltip('Int:Q', title='Interceptions Won'),
            alt.Tooltip('Fls:Q',title='Fouls Committed')
        ]
    )
    #add all the areas and the graph
    defence_chart = LILT_area + HILT_area + LIHT_area + HIHT_area + defence_chart
    defence_chart_json = defence_chart.to_json()
    return chart_apps_json,chart_ga_json,chart_cards_json,defence_chart_json