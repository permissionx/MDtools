import MDtools as mt

steps = mt.rdump('cell.dump')
displacements = []
for step in steps:
	displacement = 0
	for k,atom in step.atoms.items():
		if atom.properties['c_2[1]'] == 0:
			displacement += 1
	displacements.append(displacement)
steps = []


times = []
with open('log.lammps','r') as log:
	flag = 0
	while True:  # 这有点难 ( ╯□╰ ) 谔谔
		line = log.readline()
		if line == "Step Time Dt Temp \n":
			flag += 1
		elif line[:8] == "Fix halt":
			break
		elif flag == 2:
			words = [float(word) for word in line.split()]
			time = words[1] - 1.0
			times.append(time)

with open('results/process.data','w') as file:
	for time,displacement in zip(times,displacements):
		file.write('{0} {1}\n'.format(time, displacement))
