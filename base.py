import pygame

class Object:
    def __init__(self, x, y, width, height, color: tuple|None =None, image: str|None =None) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        if self.color and self.image:
            raise Exception("Cannot have both color and image")
        elif self.color:
            self.color = color
        elif self.image:
            self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (width, height))
        else:
            raise Exception("Must have either color or image")

    def draw(self, win: pygame.Surface) -> None:
        if self.color:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        elif self.image:
            win.blit(self.image, (self.x, self.y))

    def collide(self, obj) -> bool:
        if self.x + self.width > obj.x and self.x < obj.x + obj.width:
            if self.y + self.height > obj.y and self.y < obj.y + obj.height:
                return True
        return False


class Cat(Object):
    def __init__(self, x, y, width, height, speed: float|int, N_I: str, NE_I: str, E_I: str, SE_I: str, S_I: str, SW_I: str, W_I: str, NW_I: str) -> None:
        super().__init__(x, y, width, height, image=N_I)
        
        self.speed = speed
        
        self.N_I = N_I
        self.NE_I = NE_I
        self.E_I = E_I
        self.SE_I = SE_I
        self.S_I = S_I
        self.SW_I = SW_I
        self.W_I = W_I
        self.NW_I = NW_I

    def move(self, direction: str) -> None:
        if direction == "N":
            self.y -= self.speed
            self.image = self.N_I
        elif direction == "NE":
            self.y -= self.speed
            self.x += self.speed
            self.image = self.NE_I
        elif direction == "E":
            self.x += self.speed
            self.image = self.E_I
        elif direction == "SE":
            self.y += self.speed
            self.x += self.speed
            self.image = self.SE_I
        elif direction == "S":
            self.y += self.speed
            self.image = self.S_I
        elif direction == "SW":
            self.y += self.speed
            self.x -= self.speed
            self.image = self.SW_I
        elif direction == "W":
            self.x -= self.speed
            self.image = self.W_I
        elif direction == "NW":
            self.y -= self.speed
            self.x -= self.speed
            self.image = self.NW_I