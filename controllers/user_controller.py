from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from models.user_model import User
from services.user_service import UserService

user_blueprint = Blueprint('user', __name__, url_prefix='/user')

@user_blueprint.route("/adicionar", methods=['GET', 'POST'])
def adicionar_usuario():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Usuário já existe!', 'danger')
            return redirect(url_for('user.adicionar_usuario'))

        UserService.create_user(username, password)
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('user.adicionar_usuario'))
    
    return render_template('add_user.html')

@user_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = UserService.check_user(username=username, password=password)
        if user:
            user_id, is_admin = user
            session['user_id'] = user_id
            session['is_admin'] = is_admin
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('task.listar'))
        
        flash('Usuário ou senha inválidos!', 'danger')
    return render_template('login.html')

@user_blueprint.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('user.login'))

@user_blueprint.route("/list")
def list_users():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acesso negado. Apenas administradores logados podem acessar essa página', 'danger')
        return redirect(url_for('user.login'))
    
    users = UserService.list_users()
    print(users)
    return render_template('user_list.html', users=users)

