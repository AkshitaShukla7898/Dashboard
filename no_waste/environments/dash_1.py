from datetime import date

import pandas as pd
import json
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__)

df=pd.read_csv('dummy.csv')
date_list=pd.read_csv('date_list.csv')
col=list(df.columns)
print(col[len(col)-1])
layout=[]
output=[]
input=[]
dat={}
dd1=[]
dd2=[]

ward_61 = json.load(open('ward_61.geojson', 'r'))


dfd = pd.read_csv('dummy_w.csv')
radio=list(dfd.columns)
radio.pop(0)
l = []

# handling null values in geojson
i = 0
for feature in ward_61['features']:
    if feature['properties']['name'] is None:
            feature['properties']['name'] = 'random_' + str(i)
            i += 1
    l.append(feature['properties']['name'])
i=0
building_id_map = {}

#mapping geojson with csv using id columns (osm_id)
for feature in ward_61["features"]:
    # feature["properties"]["oid"]=i
    feature["id"] = feature["properties"]["osm_id"]
    building_id_map[feature["properties"]["name"]] = feature["id"]

dfd["id"] = dfd["name"].apply(lambda x: building_id_map[x])

print(dfd)

#function to create marks on date slider


def slider_dic():
    dat={}
    d = date_list['Date'].unique()
    d.sort()
    j=0
    for i in d:
        dat[j] = i
        j+=1
    return dat

#marks dictionary for date slider

dat=slider_dic()

layout.append(dbc.Row(dbc.Col(html.H3("MY DASH"),
                        width={'size': 8, 'offset': 5},
                        ),
                ))
layout.append(dbc.Row(dbc.Col(html.P('Select Date'),
                              width={'size': 6},)))
layout.append(dbc.Row(dbc.Col(html.Div([
    dcc.Slider(
        id='my-slider',
        min=0,
        max=len(dat)-1,
        step=1,
        marks=dat,
        value=0,
    ),
    html.Div(id='slider-output-container',children=["date selected is: "+dat[0]])
]),
width=10), justify="center"
))

#adding dropdowns to layout

# for i in range(0,len(col)):
#     dd1.append(dbc.Col(
#         html.H4(col[i]),
#         width=3
#     ))
# layout.append(dbc.Row(dd1))

dd2.append(dbc.Col(html.Div([
    html.H4(col[0]),
    dcc.Dropdown(
      id=col[0],
      options=[{"label":x,"value":x} for x in df[col[0]].unique()]

 )]),
      width=3,
      xs=10, sm=6, md=6, lg=3, xl=3,
    ),

)

for i in range(1,len(col)):
    dd2.append(dbc.Col(html.Div([
        html.H4(col[i]),
        dcc.Dropdown(
        id=col[i],
        options=[]
    ),
        ]),
    width=3,
    xs=10, sm=6, md=6, lg=3, xl=3,),


    )

layout.append(dbc.Row(dd2,justify="center"))

# adding radio buttons
layout.append(dbc.Row(html.P("Select Waste Type:")))
layout.append(dbc.Row([
    dbc.Col([

    dcc.RadioItems(
        id='waste_type',
        options=[{'value': x, 'label': x}
                 for x in radio],
        value=radio[0],
        labelStyle={'display': 'inline-block'}
    )
    ], width=1)
]

))

layout.append(dbc.Row([
    dbc.Col([
        
        dcc.Graph(id='choropleth',figure={})

    ])
]))
# layout.append(html.P(col[0]))           #topmost dropdown
# layout.append(dcc.Dropdown(
#     id=col[0],
#     options=[{"label":x,"value":x} for x in df[col[0]].unique()]
# ))
# for i in range(1,len(col)):             #remaining dropdowns
#     layout.append(html.P(col[i]))
#     layout.append(dcc.Dropdown(
#         id=col[i],
#         options=[]
#     ))

#input list for app callback

for i in range(0,len(col)-1):
    input.append(Input(col[i],'value'))
print(input)

#output list for app callback

for i in range(1,len(col)):
    output.append(Output(col[i],'options'))
print(output)

#passing layout list with all components to app layout
app.layout=html.Div(layout)

#app call back to connect input and output components here diff dropdowns
@app.callback(
    output,
    input
)
def drop(*args):
    arg=[]
    op=[]
    dff=df.copy()
    for x in args:
        arg.append(x)
    for i in range(0,len(col)-1):
        dff=dff[dff[col[i]]==arg[i]]
      #  lists.append(dff[col[i]].unique())
        op.append([{"label":k,"value":k} for k in dff[col[i+1]].unique()])
    return tuple(op)
@app.callback(
    Output('slider-output-container','children'),
    Input('my-slider','value')
)
def date_selected(date):
    return "date selected is: "+str(dat[date])



@app.callback(
    Output('choropleth','figure'),
    Input('waste_type','value')
)
def show_map(val):
    fig = px.choropleth(
        dfd,
        locations="id",
        geojson=ward_61,
        color=val,
    )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)