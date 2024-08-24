from flask import Flask, render_template
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import requests
import pandas as pd
import plotly.graph_objs as go

# Configurar Flask
server = Flask(__name__)

# Configurar Dash dentro de Flask
app = Dash(__name__, server=server, routes_pathname_prefix='/dashboard/', external_stylesheets=[dbc.themes.BOOTSTRAP])

# Definir el layout de la aplicación Dash
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Pago Total de los últimos 12 periodos"), className="text-center")
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='consumption-graph'), width=12)
    ])
], fluid=True)

# Callback para actualizar el gráfico de consumo por periodo
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
    fig = go.Figure()

    # Agregar la línea del pago total por periodo
    fig.add_trace(go.Scatter(
        x=df['periodo'],
        y=df['pago_total_mes'],
        mode='lines+markers',
        name='Pago Total Mes',
        line=dict(color='royalblue', width=3),
        marker=dict(size=8, symbol='circle')
    ))

    # Configuración de los ejes
    fig.update_layout(
        title='Pago Total de los últimos 12 periodos',
        xaxis_title='Periodo',
        yaxis_title='Pago Total Mes (S/.)',
        xaxis=dict(showline=True, showgrid=False, showticklabels=True, linecolor='rgb(204, 204, 204)', linewidth=2, ticks='outside'),
        yaxis=dict(showgrid=True, zeroline=True, showline=True, gridcolor='lightgrey', linecolor='rgb(204, 204, 204)', linewidth=2, tickprefix='S/.', ticksuffix=''),
        plot_bgcolor='white'
    )

    return fig

# Ruta principal para renderizar la página HTML
@server.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080)
