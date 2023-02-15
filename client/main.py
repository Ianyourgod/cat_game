# test
import pygame
import base

pygame.init()

FPS = 60
SCREEN_SIZE = (500, 500)
VERSION = "0.0.1"

win = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Cat Game :3")

clock = pygame.time.Clock()

cat = base.Player(win, 50, 50, 5, "images/cat/N_I.png", "images/cat/NE_I.png", "images/cat/E_I.png", "images/cat/SE_I.png", "images/cat/S_I.png", "images/cat/SW_I.png", "images/cat/W_I.png", "images/cat/NW_I.png")

second_cat_test = base.Cat(400, 400, 50, 50, 5, "images/cat/N_I.png", "images/cat/NE_I.png", "images/cat/E_I.png", "images/cat/SE_I.png", "images/cat/S_I.png", "images/cat/SW_I.png", "images/cat/W_I.png", "images/cat/NW_I.png")

box = base.Object(100, 100, 50, 50, (255, 0, 0))

GRASS = pygame.transform.scale(pygame.image.load("images/tiles/grass.png").convert(), (32, 32))


debug = False
menu = True
hitboxes = False

run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                debug = not debug
            if event.key == pygame.K_F2:
                hitboxes = not hitboxes

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        menu = True
    
    if keys[pygame.K_w] and keys[pygame.K_s]:
        pass
    elif keys[pygame.K_a] and keys[pygame.K_d]:
        pass
    elif keys[pygame.K_w] and keys[pygame.K_d]:
        cat.move("NE")
    elif keys[pygame.K_w] and keys[pygame.K_a]:
        cat.move("NW")
    elif keys[pygame.K_s] and keys[pygame.K_d]:
        cat.move("SE")
    elif keys[pygame.K_s] and keys[pygame.K_a]:
        cat.move("SW")
    elif keys[pygame.K_w]:
        cat.move("N")
    elif keys[pygame.K_s]:
        cat.move("S")
    elif keys[pygame.K_a]:
        cat.move("W")
    elif keys[pygame.K_d]:
        cat.move("E")

    win.fill((0, 0, 0))

    for y in range((SCREEN_SIZE[1]+GRASS.get_height()*2)//GRASS.get_height()):
        for x in range((SCREEN_SIZE[0]+GRASS.get_width()*2)//GRASS.get_width()):
            win.blit(GRASS, (x*GRASS.get_width()-(base.PLAYER[0]%GRASS.get_width()), y*GRASS.get_height()-(base.PLAYER[1]%GRASS.get_height())))

    for obj in base.OBJECTS:
        obj.draw(win)
        if hitboxes:
            obj.draw_hitbox(win)

    # text
    if debug:
        font = pygame.font.SysFont("ariel", 30)
        text = font.render(f"Cat Game: version {VERSION}", 1, (255, 255, 255))
        win.blit(text, (0, 0))
        text = font.render(f"FPS: {round(clock.get_fps())}", 1, (255, 255, 255))
        win.blit(text, (0, 30))
        text = font.render(f"Coords: ({base.PLAYER[0]}, {base.PLAYER[1]})", 1, (255, 255, 255))
        win.blit(text, (0, 60))
        text = font.render(f"Objects: {len(base.OBJECTS)}", 1, (255, 255, 255))
        win.blit(text, (0, 90))

    pygame.display.update()

pygame.quit()