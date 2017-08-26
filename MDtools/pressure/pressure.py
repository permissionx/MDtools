import numpy as np 
from numpy import linalg as LA
with open('test.dump','r') as infile:
	with open('out.dump','w') as outfile:
		while True:
			line = infile.readline()
			if not line:
				break
			for i in range(2):
				line = infile.readline()
				outfile.write(line)
			natoms = int(line.split()[0])
			for i in range(5):
				line = infile.readline()
				outfile.write(line)
			properties = line.split()
			sts_i = properties.index('c_2[1]') - 2
			pressure_fore = 0
			for i in range(natoms):
				line = infile.readline()
				words = line.split()
				str = [sts_i : sts_i+6]
				s_mat = np.mat([[str[0],str[3],str[5]],
							[str[3],str[1],str[4]],
							[str[5],str[4],str[2]]])
				eig_mat = LA.eig(s_mat)[1]
				s_d_mat = eig_mat.I * s_mat * eig_mat
				pressure_fore += np.array(s_d_mat)[0][0]+np.array(s_d_mat)[1][1]+np.array(s_d_mat)[2][2]



