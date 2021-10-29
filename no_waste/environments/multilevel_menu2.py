import dash
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


level3_items = [
    dbc.DropdownMenuItem("Item 5"),
    dbc.DropdownMenuItem("Item 6"),
]

level2_items = [
    dbc.DropdownMenuItem("Item 3"),
    dbc.DropdownMenuItem("Item 4"),
    dbc.DropdownMenu(level3_items),
]

level1_items = [
    dbc.DropdownMenuItem("Item 1"),
    dbc.DropdownMenuItem("Item 2"),
    dbc.DropdownMenu(level2_items),
]


app.layout = dbc.Container(
    [
        dbc.DropdownMenu(
            label="Menu", size="large", children=level1_items, className="mb-3",
        ),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
