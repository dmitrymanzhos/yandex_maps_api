import pygame
import sys
import requests
import os


class Window:
    def __init__(self, start_lon=50, start_lat=50, delta=0.002):
        self.lon = start_lon
        self.lat = start_lat
        self.delta = delta
        self.map_file = None
        self.z = 15

    def show_screen(self):
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
                    run = False
                    os.remove(self.map_file)
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_PAGEUP, pygame.K_1]:
                        print('up')
                        if self.z > 0:
                            self.delta *= 2
                            self.z -= 1
                            self.get_mapfile()
                            print('0k')
                            screen.blit(pygame.image.load(self.map_file), (0, 0))

                    elif event.key in [pygame.K_PAGEDOWN, pygame.K_2]:
                        if self.z < 17:
                            print('down')
                            self.delta /= 2
                            self.z += 1
                            self.get_mapfile()
                            print('0k')
                            screen.blit(pygame.image.load(self.map_file), (0, 0))
                    elif event.key == pygame.K_LEFT:
                        if self.lon - self.delta > -180:
                            self.lon -= self.delta
                            self.get_mapfile()
                            screen.blit(pygame.image.load(self.map_file), (0, 0))
                    elif event.key == pygame.K_RIGHT:
                        if self.lon + self.delta < 180:
                            self.lon += self.delta
                            self.get_mapfile()
                            screen.blit(pygame.image.load(self.map_file), (0, 0))
                    elif event.key == pygame.K_UP:
                        if self.lat + self.delta < 90:
                            self.lat += self.delta * 0.432
                            self.get_mapfile()
                            screen.blit(pygame.image.load(self.map_file), (0, 0))
                    elif event.key == pygame.K_DOWN:
                        if self.lat - self.delta > -90:
                            self.lat -= self.delta * 0.432
                            self.get_mapfile()
                            screen.blit(pygame.image.load(self.map_file), (0, 0))
            pygame.display.flip()

    def get_mapfile(self):
        map_params = {
            'll': ','.join([str(self.lon), str(self.lat)]),
            # 'spn': ','.join([str(self.delta), str(self.delta)]),
            'z': str(self.z),
            'size': '600,450',
            'l': 'map'}

        map_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_server, params=map_params)
        if not response:
            print('???????????? ???????????????????? ??????????????')
            exit(1)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)

        self.top = 0
        self.left = 0
        self.map_file = map_file

    def find(self, find_data):
        georecoder_server = "http://geocode-maps.yandex.ru/1.x/"
        georecoder_params = {
            'apikey': "40d1649f-0493-4b70-98ba-98533de7710b",
            'geocode': find_data,
            'format': 'json'}
        response = requests.get(georecoder_server, params=georecoder_params)
        if not response:
            print("???????????? ???????????????????? ??????????????:")
            print("Http ????????????:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        json_response = response.json()
        first_data = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

        center_data = first_data["Point"]["pos"]
        self.lon, self.lat = (float(el) for el in center_data.split(" "))
        self.delta = 0.0258


window = Window(start_lon=0, start_lat=0, delta=0.05)
window.find('??????')
window.get_mapfile()
window.show_screen()
