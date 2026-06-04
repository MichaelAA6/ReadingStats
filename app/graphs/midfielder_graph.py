import os
import random

import altair as alt
import numpy as np
import pandas as pd
from flask import current_app
def midfielders_graph():
    csv_path = os.path.join(current_app.root_path,'db', 'player_data.csv')
    stats = pd.read_csv(csv_path)
    stats['MP'] = pd.to_numeric(stats['MP'], errors='coerce')
    stats['CrdY'] = pd.to_numeric(stats['CrdY'], errors='coerce')
    stats['CrdR'] = pd.to_numeric(stats['CrdR'], errors='coerce')
    stats['Gls'] = pd.to_numeric(stats['Gls'], errors='coerce')
    stats['Ast'] = pd.to_numeric(stats['Ast'], errors='coerce')
    stats['G+A_p90'] = pd.to_numeric(stats['G+A_p90'], errors='coerce')
    stats['Crs'] = pd.to_numeric(stats['Crs'], errors='coerce')
    midfielders_stats = stats[['Player', 'Pos', 'MP', 'Gls', 'Ast', 'G+A_p90', 'CrdY', 'CrdR','Crs']].copy()
    midfielders_stats = midfielders_stats[(midfielders_stats['Pos'] == 'MF') & (midfielders_stats['MP'] > 0)]
    chart_apps = alt.Chart(midfielders_stats).encode(
        alt.Theta('MP:Q').stack(True),
        alt.Color('Player:N',
                  legend=alt.Legend(
                      offset=40
                  )
                  ),
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('MP:Q', title='Matches Played')
        ]

    )
    c1 = chart_apps.mark_arc(innerRadius=20, stroke="#fff")
    c2 = chart_apps.mark_text(radius=168, size=20).encode(
        text=alt.Text("MP:Q")
    )
    final_chart_apps = c1 + c2
    chart_apps_json = final_chart_apps.to_json()
    ga_stats = midfielders_stats[['Player', 'Gls', 'Ast', 'G+A_p90']].copy()
    ga_stats = ga_stats.melt(
        id_vars=['Player', 'G+A_p90'],
        value_vars=['Gls', 'Ast'],
        var_name='Contribution Type',
        value_name='Count'
    )
    base_ga = alt.Chart(ga_stats).encode(
        alt.X('Player:N'),
    )
    max_bar = float(ga_stats.groupby(['Player', 'Contribution Type'])['Count'].sum().max()) + 1
    bar_ga = base_ga.mark_bar().encode(
        y=alt.Y('sum(Count):Q', scale=alt.Scale(domain=[0, max_bar]),
                title='Goals/Assists'),
        xOffset='Contribution Type:N',
        color=alt.Color('Contribution Type:N',
                        scale=alt.Scale(
                            domain=['Gls', 'Ast', 'G+A_p90'],
                            range=['green', 'blue', 'red']
                        )),
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('Contribution Type:N', title='Contribution Type'),
            alt.Tooltip('Count:Q', title='Value')
        ])
    max_line = float(ga_stats['G+A_p90'].max()) + 0.01
    line_ga = base_ga.mark_line(
        color="red",
        point=alt.OverlayMarkDef(color="black", opacity=0.2),
    ).encode(
        y=alt.Y('G+A_p90:Q', scale=alt.Scale(domain=[0, max_line]),
                title="Goals + Assists Per 90"),
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('G+A_p90:Q', title='G+A per 90')
        ]
    )
    chart_ga = alt.layer(bar_ga, line_ga).resolve_scale(y="independent")
    chart_ga_json = chart_ga.to_json()
    cards_stats = midfielders_stats[['Player', 'CrdY', 'CrdR']].copy()
    cards_stats = cards_stats.melt(
        id_vars='Player',
        value_vars=['CrdY', 'CrdR'],
        var_name='CardType',
        value_name='Cards'
    )
    cards_stats['CardType'] = cards_stats['CardType'].replace({
        'CrdY': 'Yellow Cards',
        'CrdR': 'Red Cards'
    })
    chart_cards = alt.Chart(cards_stats).mark_bar().encode(
        x=alt.X('Player:N'),
        y=alt.Y('sum(Cards):Q', title='Cards'),
        color=alt.Color(
            'CardType:N',
            scale=alt.Scale(
                domain=['Yellow Cards', 'Red Cards'],
                range=['yellow', 'red']
            ),
            title='Card Type'
        ),
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('CardType:N', title='Card Type'),
            alt.Tooltip('Cards:Q', title='Cards')
        ]
    )
    chart_cards_json = chart_cards.to_json()
    cross_stats = midfielders_stats[['Player','Crs']].copy()
    avg_cross = round(float(cross_stats['Crs'].mean()))
    cross_stats['AvgCrs'] = avg_cross
    area_data = pd.DataFrame({
        'AvgCross':[avg_cross],
        'HighestCross':[float(cross_stats['Crs'].max()) +16],
        'Zero': [0]
    })
    below_avg = alt.Chart(area_data).mark_rect(opacity=0.1).encode(
        y='Zero',
        y2='AvgCross',
        color=alt.ColorValue("#FF0000")
    )
    above_avg = alt.Chart(area_data).mark_rect(opacity=0.1).encode(
        y='AvgCross',
        y2='HighestCross',
        color=alt.ColorValue("#10ba0d")
    )
    chart_cross = alt.Chart(cross_stats).mark_bar().encode(
        x=alt.X('Player:N'),
        y=alt.Y('Crs:Q', title='Crosses'),
        color=alt.Color("Player:N"),
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('Crs:Q', title='Crosses')
        ]
    )
    avg_chart = alt.Chart(cross_stats).mark_rule(color="blue").encode(
        y='AvgCrs:Q',
        tooltip=[
            alt.Tooltip('AvgCrs:N', title='Average Crosses'),
        ]
    )
    chart_cross = below_avg + above_avg + chart_cross + avg_chart
    chart_cross_json = chart_cross.to_json()
    return chart_apps_json, chart_ga_json, chart_cards_json,chart_cross_json