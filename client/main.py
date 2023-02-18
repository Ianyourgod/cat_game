import pygame
import base
import requests
import time
import os
import socket   

ABS_PATH = os.path.dirname(os.path.abspath(__file__))

def resource_path(relative_path):
    return 'assets/' + relative_path

pygame.init()

FPS = 1000
SCREEN_SIZE = (500,500)
VERSION = "0.0.5"
SERVER_IP = socket.gethostbyname(socket.gethostname())
SERVER_NAME = ""
OTHER_PLAYERS = []
Host = False

HOW_MANY_UPDATES_PER_SECOND = 20
DELAY = 1 / HOW_MANY_UPDATES_PER_SECOND

win = pygame.display.set_mode(SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Cat Game :3")

clock = pygame.time.Clock()

cat = base.Player(win, 50, 50, 5, resource_path("images/cat/N_I.png"), resource_path("images/cat/NE_I.png"), resource_path("images/cat/E_I.png"), resource_path("images/cat/SE_I.png"), resource_path("images/cat/S_I.png"), resource_path("images/cat/SW_I.png"), resource_path("images/cat/W_I.png"), resource_path("images/cat/NW_I.png"))

box = base.Object(-100, -100, 200, 200, image=resource_path("images/tiles/trashtree.gif"), collision=False)
box_hit = base.Object(-32, 80, 63, 20, (255, 0, 0), visible=False)

GRASS = pygame.transform.scale(pygame.image.load(resource_path("images/tiles/grass.png")).convert(), (32, 32))


debug = False
main_menu = True
create_menu = False
join_menu = False
hitboxes = False


debug_font = pygame.font.SysFont("ariel", 30)
menu_font = pygame.font.Font(resource_path("fonts/Eight-Bit Madness.ttf"), 30)

def create_server():
    name = create_name_t.text
    username = username_t.text
    data = requests.post(f"http://{SERVER_IP}:5000/create", json={"name": username, "room": name}).json()
    if data['success']:
        global create_menu, SERVER_NAME, Host
        create_menu = False
        create_confirm_b.visible = False
        create_confirm_b.clickable = False
        create_name_t.selected = False
        create_name_t.visible = False
        create_name_t.text = ""
        SERVER_NAME = name
        Host = True

def create_server_button():
    global main_menu, create_menu
    main_menu = False
    create_menu = True
    join_server_b.visible = False
    create_server_b.visible = False
    create_confirm_b.visible = True
    create_confirm_b.clickable = True
    create_name_t.visible = True
    username_t.selected = False
    username_t.visible = False

        
def join_server():
    name = join_name_t.text
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
        username_t.selected = False
        username_t.visible = False
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
    username_t.selected = False
    username_t.visible = False
        
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
    join_name_t.visible = False
    join_name_t.text = ""
    join_confirm_b.visible = False
    join_confirm_b.clickable = False
    username_t.visible = True  
    
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
    elif data['message'] == 'Room not found.':
        main_menu_f(True)
    else:
        print("Failed to update")

    
username_t = base.Textbox(win.get_width()/2-100, win.get_height()/2+115, 200, 50, (255, 255, 255), menu_font, "Username...", selected_image=resource_path("images/textures/textbox/Textbox_selected.png"), unselected_image=resource_path("images/textures/textbox/Textbox_unselected.png"),)

create_server_b = base.Button(win.get_width()/2-50, win.get_height()/2+50, 100, 50, "Create", 50, (0, 0, 0), menu_font, image=resource_path("images/textures/stone_button.png"), click=create_server_button)
create_name_t = base.Textbox(win.get_width()/2-100, win.get_height()/2+50, 200, 50, (255, 255, 255), menu_font, "Server name...", selected_image=resource_path("images/textures/textbox/Textbox_selected.png"), unselected_image=resource_path("images/textures/textbox/Textbox_unselected.png"), visible=False)
create_confirm_b = base.Button(win.get_width()/2-50, win.get_height()/2+120, 100, 50, "Confirm", (255, 255, 255), (0, 0, 0), menu_font, image=resource_path("images/textures/stone_button.png"), click=create_server, clickable=False, visible=False)

join_server_b = base.Button(win.get_width()/2-50, win.get_height()/2+180, 100, 50, "Join", (255, 255, 255), (0, 0, 0), menu_font, image=resource_path("images/textures/stone_button.png"), click=join_server_button)
join_name_t = base.Textbox(win.get_width()/2-100, win.get_height()/2+50, 200, 50, (255, 255, 255), menu_font, "Server name...", selected_image=resource_path("images/textures/textbox/Textbox_selected.png"), unselected_image=resource_path("images/textures/textbox/Textbox_unselected.png"), visible=False)
join_confirm_b = base.Button(win.get_width()/2-50, win.get_height()/2+120, 100, 50, "Confirm", (255, 255, 255), (0, 0, 0), menu_font, image=resource_path("images/textures/stone_button.png"), click=join_server, clickable=False, visible=False)


main_menu_f(True)

player_drawer = base.OtherPlayerDrawer()

prev_time = time.time()
run = True
while run:
    milli = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if Host:
                requests.post(f"http://{SERVER_IP}:5000/close", json={"name": username_t.text, "room": SERVER_NAME})
            else:
                requests.post(f"http://{SERVER_IP}:5000/leave", json={"name": username_t.text, "room": SERVER_NAME})
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
                        button.click()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        if Host:
            requests.post(f"http://{SERVER_IP}:5000/close", json={"name": username_t.text, "room": SERVER_NAME})
        else:
            requests.post(f"http://{SERVER_IP}:5000/leave", json={"name": username_t.text, "room": SERVER_NAME})
        main_menu_f(True)

    win.fill((0, 0, 0))

    for y in range((win.get_height()+GRASS.get_height()*2)//GRASS.get_height()):
            for x in range((win.get_width()+GRASS.get_width()*2)//GRASS.get_width()):
                win.blit(GRASS, (x*GRASS.get_width()-(base.PLAYER[0]%GRASS.get_width()), y*GRASS.get_height()-(base.PLAYER[1]%GRASS.get_height())))

    if main_menu:
        username_t.x = win.get_width()/2-100
        username_t.y = win.get_height()/2+115
        create_server_b.x = win.get_width()/2-50
        create_server_b.y = win.get_height()/2+50
        join_server_b.x = win.get_width()/2-50
        join_server_b.y = win.get_height()/2+180
        text = menu_font.render("Cat Game", 1, (255, 255, 255))
        win.blit(text, (win.get_width()//2-text.get_width()//2, win.get_height()//2-text.get_height()//2))
        create_server_b.draw(win)
        join_server_b.draw(win)
        username_t.draw(win)
    elif create_menu:
        create_name_t.x = win.get_width()/2-100
        create_name_t.y = win.get_height()/2+50
        create_confirm_b.x = win.get_width()/2-50
        create_confirm_b.y = win.get_height()/2+120
        text = menu_font.render("Create Server", 1, (255, 255, 255))
        win.blit(text, (win.get_width()//2-text.get_width()//2, win.get_height()//2-text.get_height()//2))
        create_confirm_b.draw(win)
        create_name_t.draw(win)
    elif join_menu:
        join_name_t.x = win.get_width()/2-100
        join_name_t.y = win.get_height()/2+50
        join_confirm_b.x = win.get_width()/2-50
        join_confirm_b.y = win.get_height()/2+120
        text = menu_font.render("Join Server", 1, (255, 255, 255))
        win.blit(text, (win.get_width()//2-text.get_width()//2, win.get_height()//2-text.get_height()//2))
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

        if prev_time + DELAY < time.time():
            update()
            prev_time = time.time()

        for player in OTHER_PLAYERS:
            player_drawer.draw(win, player['x'], player['y'], player['direction'], player['username'])

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