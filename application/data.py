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
            dump(Data, f, indent=4)


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

        for l in Data.get_lists(False):
            elements = [o[0] for o in l['order'] if not o[1]]

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

    def get_lists(pretty=True):
        lists = []

        for l in Data.lists.keys():
            lists.append(Data.get_list(l, pretty))

        return lists

    def get_list(lid, pretty=True):
        l = Data.lists.get(str(lid)).copy()

        if l and pretty:
            l['order'] = [(Data.get_element(e[0])['name'], e[1]) for e in l['order']]

        return l

    def get_list_by_name(name):
        for lid, l in Data.lists.items():
            if l['name'] == name:
                return Data.get_list(lid)

    def create_list(name, step, order):
        if Data.get_list_by_name(name):
            raise ValueError('Name already used')
        elif step > len(order) or step < 1:
            raise ValueError('Invalid step')
        elif len(order) < 2:
            raise ValueError('Invalid order')
        elif any([not Data.get_element_by_name(e) for e in order]):
            raise ValueError('Invalid elements in order')

        lid = max(Data.lists.keys()) + 1
        order = [(Data.get_element_by_name(o)['id'], False) for o in order]
        Data.lists[lid] = {"name": name, "id": lid, "step": step, "order": order}
        Data.Save()

    def generate_list(name, step):
        order = [e['name'] for e in Data.get_elements()]
        shuffle(order)
        Data.create(name, step, order)

    def delete_list(lid):
        if not Data.get_list(lid):
            raise ValueError("List doesnt't exist")

        del Data.lists[lid]
        Data.save()

    def update_list(ld, elements):
        if not (l := Data.get_list(lid)):
            raise ValueError("List doesn't exist")
        elif not all(Data.get_element(eid) for eid in elements):
            raise ValueError("Some elements don't exist")
        elif not all(e[1] == False for e in l['order'] if e[0] in elements):
            raise ValueError("Some elements are already checked")

        for eid in elements:
            Data.lists[lid]['order'][eid][1] = True
        
        Data.save()

    def get_lists_dashboard():
        dashboard = []
        
        for l in Data.get_lists():
            step = l["step"]
            elements = [e[0] for e in l["order"] if not e[1]]

            if elements:
                l = {'name': l['name'],
                      'id': l['id'],
                      'first_group': elements[:step],
                      'second_group': []}

                if len(elements) > step:
                    l['second_group'] = elements[step : 2*step+1]

                dashboard.append(l)
        
        return dashboard
