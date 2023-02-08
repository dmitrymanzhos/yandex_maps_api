import pygame
import sys
import requests
import os


def show(map_file):
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

    os.remove(map_file)


def get_mapfile(find_data, delta=0.002):
    georecoder_server = "http://geocode-maps.yandex.ru/1.x/"

    georecoder_params = {
        'apikey': "40d1649f-0493-4b70-98ba-98533de7710b",
        'geocode': find_data,
        'format': 'json'}
    response = requests.get(georecoder_server, params=georecoder_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    print(response.url)
    print(response.headers)
    print(response)

    json_response = response.json()
    first_data = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

    center_data = first_data["Point"]["pos"]
    lon_data, lat_data = center_data.split(" ")

    map_params = {
        'll': ','.join([lon_data, lat_data]),
        'spn': ','.join([str(delta), str(delta)]),
        'l': 'map'}

    map_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_server, params=map_params)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return map_file


def find(find_data, delta=0.002):
    show(get_mapfile(find_data, delta))


find('Москва', delta=1)
