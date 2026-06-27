"""
    kyr_lisbie_welcome.py
    used to create the graphs used to show off kyreece lisbie stats to similar players
    :returns goals/assists and shooting graph
"""

import altair as alt
import pandas as pd

#store data for graph
data = [
    ["Player","Goals","Assists","G+A Per 90","Shots","Shots On Target","Shots On Target%"],
    ["Kyreece Lisbie",11,6,0.51,74,33,44.6],
    ["Harry Anderson",12,5,0.57,45,17,37.8],
    ["Calum Agius",6,2,0.24,36,14,38.9]
]

#store it as a dataframe

df = pd.DataFrame(data[1:],columns=data[0])

"""Goals and Assists Graph"""

#melt data for specific graph
ga_stats = df.melt(
    id_vars=['Player','G+A Per 90'],
    value_vars=['Goals','Assists'],
    var_name = 'Contribution Type',
    value_name= 'Count'
)
#create basic graph and set x axis to the players
base_ga = alt.Chart(ga_stats).encode(
    alt.X('Player:N',sort=['Kyreece Lisbie', 'Harry Anderson', 'Calum Agius'])
)
#create the bar part of the chart while also creating the scale and tooltip
bar_ga = base_ga.mark_bar().encode(
    y=alt.Y('sum(Count):Q',title='Goals/Assists',
            scale=alt.Scale(domain=(0, 15))),
    xOffset='Contribution Type:N',
    color=alt.Color('Contribution Type:N',
                    scale=alt.Scale(
                        domain=['Goals','Assists','G+A Per 90'],
                        range=['green','blue','red']
                    )),
    tooltip=[
        alt.Tooltip('Player:N',title='Player Name'),
        alt.Tooltip('Contribution Type:Q',title='Type of Contribution'),
        alt.Tooltip('Count:Q',title='Value'),
    ]
)
#create linge part of graph
line_ga = base_ga.mark_line(
    color='red',
    point = alt.OverlayMarkDef(color="black",opacity=0.7),
).encode(
    y=alt.Y('G+A Per 90:Q',title='Goals And Assists Per 90'),
    tooltip=[
        alt.Tooltip('Player:N',title='Player Name'),
        alt.Tooltip('G+A Per 90:Q',title='Goals + Assists Per 90'),
    ]

)
#create text part of graph
text_ga = base_ga.mark_text(
    align='center',
    dy=-10,
    size=17
).encode(
    y=alt.Y('G+A Per 90:Q'),
    text=alt.Text('G+A Per 90:N')
)
#combine all layers to create one graph
final_ga = alt.layer(bar_ga, line_ga,text_ga
                        ).resolve_scale(y="independent").properties(width=500,height=800)
#creates the json and png of graph
final_ga.save('../../../../images/kyr_lisbie_welcome1.png')
final_ga.save('../../jsons/kyr_lisbie_welcome1.json')

"""Shooting Graph"""

#create extra column used for displaying text
df['Shots On Target%_Label'] = df['Shots On Target%'].astype(str) + '%'

#create pd for shooting
shots_stats = df.melt(
    id_vars=['Player','Shots On Target%','Shots On Target%_Label'],
    value_vars=['Shots','Shots On Target'],
    var_name = 'Shot Type',
    value_name = 'Shots Count'
)
#create base graph with players on x axis
base_shots = alt.Chart(shots_stats).encode(
    alt.X('Player:N',sort=['Kyreece Lisbie', 'Harry Anderson', 'Calum Agius'])
)
#create bar part of graph along with scale
bar_shots = base_shots.mark_bar().encode(
    y=alt.Y('sum(Shots Count):Q',title='Shots'),
    xOffset='Shot Type:N',
    color=alt.Color('Shot Type:N',
                    scale=alt.Scale(
                        domain=['Shots', 'Shots On Target', 'Shots On Target%'],
                        range=['black', 'gold', 'red']
                    )
    ),
    tooltip = [
        alt.Tooltip('Player:N',title='Player Name'),
        alt.Tooltip('Shot Type:N',title='Shot Type'),
        alt.Tooltip('Shots Count:N',title='Shots'),
    ]
)
#create line part pf graph
line_shots = base_shots.mark_line(
    color='red',
    point = alt.OverlayMarkDef(color="black",opacity=0.7),
).encode(
    y=alt.Y('Shots On Target%:Q',
            title="Shots on Target Percentage %"),
    tooltip = [
        alt.Tooltip('Player:N',title='Player Name'),
        alt.Tooltip('Shots On Target%:Q',title='Value'),
    ]
)
#create text part of graph
text_shots = base_shots.mark_text(
    align='center',
    dy=-10,
    size=17
).encode(
    y=alt.Y('Shots On Target%:Q'),
    text=alt.Text('Shots On Target%_Label:N')
)
#combine the different layers and make sure the scale it correct
final_shots = alt.layer(bar_shots, line_shots,text_shots
                        ).resolve_scale(y="independent").properties(width=500,height=800)
#create the graphs
final_shots.save('../../../../images/kyr_lisbie_welcome2.png')
final_shots.save('../../jsons/kyr_lisbie_welcome2.json')