"""This is the main file for the project. Run this file to
get going"""

from pathlib import Path
import piexif
from geopy.distance import geodesic
import math
from uuid import uuid1
import config as conf


image_dict = {}
d_distance = conf.distance_from_drone
p_distance = conf.distance_from_POI

image_location = Path(conf.images_path)
input_file_location = Path(conf.input_file_path)





"""
Generates processable data from the video files provided as input in reqired format
"""
def get_video_data(video):
    with open(video, 'r') as v:
        video_data = []
        time_data = []
        count = 0
        for line in v:
            count += 1
            if (count % 4 == 0):
                video_data.append(time_data)
                time_data = []
                continue
            else:
                if(count % 2 == 0):
                    continue
                else:
                    time_data.append(line.strip())
        video_data.append(time_data)

        count = 0
        for data in video_data:
            data[0] = int(data[0])
            data[1] = data[1].split(',')
            data[1].remove('0')
            data[1][0] = float(data[1][0])
            data[1][1] = float(data[1][1])
        return video_data



"""
Generates processable data from the asset files provided as input in reqired format
"""
def get_assets_data(asset):
    with open(asset, 'r') as a:
        count = 0
        asset_data = []
        for line in a:
            data = []
            if count:
                data = line.split(',')
            else:
                count += 1
                continue
            asset_name = data[0]
            lat_lon = []
            lat_lon.append(float(data[1]))
            lat_lon.append(float(data[2]))
            temp_asset_data = [asset_name, lat_lon]
            asset_data.append(temp_asset_data)
        return asset_data


"""
Generates filename for the output files depending upon the configurations in
the config.py
"""
def generate_file_name(input_file):
    output_path = conf.output_file_path
    filename = conf.output_file_name
    if conf.create_multiple_output:
        file_name = output_path + input_file + filename + str(uuid1()).split('-')[-1] + '.csv'
    else:
        file_name = output_path + input_file +'_'+ filename + '.csv'
    return file_name


"""
Takes latitude and longitude data of the drone or asset and distance from config
and generates all the images which are under that range
"""

def get_images_under_distance(lat_lon, distance):
    unit = conf.distance_unit
    image_list = []
    for image in image_dict:
        reversed_image_lat_lon = tuple(image_dict[image])
        image_lat_lon = reversed(reversed_image_lat_lon)
        if unit == 'meters':
            calculated_distance = geodesic(lat_lon,image_lat_lon).meters
        elif unit == 'kilometers':
            calculated_distance = geodesic(lat_lon,image_lat_lon).kilometers
        elif unit == 'miles':
            calculated_distance = geodesic(lat_lon,image_lat_lon).miles
        else:
            calculated_distance = geodesic(lat_lon,image_lat_lon).meters
        if calculated_distance <= distance:
            image_list.append(image)

    image_list.sort()
    return image_list



def create_image_list_from_input_data():
    #Reads input files from input_file_list in config file
    if conf.selective_input_file == True:
        input_file_list = conf.input_file_list.split(',')
        for input_file in input_file_list:
            input_file = str(input_file_location) + '/' + input_file
            some_funtion(input_file)
    else:
        for input_file in input_file_location.iterdir():    #Reads input files from the input_file_path
            some_funtion(input_file)


def some_funtion(data_file):
    input_filename, file_type = str(data_file).split('.')
    if (file_type == 'SRT'):
        distance = d_distance
        all_location = get_video_data(data_file)
    elif(file_type == 'csv'):
        distance = p_distance
        all_location = get_assets_data(data_file)
    else:
        print('File', data_file,'is not of proper type!')


    #codeblock to generate a dictionary or positions and repective image list
    image_on_position = {}
    for location in all_location:
        position = str(location[0])
        lat_lon = tuple(location[1])
        image_list = get_images_under_distance(lat_lon, distance)
        image_on_position[position] = image_list

    #codeblock to convert image_on_position dict to csv file
    input_file = input_filename.split('/')[-1]
    filename = generate_file_name(input_file)

    with open(filename, 'w+') as file:
        for position in image_on_position:
            string = str(position)
            for image in image_on_position[position]:
                string = string + ',' + image
            string = string + '\n'
            file.write(string)
        #file.close()


"""gps_to_lat_lon generates latitude and longitude from the gps exif values.
Values from gps exif values are in degree, minutes, second format. They are
converted into decimal degree format and the returned as list"""
def gps_to_lat_lon(gps_loc):
    lat_lon = []
    for loc in gps_loc[0]:
        degree = loc[0][0]/loc[0][1]
        minute = loc[1][0]/loc[1][1]
        second = loc[2][0]/loc[2][1]
        complete_loc = degree + minute / 60 + second / 3600
        lat_lon.append(complete_loc)

    return lat_lon


"""create_image_dict populates the above defined image_dict with the
data taken from images in /images as image_name as key at latitude
longitude value as key values"""

def create_image_dict():
    for image in  image_location.iterdir():
        image = str(image)
        path_list = str(image).split('/')
        image_name = path_list[-1]

        exif_dict = piexif.load(image)

        image_gps_loc = []
        try:
            if(exif_dict["GPS"][2] and exif_dict["GPS"][4]):
                image_gps_loc.append((exif_dict["GPS"][2],exif_dict["GPS"][4]))
            image_dict[image_name] = gps_to_lat_lon(image_gps_loc)
        except:
            print(image_name, 'does not contain EXIF metadata')


def main():
    create_image_dict()
    create_image_list_from_input_data()


if __name__ == "__main__":
    main()
