# -*- coding: iso-8859-2 -*-
import pygame, sys, datetime
import character
from location import *
from character import *

def current_time(t_secs):
    try:
        val = int(t_secs)
    except ValueError:
        return "!!!ERROR: ARGUMENT NOT AN INTEGER!!!"
    pos = abs( int(t_secs) )
    day = pos / (3600*24)
    rem = pos % (3600*24)
    hour = rem / 3600
    rem = rem % 3600
    mins = rem / 60
    secs = rem % 60
    res = 'Day %02d, Current Time: %02d:%02d:%02d' % (day, hour, mins, secs)
    if int(t_secs) < 0:
        res = "-%s" % res
    return res

def play_game():
    screen_w, screen_h = 800, 600

    pygame.init()

    screen = pygame.display.set_mode((screen_w, screen_h), 0, 32)

    pygame.font.init()
    font = pygame.font.Font("res/uni0563-webfont.ttf", 15)

    clock = pygame.time.Clock()
    fps = 60

    fps_counter = 0
    timer = 129600

    map = Map()
    bar = Bar(0, 0, screen_w, 20)
    City.spawn()
    fuzz = Fuzz(600, 500)
    agent = Player(50, 50)
    Character.starting_city(fuzz, agent)
    active_city = font.render(unicode(agent.current_city, 'utf-8'), 0, (200, 200, 200))

    while not agent.fuzzed and fuzz.fuzzed:
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
            map.move(agent, screen_w, screen_h)

        fps_counter += 1

        if fps_counter % fps == 1:
            timer += 1
            time = font.render(current_time(timer), 0, (200, 200, 200))

        if not agent.map_view:
            screen.fill((125,125,125))
            bar.draw(screen)
            screen.blit(active_city, (20,-4))
            screen.blit(time, (screen_w - 340, -4))
            #agent.current_city.draw_zone(screen, agent)
            Diamond.List.update()
            Diamond.List.draw(screen)

            if fps_counter % 20 == 0 and Diamond.List:
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
