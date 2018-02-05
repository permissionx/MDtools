import MDtools as mt
import math
import numpy as np


def get_swallowed(self):
    self.swallowed = 1


def fresh(self):
    if hasattr(self, 'swallowed'):
        del self.swallowed


mt.Atom.get_swallowed = get_swallowed
mt.Atom.fresh = fresh


def atoms_dis(atom1, atom2):
    dr = atom1.r - atom2.r
    dis = math.sqrt(dr[0] * dr[0] + dr[1] * dr[1] + dr[2] * dr[2])
    return dis


class Group:
    def __init__(self, atoms):
        self.members = atoms
        self.size = len(atoms)
        for id, atom in atoms.items():
            atom.get_swallowed()
        self.direction = np.array([list(atoms.items())[0][1].properties['d1'],
                          list(atoms.items())[0][1].properties['d2'],
                          list(atoms.items())[0][1].properties['d3']])

    def add_member(self, atom):
        self.members[atom.id] = atom
        self.size += 1
        atom.get_swallowed()

    def center(self):
        r = np.array([0., 0., 0.])
        for id, atom in self.members.items():
            r += atom.r
        return r / self.size

    def swallow(self, atoms, cut):
        self.fulled = 0
        while True:
            if self.fulled:  #
                break
            addids = []
            for id, atom in atoms.items():
                if not hasattr(atom, 'swallowed'):
                    for idm, member in self.members.items():
                        if atoms_dis(atom, member) < cut:
                            if (np.array([atom.properties['d1'], atom.properties['d2'], atom.properties['d3']]) == self.direction).all():
                                addids.append(id)
                                break
                            elif (np.array([atom.properties['d1'], atom.properties['d2'], atom.properties['d3']]) == -1 * self.direction).all():
                                addids.append(id)
                                break
            for id in addids:
                self.add_member(atoms[id])
            if len(addids) == 0:
                self.fulled = 1


def divide_atoms(atoms, cut):
    groups = []
    for id, atom in atoms.items():
        atom.fresh()
    for id, atom in atoms.items():
        if not hasattr(atom, 'swallowed'):
            group = Group({atom.id: atom})
            group.swallow(atoms, cut)
            groups.append(group)
    return groups


if __name__ == '__main__':
    steps = mt.rdump('loop.dump')
    atoms = steps[0].atoms
    groups = divide_atoms(atoms, 10)
    print(len(groups))
    print(len(groups[0].members))
    print(groups[1].size)
