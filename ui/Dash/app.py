from json.decoder import JSONDecodeError
import dash
from dash import exceptions
import redis
from datetime import datetime
from flask_caching import Cache
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash_extensions.enrich import Input, Output
from dash_extensions import Download
from dash.exceptions import PreventUpdate
import pandas as pd

import json
import sys
import os


def find_data_file(filename):
    if getattr(sys, "frozen", False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


redis = redis.Redis(
    host="redis-13884.c275.us-east-1-4.ec2.cloud.redislabs.com",
    port="13884",
    password="JhW0tL0cBzJQihh57TTnblPdE9LlaP5J",
)

app = dash.Dash(
    __name__,
    title="Glicko Ride",
    update_title=None,
    assets_folder=find_data_file("assets/"),
    external_stylesheets=[dbc.themes.GRID],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

cache = Cache(
    app.server, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "cache-directory"}
)
server = app.server

TIMEOUT = 5
cache.set("data", {})


@cache.memoize(timeout=TIMEOUT)
def call_redis():
    try:
        data = redis.get("user").decode()
    except:
        cache.clear()
        redis.set("user", "")
        raise TimeoutError
    data = data.split(";")
    data.pop()
    data_ = []
    for _ in data:
        _ = _.replace("'", '"')
        data_.append(json.loads(_))

    df = {
        "Time": [],
        "Temperature": [],
        "right_pressure": [],
        "left_pressure": [],
        "distance": [],
        "accelerometer_yaw": [],
        "accelerometer_roll": [],
        "accelerometer_pitch": [],
        "gyroscope_yaw": [],
        "gyroscope_roll": [],
        "gyroscope_pitch": [],
    }
    for _ in data_:
        df["Time"].append(datetime.fromtimestamp(_["Time"]))
        df["Temperature"].append(_["temperature"])
        df["right_pressure"].append(_["right_pressure"])
        df["left_pressure"].append(_["left_pressure"])
        df["distance"].append(_["distance"])
        df["accelerometer_yaw"].append(_["accelerometer"]["yaw"])
        df["accelerometer_roll"].append(_["accelerometer"]["roll"])
        df["accelerometer_pitch"].append(_["accelerometer"]["pitch"])
        df["gyroscope_yaw"].append(_["gyroscope"]["yaw"])
        df["gyroscope_roll"].append(_["gyroscope"]["roll"])
        df["gyroscope_pitch"].append(_["gyroscope"]["pitch"])

    return pd.DataFrame(
        df,
        columns=[
            "Time",
            "Temperature",
            "right_pressure",
            "left_pressure",
            "distance",
            "accelerometer_yaw",
            "accelerometer_roll",
            "accelerometer_pitch",
            "gyroscope_yaw",
            "gyroscope_roll",
            "gyroscope_pitch",
        ],
    )


def get_cache():
    return call_redis()


app.layout = html.Div(
    [
        html.Header(
            className="flex-display row",
            children=[
                html.Div(
                    id="header",
                    children=[
                        html.H1("Glicko Ride"),
                        html.P("Amp your ride with Glicko"),
                    ],
                ),
            ],
        ),
        html.Div(
            [
                html.Div(
                    id="display",
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        id="sensors",
                                        children=[
                                            html.Div(
                                                [
                                                    html.H4(
                                                        "Sensors readings:", id="title"
                                                    ),
                                                    html.Div(id="update_titles"),
                                                ]
                                            ),
                                            dbc.Button(
                                                "Export Data",
                                                id="download-button",
                                                color="primary",
                                                className="mb-3",
                                                n_clicks=0,
                                            ),
                                            Download(id="download_plot"),
                                            dbc.Button(
                                                "Stop/ Resume",
                                                id="stop-button",
                                                color="primary",
                                                className="mb-3",
                                                n_clicks=0,
                                            ),
                                        ],
                                    ),
                                    width=3,
                                ),
                                dbc.Col(
                                    html.Div(
                                        [
                                            dbc.Row(
                                                id="dropdown",
                                                children=[
                                                    dcc.Dropdown(
                                                        id="data-select",
                                                        multi=False,
                                                        style={
                                                            "width": "100%",
                                                            "color": "#000",
                                                        },
                                                        options=[
                                                            {
                                                                "label": "Temperature",
                                                                "value": "Temperature",
                                                            },
                                                            {
                                                                "label": "Distance",
                                                                "value": "distance",
                                                            },
                                                            {
                                                                "label": "Right Pressure",
                                                                "value": "right_pressure",
                                                            },
                                                            {
                                                                "label": "Left Pressure",
                                                                "value": "left_pressure",
                                                            },
                                                            {
                                                                "label": "Gyroscope",
                                                                "value": "gyroscope",
                                                            },
                                                            {
                                                                "label": "Accelerometer",
                                                                "value": "accelerometer",
                                                            },
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            html.Br(),
                                            dbc.Row(
                                                [
                                                    dcc.Graph(
                                                        id="graph",
                                                        responsive=True,
                                                        config={
                                                            "displaylogo": False,
                                                        },
                                                        style={"width": "100%"},
                                                    ),
                                                    dcc.Interval(
                                                        id="int",
                                                        interval=5000,
                                                        n_intervals=0,
                                                    ),
                                                    html.Br(),
                                                ]
                                            ),
                                        ]
                                    ),
                                    width=7,
                                ),
                            ],
                            justify="around",
                        )
                    ],
                ),
            ]
        ),
    ],
)


@app.callback(
    [Output("update_titles", "children")],
    [
        Input("int", "n_intervals"),
    ],
)
def update_sensor_readings(n):
    if n is None:
        raise PreventUpdate

    cache.clear()
    try:
        df = get_cache()
        cache.set("data", df)
    except TimeoutError:
        raise PreventUpdate

    temperature, right_pressure, left_pressure, distance = (
        df["Temperature"].iloc[-1],
        df["right_pressure"].iloc[-1],
        df["left_pressure"].iloc[-1],
        df["distance"].iloc[-1],
    )

    accelerometer_yaw, acceleromter_roll, accelerometer_pitch = (
        df["accelerometer_yaw"].iloc[-1],
        df["accelerometer_roll"].iloc[-1],
        df["accelerometer_pitch"].iloc[-1],
    )

    gyroscope_yaw, gyroscope_roll, gyroscope_pitch = (
        df["gyroscope_yaw"].iloc[-1],
        df["gyroscope_roll"].iloc[-1],
        df["gyroscope_pitch"].iloc[-1],
    )

    titles = [
        html.H5(f"Temperature : {temperature}°C", id="temperature"),
        html.H5(f"Right pressure : {right_pressure}", id="right_pressure"),
        html.H5(f"Left pressure : {left_pressure}", id="left_pressure"),
        html.H5(f"Distance : {distance} cm", id="distance"),
        html.H5("Accelerometer:", id="accelerometer"),
        html.H5(f"yaw = {accelerometer_yaw}°", id="accelerometer"),
        html.H5(f"roll = {acceleromter_roll}°", id="accelerometer"),
        html.H5(f" pitch = {accelerometer_pitch}°", id="accelerometer"),
        html.H5("Gyroscope:", id="gyroscope"),
        html.H5(f"yaw = {gyroscope_yaw}°", id="gyroscope"),
        html.H5(f"roll = {gyroscope_roll}°", id="gyroscope"),
        html.H5(f" pitch = {gyroscope_pitch}°", id="gyroscope"),
    ]

    return [titles]


@app.callback(
    Output("graph", "figure"),
    [
        Input("int", "n_intervals"),
        Input("data-select", "value"),
        Input("stop-button", "n_clicks"),
    ],
)
def update_graph(n, choice, n1):
    if n1 % 2 == 1:
        raise PreventUpdate

    if n is None:
        raise PreventUpdate

    if choice is None or choice == []:
        raise PreventUpdate

    df = cache.get("data")
    try:
        choices = [_ for _ in df.columns if _.startswith(choice)]
    except AttributeError:
        raise PreventUpdate

    fig = dict(
        data=[
            dict(
                x=df["Time"],
                y=df[value],
                type="line",
                name=value,
            )
            for value in choices
        ],
        layout=dict(
            title="Sensor readings over time",
            showlegend=True,
            legend=dict(orientation="h", y=100),
            yaxis=dict(
                title="Sensor reading",
                titlefont=dict(size=14),
                tickfont=dict(size=14),
            ),
            xaxis=dict(
                title="Time",
                titlefont=dict(size=14),
                tickfont=dict(size=14),
            ),
        ),
    )

    return fig


@app.callback(
    Output("download_plot", "data"),
    [
        Input("download-button", "n_clicks"),
    ],
)
def download_csv(n):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "download-button":
        data_sim = get_cache()
        return dict(content=data_sim.to_csv(index=False), filename="plot.csv")


if __name__ == "__main__":
    app.run_server(debug=True)
