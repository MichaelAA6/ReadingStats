"""
    goalkeeper_graph.py
    Used to return the goalkeepers graphs used on the website
    :returns Appearance,Cards,Conceded,Saves,Clean Sheets
"""
import os
import random
import altair as alt
import numpy as np
import pandas as pd
from flask import current_app

def goalkeepers_graph():
    #find the goalkeeper csv and store it as a data frame
    csv_path = os.path.join(current_app.root_path,'db', 'goalkeeper_data.csv')
    stats = pd.read_csv(csv_path)
    #check all the values are error free
    stats['MP'] = pd.to_numeric(stats['MP'], errors='coerce')
    stats['GA'] = pd.to_numeric(stats['GA'], errors='coerce')
    stats['GA90'] = pd.to_numeric(stats['GA90'], errors='coerce')
    stats['SoTA'] = pd.to_numeric(stats['SoTA'], errors='coerce')
    stats['Saves'] = pd.to_numeric(stats['Saves'], errors='coerce')
    stats['Save%'] = pd.to_numeric(stats['Save%'], errors='coerce')
    stats['CS'] = pd.to_numeric(stats['CS'], errors='coerce')
    stats['CS%'] = pd.to_numeric(stats['CS%'], errors='coerce')
    stats['CrdY'] = pd.to_numeric(stats['CrdY'], errors='coerce')
    stats['CrdR'] = pd.to_numeric(stats['CrdR'], errors='coerce')
    #store the stats as keeper stats
    keeper_stats = stats[['Player','Pos','MP', 'CrdY', 'CrdR','GA','GA90','SoTA','Saves','Save%','CS','CS%']].copy()
    keeper_stats = keeper_stats[(keeper_stats['Pos'] == 'GK')]

    """Appearance Graph"""

    #create a pie chart to display the number of appearances
    chart_apps = alt.Chart(keeper_stats).encode(
        #map appearances to the arc
        alt.Theta('MP:Q').stack(True),
        #add colour based on the player
        alt.Color('Player:N'),
        #view name and mp when hovering over chart
        tooltip=[
            alt.Tooltip('Player:N',title = 'Players Name'),
            alt.Tooltip('MP:Q',title='Matches Played')
        ]

    )
    #creates donut shape
    c1 = chart_apps.mark_arc(innerRadius=20, stroke="#fff")
    #adds number
    c2 = chart_apps.mark_text(radius=180,size=20).encode(
        text=alt.Text("MP:Q")
    )
    #combine both and then convert to json to allow for html
    final_chart_apps = c1+c2
    chart_apps_json = final_chart_apps.to_json()

    #returns data frame with only player and cards values
    cards_stats = keeper_stats[['Player','CrdY', 'CrdR']].copy()
    #melt frame to work better when combining the fields
    cards_stats = cards_stats.melt(
        id_vars='Player',
        value_vars=['CrdY', 'CrdR'],
        var_name = 'CardType',
        value_name = 'Cards'
    )
    #change the card names to be better for displaying
    cards_stats['CardType'] = cards_stats['CardType'].replace({
        'CrdY': 'Yellow Cards',
        'CrdR': 'Red Cards'
    })
    #create the bar chart for displaying the number of cards
    chart_cards = alt.Chart(cards_stats).mark_bar().encode(
        #x axis is players, where y is both Yellow and Red cards
        x=alt.X('Player:N'),
        y=alt.Y('sum(Cards):Q',title='Cards'),
        #set the colours to the correct domain, so red is red bar and yellow is yellow bar
        color=alt.Color(
        'CardType:N',
        scale=alt.Scale(
                domain=['Yellow Cards', 'Red Cards'],
                range=['yellow', 'red']
            ),
            #add title
            title='Card Type'
        ),
        #display details on hover
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('CardType:N', title='Card Type'),
            alt.Tooltip('Cards:Q', title='Cards')
        ]
    )
    chart_cards_json = chart_cards.to_json()

    """Conceded Graph"""

    #retrieves stats for goals conceded
    gc_stats = keeper_stats[['Player','GA','GA90']].copy()
    #melts fields
    gc_stats = gc_stats.melt(
        id_vars=['Player','GA90'],
        value_vars='GA',
        var_name = 'Conceded Type',
        value_name = 'Conceded'
    )
    #rename to be more appropriate
    gc_stats['Conceded Type'] = gc_stats['Conceded Type'].replace({
        'GA': 'Goals Conceded',
        'GA90': 'Goals Conceded Per 90'
    })
    #creates base graph with player x axis
    base_gc = alt.Chart(gc_stats).encode(
        x=alt.X('Player:N'),
    )
    #find the maximum value of the bar value of goals conceded
    max_bar = float(gc_stats.groupby(['Player', 'Contribution Type'])['Conceded'].sum().max()) + 20
    #create the bar part of the y axis
    bar_gc = base_gc.mark_bar().encode(
        #gets number of goals conceded
        y = alt.Y('sum(Conceded):Q',
                  scale=alt.Scale(domain=[0, max_bar]),
                  title='Goals Conceded'),
        xOffset='Conceded Type:N',
        #sets colours for both so they both appear on scale
        color=alt.Color('Conceded Type:N',
            scale=alt.Scale(
                domain=['Goals Conceded','Goals Conceded Per 90'],
                range=['green', 'red']
        )),
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('Conceded:Q', title='Conceded')
        ]
    )
    #find max value for line value
    max_line = float(gc_stats['GA90'].max()) + 0.1
    #create the line part of the y axis
    line_gc = base_gc.mark_line(color="red",
                #creates point for better visualisation
                point=alt.OverlayMarkDef(color="black",opacity=0.2)).encode(
        y = alt.Y('GA90:Q',
                  scale=alt.Scale(domain=[0, max_line]),
                  title='Goals Conceded Per 90'),
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('Conceded:Q', title='Conceded Per 90')
        ]
    )
    #combine both y axes
    chart_gc = alt.layer(bar_gc, line_gc).resolve_scale(y="independent")
    chart_gc_json = chart_gc.to_json()

    """Saves Chart"""

    #gets save stats
    ks_stats = keeper_stats[['Player','SoTA','Saves','Save%']].copy()
    #melts them
    ks_stats = ks_stats.melt(
        id_vars=['Player','Save%'],
        value_vars=['SoTA','Saves'],
        var_name = 'Saves Type',
        value_name = 'Saved'
    )
    #rename for better visualization
    ks_stats['Saves Type'] = ks_stats['Saves Type'].replace({
        'SoTA': 'Shots Faced',
        'Saves': 'Saves',
    })
    #creates base with x axis
    base_ks = alt.Chart(ks_stats).encode(
        x=alt.X('Player:N'),
    )
    max_bar = float(ks_stats.groupby(['Player', 'Saves Type'])['Saved'].sum().max()) + 20
    #creates bar y axis
    bar_ks = base_ks.mark_bar().encode(
        y = alt.Y('sum(Saved):Q',
                  scale=alt.Scale(domain=[0, max_bar]),
                  title='Shots Faced/Saved'),
        xOffset='Saves Type:N',
        color=alt.Color('Saves Type:N',
                        scale=alt.Scale(
                            domain=['Shots Faced','Saves','Saves Percentage'],
                            range=['red','green','blue']
                        )),
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('Saves Type:N', title='Saves Type'),
            alt.Tooltip('Saved:Q',title='Value')
        ]
    )
    max_line = float(ks_stats['Save%'].max()) + 20
    #creates line y axis
    line_ks = base_ks.mark_line(color="blue",
        point=alt.OverlayMarkDef(color="black",opacity=0.2)).encode(
        y = alt.Y('Save%:Q',scale=alt.Scale(domain=[0, max_line]),
                  title='Saves Percentage'),
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('Save%:N', title='Save Percentage'),
        ]
    )
    #combines both y-axes
    chart_ks = alt.layer(bar_ks, line_ks).resolve_scale(y="independent")
    chart_ks_json = chart_ks.to_json()

    """Clean Sheet Graph"""

    #retrieve clean sheet stats
    cs_stats = keeper_stats[['Player','CS','CS%']].copy()
    #melt frame
    cs_stats = cs_stats.melt(
        id_vars=['Player','CS%'],
        value_vars=['CS'],
        var_name = 'Clean Type',
        value_name = 'Clean'
    )
    #creates x axis base
    base_cs = alt.Chart(cs_stats).encode(
        x=alt.X('Player:N'),
    )
    max_bar = float(cs_stats.groupby(['Player', 'Clean Type'])['Clean'].sum().max()) + 3
    #creates bar for y axis
    bar_cs = base_cs.mark_bar().encode(
        y = alt.Y('sum(Clean):Q',
                  scale=alt.Scale(domain=[0, max_bar]),
                  title='Clean Sheets'),
        xOffset='Clean Type:N',
        color=alt.Color('Clean Type:N',
                        scale=alt.Scale(
                            domain=['CS','CS%'],
                            range=['red','green']
                        )),
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('Clean:Q', title='Clean Sheets'),
        ]
    )
    max_line = float(cs_stats['CS%'].max()) + 2
    #create line for y axis
    line_cs = base_cs.mark_line(color="green",
            point=alt.OverlayMarkDef(color="black",opacity=0.2)).encode(
        y = alt.Y('CS%:Q',
                  scale=alt.Scale(domain=[0, max_line]),
                  title='Clean Sheets Percentage'),
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('CS%:N', title='Clean Sheets Percentage'),
        ]
    )
    #combine the two y axes
    graph_cs = alt.layer(bar_cs, line_cs).resolve_scale(y="independent")
    graph_cs_json = graph_cs.to_json()
    #return all the graphs
    return chart_apps_json, chart_cards_json,chart_gc_json,chart_ks_json,graph_cs_json
