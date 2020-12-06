import json

from flask import Blueprint, session, redirect, render_template, request, current_app, url_for
from context_manager import UseDatabase, CredentialError, SQLError

authentication_blueprint = Blueprint('authentication_blueprint', __name__, template_folder = 'templates', static_folder = 'static')

@authentication_blueprint.route('/', methods = ['POST', 'GET'])
def authentication():
    if 'role' in session:
        return redirect(url_for('main_menu'))
        
    if request.form.get('sign_in'):
        username = request.form.get('username')
        password = request.form.get('password')
    else:
        return render_template('authentication.html')
        
    try:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            result = check_user(cursor, username, password)
            return redirect(url_for(result))
                
    except ConnectionError as err:
        return render_template('error.html', message = 'Базы данных не существует')

    except CredentialError as err:
        return render_template('error.html', message = 'Ошибка доступа')

    except SQLError as err:
        return render_template('error.html', message = 'Ошибка запроса')
 
    return render_template('authentication.html')
    
def check_user(cursor, username, password):
    _SQL = """SELECT id_role FROM user
              WHERE Username = %s AND Password = %s"""
              
    cursor.execute(_SQL,(username, password,))
    result = cursor.fetchall()
    
    if not result:
        return 'authentication_blueprint.authentication'

    session['role'] = result[0][0]
    return 'main_menu'
    
def database_access(cursor):
    role = session['role']
    _SQL = """SELECT Gr_username, Gr_password FROM role
              WHERE id_role = %s"""
              
    cursor.execute(_SQL,(role,))
    result = cursor.fetchall()
        
    res = {'host': '127.0.0.1', 'user': result[0][0], 'password': result[0][1], 'database': 'bonus_program'}

    return res
