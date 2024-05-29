Key = 'AIzaSyBJmrKUWYFYwTtYd1Rx9YrpKTG6jsXrEk8'
import googlemaps
import io
from PIL import Image, ImageTk
import tkinter as tk

def find_XY(gmaps, to_find):
    geocode_result = gmaps.geocode(to_find, language='ko')

    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]

    return latitude, longitude

def show_map(gmaps, location, zoom_level, map_type, pin_locations):
    markers = '|'.join([f"{lat},{lng}" for lat, lng in pin_locations])
    static_map = gmaps.static_map(center=location, zoom=zoom_level, size=(400, 400), maptype=map_type, markers=markers)
    static_map_bytes = b''.join(static_map)
    img_data = io.BytesIO(static_map_bytes)
    img = Image.open(img_data)
    root = tk.Tk()
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(root, image=tk_img)
    label.pack()
    root.mainloop()

def get_map_image(gmaps, location, zoom_level, map_type, pin_locations):
    markers = '|'.join([f"{lat},{lng}" for lat, lng in pin_locations])
    static_map = gmaps.static_map(center=location, zoom=zoom_level, size=(400, 400), maptype=map_type, markers=markers)
    static_map_bytes = b''.join(static_map)
    img_data = io.BytesIO(static_map_bytes)
    img = Image.open(img_data)
    return img


# Google Maps API 키
Google_API_Key = Key
gmaps = googlemaps.Client(Google_API_Key)


def print_map(location_name):
    gmaps = googlemaps.Client(key='AIzaSyBJmrKUWYFYwTtYd1Rx9YrpKTG6jsXrEk8')
    zoom_level = 15
    map_type = 'satellite'

    latitude, longitude = find_XY(gmaps, location_name)
    pin_locations = [(latitude, longitude)]
    img = get_map_image(gmaps, (latitude, longitude), zoom_level, map_type, pin_locations)
    return img

if __name__ == "__main__":
    location_name = '북한산'
    print_map(location_name)
=======

# 검색할 지역명
location_name = '북한산'
# 지도의 줌 레벨
zoom_level = 20

map_type = 'satellite'

# 지역명으로 좌표 검색
latitude, longitude = find_XY(gmaps, location_name)


pin_locations = [(latitude, longitude)]

# 검색된 좌표로 지도를 보여주기
show_map(gmaps, (latitude, longitude), zoom_level, map_type, pin_locations)

print(pin_locations
      )
NX = int(pin_locations[0][0])
NY = int(pin_locations[0][1])

print(NX,NY)
