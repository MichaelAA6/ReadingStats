"""
    historical_graph.py
    Used to return the historical graphs used on the website
    :returns
"""
import os
import altair as alt
import pandas as pd
from flask import current_app

def historical_graph():
    #find position database and create a pd Frame
    csv_path = os.path.join(current_app.root_path, 'db', 'historical_positions.csv')
    stats = pd.read_csv(csv_path)
    #check goal values are error free
    stats['Goals'] = pd.to_numeric(stats['Goals'],errors='coerce')

    """Position Chart"""

    #define the different league areas
    league_areas= pd.DataFrame({
        "PremTop":[0],
        "PremBottom":[20],
        "ChampBottom":[44],
        "L1Bottom":[68],
        "L2Bottom":[92],
    })
    #create areas which will display the different leagues with colours
    prem_area = alt.Chart(league_areas).mark_rect(opacity=0.1).encode(
        y="PremTop",
        y2="PremBottom",
        color=alt.ColorValue("#199c10")
    )
    champ_area = alt.Chart(league_areas).mark_rect(opacity=0.1).encode(
        y="PremBottom",
        y2="ChampBottom",
        color=alt.ColorValue("#3168de")
    )
    L1_area = alt.Chart(league_areas).mark_rect(opacity=0.1).encode(
        y="ChampBottom",
        y2="L1Bottom",
        color=alt.ColorValue("#f8ff26")
    )
    L2_area = alt.Chart(league_areas).mark_rect(opacity=0.1).encode(
        y="L1Bottom",
        y2="L2Bottom",
        color=alt.ColorValue("#d60d0d")
    )
    #create line graph
    position_chart = alt.Chart(stats).mark_line(
        #make dots so its easier to hover over
        point=alt.OverlayMarkDef(color="black", opacity=0.7)
    ).encode(
        #x-axis is the season
        x=alt.X('Season:N'),
        #y-axis is the position of the clubs in the 92
        y=alt.Y('Position92:Q',scale=alt.Scale(
            #sets the domain and reverses graph so 1st is at top
            domain=[1,92],reverse=True,nice=False,padding=0),title="Position"),
        #display all infor when hovering
        tooltip=[
            alt.Tooltip('Season:N',title="Season"),
            alt.Tooltip('Division:N',title="Division"),
            alt.Tooltip('Position:Q',title="Position in League"),
            alt.Tooltip('Position92:Q',title="Position in 92"),
            alt.Tooltip('TopGoal:N',title="Top Goal Scorer"),
            alt.Tooltip('Goals:Q',title="Goals"),
            alt.Tooltip('Event:N',title="Events"),
        ],
    ).properties(
        height=900,
        width=900
    )
    position_chart = prem_area + champ_area + L1_area + L2_area + position_chart
    position_chart_json = position_chart.to_json()

    """Top Scorer Chart"""

    tgs_bar = alt.Chart(stats).mark_bar().encode(
        x=alt.X('Season:N',scale=alt.Scale(paddingInner=0.5)),
        y=alt.Y('Goals:Q'),
        color=alt.Color('TopGoal:N', legend=None,scale=alt.Scale(scheme='tableau20')),
        tooltip=[
            alt.Tooltip('Season:N',title="Season"),
            alt.Tooltip('Division:N',title="Division"),
            alt.Tooltip('TopGoal:N',title="Top Goal Scorer"),
            alt.Tooltip('Goals:Q',title="Goals"),
        ]
    )
    tgs_text = tgs_bar.mark_text(
        align='center',
        baseline='bottom',
        fontSize=12,
        angle=270,
        dx=45,
        dy=5,
    ).encode(
        text=alt.Text('TopGoal:N'),
        color=alt.value('black')
    )
    tgs_chart = tgs_bar + tgs_text
    tgs_chart_json = tgs_chart.to_json()
    return position_chart_json, tgs_chart_json


