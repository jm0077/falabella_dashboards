from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Banco, UsuarioBanco, UsuarioEstado
import functools
from config import DB_URL, FLASK_SECRET_KEY
from datetime import datetime

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

@app.route('/api/bancos', methods=['GET'])
@with_database_session
def get_bancos(session):
    bancos = session.query(Banco).all()
    return jsonify([{'id': banco.id, 'nombre': banco.nombre} for banco in bancos])

@app.route('/api/usuario-bancos', methods=['GET'])
@with_database_session
def get_usuario_bancos(session):
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'error': 'userId es requerido'}), 400

    usuario_bancos = session.query(UsuarioBanco).filter(UsuarioBanco.userId == user_id).all()
    return jsonify([{
        'id': ub.id,
        'banco_id': ub.banco_id,
        'banco_nombre': ub.banco.nombre,
        'habilitado': ub.habilitado
    } for ub in usuario_bancos])

@app.route('/api/usuario-bancos', methods=['PUT'])
@with_database_session
def update_usuario_banco(session):
    data = request.json
    user_id = data.get('userId')
    banco_id = data.get('banco_id')
    habilitado = data.get('habilitado')

    if not all([user_id, banco_id, habilitado is not None]):
        return jsonify({'error': 'userId, bancoId y habilitado son requeridos'}), 400

    usuario_banco = session.query(UsuarioBanco).filter(
        UsuarioBanco.userId == user_id,
        UsuarioBanco.banco_id == banco_id
    ).first()

    if not usuario_banco:
        return jsonify({'error': 'No se encontró la relación usuario-banco'}), 404

    usuario_banco.habilitado = habilitado
    session.commit()

    return jsonify({
        'id': usuario_banco.id,
        'banco_id': usuario_banco.banco_id,
        'banco_nombre': usuario_banco.banco.nombre,
        'habilitado': usuario_banco.habilitado
    })

@app.route('/api/usuario-estado', methods=['GET'])
@with_database_session
def get_usuario_estado(session):
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'error': 'userId es requerido'}), 400

    usuario_estado = session.query(UsuarioEstado).filter(UsuarioEstado.userId == user_id).first()
    
    if not usuario_estado:
        return jsonify({'error': 'No se encontró el estado del usuario'}), 404

    return jsonify({
        'id': usuario_estado.id,
        'userId': usuario_estado.userId,
        'primer_ingreso': usuario_estado.primer_ingreso,
        'documento_cargado': usuario_estado.documento_cargado,
        'fecha_primer_ingreso': usuario_estado.fecha_primer_ingreso.isoformat() if usuario_estado.fecha_primer_ingreso else None,
        'fecha_primera_carga': usuario_estado.fecha_primera_carga.isoformat() if usuario_estado.fecha_primera_carga else None
    })

@app.route('/api/usuario-estado', methods=['PUT'])
@with_database_session
def update_usuario_estado(session):
    data = request.json
    user_id = data.get('userId')

    if user_id is None:
        return jsonify({'error': 'El campo userId es obligatorio'}), 400

    usuario_estado = session.query(UsuarioEstado).filter(UsuarioEstado.userId == user_id).first()
    if not usuario_estado:
        return jsonify({'error': 'No se encontró el estado del usuario'}), 404

    primer_ingreso = data.get('primer_ingreso')
    documento_cargado = data.get('documento_cargado')
    fecha_primer_ingreso = data.get('fecha_primer_ingreso')
    fecha_primera_carga = data.get('fecha_primera_carga')

    if primer_ingreso is not None:
        usuario_estado.primer_ingreso = primer_ingreso
    if documento_cargado is not None:
        usuario_estado.documento_cargado = documento_cargado
    if fecha_primer_ingreso:
        usuario_estado.fecha_primer_ingreso = datetime.fromisoformat(fecha_primer_ingreso)
    if fecha_primera_carga:
        usuario_estado.fecha_primera_carga = datetime.fromisoformat(fecha_primera_carga)

    session.commit()

    return jsonify({
        'id': usuario_estado.id,
        'userId': usuario_estado.userId,
        'primer_ingreso': usuario_estado.primer_ingreso,
        'documento_cargado': usuario_estado.documento_cargado,
        'fecha_primer_ingreso': usuario_estado.fecha_primer_ingreso.isoformat() if usuario_estado.fecha_primer_ingreso else None,
        'fecha_primera_carga': usuario_estado.fecha_primera_carga.isoformat() if usuario_estado.fecha_primera_carga else None
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)