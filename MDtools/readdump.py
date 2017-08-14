import numpy as np

class Step:
	def __init__(self, atoms, count, box):
		self.atoms = atoms   # dict
		self.count = count
		self.box = box

class Atom:
	def __init__(self, properties):
		for key in properties.keys():
			properties[key] = float(properties[key])
		for intkey in ['id','type']:
			if intkey in properties.keys():
				properties[intkey] = int(properties[intkey])
		self.properties = properties 	# dict
		self.packacge()
	def packacge(self):
		properties = self.properties
		keys = properties.keys()
		if 'x' in keys and 'y' in keys and 'z' in keys:
			self.r = np.array([properties['x'],properties['y'],properties['z']])
		if 'id' in keys:
			self.id = properties['id']
		if 'type' in keys:
			self.type = properties['type']

def rdump(filename):
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
				properties = {}
				for kw in kws:
					properties[kw] = words[kws.index(kw)]
				atom = Atom(properties)
				if 'id' in kws:
					atoms[atom.properties['id']] = atom
				else:
					atoms[i] = atom
			step = Step(atoms, count_step, box)
			steps.append(step)
	return steps

if __name__ == '__main__':
	filename = input('dump file name: ')
	steps = read(filename)