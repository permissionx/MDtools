import numpy as np
from numpy import linalg as LA


def compute_pressure(steps, c_stress='c_2'):
    # unit: bar*A^3
    for step in steps:
        for id_, atom in step.atoms.items():
            sts = [atom.properties[c_stress +
                                   '[{0}]'.format(i)] for i in range(1, 7)]
            stress_mat = np.mat([[sts[0], sts[3], sts[5]],
                                 [sts[3], sts[1], sts[4]],
                                 [sts[5], sts[4], sts[2]]])
            eig_mat = LA.eig(stress_mat)[1]
            diag_mat = eig_mat.I * stress_mat * eig_mat
            pressure_v = np.array(diag_mat)[0][
                0] + np.array(diag_mat)[1][1] + np.array(diag_mat)[2][2]
            atom.properties['ps_v'] = pressure_v

if __name__ == '__main__':
    import MDtools as mt
    filename = input('File name: ')
    steps = mt.rdump(filename)
    compute_pressure(steps)
    mt.wdump(steps, 'ps_v.' + filename)
