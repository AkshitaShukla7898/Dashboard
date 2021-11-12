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
#print(col[len(col)-1])
layout=[]
output=[]
input=[]
dat={}
dd1=[]
dd2=[]

ward_61 = json.load(open('ward61.geojson', 'r'))
regions = json.load(open('regions.geojson', 'r'))


dfd = pd.read_csv('ward_61_data_1.csv')
dfr = pd.read_csv('dummy_r.csv')
radio=list(dfd.columns)
for i in range(0,12,1):
    radio.pop(0)
l = []

# handling null values in geojson
# i = 0
# for feature in ward_61['features']:
#     if feature['properties']['name'] is None:
#             feature['properties']['name'] = 'random_' + str(i)
#             i += 1
#     l.append(feature['properties']['name'])
i=0
building_id_map = {}
reg_map={}
#mapping geojson with csv using id columns (osm_id)
for feature in ward_61["features"]:
    # feature["properties"]["oid"]=i
    # feature["id"] = feature["properties"]["osm_id"]
    feature["id"] = i
    i+=1
    building_id_map[feature["properties"]["name"]] = feature["id"]

dfd["id"] = dfd["name"].apply(lambda x: building_id_map[x])
i=0
# for feature in regions["features"]:
#     # feature["properties"]["oid"]=i
#     # feature["id"] = feature["properties"]["id"]
#     feature["id"] = i
#     i+=1
#     reg_map[feature["properties"]["region_nam"]] = feature["id"]
#
# dfr["id"] = dfr["region_nam"].apply(lambda x: reg_map[x])

#print(dfd)

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
    ], width=12)
]

))

layout.append(dbc.Row(html.P("Select Area:")))
layout.append(dbc.Row([
    dbc.Col([

    dcc.RadioItems(
        id='area',
        options=[{'value': x, 'label': x}
                 for x in col],
        value=col[2],
        labelStyle={'display': 'inline-block'}
    )
    ], width=12)
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
#print(input)

#output list for app callback

for i in range(1,len(col)):
    output.append(Output(col[i],'options'))
#print(output)

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



# @app.callback(
#     Output('choropleth','figure'),
#     [Input('waste_type','value'),
#      ]
# )
# def show_map(val):
#     fig = px.choropleth(
#         dfd,
#         locations="id",
#         geojson=ward_61,
#         color=val,
#     )
#     fig.update_geos(fitbounds="locations", visible=False)
#     return fig
data=dfr
geo=regions
ip=[]
ip.append(Input('waste_type','value'))
ip.append(Input('area','value'))
for i in range(3,len(col)):
    ip.append(Input(col[i],'value'))
@app.callback(
    Output('choropleth','figure'),
    ip
)
def show_map(*args):
    arg=[]
    for x in args:
        arg.append(x)
    if arg[1]=='Ward':
        geo=regions

        ##CREATING DATAFRAME FOR REGIONS

        # print(dfd)

        reg = dfd['region'].unique()

        dat = []

        fields = ['region', 'total waste', 'wet waste', 'dry waste']

        for i in reg:
            l = []
            l.append(i)
            for i in range(3):
                l.append(0)
            dat.append(l)

        for ind in dfd.index:
            for li in dat:
                if li[0] == dfd['region'][ind]:
                    li[1] += dfd['total waste'][ind]
                    li[2] += dfd['wet waste'][ind]
                    li[3] += dfd['dry waste'][ind]
                    break

        data = pd.DataFrame(dat, columns=fields)
        i=0
        map={}
        for feature in geo["features"]:
            # feature["properties"]["oid"]=i
            # feature["id"] = feature["properties"]["osm_id"]
            feature["id"] = i
            i += 1
            map[feature["properties"]["region_nam"]] = feature["id"]

        data["id"] = data["region"].apply(lambda x: map[x])
    elif arg[1]=='Region':
        geo=ward_61.copy()

        ##CREATING DATAFRAME FOR BUILDING CLUSTERS

        # print(dfd)

        # reg = dfd['building_cluster']
        # bn = dfd['name']
        dat = []

        fields = ['building_cluster', 'name','total waste', 'wet waste', 'dry waste']

        for i in dfd.index:
            l = []
            l.append(dfd['building_cluster'][i])
            l.append(dfd['name'][i])
            for j in range(3):
                l.append(0)
            dat.append(l)

        for ind in dfd.index:
            for li in dat:
                if li[0] == dfd['building_cluster'][ind]:
                    li[2] += dfd['total waste'][ind]
                    li[3] += dfd['wet waste'][ind]
                    li[4] += dfd['dry waste'][ind]


        data = pd.DataFrame(dat, columns=fields)
        print(data)
        i=0
        map={}
        for feature in geo["features"]:
            # feature["properties"]["oid"]=i
            # feature["id"] = feature["properties"]["osm_id"]
            feature["id"] = i
            i+=1

            map[feature["properties"]["name"]] = feature["id"]

        data["id"] = data["name"].apply(lambda x: map[x])
       # PREPARING GEOJSON
        feat = []
        for i in ward_61['features']:
            if (i['properties']['region'] == arg[2]):
                feat.append(i)
        mody = ward_61.copy()
        mody['features'] = feat
        geo=mody

    if arg[1]=='Building_Cluster':
        feat = []
        for i in ward_61['features']:
            if (i['properties']['building_cluster'] == arg[3]):
                feat.append(i)
        mody = ward_61.copy()
        mody['features'] = feat
        data=dfd
        geo=mody
    fig = px.choropleth(
        data,
        locations="id",
        geojson=geo,
        color=arg[0],
    )
    fig.update_geos(fitbounds="locations", visible=False)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)