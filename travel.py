#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from main import *
from math import radians, sqrt, sin, cos, atan2
from random import randint

class City():

    List = {}

    def __init__(self, name, lon, lat, state, size, population):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.state = state
        self.size = size
        self.population = population
        self.layout = []
        self.zones = []
        self.fuzzed = False
        self.List[self.name] = self
        self.wanderers = []

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
        print current_city, destination_city
        lat1 = radians(float(City.List[current_city].lat))
        lon1 = radians(float(City.List[current_city].lon))
        lat2 = radians(float(City.List[destination_city].lat))
        lon2 = radians(float(City.List[destination_city].lon))

        dlon = lon1 - lon2

        EARTH_R = 6372.8

        y = sqrt(
            (cos(lat2) * sin(dlon)) ** 2
            + (cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)) ** 2
            )
        x = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(dlon)
        c = atan2(y, x)
        return EARTH_R * c

class Train():
    pass


class Map(pygame.sprite.Sprite):

    Image = None

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.keys_pressed = []
        if not Map.Image:
            Map.Image = pygame.image.load("res/map.png").convert()
        self.rect = Map.Image.get_rect()
        self.rect.topleft = (1, 1)

    def draw(self, screen):
        screen.blit(Map.Image, self.rect)

    def move(self, player):
        if player.keys_pressed[pygame.K_s]:
            self.rect.y -= self.speed
        if player.keys_pressed[pygame.K_w]:
            self.rect.y += self.speed
        if player.keys_pressed[pygame.K_a]:
            self.rect.x += self.speed
        if player.keys_pressed[pygame.K_d]:
            self.rect.x -= self.speed

if __name__ == '__main__':
    City.spawn()
    cities = City.List.keys()
    print City.geocalc(cities[0], cities[5])
