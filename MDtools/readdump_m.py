import MDtools as mt

class


class Atoms

def rdump_m(filename):
    steps = []
    with open(filename, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            line = file.readline()
            count_step = int(line.split()[0])
            for i in range(2):
                line = file.readline()
            natoms = int(line.split()[0])
            file.readline()
            box = []
            for i in range(3):
                line = file.readline()
                box.append([float(word) for word in line.split()])
            line = file.readline()
            kws = line.split()[2:]
            atoms = {}
            for i in range(natoms):
                line = file.readline()
                words = line.split()
                properties = words
                atom = Atom_m(properties)
                atoms[atom.get_property('id',kws)] = atom
            step = mt.Step(atoms, count_step, box)
            steps.append(step)
    return steps,kws


if __name__ == '__main__':
    steps,kws = rdump_m('H2.dump')
