from json import load, dump
from random import shuffle

from configs import ELEMENTS


class Lists:
    lists = {}

    def load():
        with open('lists.json') as f:
            Lists.lists = load(f)

    def save():
        with open('lists.json', 'w') as f:
            dump(Lists.lists, f)

    def create(name, step, elements):
        if Lists.get(name):
            raise ValueError('Lists already exists')
        elif step > elements:
            raise ValueError('Step too big')
        elif any([e not in ELEMENTS for e in elements]):
            raise ValueError('Invalid elements')

        l = {"name": name, "step": step, "elements": elements, "checked": []}
        save()

    def generate(name, step):
        elements = [e for e in ELEMENTS]
        shuffle(elements)
        return Lists(name, step, elements)

    def get(name):
        return Lists.lists.get(name)

    def get_names():
        return list(Lists.lists.keys())

    def get_dashboard():
        dashboard = {}
        
        for data in Lists.lists.values():
            name = data["name"]
            step = data["step"]
            elements = [e for e in data["elements"] if e not in data["checked"]]

            if elements:
                dashboard[name] = [elements[:step]]
        
                if len(elements) > step:
                    dashboard[name].append(elements[step : 2*step+1])
        
        return dashboard

    def check_elements(name, elements):
        if not Lists.get(name):
            raise ValueError("List doesn't exist")

        Lists.lists[name]["checked"].extend(elements)
        Lists.save()

    def delete(name):
        if not Lists.get(name):
            raise ValueError("List doesnt't exist")

        del Lists.lists[name]
        Lists.save()
