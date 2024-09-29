from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Banco, UsuarioBanco
import functools
from config import DB_URL, FLASK_SECRET_KEY

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
    banco_id = data.get('bancoId')
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)