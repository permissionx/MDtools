import MDtools as mt
import numpy as np
import math
import matplotlib.pyplot as plt
import os


def distance(r1, r2):
    return math.sqrt((r2[0] - r1[0])**2 + (r2[1] - r1[1])**2 + (r2[2] - r1[2])**2)


steps = mt.rdump('cell_direction.dump')

atoms = steps[0].atoms

s_center = np.array([0., 0., 0.])
s_n = 0
v_center = np.array([0., 0., 0.])
v_n = 0
for id_, atom in atoms.items():
    if atom.properties['c_2[1]'] >= 2:
        s_center += atom.r
        s_n += 1
    else:
        v_center += atom.r
        v_n += 1

s_center /= s_n
v_center /= v_n

s_dis = 0
v_dis = 0
s_diss = []
v_diss = []
for id_, atom in atoms.items():
    if atom.properties['c_2[1]'] == 2:
        s_dis += distance(atom.r, s_center)
        s_diss.append(distance(atom.r, s_center))
    else:
        v_dis += distance(atom.r, v_center)
        v_diss.append(distance(atom.r, v_center))
s_dis /= s_n
v_dis /= v_n

os.system('mkdir results')

with open('results/global.out', 'w') as file:
    file.write('Number_of_sias {0}\n'.format(s_n))
    file.write('Number_of_vacancies(or the displacements) {0}\n'.format(v_n))
    file.write('Range_of_sias(Angstrom) {0}\n'.format(s_dis))
    file.write('Range_of_vacancies(Angstrom) {0}\n'.format(v_dis))


fig, ax = plt.subplots()
n, bins, patches1 = ax.hist(s_diss, 25, alpha=0.8, normed=1, label='Sias')
n, bins, patches2 = ax.hist(v_diss, 25, alpha=0.8,
                            normed=1, label='Vacancies or vaccums')
plt.legend()
plt.xlabel(r"Distance to the center of mass (${\rm \AA}$)")
plt.ylabel("Probability")
plt.title('Defect cluster spatial distribution')
plt.savefig('results/spatial_distribution.jpg', dpi=1200)


import MDtools.group_cluster as mgc
groups = mgc.divide_atoms(atoms, 6)
groups_v = [group for group in groups
            if list(group.direction) == [0, 0, 0]]
groups_s111 = [group for group in groups
               if abs(group.direction)[0] + abs(group.direction)[1] + abs(group.direction)[2] == 3]
groups_s110 = [group for group in groups
               if abs(group.direction)[0] + abs(group.direction)[1] + abs(group.direction)[2] == 2]
groups_s100 = [group for group in groups
               if abs(group.direction)[0] + abs(group.direction)[1] + abs(group.direction)[2] == 1]
vsizes = [len(group.members) for group in groups_v]
s111sizes = [len(group.members) for group in groups_s111]
s110sizes = [len(group.members) for group in groups_s110]
s100sizes = [len(group.members) for group in groups_s100]

max_cluster = max([max(vsizes), max(s111sizes),
                   max(s110sizes), max(s100sizes)])

fig, ax = plt.subplots()
n1, bins1, patches1 = ax.hist(vsizes, max_cluster + 1, range=(1, max_cluster + 1),
                              alpha=0.5, label='Vacancies or vaccums')
n2, bins2, patches2 = ax.hist(s111sizes, max_cluster + 1, range=(1, max_cluster + 1),
                              alpha=0.5, label='[111] sias')
n3, bins3, patches2 = ax.hist(s110sizes, max_cluster + 1, range=(1, max_cluster + 1),
                              alpha=0.5, label='[110] sias')
n4, bins4, patches2 = ax.hist(s100sizes, max_cluster + 1, range=(1, max_cluster + 1),
                              alpha=0.5, label='[100] sias')

fix, ax = plt.subplots()
plt.bar(bins1[:-1], n1, 0.8, label='Vacancies or vaccums')
plt.bar(bins2[:-1], n2, 0.8, bottom=n1, label='[111] sias')
plt.bar(bins3[:-1], n3, 0.8, bottom=n1 + n2, label='[110] sias')
plt.bar(bins4[:-1], n4, 0.8, bottom=n1 + n2 + n3, label='[100] sias')
plt.ylim(0, max(n1+n2+n3+n4)*1.1)
plt.xlabel('Cluster size')
plt.ylabel('Cluster numebr')
plt.title('Defect cluster size distribution')
plt.legend()
plt.savefig('results/size.jpg', dpi=1200)
