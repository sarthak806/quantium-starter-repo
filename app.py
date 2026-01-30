import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load the processed data
df = pd.read_csv("final_output.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort by date
df = df.sort_values("date")

# Create line chart
fig = px.line(
    df,
    x="date",
    y="sales",
    color="region",
    title="Pink Morsel Sales Over Time",
    labels={
        "date": "Date",
        "sales": "Sales ($)",
        "region": "Region"
    }
)

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Visualiser", style={"textAlign": "center"}),

    dcc.Graph(figure=fig),

    html.P(
        "This chart shows Pink Morsel sales over time. "
        "The price increase occurred on 15th January 2021. "
        "From the chart, it is clear whether sales were higher before or after this date.",
        style={"textAlign": "center"}
    )
])

if __name__ == "__main__":
    app.run(debug=True)

