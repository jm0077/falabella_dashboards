from flask import Flask, render_template
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd

# Configurar Flask
server = Flask(__name__)

# Configurar Dash dentro de Flask
app = Dash(__name__, server=server, routes_pathname_prefix='/dashboard/', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Definir el layout de la aplicación Dash
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Pago Total Mensual"), className="text-center")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='consumption-graph'), width=12)
    ])
], fluid=True)

# Callback para actualizar el gráfico de consumo mensual
@app.callback(
    Output('consumption-graph', 'figure'),
    Input('consumption-graph', 'id')
)
def update_consumption_graph(_):
    # Realizar solicitud al backend
    response = requests.get("https://backend-falabella-app-service-alhjlx25pa-tl.a.run.app/api/consumption-data")
    data = response.json()

    # Crear DataFrame
    df = pd.DataFrame(data)

    # Crear la figura del gráfico de líneas
    fig = {
        'data': [
            {'x': df['mes'], 'y': df['pago_total_mes'], 'type': 'line', 'name': 'Pago Total Mes'},
        ],
        'layout': {
            'title': 'Pago Total Mensual',
            'xaxis': {'title': 'Mes'},
            'yaxis': {'title': 'Pago Total Mes'},
        }
    }
    return fig

# Ruta principal para renderizar la página HTML
@server.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)
