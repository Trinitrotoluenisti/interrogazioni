from flask import render_template, request, make_response, redirect
from uuid import uuid4

from . import app, Data
from .admin_password import ADMIN_PASSWORD


admin = {'password': ADMIN_PASSWORD, 'token': ''}


@app.route('/')
def index(error=''):
    lists = Data.get_lists()
    dashboard = Data.get_lists_dashboard()
    isadmin = request.cookies.get('token') == admin['token'] and admin['token']

    return render_template('index.html', dashboard=dashboard, lists=lists, error=error, admin=isadmin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    password = request.form.get('password')
    if password == admin['password']:
        admin['token'] = uuid4().hex
        r = make_response(redirect('/'))
        r.set_cookie('token', admin['token'])
        return r
    else:
        return index(error='Incorrect password'), 401

@app.route('/logout')
def logout():
    if request.cookies.get('token') == admin['token']:
        admin['token'] = ''
        r = make_response(redirect('/'))
        r.set_cookie('token', '')
        return r
    else:
        return index(error='You are not logged in'), 401

@app.route('/lists/<int:lid>')
def list_page(lid):
    if (l := Data.get_list(lid)):
        return render_template('list.html', list=l)
    else:
        return None, 404
