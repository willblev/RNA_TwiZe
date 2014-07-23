#!/usr/bin/env python
def compare_files(files_list):
	"""Takes a list of PDB files and their paths, and runs SARA to create pairwise comparisons between RNA structures; outputs comparisons into same directory as input PDBs"""
	from Bio.PDB.PDBParser import PDBParser
	import sys
	import os
	import time
	from math import factorial

	start_time = time.time()
	parser = PDBParser(PERMISSIVE=1,QUIET=1)
	files_path=os.path.dirname(files_list[1])
	import os.path
	filter_file_name="filtered_structures_%d.txt"%len(files_list)

	if os.path.exists(os.path.join(files_path,filter_file_name)):
		print >> sys.stderr, "List of filtered structures already exists!"
		input_list = open (os.path.join(files_path,filter_file_name),"r")
		structures=[]
		for structure in input_list:
			structure=structure.rstrip()
			structures.append(structure)
		time_filtering=time.time()
		input_list.close()
		print >> sys.stderr, structures
		
	else:
		if files_path:   
			print >> sys.stderr, "Beginning structure selection process..."
			filtered_list = open(os.path.join(files_path,filter_file_name),"w")
			structures=[]
			sequences=[]
	
			print >> sys.stderr, "%d PDB files found" % len(files_list)
		
			n=1
			for file in files_list:
				s = parser.get_structure('structure', file)
				for chain in s.get_chains():
					res_num=chain.__len__()
					if res_num > 20 and res_num < 500:
						residues=chain.get_unpacked_list()
						sequence=""
						for residue in residues:
							residue = residue.resname.replace(" ", "")
							if residue.__len__() == 1:
								sequence+=residue
						if sequence not in sequences and sequence.__len__()>0:
							sequences.append(sequence)
							structures.append(os.path.basename(file[:-4])+":"+chain.id)
							print >> sys.stderr, "%s fit filter criteria and was selected." % str(os.path.basename(file[:-4])+":"+chain.id)
							filtered_list.write(os.path.basename(file[:-4])+":"+chain.id+"\n")
				print >> sys.stderr, "%d PDB files left, %d structures saved." %(len(files_list)-n,len(structures))
				n+=1
	
			time_filtering=time.time()
			print >> sys.stderr,"Time of filtering: %f seconds" % (time.time() - start_time)
			filtered_list.close()
		print >> sys.stderr, "Beginning pairwise comparisons with SARA..."

	comparisons=[]
	possible_comparisons=factorial(len(structures))/(factorial(len(structures)-2)*factorial(2))
	print >> sys.stderr, structures
	print >> sys.stderr, "%d total possible pairwise comparisons." % possible_comparisons
	n=1
	from file_finder import find_a_file
	SARA_path=find_a_file("runsara.py")
	for x in range(len(structures)):
		rna1=structures[x][:4]
		chain1=structures[x][5:]
		for y in range(x):
			rna2=structures[y][:4]
			chain2=structures[y][5:]
			output=rna1+":"+chain1+"-"+rna2+":"+chain2
			comparisons.append(output)
			if not os.path.isfile(os.path.join(files_path,"SARA_"+output+".pdb")):
				os.system("python %s %s %s %s %s -p %s -b -e 0.60 -s" %(SARA_path,os.path.join(files_path,rna1+".pdb"),chain1,os.path.join(files_path,rna2+".pdb"),chain2,os.path.join(files_path,"SARA_"+output)))
			else:
				print >> sys.stderr, "File %s already exists; skipping analysis." % (os.path.join(files_path,"SARA_"+output+".pdb"))
			print >> sys.stderr, "%d comparisons left\n" % (possible_comparisons-n) 
			n+=1
	print  "Time to complete pairwise comparisons: %f seconds." % (time.time() - time_filtering)

	return comparisons
	
