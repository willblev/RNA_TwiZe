from file_finder import find_a_file

def is_module_installed(mod_name, should_exit=False):
	try: 
		__import__(mod_name)
		print "Python module %s is already installed, huzzah!"% mod_name
	except ImportError: 
		print "Darn it! Python was unable to import the module '%s'; please make sure it is installed correctly." % mod_name
		if should_exit:
			exit(0)
	

user_response=raw_input('Is X3DNA v2.1 installed on your computer? (y/n)')
if (user_response.upper()=='Y' or user_response.upper()=='YES' or user_response==''):
	print "Setup will now attempt to find where X3DNA is installed."
	print "Woo hoo! Found X3DNA file '%s' in %s" % ('find_pair',find_a_file("find_pair"))
else:
	print 'Please download and install X3DNA (http://rutchem.rutgers.edu/~xiangjun/3DNA/) as well as the optional file "x3dna-dssr".'
	exit(0)	

user_response=raw_input("\nIs SARA v1.0.7 installed on this computer? (y/n)")
if (user_response.upper()=='Y' or user_response.upper()=='YES' or user_response==''):
	print "Setup will now attempt to find where SARA is installed."
	print "Awesome! Found SARA file '%s' in %s" % ('runsara.py',find_a_file("runsara.py"))
else:
	print 'Please install SARA (http://structure.biofold.org/sara/download.html)'
	exit(0)

print "\n\nChecking for required Python modules....\n"
is_module_installed("Bio")
is_module_installed("Tkinter")
is_module_installed("tkFileDialog")
is_module_installed("tkMessageBox")
is_module_installed("Tkinter")
is_module_installed("math")
is_module_installed("urllib")
is_module_installed("time")
is_module_installed("pylab")
is_module_installed("numpy")

print "\n\nCongratulations! You can now use RNA_TwiZe!\n\n"
exit(0)
	
	
