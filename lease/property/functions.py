
import requests
import overpy
import numpy as np
from geopy import Nominatim
# from requests.utils import quote
from skimage.measure import find_contours, points_in_poly, approximate_polygon
from skimage import io
from skimage import color
from threading import Thread

class Map:
    import overpy

    def get_layout_geo_py(self, latitude, longitude):
        geolocator = Nominatim(user_agent="geoapiExerciser")
        location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True)
        if location:
            address, (latitude, longitude) = location
            response = location.raw['boundingbox']
            response = {
                "latitude_max": response[0],
                "longitude_max": response[2],
                "latitude_min": response[1],
                "longitude_min": response[3],
            }
        else:
            response = {
                "latitude_max": latitude,
                "longitude_max": longitude,
                "latitude_min": latitude,
                "longitude_min": longitude,
            }


        return response

    def get_layout(self, latitude, longitude):
        api = overpy.Overpass()

        result = api.query(f"""
            way
                ["building"]
                (around:1,{latitude},{longitude});
            (._;>;);
            out body;
        """)
        if len(result.ways)>0:
            # Initialize variables to store the bounding box information
            lat_min = float(result.ways[0].nodes[0].lat)
            lat_max = float(result.ways[0].nodes[0].lat)
            lon_min = float(result.ways[0].nodes[0].lon)
            lon_max = float(result.ways[0].nodes[0].lon)
        else:
            lat_min = latitude
            lat_max = latitude
            lon_max = longitude
            lon_min = longitude

        # Loop through the results to get the bounding box information
        for building in result.ways:
            for node in building.nodes:
                lat = float(node.lat)
                lon = float(node.lon)
                lat_min = min(lat_min, lat)
                lat_max = max(lat_max, lat)
                lon_min = min(lon_min, lon)
                lon_max = max(lon_max, lon)

        response = {
            "latitude_max": lat_max,
            "longitude_max": lon_max,
            "latitude_min": lat_min,
            "longitude_min": lon_min,
        }

        # Return the bounding box information
        return response

    def get_layout_google(self, latitude, longitude):
        center_latitude = latitude
        center_longitude = longitude
        mapZoom = str(20)
        midX = 300
        midY = 300
        API_KEY = 'AIzaSyDEo0zcs71yV8XkDUuWmqNIXYGWnENDQMo'
        str_Center = str(center_latitude) + "," + str(center_longitude)
        str_Size = str(midX * 2) + "x" + str(midY * 2)
        safeURL_Style = quote(
            'feature:landscape.man_made|element:geometry.stroke|visibility:on|color:0xffffff|weight:1')
        urlBuildings = "http://maps.googleapis.com/maps/api/staticmap?center=" + str_Center + "&zoom=" + mapZoom + "&format=png32&sensor=false&size=" + str_Size + "&maptype=roadmap&style=visibility:off&style=" + safeURL_Style+ "&key=" + API_KEY

        mainBuilding = None
        imgBuildings = io.imread(urlBuildings)
        gray_imgBuildings = color.rgb2gray(imgBuildings)
        binary_imageBuildings = np.where(gray_imgBuildings > np.mean(gray_imgBuildings), 0.0, 1.0)
        contoursBuildings = find_contours(binary_imageBuildings, 0.1)

        for n, contourBuilding in enumerate(contoursBuildings):
            if (contourBuilding[0, 1] == contourBuilding[-1, 1]) and (contourBuilding[0, 0] == contourBuilding[-1, 0]):
                isInside = False
                skipPoly = False
                for othersPolygon in contoursBuildings:
                    isInside = points_in_poly(contourBuilding, othersPolygon)
                    if all(isInside):
                        skipPoly = True
                        break

                if skipPoly == False:
                    center_inside = points_in_poly(np.array([[midX, midY]]), contourBuilding)
                    if center_inside:
                        mainBuilding = approximate_polygon(contourBuilding, tolerance=2)

        # Find the minimum and maximum latitude and longitude values from the mainBuilding polygon
        lat_max = -90
        lat_min = 90
        lon_max = -180
        lon_min = 180
        for point in mainBuilding:
            lat, lon = point[1], point[0]
            if lat > lat_max:
                lat_max = lat
            if lat < lat_min:
                lat_min = lat
            if lon > lon_max:
                lon_max = lon
            if lon < lon_min:
                lon_min = lon

        response = {
            "latitude_max": lat_max,
            "longitude_max": lon_max,
            "latitude_min": lat_min,
            "longitude_min": lon_min,
        }
        return response




