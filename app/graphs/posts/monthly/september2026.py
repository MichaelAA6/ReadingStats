import altair as alt
import pandas as pd
from pathlib import Path


root = Path(__file__).resolve().parents[4]

data = [
    ["ID","Game","Possession","Goals","xG","Goals Conceded","xG Faced","Pass%","Long Ball%","Cross%"],
    [1,"Mansfield(H)",54,5,3.30,0,1.36,77,29,12],
    [2,"Blackpool(H)",34,3,3.52,1,0.53,70,33,25],
    [3,"Cambridge(A)",56,1,1.99,2,0.94,74,28,36],
    [4,"Brentford(H)",29,1,1.48,2,3.17,73,33,33],
    [5,"Notts County(H)",48,2,2.44,0,0.58,79,45,26],
    [6,"Wycombe(A)",45,2,1.25,2,1.96,75,34,20]
]

df = pd.DataFrame(data[1:],columns=data[0])
png_path1 = root / 'images' / 'possessionseptember2026.png'
json_path1 = root / 'app' / 'static' / 'jsons' / 'monthly' / 'september2026' / 'possession.json'
png_path2 = root / 'images' / 'attackingseptember2026.png'
json_path2 = root / 'app' / 'static' / 'jsons' / 'monthly' / 'september2026' / 'attacking.json'
png_path3 = root / 'images' / 'defenceseptember2026.png'
json_path3 = root / 'app' / 'static' / 'jsons' / 'monthly' / 'september2026' / 'defence.json'
png_path4 = root / 'images' / 'passingseptember2026.png'
json_path4 = root / 'app' / 'static' / 'jsons' / 'monthly' / 'september2026' / 'passing.json'
png_path5 = root / 'images' / 'longballseptember2026.png'
json_path5 = root / 'app' / 'static' / 'jsons' / 'monthly' / 'september2026' / 'longball.json'
png_path6 = root / 'images' / 'crossseptember2026.png'
json_path6 = root / 'app' / 'static' / 'jsons' / 'monthly' / 'september2026' / 'cross.json'

#create dataframe just including the game and possession
possession_stats = df.melt(
    id_vars=["Game"],
    value_vars=["Possession"],
    var_name="Type",
    value_name="Count",
)

#create the bar graph for the possession
possession_chart = alt.Chart(possession_stats).mark_bar().encode(
    x=alt.X("Game",axis=alt.Axis(labelFontSize=20,titleFontSize=20),title="Matches",sort=["ID"]),
    y=alt.Y("sum(Count):Q",axis=alt.Axis(titleFontSize=20),title="Possession",
            scale=alt.Scale(domain=[20,70])),
    color=alt.Color("Type:N",
                    scale=alt.Scale(
                        domain=["Possession","Month Average Possession","Season Average Possession"],
                        range=["#002d62","#cfb381","#ebac3d"]
    )),
    tooltip=[
        alt.Tooltip("Team:N",title="Match"),
        alt.Tooltip("Count:Q",title="Possession")
    ]
)
#finds the avg possession for all games
possession_avg = round(float(possession_stats["Count"].mean()))
season_pos_avg = 51
#creates the line for the avg possession
possession_avg_line = alt.Chart(possession_stats).mark_rule(
    strokeWidth=4,color="#cfb381"
).encode(
    y=alt.datum(possession_avg),
    tooltip=[
        alt.Tooltip("possession_avg:Q",title="Average Month Possession"),
    ]
)

season_pos_line = alt.Chart(possession_stats).mark_rule(
    strokeWidth=4,color="#ebac3d"
).encode(
    y=alt.datum(season_pos_avg),
    tooltip=[
        alt.Tooltip("season_pos_avg:Q",title="Average Season Possession"),
    ]
)

#creates both text for the possession and avg
possession_text = possession_chart.mark_text(
    align="center",dy=-10,size=23
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q'))
possession_avg_text = possession_avg_line.mark_text(
    align="center",dy=-15,dx=80,size=23,color="#cfb381"
).encode(
    y=alt.datum(possession_avg),
    text=alt.value(f"Month Avg: {possession_avg}%")
)
season_pos_text = season_pos_line.mark_text(
    align="center",dy=-15,dx=100,size=23,color="#ebac3d"
).encode(
    y=alt.datum(season_pos_avg),
    text=alt.value(f"Season Avg: {season_pos_avg:.1f}%")
)

possession_chart = (possession_chart + possession_avg_line +
                    possession_text + possession_avg_text +
                    season_pos_line + season_pos_text).properties(width=1000,height=600)
possession_chart.save(png_path1,scale_factor=2.0)
possession_chart.save(json_path1)

#create dataframe for attacking including xG and Goals
attacking_stats = df.melt(
    id_vars=["Game"],
    value_vars=["Goals","xG"],
    var_name="Type",
    value_name="Count",
)

#create the bar chart that includes both Goals and xG
attacking_chart = alt.Chart(attacking_stats).mark_bar().encode(
    x=alt.X("Game", axis=alt.Axis(labelFontSize=20, titleFontSize=20),
            title="Matches",sort=["ID"]),
    y=alt.Y("sum(Count):Q",axis=alt.Axis(titleFontSize=20),title="Goals",
            scale=alt.Scale(domain=[0,5])),
    xOffset=alt.XOffset('Type:N',scale=alt.Scale(paddingInner=0.1)),
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

#finds both of the averages of goals and xG
goals_avg = float(attacking_stats.loc[attacking_stats["Type"] == "Goals", "Count"].mean())
xG_avg = float(attacking_stats.loc[attacking_stats["Type"] == "xG", "Count"].mean())

#create the avg line for both averages
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
#creates the text for the graph
attacking_text = attacking_chart.mark_text(
    align="center",
    dy=-30,
    size=23
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q')
)
goals_avg_text = alt.Chart().mark_text(
    align="left",
    dy=-15,
    size=23,
    color="#0066de"
).encode(
    y=alt.datum(goals_avg),
    text=alt.value(f"Avg: {goals_avg:.3f}")
)

xG_avg_text = alt.Chart().mark_text(
    align="right",
    dy=15,
    dx=110,
    size=23,
    color="#ebac3d"
).encode(
    y=alt.datum(xG_avg),
    text=alt.value(f"Avg: {xG_avg:.3f}")
)
#combine all elements
attacking_chart = (attacking_chart + goals_avg_line + xG_avg_line +
                    goals_avg_text + xG_avg_text + attacking_text
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
    y=alt.Y("sum(Count):Q",axis=alt.Axis(titleFontSize=20),title="Goals Conceded",
            scale=alt.Scale(domain=[0,3.2])),
    xOffset=alt.XOffset('Type:N',scale=alt.Scale(paddingInner=0.1)),
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
    dx=200,
    size=23,
    color="#0066de"
).encode(
    y=alt.datum(goals_conceded_avg),
    text=alt.value(f"Avg: {goals_conceded_avg:.3f}")
)
xG_faced_avg_text = alt.Chart().mark_text(
    align="right",
    dy=-15,
    dx=310,
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

pass_stats = df.melt(
    id_vars=["Game"],
    value_vars=["Pass%"],
    var_name="Type",
    value_name="Count",
)

pass_chart = alt.Chart(pass_stats).mark_bar().encode(
    x=alt.X("Game",axis=alt.Axis(labelFontSize=20,titleFontSize=20),
            title="Matches",sort=["ID"],),
    y=alt.Y("sum(Count):Q",axis=alt.Axis(titleFontSize=20),title="Passing%",
            scale=alt.Scale(domain=[69,80]),),
    xOffset='Type:N',
    color=alt.Color("Type:N",
                    scale=alt.Scale(
                        domain=["Pass%","Month Pass%","Season Pass%"],
                        range=["#002d62","#cfb381","#ebac3d"]

    )),
    tooltip=[
        alt.Tooltip("Game:N",title="Match"),
        alt.Tooltip("Count:N",title="Count"),
    ]
)
pass_avg = float(pass_stats.loc[pass_stats["Type"] == "Pass%","Count"].mean())
season_pass_avg = 76.8
pass_avg_line = alt.Chart(pass_stats).mark_rule(
    strokeWidth=4,
    color="#cfb381"
).encode(
    y=alt.datum(pass_avg),
    tooltip=[
        alt.Tooltip("pass_avg:Q",title="Month Average Pass%"),
    ]
)
last_pass_avg_line = alt.Chart(pass_stats).mark_rule(
    strokeWidth=4,
    color="#ebac3d"
).encode(
    y=alt.datum(season_pass_avg),
    tooltip=[
        alt.Tooltip("last_pass_avg:Q",title="Season Average Pass%"),
    ]
)

pass_text = pass_chart.mark_text(
    align="center",
    dy=-10,
    size=23
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q')
)
pass_avg_text = alt.Chart().mark_text(
    align="right",
    dy=-15,
    size=23,
    color="#cfb381"
).encode(
    y=alt.datum(pass_avg),
    text=alt.value(f"Month Avg: {pass_avg:.1f}%")
)
last_pass_avg_text = alt.Chart().mark_text(
    align="right",
    dy=-15,
    size=23,
    color="#ebac3d"
).encode(
    y=alt.datum(season_pass_avg),
    text=alt.value(f"Season Avg: {season_pass_avg:.1f}%")
)


pass_chart = (pass_chart + pass_avg_line + pass_text +
              pass_avg_text + last_pass_avg_line + last_pass_avg_text
              ).properties(width=600,height=1000)
pass_chart.save(png_path4,scale_factor=2.0)
pass_chart.save(json_path4)


longball_stats = df.melt(
    id_vars=["Game"],
    value_vars=["Long Ball%"],
    var_name="Type",
    value_name="Count",
)

longball_chart = alt.Chart(longball_stats).mark_bar().encode(
    x=alt.X("Game",axis=alt.Axis(labelFontSize=20,titleFontSize=20),
            title="Matches",sort=["ID"],),
    y=alt.Y("sum(Count):Q",axis=alt.Axis(titleFontSize=20),title="Passing%",
            scale=alt.Scale(domain=[10,50]),),
    xOffset='Type:N',
    color=alt.Color("Type:N",
                    scale=alt.Scale(
                        domain=["Long Ball%","Month Long Ball%","Season Long Ball%"],
                        range=["#002d62","#cfb381","#ebac3d"]

    )),
    tooltip=[
        alt.Tooltip("Game:N",title="Match"),
        alt.Tooltip("Count:N",title="Count"),
    ]
)

longball_avg = float(longball_stats.loc[longball_stats["Type"] == "Long Ball%","Count"].mean())
season_longball_avg = 34.4

longball_avg_line = alt.Chart(longball_stats).mark_rule(
    strokeWidth=4,
    color="#cfb381"
).encode(
    y=alt.datum(longball_avg),
    tooltip=[
        alt.Tooltip("longball_avg:Q",title="Month Average Longball%"),
    ]
)
season_longball_line = alt.Chart(longball_stats).mark_rule(
    strokeWidth=4,
    color="#ebac3d"
).encode(
    y=alt.datum(season_longball_avg),
    tooltip=[
        alt.Tooltip("season_longball_avg:Q",title="Season Average Longball%"),
    ]
)

longball_text = longball_chart.mark_text(
    align="center",
    dy=-25,
    size=23
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q')
)
longball_avg_text = alt.Chart().mark_text(
    align="center",
    dy=25,
    size=23,
    color="#cfb381"
).encode(
    y=alt.datum(longball_avg),
    text=alt.value(f"Month Avg: {longball_avg:.1f}%")
)
season_longball_text = alt.Chart().mark_text(
    align="center",
    dy=-15,
    size=23,
    color="#ebac3d"
).encode(
    y=alt.datum(season_longball_avg),
    text=alt.value(f"Season Avg: {season_longball_avg:.1f}%")
)


longball_chart = (longball_chart + longball_avg_line + longball_text +
              longball_avg_text + season_longball_line + season_longball_text
              ).properties(width=600,height=1000)
longball_chart.save(png_path5,scale_factor=2.0)
longball_chart.save(json_path5)




cross_stats = df.melt(
    id_vars=["Game"],
    value_vars=["Cross%"],
    var_name="Type",
    value_name="Count",
)

cross_chart = alt.Chart(cross_stats).mark_bar().encode(
    x=alt.X("Game",axis=alt.Axis(labelFontSize=20,titleFontSize=20),
            title="Matches",sort=["ID"],),
    y=alt.Y("sum(Count):Q",axis=alt.Axis(titleFontSize=20),title="Passing%",
            scale=alt.Scale(domain=[10,40]),),
    xOffset='Type:N',
    color=alt.Color("Type:N",
                    scale=alt.Scale(
                        domain=["Cross%","Month Cross%","Season Cross%"],
                        range=["#002d62","#cfb381","#ebac3d"]

    )),
    tooltip=[
        alt.Tooltip("Game:N",title="Match"),
        alt.Tooltip("Count:N",title="Count"),
    ]
)
cross_avg = float(cross_stats.loc[cross_stats["Type"] == "Cross%","Count"].mean())
season_cross_avg = 20.6
cross_avg_line = alt.Chart(cross_stats).mark_rule(
    strokeWidth=4,
    color="#cfb381"
).encode(
    y=alt.datum(cross_avg),
    tooltip=[
        alt.Tooltip("cross_avg:Q",title="Month Average Pass%"),
    ]
)
season_cross_line = alt.Chart(cross_stats).mark_rule(
    strokeWidth=4,
    color="#ebac3d"
).encode(
    y=alt.datum(season_cross_avg),
    tooltip=[
        alt.Tooltip("season_cross_avg:Q",title="Season Average Pass%"),
    ]
)

cross_text = cross_chart.mark_text(
    align="center",
    dy=-15,
    size=23
).encode(
    y=alt.Y('sum(Count):Q'),
    text=alt.Text('sum(Count):Q')
)
cross_avg_text = alt.Chart().mark_text(
    align="center",
    dy=-15,
    size=23,
    color="#cfb381"
).encode(
    y=alt.datum(cross_avg),
    text=alt.value(f"Month Avg: {cross_avg:.1f}%")
)
season_cross_text = alt.Chart().mark_text(
    align="center",
    dy=-15,
    size=23,
    color="#ebac3d"
).encode(
    y=alt.datum(season_cross_avg),
    text=alt.value(f"Season Avg: {season_cross_avg:.1f}%")
)


cross_chart = (cross_chart + cross_avg_line + cross_text +
              cross_avg_text + season_cross_line + season_cross_text
              ).properties(width=600,height=1000)
cross_chart.save(png_path6,scale_factor=2.0)
cross_chart.save(json_path6)
