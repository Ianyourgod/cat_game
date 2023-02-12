# test
import pygame
import base

pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Cat Game: 0")

clock = pygame.time.Clock()

cat = base.Cat(250, 250, 50, 50, 5, "images/cat/N.png", "images/cat/NE.png", "images/cat/E.png", "images/cat/SE.png", "images/cat/S.png", "images/cat/SW.png", "images/cat/W.png", "images/cat/NW.png")