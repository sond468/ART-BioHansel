import os
file_name = input('File name ')
files=[]

with open(file_name+'.txt','r') as f:
	for line in f:
		files.append(line.strip())

for i in range(len(files)):
	filein = files[i]
	outnum = filein[4:13]
	outing = "art_illumina -ss MSv3 -i " + filein+ " -l 250 -f 60 -o "+ outnum
	os.system(outing)
os.system('mkdir art_files')
os.system('mv *.fq art_files/')
