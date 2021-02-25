from flask import render_template

from . import app, Lists


@app.route('/')
def index():
    dashboard = Lists.get_dashboard()
    lists = Lists.get_all()
    return render_template('index.html', dashboard=dashboard, lists=lists)

@app.route('/login')
def login():
    return render_template('login.html')

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
        return index(), 404
