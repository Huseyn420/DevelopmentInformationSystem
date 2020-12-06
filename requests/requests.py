import mysql.connector
import json

from flask import Flask, render_template, request, redirect, Blueprint, url_for, current_app, session
from authentication.authentication import database_access
from context_manager import UseDatabase, CredentialError, SQLError

with open('data_files/requests.json', 'r') as f:
    data_requests = json.load(f)

request_blueprint = Blueprint('request_blueprint', __name__, template_folder = 'templates', static_folder = 'static')

@request_blueprint.route('/menu/request=<number>', methods = ['GET', 'POST'])
def query_result(number):
    try:
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            user = database_access(cursor)
    
        with UseDatabase(user) as cursor:
            result = database_query(cursor, number)
            
            if not result:
                return render_template('error.html', message = "Not found")
                        
    except ConnectionError as err:
        return render_template('error.html', message = 'Базы данных не существует')

    except CredentialError as err:
        return render_template('error.html', message = 'Ошибка доступа')

    except SQLError as err:
        return render_template('error.html', message = 'Ошибка запроса')
          
    page = data_requests[number]['file_name']
    return render_template(page, strings = result)


def database_query(cursor, number):
    _SQL = data_requests[number]['request']
    cursor.execute(_SQL,)
    result = cursor.fetchall()

    res = []
    schema = data_requests[number]['schema']
    
    for line in result:
        res.append(dict(zip(schema, line)))

    return res

