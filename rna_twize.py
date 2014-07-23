import Tkinter
import tkFileDialog
import tkMessageBox
from Tkinter import *
import os
import sys  
from math import factorial


class Unbuffered(object):
	"""Attempts to create an unbuffered STDOUT"""
	def __init__(self, stream):
		self.stream = stream
	def write(self, data):
		self.stream.write(data)
		self.stream.flush()
	def __getattr__(self, attr):
		return getattr(self.stream, attr)


sys.stdout = Unbuffered(sys.stdout)
files_list=[]
	
class RNA_Twilight_Zone_Curve(Tkinter.Frame):
	"""Tkinter GUI that lets a user select PDB files with RNA structures and creates a Twilight-Zone curve."""
	
	def open_pdb_files(self):
		"""Allows the user to select multiple PDB files from a Tkinter prompt"""
		if len(self.display_list)>0:
			answer = tkMessageBox.askokcancel(message = "Are you sure you want to load new PDB files? Current workspace will be lost.")
			if not answer:
				return
			else: 
				del files_list[:]
				print "####   Started a new project    ####"
		self.display_list=[]
		list_filename_paths = tkFileDialog.askopenfilenames(parent=root,title="Select multiple files (by holding SHIFT or CTRL).", filetypes=[("PDB files","*.pdb"),("All files","*")] )
		if len(list_filename_paths)==1:
			tkMessageBox.showerror("Too Few PDB Files!","You must select at least two PDB files.")
			return
		elif len(list_filename_paths)==0:
			return
		for each_file in list_filename_paths:
			filename=os.path.basename(each_file)[:-4]
			print >> sys.stderr, "Loaded %s"% filename   
			if each_file not in files_list:  # could use a set to avoid redundancies 
				files_list.append(each_file)
			if filename not in self.display_list:
				self.display_list.append(filename)
		#Sort the list by id
		self.display_list.sort(key=lambda x: x)
		#Add the identifiers to the workspace list
		self.pdb_id_listbox.delete(0, Tkinter.END)
		index = 1
		for record in self.display_list:
			self.pdb_id_listbox.insert(index, record.upper())	
			index+=1
		
		print "Loaded %d PDB files."%len(self.display_list)
		self.current_SeqRecord = None
		print  >> sys.stderr, "Locations of PDB files:"
		for fils_paths in files_list:
			print  >> sys.stderr, fils_paths


	def open_list_file(self):           #Opens a list file and gets each ID
		"""Opens a prompt that allows the user to select a text file containing a list of PDB IDs, which is then used to download the PDB files if the do not already exist."""
		if len(self.display_list)>0:
			answer = tkMessageBox.askokcancel(message = "Are you sure you want to load new PDB files? Current workspace will be lost.")
			if answer is False:
				return
			else: 
				del files_list[:]
				print "####   Started a new project    ####"
		self.display_list=[]
		list_filename_path = tkFileDialog.askopenfilename(	title="Select a list of PDB IDs.", filetypes=[("Text files","*.txt"),("Text files","*.tbl"),("Text files","*.tsv"),("Text files","*.csv"),("All files","*")] )
		if list_filename_path=="":
			return	
		
		self.display_list = []	
		just_path=os.path.dirname(list_filename_path)
		new_dir_name=os.path.join(just_path,os.path.basename(list_filename_path)+"_pdb_files")
		if not os.path.exists(new_dir_name):
			os.makedirs(os.path.join(just_path,os.path.basename(list_filename_path)+"_pdb_files"))
	
		#open list and parse PDB IDs
		handle = open(list_filename_path,"r")
		entire_file=''
		print >> sys.stderr, "Fetching PDB files..."
		for line in handle:
			entire_file+=line
		if "," in entire_file:
			pdb_id_list=[x.strip() for x in entire_file.split(',')]
		elif ";" in entire_file:
			pdb_id_list=[x.strip() for x in entire_file.split(';')]
		else:
			pdb_id_list=[x.strip() for x in entire_file.split()]
	
		for pdb_id in pdb_id_list:
			if pdb_id[:4].upper() not in self.display_list:
				self.display_list.append(pdb_id[:4].upper())
		self.display_list.sort(key=lambda x: x)
	
		#Add the identifiers to the list
		
		self.pdb_id_listbox.delete(0, Tkinter.END)
		index = 1
		answer = tkMessageBox.askokcancel(message = "Download %d PDB files? This will probably take between %0.2f and %0.2f minutes. This window will close when process has completed." % (len(self.display_list), len(self.display_list)*0.03,len(self.display_list)*0.07))
		if answer is False:
			return
		from pdb_getter import get_pdb_structure
		for record in self.display_list:
			self.pdb_id_listbox.insert(index, record.upper())
			files_list.append(get_pdb_structure(record,new_dir_name))
			index+=1
		handle.close()
		print "Loaded %d PDB files." % (len(self.display_list))
		self.current_SeqRecord = None
		print  >> sys.stderr, "Locations of PDB files:"
		 
		for fils in files_list:
			print  >> sys.stderr, fils
		print "You may now run an analysis with 'File' >> 'Run Analysis'."

	def open_previous_files(self):
		"""Allows the user to select files from previously running an analysis."""
		if len(self.display_list)>0:
			answer = tkMessageBox.askokcancel(message = "Are you sure you want to load new PDB files? Current workspace will be lost.")
			if answer is False:
				return
			else: 
				del files_list[:]
				print "####   Started a new project    ####"
		self.display_list=[]
		list_filename_paths = tkFileDialog.askopenfilenames(parent=root,title="Select multiple files (by holding SHIFT or CTRL).", filetypes=[("PDB files","SARA_*.pdb"),("All files","*")] )
		if len(list_filename_paths)==0:
			return
		for each_file in list_filename_paths:
			filename=os.path.basename(each_file)[5:-4]
			print >> sys.stderr, "Loaded %s"% filename   
			if each_file not in files_list:
				files_list.append(each_file)
			if filename not in self.display_list:
				self.display_list.append(filename)
		#Sort the list by id
		self.display_list.sort(key=lambda x: x)
		#Add the identifiers to the list
		self.pdb_id_listbox.delete(0, Tkinter.END)
		index = 1
		for record in self.display_list:
			self.pdb_id_listbox.insert(index, record.upper())	
			index+=1
		print "Loaded %d files from previous analysis." % len(files_list)


	def run_analysis(self):
		"""Using the previously selected PDB files, filters out RNA structures that are not identical and between 20 and 500 bases long. This filtered list is then compared with SARA"""
		if len(files_list)>0:
			runtime_approx=factorial(len(files_list))/(factorial(len(files_list)-2)*factorial(2))
			answer = tkMessageBox.askokcancel("Run Analysis","The analysis will probably take between %0.2f and %0.2f minutes to run these comparisons. Do you want to continue now? This window will close when process has completed." % (runtime_approx*0.04,runtime_approx*0.09))
			if answer is False:	
				return
		
			from pdb_comparer import compare_files
			refresh_listbox=compare_files(files_list)
			print "The analysis has created %d pairwise comparison files."% len(refresh_listbox)
			self.pdb_id_listbox.delete(0, Tkinter.END)
			index = 1
			for record in refresh_listbox:
				self.pdb_id_listbox.insert(index, record.upper())
				index+=1
			self.current_SeqRecord = None
			print "You may now plot your results with 'File' >> 'Make Plot'."
		else:
			tkMessageBox.showerror("No files loaded!","There are currently no files loaded. First you should select PDB files.")
	
	def make_plot(self):
		"""Uses the files created by the pairwise alignments to make a plot."""
		if len(files_list)>0:
			from make_twize_graph import make_twilight_zone_curve
			make_twilight_zone_curve(os.path.dirname(files_list[0]))
		else:
			tkMessageBox.showerror("No files loaded!","There are currently no files loaded. First import PDBs, then run then analysis before you try to plot.")

			
	def show_help(self):
		"""Displays the help dialogue, and provides extra information by searching for and opening the README file."""
		answer=tkMessageBox.askokcancel(title="Help", message="Welcome to RNA_Twize. The basic flow of the program is as follows: \n     1. Open several PDB files\n     2. Run the analysis\n     3. Plot your results\n     4. Save your plot \nFor more detailed information, please see the README.txt file included with this package.\n\n Open README.txt now?")
		if answer:
			where_are_we = os.path.dirname(os.path.realpath(__file__))
			try:
				open_help_string="gedit %s &" % (os.path.join(os.path.dirname(where_are_we),"README.txt"))
				os.system(open_help_string)
			except:
				open_help_string="more %s " % (os.path.join(os.path.dirname(where_are_we),"README.txt"))
				os.system(open_help_string)

	def show_about(self):
		"""Displays a short message from the creators of the program"""
		tkMessageBox.showinfo(title="About", message="This program was written by Andres Lanzos Camionai and Will Blevins in 2014. We would like to thank Emidio Capriotti for creating SARA, and Javier Garcia Garcia for providing us with useful templates for our Tkinter GUI.")


	def create_left_frame(self):
		self.left_frame = Tkinter.LabelFrame(self, text="Workspace List", padx=5, pady=5)
		self.create_pdb_id_listbox()
		self.left_frame.grid(row=0, column=0, sticky=Tkinter.W+Tkinter.E+Tkinter.N+Tkinter.S)	

	def create_pdb_id_listbox(self):
		"""Creates a frame that contains a listbox with a scroll bar"""
		frame = Tkinter.Frame(self.left_frame)
		scrollbar = Tkinter.Scrollbar(frame, orient=Tkinter.VERTICAL)
		self.pdb_id_listbox = Tkinter.Listbox(frame, selectmode=Tkinter.SINGLE, height=20, yscrollcommand = scrollbar.set)
		scrollbar.config(command=self.pdb_id_listbox.yview)
		scrollbar.pack( side=Tkinter.RIGHT, fill=Tkinter.Y)
		self.pdb_id_listbox.pack( side=Tkinter.LEFT, expand=True, fill=Tkinter.BOTH)
		frame.pack( fill=Tkinter.BOTH )

	def create_right_frame(self):
		"""Makes a tkinter frame"""
		self.text_frame = Tkinter.LabelFrame(self, text="Program Feedback", width=400, padx=5, pady=5)		
		self.text_frame.grid(row=0, column=2, sticky=Tkinter.W)		
		self.right_frame = Tkinter.Frame(self.text_frame, borderwidth=5)
		self.right_frame.grid()
		
	def create_feedback_label(self):
		"""A label that scrapes STDOUT and prints it in a feedback window"""	
		class IORedirector(object):
			def __init__(self,TEXT_INFO):
				self.TEXT_INFO = TEXT_INFO
		class StdoutRedirector(IORedirector):
			def write(self,str):
				self.TEXT_INFO.config(text=self.TEXT_INFO.cget('text') + str)
				
		self.TEXT_INFO = Label(self.right_frame, height=20, width=70, bg="grey",borderwidth=5, relief=RIDGE)
		self.TEXT_INFO.grid(row=1, column=1)
		sys.stdout = StdoutRedirector(self.TEXT_INFO)
		

	def quit(self):
		if tkMessageBox.askyesno("Quit","Are you sure you want to exit?"):
			Tkinter.Frame.quit(self)
			exit(0)

	#CREATE THE FILEMENU	
	def create_menu(self):
		self.menubar = Tkinter.Menu(self)
		filemenu = Tkinter.Menu(self.menubar)
		filemenu.add_command(label="Open PDB Files", command=self.open_pdb_files)
		filemenu.add_command(label="Open List Of PDBs", command=self.open_list_file)
		filemenu.add_command(label="Open Previous Analysis", command=self.open_previous_files)
		filemenu.add_separator()
		filemenu.add_command(label="Run Analysis", command=self.run_analysis)
		filemenu.add_separator()
		filemenu.add_command(label="Make Plot", command=self.make_plot)
		filemenu.add_separator()
		filemenu.add_command(label="QUIT", command=self.quit)

	#CREATE THE HELP MENU
		helpmenu = Tkinter.Menu(self.menubar)
		helpmenu.add_command(label="Help", command=self.show_help)
		helpmenu.add_command(label="About", command=self.show_about)
		self.menubar.add_cascade(label="File", menu=filemenu)
		self.menubar.add_cascade(label="Help", menu=helpmenu)
		self.master.config(menu=self.menubar)	
		
		
		
	def createWidgets(self):
		self.create_menu()
		self.create_left_frame()
		self.create_right_frame()
		self.create_feedback_label()
		self.grid(row=0)

	def __init__(self, master=None, **kwargs):
		Tkinter.Frame.__init__(self, master, **kwargs)
		self.master.wm_title("RNA TwiZe: Twilight-Zone Curve Maker")
		self.master.resizable(width=False, height=False)


        #DEFINE ATTRIBUTES
		self.display_list = []
		self.pdb_id_listbox = None
		self.menubar = None
		self.current_SeqRecord = None
		self.sequence_text = None
		self.createWidgets()





"""Makes the GUI pop up in the middle of the screen"""	
root = Tkinter.Tk()
app = RNA_Twilight_Zone_Curve(master=root,padx=10, pady=10)
#make screen dimensions work
w = 800 
h = 380 
# get screen width and height
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
# calculate position x, y
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
print "Welcome to RNA_TwiZe. Open files using the toolbar menu to begin."
app.mainloop()
