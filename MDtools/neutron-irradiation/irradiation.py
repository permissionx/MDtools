
import random
import math
import MDtools as mt

def free_path(lambda_, seed):
	random.seed(seed)
	p = random.random()
	z = -lambda_*math.log(1-p)
	return z

def convert_to_dump(pkas):
	import numpy as np
	atoms = {}
	for pka in pkas:
		atom = mt.Atom({'id':pka[0],'x':pka[2]*1e10,'y':pka[3]*1e10,'z':pka[4]*1e10,'E':pka[5],'time':pka[1]*1e6})
		atoms[atom.id] = atom
	step = mt.Step(atoms, 0, np.array(box)*1e10)
	steps = [step]
	mt.wdump(steps, 'pkas.dump',['id','x','y','z','E','time'])

def irradiation(fluence, box, total_time, seed, lambda_, E_i):
	lx = box[0][1]-box[0][0]
	ly = box[1][1]-box[1][0]
	mean_time = 1/(fluence*lx*ly)
	t = 0 
	pkas = []
	id_ = 0
	while t < total_time:
		seed += 1
		random.seed(seed)
		t += mean_time * random.uniform(0,2)
		z = box[2][1] - free_path(lambda_, seed)
		seed += 1
		if z < box[2][0]:
			continue
		seed += 1
		random.seed(seed)
		E_0 = E_i * random.random()
		seed += 1
		random.seed(seed)
		x = box[0][0] + lx*random.random()
		seed += 1
		random.seed(seed)
		y = box[1][0] + ly*random.random()
		id_ += 1
		pkas.append([id_,t,x,y,z,E_0])
	convert_to_dump(pkas)
	with open('pkas.dat','w') as file:
		file.write('id time(s) x(m) y(m) z(m) E_0(keV)\n')
		for pka in pkas:
			file.write('{0} {1} {2} {3} {4} {5}\n'.format(pka[0],pka[1],pka[2],pka[3],pka[4],pka[5]))
	print(len(pkas))

if __name__ == '__main__':
	#units : m, s , keV
	fluence = 1e18   #  1e18 m^(-2)s^(-1)
	box = [[0,1e-6],[0,1e-6],[-1e-6,0]]
	total_time = 1
	seed = 1
	lambda_ = 0.03 # 3 cm
	E_i = 300 
	irradiation(fluence, box, total_time, seed, lambda_, E_i)

