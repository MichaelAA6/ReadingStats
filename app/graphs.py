import os
import random

import altair as alt
import numpy as np
import pandas as pd
from flask import current_app

def home_graph():
    csv_path = os.path.join(current_app.root_path, 'player_data.csv')
    stats = pd.read_csv(csv_path)
    stats['Min'] = stats['Min'].replace({',': ''}, regex=True).astype(float)
    stats['Gls'] = pd.to_numeric(stats['Gls'], errors='coerce')
    goal_stats = stats[['Player', 'Gls', 'Min']].copy()
    goal_stats = goal_stats[(goal_stats['Gls'] > 0) & (goal_stats['Min'] > 0)]
    goal_stats['Rotation'] = np.random.uniform(0, 90, size=len(goal_stats))
    goal_stats['Color'] = [
        f"#{random.randint(0, 0xFFFFFF):06x}"
        for _ in range(len(goal_stats))
    ]


    chart = alt.Chart(goal_stats).mark_point(shape="diamond",size=4000,filled=True,opacity=0.8).encode(
        x=alt.X('Gls:Q', title='Goals'),
        y=alt.Y('Min:Q', title='Minutes'),
        tooltip=['Player', 'Gls', 'Min'],
        angle=alt.Angle('Rotation:Q', scale=alt.Scale(domain=[0, 90])),
        color=alt.Color('Color:N', scale=None)
    ).properties(
        width=400,  # Wider chart
        height=800  # Taller chart
    ).interactive()

    chart_json = chart.to_json()
    return chart_json

def goalkeepers_graph():
    csv_path = os.path.join(current_app.root_path, 'player_data.csv')
    stats = pd.read_csv(csv_path)
    stats['MP'] = pd.to_numeric(stats['MP'], errors='coerce')
    stats['CrdY'] = pd.to_numeric(stats['CrdY'], errors='coerce')
    stats['CrdR'] = pd.to_numeric(stats['CrdR'], errors='coerce')
    keeper_stats = stats[['Player','Pos','MP', 'CrdY', 'CrdR']].copy()
    keeper_stats = keeper_stats[(keeper_stats['Pos'] == 'GK')]
    chart_apps = alt.Chart(keeper_stats).encode(
        alt.Theta('MP:Q').stack(True),
        alt.Color('Player:N'),
        tooltip=[
            alt.Tooltip('Player:N',title = 'Players Name'),
            alt.Tooltip('MP:Q',title='Matches Played')
        ]

    )
    c1 = chart_apps.mark_arc(innerRadius=20, stroke="#fff")
    c2 = chart_apps.mark_text(radius=180,size=20).encode(
        text=alt.Text("MP:Q")
    )
    final_chart_apps = c1+c2
    chart_apps_json = final_chart_apps.to_json()

    cards_stats = keeper_stats[['Player','CrdY', 'CrdR']].copy()
    cards_stats = cards_stats.melt(
        id_vars='Player',
        value_vars=['CrdY', 'CrdR'],
        var_name = 'CardType',
        value_name = 'Cards'
    )
    cards_stats['CardType'] = cards_stats['CardType'].replace({
        'CrdY': 'Yellow Cards',
        'CrdR': 'Red Cards'
    })
    chart_cards = alt.Chart(cards_stats).mark_bar().encode(
        x=alt.X('Player:N'),
        y=alt.Y('sum(Cards):Q',title='Cards'),
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
    return chart_apps_json, chart_cards_json

def defenders_graph():
    csv_path = os.path.join(current_app.root_path, 'player_data.csv')
    stats = pd.read_csv(csv_path)
    stats['MP'] = pd.to_numeric(stats['MP'], errors='coerce')
    stats['CrdY'] = pd.to_numeric(stats['CrdY'], errors='coerce')
    stats['CrdR'] = pd.to_numeric(stats['CrdR'], errors='coerce')
    stats['Gls'] = pd.to_numeric(stats['Gls'], errors='coerce')
    stats['Ast'] = pd.to_numeric(stats['Ast'], errors='coerce')
    stats['G+A_p90'] = pd.to_numeric(stats['G+A_p90'], errors='coerce')
    defender_stats = stats[['Player','Pos','MP', 'Gls','Ast','G+A_p90','CrdY','CrdR']].copy()
    defender_stats = defender_stats[(defender_stats['Pos'] == 'DF')]
    chart_apps = alt.Chart(defender_stats).encode(
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
    ga_stats = defender_stats[['Player','Gls','Ast','G+A_p90']].copy()
    ga_stats = ga_stats.melt(
        id_vars=['Player','G+A_p90'],
        value_vars=['Gls','Ast'],
        var_name = 'Contribution Type',
        value_name = 'Count'
    )
    base_ga = alt.Chart(ga_stats).encode(
        alt.X('Player:N'),
    )
    max_bar = float(ga_stats.groupby(['Player', 'Contribution Type'])['Count'].sum().max()) + 1
    bar_ga = base_ga.mark_bar().encode(
        y=alt.Y('sum(Count):Q',scale=alt.Scale(domain=[0,max_bar]),
                title='Goals/Assists'),
        xOffset='Contribution Type:N',
        color=alt.Color('Contribution Type:N',
            scale=alt.Scale(
                domain=['Gls', 'Ast', 'G+A_p90'],
                range=['green', 'blue','red']
            )),
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('Contribution Type:N', title='Contribution Type'),
            alt.Tooltip('Count:Q', title='Value')
        ])
    max_line = float(ga_stats['G+A_p90'].max()) + 0.01
    line_ga = base_ga.mark_line(
        color="red",
        point = alt.OverlayMarkDef(color="black", opacity=0.2),
        ).encode(
        y=alt.Y('G+A_p90:Q',scale=alt.Scale(domain=[0,max_line]),
                title = "Goals + Assists Per 90"),
        tooltip=[
            alt.Tooltip('Player:N', title='Players Name'),
            alt.Tooltip('G+A_p90:Q', title='G+A per 90')
        ]
    )
    chart_ga = alt.layer(bar_ga, line_ga).resolve_scale(y="independent")
    chart_ga_json = chart_ga.to_json()
    cards_stats = defender_stats[['Player', 'CrdY', 'CrdR']].copy()
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
    return chart_apps_json,chart_ga_json,chart_cards_json