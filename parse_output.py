import pandas as pd 
import h5py 
import numpy as np 
import matplotlib.pyplot as plt 

# open the file 
megafile = open("output_sf1.1_enia.tmp", "r") 

halo_id_now = []
halo_id_then = []
mass_now = []
mass_then = []
dyntime = []
mar = []
sf_now = []
sf_then = []

for line in megafile: 
	if "#" in line: continue

	# parse out the file 
	var = line.split(" ")[-1].strip()

	if "accretion rate" in line: 
		var = line.split(" ")[-2].strip()
		mar.append(float(var))
	
	if var == '': continue

	if "halo mass now" in line: 
		mass_now.append(float(var))
	if "halo mass then" in line: 
		mass_then.append(float(var))
	if "dynamical time" in line: 
		dyntime.append(float(var))
	if "scale factor now" in line: 
		sf_now.append(float(var))
	if "scale factor then" in line: 
		sf_then.append(float(var))
	if "ID now" in line: 
		halo_id_now.append(float(var))
	if "ID then" in line: 
		halo_id_then.append(float(var))
	

data = {"mass_now" : mass_now, "mass_then": mass_then, 
"tdyn": dyntime, "MAR": mar, "sf_now": sf_now, "sf_then":sf_then, "id_now": halo_id_then, "id_then":halo_id_then}


dataframe = pd.DataFrame(data=data)

dataframe.to_csv("organized_output.txt")


# WE NEED TO FIND WHICH IS THE RIGHT MASS HE IS USING. FIGURE THIS OUT THROUGH THE CATALOG 

hlist_dir = "/Users/eniaxhakaj/data/gamma_tests/hlist_1.10000.hdf5"
halocat = h5py.File(hlist_dir, "r")
halos = halocat["data"]

# for each of the ID's print the masses, and check if they are the same 

for iID, ID in enumerate(halo_id_now):

	print ("Working with IDs")
	
	# get the mass in the consistent tree code 
	orig_mvir = mass_now[iID]

	# where is this idx in the halocat file 
	rs_id = halocat["data"]["halo_id"]
	rs_idx = np.where(ID==rs_id)[0]

	# get the masses that correspond to that ID 

	m200b_all = halocat["data"]["halo_M200b_all"][rs_idx]
	mvir = halocat["data"]["halo_Mvir"][rs_idx]
	m200b = halocat["data"]["halo_M200b"][rs_idx]

	print (ID, orig_mvir, m200b_all, m200b, mvir)

plt.figure()
plt.title("Orig Mvir vs M200b")
plt.scatter(mass_now, m200b)
plt.ylabel("M200b")
plt.xlabel("Orig_Mvir")
plt.grid()
plt.savefig("/Users/eniaxhakaj/Desktop/scatter_origmvir_m200b.png")






