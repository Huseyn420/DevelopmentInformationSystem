import mysql.connector
import json

from flask import Flask, render_template, request, redirect, Blueprint, url_for, current_app, session
from authentication.authentication import database_access
from requests.requests import database_query, data_requests
from context_manager import UseDatabase, CredentialError, SQLError

procedure_blueprint = Blueprint('procedure_blueprint', __name__, template_folder = 'templates', static_folder = 'static')

@procedure_blueprint.route('/menu/procedure', methods = ['GET', 'POST'])
def procedure():
    try:
        if not request.form.get('search'):
            return render_template('procedure_menu.html')
    
        with UseDatabase(current_app.config['dbconfig']) as cursor:
            user = database_access(cursor)
    
        with UseDatabase(user) as cursor:
            args = (request.form['month'], request.form['year'])
            cursor.callproc('report', args)
            result = database_query(cursor, "procedure")
            
            if not result:
                return render_template('error.html', message = "Not found")
                        
    except ConnectionError as err:
        return render_template('error.html', message = 'Базы данных не существует')

    except CredentialError as err:
        return render_template('error.html', message = 'Ошибка доступа')

    except SQLError as err:
        return render_template('error.html', message = 'Ошибка запроса')\
        
    except:
        return render_template('procedure_menu.html')
          
    page = data_requests['procedure']['file_name']
    return render_template(page, strings = result)
