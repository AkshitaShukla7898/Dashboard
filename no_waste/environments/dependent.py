import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

df=pd.read_csv('dummy.csv')
coun=df['Country'].unique()
#print(coun)

app.layout= html.Div([
    html.Div([
        html.P("Country"),
        dcc.Dropdown(
            id='country',
            value=coun[0],
            options=[{"label":x,"value":x} for x in coun]
        ),
        html.P("State"),
        dcc.Dropdown(
            id='state',
            options=[]
        ),
        html.P("City"),
        dcc.Dropdown(
            id='city',
            options=[]
        )
    ])
])

@app.callback(
    Output('state','options'),
    Input('country','value')
)
def drop(country):
    dff=df[df['Country']==country]
    print(dff)
    return [{"label":i,"value":i} for i in dff['State'].unique()]

@app.callback(
    Output('city','options'),
    [Input('state','value'),
     Input('country','value')]
)
def drop(state,country):
   # df=pd.read_csv('dummy.csv')
    dfs=df[df['Country']==country]
    print('Here')
    print(dfs)
    print(country)
    print(state)
    dfs=dfs[dfs['State']==state]
    print(dfs)
    return [{"label":j,"value":j} for j in dfs['City'].unique()]


if __name__ == "__main__":
    app.run_server(debug=True)