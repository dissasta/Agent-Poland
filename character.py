import pygame
from main import *
from random import randint

class Diamond(pygame.sprite.Sprite):

    images = []
    List = pygame.sprite.Group()

    def __init__(self, x, y, origin):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.origin = origin

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
        if origin == 'Drop':
            self.image = Diamond.images[19]
        elif origin == 'Clone':
            self.image = Diamond.images[1]

        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.List.add(self)

        if len(pygame.sprite.spritecollide(self, Diamond.List, False)) > 1 or pygame.sprite.spritecollide(self, Character.List, False):
            Diamond.List.remove(self)

    def update(self):
        if self.origin == 'Clone' and self.index != len(Diamond.images):
            self.image = Diamond.images[self.index]
            self.image.set_colorkey((255, 255, 255))
            self.index += 1

    def spawn(self, screen_w, screen_h):
        if randint(1, 10) == 1:
            zones = []
            if self.rect.x in range(self.rect.w, screen_w - self.rect.w * 2) and self.rect.y in range(self.rect.h, screen_h - self.rect.h * 2):
                zone1 = [self.rect.x - self.rect.w, randint((self.rect.y - self.rect.h),(self.rect.y + self.rect.h))]
                zones.append(zone1)
            if self.rect.x in range(self.rect.w, screen_w - self.rect.w * 2) and self.rect.y in range(self.rect.h, screen_h - self.rect.h * 2):
                zone2 = [self.rect.x + self.rect.w, randint((self.rect.y - self.rect.h),(self.rect.y + self.rect.h))]
                zones.append(zone2)
            if self.rect.y in range(self.rect.h, screen_h - self.rect.h * 2) and self.rect.x in range(self.rect.w, screen_w - self.rect.w * 2):
                zone3 = [randint((self.rect.x - self.rect.w), (self.rect.x + self.rect.w)), self.rect.y - self.rect.h]
                zones.append(zone3)
            if self.rect.y in range(self.rect.h, screen_h - self.rect.h * 2) and self.rect.x in range(self.rect.w, screen_w - self.rect.w * 2):
                zone4 = [randint((self.rect.x - self.rect.w), (self.rect.x  + self.rect.w)), self.rect.y + self.rect.h]
                zones.append(zone4)

            try:
                rand_zone = zones[randint(0, len(zones) - 1)]
                Diamond(rand_zone[0], rand_zone[1], 'Clone')
            except ValueError:
                pass

class Character(pygame.sprite.Sprite):

    List = pygame.sprite.Group()

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 40
        self.height = 40
        self.speed = 3
        self.diamonds = 0
        self.fuzzed = False
        self.current_city = None
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), (self.rect.x, self.rect.y, self.width, self.height))

    def collect_diamond(self):
        if self.diamonds != 100:
            self.diamonds += 1

class Player(Character):

    images = []

    def __init__(self, x, y):
        Character.__init__(self,x, y)
        self.speed = 3
        self.diamonds = 50
        self.keys_pressed = []
        self.map_view = False
        self.rect = pygame.Rect(x, y, self.width, self.height)
        Character.List.add(self)

    def drop_diamond(self):
        x = self.rect.x + self.width / 2
        y = self.rect.y + self.height / 2
        if self.diamonds > 0:

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
                Diamond(x, y, 'Drop')
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

                Diamond(x, y,'Drop')
                self.diamonds -= 1

    def move(self):
        if self.keys_pressed[pygame.K_s]:
            self.rect.y += self.speed
        if self.keys_pressed[pygame.K_w]:
            self.rect.y -= self.speed
        if self.keys_pressed[pygame.K_a]:
            self.rect.x -= self.speed
        if self.keys_pressed[pygame.K_d]:
            self.rect.x += self.speed

class Wanderer(Character):

    images = []

    def __init__(self, x, y):
        Character.__init__(self, x, y)
        self.x = x
        self.y = y

class Fuzz(Character):

    images = []

    def __init__(self, x, y):
        Character.__init__(self, x, y)
        self.x = x
        self.y = y
        self.fuzzed = True