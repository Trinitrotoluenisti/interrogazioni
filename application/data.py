from json import load, dump
from copy import deepcopy
from random import shuffle


class Data:
    lists = {}
    elements = {}


    def load():
        with open('application/data.json') as f:
            data = load(f)

        Data.lists = data['lists']
        Data.elements = data['elements']

    def save():
        data = {'lists': Data.lists, 'elements': Data.elements}

        with open('application/data.json', 'w') as f:
            dump(data, f, indent=4)


    def get_elements():
        return deepcopy(list(Data.elements.values()))

    def get_element(eid):
        return deepcopy(Data.elements.get(str(eid)))

    def get_element_by_name(name):
        for e in Data.elements.values():
            if e['name'] == name:
                return dict(e)

    def get_element_dashboard(eid):
        eid = int(eid)

        if not Data.get_element(eid):
            return None

        dashboard = {'first': [], 'second': [], 'other': [], 'done': []}

        for l in Data.get_lists():
            elements = [o['id'] for o in l['order'] if not o['checked']]

            if not eid in elements:
                dashboard['done'].append([0, l['name'], l['id']])
            elif (i := elements.index(eid)) < l['step']:
                dashboard['first'].append([i, l['name'], l['id']])
            elif i < 2*l['step']+1:
                dashboard['second'].append([i, l['name'], l['id']])
            else:
                dashboard['other'].append([i, l['name'], l['id']])

        dashboard['first'].sort()
        dashboard['second'].sort()
        dashboard['other'].sort()
        dashboard['done'].sort()

        return dashboard


    def get_lists():
        return deepcopy(list(Data.lists.values()))

    def get_list(lid):
        return deepcopy(Data.lists.get(str(lid)))

    def get_list_by_name(name):
        for lid, l in Data.lists.items():
            if l['name'] == name:
                return Data.get_list(lid)

    def generate_list(name, step):
        order = Data.get_elements()
        shuffle(order)

        if Data.get_list_by_name(name):
            raise ValueError('Nome già usato')
        elif step > len(order) or step < 1:
            raise ValueError('Numero di interrogati non valido')

        if Data.lists:
            lid = str(max(map(int, Data.lists.keys())) + 1)
        else:
            lid = 1

        for o in order:
            o.update(checked=False)

        Data.lists[lid] = {"name": name, "id": lid, "step": step, "order": order}
        Data.save()

    def delete_list(lid):
        lid = str(lid)

        if not Data.get_list(lid):
            raise ValueError('La lista specificata non esiste')

        del Data.lists[lid]
        Data.save()

    def toggle_list(lid, eids):
        l = Data.get_list(lid)
        if not l:
            raise ValueError('La lista specificata non esiste')

        eids = list(map(int, eids))
        oids = [o['id'] for o in l['order']]
        if not all([eid in oids for eid in eids]):
            raise ValueError('Uno o più studenti non sono in lista')

        for oid, o in enumerate(l['order']):
            if o['id'] in eids:
                Data.lists[str(lid)]['order'][oid]['checked'] = not o['checked']
                Data.save()

    def reorder_list(lid, eids):
        l = Data.get_list(lid)
        if not l:
            raise ValueError('La lista specificata non esiste')

        eids = list(map(int, eids))
        if set(eids) != {e['id'] for e in l['order']} or len(eids) != len(l['order']):
            raise ValueError('Nel nuovo ordine mancano studenti o ce ne sono di nuovi')

        new_order = []
        old_order = {e['id']: e for e in l['order']}

        for eid in eids:
            new_order.append(old_order[eid])

        Data.lists[str(lid)]['order'] = new_order
        Data.save()

    def get_lists_dashboard():
        dashboard = []
        
        for l in Data.get_lists():
            step = l["step"]
            elements = [e['name'] for e in l["order"] if not e['checked']]

            if elements:
                l = {'name': l['name'],
                      'id': l['id'],
                      'first_group': elements[:step],
                      'second_group': []}

                if len(elements) > step:
                    l['second_group'] = elements[step : 2*step+1]

                dashboard.append(l)
        
        return dashboard
