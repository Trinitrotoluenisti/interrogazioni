from flask import render_template, request, make_response, redirect
from uuid import uuid4

from . import app, Data
from .admin_password import ADMIN_PASSWORD


admin = {'password': ADMIN_PASSWORD, 'token': ''}


@app.route('/')
def index(error=''):
    dashboard = Data.get_lists_dashboard()

    return render_template('index.html', dashboard=dashboard, index=True, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login(error=''):
    if request.method == 'GET' or error:
        return render_template('login.html', error=error)

    password = request.form.get('password')
    if password == admin['password']:
        admin['token'] = uuid4().hex
        r = make_response(redirect('/'))
        r.set_cookie('token', admin['token'])
        return r
    else:
        return login(error='Incorrect password'), 401

@app.route('/logout')
def logout():
    if request.cookies.get('token') == admin['token']:
        admin['token'] = ''
        r = make_response(redirect('/'))
        r.set_cookie('token', '')
        return r
    else:
        return index(error='You are not logged in'), 401

@app.route('/lists')
@app.route('/elements')
def show_options():
    path = str(request.url_rule)[1:]

    if path == 'lists':
        prompt = "Seleziona una lista"
        options = Data.get_lists()
    else:
        prompt = "Seleziona uno studente"
        options = Data.get_elements()

    return render_template('options.html', prompt=prompt, options=options, path=path)

@app.route('/lists/<int:lid>')
def list_page(lid):
    if (l := Data.get_list(lid)):
        return render_template('list.html', list=l)
    else:
        return None, 404

@app.route('/elements/<int:eid>')
def element_page(eid):
    if (e := Data.get_element(eid)):
        dashboard = Data.get_element_dashboard(eid)
        return render_template('element.html', element=e, dashboard=dashboard)
    else:
        return None, 404
