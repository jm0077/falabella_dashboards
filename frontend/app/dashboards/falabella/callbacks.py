from dash import html, dcc, no_update
from dash.dependencies import Input, Output, State
import requests
from flask import session
import pandas as pd
import plotly.graph_objs as go
from config import BACKEND_ENDPOINT

def register_callbacks(app):
    @app.callback(
        [
            Output('pago-total-mes-falabella', 'children'),
            Output('pago-minimo-mes-falabella', 'children'),
            Output('fecha-maxima-pago-falabella', 'children'),
            Output('linea-disponible-falabella', 'children'),
            Output('movimientos-table-falabella', 'data'),
            Output('periodo-facturacion-falabella', 'children'),
            Output('pago-total-comparison-falabella', 'children'),
            Output('pago-minimo-comparison-falabella', 'children'),
        ],
        [Input('url', 'pathname')],
        [State('movimientos-table-falabella', 'id')]
    )
    def update_latest_period(pathname, _):
        if pathname != '/dashboard/falabella/':
            return no_update
        
        user_id = session.get('user_id')
        if not user_id:
            return ("Error", "Error", "Error", "Error", [], "Error: No user ID", "Error", "Error")
        
        try:
            response_period = requests.get(f"{BACKEND_ENDPOINT}/latest-period-data", params={'userId': user_id})
            response_period.raise_for_status()
            data_period = response_period.json()

            pago_total_mes = f"S/ {data_period['pago_total_mes']:.2f}"
            pago_minimo_mes = f"S/ {data_period['pago_minimo_mes']:.2f}"
            fecha_maxima_pago = data_period['ultimo_dia_pago']
            linea_disponible = f"S/ {data_period['linea_disponible']:.2f}"
            ultimo_periodo = data_period['periodo']
            movimientos = data_period['movimientos']

            for mov in movimientos:
                mov['fecha_transaccion'] = pd.to_datetime(mov['fecha_transaccion']).strftime('%Y-%m-%d')
                mov['monto'] = "-" if mov['monto'] == 0.00 else f"{mov['monto']:.2f}"
                mov['porcentaje_tea'] = "-" if mov['porcentaje_tea'] == 0.00 else f"{mov['porcentaje_tea']:.2f}"
                mov['capital'] = "-" if mov['capital'] == 0.00 else f"{mov['capital']:.2f}"
                mov['interes'] = "-" if mov['interes'] == 0.00 else f"{mov['interes']:.2f}"
                mov['total'] = f"{mov['total']:.2f}"
                mov['cuota_cargada'] = "-" if mov['cuota_cargada'] == "NA" else mov['cuota_cargada']

            # Manejar el caso de un solo periodo
            try:
                response_change = requests.get(f"{BACKEND_ENDPOINT}/percentage-change", params={'userId': user_id})
                response_change.raise_for_status()
                data_change = response_change.json()
                
                change_total = data_change.get('change_total')
                change_minimo = data_change.get('change_minimo')
            except:
                # Si hay error al obtener los cambios porcentuales, asumimos que es el primer periodo
                change_total = None
                change_minimo = None

            # Manejo de visualización para cambios porcentuales
            if change_total is not None:
                if change_total < 0:
                    change_total_text = html.Span(f"▼{abs(change_total):.2f}%", style={"color": "green"})
                else:
                    change_total_text = html.Span(f"▲{change_total:.2f}%", style={"color": "red"})
            else:
                change_total_text = html.Span("-", style={"color": "gray"})

            if change_minimo is not None:
                if change_minimo < 0:
                    change_minimo_text = html.Span(f"▼{abs(change_minimo):.2f}%", style={"color": "green"})
                else:
                    change_minimo_text = html.Span(f"▲{change_minimo:.2f}%", style={"color": "red"})
            else:
                change_minimo_text = html.Span("-", style={"color": "gray"})

            periodo_facturacion = html.Span([
                "Periodo de facturación: ",
                html.Span(ultimo_periodo, style={"color": "#007bff"})
            ])

            return (
                pago_total_mes,
                pago_minimo_mes,
                fecha_maxima_pago,
                linea_disponible,
                movimientos,
                periodo_facturacion,
                change_total_text,
                change_minimo_text
            )

        except requests.exceptions.RequestException as e:
            error_text = html.Span("Error al cargar datos", style={"color": "red"})
            return (
                "Error",
                "Error",
                "Error",
                "Error",
                [],
                error_text,
                error_text,
                error_text
            )

    @app.callback(
        Output('consumption-graph-falabella', 'figure'),
        [Input('url', 'pathname')],
        [State('consumption-graph-falabella', 'id')]
    )
    def update_graph(pathname, _):
        if pathname != '/dashboard/falabella/':
            return no_update
        
        user_id = session.get('user_id')
        if not user_id:
            return go.Figure()
        
        try:
            response = requests.get(f"{BACKEND_ENDPOINT}/consumption-data", params={'userId': user_id})
            response.raise_for_status()
            data = response.json()

            df = pd.DataFrame(data)

            # Crear una figura incluso con un solo punto de datos
            figure = go.Figure(data=[
                go.Scatter(
                    x=df['periodo'], 
                    y=df['pago_total_mes'], 
                    mode='lines+markers', 
                    line=dict(color='#007bff', width=2)
                )
            ])

            # Ajustar el layout para manejar un solo punto
            figure.update_layout(
                xaxis_title="Periodo de Facturación",
                yaxis_title="Pago Total (S/)",
                font=dict(family="Montserrat", size=16),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=50, r=20, t=50, b=100),
                height=350,
                hovermode="x unified",
                xaxis=dict(
                    showgrid=True,
                    gridcolor='lightgrey',
                    linecolor='black',
                    tickangle=45,
                    tickfont=dict(size=14),
                    tickformat='%m/%y',
                    nticks=len(df) if len(df) < 6 else 6  # Ajustar número de ticks según cantidad de datos
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='lightgrey',
                    linecolor='black',
                    tickformat=',.0f',
                    nticks=5,
                    tickfont=dict(size=14),
                    # Asegurar que el rango del eje y tenga un padding adecuado
                    range=[
                        min(df['pago_total_mes']) * 0.9 if len(df) > 0 else 0,
                        max(df['pago_total_mes']) * 1.1 if len(df) > 0 else 1000
                    ]
                ),
            )
            
            # Ajustes específicos para dispositivos móviles
            figure.update_layout(
                autosize=True,
                xaxis=dict(
                    rangeselector=dict(visible=False),
                    rangeslider=dict(visible=False)
                )
            )

            return figure

        except requests.exceptions.RequestException as e:
            # Retornar una figura vacía con mensaje de error
            fig = go.Figure()
            fig.add_annotation(
                text="Error al cargar datos",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16, color="red")
            )
            return fig