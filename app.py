"""Dash app"""
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

def load_json(file_name: str) -> pd.DataFrame:
    """load json locally
    file_name: the file name of the json to load
    return: A data frame
    """
    with open(file_name, "rt") as json_file:
        contents = json.load(json_file)
        frame                          = pd.DataFrame(contents["result"]["records"])
        frame['floor_area_sqm']        = pd.to_numeric(frame['floor_area_sqm'])
        frame['lease_commence_date']   = pd.to_datetime(frame['month'])
        frame['resale_price']          = pd.to_numeric(frame['resale_price']) / 1000
        frame['month']                 = pd.to_datetime(frame['month'])
        return frame


def get_town_price(frame: pd.DataFrame) -> pd.DataFrame:
    """get the column for town in the data frame
    frame: The frame of the to get
    return: The data frame for town and resale_price
    """
    return frame.loc[:,["town", "resale_price"]]


df = load_json("hdb_resale.json")

@app.callback(
    Output(component_id='my-box', component_property='figure'),
    Output(component_id='my-mean-bar', component_property='figure'),
    Output(component_id='my-median-bar', component_property='figure'),
    Input(component_id='my-slider', component_property='value')
)
def update_graph(year):
    """Update the graph in dash
    year -- The year which was selected in the slider
    """
    filtered_df = df[df['month'].dt.year == year]
    towns = get_town_price(filtered_df)

    box = px.box(towns, x="town", y="resale_price")
    box.update_layout(transition_duration=500)

    towns = towns.groupby(['town'])
    means = towns.mean()
    means.reset_index(inplace=True)
    means = means.sort_values(by="resale_price")
    means.rename(columns = {'resale_price':'mean'}, inplace = True)

    mean_bar = px.bar(means, x="town", y="mean")
    mean_bar.update_layout(transition_duration=500)

    median = towns.median()
    median.reset_index(inplace=True)
    median = median.sort_values(by="resale_price")
    median.rename(columns = {'resale_price':'median'}, inplace = True)

    median_bar = px.bar(median, x="town", y="median")
    median_bar.update_layout(transition_duration=500)

    return box, mean_bar, median_bar

app.layout = html.Div(children=[
    html.H1(children='HDB Resale data'),

    html.Div(children='''
        Dashboard for HDB resale data
    '''),

    dcc.Slider(
        id='my-slider',
        min=df['month'].dt.year.min(),
        max=df['month'].dt.year.max(),
        step=None,
        value=2020,
        marks={str(year): str(year) for year in df["month"].dt.year.unique()},
    ),
    dcc.Graph(
        id='my-box'
    ),
    dcc.Graph(
        id='my-mean-bar'
    ),
    dcc.Graph(
        id='my-median-bar'
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
# -*- coding: utf-8 -*-
