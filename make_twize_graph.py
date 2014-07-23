from pylab import *
def make_twilight_zone_curve(files_path):
	"""Takes all the files created from the pairwise comparisons with SARA and creates a plot"""
	import time, os, sys
	start_time = time.time()
	files_list=[]
	
	for fname in os.listdir(files_path):   ##puts all the comparison files into the list files_list
		if fname.startswith("SARA_"):
			files_list.append(fname)

	print >> sys.stderr, "Beginning filtering of alignments..."
	related=[]
	non_related=[]
	print  >> sys.stderr, "%d total alignments found."% len(files_list)
	summary={}
	NR_set_list=[]
	n=0
	for filename in files_list:
		file=open(os.path.join(files_path,filename),"r")     #open each comparison file to check criteria
		chain1=filename[:6]
		chain2=filename[7:13]
		IDS="None"
		SNORM="None"
		NSS="None"
		RMS="None"
		PID="None"
		PSS="None"
		PSI="None"
		LPID="None"
		LPSS="None"
		LPSI="None"
		TYPE="None"
		m=0
		for line in file:
			line=line.rstrip()
			
			if "SecStructure: False" in line:
				break		
			if "REMARK SARANALI " in line:
				IDS=float(line[18:]) # Identities in the sequence alignment
				m+=1
			if "REMARK SARANORM " in line:
				SNORM=float(line[18:]) # Length of the shortest sequence chain
				m+=1
			if "REMARK SARANSS " in line:
				NSS=float(line[18:]) # Lower number of base pairs between chain1 and chain2
				m+=1
			if "REMARK SARARMS " in line:
				RMS=float(line[18:])
				m+=1
			if "REMARK SARASID " in line:
				PID=float(line[18:]) # Percentage of sequence identity in the 3D alignment
				m+=1
			if "REMARK SARAPSS " in line:
				PSS=float(line[18:]) # Percentage of secondary structure identity in the 3D alignment
				m+=1
			if "REMARK SARAPSI " in line:
				PSI=float(line[18:]) # Percentage structural identitiy
				m+=1
			if "REMARK SARALNSID " in line:
				LPID=float(line[18:]) # Negative logarithm of PSI p-value
				m+=1
			if "REMARK SARALNPSS " in line:
				LPSS=float(line[18:]) # Negative logarithm of PSS p-value
				m+=1
			if "REMARK SARALNPSI " in line:
				LPSI=float(line[18:]) # Negative logarithm of PSI p-value
				m+=1
			if m==10:
				break
		if m==10:
			summary[filename]={}
			summary[filename]["chain1"]={chain1}
			summary[filename]["chain2"]=chain2
			summary[filename]["IDS"]=IDS
			summary[filename]["SNORM"]=SNORM
			summary[filename]["SID"]=IDS/SNORM*100
			summary[filename]["NSS"]=NSS
			summary[filename]["RMS"]=RMS
			summary[filename]["PID"]=PID
			summary[filename]["PSS"]=PSS
			summary[filename]["PSI"]=PSI
			summary[filename]["LPID"]=LPID
			summary[filename]["LPSS"]=LPSS
			summary[filename]["LPSI"]=LPSI
			summary[filename]["SID"]=IDS/SNORM*100.0 # Percentage of sequence alignment (100*IDS/SNORM)
			if summary[filename]["SID"] <= 25.0:
				NR_set_list.append(filename)
	

	print  >> sys.stderr, "Found %d structural alignments useful."% len(summary)

	print  >> sys.stderr, "Classifying the alignments and plotting the results..."

	LPSS_threshold=4
	LPID_threshold=4
	LPSI_threshold=4
	
	HA_set_list=[]
	number_related=0
	number_medium_accuracy=0
	number_non_related=0


	TN_SID_list=[]
	TN_Length_list=[]
	TP_SID_list=[]
	TP_Length_list=[]
	MA_SID_list=[]
	MA_Length_list=[]
	TP_PSI_list=[]
	TP_PID_list=[]
	TP_RMS_list=[]
	TP_PSS_list=[]
	all_length_list=[]
	for alignment in summary:
		all_length_list.append(summary[alignment]["SNORM"])
		if summary[alignment]["LPSS"] >= LPSS_threshold and summary[alignment]["LPID"] >= LPID_threshold and summary[alignment]["LPSI"] >= LPSI_threshold:
			HA_set_list.append(alignment)
			summary[alignment]["TYPE"] = "True positive"
			number_related+=1
			TP_SID_list.append(summary[alignment]["SID"])
			TP_Length_list.append(summary[alignment]["SNORM"])
			TP_PSI_list.append(summary[alignment]["PSI"])
			TP_PID_list.append(summary[alignment]["PID"])
			TP_PSS_list.append(summary[alignment]["PSS"])
			TP_RMS_list.append(summary[alignment]["RMS"])
		elif summary[alignment]["LPSS"] < LPSS_threshold and summary[alignment]["LPID"] < LPID_threshold and summary[alignment]["LPSI"] < LPSI_threshold:
			summary[alignment]["TYPE"] = "True negative"
			number_non_related+=1
			TN_SID_list.append(summary[alignment]["SID"])
			TN_Length_list.append(summary[alignment]["SNORM"])
		else:
			summary[alignment]["TYPE"] = "Medium accuracy"
			number_medium_accuracy+=1
			MA_SID_list.append(summary[alignment]["SID"])
			MA_Length_list.append(summary[alignment]["SNORM"])

	print "Time taken to classify alignments : %0.2f seconds." % (time.time() - start_time)
	print >> sys.stderr, "True positives: %d \t True negatives: %d \t Medium Accuracy: %d" % (number_related, number_non_related,number_medium_accuracy)
	
	
	#printing the curve
	max_length=max(all_length_list)
	curve_x_list=range(1,int(max_length))
	curve_y_list=[]
	
	for x in curve_x_list:
		y=480.0*x**(-0.32*(1+2.71828**(-x/(10**len(str(max_length))))))
		curve_y_list.append(y)
		
	
	TN_as_N=0.0
	TN_as_P=0.0
	for i in range(len(TN_Length_list)):
		x=TN_Length_list[i]
		x=int(x)
		y_threshold=480.0*x**(-0.32*(1+2.71828**(-x/(10**len(str(max_length))))))
		if TN_SID_list[i]>y_threshold: TN_as_P+=1
		else: TN_as_N+=1
	if TN_as_N+TN_as_P>0:
		print "True negative alignments classified as Negative:%d\t%0.2f" %(TN_as_N,TN_as_N/(TN_as_N+TN_as_P)*100)+"%"
		print "True negative alignments classified as Positive:%d\t%0.2f" %(TN_as_P,TN_as_P/(TN_as_N+TN_as_P)*100)+"%"
	
	TP_as_N=0.0
	TP_as_P=0.0
	for i in range(len(TP_Length_list)):
		x=TP_Length_list[i]
		x=int(x)
		y_threshold=480.0*x**(-0.32*(1+2.71828**(-x/(10**len(str(max_length))))))
		if TP_SID_list[i]>=y_threshold: TP_as_P+=1
		else: TP_as_N+=1
	if TP_as_N+TP_as_P>0:
		print "True positive alignments classified as Negative:%d\t%0.2f" %(TP_as_N,TP_as_N/(TP_as_N+TP_as_P)*100)+"%"
		print "True positive alignments classified as Positive:%d\t%0.2f" %(TP_as_P,TP_as_P/(TP_as_N+TP_as_P)*100)+"%"
	
	MA_as_N=0.0
	MA_as_P=0.0
	for i in range(len(MA_Length_list)):
		x=MA_Length_list[i]
		x=int(x)
		y_threshold=480.0*x**(-0.32*(1+2.71828**(-x/(10**len(str(max_length))))))
		if MA_SID_list[i]>=y_threshold: MA_as_P+=1
		else: MA_as_N+=1
	if MA_as_N+MA_as_P>0:
		print "Medium accuracy alignments classified as Negative:%d\t%0.2f" %(MA_as_N,MA_as_N/(MA_as_N+MA_as_P)*100.0)+"%"
		print "Medium accuracy alignments classified as Positive:%d\t%0.2f" %(MA_as_P,MA_as_P/(MA_as_N+MA_as_P)*100.0)+"%"
	
	
	plot(curve_x_list,curve_y_list)
	plot(TN_Length_list, TN_SID_list,'^',label="True Negative")
	plot(TP_Length_list, TP_SID_list,'o',label="True Positive")
	plot(MA_Length_list, MA_SID_list,'*',label="Medium accuracy")
	ylim([0,100])
	legend(loc="upper right", bbox_to_anchor=(1,1),numpoints=1,prop={'size':7})
	xlabel('Length of alignment')
	ylabel('% sequence identity')
	title('RNA Twilight-Zone Curve')
	show()
	
	print "Plot generated."
	
	#### There are other ways of representing the data, but we wanted a more simple interface and not too many options. Some other plots follow:#####
	
	
	#plot(TP_PID_list, TP_PSI_list,'o')
	#legend(loc='right')
	#xlabel('PID')
	#ylabel('PSI')
	#show()
	
	#plot(TP_PID_list, TP_RMS_list,'o')
	#legend(loc='right')
	#xlabel('PID')
	#ylabel('RMS')
	#show()

	#plot(TP_PSS_list, TP_PSI_list,'o')
	#legend(loc='right')
	#xlabel('PSS')
	#ylabel('PSI')
	#show()

	#plot(TP_PID_list, TP_PSS_list,'o')
	#legend(loc='right')
	#xlabel('PID')
	#ylabel('PSS')
	#show()
