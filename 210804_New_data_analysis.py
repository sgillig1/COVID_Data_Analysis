import pandas as pd 
import numpy as np 
import os

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 3})
line_width = 0.3
high_stream = 12
pad_label = 0.7;
tick_label = 0.7;

# Import the new data sheet. Also add the sample # as an index
new_data = pd.read_excel("/Users/ShaneGS/Desktop/210701_Data_Analysis/ForShane.xlsx", 2, header=0, skiprows=[1]) 

# File names of all of the folders for each device
file_names = {"2021.06.26#1": "06.26.21#1", "2021.06.26#2": "2016.06.26 #2", 
"2021.06.26#3": "2021.06.26 #3", "2021.06.26#4": "2021.06.26 #4",
"2021.06.26#5": "2021.06.26 #5", "UW2": "UW#2",
"UW8": "UW#8", "UW9": "UW#9",
"UW10": "UW#10"}

# Old data folder
new_data_folder = "/Users/ShaneGS/Desktop/210701_Data_Analysis/210701_New_Data"

# Sort the LEA samples
new_data[:29] = new_data.loc[:28].sort_values('Sample')
print(new_data)


plot_i = 1 # Iterator for the figure page
plot_j = plot_i + 1
fig = 1 # Iterator for naming output files

print(new_data.columns)
print(new_data.iloc[0].values)

for index, row in new_data.iterrows(): # Iterate through the row of the data frame, returning each row as row
	# Fill up a page of 4 x 4 graphs
	if plot_i >= 16:
		plot_i = 1
		plot_j = plot_i + 1
		plt.subplots_adjust(left=0.1, # Adjust the figure layout
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
		plt.savefig('Figure'+ str(fig), dpi = 1000,  bbox_inches='tight') # When the figure is full then save and make the next
		plt.close()
		fig = fig + 1


	device = row["Phone"]
	rep1_well = int(row["Well position Rep1"])
	rep1_run = int(row["Run1#"])
	rep2_well = int(row["Well position Rep2"])
	rep2_run = int(row["Run2#"])

	well_IAC1 = "Well" + str(rep1_well) + "Green" # Based on the well name find the well ID for the sample and IAC
	well_Sample1 = "Well" + str(rep1_well) + "Red"
	well_IAC2 = "Well" + str(rep2_well) + "Green" # Based on the well name find the well ID for the sample and IAC
	well_Sample2 = "Well" + str(rep2_well) + "Red"

	sample = str(row["Cohort"]) + str(row["Sample"])
	sample_num = str(row["Sample"])

	if sample == 'xprizeA1':
		plt.subplots_adjust(left=0.1, # Adjust the figure layout
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
		plt.savefig('Figure'+ str(fig), dpi = 1000) # When the figure is full then save and make the next
		plt.close()
		fig = fig + 1
		plot_i = 1
		plot_j = plot_i + 1

	software_call1 = row["Replicate 1"]
	software_call2 = row["Replicate 2"]

	sample_time1 = row["Unnamed: 19"]
	IAC_time1 = row["Unnamed: 20"]
	sample_time2 = row["Unnamed: 23"]
	IAC_time2 = row["Unnamed: 24"]

	if sample in ['Lea17']:
		IAC_time2 = "nan"

	cohort = row["Cohort"]

	xprize_ct = row["Ct N1 (copy)"]
	xprize_sample = row["Ct N2 (copy)"]

	print(sample_time1, IAC_time1, sample_time2, IAC_time2)

	rep1_file_name = ''
	rep2_file_name = ''

	device_folder = file_names[device]
	directory_device = new_data_folder + "/" + device_folder

	for i in range(1, high_stream):
		try:
			summary_file = "testrun" + str(rep1_run) + "_stream" + str(i) + "_raw_summary.txt"
			summary_dir = directory_device + '/' + summary_file
			pd.read_csv(summary_dir) # Import the CSV table
			rep1_file_name = "testrun" + str(rep1_run) + "_stream" + str(i) + "_temp_corrected.txt"
			break
		except:
			print(summary_file)

	for j in range(1, high_stream):
		try:
			summary_file = "testrun" + str(rep2_run) + "_stream" + str(j) + "_raw_summary.txt"
			summary_dir = directory_device + '/' + summary_file
			pd.read_csv(summary_dir) # Import the CSV table
			rep2_file_name = "testrun" + str(rep2_run) + "_stream" + str(j) + "_temp_corrected.txt"
			break
		except:
			print(summary_file)
	
	error_run = ''
	try:
		summary_file = "testrun" + str(rep2_run) + "_stream" + "1" + "_raw.txt"
		summary_dir = directory_device + '/' + summary_file
		pd.read_csv(summary_dir) # Import the CSV table
	except:	
		print("No Run")	
		error_run = "error"

	if sample == "Lea73":
		rep1_file_name = "testrun24_stream1_temp_corrected.txt"
		rep2_file_name = "testrun24_stream1_temp_corrected.txt"

	if sample == "xprizeE6":
		rep1_file_name = "testrun9_stream1_temp_corrected_NEW.txt"
		rep2_file_name = "testrun9_stream1_temp_corrected_NEW.txt"

	# if sample in ['xprizeF1', 'xprizeF3']:
	# 	rep1_file_name = "testrun5_stream1_raw.txt"
	# 	rep2_file_name = "testrun5_stream1_raw.txt"

	directory1 = directory_device + '/' + rep1_file_name
	directory2 = directory_device + '/' + rep2_file_name

	print(rep1_file_name, directory1)
	print(rep2_file_name, directory2)

	title1 = ''
	title2 = ''
	if software_call1[0:3] == 'pos':
		software_call1 = "POSITIVE"
	if software_call1[0:3] == 'neg':
		software_call1 = "NEGATIVE"
	if software_call2[0:3] == 'pos':
		software_call2 = "POSITIVE"
	if software_call2[0:3] == 'neg':
		software_call2 = "NEGATIVE"


	if cohort == "Lea":
		title1 = 'Sample ' + sample_num + " (1): " + software_call1
		title2 = 'Sample ' + sample_num + " (2): " + software_call2
	if cohort == "xprize":
		title1 = str(int(xprize_ct)) + ' copies in ' + xprize_sample + ' (1): ' + software_call1
		title2 = str(int(xprize_ct)) + ' copies in ' + xprize_sample + ' (2): ' + software_call2

	try:
		inter_df1 = pd.read_csv(directory1, header=0, delimiter = "\t") # Import the CSV table
		inter_df2 = pd.read_csv(directory2, header=0, delimiter = "\t") # Import the CSV table

		min_index1 = inter_df1[well_Sample1].idxmin()
		min_index2 = inter_df1[well_Sample2].idxmin()
		inter_df1 = inter_df1[min_index1:]
		inter_df2 = inter_df2[min_index2:]

		print(sample)
		if sample in ['xprizeC11']:
			initial_check = 30
			final_check = 1000

			dip_check = inter_df1[inter_df1["Seconds"] > inter_df1["Seconds"].iloc[0]+initial_check]	
			min_index_check = dip_check[well_Sample1].idxmin()
			print(inter_df1["Seconds"].iloc[min_index_check])
			print(inter_df1["Seconds"].iloc[0]+final_check)

			if inter_df1["Seconds"].iloc[min_index_check] < inter_df1["Seconds"].iloc[0]+final_check:
				inter_df1 = inter_df1[min_index_check:]
		if sample in ['xprizeE10', 'xprizeD11']:
			initial_check = 30
			final_check = 1000

			dip_check = inter_df1[inter_df2["Seconds"] > inter_df2["Seconds"].iloc[0]+initial_check]	
			min_index_check = dip_check[well_Sample2].idxmin()
			print(inter_df2["Seconds"].iloc[min_index_check])
			print(inter_df2["Seconds"].iloc[0]+final_check)

			if inter_df2["Seconds"].iloc[min_index_check] < inter_df2["Seconds"].iloc[0]+final_check:
				inter_df2 = inter_df2[min_index_check:]


		time1 = inter_df1["Seconds"].div(60)
		time2 = inter_df2["Seconds"].div(60)
		elapsed_time1 = time1.apply(lambda row: row - time1.iloc[0]) # Calculate the elapsed time in the run
		elapsed_time2 = time2.apply(lambda row: row - time2.iloc[0]) # Calculate the elapsed time in the run
		# Extract the Sample and IAC data
		Sample1 = inter_df1[well_Sample1]
		IAC1 = inter_df1[well_IAC1]
		Sample2 = inter_df2[well_Sample2]
		IAC2 = inter_df2[well_IAC2]

		if isinstance(sample_time1, float): sample_time1 = round(sample_time1, 1)
		if isinstance(IAC_time1, float): IAC_time1 = round(IAC_time1, 1)
		if isinstance(sample_time2, float):sample_time2 = round(sample_time2, 1)
		if isinstance(IAC_time2, float): IAC_time2 = round(IAC_time2, 1)

		# Plot the data
		plt.subplot(4,4,plot_i)
		plt.plot(elapsed_time1,Sample1, linewidth=line_width, color = '#2E3191', alpha = 0.7)
		plt.plot(elapsed_time1, IAC1, linewidth=line_width, color = '#00A651', alpha = 0.7)
		plt.title(title1, pad = -1, fontsize=4, fontweight='bold')
		plt.xlabel('Time (min)', labelpad=pad_label, fontsize=4)
		plt.ylabel('Signal (a.u.)', labelpad=pad_label, fontsize=4)
		table = plt.table(cellText=[[sample_time1], [IAC_time1]], bbox = [0.07, 0.77, 0.12, 0.17], zorder=2.5)
		table.get_celld()[(0,0)].get_text().set_color(color = '#00A651')
		table.get_celld()[(1,0)].get_text().set_color(color = '#2E3191')
		ax = plt.gca()
		ax.tick_params(axis='x', pad=tick_label)
		ax.tick_params(axis='y', pad=tick_label)
		print(plot_i, plot_j)
		plt.subplot(4,4,plot_j)
		plt.plot(elapsed_time2,Sample2, linewidth=line_width, color = '#2E3191', alpha = 0.7)
		plt.plot(elapsed_time2, IAC2, linewidth=line_width, color = '#00A651', alpha = 0.7)
		plt.title(title2, pad = -1, fontsize=4, fontweight='bold')
		plt.xlabel('Time (min)', labelpad=pad_label, fontsize=4)
		plt.ylabel('Signal (a.u.)', labelpad=pad_label, fontsize=4)
		table = plt.table(cellText=[[sample_time2], [IAC_time2]], bbox = [0.07, 0.77, 0.12, 0.17], zorder=2.5)
		table.get_celld()[(0,0)].get_text().set_color(color = '#00A651')
		table.get_celld()[(1,0)].get_text().set_color(color = '#2E3191')
		ax = plt.gca()
		ax.tick_params(axis='x', pad=tick_label)
		ax.tick_params(axis='y', pad=tick_label)

	except Exception as e:
		print(e)
		if rep1_file_name == '' and rep2_file_name == '' and error_run == '':
			plt.subplot(4,4,plot_i) # If error then plot an empty plot (for now)
			plt.plot()
			plt.title("Error No Summary" + sample, pad = -1)
			plt.subplot(4,4,plot_j) # If error then plot an empty plot (for now)
			plt.plot()
			plt.title("Error No Summary" + sample, pad = -1)
		elif rep1_file_name == '' and rep2_file_name == '' and error_run == 'error':
			plt.subplot(4,4,plot_i) # If error then plot an empty plot (for now)
			plt.plot()
			plt.title("Error No Run" + sample, pad = -1)
			plt.subplot(4,4,plot_j) # If error then plot an empty plot (for now)
			plt.plot()
			plt.title("Error No Run" + sample, pad = -1)
		else:
			print("No file found")
			print(sample)
			plt.subplot(4,4,plot_i) # If error then plot an empty plot (for now)
			plt.plot()
			plt.title("Error " + sample, pad = -1)
			plt.subplot(4,4,plot_j) # If error then plot an empty plot (for now)
			plt.plot()
			plt.title("Error " + sample, pad = -1)
			#plt.savefig('myfig'+ sample)
			#plt.close()

	plot_i = plot_i+2
	plot_j = plot_i +1