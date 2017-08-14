import numpy 

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
