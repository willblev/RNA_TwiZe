=============
**RNA_TwiZe**
=============
-RNA Twilight-Zone Curve Maker-

RNA_TwiZe is a program that allows you to analyze the relationship between sequence and structure of RNA molecules. First, you provide the program with PDB files or a list of PDB IDs, and the program then runs the analysis and outputs a Twilight-Zone curve plot. 

**Installation**
================

To use RNA_TwiZe, first check to make sure your system passes all the requirements. This can be done quickly and easily by running the script 'check_requirements.py' and following the prompts::
    
    user@host:~/RNA_TwiZe/rna_twize$ python check_requirements.py

If you wish to install the RNA_TwiZe package to your computer so that you can execute it from any directory, you must run::

    user@host:~/RNA_TwiZe$ sudo python setup.py install

This will install the package so that it will be directly accessible from the Python interpreter. To open the graphical interface of RNA_TwiZe::

    user@host:~/$ python
    >>> from rna_twize import rna_twize



*Requirements*
--------------

*-To use RNA_TwiZe, please download and install the following programs in this order:*
1. Python 2.7

2. Python modules: scipy (numpy and pylab), Bio  
 
3. X3DNA v2.1   (and x3dna-dssr add-on)  	http://x3dna.org/

4. SARA v1.0.7   (and  out3dna.py)	 	http://structure.biofold.org/sara/download.html

RNA_TwiZe can be then be run by entering the following command in terminal (make sure you are in the directory rna_twize)::
    
    user@host:~/rna_twize$ python rna_twize.py

This will open a new window (Tkinter-powered GUI).
 
**Introduction**
================

One challenge that scientists in many fields must contend with is the task of finding homologs for a given sequence. Over the last few decades, scientists have thoroughly studied the relationship in proteins between sequence, secondary structure, 3D structure, as well as function. Two homologous proteins with  similar functions generally have similar 3D structures, and are also expected to show  sequence similarity, albeit to a lesser degree. Conversely, sequence similarity should imply structural similarity as well. As functional and structural comparison between proteins is difficult and time consuming, a simpler approach when searching for homologs is to just compare the sequences. This method is not as reliable as comparing tertiary structures, but it is orders of magnitude faster, and can be applied to proteins of which the 3D structure is not known. However, one must take into account the relationship between structure conservation and sequence conservation. This relationship can be displayed as a plot of many different proteins, comparing the percent similarity of an alignment between two sequences and the length of the alignment; highly-similar sequences are more likely to be structural homologs, and this plot will show us the 'general rule' to decide if a sequence comparison is sufficient to deem two proteins homologous. Some sequences are very similar, and are probably homologs, others are very dissimilar and probably not related, but in-between there is a 'Twilight-Zone' of sequence similarity; a range in which homology is not as certain. 

As our understanding of biological systems has grown, we have become increasingly interested in non-coding regions of DNA that were previously referred to as 'junk'. We used to regard some of the intermediate steps of translation and other processes as nothing more than 'half-finished molecules', but we are now finding that sometimes they have their own purpose. The investigation of different types of RNA molecule interactions is rapidly-growing field of study. Just as with proteins,  understanding the relationship between sequence, structure, and function of RNA is very useful. As RNA  molecules are completely different to proteins in many aspects, the 'general rule' for comparing RNA sequences to determine homology must be redefined. Knowing where the Twilight-Zone for RNA starts and ends can be very useful for future research.

Our objective was to create a program to show the relationship between RNA sequence conservation and structural conservation, using any set of RNA structures. The user can select which structures they wish to use, and get a plot as output. 


**Usage**
=========
Once you have opened the program (by opening terminal and running)::

    user@host:~/rna_twize$ python rna_twize.py

You must select which PDB files you would like to include in your analysis.

*Opening PDBs*
--------------
If you have the desired PDB files saved on your disk, please see option 1; If you need to download the PDB files but have a list of PDB IDs, see option 2.

1. In the top left corner, click "File" > "Open PDB Files". This will open a file browser that allows you to navigate to the directory in which you have saved your PDB files. To select multiple files, hold down SHIFT or CONTROL while clicking the files. Once you have selected all the files you wish to open, click "Open". **At the moment, you can only select from files that exist in the same directory; you cannot open files from different directories at the same time.**

2. A PDB ID consists of four alpha-numeric characters (e.g. "7WV2"). Make sure your list is in one of the following formats: PDB IDs separated by whitespace, PDB IDs separated by newline characters, PDB IDs separated by tabs, PDB IDs separated by commas, or PDB IDs separated by semicolons. It does not matter if your list is uppercase or lowercase, or if the IDs contain the chains as well (e.g. "7wv2:A"). Click "File" > "Open List of PDBs", and select your list. The program will then prompt you asking if you wish to download the PDB files; they will be stored in a new directory that is named after the filename of your list. For example, if your list file was called 'desired_pdbs.txt', RNA_TwiZe will create a new directory called 'desired_pdbs.txt_pdb_files' and save the downloaded PDB files there. **A PDB file can take up to a few seconds to download per file; the dialog box will disappear once the download process has completed.**

*Running The Analysis*
----------------------
Now that you have selected your PDBs, you can begin to run the analysis. Click "File" > "Run Analysis" to begin. When the analysis has completed, the dialog box will dissappear. **Analysis times can vary greatly depending on the number of RNA structures being used.**

*Making The Twilight-Zone Curve*
--------------------------------
Click "File" > "Make Plot" to plot your data.

*Saving The Twilight-Zone Curve*
--------------------------------
After you have made your plot, a new window will appear. In the bottom toolbar, there is a blue floppy disk icon that allows you to save a .png image file of your plot. **You also have some basic tools to adjust the dimensions and zoom of the plot.**


**Example**
===========

Once everything is properly installed, you can try RNA_TwiZe with this example::

    user@host:~/rna_twize_test$ python rna_twize_test.py example.txt_pdb_files

This example automatically uses a set of 7 pre-selected PDB files, and outputs some intermediate files and a plot image. If you prefer to follow along with the example in the GUI, you can open the files in RNA_TwiZe; they are in the directory '~/RNA_TwiZe/rna_twize/rna_twize_test/example.txt_pdb_files'. Then run the analysis, and you should see that your plot matches the .png image file '~/RNA_TwiZe/rna_twize/rna_twize_test/example_plot.png'.


**Acknowledgements**
====================

We would like to thank the creators of SARA and authors of the following paper:

"Quantifying the relationship between sequence and three-dimensional structure conservation in RNA",  Emidio Capriotti and Marc A. Marti-Renom, 2009. http://www.biomedcentral.com/1471-2105/11/322

We would also like to acknowledge the following authors and articles, as they helped guide our decisions and figure out how to design our program:

"Twilight zone of protein sequence alignments", Burkhard Rost, 1999.

"Tertiary Motifs in RNA Structure and Folding", Robert T. Batey, Robert P. Rambo, and Jennifer A. Doudna, 1999.

"A structural explanation for the twilight zone of protein sequence homology", Su Yun Chung and S. Subbiah, 1996.

Finally, we want to thank our Python teacher Javier Garcia Garcia for his templates and help, as well as our other teacher Baldo Oliva for answering all of our questions.


**Epilogue**
============

There are many ideas that we decided not to implement in order to keep the interface simple and intuitive. As a consequence, the program is not as customizable as it may be. In future versions, we can implement an 'Advanced Options' menu in which the user can change the default filters and cut-offs for minimum sequence length, minimum number of base pairs per alignment, etc. While there may be many ways to make the program itself more efficient, the bottleneck in terms of execution time is due to SARA. To optimize this process, it may be quicker to run several alignments in parallel instead of waiting for each alignment to finish before starting the next. There are many other ways to graphically represent the output of SARA, for example a plot between PID and PSS, or a plot between PSS and PSI. However, as the intent of our project was to make a Twilight-Zone curve, we commented out those plots in our code.

