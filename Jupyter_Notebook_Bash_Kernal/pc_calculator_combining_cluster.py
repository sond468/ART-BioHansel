"""
Creating "contaminated" data
David Son
"""
import os
import shutil
import sys
#----------------------------------------------------------------------------------------
#									DEFINING FUNCTIONS
#Separate generator function for rawpycount
def _make_gen(reader):
	b = reader(1048576)
	while b:
		yield b
		b = reader(1048576)

#Counting the lines of one file
def rawpycount(filename):
	f = open(filename,'rb')
	f_gen = _make_gen(f.raw.read)
	return sum(buf.count(b'\n') for buf in f_gen)

#Ensuring the final number of lines is a multiple of four because of fq files	
def rounding(rounding_number):
	return int(4 * round(float(rounding_number)/4))

#----------------------------------------------------------------------------------------
#						       INITIALIZING VARIABLES 
#Inputting a .txt file name of all the files to run through
file_name = 'combining_list'
percentage = float(sys.argv[1])
files = []
lines_list = []
first_pc_list = []
sec_pc_list = []
other_percent = 1.00 - percentage
if other_percent == percentage:
	other_percent = "second_percentage"
#----------------------------------------------------------------------------------------
#					MAKING THE LISTS OF FILES AND PERCENTAGE OF LINES
#Filtering the txt files to format the file names into a list
file_list = open(file_name+'.txt','r')
for lines in file_list:
	files.append(lines.strip())
file_list.close()

#Finding how many lines makes up the stated percentage
for i in files:
	lines_list.append(rounding(rawpycount(i) * percentage))
	
#Finding the number of lines in each genome ***REPLACED THIS WITH THE NEW FUNCTIONS
#for i in files:
#	with open(i,'r') as f:
#		total_rows = sum(1 for row in f)
#		print(total_rows)
	
#----------------------------------------------------------------------------------------	
#                     REWRITING ORIGINAL FILE INTO TWO NEW FQ FILES
#Opening each file in the list 'files' and then writing them into two new files
for looping in range(len(files)):
	count1 =0
	with open(files[looping], 'r') as f:
		with open(str(percentage)+'_'+files[looping],'w') as outf:
			for rows in f:
				outf.write(rows)
				count1 += 1
				#breaking the loop after it reaches the line of the specified percentage
				if count1 == lines_list[looping]:
					break
		#writing the rest of the original file into this new file
		with open(str(other_percent)+'_'+files[looping], 'w') as secondoutf:
			for rows2 in f:
				secondoutf.write(rows2)


full_dir = os.listdir()
#Creating a list of all the files for the first percentage
for first_list in full_dir:
	if str(percentage) in first_list:
		first_pc_list.append(first_list)

#Creating a list of all the files for the second percentage
for second_list in full_dir:
	if str(other_percent) in second_list:
		sec_pc_list.append(second_list)

gettingpath = os.getcwd()
#Combining the two files together
for small in first_pc_list:
	with open(small,'rb') as fin:
		for big in sec_pc_list:
			fin.seek(0)
			with open(gettingpath+'/combined_files/'+small[:-3]+"-"+big,'wb') as outing:
				with open(big,'rb') as f2in:
					shutil.copyfileobj(f2in,outing)
				shutil.copyfileobj(fin,outing)
