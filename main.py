# test
import pygame
import base

pygame.init()

FPS = 60

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Cat Game: 0")

clock = pygame.time.Clock()

cat = base.Player(win, 50, 50, 5, "images/cat/N_I.png", "images/cat/NE_I.png", "images/cat/W_I.png", "images/cat/SE_I.png", "images/cat/S_I.png", "images/cat/SW_I.png", "images/cat/E_I.png", "images/cat/NW_I.png")

box = base.Object(100, 100, 50, 50, (255, 0, 0))

run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

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
    for obj in base.OBJECTS:
        obj.draw(win)
    pygame.display.update()

    pygame.display.set_caption(f"Cat Game: {round(clock.get_fps())}")