from dataclasses import dataclass, field
from pickle import load, dump
from random import shuffle


# Instances containers
students = set()
lists = set()


@dataclass
class Student:
    index: int = field(init=False)
    name: str

    def __post_init__(self):
        # Calculates the index
        self.index = len(students)

        # Checks if the name is unique
        if self.name in [s.name for s in students]:
            raise ValueError('Esiste già uno studente con lo stesso nome')

        # Appends the student to the container
        students.add(self)
        save_data()

    @staticmethod
    def by_index(index):
        # Search for a student with that index
        for s in students:
            if s.index == index:
                return s

        # If there isn't anyone with that id it raises an error
        raise ValueError('Studente non trovato')

    def __hash__(self):
        return id(self)

@dataclass
class List:
    index: int
    name: str
    step: int
    order: list

    def __post_init__(self):
        # If the index is set to -1 it calculates a new one,
        # otherwise it checks if it's valid
        if self.index == -1:
            self.index = 1 if (not len(lists)) else (max([l.index for l in lists]) + 1)
        elif self.index < 0:
            raise ValueError('Indice della lista non valido')

        # Checks if the name is unique
        if self.name in [l.name for l in lists]:
            raise ValueError('Esiste già una lista con lo stesso nome')

        # Checks if step is valid
        if self.step < 1 or self.step > len(students):
            raise ValueError('Step troppo grande/piccolo')

        # Creates an order if it isn't given
        if not self.order:
            self.order = [[i, False] for i in range(len(students))]
            shuffle(self.order)
        else:
            # If it's given ensures that it's valid
            if len(self.order) != len(students):
                raise ValueError('Ci sono troppi o troppi pochi studenti nella lista')
            elif not all([len(o) == 2 for o in self.order]):
                raise ValueError('Il formato dell\'ordine non è valido')
            elif not all([o[0] in range(len(students)) for o in self.order]):
                raise ValueError('Alcuni studenti della lista non esistono')

        # Saves the list in the container
        lists.add(self)
        save_data()

    def toggle_students(self, toggled):
        # Ensures that all the students exist
        for student in toggled:
            if student not in range(len(students)):
                raise ValueError('Alcuni studenti della lista non esistono')

        # Toggles their values
        for student in toggled:
            for o in self.order:
                if o[0] == student:
                    o[1] = not o[1]
                    continue

        # Saves changes
        save_data()

    def change_order(self, new_order):
        # Checks if the new order has the same students of
        # the previous one
        if len(new_order) != len(self.order):
            raise ValueError('Ci sono troppi o troppi pochi studenti nel nuovo ordine')
        elif len(new_order) != len(set(new_order)):
            raise ValueError('Alcuni studenti sono duplicati')
        elif [no for no in new_order if no not in range(len(students))]:
            raise ValueError('Alcuni studenti della lista non esistono')

        # Gets the students' values from the previous order
        for i in range(len(new_order)):
            for o in self.order:
                if o[0] == new_order[i]:
                    new_order[i] = [new_order[i], o[1]]
                    break

        # Saves the new one
        self.order = new_order

        # Saves changes
        save_data()

    def delete(self):
        lists.remove(self)

        # Saves changes
        save_data()

    @staticmethod
    def by_index(index):
        # Search for a list with that index
        for l in lists:
            if l.index == index:
                return l

        # If there isn't anyone with that id it raises an error
        raise ValueError('Lista non trovata')

    def __hash__(self):
        return id(self)


def save_data():
    global students, lists

    # Exports data to data.dat
    with open('application/data.dat', 'wb') as f:
        dump([students, lists], f)

def load_data():
    global students, lists

    try:
        # Imports data from data.dat
        with open('application/data.dat', 'rb') as f:
            students, lists = load(f)
    except FileNotFoundError:
        # If data.dat is not found it creates a new file by reading
        # students' data from students.txt
        with open('application/students.txt', 'r') as f:
            for s in f.readlines():
                Student(s.strip())

        # And saves them for the next time
        save_data()
