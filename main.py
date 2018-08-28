"""This is the main file for the project. Run this file to
get going"""

from pathlib import Path
import piexif
from geopy.distance import geodesic
import math
import config as c

image_dict = {}
d_distance = c.distance_from_drone
p_distance = c.distance_from_POI

image_location = Path(c.images_path)
video_location = Path(c.videos_path)


def create_image_list_from_video():
    for video in video_location.iterdir():
        all_location = get_video_data(video)
        image_on_position = {}
        for location in all_location:
            position = str(location[0])
            lat_lon = tuple(location[1])
            image_list = get_images_under_distance(lat_lon, d_distance)
            image_on_position[position] = image_list
        #code to convert image_on_position dict to csv file
        print(image_on_position)





def get_video_data(video):
    with open(video, 'r') as v:
        video_data = []
        time_data = []
        count = 0
        for line in v:
            count += 1
            if (count%4 == 0):
                video_data.append(time_data)
                time_data = []
                continue
            else:
                if(count%2 == 0):
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



"""create_image_dict populates the above defined image_dict with the
data taken from images in /images as image_name as key at latitude
longitude value as key values"""

def create_image_dict():
    for image in  image_location.iterdir():
        image = str(image)
        path_list = image.split('/')
        image_name = path_list[-1]

        exif_dict = piexif.load(image)

        image_gps_loc = []
        try:
            if(exif_dict["GPS"][2] and exif_dict["GPS"][4]):
                image_gps_loc.append((exif_dict["GPS"][2],exif_dict["GPS"][4]))
            image_dict[image_name] = gps_to_lat_lon(image_gps_loc)
        except:
            print(image_name, 'does not contain EXIF metadata')



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


def get_images_under_distance(lat_lon, distance):
    image_list = []
    for image in image_dict:
        reversed_image_lat_lon = tuple(image_dict[image])
        image_lat_lon = reversed(reversed_image_lat_lon)
        calculated_distance = geodesic(lat_lon,image_lat_lon).meters
        print(calculated_distance)
        if calculated_distance <= distance:
            image_list.append(image)

    image_list.sort()

    return image_list

if __name__ == "__main__":
    create_image_dict()
    create_image_list_from_video()

#create_image_dict()
#print(image_dict)
create_image_list_from_video()
