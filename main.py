import pygame
import sys
import requests
import os


# def show(map_file):
#     pygame.init()
#     screen = pygame.display.set_mode((600, 450))
#     # Рисуем картинку, загружаемую из только что созданного файла.
#     screen.blit(pygame.image.load(map_file), (0, 0))
#     # Переключаем экран и ждем закрытия окна.
#     pygame.display.flip()
#     run = True
#     while run:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_PAGEUP:
#                     pass
#
#     pygame.quit()
#
#     # Удаляем за собой файл с изображением.
#     os.remove(map_file)
#
#
# def get_mapfile(find_data, delta=0.002):
#     georecoder_server = "http://geocode-maps.yandex.ru/1.x/"
#
#     georecoder_params = {
#         'apikey': "40d1649f-0493-4b70-98ba-98533de7710b",
#         'geocode': find_data,
#         'format': 'json'}
#     response = requests.get(georecoder_server, params=georecoder_params)
#     if not response:
#         print("Ошибка выполнения запроса:")
#         print("Http статус:", response.status_code, "(", response.reason, ")")
#         sys.exit(1)
#     print(response.url)
#     print(response.headers)
#     print(response)
#
#     json_response = response.json()
#     first_data = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
#
#     center_data = first_data["Point"]["pos"]
#     lon_data, lat_data = center_data.split(" ")
#     # delta = "0.005"
#
#     map_params = {
#         'll': ','.join([lon_data, lat_data]),
#         'spn': ','.join([str(delta), str(delta)]),
#         'l': 'map'}
#
#     map_server = "http://static-maps.yandex.ru/1.x/"
#     response = requests.get(map_server, params=map_params)
#
#     map_file = "map.png"
#     with open(map_file, "wb") as file:
#         file.write(response.content)
#
#     return map_file
#
#
# def find(find_data, delta=0.002):
#     show(get_mapfile(find_data, delta))
#
#
# find('Москва', delta=1)


class Window:
    def __init__(self, start_lon=50, start_lat=50, delta=0.002):
        self.lon = start_lon
        self.lat = start_lat
        self.delta = delta
        self.map_file = None

    def show(self):
        if not self.map_file:
            print('no file')
            exit(1)
        pygame.init()
        screen = pygame.display.set_mode((600, 450))
        screen.blit(pygame.image.load(self.map_file), (0, 0))
        pygame.display.flip()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_PAGEUP:
                        # print('up')
                        # new_mapfile = get_mapfile()
                        pass

        pygame.quit()

        # Удаляем за собой файл с изображением.
        os.remove(self.map_file)

    def get_mapfile(self):
        # georecoder_server = "http://geocode-maps.yandex.ru/1.x/"
        # georecoder_params = {
        #     'apikey': "40d1649f-0493-4b70-98ba-98533de7710b",
        #     'geocode': find_data,
        #     'format': 'json'}
        # response = requests.get(georecoder_server, params=georecoder_params)
        # if not response:
        #     print("Ошибка выполнения запроса:")
        #     print("Http статус:", response.status_code, "(", response.reason, ")")
        #     sys.exit(1)
        # print(response.url)
        # print(response.headers)
        # print(response)
        #
        # json_response = response.json()
        # first_data = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        #
        # center_data = first_data["Point"]["pos"]
        # lon_data, lat_data = center_data.split(" ")
        # # delta = "0.005"
        map_params = {
            'll': ','.join([str(self.lon), str(self.lat)]),
            'spn': ','.join([str(self.delta), str(self.delta)]),
            'l': 'map'}

        map_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_server, params=map_params)

        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)

        self.map_file = map_file
        return map_file

    def find(self, find_data, delta=0.002):
        self.show(self.get_mapfile(delta))
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
        # delta = "0.005"


window = Window(start_lon=20, start_lat=20, delta=5)

window.get_mapfile()
window.show()
