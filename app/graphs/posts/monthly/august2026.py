import altair as alt
import pandas as pd
from pathlib import Path


root = Path(__file__).resolve().parents[4]

data = [
    ["ID","Game","Possession","Goals","xG","Goals Conceded","xG Faced","Pass%","Long Ball%","Cross%"],
    [1,"Bromley(A)",59,1,2.39,1,1.67,78,37,33],
    [2,"Luton(H)",41,3,1.61,4,1.65,70,44,11],
    [3,"Wycombe(H)",48,1,0.92,1,1.25,78,28,17],
    [4,"Wimbledon(A)",63,0,1.28,0,0.37,80,25,20],
    [5,"Stevenage(A)",43,3,1.70,0,0.72,78,38,22]
]

df = pd.DataFrame(data[1:],columns=data[0])
png_path1 = root / 'images' / 'possession.png'
json_path1 = root / 'app' / 'static' / 'jsons' / 'monthly' / 'august2026' / 'possession.json'
png_path2 = root / 'images' / 'attacking.png'
json_path2 = root / 'app' / 'static' / 'jsons' / 'monthly' / 'august2026' / 'attacking.json'
png_path3 = root / 'images' / 'defence.png'
json_path3 = root / 'app' / 'static' / 'jsons' / 'monthly' / 'august2026' / 'defence.json'
png_path4 = root / 'images' / 'passing.png'
json_path4 = root / 'app' / 'static' / 'jsons' / 'monthly' / 'august2026' / 'passing.json'

possession_stats = df.melt(
    id_vars=["Game"],
    value_vars=["Possession"],
    var_name="Type",
    value_name="Count",
)

possession_chart = alt.Chart(possession_stats).mark_bar().encode(
    x=alt.X("Game",axis=alt.Axis(labelFontSize=20,titleFontSize=20),
            title="Matches",sort=["ID"]),
    y=alt.Y("sum(Count):Q",axis=alt.Axis(titleFontSize=20),title="Possession"),
    color=alt.Color("Type:N",
                    scale=alt.Scale(
                        domain=["Possession","Average Possession"],
                        range=["#002d62","black"]
    )),
    tooltip=[
        alt.Tooltip("Team:N",title="Match"),
        alt.Tooltip("Count:Q",title="Possession")
    ]
)
possession_avg = round(float(possession_stats["Count"].mean()))
possession_avg_line = alt.Chart(possession_stats).mark_rule(
    strokeWidth=4
).encode(
    y=alt.datum(possession_avg),
    tooltip=[
        alt.Tooltip("possession_avg:Q",title="Average Possession"),
    ]
)
possession_text = possession_chart.mark_text(
    align="center",
    dy=-10,
    size=23
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q')
)
possession_avg_text = possession_avg_line.mark_text(
    align="center",
    dy=-15,
    size=23
).encode(
    y=alt.datum(possession_avg),
    text=alt.value(f"Avg: {possession_avg}%")
)

possession_chart = (possession_chart + possession_avg_line +
                    possession_text + possession_avg_text
                    ).properties(width=1000,height=600)
possession_chart.save(png_path1,scale_factor=2.0)
possession_chart.save(json_path1)

attacking_stats = df.melt(
    id_vars=["Game"],
    value_vars=["Goals","xG"],
    var_name="Type",
    value_name="Count",
)

attacking_chart = alt.Chart(attacking_stats).mark_bar().encode(
    x=alt.X("Game", axis=alt.Axis(labelFontSize=20, titleFontSize=20),
            title="Matches",sort=["ID"]),
    y=alt.Y("sum(Count):Q",axis=alt.Axis(titleFontSize=20),title="Goals"),
    xOffset='Type:N',
    color=alt.Color("Type:N",
                    scale=alt.Scale(
                        domain=["Goals","Avg Goals","xG","Avg xG"],
                        range=["#002d62","#0066de","#cfb381","#ebac3d"]
    )),
    tooltip=[
        alt.Tooltip("Game:N",title="Match"),
        alt.Tooltip("Type:N",title="Goals"),
        alt.Tooltip("Count:Q",title="Count"),
    ]
)

goals_avg = float(attacking_stats.loc[attacking_stats["Type"] == "Goals", "Count"].mean())
xG_avg = float(attacking_stats.loc[attacking_stats["Type"] == "xG", "Count"].mean())

goals_avg_line = alt.Chart(attacking_stats).mark_rule(
    strokeWidth=4,
    color="#0066de"
).encode(
    y=alt.datum(goals_avg),
    tooltip=[
        alt.Tooltip("goals_avg:Q",title="Average Goals"),
    ]
)
xG_avg_line = alt.Chart(attacking_stats).mark_rule(
    strokeWidth=4,
    color="#ebac3d"
).encode(
    y=alt.datum(xG_avg),
    tooltip=[
        alt.Tooltip("xG_avg:Q",title="Average xG"),
    ]
)

attacking_text = attacking_chart.mark_text(
    align="center",
    dy=-10,
    size=23
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q')
)
goals_avg_text = alt.Chart().mark_text(
    align="left",
    dy=-15,
    dx=-500,
    size=23,
    color="#0066de"
).encode(
    y=alt.datum(goals_avg),
    text=alt.value(f"Avg: {goals_avg:.3f}")
)

xG_avg_text = alt.Chart().mark_text(
    align="right",
    dy=-15,
    dx=300,
    size=23,
    color="#ebac3d"
).encode(
    y=alt.datum(xG_avg),
    text=alt.value(f"Avg: {xG_avg:.3f}")
)

attacking_chart = (attacking_chart + goals_avg_line + xG_avg_line +
                   attacking_text + goals_avg_text + xG_avg_text
                   ).properties(width=1000,height=600)

attacking_chart.save(png_path2,scale_factor=2.0)
attacking_chart.save(json_path2)

defence_stats = df.melt(
    id_vars=["Game"],
    value_vars=["Goals Conceded","xG Faced"],
    var_name="Type",
    value_name="Count",
)

defence_chart = alt.Chart(defence_stats).mark_bar().encode(
    x=alt.X("Game", axis=alt.Axis(labelFontSize=20, titleFontSize=20),
            title="Matches", sort=["ID"]),
    y=alt.Y("sum(Count):Q",axis=alt.Axis(titleFontSize=20),title="Goals Conceded"),
    xOffset='Type:N',
    color=alt.Color("Type:N",
                    scale=alt.Scale(
                        domain=["Goals Conceded","Avg Goals Conceded","xG Faced","Avg xG Faced"],
                        range=["#002d62","#0066de","#cfb381","#ebac3d"]
                    )),
    tooltip=[
        alt.Tooltip("Game:N",title="Match"),
        alt.Tooltip("Type:N",title="Goals Conceded"),
        alt.Tooltip("Count:Q",title="Count"),
    ]

)

goals_conceded_avg = float(defence_stats.loc[defence_stats["Type"] == "Goals Conceded", "Count"].mean())
xG_faced_avg = float(defence_stats.loc[defence_stats["Type"] == "xG Faced", "Count"].mean())

goals_conceded_avg_line = alt.Chart(defence_stats).mark_rule(
    strokeWidth=4,
    color="#0066de"
).encode(
    y=alt.datum(goals_conceded_avg),
    tooltip=[
        alt.Tooltip("goals_conceded_avg:Q",title="Average Goals Conceded"),
    ]
)
xG_faced_avg_line = alt.Chart(defence_stats).mark_rule(
    strokeWidth=4,
    color="#ebac3d"
).encode(
    y=alt.datum(xG_faced_avg),
    tooltip=[
        alt.Tooltip("xG_faced_avg:Q",title="Average xG Faced"),
    ]
)
defence_text = defence_chart.mark_text(
    align="center",
    dy=-10,
    size=23
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q')
)
goals_conceded_avg_text = alt.Chart().mark_text(
    align="left",
    dy=-15,
    dx=-500,
    size=23,
    color="#0066de"
).encode(
    y=alt.datum(goals_conceded_avg),
    text=alt.value(f"Avg: {goals_conceded_avg:.3f}")
)
xG_faced_avg_text = alt.Chart().mark_text(
    align="right",
    dy=15,
    dx=500,
    size=23,
    color="#ebac3d"
).encode(
    y=alt.datum(xG_faced_avg),
    text=alt.value(f"Avg: {xG_faced_avg:.3f}")
)

defence_chart = (defence_chart + goals_conceded_avg_line + xG_faced_avg_line +
                 defence_text + goals_conceded_avg_text + xG_faced_avg_text
                 ).properties(width=1000,height=600)
defence_chart.save(png_path3,scale_factor=2.0)
defence_chart.save(json_path3)

passing_stats = df.melt(
    id_vars=["Game"],
    value_vars=["Pass%","Long Ball%","Cross%"],
    var_name="Type",
    value_name="Count",
)
passing_chart = alt.Chart(passing_stats).mark_bar().encode(
    x=alt.X("Game",axis=alt.Axis(labelFontSize=20,titleFontSize=20),
            title="Matches",sort=["ID"],),
    y=alt.Y("sum(Count):Q",axis=alt.Axis(titleFontSize=20),title="Passing%"),
    xOffset='Type:N',
    color=alt.Color("Type:N",
                    scale=alt.Scale(
                        domain=["Pass%","Avg Pass%","Long Ball%",
                                "Avg Long Ball%","Cross%","Avg Cross%"],
                        range=["#0a7d14","#095214","#1609d6","#090f80","#c72614","#961717"]

    )),
    tooltip=[
        alt.Tooltip("Game:N",title="Match"),
        alt.Tooltip("Type:N",title="Passing"),
        alt.Tooltip("Count:N",title="Count"),
    ]
)

pass_avg = float(passing_stats.loc[passing_stats["Type"] == "Pass%","Count"].mean())
long_ball_avg = float(passing_stats.loc[passing_stats["Type"] == "Long Ball%","Count"].mean())
cross_avg = float(passing_stats.loc[passing_stats["Type"] == "Cross%","Count"].mean())

pass_avg_line = alt.Chart(passing_stats).mark_rule(
    strokeWidth=4,
    color="#095214"
).encode(
    y=alt.datum(pass_avg),
    tooltip=[
        alt.Tooltip("pass_avg:Q",title="Average Pass%"),
    ]
)
long_ball_line = alt.Chart(passing_stats).mark_rule(
    strokeWidth=4,
    color="#090f80"
).encode(
    y=alt.datum(long_ball_avg),
    tooltip=[
        alt.Tooltip("long_ball_avg:Q",title="Average Long Ball%"),
    ]
)
cross_avg_line = alt.Chart(passing_stats).mark_rule(
    strokeWidth=4,
    color="#961717"
).encode(
    y=alt.datum(cross_avg),
    tooltip=[
        alt.Tooltip("cross_avg:Q",title="Average Cross%"),
    ]
)

passing_text = passing_chart.mark_text(
    align="center",
    dy=-10,
    size=23
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q')
)
pass_avg_text = alt.Chart().mark_text(
    align="left",
    dy=-15,
    size=23,
    color="#095214"
).encode(
    y=alt.datum(pass_avg),
    text=alt.value(f"Avg: {pass_avg:.1f}%")
)
long_ball_avg_text = alt.Chart().mark_text(
    align="left",
    dy=-15,
    size=23,
    color="#090f80"
).encode(
    y=alt.datum(long_ball_avg),
    text=alt.value(f"Avg: {long_ball_avg:.1f}%")
)
cross_avg_text = alt.Chart().mark_text(
    align="left",
    dy=-15,
    size=23,
    color="#961717"
).encode(
    y=alt.datum(cross_avg),
    text=alt.value(f"Avg: {cross_avg:.1f}%")
)

passing_chart = (passing_chart + passing_text + pass_avg_line + long_ball_line +
                 cross_avg_line + pass_avg_text + long_ball_avg_text + cross_avg_text
                 ).properties(width=1000,height=600)
passing_chart.save(png_path4,scale_factor=2.0)
passing_chart.save(json_path4)