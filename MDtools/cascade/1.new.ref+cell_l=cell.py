import pandas as pd
import MDtools as mt


def rdump(filename):
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
            kws = line.split()[3:]
            dir = {}
            for kw in kws:
                dir[kw] = []
            index = []
            for i in range(natoms):
                line = file.readline()
                words = [float(word) for word in line.split()]
                for word, kw in zip(words[1:], kws):
                    dir[kw].append(word)
                index.append(int(words[0]))
                if i % 100000 == 0:
                    print('Loading atoms:', i)
            atoms = pd.DataFrame(dir, index)
            dir = {}
            step = mt.Step(atoms, count_step, box)
            steps.append(step)
    return steps


def sia_va(refdump, cascadedump, siavadump):
    steps = rdump(refdump)
    refatoms = steps[0].atoms
    #print('Loading reference atoms...')
    #refatoms = pd.read_csv('refatoms.csv',index_col = 0)
    #print('Loading compeleted!')
    with open(cascadedump, 'r') as file:
        cascade_lines = file.readlines()
    with open(siavadump, 'w') as file:
        nline = 0
        nstep = 0
        while nline < len(cascade_lines):
            for i in range(4):
                line = cascade_lines[nline]
                file.write(line)
                nline += 1
            ndefects = int(line.split()[0])
            for i in range(4):
                line = cascade_lines[nline]
                file.write(line)
                nline += 1
            for i in range(1):
                line = "ITEM: ATOMS id type x y z c_2[1]\n"
                file.write(line)
                nline += 1
            for i in range(ndefects):
                line = cascade_lines[nline]
                words = line.split()
                id = int(words[0])
                r = list(refatoms.ix[id, ['x', 'y', 'z']])
                words = words[:2] + [str(xs) for xs in r] + words[2:]
                words[2:5] = [str(xs) for xs in r]
                line = "{0} {1} {2} {3} {4} {5}\n".format(
                    words[0], words[1], words[2], words[3], words[4], words[5])
                file.write(line)
                nline += 1
            nstep += 1
            print(nstep, ndefects)


if __name__ == '__main__':
    print('Processing')
    sia_va(refdump='ref.dump', cascadedump='cell_lammps.dump',
           siavadump='cell.dump')
    #steps = rdump(refdump)
    #refatoms = steps[0].atoms
    # refatoms.to_csv('refatoms.csv')
    print('Good Luck!')

