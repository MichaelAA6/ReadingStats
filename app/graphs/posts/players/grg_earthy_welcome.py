"""
    grg_earthy_welcome.py
"""
import altair as alt
import pandas as pd
from pathlib import Path
root = Path(__file__).resolve().parents[4]
png_path1 = root / 'images' / 'grg_earthy_welcome1.png'
json_path1 = root / 'app' / 'static' / 'jsons' / 'players' / 'GE' / 'grg_earthy_welcome1.json'
png_path2 = root / 'images' / 'grg_earthy_welcome2.png'
json_path2 = root / 'app' / 'static' / 'jsons' / 'players' / 'GE' / 'grg_earthy_welcome2.json'
png_path3 = root / 'images' / 'grg_earthy_welcome3.png'
json_path3 = root / 'app' / 'static' / 'jsons' / 'players' / 'GE' / 'grg_earthy_welcome3.json'

data =[
    ["Player","Pass%90","Longball%90","Dribble%90","G+A90","ExpG+A90"],
    ["George Earthy",86.6,33.3,23.1,0.25,0.29],
    ["Romaine Mundle",82.8,58.8,43.2,0.43,0.30],
    ["Jesurun Rak-Sakyi",80.6,39.1,54.7,0.46,0.50]
]

df = pd.DataFrame(data[1:],columns=data[0])

pass_stats = df.melt(
    id_vars=['Player'],
    value_vars=['Pass%90','Longball%90'],
    var_name='Pass Type',
    value_name='Count'
)

pass_chart = alt.Chart(pass_stats).mark_bar().encode(
    x=alt.X('Player:N',title='Player'),
    y=alt.Y('sum(Count):Q',title='Pass/Long Ball'),
    xOffset='Pass Type:N',
    color=alt.Color('Pass Type:N',
                    scale=alt.Scale(
                        domain=['Pass%90','Longball%90',],
                        range=['green','blue']
                    )),
    tooltip=[
        alt.Tooltip('Player:N', title='Player'),
        alt.Tooltip('Pass Type:N', title='Pass/Long Ball % per 90'),
        alt.Tooltip('Count:Q', title='Count')
    ]

)

pass_text = pass_chart.mark_text(
    align='center',
    dy=-10,
    size=17
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q')
)

pass_chart = (pass_chart + pass_text).properties(width=500,height=800)

pass_chart.save(png_path1,scale_factor=2.0)
pass_chart.save(json_path1)

dribble_stats = df.melt(
    id_vars=['Player'],
    value_vars=['Dribble%90'],
    var_name='Dribble Type',
    value_name='Count'
)

dribble_chart = alt.Chart(dribble_stats).mark_bar().encode(
    x=alt.X('Player:N',title='Player'),
    y=alt.Y('sum(Count)',title='Dribble Percentage per 90'),
    xOffset='Dribble Type:N',
    color=alt.Color('Dribble Type:N',scale=alt.Scale(
        domain=['Dribble%90'],
        range=['red']
    )),
    tooltip=[
        alt.Tooltip('Player:N', title='Player'),
        alt.Tooltip('Dribble Type', title='Dribble Type'),
        alt.Tooltip('Count:Q', title='Count')
    ]
)

dribble_text = dribble_chart.mark_text(
    align='center',
    dy=-10,
    size=17
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q'),
)

dribble_chart = (dribble_chart + dribble_text).properties(width=500,height=800)

dribble_chart.save(png_path2,scale_factor=2.0)
dribble_chart.save(json_path2)

ga_stats = df.melt(
    id_vars=['Player'],
    value_vars=["G+A90","ExpG+A90"],
    var_name='GA Type',
    value_name='Count'
)
ga_chart = alt.Chart(ga_stats).mark_bar().encode(
    x=alt.X('Player:N',title='Player'),
    y=alt.Y('sum(Count):Q',title='G+A/Expected G+A per 90'),
    xOffset='GA Type:N',
    color=alt.Color('GA Type:N',scale=alt.Scale(
        domain=['G+A90','ExpG+A90'],
        range=['#002d62','#cfb381']
    )),
    tooltip=[
        alt.Tooltip('Player:N', title='Player'),
        alt.Tooltip('GA Type:N', title='GA Type'),
        alt.Tooltip('Count:Q', title='Count')
    ]
)
ga_text = ga_chart.mark_text(
    align='center',
    dy=-10,
    size=17
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q')
)
ga_chart = (ga_chart + ga_text).properties(width=500,height=800)
ga_chart.save(png_path3,scale_factor=2.0)
ga_chart.save(json_path3)