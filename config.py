""" This is the config file for the project. All the configurations
which are necessary to run this project can be stored here. Change
these configurations according to your needs before running the project"""

#videos_path stores the path for the SRT file for the videos
input_file_path = 'videos'

#images_path stores the path for the images for the given video SRT file
images_path = 'images'


#selective_input_file is set if you want to provide the input file names
#directly to the program. If it is set then program will read files from
#input_file_list down below
selective_input_file = True


#If selective_input_file is set then input_file_list should have the names
#of input files seperated by a ',' and those files should pe present in
#input_file_path
# eg: 'filename1.csv,filename2.SRT,.....'
#Note that there should be no space and program assumes all files in csv
#format as asset files and files in SRT format as video files
input_file_list = 'assets.csv'


# sets the unit of distances used in the program. if set than all the input
#distances should also be in the same unit. If not set then by defauld it will
#use meters as the distance distance_unit
#options for unit are : meters, kilometers, and miles
distance_unit = 'kilometers'


#distance_from_drone stores the distance under which you want all your images
#to be from the position of drone
distance_from_drone = 0.035


#distance_from_POI stores the distance under which you want all your images
#to be from the position of POI
distance_from_POI = 0.050

#output_file_path stores the path for the output file. If not specified
#output files will be created in the same directory where main.py is.
output_file_path = 'output/'

#create_multiple_output is set to True if you want a new output to be created
#every time you run the program. If set to false, program will overwrite the
#same output file everytime
create_multiple_output = False

#program will create the output file with the name output_file_name.csv in the
#directory in output_file_path if create_multiple_output is set to False else
# output file will be created with some random values concatinated in the end.
output_file_name = 'output'
