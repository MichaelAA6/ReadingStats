import altair as alt
import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[4]
print(root)
png_path1 = root / 'images' / 'josh_knight_welcome1.png'
json_path1 = root / 'app' / 'static' / 'jsons' / 'players' / 'JK' / 'josh_knight_welcome1.json'
png_path2 = root / 'images' / 'josh_knight_welcome2.png'
json_path2 = root / 'app' / 'static' / 'jsons' / 'players' / 'JK' / 'josh_knight_welcome2.json'
png_path3 = root / 'images' / 'josh_knight_welcome3.png'
json_path3 = root / 'app' / 'static' / 'jsons' / 'players' / 'JK' / 'josh_knight_welcome3.json'


data =[
    ["Player","Pass%","LongBall%","Duels%","Aerial_Duels%","Defensive Contributions","Recoveries","Interceptions","Tackles"],
    ["Josh Knight",79.1,37.9,56.6,51.7,9.54,3.80,0.74,0.56],
    ["Dan Scarr",81.0,35.2,59.2,66.3,10.39,1.63,0.95,0.14],
    ["Hayden Matthews",82.6,29.6,57.0,52.8,10.13,2.19,1.15,1.38]
]

df = pd.DataFrame(data[1:],columns=data[0])

pass_stats = df.melt(
    id_vars=['Player'],
    value_vars=["Pass%","LongBall%"],
    var_name='Passing',
    value_name='Value',
)

pass_chart = alt.Chart(pass_stats).mark_bar().encode(
    x=alt.X('Player:N',sort=['Udoka Malfie']),
    y=alt.Y('sum(Value):Q',title='Pass%'),
    xOffset = 'Passing:N',
    color=alt.Color('Passing:N',
                    scale=alt.Scale(
                        domain=['Pass%', 'LongBall%'],
                        range=['#2e2b5c', '#004a1e']
                    ),),
    tooltip=[
        alt.Tooltip('Player:N',title='Player Name'),
        alt.Tooltip('Passing:N',title='Passing Type'),
        alt.Tooltip('Value:Q',title='Total'),
    ]
)
pass_text = pass_chart.mark_text(
    align='center',
    dy=-10,
    size=17
).encode(
    y=alt.Y('sum(Value):Q'),
    text=alt.Text('sum(Value):Q'),
)
pass_chart = (pass_chart + pass_text).properties(width=500, height=800)

pass_chart.save(png_path1,scale_factor=2)
pass_chart.save(json_path1)


duels_stats = df.melt(
    id_vars=['Player'],
    value_vars=["Duels%","Aerial_Duels%"],
    var_name = 'Duel Type',
    value_name = 'Value'
)

duel_chart = alt.Chart(duels_stats).mark_bar().encode(
    x=alt.X('Player:N',sort=['Udoka Malfie']),
    y=alt.Y('sum(Value):Q',title='Duel%'),
    xOffset = 'Duel Type:N',
    color=alt.Color('Duel Type:N',
                    scale=alt.Scale(
                        domain=['Duels%', 'Aerial_Duels%'],
                        range=['#096310', '#09e2ed']
                    )),
    tooltip = [
        alt.Tooltip('Player:N',title='Player Name'),
        alt.Tooltip('Duel Type:N',title='Duel Type'),
        alt.Tooltip('Value:Q',title='Total'),
    ]
)

duel_text = duel_chart.mark_text(
    align='center',
    dy=-10,
    size=17
).encode(
    y=alt.Y('sum(Value):Q'),
    text=alt.Text('sum(Value):Q'),
)
duel_chart = (duel_chart + duel_text).properties(width=500, height=800)

duel_chart.save(png_path2,scale_factor=2)
duel_chart.save(json_path2)

def_stats = df.melt(
    id_vars=['Player'],
    value_vars=["Defensive Contributions","Recoveries","Interceptions","Tackles"],
    var_name = 'Def Type',
    value_name = 'Value'
)

def_chart = alt.Chart(def_stats).mark_bar().encode(
    x=alt.X('Player:N',sort=['Udoka Malfie']),
    y=alt.Y('sum(Value):Q',title='Defensive Stats Per 90'),
    xOffset = 'Def Type:N',
    color=alt.Color('Def Type:N',
                    scale=alt.Scale(
                        domain=['Defensive Contributions','Recoveries', 'Interceptions', 'Tackles'],
                        range=['#ffd900','#148c26', '#1017cc','#eb3c07']
                    )),
    tooltip = [
        alt.Tooltip('Player:N',title='Player Name'),
        alt.Tooltip('Def Type:N',title='Def Type'),
        alt.Tooltip('Value:Q',title='Total'),
    ]
)

def_text = def_chart.mark_text(
    align='center',
    dy=-10,
    size=17
).encode(
    y=alt.Y('sum(Value):Q'),
    text=alt.Text('sum(Value):Q'),
)
def_chart = (def_chart + def_text).properties(width=500, height=800)
def_chart.save(png_path3,scale_factor=2)
def_chart.save(json_path3)