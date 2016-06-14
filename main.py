import pygame, sys, datetime
import character
from travel import *
from character import *

def current_time():
    pass

class Bar(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, w, h)
        character.Blocked.add(self)

    def draw(self, screen):
        pygame.draw.rect(screen, (0,0,0), (self.rect.x, self.rect.y, self.rect.w, self.rect.h))

def play_game():
    screen_w, screen_h = 800, 600

    pygame.init()

    screen = pygame.display.set_mode((screen_w, screen_h), 0, 32)

    clock = pygame.time.Clock()
    fps = 60

    fps_counter = 0
    timer = 0

    agent = Player(50, 50)
    bar = Bar(0, 0, screen_w, 20)
    map = Map()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    agent.drop_diamond(screen_w, screen_h)
                if event.key == pygame.K_m:
                    agent.map_view = True
                if event.key == pygame.K_n and agent.map_view:
                    agent.map_view = False

        agent.keys_pressed = pygame.key.get_pressed()
        if not agent.map_view:
            agent.move()
        elif agent.map_view:
            map.move(agent)

        fps_counter += 1

        if fps_counter % fps == 1:
            timer += 1

        if not agent.map_view:
            screen.fill((125,125,125))
            bar.draw(screen)
            Diamond.List.update()
            Diamond.List.draw(screen)

            if fps_counter % 10 == 0 and Diamond.List:
                for diamond in Diamond.List:
                    diamond.spawn(screen_w, screen_h)

            agent.draw(screen)

            if pygame.sprite.spritecollide(agent, Diamond.List, True):
                agent.collect_diamond()

        elif agent.map_view:
            map.draw(screen)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    play_game()
