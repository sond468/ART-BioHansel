import os
file_name = 'arts_list'
files=[]
with open(file_name+'.txt','r') as f:
    for line in f:
        files.append(line.strip())

for i in range(len(files)):
    filein = files[i]
    outnum = filein[4:13]
    outing = "art_illumina -ss MSv3 -na -rs 1547652831 -i " + filein+ " -l 250 -f 60 -o "+ outnum
    os.system(outing)