from json import load, dump
from random import shuffle

from .configs import ELEMENTS


class Lists:
    lists = {}
    names = {}

    def load():
        with open('application/lists.json') as f:
            lists = load(f)

        Lists.lists.clear()
        Lists.names.clear()
        for data in lists:
            Lists.lists[data['id']] = data
            Lists.names[data['id']] = data['name']

    def save():
        with open('application/lists.json', 'w') as f:
            dump(list(Lists.lists.values()), f, indent=4)

    def create(name, step, order):
        if name in Lists.names.values():
            raise ValueError('Lists already exists')
        elif step > order:
            raise ValueError('Step too big')
        elif any([e not in ELEMENTS for e in order]):
            raise ValueError('Invalid items in order')

        list_id = max(Lists.names.keys()) + 1
        Lists.names[list_id] = name
        Lists.lists[list_id] = {"name": name,
                                "id": list_id,
                                "step": step,
                                "order": [(o, False) for o in order]}

        Lists.Save()

    def generate(name, step):
        order = [e for e in ELEMENTS]
        shuffle(order)
        Lists.create(name, step, order)

    def get(identifier):
        return Lists.lists.get(identifier)

    def get_all():
        return Lists.names

    def get_dashboard():
        dashboard = []
        
        for data in Lists.lists.values():
            step = data["step"]
            order = [e[0] for e in data["order"] if not e[1]]

            if order:
                list_ = {'name': data['name'],
                         'id': data['id'],
                         'first_group': order[:step],
                         'second_group': []}

                if len(order) > step:
                    list_['second_group'] = order[step:2*step+1]

                dashboard.append(list_)
        
        return dashboard

    def check_items(list_id, items):
        list_ = Lists.get(list_id)

        if not l:
            raise ValueError("List doesn't exist")

        for item_id in items:
            if item_id not in range(len(list_['order'])):
                raise ValueError("Some items don't exist")
            elif list_['order'][item_id][1]:
                raise ValueError("Some items are already checked")

        for item_id in items:
            list_['order'][item_id][1] = True
        
        Lists.save()

    def delete(list_id):
        if not Lists.get(list_id):
            raise ValueError("List doesnt't exist")

        del Lists.lists[list_id]
        Lists.save()
