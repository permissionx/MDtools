def msd_one(steps, nplot, istep, timestep):
	'''
	compute msd of a single atom
	unit: Angstrom^2/ps
	'''
	step_dt = (steps[1].count - steps[0].count)*timestep
	rs = ajust_boundary(steps)
	avemsd = {}
	for inter_point in range(1,nplot+1):
		inter_step = inter_point * istep
		cstep = 0
		tmsd = 0
		nadd = 1
		while cstep+inter_step < len(steps):
			tmsd += dr2(rs[cstep+inter_step],rs[cstep])
			cstep += 1
			nadd += 1
		avemsd[inter_step*step_dt] = tmsd / nadd
		print('Number of inter points: {0}'.format(inter_point))
	return avemsd

def dr2(r0,r1):
	result = (r1[0]-r0[0])**2 + (r1[1]-r0[1])**2 + (r1[2]-r0[2])**2 
	return result


def ajust_boundary(steps):
	rs = [[],[],[]]
	key = list(steps[0].atoms.keys())[0]
	for step in steps:
		for x,xname in zip(rs,['x','y','z']):
			x.append(step.atoms[key].properties[xname])
	for xs,d in zip(rs,range(3)):
		for i in range(len(xs)-1):
			boundary = steps[i].box[d]
			lenth = boundary[1]-boundary[0]
			dx = xs[i+1] - xs[i]
			if -1/2*lenth < dx < 1/2*lenth:
				pass
			elif dx > 1/2*lenth:
				j = i+1
				while j <= len(xs):
					xs[j] -= lenth
					j += 1
			else:
				j = i+1
				while j <= len(xs):
					sz[j] += lenth
					j += 1
	return list(zip(rs[0],rs[1],rs[2]))

if __name__ == '__main__':
	import MDtools as mt
	file = input('test file: ')
	steps = mt.rdump(file)
	print(len(steps))
	nplot = int(input('nplot: '))
	istep = int(input('init_delta_step: '))
	timestep = float(input('timestep: '))
	msd = msd_one(steps, nplot, istep, timestep)




