import json
import mysql.connector

from flask import Flask, url_for, request, render_template, redirect, Blueprint, session

with open('data_files/dbconfig.json', 'r') as f:
    dbconfig = json.load(f)

with open('data_files/menu_request.json', 'r') as f:
    requests_data = json.load(f)
    
with open('data_files/secret_key.json', 'r') as f:
    secret_key = json.load(f)['secret_key']

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = False
app.config['dbconfig'] =  dbconfig
app.secret_key = secret_key

from requests.requests import request_blueprint
from editing_users.editing_users import editing_users_blueprint
from authentication.authentication import authentication_blueprint
from procedure.procedure import procedure_blueprint

app.register_blueprint(request_blueprint)
app.register_blueprint(editing_users_blueprint)
app.register_blueprint(authentication_blueprint)
app.register_blueprint(procedure_blueprint)

@app.route('/menu/', methods = ['GET', 'POST'])
def main_menu():
    point = request.args.get('point')
    
    if 'role' in session:
        if point is None:
            return render_template('menu.html', requests = requests_data)
        elif point in list(map(str, range(1, len(requests_data) + 1))):
            return redirect(url_for('request_blueprint.query_result', number = point))
        elif point in 'procedure':
            return redirect(url_for('procedure_blueprint.procedure'))
        elif point in 'users':
            return redirect(url_for('editing_users_blueprint.users'))
        else:
            session.clear()
            
    return redirect(url_for('authentication_blueprint.authentication'))

app.run(port = 5000, debug = True)
