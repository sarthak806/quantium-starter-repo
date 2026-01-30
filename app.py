import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("final_output.csv")

# Ensure correct types
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

app = Dash(__name__)

app.layout = html.Div(
    style={"padding": "20px"},
    children=[

        # HEADER (TEST 1 expects this)
        html.H1(
            "Soul Foods Pink Morsel Sales Dashboard",
            id="header"
        ),

        # REGION PICKER (TEST 3 expects this id)
        dcc.RadioItems(
            id="region-filter",
            options=[
                {"label": "All", "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "East", "value": "east"},
                {"label": "South", "value": "south"},
                {"label": "West", "value": "west"},
            ],
            value="all",
            inline=True
        ),

        # GRAPH (TEST 2 expects this id)
        dcc.Graph(id="sales-graph"),
    ]
)


@app.callback(
    Output("sales-graph", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):
    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        title="Pink Morsel Sales Over Time"
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
