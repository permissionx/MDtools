class Step:
	def __init__(self, atoms, count):
		self.atoms = atoms   # dict
		self.count = count

class Atom:
	def __init__(self, properties):
		for key in properties.keys():
			properties[key] = float(properties[key])
		for intkey in ['id','type']:
			if intkey in properties.keys():
				properties[intkey] = int(properties[intkey])
		self.properties = properties 	# dict



def read(filename):
	steps = []
	with open(filename,'r') as file:
		while True:
			line = file.readline()
			if not line:
				break
			line = file.readline()
			count_step = int(line.split()[0])
			for i in range(2):
				line = file.readline()
			natoms = int(line.split()[0])
			for i in range(5):
				line = file.readline()
			kws = line.split()[2:]
			atoms = {}
			for i in range(natoms):
				line = file.readline()
				words = line.split()
				properties = {}
				for kw in kws:
					properties[kw] = words[kws.index(kw)]
				atom = Atom(properties)
				if 'id' in kws:
					atoms[atom.properties['id']] = atom
				else:
					atoms[i] = atom
			step = Step(atoms, count_step)
			steps.append(step)
	return steps

if __name__ == '__main__':
	steps = read('H.dump')