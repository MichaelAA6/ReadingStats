import altair as alt
import pandas as pd
from pathlib import Path
root = Path(__file__).resolve().parents[4]

data = [
    ["Player","SoT90","HdSt90","ExG90","Chances90","Duels%90","Aerial_Duels%90"],
    ["Jacob Brown",1.11,0.92,0.36,0.92,27.7,30.2],
    ["Jack Marriott",1.53,0.36,0.38,0.86,22.1,16.1],
    ["Lars-Jørgen Salvesen",1.32,0.94,0.54,0.94,34.0,41.0]
]
png_path1 = root / 'images' / 'jacob_brown_welcome1.png'
json_path1 = root / 'app' / 'static' / 'jsons' / 'players' / 'JB' / 'jacob_brown_welcome1.json'
png_path2 = root / 'images' / 'jacob_brown_welcome2.png'
json_path2 = root / 'app' / 'static' / 'jsons' / 'players' / 'JB' / 'jacob_brown_welcome2.json'
png_path3 = root / 'images' / 'jacob_brown_welcome3.png'
json_path3 = root / 'app' / 'static' / 'jsons' / 'players' / 'JB' / 'jacob_brown_welcome3.json'

df = pd.DataFrame(data[1:],columns=data[0])

attacking_stats = df.melt(
    id_vars=['Player'],
    value_vars=["SoT90","HdSt90","ExG90"],
    var_name='Attacking',
    value_name='Count'
)
attack_chart = alt.Chart(attacking_stats).mark_bar().encode(
    x=alt.X('Player:N',sort=['Jacob Brown']),
    y=alt.Y('sum(Count):Q',title="Attacking per 90"),
    xOffset= 'Attacking',
    color=alt.Color('Attacking:N',
                    scale=alt.Scale(
                        domain=["SoT90","HdSt90","ExG90"],
                        range=["#9c8205","#0c36cf","#d1493d"]
                    )),
    tooltip=[
        alt.Tooltip('Player:N',title='Player Name'),
        alt.Tooltip('Attacking:N',title='Attacking per 90'),
        alt.Tooltip('Count:Q',title='Total'),
    ]
)

attack_text = attack_chart.mark_text(
    align='center',
    dy= -10,
    size= 17,
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q',)
)

attack_chart = (attack_chart + attack_text).properties(width=500,height=800)
attack_chart.save(png_path1,scale_factor=2)
attack_chart.save(json_path1)

chance_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('Player:N',sort=['Jacob Brown']),
    y=alt.Y('Chances90:Q'),
    color=alt.Color('Chances90:N'),
    tooltip=[
        alt.Tooltip('Player:N',title='Player Name'),
        alt.Tooltip('Chances90:Q',title='Chances per 90'),
    ]
)

chance_text = chance_chart.mark_text(
    align='center',
    dy= -10,
    size=17,
).encode(
    y=alt.Y('Chances90:Q'),
    text=alt.Text('Chances90:N'),
)

chance_chart = (chance_chart + chance_text).properties(width=500,height=800)

chance_chart.save(png_path2,scale_factor=2)
chance_chart.save(json_path2)

duel_stats = df.melt(
    id_vars=['Player'],
    value_vars=["Duels%90","Aerial_Duels%90"],
    var_name='Dueling',
    value_name='Count'
)

duel_chart = alt.Chart(duel_stats).mark_bar().encode(
    x=alt.X('Player:N',sort=['Jacob Brown']),
    y=alt.Y('sum(Count):Q',title="Duels percentage per 90"),
    xOffset= 'Dueling',
    color=alt.Color('Dueling:N',
                    scale=alt.Scale(
                        domain=["Duels%90","Aerial_Duels%90"],
                        range=["#750c02","#1092c2"],
                    )),
    tooltip=[
        alt.Tooltip('Player:N',title='Player Name'),
        alt.Tooltip('Dueling:N',title='Dueling per 90'),
        alt.Tooltip('Count:Q',title='Dueling per 90'),
    ]

)

duel_text = duel_chart.mark_text(
    align='center',
    dy= -10,
    size=17,
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q'),
)

duel_chart = (duel_chart + duel_text).properties(width=500,height=800)
duel_chart.save(png_path3,scale_factor=2)
duel_chart.save(json_path3)