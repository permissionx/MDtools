def msd_single(steps, id, nplot, istep, ave_level, timestep):
    '''
    compute msd of a single atom
    unit: Angstrom^2, ps
    '''
    step_dt = (steps[1].count - steps[0].count) * timestep
    rs = ajust_boundary(steps, id)
    avemsd = {}
    for inter_point in range(1, nplot + 1):
        inter_step = inter_point * istep
        cstep = 0
        tmsd = 0
        nadd = 0
        while cstep + inter_step < len(steps):
            tmsd += dr2(rs[cstep + inter_step], rs[cstep])
            cstep += int(len(steps) / ave_level)
            nadd += 1
        avemsd[inter_step * step_dt] = tmsd / nadd
        print('Number of inter points and add: {0} {1}'.format(
            inter_point, nadd))
    return avemsd


def dr2(r0, r1):
    result = (r1[0] - r0[0])**2 + (r1[1] - r0[1])**2 + (r1[2] - r0[2])**2
    return result


def ajust_boundary(steps, id):
    rs = [[], [], []]
    key = id
    for step in steps:
        for x, xname in zip(rs, [0, 1, 2]):
            x.append(step.atoms[key].r[xname])
    for xs, d in zip(rs, range(3)):
        for i in range(len(xs) - 1):
            boundary = steps[i].box[d]
            lenth = boundary[1] - boundary[0]
            dx = xs[i + 1] - xs[i]
            if -1 / 2 * lenth < dx < 1 / 2 * lenth:
                pass
            elif dx > 1 / 2 * lenth:
                j = i + 1
                while j < len(xs):
                    xs[j] -= lenth
                    j += 1
            else:
                j = i + 1
                while j < len(xs):
                    xs[j] += lenth
                    j += 1
    return list(zip(rs[0], rs[1], rs[2]))


def compute_msd(steps, ids, timestep=0.0001, istep=1, nplot=10, ave_level=1000):
    '''
    compute average MSD of atoms with id in ids
    '''
    ave_msd = msd_single(steps, ids[0], nplot, istep, ave_level, timestep)
    for id in ids[1:]:
        msd = msd_single(steps, id, nplot, istep, ave_level, timestep)
        for key, value in msd.items():
            ave_msd[key] += value
    for key, value in ave_msd.items():
        ave_msd[key] /= len(ids)
    return ave_msd


def compute_diff_coe(msddata):
    '''
    unit: unit: Angstrom^2/ps
    '''
    from scipy import stats
    times = []
    x2s = []
    for time, x2 in msddata.items():
        times.append(time)
        x2s.append(x2)
    linregress = stats.linregress(times, x2s)
    diff_coe = linregress[0]
    r2 = linregress[2]
    return diff_coe, r2


if __name__ == '__main__':
    import MDtools as mt
    steps = mt.rdump('H1.dump')
    msd = compute_msd(steps, [2001], istep=1000, ave_level=100, nplot=5)
    coe = compute_diff_coe(msd)
    print(coe)
    for k, v in msd.items():
        print(k, v)
