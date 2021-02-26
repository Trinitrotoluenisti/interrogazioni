from flask import render_template, request, make_response, redirect
from uuid import uuid4

from . import app, Lists
from .configs import ADMIN_PASSWORD


admin = {'password': ADMIN_PASSWORD, 'token': ''}


@app.route('/')
def index(error=''):
    isadmin = request.cookies.get('token') == admin['token'] and admin['token']

    dashboard = Lists.get_dashboard()
    lists = Lists.get_all()

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

@app.route('/lists/<int:list_id>')
def list_page(list_id):
    if (l := Lists.get(list_id)):
        groups = [l for l in Lists.get_dashboard() if l['id'] == list_id]
        if groups:
            groups = groups[0]
        else:
            groups = None

        return render_template('list.html', name=l['name'], order=l['order'], groups=groups)
    else:
        return None, 404
