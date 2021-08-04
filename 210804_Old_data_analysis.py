import pandas as pd 
import numpy as np 
import os

import sys

import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 3, 'font.sans-serif': 'Arial'})
line_width = 0.3;
pad_label = 0.5;
tick_label = 0.5;

# Import the old data sheet (ignoring the first 2 rows). 
old_data = pd.read_excel("/Users/ShaneGS/Desktop/210701_Data_Analysis/ForShane.xlsx", 1, header=2) 

# File names of all of the folders for each device
file_names = {"UW1": "eab1b833-c242-42e6-8f95-f4d20e4f8df2-UW#1", "UW2": "2e865d8a-c627-4953-a3c3-7355190c02ee-UW#2", 
"UW3": "ed2e2d79-a3c7-48f7-ba1f-0fc84603751b-UW#3", "UW4": "d5ea9251-97ab-48f0-9bdd-17fb882a321d-UW#4",
"UW5": "39a83807-7b69-4520-96bf-2cff9b007c29-UW#5", "UW6": "f6449c8e-bfc3-481f-bf00-05ee411eaf0b-UW#6",
"UW7": "ef8139c7-629a-4ac2-92ab-746a4b9b512a-UW#7", "UW8": "76b3ec35-b05f-4765-a80b-a48ff7aa5db1-UW#8",
"UW9": "d4e94ac1-608d-4295-b3f4-b346700f226b-UW#9", "UW10": "0511745c-ad83-441a-abcc-2ab94a9fb150-UW#10",
"UW11": "5b106743-4c52-44f5-ae8c-b8e1be6157d0-UW#11"}

# Old data folder
old_data_folder = "/Users/ShaneGS/Desktop/210701_Data_Analysis/210701_Old_Data"


i = 0 # Iterator for the figure page
fig = 1 # Iterator for naming output files

for index, row in old_data.iterrows(): # Iterate through the row of the data frame, returning each row as row
	# Fill up a page of 4 x 4 graphs
	if i >= 16:
		i = 0
		plt.subplots_adjust(left=0.1, # Adjust the figure layout
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
		plt.savefig('Figure'+ str(fig), dpi = 1000, bbox_inches='tight') # When the figure is full then save and make the next
		plt.close()
		fig = fig + 1
	i = i+1
	
	# Extract the relevant data fields
	device = row["Device"]
	file_name = row["File name"]
	if file_name[0:9] == "Titration":
		i = i - 1 
		continue

	run = row["Run"]
	well = row["well"]
	sample = str(row["Sample #"])
	NP_ID = str(int(row["NP_ID"]))
	replicate = str(int(row["Rep"]))

	call = row["call"]

	sample_time = row["tTargetDetect"]
	IAC_time = row["tIacDetect"]


	well_IAC = "Well" + str(well) + "Green" # Based on the well name find the well ID for the sample and IAC
	well_Sample = "Well" + str(well) + "Red"

	# Match the Device name to the folder that the data is in. Find the directory of the device
	device_folder = file_names[device]

	## Add file names for the not needed files
	corrections = {"Not needed38":"testrun38_stream1_temp_corrected.txt", 
	"Not needed35":"testrun35_stream1_temp_corrected.txt"}

	if file_name == "Not needed":
		file_name = corrections[file_name+str(run)]
	directory = old_data_folder + "/" + device_folder + "/" + file_name

	print(device, file_name, well, device_folder)

	if (file_name == "I think this one should be both streams 1&2"): # This is for the case where we need both streams 1 and 2
		# Formulate the file names and directory for the 2 streams
		file_name1 = "testrun" + str(run) + "_stream1_temp_corrected.txt"
		file_name2 = "testrun" + str(run) + "_stream2_temp_corrected.txt"
		directory1 = old_data_folder + "/" + device_folder + "/" + file_name1
		directory2 = old_data_folder + "/" + device_folder + "/" + file_name2
		try:
			inter_df1 = pd.read_csv(directory1, header=0, delimiter = "\t") # Import the CSV table
			inter_df2 = pd.read_csv(directory2, header=0, delimiter = "\t")
			inter_df_concat = pd.concat([inter_df1, inter_df2]) # Concatenate the two streams
			min_index = inter_df_concat[well_Sample].idxmin()
			inter_df_concat = inter_df_concat[min_index:]

			time = inter_df_concat["Seconds"].div(60)
			elapsed_time = time.apply(lambda row: row - time.iloc[0]) # Calculate the elapsed time in the run
			# Extract the Sample and IAC data
			Sample = inter_df_concat[well_Sample]
			IAC = inter_df_concat[well_IAC]
			
			sample_time = round(sample_time/60, 1)
			IAC_time = round(IAC_time/60, 1)

			# Plot the data
			plt.subplot(4,4,i)
			plt.plot(elapsed_time,Sample, linewidth=line_width, color = '#2E3191', alpha = 0.7)
			plt.plot(elapsed_time, IAC, linewidth=line_width, color = '#00A651', alpha = 0.7)
			plt.title('Sample ' + NP_ID + " (" + replicate + ")" ": " + call, pad = -1, fontsize=4, fontweight='bold')
			plt.ylabel('Signal (a.u.)', labelpad=pad_label, fontsize=4)
			plt.xlabel('Time (min)', labelpad=pad_label, fontsize=4)
			table = plt.table(cellText=[[sample_time], [IAC_time]], bbox = [0.05, 0.78, 0.12, 0.17], zorder=2.5)
			table.get_celld()[(0,0)].get_text().set_color(color = '#00A651')
			table.get_celld()[(1,0)].get_text().set_color(color = '#2E3191')
			ax = plt.gca()
			ax.tick_params(axis='x', pad=tick_label)
			ax.tick_params(axis='y', pad=tick_label)
			#plt.xlim([0, 100])
			continue
		except:
			print("No file found -- 1&2")
			print(file_name, file_name1, file_name2)

	try:
		inter_df = pd.read_csv(directory, header=0, delimiter = "\t") # Import the CSV table
		
		min_index = inter_df[well_Sample].idxmin()
		print(min_index)

		if sample in ['17', '27', '37', '43', '48', '49', '61', '65', '66','67','68','81','96','108','109',
		'114','120','123','124','125','126','127','128','129','131','139','140','141','143','146','150','151',
		'152','153','158','159','160','163','167','168','173','174','175','186','187','189','190','191',
		'192','194','197','198','199','200','201','202','203','205','206','207','208','211','213']:
			#min_index = inter_df[well_Sample][:min_index-100].idxmin()
			min_index = inter_df[well_IAC].idxmin()
			print("SAMPLE")
			print(sample)
			print(min_index)

		if sample == '181':
			inter_df_inter = inter_df
		inter_df = inter_df[min_index:]

		initial_check = 300
		final_check = 2000

		print(sample)
		## Below is the correction for multiple initial spikes. The first correction deals with only the first spike.
		## If there are two then I manuallly am setting the distance until the next
		if sample == '19': 
			initial_check = 50

		if sample in ['45', '156', '162', '178']:
			initial_check = 15

		if sample in ['41']:
			initial_check = 30

		if sample in ['42', '44', '46', '153', '169']:
			initial_check = 100

		if sample in ['51', '52', '53', '54']:
			initial_check = 1000

		if sample in ['23', '24', '25', '26']:
			initial_check = 0

		if sample == '58':
			initial_check = 10

		if sample in ['65', '67', '158','160', '192', '200']: # Samples with small spike
			initial_check = 5

		if sample in ['194', '198']: # Samples with really small spike
			initial_check = 15

		if sample in ['127', '129', '151', '167']: # Samples with normal spike
			initial_check = 10

		### This is the low index check
		dip_check = inter_df[inter_df["Seconds"] > inter_df["Seconds"].iloc[0]+initial_check]	

		if sample == '58':
			dip_check = dip_check[:2000]

		## This will find the minimum index (The try is for file 181)
		try:
			min_index_check = dip_check[well_Sample].idxmin()
		except:
			min_index_check = 20

		if sample == '177': # this one was not able to configure for some reason
			min_index_check = 38



		if sample in ['47', '71', '72', '78','87', '88', '89', '90', '91', '92', '93','94', 
		'95', '113', '119', '135', '161', '179','181', '183']:
			min_index_check = 20

		if sample in ['43', '174']:
			inter_df = inter_df[5:]

		#print(inter_df["Seconds"].iloc[min_index_check])
		#print(inter_df["Seconds"].iloc[0]+final_check)
		#print(min_index_check)

		if sample not in ['17', '27', '37', '48', '49', '61','66','68','81','96','108','109',
		'114','120','123','124','125','126','128','131','139','140','141','143','146','150',
		'152','153','159','163','168','173','174','175','186','187','189','190','191',
		'197','199','201','202','203','205','206','207','208','211','213']:
			try:
				if inter_df["Seconds"].iloc[min_index_check] < inter_df["Seconds"].iloc[0]+final_check:
					inter_df = inter_df[min_index_check:]
			except:
				print("error")

		if sample == '181':
			inter_df = inter_df_inter[40:]

		# This will get rid of a large spike at the end
		if sample in ['99', '100', '121', '122', '44', '60', '62', '58', '78']:
			diff = 0.002
			last = 0
			current = 0
			row_big = 0
			#print(inter_df)
			for index1, row1 in inter_df.iterrows():
				#print(row1[well_Sample])
				gap = row1[well_Sample] - last
				last = row1[well_Sample]
				if gap > diff:
					big_gap = gap
					row_big = current
				current = current + 1
			max_index_check = row_big - 1
			inter_df = inter_df[:max_index_check]


		time = inter_df["Seconds"].div(60)
		elapsed_time = time.apply(lambda row: row - time.iloc[0]) # Calculate the elapsed time in the run
		# Extract the Sample and IAC data
		Sample = inter_df[well_Sample]
		IAC = inter_df[well_IAC]

		sample_time = round(sample_time/60, 1)
		IAC_time = round(IAC_time/60, 1)

		# Plot the data
		plt.subplot(4,4,i)
		plt.plot(elapsed_time,Sample, linewidth=line_width, color = '#2E3191', alpha = 0.7)
		plt.plot(elapsed_time, IAC, linewidth=line_width, color = '#00A651', alpha = 0.7)
		plt.title('Sample ' + NP_ID + " (" + replicate + ")" ": " + call, pad = -1, fontsize=4, fontweight='bold')
		plt.xlabel('Time (min)', labelpad=pad_label, fontsize=4)
		plt.ylabel('Signal (a.u.)', labelpad=pad_label, fontsize=4)
		table = plt.table(cellText=[[sample_time], [IAC_time]], bbox = [0.07, 0.77, 0.12, 0.17], zorder=2.5)
		table.get_celld()[(0,0)].get_text().set_color(color = '#00A651')
		table.get_celld()[(1,0)].get_text().set_color(color = '#2E3191')
		ax = plt.gca()
		ax.tick_params(axis='x', pad=tick_label)
		ax.tick_params(axis='y', pad=tick_label)
		#plt.xlim([0, 100])
		#plt.savefig('myfig'+ sample)
		#plt.close()

	except Exception as e:
		print(e)
		print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))
		print("No file found")
		print(file_name)
		plt.subplot(4,4,i) # If error then plot an empty plot (for now)
		plt.plot()
		plt.title("Error " + file_name, pad = -1)
		#plt.savefig('myfig'+ sample)
		#plt.close()



