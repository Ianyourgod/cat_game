import pygame

PLAYER = [0,0]

OBJECTS = []

class Object:
    def __init__(self, x, y, width, height, color: tuple|None =None, image: str|None =None) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

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
        if self.color:
            pygame.draw.rect(win, self.color, (self.x-PLAYER[0], self.y-PLAYER[1], self.width, self.height))
        elif self.image:
            win.blit(self.image, (self.x, self.y))

    def collide(self, obj) -> bool:
        if self.x + self.width > obj.x and self.x < obj.x + obj.width:
            if self.y + self.height > obj.y and self.y < obj.y + obj.height:
                print(self.x, obj.x)
                return True
        return False


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

    def move(self, direction: str) -> None:
        if direction == "N":
            self.y -= self.speed
            self.image = self.N_I
        elif direction == "NE":
            self.x += self.speed
            self.y -= self.speed
            self.image = self.NE_I
        elif direction == "E":
            self.x += self.speed
            self.image = self.E_I
        elif direction == "SE":
            self.x += self.speed
            self.y += self.speed
            self.image = self.SE_I
        elif direction == "S":
            self.y += self.speed
            self.image = self.S_I
        elif direction == "SW":
            self.x -= self.speed
            self.y += self.speed
            self.image = self.SW_I
        elif direction == "W":
            self.x -= self.speed
            self.image = self.W_I
        elif direction == "NW":
            self.x -= self.speed
            self.y -= self.speed
            self.image = self.NW_I
        for obj in OBJECTS:
            if obj != self:
                if self.collide(obj):
                    if direction == "N":
                        self.y += self.speed
                    elif direction == "NE":
                        self.x -= self.speed
                        self.y += self.speed
                    elif direction == "E":
                        self.x -= self.speed
                    elif direction == "SE":
                        self.x -= self.speed
                        self.y -= self.speed
                    elif direction == "S":
                        self.y -= self.speed
                    elif direction == "SW":
                        self.x += self.speed
                        self.y -= self.speed
                    elif direction == "W":
                        self.x += self.speed
                    elif direction == "NW":
                        self.x += self.speed
                        self.y += self.speed
                    break


class Player(Cat):
    def __init__(self, win: pygame.Surface, width, height, speed: float|int, N_I: str, NE_I: str, E_I: str, SE_I: str, S_I: str, SW_I: str, W_I: str, NW_I: str) -> None:
        super().__init__(win.get_width()//2-width/2, win.get_height()//2-height/2, width, height, speed, N_I, NE_I, E_I, SE_I, S_I, SW_I, W_I, NW_I)
        self.extra = [win.get_width()//2-width/2, win.get_height()//2-height/2]
    def move(self, direction: str) -> None:
        super().move(direction)
        PLAYER[0] = self.x - self.extra[0]
        PLAYER[1] = self.y - self.extra[1]

    def draw(self, win: pygame.Surface) -> None:
        win.blit(self.image, (win.get_width()//2-self.width/2, win.get_height()//2-self.height/2))