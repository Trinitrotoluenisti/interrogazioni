from flask import render_template as render_template_raw
from flask import request, make_response, redirect, abort
from uuid import uuid4

from . import app
from .data import *


# admin is the token of the admin currently logged in.
# If nobody is logged in, admin is an empty string.
admin = ''
is_admin = lambda: ((request.cookies.get('token') == admin) and admin)

# Rewrites render_template in order to check every time if
# the admin is logged in
def render_template(*args, **kwargs):
    return render_template_raw(*args, **kwargs, is_admin=is_admin())


@app.route('/')
def index_route():
    # Prepares the dashboard
    dashboard = [] 

    # Selects all the lists
    for l in lists:
        queue = [o[0] for o in l.order if not o[1]]

        # If there are some unchecked students
        if queue:
            # Divides them in one or two groups
            data = {'index': l.index, 'name': l.name}
            data['group_1'] = queue[:l.step]
            data['group_2'] = (queue[l.step : 2*l.step+1]) if (len(queue) > l.step) else []

            # Changes the ids to the names
            data['group_1'] = list(map(lambda i: Student.by_index(i).name, data['group_1']))
            data['group_2'] = list(map(lambda i: Student.by_index(i).name, data['group_2']))

            dashboard.append(data)

    # Returns index.html
    return render_template('index.html', dashboard=dashboard, index=True)

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    # If it's a GET requests it returns the html page
    if request.method == 'GET':
        return render_template('login.html')
    
    # Reads the given password from form and the real one from the file
    password = request.form.get('password')
    with open('application/password.txt') as f:
        admin_password = f.readlines()[0].strip()

    # Ensures they're the same
    if password != admin_password:
        return render_template('login.html', error='Credenziali invalide'), 401

    # Generates and saves a token for it
    global admin
    admin = uuid4().hex

    # Creates and returns the response
    r = make_response(redirect('/'))
    r.set_cookie('token', admin)
    return r

@app.route('/logout')
def logout_route():
    global admin

    r = make_response(redirect('/'))

    # If the request is from the admin, it logs it out
    if is_admin():
        admin = ''
        r.set_cookie('token', '')

    return r

@app.route('/lists')
@app.route('/students')
def showcase_route():
    # Checks if it has to show lists or students
    path = str(request.url_rule)[1:]

    # Prepares the data
    prompt = 'Seleziona un' + ('a lista' if (path == 'lists') else 'o studente')
    elements = lists if (path == 'lists') else students
    elements = sorted(elements, key=lambda e: e.index)

    # Returns the showcase page
    return render_template('showcase.html', prompt=prompt, elements=elements, path=path)

@app.route('/students/<int:index>')
def student_route(index):
    # Ensures the student exists
    try:
        s = Student.by_index(index)
    except:
        return abort(404)

    # Prepares its dashboard
    dashboard = {'group_1': [], 'group_2': [], 'group_3': [], 'done': []}

    # Checks in all the lists
    for l in lists:
        queue = [o[0] for o in l.order if not o[1]]

        # Checks if the student is checked in that list,
        # otherwise it puts it in onw of the three groups
        if not s.index in queue:
            dashboard['done'].append([-1, l.name, l.index])
        else:
            i = queue.index(s.index)
            group = '1' if i < l.step else ('2' if i < 2 * l.step + 1 else '3')
            dashboard['group_' + group].append([i, l.name, l.index])

    # Sorts the groups' content
    for g in dashboard.values():
        g.sort()

    # Returns student.html
    return render_template('student.html', student=s, dashboard=dashboard)

@app.route('/lists/<int:index>')
def list_route(index):
    # Ensures the list exists
    try:
        l = List.by_index(index)
    except:
        return abort(404)

    # Creates a dashboard with the students in the queue
    dashboard = []
    for position, s in enumerate(l.order):
        dashboard.append([position, s[0], Student.by_index(s[0]).name, s[1]])

    # Returns list.html
    return render_template('list.html', list=l, dashboard=dashboard)

@app.route('/lists/new', methods=['GET', 'POST'])
def new_list_route():
    # If the user isn't an admin it returns the homepage
    if not is_admin():
        return abort(401)

    # If it's a GET request it returns create_list.html
    if request.method == 'GET':
        return render_template('create_list.html')

    # Collects data from the request
    data = dict(request.form)
    
    # Tries to create a new list
    try:
        List(-1, data['name'], int(data['step']), [])
    except ValueError as e:
        return render_template('create_list.html', error=str(e), **data)
    except KeyError:
        return render_template('create_list.html', error='Dati insufficienti', **data)

    return redirect('/')

@app.route('/lists/<int:index>/delete', methods=['POST'])
def delete_list_route(index):
    # Ensures the user is an admin
    if not is_admin():
        return abort(401)

    # Tries to delete the list
    try:
        List.by_index(index).delete()
    except ValueError:
        return abort(404)

    return redirect('/lists')

@app.route('/lists/<int:index>/update', methods=['POST'])
def update_list_route(index):
    # Ensures the user is an admin
    if not is_admin():
        return abort(401)

    # Ensures the list exists
    try:
        l = List.by_index(index)
    except:
        return abort(404)

    # Collects data from the request
    data = dict(request.form)

    try:
        # Calculate the differences between the previous toggled
        # and the new ones
        checked = {s[0] for s in l.order if s[1]}
        new_checked = {int(s.replace('-checked', '')) for s in data if s.endswith('-checked')}

        # Updates them
        l.toggle_students(checked ^ new_checked)
    except ValueError as e:
        return render_template('list.html', list=l, error=str(e))

    try:
        # Calculates the new order
        new_order = {p: i.replace('-order', '') for i, p in data.items() if i.endswith('-order')}
        new_order = [int(new_order[str(i+1)]) for i in range(len(new_order))]

        # Updates it
        l.change_order(new_order)
    except ValueError as e:
        return render_template('list.html', list=l, error=str(e))
    
    return redirect('.')

@app.errorhandler(401)
def handle_401(e):
    return redirect('/')

@app.errorhandler(404)
def handle_404(e):
    # Returns the error page
    return render_template('error.html')
