import os
import sys
import h5py
import numpy as np
import datatable as dt


def ims2csv(file_name, outfile=None):
	#read in image file
	
	file_name = os.path.abspath(file_name)
	f = h5py.File(file_name, 'r')
	#f.visit(print)
	#todo ensure that 'DataSet' and 'ResolutionLevel' each have only 1 key
	
	channel_names = list(f['DataSet']['ResolutionLevel 0']['TimePoint 0'].keys())
	
	
	Cn = [''.join(f['DataSetInfo'][ch].attrs['Name'].astype(str)) for ch in channel_names]
	Dn = [''.join(f['DataSetInfo'][ch].attrs['DyeName'].astype(str)) for ch in channel_names]
	Ex = [round(float(''.join(f['DataSetInfo'][ch].attrs['LSMExcitationWavelength'].astype(str)))) for ch in channel_names]
	Em = [round(float(''.join(f['DataSetInfo'][ch].attrs['LSMEmissionWavelength'].astype(str)))) for ch in channel_names]
	Ex = ['Ex' + str(x) for x in Ex]
	Em = ['Em' + str(x) for x in Em]
	for i in range(len(Dn)):
		if Dn[i] == '':
			Dn[i] = Ex[i] + '/' + Em[i]
	
	nice_names = [Cn + " [" + Dn + "]" for Cn, Dn in zip(Cn, Dn)]
	
	a = [f['DataSet']['ResolutionLevel 0']['TimePoint 0'][ch]['Data'] for ch in channel_names]
	
	a=np.stack(a)
	
	a=np.transpose(a)
	
	#flatten array
	
	Zaxis = a.shape[2]
	
	slicer = [np.any(a[:,:,i,:]) for i in range(Zaxis)]
	
	a = a[:,:,slicer,:]
	
	NI, NJ, NK, CH = a.shape
	
	dat = dt.Frame(x = np.repeat(range(NI),NJ*NK), 
	y = np.tile(np.repeat(range(NJ),NK), NI),
	z = np.tile(range(NK), NI*NJ))
	
	
	for ch in range(CH):
		dat[channel_names[ch]] = np.float32(a[:,:,:,ch].flatten())
	del dat.names
	dat.names = ['x', 'y', 'z'] + nice_names
	#save as a csv file
	
	if outfile is None:
		file_name = os.path.basename(file_name)
		base = os.path.splitext(file_name)[0]
		
		new_file_name = base + '.csv'
		
		current_dir = os.getcwd()
		
		new_file_name = os.path.join(current_dir, new_file_name)
	else: new_file_name=outfile
		
	
	dat.to_csv(new_file_name)
	print('file saved to ' + new_file_name)





