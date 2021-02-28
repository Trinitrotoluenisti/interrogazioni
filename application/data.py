from json import load, dump
from random import shuffle


class Data:
    lists = {}
    elements = {}

    # Save and load

    def load():
        with open('application/data.json') as f:
            data = load(f)

        Data.lists = data['lists']
        Data.elements = data['elements']

    def save():
        data = {'lists': Data.lists, 'elements': Data.elements}

        with open('application/data.json', 'w') as f:
            dump(data, f, indent=4)


    # Elements

    def get_elements():
        return list(Data.elements.values())

    def get_element(eid):
        return Data.elements.get(str(eid)).copy()

    def get_element_by_name(name):
        for e in Data.elements.values():
            if e['name'] == name:
                return dict(e)

    def get_element_dashboard(eid):
        if not Data.get_element(eid):
            return None

        dashboard = {'first': [], 'second': [], 'other': [], 'done': []}

        for l in Data.get_lists():
            elements = [o['id'] for o in l['order'] if not o['checked']]

            if not eid in elements:
                dashboard['done'].append([0, l['name']])
            elif (i := elements.index(eid)) < l['step']:
                dashboard['first'].append([i, l['name']])
            elif i < 2*l['step']+1:
                dashboard['second'].append([i, l['name']])
            else:
                dashboard['other'].append([i, l['name']])

        dashboard['first'].sort()
        dashboard['second'].sort()
        dashboard['other'].sort()
        dashboard['done'].sort()

        return dashboard

    # Lists

    def get_lists():
        return list(Data.lists.values())

    def get_list(lid):
        return Data.lists.get(str(lid)).copy()

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

        lid = str(max(map(int, Data.lists.keys())) + 1)

        for o in order: o.update(checked=False)

        Data.lists[lid] = {"name": name, "id": lid, "step": step, "order": order}
        Data.save()

    def delete_list(lid):
        if not Data.get_list(lid):
            raise ValueError('La lista specificata non esiste')

        del Data.lists[lid]
        Data.save()

    def update_list(lid, eid):
        l = Data.get_list(lid)

        if not l:
            raise ValueError('La lista specificata non esiste')

        for oid, o in enumerate(l['order']):
            if o['id'] == eid:
                if o['checked']:
                    raise ValueError('Lo studente è già stato interrogato')
                else:              
                    Data.lists[str(lid)]['order'][oid]['checked'] = True
                    Data.save()
                    return
        
        raise ValueError('Lo studente selezionato non è nella lista')

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
