import pygame
from main import *
from random import randint
from random import sample

Blocked = pygame.sprite.Group()

class Diamond(pygame.sprite.Sprite):

    images = []
    List = pygame.sprite.Group()

    def __init__(self, x, y, clone, zone):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.clone = clone
        self.zone = zone

        if not Diamond.images:
            Diamond.images.append(pygame.image.load("res/diamond_spawn04.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn05.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn06.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn07.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn08.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn09.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn10.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn11.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn12.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn13.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn14.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn15.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn16.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn17.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn18.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn19.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn20.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn21.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn22.png").convert())
            Diamond.images.append(pygame.image.load("res/diamond_spawn23.png").convert())

        self.index = 0

        if not self.clone:
            self.image = Diamond.images[19]
        else:
            self.image = Diamond.images[1]

        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.zone.diamonds.add(self)

        if len(pygame.sprite.spritecollide(self, self.zone.diamonds, False)) > 1 or pygame.sprite.spritecollide(self, Blocked, False) or pygame.sprite.spritecollide(self, self.zone.blocked, False):
            self.zone.diamonds.remove(self)

    def update(self):
        if self.clone and self.index != len(Diamond.images):
            self.image = Diamond.images[self.index]
            self.image.set_colorkey((255, 255, 255))
            self.index += 1

    def spawn(self, screen_w, screen_h):
        if randint(1, 10) == 1:
            zones = []
            if self.rect.x in range(self.rect.w, screen_w - self.rect.w * 2) and self.rect.y in range(self.rect.h, screen_h - self.rect.h * 2):
                zone1 = [self.rect.x - self.rect.w, randint((self.rect.y - self.rect.h),(self.rect.y + self.rect.h))] #left side
                zone2 = [self.rect.x + self.rect.w, randint((self.rect.y - self.rect.h),(self.rect.y + self.rect.h))] #right side
                zone3 = [randint((self.rect.x - self.rect.w), (self.rect.x + self.rect.w)), self.rect.y - self.rect.h] # top side
                zone4 = [randint((self.rect.x - self.rect.w), (self.rect.x  + self.rect.w)), self.rect.y + self.rect.h] #bottom side
                zones = [zone1, zone2, zone3, zone4]
            elif self.rect.x < self.rect.w:
                zones = [[self.rect.x + self.rect.w, self.rect.y]] #right side
            elif self.rect.x > screen_w - self.rect.w * 2:
                zones = [[self.rect.x - self.rect.w, self.rect.y]] #left side
            elif self.rect.y < self.rect.h:
                zones = [[self.rect.x, self.rect.y + self.rect.h]] #bottom side
            elif self.rect.y > screen_h - self.rect.h * 2:
                zones = [[self.rect.x, self.rect.y - self.rect.h]] #top side

            try:
                rand_zone = zones[randint(0, len(zones) - 1)]
                Diamond(rand_zone[0], rand_zone[1], True, self.zone)
            except ValueError:
                pass

class Character(pygame.sprite.Sprite):

    List = pygame.sprite.Group()

    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.w = w
        self.h = h
        self.speed = 3
        self.diamonds = 0
        self.fuzzed = False
        self.current_city = None
        self.current_zone = None
        self.traveling_to = None
        self.rect = pygame.Rect(x, y, self.w, self.h)

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), (self.rect.x, self.rect.y, self.rect.w, self.rect.h))

    def collect_diamond(self):
        if self.diamonds != 100:
            self.diamonds += 1

    def starting_city(fuzz, agent):

        fuzz.current_city = sample(City.List, 1)[0]

        distances = {}
        for city in City.List:
            distances[city] = City.geocalc(fuzz.current_city, city)

        furthest_city = sorted(distances.values())[-1]

        for i in distances.iteritems():
            if i[1] == furthest_city:
                agent.current_city = i[0]
                agent.current_city.visited = True

    def starting_xy(self):
        pass

class Player(Character):

    images = []

    def __init__(self, x, y):
        Character.__init__(self, x, y, 40, 40)
        self.speed = 3
        self.diamonds = 5
        self.keys_pressed = []
        self.map_view = False
        self.current_city = None
        self.current_zone = [0, 1]
        Blocked.add(self)

    def drop_diamond(self, screen_w, screen_h):
        x = self.rect.x + self.rect.w / 2
        y = self.rect.y + self.rect.h / 2
        diamonds_count = len(self.current_zone.diamonds)
        if self.diamonds > 0 and self.rect.x in range(self.rect.w, screen_w - self.rect.w * 2) and self.rect.y in range(self.rect.h - 10, screen_h - self.rect.h * 2 + 10):

            if self.keys_pressed.count(1) == 2:
                if self.keys_pressed[pygame.K_s] and self.keys_pressed[pygame.K_a]:
                    x += 20
                    y -= 40
                elif self.keys_pressed[pygame.K_s] and self.keys_pressed[pygame.K_d]:
                    x -= 40
                    y -= 50
                elif self.keys_pressed[pygame.K_w] and self.keys_pressed[pygame.K_a]:
                    x += 20
                    y += 20
                elif self.keys_pressed[pygame.K_w] and self.keys_pressed[pygame.K_d]:
                    x -= 40
                    y += 20

                Diamond(x, y, False, self.current_zone)

                if len(self.current_zone.diamonds) != diamonds_count:
                    self.diamonds -= 1

            elif self.keys_pressed.count(1) == 1:
                if self.keys_pressed[pygame.K_s]:
                    x -= 20
                    y -= 50
                if self.keys_pressed[pygame.K_w]:
                    x -= 20
                    y += 20
                if self.keys_pressed[pygame.K_a]:
                    x += 20
                    y -= 10
                if self.keys_pressed[pygame.K_d]:
                    x -= 60
                    y -= 10

                Diamond(x, y, False, self.current_zone)
                if len(self.current_zone.diamonds) != diamonds_count:
                    self.diamonds -= 1

    def move(self, screen_w, screen_h):
        if self.keys_pressed[pygame.K_s]:
            self.rect.y += self.speed
            if pygame.sprite.spritecollide(self, self.current_zone.blocked, False):
                self.rect.y -= self.speed

        if self.keys_pressed[pygame.K_w]:
            self.rect.y -= self.speed
            if pygame.sprite.spritecollide(self, self.current_zone.blocked, False):
               self.rect.y += self.speed

        if self.keys_pressed[pygame.K_a]:
            self.rect.x -= self.speed
            if pygame.sprite.spritecollide(self, self.current_zone.blocked, False):
                self.rect.x += self.speed

        if self.keys_pressed[pygame.K_d]:
            self.rect.x += self.speed
            if pygame.sprite.spritecollide(self, self.current_zone.blocked, False):
                self.rect.x -= self.speed

        direction = None

        if self.rect.y < 20 - self.rect.h:
            direction = 'N'
        if self.rect.y > screen_h:
            direction = 'S'
        if self.rect.x < 0 - self.rect.w:
            direction = 'W'
        if self.rect.x > screen_w:
            direction = 'E'

        self.teleport(direction, screen_w, screen_h)

    def teleport(self, direction, screen_w, screen_h):
        if not direction:
            pass

        else:
            lay = self.current_zone.id[0]
            zon = self.current_zone.id[1]
            print lay, zon
            if direction == "N":
                self.current_zone = self.current_city.zones[str([lay - 1, zon])]
                self.rect.y = screen_h - 1
            elif direction == "S":
                self.current_zone = self.current_city.zones[str([lay + 1, zon])]
                self.rect.y = 1 - self.rect.h / 2
            elif direction == 'W':
                self.current_zone = self.current_city.zones[str([lay, zon - 1])]
                self.rect.x = screen_w - 1
            elif direction == 'E':
                self.current_zone = self.current_city.zones[str([lay, zon + 1])]
                self.rect.x = 1 - self.rect.w

class Wanderer(Character):

    images = []

    def __init__(self, x, y):
        Character.__init__(self, x, y, 40, 40)
        self.x = x
        self.y = y

class Fuzz(Character):

    images = []

    def __init__(self, x, y):
        Character.__init__(self, x, y, 80, 80)
        self.fuzzed = True
        self.current_city = None
