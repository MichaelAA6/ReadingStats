import altair as alt
import pandas as pd
from pathlib import Path


root = Path(__file__).resolve().parents[4]

data = [
    ["Team","xG","Shots","Shots On Target","Touches in Opposition Box","Tackles","Interceptions","Blocks","Clearances","Pass%","LongBall%","Cross%"],
    ["Reading",0.9,12,3,33,8,6,1,40,80,26,20],
    ["Wimbledon",0.34,4,2,16,9,14,6,25,64,30,24]
]

png_path1 = root / 'images' / 'L1_wimbledon_a_1.png'
json_path1 = root / 'app' / 'static' / 'jsons' / 'matches' / '2627' / 'Wimbledon' / 'L1_wimbledon_a_1.json'
png_path2 = root / 'images' / 'L1_wimbledon_a_2.png'
json_path2 = root / 'app' / 'static' / 'jsons' / 'matches' / '2627' / 'Wimbledon' / 'L1_wimbledon_a_2.json'
png_path3 = root / 'images' / 'L1_wimbledon_a_3.png'
json_path3 = root / 'app' / 'static' / 'jsons' / 'matches' / '2627' / 'Wimbledon' / 'L1_wimbledon_a_3.json'

df = pd.DataFrame(data[1:],columns=data[0])

attacking_stats = df.melt(
    id_vars=["Team"],
    value_vars=["Shots","Shots On Target","Touches in Opposition Box"],
    var_name="Attacking",
    value_name="Count",
)

attack_chart = alt.Chart(attacking_stats).mark_bar().encode(
    x = alt.X('Team',sort=['Reading']),
    y = alt.Y('sum(Count):Q',title="Attacking Stats"),
    xOffset= 'Attacking',
    color=alt.Color('Attacking:N',
                    scale=alt.Scale(
                        domain=['Shots','Shots On Target','Touches in Opposition Box'],
                        range=["#0a7d14","#1609d6","#c72614"]
                    )),
    tooltip=[
        alt.Tooltip("Team:N",title="Team"),
        alt.Tooltip("Attacking:N",title="Attacking"),
        alt.Tooltip("Count:Q",title="Count"),
    ],
)

attack_text = attack_chart.mark_text(
    align="center",
    dy= -10,
    size= 17,
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q')
)

attack_chart = (attack_chart + attack_text).properties(width=500, height=800)
attack_chart.save(png_path1,scale_factor=2)
attack_chart.save(json_path1)

defending_stats = df.melt(
    id_vars=["Team"],
    value_vars=["Tackles","Interceptions","Blocks","Clearances"],
    var_name="Defending",
    value_name="Count",
)

defending_chart = alt.Chart(defending_stats).mark_bar().encode(
    x = alt.X('Team',sort=['Reading']),
    y = alt.Y('sum(Count):Q',title="Defending Stats"),
    xOffset= 'Defending',
    color=alt.Color('Defending:N',
                    scale=alt.Scale(
                        domain=['Tackles','Interceptions','Blocks','Clearances'],
                        range=["#0a7d14","#1609d6","#c72614","#f0f000"]
                    )),
    tooltip=[
        alt.Tooltip("Team:N",title="Team"),
        alt.Tooltip("Defending:N",title="Defending"),
        alt.Tooltip("Count:Q",title="Count"),
    ]
)

defending_text = defending_chart.mark_text(
    align="center",
    dy= -10,
    size= 17,
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q')
)
defending_chart = (defending_chart + defending_text).properties(width=500, height=800)
defending_chart.save(png_path2,scale_factor=2)
defending_chart.save(json_path2)

passing_stats = df.melt(
    id_vars=["Team"],
    value_vars=["Pass%","LongBall%","Cross%"],
    var_name="Passing",
    value_name="Count",
)

passing_chart = alt.Chart(passing_stats).mark_bar().encode(
    x = alt.X('Team',sort=['Reading']),
    y = alt.Y('sum(Count):Q',title="Passing Stats"),
    xOffset= 'Passing',
    color=alt.Color('Passing:N',
                    scale=alt.Scale(
                        domain=["Pass%","LongBall%","Cross%"],
                        range=["#0a7d14","#1609d6","#c72614"]
                    )),
    tooltip=[
        alt.Tooltip("Team:N",title="Team"),
        alt.Tooltip("Passing:N",title="Passing"),
        alt.Tooltip("Count:Q",title="Count"),
    ]
)

passing_text = passing_chart.mark_text(
    align="center",
    dy= -10,
    size= 17,
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q')
)
passing_chart = (passing_chart + passing_text).properties(width=500, height=800)
passing_chart.save(png_path3,scale_factor=2)
passing_chart.save(json_path3)