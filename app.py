from dash import Dash, html, dcc, Input, Output, callback_context
from components import side_panel, chart  # Import modules
import os

app = Dash(__name__,external_stylesheets=['assets/style.css'])

app.layout = html.Div([
    html.Div([
        dcc.Interval(id="interval-component", interval=30 * 1000, n_intervals=0),
        side_panel.layout,
        chart.layout,
    ]),
    html.Div([])
])


from callbacks import chart_callback, side_panel_callback,results_panel_callback  # Import callbacks

chart_callback.register_callback(app)  # Register callbacks
side_panel_callback.register_callback(app)  # Register callbacks
results_panel_callback.ButtonComponent(app)

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8888)))