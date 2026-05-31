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
    csv_path = os.path.join(current_app.root_path, 'goalkeeper_data.csv')
    stats = pd.read_csv(csv_path)
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
    keeper_stats = stats[['Player','Pos','MP', 'CrdY', 'CrdR','GA','GA90','SoTA','Saves','Save%','CS','CS%']].copy()
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
    gc_stats = keeper_stats[['Player','GA','GA90']].copy()
    gc_stats = gc_stats.melt(
        id_vars=['Player','GA90'],
        value_vars='GA',
        var_name = 'Conceded Type',
        value_name = 'Conceded'
    )
    gc_stats['Conceded Type'] = gc_stats['Conceded Type'].replace({
        'GA': 'Goals Conceded',
        'GA90': 'Goals Conceded Per 90'
    })
    base_gc = alt.Chart(gc_stats).encode(
        x=alt.X('Player:N'),
    )
    max_bar = float(gc_stats.groupby(['Player', 'Contribution Type'])['Conceded'].sum().max()) + 20
    bar_gc = base_gc.mark_bar().encode(
        y = alt.Y('sum(Conceded):Q',
                  scale=alt.Scale(domain=[0, max_bar]),
                  title='Goals Conceded'),
        xOffset='Conceded Type:N',
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
    max_line = float(gc_stats['GA90'].max()) + 0.1
    line_gc = base_gc.mark_line(color="red",
                point=alt.OverlayMarkDef(color="black",opacity=0.2)).encode(
        y = alt.Y('GA90:Q',
                  scale=alt.Scale(domain=[0, max_line]),
                  title='Goals Conceded Per 90'),
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('Conceded:Q', title='Conceded Per 90')
        ]
    )
    chart_gc = alt.layer(bar_gc, line_gc).resolve_scale(y="independent")
    chart_gc_json = chart_gc.to_json()
    ks_stats = keeper_stats[['Player','SoTA','Saves','Save%']].copy()
    ks_stats = ks_stats.melt(
        id_vars=['Player','Save%'],
        value_vars=['SoTA','Saves'],
        var_name = 'Saves Type',
        value_name = 'Saved'
    )
    ks_stats['Saves Type'] = ks_stats['Saves Type'].replace({
        'SoTA': 'Shots Faced',
        'Saves': 'Saves',
    })
    base_ks = alt.Chart(ks_stats).encode(
        x=alt.X('Player:N'),
    )
    max_bar = float(ks_stats.groupby(['Player', 'Saves Type'])['Saved'].sum().max()) + 20
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
    line_ks = base_ks.mark_line(color="blue",
        point=alt.OverlayMarkDef(color="black",opacity=0.2)).encode(
        y = alt.Y('Save%:Q',scale=alt.Scale(domain=[0, max_line]),
                  title='Saves Percentage'),
        tooltip=[
            alt.Tooltip('Player:N', title='Player'),
            alt.Tooltip('Save%:N', title='Save Percentage'),
        ]
    )
    chart_ks = alt.layer(bar_ks, line_ks).resolve_scale(y="independent")
    chart_ks_json = chart_ks.to_json()
    cs_stats = keeper_stats[['Player','CS','CS%']].copy()
    cs_stats = cs_stats.melt(
        id_vars=['Player','CS%'],
        value_vars=['CS'],
        var_name = 'Clean Type',
        value_name = 'Clean'
    )
    base_cs = alt.Chart(cs_stats).encode(
        x=alt.X('Player:N'),
    )
    max_bar = float(cs_stats.groupby(['Player', 'Clean Type'])['Clean'].sum().max()) + 3
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
    graph_cs = alt.layer(bar_cs, line_cs).resolve_scale(y="independent")
    graph_cs_json = graph_cs.to_json()
    return chart_apps_json, chart_cards_json,chart_gc_json,chart_ks_json,graph_cs_json

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
    defender_stats = defender_stats[(defender_stats['Pos'] == 'DF') & (defender_stats['MP'] > 0)]
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

def midfielders_graph():
    csv_path = os.path.join(current_app.root_path, 'player_data.csv')
    stats = pd.read_csv(csv_path)
    stats['MP'] = pd.to_numeric(stats['MP'], errors='coerce')
    stats['CrdY'] = pd.to_numeric(stats['CrdY'], errors='coerce')
    stats['CrdR'] = pd.to_numeric(stats['CrdR'], errors='coerce')
    stats['Gls'] = pd.to_numeric(stats['Gls'], errors='coerce')
    stats['Ast'] = pd.to_numeric(stats['Ast'], errors='coerce')
    stats['G+A_p90'] = pd.to_numeric(stats['G+A_p90'], errors='coerce')
    midfielders_stats = stats[['Player', 'Pos', 'MP', 'Gls', 'Ast', 'G+A_p90', 'CrdY', 'CrdR']].copy()
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
    return chart_apps_json, chart_ga_json, chart_cards_json

def forwards_graph():
    csv_path = os.path.join(current_app.root_path, 'player_data.csv')
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
    forwards_stats = stats[['Player','Pos','MP', 'Gls','Ast','G+A_p90','Sh','SoT','SoT%','CrdY','CrdR']].copy()
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
    return chart_apps_json, chart_ga_json, chart_cards_json,chart_shots_json