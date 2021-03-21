from flask import render_template, request, make_response, redirect
from functools import wraps
from uuid import uuid4

from . import app, Data
from .admin_password import ADMIN_PASSWORD


admin = {'password': ADMIN_PASSWORD, 'token': ''}


def check_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        is_admin = (request.cookies.get('token') == admin['token']) and admin['token']
        return func(*args, **kwargs, is_admin=is_admin)
    
    return wrapper


@app.route('/')
@check_admin
def index_page(is_admin=False):
    dashboard = Data.get_lists_dashboard()
    return render_template('index.html', dashboard=dashboard, index=True, is_admin=is_admin)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')

    password = request.form.get('password')
    if password == admin['password']:
        admin['token'] = uuid4().hex
        r = make_response(redirect('/'))
        r.set_cookie('token', admin['token'])
        return r
    else:
        return render_template('login.html', error='Credenziali invalide'), 401

@app.route('/logout')
@check_admin
def logout_page(is_admin=False):
    r = make_response(redirect('/'))

    if is_admin:
        admin['token'] = ''
        r.set_cookie('token', '')

    return r

@app.route('/lists')
@app.route('/elements')
def options_page():
    path = str(request.url_rule)[1:]

    if path == 'lists':
        prompt = "Seleziona una lista"
        options = Data.get_lists()
    else:
        prompt = "Seleziona uno studente"
        options = Data.get_elements()

    return render_template('options.html', prompt=prompt, options=options, path=path)

@app.route('/lists/<int:lid>')
@check_admin
def list_page(lid, is_admin=False):
    if (l := Data.get_list(lid)):
        return render_template('list.html', list=l, is_admin=is_admin)
    else:
        return None, 404

@app.route('/elements/<int:eid>')
def element_page(eid):
    if (e := Data.get_element(eid)):
        dashboard = Data.get_element_dashboard(eid)
        return render_template('element.html', element=e, dashboard=dashboard)
    else:
        return None, 404

@app.route('/lists/new', methods=['GET', 'POST'])
@check_admin
def new_list_page(is_admin=False):
    if not is_admin:
        return redirect('/'), 401
    elif request.method == 'GET':
        return render_template('create_list.html')

    data = dict(request.form)

    if not 'name' in data or not 'step' in data:
        return render_template('create_list.html', error='Dati insufficienti', **data)
    
    try:
        Data.generate_list(data['name'], int(data['step']))
    except ValueError as e:
        return render_template('create_list.html', error=str(e), **data)

    return redirect('/')

@app.route('/lists/<int:lid>/delete', methods=['POST'])
@check_admin
def delete_list_endpoint(lid, is_admin=False):
    if not is_admin:
        return redirect(f'/lists/{lid}'), 401

    try:
        Data.delete_list(lid)
    except ValueError as e:
        return render_template('list.html', list=Data.get_list(lid), is_admin=is_admin, error=str(e))

    return redirect('/lists')

@app.route('/lists/<int:lid>/update', methods=['POST'])
@check_admin
def update_list_endpoint(lid, is_admin=False):
    if not is_admin:
        return redirect('/'), 401

    l = Data.get_list(lid)
    if not l:
        return handle_404(None)

    data = dict(request.form)
    new_elements = {i: e.replace('-order', '') for e, i in data.items() if e.endswith('-order')}
    new_order = [0] * len(new_elements)

    for index, element in new_elements.items():
        new_order[int(index) - 1] = element

    Data.reorder_list(lid, new_order)

    changed = []
    for element in l['order']:
        if bool(element['checked']) != bool(f'{element["id"]}-checked' in data):
            changed.append(element['id'])
    try:
        Data.reorder_list(lid, new_order)
        Data.toggle_list(lid, changed)
    except ValueError as e:
        return render_template('list.html', list=l, is_admin=is_admin, error=str(e))

    return redirect('/')

@app.errorhandler(404)
def handle_404(e):
    return render_template('error.html')
