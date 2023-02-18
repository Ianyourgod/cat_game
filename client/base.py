import pygame
import os

ABS_PATH = os.path.dirname(os.path.abspath(__file__))

def resource_path(relative_path):
    return 'assets/' + relative_path


def null():
    return

PLAYER = [0,0]

BUTTONS = []

OBJECTS = []

TEXTBOXES = []

class Object:
    def __init__(self, x, y, width, height, color: tuple|None =None, image: str|None = None, collision: bool = True, visible=True) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.visible = visible

        self.collision = collision

        self.color = None
        self.image = None

        if color and image:
            raise Exception("Cannot have both color and image")
        elif color:
            self.color = color
        elif image:
            self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (width, height))
        else:
            raise Exception("Must have either color or image")

        OBJECTS.append(self)

    def draw(self, win: pygame.Surface) -> None:
        if self.visible:
            if self.color:
                pygame.draw.rect(win, self.color, (self.x-PLAYER[0], self.y-PLAYER[1], self.width, self.height))
            elif self.image:
                win.blit(self.image, (self.x-PLAYER[0], self.y-PLAYER[1]))

    def collide(self, obj) -> bool:
        if self.collision and obj.collision:
            if self.x + self.width > obj.x and self.x < obj.x + obj.width:
                if self.y + self.height > obj.y and self.y < obj.y + obj.height:
                    return True
        return False

    def draw_hitbox(self, win: pygame.Surface) -> None:
        if self.collision:
            pygame.draw.rect(win, (230, 230, 230), (self.x-PLAYER[0], self.y-PLAYER[1], self.width, self.height), 2)


class Cat(Object):
    def __init__(self, x, y, width, height, speed: float|int, N_I: str, NE_I: str, E_I: str, SE_I: str, S_I: str, SW_I: str, W_I: str, NW_I: str) -> None:
        super().__init__(x, y, width, height, image=N_I)
        
        self.speed = speed
        
        self.color = None

        self.N_I = pygame.transform.scale(pygame.image.load(N_I).convert_alpha(), (width, height))
        self.NE_I = pygame.transform.scale(pygame.image.load(NE_I).convert_alpha(), (width, height))
        self.E_I = pygame.transform.scale(pygame.image.load(E_I).convert_alpha(), (width, height))
        self.SE_I = pygame.transform.scale(pygame.image.load(SE_I).convert_alpha(), (width, height))
        self.S_I = pygame.transform.scale(pygame.image.load(S_I).convert_alpha(), (width, height))
        self.SW_I = pygame.transform.scale(pygame.image.load(SW_I).convert_alpha(), (width, height))
        self.W_I = pygame.transform.scale(pygame.image.load(W_I).convert_alpha(), (width, height))
        self.NW_I = pygame.transform.scale(pygame.image.load(NW_I).convert_alpha(), (width, height))

        self.direction = "N"

    def move(self, direction: str, milli: int|float) -> None:
        self.direction = direction
        speed = self.speed * (milli/16)
        if direction == "N" or direction == "NE" or direction == "NW":
            if direction == "N":
                self.y -= speed
                self.image = self.N_I
            elif direction == "NE":
                self.y -= speed/2
                self.image = self.NE_I
            elif direction == "NW":
                self.y -= speed/2
                self.image = self.NW_I
            for i in OBJECTS:
                if self.collide(i) and i != self:
                    self.y += speed
                    break
        if direction == "S" or direction == "SE" or direction == "SW":
            if direction == "S":
                self.y += speed
                self.image = self.S_I
            elif direction == "SE":
                self.y += speed/2
                self.image = self.SE_I
            elif direction == "SW":
                self.y += speed/2
                self.image = self.SW_I
            for i in OBJECTS:
                if self.collide(i) and i != self:
                    self.y -= speed
                    break
        if direction == "E" or direction == "NE" or direction == "SE":
            if direction == "E":
                self.x += speed
                self.image = self.E_I
            elif direction == "NE":
                self.x += speed/2
                self.image = self.NE_I
            elif direction == "SE":
                self.x += speed/2
                self.image = self.SE_I
            for i in OBJECTS:
                if self.collide(i) and i != self:
                    self.x -= speed
                    break
        if direction == "W" or direction == "NW" or direction == "SW":
            if direction == "W":
                self.x -= speed
                self.image = self.W_I
            elif direction == "NW":
                self.x -= speed/2
                self.image = self.NW_I
            elif direction == "SW":
                self.x -= speed/2
                self.image = self.SW_I
            for i in OBJECTS:
                if self.collide(i) and i != self:
                    self.x += speed
                    break


class Player(Cat):
    def __init__(self, win: pygame.Surface, width, height, speed: float|int, N_I: str, NE_I: str, E_I: str, SE_I: str, S_I: str, SW_I: str, W_I: str, NW_I: str) -> None:
        super().__init__(win.get_width()//2-width/2, win.get_height()//2-height/2, width, height, speed, N_I, NE_I, E_I, SE_I, S_I, SW_I, W_I, NW_I)
        self.extra = [win.get_width()//2-width/2, win.get_height()//2-height/2]
    def move(self, direction: str, milli: int|float) -> None:
        super().move(direction, milli)
        PLAYER[0] = self.x - self.extra[0]
        PLAYER[1] = self.y - self.extra[1]

    def draw(self, win: pygame.Surface) -> None:
        win.blit(self.image, (win.get_width()//2-self.width/2, win.get_height()//2-self.height/2))
        
        
class Button(Object):
    def __init__(self, x, y, width, height, text: str, text_size: int, text_color: tuple, font:pygame.font.Font, color: tuple | None = None, image: str | None = None, visible: bool = True, click = null, clickable:bool=True) -> None:
        super().__init__(x, y, width, height, color, image, False, visible)
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.font = font
        self.click = click
        self.clickable = clickable
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        BUTTONS.append(self)

    def draw(self, win: pygame.Surface) -> None:
        if not self.visible:
            return
        if self.color:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        if self.image:
            win.blit(self.image, (self.x, self.y))
        text = self.font.render(self.text, True, self.text_color)
        win.blit(text, (self.x+self.width/2-text.get_width()/2, self.y+self.height/2-text.get_height()/2))
        
        
class Text(Object):
    def __init__(self, x, y, text: str, text_size: int, text_color: tuple, font:pygame.font.Font, color: tuple | None = None, image: str | None = None, visible: bool = True) -> None:
        super().__init__(x, y, 0, 0, color, image, False, visible)
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.font = font
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win: pygame.Surface) -> None:
        if not self.visible:
            return
        if self.color:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        if self.image:
            win.blit(self.image, (self.x, self.y))
        text = self.font.render(self.text, True, self.text_color)
        win.blit(text, (self.x, self.y))
        

class Textbox(Object):
    def __init__(self, x: int|float, y: int|float, width: int|float, height: int|float, text_color: tuple, font: pygame.font.Font, placeholder: str = "", unselected_color: tuple = None, selected_color: tuple=None, unselected_image: str | None = None, selected_image: str | None = None, image: str|None = None, visible: bool = True) -> None:
        if unselected_image and selected_image:
            image = unselected_image
        super().__init__(x, y, width, height, unselected_color, image, False, visible)
        self.text_color = text_color
        self.font = font
        self.placeholder = placeholder
        self.unselected_color = unselected_color
        self.selected_color = selected_color
        self.selected_image = None
        self.unselected_image = None
        if selected_image and unselected_image:
            self.unselected_image = pygame.transform.scale(pygame.image.load(unselected_image).convert_alpha(), (self.width, self.height))
            self.selected_image = pygame.transform.scale(pygame.image.load(selected_image).convert_alpha(), (self.width, self.height))
        self.text = ""
        self.selected = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        OBJECTS.remove(self)
        TEXTBOXES.append(self)
    def draw(self, win: pygame.Surface):
        if not self.visible:
            return
        if self.selected:
            if self.selected_color:
                pygame.draw.rect(win, self.selected_color, (self.x, self.y, self.width, self.height))
            if self.selected_image:
                win.blit(self.selected_image, (self.x, self.y))
            if self.image:
                win.blit(self.image, (self.x, self.y))
        else:
            if self.unselected_color:
                pygame.draw.rect(win, self.unselected_color, (self.x, self.y, self.width, self.height))
            if self.unselected_image:
                win.blit(self.unselected_image, (self.x, self.y))
            if self.image:
                win.blit(self.image, (self.x, self.y))
        if self.text == "" and not self.selected:
            text = self.font.render(self.placeholder, True, self.text_color)
        else:
            text = self.font.render(self.text, True, self.text_color)
        win.blit(text, (self.x+self.width/2-text.get_width()/2, self.y+self.height/2-text.get_height()/2))
    
    def keypress(self, event):
        if self.selected:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                return
            if event.key == pygame.K_RETURN:
                self.selected = False
                return
            if event.key == pygame.K_TAB:
                self.selected = False
                return
            if event.key == pygame.K_ESCAPE:
                self.selected = False
                return
            if event.key == pygame.K_ESCAPE:
                self.selected = False
                return
            self.text += event.unicode


class OtherPlayerDrawer:
    def __init__(self):
        self.font = pygame.font.Font(resource_path("fonts/Eight-Bit Madness.ttf"), 30)

        N_I, NE_I, E_I, SE_I, S_I, SW_I, W_I, NW_I = resource_path("images/cat/N_I.png"), resource_path("images/cat/NE_I.png"), resource_path("images/cat/E_I.png"), resource_path("images/cat/SE_I.png"), resource_path("images/cat/S_I.png"), resource_path("images/cat/SW_I.png"), resource_path("images/cat/W_I.png"), resource_path("images/cat/NW_I.png")
        
        width, height = 50, 50

        self.N_I = pygame.transform.scale(pygame.image.load(N_I).convert_alpha(), (width, height))
        self.NE_I = pygame.transform.scale(pygame.image.load(NE_I).convert_alpha(), (width, height))
        self.E_I = pygame.transform.scale(pygame.image.load(E_I).convert_alpha(), (width, height))
        self.SE_I = pygame.transform.scale(pygame.image.load(SE_I).convert_alpha(), (width, height))
        self.S_I = pygame.transform.scale(pygame.image.load(S_I).convert_alpha(), (width, height))
        self.SW_I = pygame.transform.scale(pygame.image.load(SW_I).convert_alpha(), (width, height))
        self.W_I = pygame.transform.scale(pygame.image.load(W_I).convert_alpha(), (width, height))
        self.NW_I = pygame.transform.scale(pygame.image.load(NW_I).convert_alpha(), (width, height))

    def draw(self, win: pygame.Surface, x, y, dir, name):
        if dir == "N":
            win.blit(self.N_I, (x-PLAYER[0], y-PLAYER[1]))
        elif dir == "NE":
            win.blit(self.NE_I, (x-PLAYER[0], y-PLAYER[1]))
        elif dir == "E":
            win.blit(self.E_I, (x-PLAYER[0], y-PLAYER[1]))
        elif dir == "SE":
            win.blit(self.SE_I, (x-PLAYER[0], y-PLAYER[1]))
        elif dir == "S":
            win.blit(self.S_I, (x-PLAYER[0], y-PLAYER[1]))
        elif dir == "SW":
            win.blit(self.SW_I, (x-PLAYER[0], y-PLAYER[1]))
        elif dir == "W":
            win.blit(self.W_I, (x-PLAYER[0], y-PLAYER[1]))
        elif dir == "NW":
            win.blit(self.NW_I, (x-PLAYER[0], y-PLAYER[1]))
        else:
            raise Exception("Invalid direction")

        text = self.font.render(name, True, (0, 0, 0))
        win.blit(text, (x-PLAYER[0], y-30-PLAYER[1]))