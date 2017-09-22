import MDtools as mt
import math
import numpy as np

print('processing...  don\'t touch me\n')
atoms_cell = mt.rdump('cell.dump')[-1].atoms
atoms_sia = mt.rdump('sia_lammps.dump')[-1].atoms

print('reading completed.')
print('start computing...')


def c_distance(r1, r2):
    return math.sqrt(np.dot(r1 - r2, r1 - r2))


def find_neibour(self, atoms):
    atoms_sorted = sorted(
        atoms.items(), key=lambda item: c_distance(item[1].r, self.r))
    self.neibours = [atoms_sorted[0][1], atoms_sorted[1][1]]


def sia_dirction(self):
    dr = self.neibours[1].r - self.neibours[0].r
    maxr = max(abs(dr))
    for i in range(3):
        if abs(dr[i]) / maxr < 0.2:
            dr[i] = 0
    self.dirction = [int(i / abs(i)) if i != 0 else 0 for i in dr]
    self.properties['c_2[1]'] = int(self.properties['c_2[1]'])
    if self.properties['c_2[1]'] == 0:
        self.dirction = [0, 0, 0]
    self.properties['d1'] = self.dirction[0]
    self.properties['d2'] = self.dirction[1]
    self.properties['d3'] = self.dirction[2]


mt.Atom.find_neibour = find_neibour
mt.Atom.sia_dirction = sia_dirction
for k, atom in atoms_cell.items():
    atom.find_neibour(atoms_sia)
    atom.sia_dirction()
    # print(atom.dirction)

step = mt.Step(atoms_cell, 0, mt.rdump('cell.dump')[-1].box)
steps = [step]
mt.wdump(steps, 'cell_direction.dump', [
         'id', 'type', 'x', 'y', 'z', 'c_2[1]', 'd1', 'd2', 'd3'])
print('good luck!')
