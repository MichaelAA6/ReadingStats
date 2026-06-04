import os
import random

import altair as alt
import numpy as np
import pandas as pd
from flask import current_app
def forwards_graph():
    csv_path = os.path.join(current_app.root_path,'db', 'player_data.csv')
    stats = pd.read_csv(csv_path)
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
    forwards_stats = stats[['Player','Pos','MP', 'Gls','Ast','G+A_p90','Sh','SoT','SoT%','CrdY','CrdR','Off']].copy()
    forwards_stats = forwards_stats[(forwards_stats['Pos'] == 'FW') & (forwards_stats['MP'] > 0)]
    chart_apps = alt.Chart(forwards_stats).encode(
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
    ga_stats = forwards_stats[['Player', 'Gls', 'Ast', 'G+A_p90']].copy()
    ga_stats = ga_stats.melt(
        id_vars=['Player', 'G+A_p90'],
        value_vars=['Gls', 'Ast'],
        var_name='Contribution Type',
        value_name='Count'
    )
    base_ga = alt.Chart(ga_stats).encode(
        alt.X('Player:N'),
    )
    max_bar_ga = float(ga_stats.groupby(['Player', 'Contribution Type'])['Count'].sum().max()) + 1
    bar_ga = base_ga.mark_bar().encode(
        y=alt.Y('sum(Count):Q', scale=alt.Scale(domain=[0, max_bar_ga]),
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
    max_line_ga = float(ga_stats['G+A_p90'].max()) + 0.01
    line_ga = base_ga.mark_line(
        color="red",
        point=alt.OverlayMarkDef(color="black", opacity=0.2),
    ).encode(
        y=alt.Y('G+A_p90:Q', scale=alt.Scale(domain=[0, max_line_ga]),
                title="Goals + Assists Per 90"),
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('G+A_p90:Q', title='G+A per 90')
        ]
    )
    chart_ga = alt.layer(bar_ga, line_ga).resolve_scale(y="independent")
    chart_ga_json = chart_ga.to_json()
    cards_stats = forwards_stats[['Player', 'CrdY', 'CrdR']].copy()
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
    shots_stats = forwards_stats[['Player', 'Sh', 'SoT', 'SoT%']].copy()
    shots_stats = shots_stats.melt(
        id_vars=['Player', 'SoT%'],
        value_vars=['Sh', 'SoT'],
        var_name='Shot Type',
        value_name='Shots'
    )
    base_shots = alt.Chart(shots_stats).encode(
        alt.X('Player:N'),
    )
    max_bar_shots = float(shots_stats.groupby(['Player', 'Shot Type'])['Shots'].sum().max()) + 5
    bar_shots = base_shots.mark_bar().encode(
        y=alt.Y('sum(Shots):Q', scale=alt.Scale(domain=[0, max_bar_shots]),
                title='Shots/Shots On Target'),
        xOffset='Shot Type:N',
        color=alt.Color('Shot Type:N',
                        scale=alt.Scale(
                            domain=['Sh', 'SoT','SoT%'],
                            range=['black', 'green','red']
                        )),
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('Shot Type:N', title='Contribution Type'),
            alt.Tooltip('Shots:Q', title='Value')
        ])
    max_line_shots = float(shots_stats['SoT%'].max()) + 1
    line_shots = base_shots.mark_line(
        color="red",
        point=alt.OverlayMarkDef(color="black", opacity=0.2),
    ).encode(
        y=alt.Y('SoT%:Q', scale=alt.Scale(domain=[0, max_line_shots]),
                title="Shots on Target Percentage %"),
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('SoT%:Q', title='Percentage')
        ]
    )

    chart_shots = alt.layer(bar_shots, line_shots).resolve_scale(y="independent")
    chart_shots_json = chart_shots.to_json()
    off_stats = forwards_stats[['Player', 'Off']].copy()
    avg_off = round(float(off_stats['Off'].mean()))
    off_stats['AvgOff'] = avg_off
    area_data = pd.DataFrame({
        'AvgOff': [avg_off],
        'HighestOffside':[float(off_stats['Off'].max())],
        'Zero':[0]
    })
    below_avg = alt.Chart(area_data).mark_rect(opacity=0.1).encode(
        y='Zero',
        y2='AvgOff',
        color=alt.ColorValue("#10ba0d")
    )
    above_avg = alt.Chart(area_data).mark_rect(opacity=0.1).encode(
        y='AvgOff',
        y2='HighestOffside',
        color=alt.ColorValue("#FF0000")
    )
    chart_off = alt.Chart(off_stats).mark_bar().encode(
        x=alt.X('Player:N'),
        y=alt.Y('Off:Q', title='Offside'),
        color=alt.Color('Player:N'),
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('Off:Q', title='Offside')
        ]
    )
    line_off = alt.Chart(off_stats).mark_rule(color='blue').encode(
        y='AvgOff:Q',
        tooltip=[
            alt.Tooltip('AvgOff:N', title='Average Offside'),
        ]
    )
    chart_off = below_avg + above_avg + chart_off + line_off
    chart_off_json = chart_off.to_json()
    return chart_apps_json, chart_ga_json, chart_cards_json,chart_shots_json,chart_off_json