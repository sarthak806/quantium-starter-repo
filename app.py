import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("final_output.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

app = Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": "#f2f2f2",
        "padding": "20px",
        "fontFamily": "Arial"
    },
    children=[

        html.H1(
            "Soul Foods Pink Morsel Sales Dashboard",
            style={
                "textAlign": "center",
                "color": "#2c3e50"
            }
        ),

        html.Div(
            children=[
                html.Label("Select Region:", style={"fontWeight": "bold"}),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "South", "value": "south"},
                        {"label": "East", "value": "east"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    style={"margin": "10px"}
                ),
            ],
            style={
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "10px",
                "boxShadow": "0px 0px 10px rgba(0,0,0,0.1)",
                "marginBottom": "20px",
                "textAlign": "center"
            }
        ),

        dcc.Graph(id="sales-graph"),

        html.P(
            "This dashboard helps Soul Foods understand whether sales were higher before or after the Pink Morsel price increase on 15 Jan 2021.",
            style={"textAlign": "center", "marginTop": "20px"}
        )
    ]
)

# Callback to update graph based on region
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
        title="Pink Morsel Sales Over Time",
        labels={
            "date": "Date",
            "sales": "Sales ($)"
        }
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
