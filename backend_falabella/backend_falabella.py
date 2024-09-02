from flask import Flask, jsonify
from config import DB_URL, FLASK_SECRET_KEY
from models import InfoGeneral, Movimiento
from datetime import datetime, timedelta
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Text, ForeignKey
import functools

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY

# Create the database connection
engine = create_engine(DB_URL)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

def with_database_session(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        session = Session()
        try:
            return func(session, *args, **kwargs)
        finally:
            session.close()
    return wrapper

@app.route('/api/consumption-data', methods=['GET'])
@with_database_session
def get_consumption_data(session):
    twelve_months_ago = datetime.now() - timedelta(days=365)
    results = session.query(
        InfoGeneral.periodo_facturacion.label('periodo'),
        InfoGeneral.pago_total_mes
    ).filter(
        InfoGeneral.ultimo_dia_pago >= twelve_months_ago
    ).order_by(
        InfoGeneral.ultimo_dia_pago.asc()
    ).all()

    response = [
        {'periodo': r.periodo, 'pago_total_mes': r.pago_total_mes}
        for r in results
    ]
    return jsonify(response)

@app.route('/api/latest-period-data', methods=['GET'])
@with_database_session
def get_latest_period_data(session):
    latest_period = session.query(InfoGeneral).order_by(InfoGeneral.ultimo_dia_pago.desc()).first()
    if not latest_period:
        return jsonify({'error': 'No se encontró información del último período'}), 404

    movements = session.query(
        Movimiento.fecha_transaccion,
        Movimiento.fecha_proceso,
        Movimiento.detalle,
        Movimiento.monto,
        Movimiento.cuota_cargada,
        Movimiento.porcentaje_tea,
        Movimiento.capital,
        Movimiento.interes,
        Movimiento.total
    ).filter(Movimiento.info_general_id == latest_period.id).all()

    response = {
        'periodo': latest_period.periodo_facturacion,
        'pago_total_mes': latest_period.pago_total_mes,
        'pago_minimo_mes': latest_period.pago_minimo_mes,
        'ultimo_dia_pago': latest_period.ultimo_dia_pago.strftime('%Y-%m-%d'),
        'linea_disponible': latest_period.linea_disponible,
        'movimientos': [
            {
                'fecha_transaccion': m.fecha_transaccion,
                'fecha_proceso': m.fecha_proceso,
                'detalle': m.detalle,
                'monto': m.monto,
                'cuota_cargada': m.cuota_cargada,
                'porcentaje_tea': m.porcentaje_tea,
                'capital': m.capital,
                'interes': m.interes,
                'total': m.total
            } for m in movements
        ]
    }
    return jsonify(response)

@app.route('/api/percentage-change', methods=['GET'])
@with_database_session
def get_percentage_change(session):
    latest_two_periods = _get_latest_two_periods(session)
    if len(latest_two_periods) < 2:
        return jsonify({'error': 'No se encontraron suficientes períodos para calcular el cambio porcentual'}), 404

    latest_period, previous_period = latest_two_periods
    change_total = _calculate_percentage_change(latest_period.pago_total_mes, previous_period.pago_total_mes)
    change_minimo = _calculate_percentage_change(latest_period.pago_minimo_mes, previous_period.pago_minimo_mes)

    response = {
        'change_total': change_total,
        'change_minimo': change_minimo
    }
    return jsonify(response)

def _get_latest_two_periods(session):
    return session.query(
        InfoGeneral.pago_total_mes,
        InfoGeneral.pago_minimo_mes
    ).order_by(
        InfoGeneral.ultimo_dia_pago.desc()
    ).limit(2).all()

def _calculate_percentage_change(latest, previous):
    if previous != 0:
        return round(((latest - previous) / previous) * 100, 2)
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
