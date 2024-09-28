# dashboard.py
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from kafka import KafkaConsumer
import json
import threading
import time
import pandas as pd

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server  # For deploying on AWS or other platforms

# Global DataFrame to store traffic data
traffic_df = pd.DataFrame(columns=['Timestamp', 'Location', 'Traffic Level'])

# Function to consume Kafka messages in a separate thread
def consume_kafka():
    global traffic_df
    consumer = KafkaConsumer(
        'traffic-data',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='dashboard-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    for message in consumer:
        data = message.value
        # Append new data to the DataFrame
        traffic_df = traffic_df.append({
            'Timestamp': pd.to_datetime(data['timestamp'], unit='s'),
            'Location': data['location'],
            'Traffic Level': data['traffic_level']
        }, ignore_index=True)
        # Keep only the latest 100 data points
        traffic_df = traffic_df.tail(100)

# Start Kafka consumer thread
threading.Thread(target=consume_kafka, daemon=True).start()

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Real-Time Traffic Management Dashboard"),
    dcc.Graph(id='live-traffic-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Update every second
        n_intervals=0
    )
])

# Callback to update the graph
@app.callback(Output('live-traffic-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    if traffic_df.empty:
        return go.Figure()

    # Group data by location
    grouped = traffic_df.groupby('Location').mean().reset_index()

    # Create bar chart for traffic levels
    data = [
        go.Bar(
            x=grouped['Location'],
            y=grouped['Traffic Level'],
            name='Traffic Level'
        )
    ]

    layout = go.Layout(
        title='Current Traffic Levels by Location',
        xaxis=dict(title='Location'),
        yaxis=dict(title='Traffic Level'),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return go.Figure(data=data, layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True)
