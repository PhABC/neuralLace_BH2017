
import numpy as np 
import os
import scipy.io 
rootDir = os.getcwd()

os.chdir(rootDir)
os.chdir("dataAhren")
os.chdir("20140805_1_3_cy74_6d_spon_20140805_170009")
# os.chdir("20140820_2_3_7d_cy74_spon_20140820_171414")
# os.chdir("20140827_1_7_GAD_H2B_6d_spon_20140827_121957")


###########################
###  X Y Z COORDINATES  ###
###########################

# mat = scipy.io.loadmat('cell_info.mat')
# print(mat['cell_info'].shape)

# xyz=[]
# for i in range(102512):
# 	x = mat['cell_info']["center"][0][i][0][0]
# 	y = mat['cell_info']["center"][0][i][0][1]
# 	z = mat['cell_info']["slice"][0][i][0][0]
# 	xyz.append([x,y,z])

# np.save("data_xyz.npy", xyz)

###########################
###     big X matrix    ###
###########################

# mat = scipy.io.loadmat('full_cell_resp.mat')
# np.save("data_X.npy", mat["cell_resp"])

###########################
###    parcel(Y,edge)   ###
###########################

def findcube(neuron, lox,hix, loy,hiy, loz,hiz, edge):
	volind = 0
	zind = loz 
	while zind <= hiz:
		yind = loy
		while yind <= hiy:
			xind = lox
			while xind <= hix:
				volind += 1
				if (xind<=neuron[0]<xind+edge) and (yind<=neuron[1]<yind+edge) and (zind<=neuron[2]<zind+edge):
					# print(volind)
					return volind
				xind += edge
			yind += edge
		zind += edge



def parcel(xyz, edge):

	allX = xyz[:,0]
	allY = xyz[:,1]
	allZ = xyz[:,2]

	# print(xyz.shape)
	minx,maxx = [np.min(allX), np.max(allX)]
	miny,maxy = [np.min(allY), np.max(allY)]
	minz,maxz = [np.min(allZ), np.max(allZ)]
	# print(minx,maxx,miny,maxy,minz,maxz)

	cube_labels_for_neurons = np.zeros(len(xyz))
	for neurIND,neuron in enumerate(xyz):
		tmp = findcube(neuron, minx,maxx, miny,maxy, minz,maxz, edge)
		cube_labels_for_neurons[neurIND] = int(tmp)
		# print(neurIND,neuron,tmp)
		if neurIND %10000 ==0:
			print(neurIND)

	return cube_labels_for_neurons


def cube_removal(cube_labels, min_num_neurons):	
	cube_labels_final = cube_labels
	all_labels = {}
	for lbl in cube_labels_final:
		if lbl not in all_labels:
			all_labels[int(lbl)] = 1
		else:
			all_labels[int(lbl)] +=1

	# print(all_labels)	
	for lbl in all_labels:
		if all_labels[lbl] < min_num_neurons:
			all_labels[lbl] = -1
	# print(all_labels) 	

	for neurIND,neuron in enumerate(cube_labels_final):
		if all_labels[neuron] < 0:
			cube_labels_final[neurIND] = int(-1)
			# print(neurIND, cube_labels[neurIND])

	return	cube_labels_final
	



data_xyz = np.load("data_xyz.npy")
print(data_xyz.shape)


cubSize = 50
cube_labels = parcel(data_xyz, cubSize)
np.save("parcellation_cube"+str(cubSize)+".npy", cube_labels)

min_neurons_thres = 50
cube_labels_removed = cube_removal(cube_labels, min_neurons_thres)
np.save("parcellation_cube"+str(cubSize)+"_min"+str(min_neurons_thres)+".npy", cube_labels_removed)



fout = open("output_cube"+str(cubSize)+"_min"+str(min_neurons_thres)+".txt", "w")
for obj in cube_labels:
	fout.write(str(int(obj))+"\n")
fout.close()
