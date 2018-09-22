# from PIL import Image
# from PIL.ExifTags import TAGS, GPSTAGS

# import logging
import urllib.request
import piexif
import exifread
from flask import request, jsonify

from codeitsuisse import app

# logger = logging.getLogger(__name__)



@app.route('/imagesGPS', methods=['POST'])
def photogps():
    data = request.get_json()
    app.logger.info("data sent for evaluation {}".format(data))
    result = []
    for link in data:
        # app.logger.info(link['path']) #geturl
        url = link['path']
        local_filename, headers = urllib.request.urlretrieve(url)
        resource = open(local_filename, 'rb')
        # app.logger.info(resource)
        # resource = urllib.request.urlopen(link['path']).read()
        # app.logger.info(resource) #geturl
        result.append(extract(resource))
    return jsonify(result)

def extract(file):
    # exif_dict = piexif.load("foo1.jpg")
    # exif_dict = piexif.load(file)
    # app.logger.info(file)
    # file = open(, 'rb')
    exif_dict = exifread.process_file(file, details=False)
    # app.logger.info(exif_dict)
    # app.logger.info(exif_dict['GPS GPSLatitude'])
    
    lat=_convert_to_degress(exif_dict['GPS GPSLatitude'])
    lon=_convert_to_degress(exif_dict["GPS GPSLongitude"])
    return {
        "lat":lat,
        "long":lon
    }

    # for ifd in ("0th", "Exif", "GPS", "1st"):
    # for ifd in ("GPS",):
    #     for tag in exif_dict[ifd]:
    #         # pass
    #         app.logger.info(exif_dict[ifd][tag])
    #         # app.logger.info(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])

def convert_to_degress(value):

    """Helper function to convert the GPS coordinates 
    stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)


# class ImageMetaData(object):
#     '''
#     Extract the exif data from any image. Data includes GPS coordinates, 
#     Focal Length, Manufacture, and more.
#     '''
#     exif_data = None
#     image = None

#     def __init__(self, img_path):
#         self.image = Image.open(img_path)
#         #print(self.image._getexif())
#         self.get_exif_data()
#         super(ImageMetaData, self).__init__()

#     def get_exif_data(self):
#         """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
#         exif_data = {}
#         info = self.image._getexif()
#         if info:
#             for tag, value in info.items():
#                 decoded = TAGS.get(tag, tag)
#                 if decoded == "GPSInfo":
#                     gps_data = {}
#                     for t in value:
#                         sub_decoded = GPSTAGS.get(t, t)
#                         gps_data[sub_decoded] = value[t]

#                     exif_data[decoded] = gps_data
#                 else:
#                     exif_data[decoded] = value
#         self.exif_data = exif_data
#         return exif_data

#     def get_if_exist(self, data, key):
#         if key in data:
#             return data[key]
#         return None

#     def convert_to_degress(self, value):

#         """Helper function to convert the GPS coordinates 
#         stored in the EXIF to degress in float format"""
#         d0 = value[0][0]
#         d1 = value[0][1]
#         d = float(d0) / float(d1)

#         m0 = value[1][0]
#         m1 = value[1][1]
#         m = float(m0) / float(m1)

#         s0 = value[2][0]
#         s1 = value[2][1]
#         s = float(s0) / float(s1)

#         return d + (m / 60.0) + (s / 3600.0)

#     def get_lat_lng(self):
#         """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
#         lat = None
#         lng = None
#         exif_data = self.get_exif_data()
#         #print(exif_data)
#         if "GPSInfo" in exif_data:      
#             gps_info = exif_data["GPSInfo"]
#             gps_latitude = self.get_if_exist(gps_info, "GPSLatitude")
#             gps_latitude_ref = self.get_if_exist(gps_info, 'GPSLatitudeRef')
#             gps_longitude = self.get_if_exist(gps_info, 'GPSLongitude')
#             gps_longitude_ref = self.get_if_exist(gps_info, 'GPSLongitudeRef')
#             if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
#                 lat = self.convert_to_degress(gps_latitude)
#                 if gps_latitude_ref != "N":                     
#                     lat = 0 - lat
#                 lng = self.convert_to_degress(gps_longitude)
#                 if gps_longitude_ref != "E":
#                     lng = 0 - lng
#         return lat, lng