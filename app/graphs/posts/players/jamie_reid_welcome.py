import altair as alt
import pandas as pd
from pathlib import Path
root = Path(__file__).resolve().parents[4]

data = [
    ["Player","Shots90","SoT90","HdSt90","xG90","Chances90","Duels%90","Aerial_Duels%90"],
    ["Jamie Reid",2.13,1.07,0.31,0.38,0.55,29.2,31.7],
    ["Jack Marriott",2.75,1.53,0.36,0.38,0.86,22.1,16.1],
    ["Joe Taylor",2.67,1.38,0.20,0.5,0.20,29.3,28.0]
]
png_path1 = root / 'images' / 'jamie_reid_welcome1.png'
json_path1 = root / 'app' / 'static' / 'jsons' / 'players' / 'JR' / 'jamie_reid_welcome1.json'
png_path2 = root / 'images' / 'jamie_reid_welcome2.png'
json_path2 = root / 'app' / 'static' / 'jsons' / 'players' / 'JR' / 'jamie_reid_welcome2.json'
png_path3 = root / 'images' / 'jamie_reid_welcome3.png'
json_path3 = root / 'app' / 'static' / 'jsons' / 'players' / 'JR' / 'jamie_reid_welcome3.json'

df = pd.DataFrame(data[1:],columns=data[0])

attacking_stats = df.melt(
    id_vars=['Player'],
    value_vars=["Shots90","SoT90","HdSt90"],
    var_name='Attacking',
    value_name='Count'
)
attack_chart = alt.Chart(attacking_stats).mark_bar().encode(
    x=alt.X('Player:N',sort=['Jamie Reid']),
    y=alt.Y('sum(Count):Q',title="Attacking per 90"),
    xOffset= 'Attacking',
    color=alt.Color('Attacking:N',
                    scale=alt.Scale(
                        domain=["Shots90","SoT90","HdSt90"],
                        range=["#ffbb00","#c20e0e","#cdd400"]
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

chance_stats = df.melt(
    id_vars=['Player'],
    value_vars=["xG90","Chances90"],
    var_name='Chance',
    value_name='Count'
)
chance_chart = alt.Chart(chance_stats).mark_bar().encode(
    x=alt.X('Player:N',sort=['Jamie Reid']),
    y=alt.Y('sum(Count):Q'),
    xOffset= 'Chance',
    color=alt.Color('Chance:N',
                    scale=alt.Scale(
                        domain=["xG90","Chances90"],
                        range=["#0a8018","#0c1bed"]
                    )),
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
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q'),
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
    x=alt.X('Player:N',sort=['Jamie Reid']),
    y=alt.Y('sum(Count):Q',title="Duels percentage per 90"),
    xOffset= 'Dueling',
    color=alt.Color('Dueling:N',
                    scale=alt.Scale(
                        domain=["Duels%90","Aerial_Duels%90"],
                        range=["#096310","#09e2ed"],
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