# -*- coding: utf-8 -*-
import pygame
from main import *
from math import radians, sqrt, sin, cos, atan2
from random import randint

pygame.font.init()
font = pygame.font.Font("res/uni0563-webfont.ttf", 15)
Blocked = pygame.sprite.Group()

class MenuBar(pygame.sprite.Sprite):
    diamond = pygame.image.load("res/diamond_spawn23.png")
    diamond = pygame.transform.scale(diamond, (18, 18))

    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self, Blocked)
        self.rect = pygame.Rect(x, y, w, h)
        character.Blocked.add(self)
        MenuBar.diamond.convert()
        MenuBar.diamond.set_colorkey((255,255,255))

    def draw(self, screen, agent, time):
        pygame.draw.rect(screen, (0,0,0), (self.rect.x, self.rect.y, self.rect.w, self.rect.h))
        active_city = font.render(unicode(agent.current_city.name, 'utf-8'), 0, (200, 200, 200))
        agent_diamonds = font.render(str(agent.diamonds), 0, (200, 200, 200))
        screen.blit(active_city, (20,-4))
        screen.blit(time, (280, -4))
        screen.blit(agent_diamonds, (750, -4))
        screen.blit(MenuBar.diamond, (720, 0))

class Zone():
    def __init__(self, id, city):
        self.id = id
        self.diamonds = pygame.sprite.Group()
        self.blocked = pygame.sprite.Group()
        self.wanderers = pygame.sprite.Group()
        city.zones[str(id)] = self

    def spawn(self):
        pass

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, zone):
        pygame.sprite.Sprite.__init__(self, zone.blocked)
        self.rect = pygame.Rect(x, y, w, h)

    @staticmethod
    def spawn_core(zone):
        Wall(0, 20, 4, 200, zone) #left top
        Wall(0, 380, 4, 220, zone) #left bottom
        Wall(796, 20, 4, 200, zone) #left top
        Wall(796, 380, 4, 220, zone) #left bottom
        Wall(0, 20, 320, 4, zone) #top lef
        Wall(480, 20, 320, 4, zone) #top right
        Wall(0, 596, 320, 4, zone) #bottom left
        Wall(480, 596, 320, 4, zone) #bottom right

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), (self.rect.x, self.rect.y, self.rect.w, self.rect.h))

class City():

    List = []

    def __init__(self, name, lon, lat, state, size, population):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.state = state
        self.size = 5
        self.population = population
        self.layout = [[0, 1, 0],
                       [0, 1, 0],
                       [0, 0, 0]]
        self.zones = {}
        self.visited = False
        self.fuzzed = False
        self.List.append(self)

    def build(self):
        self.create_layout()
        self.generate_zones()
        self.generate_walls()
        #self.populate_zones()

    def create_layout(self):
        excluded = [[0,1], [1, 1]]
        active = 0
        for layer in self.layout:
            for zone in layer:
                if zone:
                    active += 1

        while active != self.size:
            zone = excluded[randint(0, len(excluded) - 1)]
            if zone != [0, 1]:
                empty_zones = self.check_surrounding(zone)
                try:
                    new_zone = empty_zones[randint(0, len(empty_zones) - 1)]
                    excluded.append(new_zone)
                    self.layout[new_zone[0]][new_zone[1]] = 1
                    active += 1
                except ValueError:
                    pass

    def check_surrounding(self, zone):
        layout_width = len(self.layout[0])
        layout_height = len(self.layout)
        x, y = zone[1], zone[0]
        surrounding_zones = []

        if y > 0 and not self.layout[y - 1][x]:                  #check top
            surrounding_zones.append([y - 1, x])
        if y < layout_height - 1 and not self.layout[y + 1][x]: #check bottom
            surrounding_zones.append([y + 1, x])
        if x > 0 and not self.layout[y][x - 1]:                  #check left
            surrounding_zones.append([y, x - 1])
        if x < layout_width - 1 and not self.layout[y][x + 1]:     #check right
            surrounding_zones.append([y, x + 1])

        return surrounding_zones

    def generate_zones(self):
        lay = 0
        for layer in self.layout:
            zon = 0
            for zone in layer:
                if zone:
                    Zone([lay, zon], self)
                zon += 1
            lay += 1
        for i in self.layout:
            print i

    def generate_walls(self):
        for zone in self.zones.itervalues():
            Wall.spawn_core(zone)
            

    @staticmethod
    def spawn():
        cities_count = randint(50, 100)

        with open('cities.txt', 'r') as f:
            list = [line.rstrip().split('\t') for line in f]

        for i in range(1, cities_count):
            city = list[randint(0, len(list) - 1)]

            name = city[0]
            lon = city[1]
            lat = city[2]
            state = city[3]
            size = city[4]
            population = city[5]

            City(name, lon, lat, state, size, population)

    @staticmethod
    def geocalc(current_city, destination_city):
        #print current_city, destination_city
        lat1 = radians(float(current_city.lat))
        lon1 = radians(float(current_city.lon))
        lat2 = radians(float(destination_city.lat))
        lon2 = radians(float(destination_city.lon))

        dlon = lon1 - lon2

        EARTH_R = 6372.8

        y = sqrt(
            (cos(lat2) * sin(dlon)) ** 2
            + (cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)) ** 2
            )
        x = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(dlon)
        c = atan2(y, x)
        return EARTH_R * c
        #return vincenty((City.List[current_city].lat, City.List[current_city].lon), (City.List[destination_city].lat, City.List[destination_city].lon)).meters / 1000

class Train():
    pass


class Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.keys_pressed = []
        self.image = pygame.image.load("res/map.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (1, 1)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, player, screen_w, screen_h):
        if player.keys_pressed[pygame.K_s]:
            print self.rect.y
            print -self.rect.h
            if self.rect.y > screen_h - self.rect.h + self.speed:
                self.rect.y -= self.speed
        if player.keys_pressed[pygame.K_w]:
            if self.rect.y < 0:
                self.rect.y += self.speed
            else:
                self.rect.y = 0
        if player.keys_pressed[pygame.K_a]:
            self.rect.x += self.speed
        if player.keys_pressed[pygame.K_d]:
            self.rect.x -= self.speed

