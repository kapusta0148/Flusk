from io import BytesIO
import requests
from PIL import Image
from scale_utils import get_spn


toponym_to_find = input()

geocoder_api_server = "https://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": toponym_to_find,
    "format": "json"
}
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    raise RuntimeError("Ошибка запроса к геокодеру")

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

toponym_coordinates = toponym["Point"]["pos"]
longitude, latitude = toponym_coordinates.split(" ")

envelope = toponym["boundedBy"]["Envelope"]
dx, dy = get_spn(envelope)

map_api_server = "https://static-maps.yandex.ru/v1"
map_params = {
    "ll": ",".join([longitude, latitude]),
    "spn": ",".join([dx, dy]),
    "l": "map",
    "pt": f"{longitude},{latitude},pm2rdm",
    "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
}
map_response = requests.get(map_api_server, params=map_params)


image = Image.open(BytesIO(map_response.content))
image.show()
