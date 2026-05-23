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
