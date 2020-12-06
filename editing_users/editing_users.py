import mysql.connector
import json

from flask import Flask, render_template, request, redirect, Blueprint, url_for, current_app, session
from authentication.authentication import database_access
from requests.requests import database_query, data_requests
from context_manager import UseDatabase, CredentialError, SQLError

editing_users_blueprint = Blueprint('editing_users_blueprint', __name__, template_folder = 'templates', static_folder = 'static')

@editing_users_blueprint.route('/menu/users', methods = ['GET', 'POST'])
def users():
    try:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            user = database_access(cursor)
    
        with UseDatabase(user) as cursor:
            id_user = request.form.get('id')

            if request.form.get('delete'):
                delete_user(cursor, id_user)
            
            if request.form.get('back'):
                return redirect(url_for('main_menu'))
                
            if request.form.get('add'):
                return redirect(url_for('editing_users_blueprint.add_users'))
                
            if request.form.get('edit'):
                return redirect(url_for('editing_users_blueprint.edit_user', id = id_user))
                
            data_users = database_query(cursor, 'users')
                
    except ConnectionError as err:
        return render_template('error.html', message = 'Базы данных не существует')

    except CredentialError as err:
        return render_template('error.html', message = 'Ошибка доступа')

    except SQLError as err:
        return render_template('error.html', message = 'Ошибка запроса')
        
    return render_template('editing_users.html', users = data_users)
        
def delete_user(cursor, id_user):
    _SQL = """DELETE FROM user WHERE id_user = %s;"""
    cursor.execute(_SQL,(id_user,))
    

@editing_users_blueprint.route('/menu/users/add_users', methods = ['GET', 'POST'])
def add_users():
    try:
        if request.form.get('back'):
            return redirect(url_for('editing_users_blueprint.users'))
    
        full_name = request.form['full_name']
        birthday = request.form['birthday']
        username = request.form['username']
        password = request.form['password']
        position = request.form['position']
        
        if request.form.get('add'):
            with UseDatabase(current_app.config['dbconfig']) as cursor:
                user = database_access(cursor)
                
            with UseDatabase(user) as cursor:
                save_data(cursor, full_name, birthday, username, password, position)
                return render_template('success.html')
                
    except ConnectionError as err:
        return render_template('error.html', message = 'Базы данных не существует')

    except CredentialError as err:
        return render_template('error.html', message = 'Ошибка доступа')

    except SQLError as err:
        return render_template('error.html', message = 'Ошибка запроса')
        
    except:
        return render_template('adding_user.html')
    
    return render_template('adding_user.html')
        
def save_data(cursor, full_name, birthday, username, password, position):
    _SQL = """INSERT INTO bonus_program.user VALUES (NULL, %s, %s, %s, %s, %s);"""
    cursor.execute(_SQL,(username, password, position, full_name, birthday,))


@editing_users_blueprint.route('/menu/users/edit_user/id=<id>', methods = ['GET', 'POST'])
def edit_user(id):
    try:
        if request.form.get('back'):
            return redirect(url_for('editing_users_blueprint.users'))
    
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            user = database_access(cursor)
    
        with UseDatabase(user) as cursor:
            if request.form.get('edit'):
                full_name = request.form['full_name']
                birthday = request.form['birthday']
                username = request.form['username']
                position = request.form['position']
                update_data(cursor, full_name, username, birthday, position, id)
                return render_template('success.html')
        
            data = user_data(cursor, id)
            
    except ConnectionError as err:
        return render_template('error.html', message = 'Базы данных не существует')

    except CredentialError as err:
        return render_template('error.html', message = 'Ошибка доступа')

    except SQLError as err:
        return render_template('error.html', message = 'Ошибка запроса')
        
    except:
        return render_template('error.html', message = 'Ошибка! Заполните все поля.')

    return render_template('editing_data.html', full_name = data.get('Full_name'), username = data.get('Username'), birthday = data.get('Birthday'))
    
def user_data(cursor, id):
    _SQL = """SELECT Full_name, Username, Birthday, id_role FROM user
              WHERE id_user = %s"""
              
    cursor.execute(_SQL,(id,))
    result = cursor.fetchall()
    
    if not result:
        return []
    
    schema = ['Full_name', 'Username', 'Birthday', 'Position']
    res = dict(zip(schema, result[0]))

    return res

def update_data(cursor, full_name, username, birthday, position, id):
    _SQL = """UPDATE user
              SET Full_name = %s, Username = %s, Birthday = %s, id_role = %s
              WHERE id_user = %s;"""
              
    cursor.execute(_SQL,(full_name, username, birthday, position, id,))
