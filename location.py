#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from main import *
from math import radians, sqrt, sin, cos, atan2
from random import randint
from geopy.distance import vincenty

class Bar(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, w, h)
        character.Blocked.add(self)

    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), (self.rect.x, self.rect.y, self.rect.w, self.rect.h))

class Zone():
    def __init__(self):
        self.id = None
        self.blocked = pygame.sprite.Group()
        self.wanderers = pygame.sprite.Group()

    def spawn(self):
        pass

class City():

    List = {}

    def __init__(self, name, lon, lat, state, size, population):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.state = state
        self.size = size
        self.population = population
        self.layout = [[0, 1, 0],
                       [0, 1, 0],
                       [0, 0, 0]]
        self.zones = []
        self.fuzzed = False
        self.List[self.name] = self
        self.generate_zones()

    def generate_zones(self):
        active = 0
        for layer in self.layout:
            for zone in layer:
                if zone:
                    active += 1

        if active != self.size:
            pass

    def draw_zone(self, screen, player):
        for obj in player.current_zone:
            obj.draw(screen)

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
        return vincenty((City.List[current_city].lat, City.List[current_city].lon), (City.List[destination_city].lat, City.List[destination_city].lon)).meters / 1000

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