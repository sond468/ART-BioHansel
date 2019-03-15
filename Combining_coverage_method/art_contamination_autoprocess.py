import os
art_file_name = input('file name for sequences: ') 
contamination_number = input('Percent of contaimination wanted (0.00-1.00): ')
art_files = []
first_art = {}
first_count = 0
second_art = {}
second_count = 0
contamination = 60 * float(contamination_number)
contamination_compliment = 60 - contamination

with open(art_file_name+'.txt','r') as f:
	for line in f:
		art_files.append(line.strip())


for i in range(len(art_files)):
	if art_files[i].lower().endswith('.fasta'):
		outnum = art_files[i][:-6]
	elif art_files[i].lower().endswith('.fna'):
		outnum = art_files[i][:-4]
	outing = "art_illumina -ss MSv3 -na -rs 1547652831 -i " + art_files[i]+ " -l 250 -f "+str(contamination)+" -o "+ str(contamination)+"x"+outnum
	os.system(outing)
	first_art[str(contamination)+"x"+outnum+".fq"] = first_count
	first_count += 1

os.system('mkdir first_half_art_files')
os.system('mv *.fq first_half_art_files/')

for i in range(len(art_files)):
	if art_files[i].lower().endswith('.fasta'):
		outnum = art_files[i][:-6]
	elif art_files[i].lower().endswith('.fna'):
		outnum = art_files[i][:-4]
	outing2 = "art_illumina -ss MSv3 -na -rs 1547652831 -i " + art_files[i]+ " -l 250 -f "+str(contamination_compliment)+" -o "+ str(contamination_compliment)+"x"+outnum
	os.system(outing2)
	second_art[str(contamination_compliment)+"x"+outnum+".fq"] = second_count
	second_count += 1

os.system('mkdir second_half_art_files')
os.system('mv *.fq second_half_art_files/')

os.system('mkdir contamination_files')
for first in os.listdir('first_half_art_files/'):
	for second in os.listdir('second_half_art_files/'):
		if first_art[first] == second_art[second]:
			continue
		with open('contamination_files/'+first[:-3]+'-'+second,'a') as outf:
			with open('first_half_art_files/'+first,'r') as firstfile:
				for line in firstfile:
					outf.write(line)
			with open('second_half_art_files/'+second,'r') as secondfile:
				for sline in secondfile:
					outf.write(sline)
