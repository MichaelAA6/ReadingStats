"""
    midfielders_graph.py
    Used to return the midfielders graph on the website
    :returns Appearance, Goals and Assists, Cards, Shots, Offside
"""
import os
import random

import altair as alt
import numpy as np
import pandas as pd
from flask import current_app
def forwards_graph(csv_name):
    #find the players in the database and create a pd Frame
    csv_path = os.path.join(current_app.root_path,'db', csv_name)
    stats = pd.read_csv(csv_path)
    #check all values are error free
    stats['MP'] = pd.to_numeric(stats['MP'], errors='coerce')
    stats['CrdY'] = pd.to_numeric(stats['CrdY'], errors='coerce')
    stats['CrdR'] = pd.to_numeric(stats['CrdR'], errors='coerce')
    stats['Gls'] = pd.to_numeric(stats['Gls'], errors='coerce')
    stats['Ast'] = pd.to_numeric(stats['Ast'], errors='coerce')
    stats['G+A_p90'] = pd.to_numeric(stats['G+A_p90'], errors='coerce')
    stats['Sh'] = pd.to_numeric(stats['Sh'], errors='coerce')
    stats['SoT'] = pd.to_numeric(stats['SoT'], errors='coerce')
    stats['SoT%'] = pd.to_numeric(stats['SoT%'], errors='coerce')
    stats['Off'] = pd.to_numeric(stats['Off'], errors='coerce')
    #copy the stats and make sure they only show forwards and have played a match
    forwards_stats = stats[['Player','Pos','MP', 'Gls','Ast','G+A_p90','Sh','SoT','SoT%','CrdY','CrdR','Off']].copy()
    forwards_stats = forwards_stats[(forwards_stats['Pos'] == 'FW') & (forwards_stats['MP'] > 0)]

    """Appearance Chart"""

    #creates a chart that creates the pie chart showing the player chart
    chart_apps = alt.Chart(forwards_stats).encode(
        #maps the appearances to the arc
        alt.Theta('MP:Q').stack(True),
        #maps the colour to the player
        alt.Color('Player:N',
                  legend=alt.Legend(
                      offset=40
                  )
                  ),
        #view name and appearances when hovering
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('MP:Q', title='Matches Played')
        ]

    )
    #create donut shape
    c1 = chart_apps.mark_arc(innerRadius=20, stroke="#fff")
    #add the numbers to outside the chart
    c2 = chart_apps.mark_text(radius=268, size=20).encode(
        text=alt.Text("MP:Q")
    )
    #combine the charts
    final_chart_apps = (c1 + c2).properties(height=700, width=500)
    chart_apps_json = final_chart_apps.to_json()

    """Goals and Assists Chart"""

    #only copy required stats
    ga_stats = forwards_stats[['Player', 'Gls', 'Ast', 'G+A_p90']].copy()
    #melt the frame to better combine the fields
    ga_stats = ga_stats.melt(
        id_vars=['Player', 'G+A_p90'],
        value_vars=['Gls', 'Ast'],
        var_name='Contribution Type',
        value_name='Count'
    )
    #creates base graph with players on the x-axis
    base_ga = alt.Chart(ga_stats).encode(
        alt.X('Player:N'),
    )
    #find the max goals and assists by a player
    max_bar_ga = float(ga_stats.groupby(['Player', 'Contribution Type'])['Count'].sum().max()) + 1
    #create the bar graph used to represent goals and assists
    bar_ga = base_ga.mark_bar().encode(
        #store the goals and assists
        y=alt.Y('sum(Count):Q', scale=alt.Scale(domain=[0, max_bar_ga]),
                title='Goals/Assists'),
        xOffset='Contribution Type:N',
        #create the colours for the scale including the other y-axis
        color=alt.Color('Contribution Type:N',
                        scale=alt.Scale(
                            domain=['Gls', 'Ast', 'G+A_p90'],
                            range=['green', 'blue', 'red']
                        )),
        #let the user view the players name and type and total of that type
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('Contribution Type:N', title='Contribution Type'),
            alt.Tooltip('Count:Q', title='Value')
        ])
    #find the max GA per 90
    max_line_ga = float(ga_stats['G+A_p90'].max()) + 0.01
    #create the line graph used to represent GA per 90
    line_ga = base_ga.mark_line(
        #create red line with black dots
        color="red",
        point=alt.OverlayMarkDef(color="black", opacity=0.2),
    ).encode(
        #add y value with line
        y=alt.Y('G+A_p90:Q', scale=alt.Scale(domain=[0, max_line_ga]),
                title="Goals + Assists Per 90"),
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('G+A_p90:Q', title='G+A per 90')
        ]
    ).properties(height=500, width=1000)
    #combine the graphs
    chart_ga = alt.layer(bar_ga, line_ga).resolve_scale(y="independent")
    chart_ga_json = chart_ga.to_json()

    """Cards Chart"""

    #only retrieve required stats
    cards_stats = forwards_stats[['Player', 'CrdY', 'CrdR']].copy()
    #melt the frame so fields are combined so they work better
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
    #create bar chart for displaying graphs
    chart_cards = alt.Chart(cards_stats).mark_bar().encode(
        #display player name on x-axis
        x=alt.X('Player:N'),
        #display cards on y-axis
        y=alt.Y('sum(Cards):Q', title='Cards'),
        #display bars as correct colour types
        color=alt.Color(
            'CardType:N',
            scale=alt.Scale(
                domain=['Yellow Cards', 'Red Cards'],
                range=['yellow', 'red']
            ),
            title='Card Type'
        ),
        #let them view the players name, the type of card and how many
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('CardType:N', title='Card Type'),
            alt.Tooltip('Cards:Q', title='Cards')
        ]
    ).properties(height=700, width=500)
    chart_cards_json = chart_cards.to_json()

    """Shots Chart"""

    #only copy required stats
    shots_stats = forwards_stats[['Player', 'Sh', 'SoT', 'SoT%']].copy()
    #melt frame to better combine fields
    shots_stats = shots_stats.melt(
        id_vars=['Player', 'SoT%'],
        value_vars=['Sh', 'SoT'],
        var_name='Shot Type',
        value_name='Shots'
    )
    #create base graph making the x-axis players
    base_shots = alt.Chart(shots_stats).encode(
        alt.X('Player:N'),
    )
    #find the max shots
    max_bar_shots = float(shots_stats.groupby(['Player', 'Shot Type'])['Shots'].sum().max()) + 5
    #create bar chart for shots and shots on target
    bar_shots = base_shots.mark_bar().encode(
        #display both shots and shots on target
        y=alt.Y('sum(Shots):Q', scale=alt.Scale(domain=[0, max_bar_shots]),
                title='Shots/Shots On Target'),
        xOffset='Shot Type:N',
        #set the colours for the scale including the other y-axis
        color=alt.Color('Shot Type:N',
                        scale=alt.Scale(
                            domain=['Sh', 'SoT','SoT%'],
                            range=['black', 'green','red']
                        )),
        #can view the player and the type of shot and the amount they had
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('Shot Type:N', title='Contribution Type'),
            alt.Tooltip('Shots:Q', title='Value')
        ])
    #find the max sot percentage
    max_line_shots = float(shots_stats['SoT%'].max()) + 1
    #create line graph
    line_shots = base_shots.mark_line(
        #make line red and black dots
        color="red",
        point=alt.OverlayMarkDef(color="black", opacity=0.2),
    ).encode(
        y=alt.Y('SoT%:Q', scale=alt.Scale(domain=[0, max_line_shots]),
                title="Shots on Target Percentage %"),
        #show the players name and value
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('SoT%:Q', title='Percentage')
        ]
    )
    #combine the graphs
    chart_shots = alt.layer(bar_shots, line_shots).resolve_scale(y="independent").properties(height=500, width=1000)
    chart_shots_json = chart_shots.to_json()

    """Offside Chart"""

    #only returns stats that are required
    off_stats = forwards_stats[['Player', 'Off']].copy()
    #find the average offside number
    avg_off = round(float(off_stats['Off'].mean()))
    #store the avg offside as a stat
    off_stats['AvgOff'] = avg_off
    #crearte a frame storing the average offside, highest and zero
    area_data = pd.DataFrame({
        'AvgOff': [avg_off],
        'HighestOffside':[float(off_stats['Off'].max())],
        'Zero':[0]
    })
    #create an area showing the below avg offside
    below_avg = alt.Chart(area_data).mark_rect(opacity=0.1).encode(
        y='Zero',
        y2='AvgOff',
        color=alt.ColorValue("#10ba0d")
    )
    #create an area showing the above avg offside
    above_avg = alt.Chart(area_data).mark_rect(opacity=0.1).encode(
        y='AvgOff',
        y2='HighestOffside',
        color=alt.ColorValue("#FF0000")
    )
    #create bar chart
    chart_off = alt.Chart(off_stats).mark_bar().encode(
        #make x-axis players
        x=alt.X('Player:N'),
        #make y-axis offsides
        y=alt.Y('Off:Q', title='Offside',scale=alt.Scale(domain=[0, float(off_stats['Off'].max())],nice=False,padding=0)),
        #match the colour to the player
        color=alt.Color('Player:N'),
        #can hover and view the player and number of offsides
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('Off:Q', title='Offside')
        ]
    )
    #creates line showing the avg offside, allowing users to view the value
    line_off = alt.Chart(off_stats).mark_rule(color='blue').encode(
        y='AvgOff:Q',
        tooltip=[
            alt.Tooltip('AvgOff:N', title='Average Offside'),
        ]
    )
    #combine the elements
    chart_off = (below_avg + above_avg + chart_off + line_off).properties(height=700, width=500)
    chart_off_json = chart_off.to_json()
    return chart_apps_json, chart_ga_json, chart_cards_json,chart_shots_json,chart_off_json