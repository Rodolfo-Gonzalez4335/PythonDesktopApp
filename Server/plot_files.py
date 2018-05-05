import os
import numpy as np
import matplotlib.pyplot as plt

def delete_files(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def plot_file(file_name):
	try:
		file = open(file_path,"r")
		array_of_nums = []

		for line in file:
			if 'DefectList' in line:
				for line in file:
					if 'SummarySpec' in line:
						break
					nums = []
					for num in line.strip(' ').split(' '):
						try:
							nums.append(float(num))
						except ValueError:
							if num!="":
								num = num.replace(';','')
								nums.append(float(num))
								pass
					array_of_nums.append(nums)
				continue
		file.close()
		x_offs = np.array(self.column(array_of_nums,3))
		y_offs = np.array(self.column(array_of_nums,4))
		x_locs = np.array(self.column(array_of_nums,1))
		y_locs = np.array(self.column(array_of_nums,2))
		x = np.add(x_locs, 1000*x_offs)
		y = np.add(y_locs, 1000*y_offs)
		
		# Plot a scatter plot
		plt.figure(figsize=(8, 6))
		plt.scatter(x,y)
		frame1 = plt.gca()
		frame1.axes.xaxis.set_ticklabels([])
		frame1.axes.yaxis.set_ticklabels([])
		file_name= file_name.replace(".txt","")
		
		plot_name = os.path.join(os.getcwd(), "plotted_images/", file_name)
		plt.savefig('{}.png'.format(plot_name))
		plt.close()
	except Exception as e:
		print (e)

def main:
	try:
		dir_path = os.path.join(os.getcwd(), "files_to_plot/")
		for filename in os.listdir(dir_path):
			if filename.endswith(".txt") :
				image_path = plot_file(filename)
		delete_files(dir_path) # Delete files to be plotted after plotting
	except Exception as e:
		print (e)

if __name__ == "__main__":
	# execute only if run as a script
	main()
