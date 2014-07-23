def get_pdb_structure(pdb_id,path):
	"""Fetches the atomic 3D structure corresponding to a PDB ID (case insensitive) using the modules urllib and re; creates the PDB file in specified path if it doesn't exist."""
	import urllib
	import re
	import os.path
	import sys
	if not os.path.isfile(os.path.join(path,pdb_id+'.pdb')) and not os.path.isfile(os.path.join(path,pdb_id.lower()+'.pdb')):
		try:
			url_fd = urllib.urlopen("http://www.rcsb.org/pdb/files/%s.pdb" % (pdb_id))
			content = url_fd.read()
			url_fd.close()
			if "404 Not Found" in content:
				raise IOError("The PDB webpage could not be accessed. Check that your internet connection is working.")	
		except IOError:
			raise IOError("The PDB webpage could not be accessed. Check that your internet connection is working.")
			
		f = open(os.path.join(path,(pdb_id.upper()+'.pdb')),'w')
		f.write(content) 
		f.close() 
		print >> sys.stderr,  "Downloaded %s" % (pdb_id.upper())
		return os.path.join(path,pdb_id.upper()+'.pdb')
	else:
		if os.path.isfile(os.path.join(path,pdb_id+'.pdb')):
			print  >> sys.stderr, "File %s.pdb already exists!" % (pdb_id)
			return os.path.join(path,pdb_id+'.pdb')
		else:
			print  >> sys.stderr, "File %s.pdb already exists!" % (pdb_id.lower())
			return os.path.join(path,pdb_id.lower()+'.pdb')

	
