from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from .models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':  # Usuario y contraseña hardcodeados
            user = User(username)
            login_user(user)
            return redirect(url_for('auth.index'))  # Cambiado a 'auth.index'
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    
# Ruta principal para renderizar la página HTML
@auth_bp.route('/')
@login_required
def index():
    return render_template('index.html')