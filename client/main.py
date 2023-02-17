import pygame
import base
import requests
import time

pygame.init()

FPS = 1000
SCREEN_SIZE = (500, 500)
VERSION = "0.0.5"
SERVER_IP = "192.168.2.7"
SERVER_NAME = ""
OTHER_PLAYERS = []

win = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Cat Game :3")

clock = pygame.time.Clock()

cat = base.Player(win, 50, 50, 5, "images/cat/N_I.png", "images/cat/NE_I.png", "images/cat/E_I.png", "images/cat/SE_I.png", "images/cat/S_I.png", "images/cat/SW_I.png", "images/cat/W_I.png", "images/cat/NW_I.png")

box = base.Object(-100, -100, 200, 200, image="images/tiles/trashtree.gif", collision=False)
box_hit = base.Object(-32, 80, 63, 20, (255, 0, 0), visible=False)

GRASS = pygame.transform.scale(pygame.image.load("images/tiles/grass.png").convert(), (32, 32))


debug = False
main_menu = True
create_menu = False
join_menu = False
hitboxes = False


debug_font = pygame.font.SysFont("ariel", 30)
menu_font = pygame.font.Font("fonts/Eight-Bit Madness.ttf", 30)

def create_server():
    name = create_name_t.text
    username = username_t.text
    data = requests.post(f"http://{SERVER_IP}:5000/create", json={"name": username, "room": name}).json()
    if data['success']:
        global create_menu, SERVER_NAME
        create_menu = False
        create_confirm_b.visible = False
        create_confirm_b.clickable = False
        create_name_t.selected = False
        create_name_t.visible = False
        create_name_t.text = ""
        SERVER_NAME = name

def create_server_button():
    print("WHYY")
    global main_menu, create_menu
    main_menu = False
    create_menu = True
    join_server_b.visible = False
    create_server_b.visible = False
    create_confirm_b.visible = True
    create_confirm_b.clickable = True
    create_name_t.visible = True

        
def join_server():
    name = create_name_t.text
    username = username_t.text
    data = requests.post(f"http://{SERVER_IP}:5000/join", json={"name": username, "room": name}).json()
    if data['success']:
        global join_menu, SERVER_NAME
        join_menu = False
        join_confirm_b.visible = False
        join_confirm_b.clickable = False
        join_name_t.selected = False
        join_name_t.visible = False
        join_name_t.text = ""
        SERVER_NAME = name
def join_server_button():
    global main_menu, join_menu
    main_menu = False
    join_menu = True
    join_server_b.visible = False
    join_name_t.visible = True
    join_confirm_b.visible = True
    join_confirm_b.clickable = True
    create_server_b.visible = False
    create_server_b.clickable = False
        
def leave_server():
    name = create_name_t.text
    username = username_t.text
    data = requests.post(f"http://{SERVER_IP}:5000/leave", json={"name": username, "room": name}).json()
    if data['success']:
        global main_menu
        main_menu = True
        join_server_b.visible = True
        create_server_b.visible = True
        
def main_menu_f(y_n):
    global main_menu, create_menu, join_menu
    true = y_n
    main_menu = true
    join_server_b.visible = true
    create_server_b.visible = true
    create_name_t.visible = False
    create_menu = False
    join_menu = False
    create_name_t.text = ""
    create_confirm_b.visible = False
    create_confirm_b.clickable = False  
    
def update():
    name = SERVER_NAME
    username = username_t.text
    data = requests.post(f"http://{SERVER_IP}:5000/update", json={"name": username, "room": name, "x": cat.x, "y": cat.y, "direction": cat.direction}).json()
    if data['success']:
        global OTHER_PLAYERS
        OTHER_PLAYERS = data['players']
        for player in OTHER_PLAYERS:
            if player['username'] == username:
                OTHER_PLAYERS.remove(player)
                break

    
username_t = base.Textbox(SCREEN_SIZE[0]/2-100, SCREEN_SIZE[1]/2+115, 200, 50, (255, 255, 255), menu_font, "Username...", image="images/textures/stone_button.png")

create_server_b = base.Button(SCREEN_SIZE[0]/2-50, SCREEN_SIZE[1]/2+50, 100, 50, "Create", (255, 255, 255), (0, 0, 0), menu_font, image="images/textures/stone_button.png", click=create_server_button)
create_name_t = base.Textbox(SCREEN_SIZE[0]/2-100, SCREEN_SIZE[1]/2+50, 200, 50, (255, 255, 255), menu_font, "Server name...", image="images/textures/stone_button.png", visible=False)
create_confirm_b = base.Button(SCREEN_SIZE[0]/2-50, SCREEN_SIZE[1]/2+120, 100, 50, "Confirm", (255, 255, 255), (0, 0, 0), menu_font, image="images/textures/stone_button.png", click=create_server, clickable=False, visible=False)

join_server_b = base.Button(SCREEN_SIZE[0]/2-50, SCREEN_SIZE[1]/2+180, 100, 50, "Join", (255, 255, 255), (0, 0, 0), menu_font, image="images/textures/stone_button.png", click=join_server_button)
join_name_t = base.Textbox(SCREEN_SIZE[0]/2-100, SCREEN_SIZE[1]/2+50, 200, 50, (255, 255, 255), menu_font, "Server name...", image="images/textures/stone_button.png", visible=False)
join_confirm_b = base.Button(SCREEN_SIZE[0]/2-50, SCREEN_SIZE[1]/2+120, 100, 50, "Confirm", (255, 255, 255), (0, 0, 0), menu_font, image="images/textures/stone_button.png", click=join_server, clickable=False, visible=False)


main_menu_f(True)

player_drawer = base.OtherPlayerDrawer()

prev_time = time.time()
run = True
while run:
    milli = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                debug = not debug
            if event.key == pygame.K_F2:
                hitboxes = not hitboxes
            for box in base.TEXTBOXES:
                box.keypress(event)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pos = event.pos
                for box in base.TEXTBOXES:
                    if box.rect.collidepoint(pos) and box.visible:
                        box.selected = True
                    else:
                        box.selected = False
                for button in base.BUTTONS:
                    if button.rect.collidepoint(pos) and button.clickable:
                        print(button.text)
                        button.click()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        main_menu_f(True)
        

    win.fill((0, 0, 0))

    for y in range((SCREEN_SIZE[1]+GRASS.get_height()*2)//GRASS.get_height()):
            for x in range((SCREEN_SIZE[0]+GRASS.get_width()*2)//GRASS.get_width()):
                win.blit(GRASS, (x*GRASS.get_width()-(base.PLAYER[0]%GRASS.get_width()), y*GRASS.get_height()-(base.PLAYER[1]%GRASS.get_height())))

    if main_menu:
        text = menu_font.render("Cat Game", 1, (255, 255, 255))
        win.blit(text, (SCREEN_SIZE[0]//2-text.get_width()//2, SCREEN_SIZE[1]//2-text.get_height()//2))
        create_server_b.draw(win)
        join_server_b.draw(win)
        username_t.draw(win)
    elif create_menu:
        text = menu_font.render("Create Server", 1, (255, 255, 255))
        win.blit(text, (SCREEN_SIZE[0]//2-text.get_width()//2, SCREEN_SIZE[1]//2-text.get_height()//2))
        create_confirm_b.draw(win)
        create_name_t.draw(win)
    elif join_menu:
        text = menu_font.render("Join Server", 1, (255, 255, 255))
        win.blit(text, (SCREEN_SIZE[0]//2-text.get_width()//2, SCREEN_SIZE[1]//2-text.get_height()//2))
        join_confirm_b.draw(win)
        join_name_t.draw(win)
    else:

        if keys[pygame.K_w] and keys[pygame.K_s]:
            pass
        elif keys[pygame.K_a] and keys[pygame.K_d]:
            pass
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            cat.move("NE", milli)
        elif keys[pygame.K_w] and keys[pygame.K_a]:
            cat.move("NW", milli)
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            cat.move("SE", milli)
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            cat.move("SW", milli)
        elif keys[pygame.K_w]:
            cat.move("N", milli)
        elif keys[pygame.K_s]:
            cat.move("S", milli)
        elif keys[pygame.K_a]:
            cat.move("W", milli)
        elif keys[pygame.K_d]:
            cat.move("E", milli)

        if prev_time + 0.2 < time.time():
            update()
            prev_time = time.time()

        for player in OTHER_PLAYERS:
            player_drawer.draw(win, player.x, player.y, player.direction, player.username)

        for obj in base.OBJECTS:
            obj.draw(win)
            
        if hitboxes:
            for obj in base.OBJECTS:
                obj.draw_hitbox(win)

        if debug:
            text = debug_font.render(f"Cat Game: version {VERSION}", 1, (255, 255, 255))
            win.blit(text, (0, 0))
            text = debug_font.render(f"FPS: {round(clock.get_fps())}", 1, (255, 255, 255))
            win.blit(text, (0, 30))
            text = debug_font.render(f"Coords: ({base.PLAYER[0]}, {base.PLAYER[1]})", 1, (255, 255, 255))
            win.blit(text, (0, 60))
            text = debug_font.render(f"Objects: {len(base.OBJECTS)}", 1, (255, 255, 255))
            win.blit(text, (0, 90))

    pygame.display.update()

pygame.quit()