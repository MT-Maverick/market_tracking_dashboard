import os
from dash import Dash, html, dcc
from components import side_panel, chart,share_stats  # Import modules
from callbacks import chart_callback, side_panel_callback, share_stats_callback  # Import callbacks

app = Dash(__name__,external_stylesheets=['assets/styles.css'])

app.layout = html.Div(
    children=[
        dcc.Interval(id="interval-component", interval=30 * 1000, n_intervals=0),
        side_panel.layout,
        chart.layout,
        share_stats.layout,
    ],
    style={"overflow": "hidden"},
)

chart_callback.register_callback(app)  # Register callbacks
side_panel_callback.register_callback(app)  # Register callbacks
share_stats_callback.register_callback(app)  # Register callbacks



if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8888)))