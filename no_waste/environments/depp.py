import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

df=pd.read_csv('dummy.csv')
col=list(df.columns)
print(col[len(col)-1])
layout=[]
output=[]
input=[]
#lists=[]
layout.append(html.P(col[0]))
layout.append(dcc.Dropdown(
    id=col[0],
    options=[{"label":x,"value":x} for x in df[col[0]].unique()]
))
for i in range(1,len(col)):
    layout.append(html.P(col[i]))
    layout.append(dcc.Dropdown(
        id=col[i],
        options=[]
    ))
for i in range(0,len(col)-1):
    input.append(Input(col[i],'value'))
print(input)
for i in range(1,len(col)):
    output.append(Output(col[i],'options'))
print(output)
app.layout=html.Div([
    html.Div(
        layout
    )
])

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
if __name__ == "__main__":
    app.run_server(debug=True)