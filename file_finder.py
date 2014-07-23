def find_a_file(query_file_name):
	"""Searches for a file such as rna_twize.py by walking through the systems directories, and returns it's location"""
	import sys, os
	if os.path.exists(query_file_name+"_location"):
		print >> sys.stderr, "You already know where %s is!" % query_file_name
		with open(query_file_name+"_location","r") as here_it_is:
			for line in here_it_is:
				return line
	else:			
		print >> sys.stderr, "Searching for file %s...." % query_file_name
		for dpath, dnames, fnames in os.walk("/"):
			for i, fname in enumerate([os.path.join(dpath, fname) for fname in fnames]):
				if os.path.basename(fname)==query_file_name:
					with open(query_file_name+"_location","w") as saving_path:
						saving_path.write(os.path.join(os.path.dirname(fname),fname))
					return os.path.join(os.path.dirname(fname),fname)
				

		
