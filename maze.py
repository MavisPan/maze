from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = "left"
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= win_width - 85:
            self.direction = "left"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x=wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Maze')
background = transform.scale(image.load('background.jpg'), (win_width, win_height))
font.init()
font = font.Font(None, 100)
win = font.render('You Win! :>', True, (255,200,10))
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

FPS = 360
clock = time.Clock()
game = True
finish = False
player = Player('hero.png', 50, 50, 2)
enemy = Enemy('cyborg.png', 500, 250, 1)
treasure = GameSprite('treasure.png', 500, 400, 20)
wall_1 = Wall(200, 255, 179, 200, 0, 30, 350)
wall_2 = Wall(200, 255, 179, 200, 150, 130, 10)
wall_3 = Wall(200, 255, 179, 420, 70, 30, 500)
wall_4 = Wall(200, 255, 179, 420, 180, 150, 10)

while game:  
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background,(0,0))
        wall_1.draw_wall()
        wall_2.draw_wall()
        wall_3.draw_wall()
        wall_4.draw_wall()
        player.update()
        player.reset()
        enemy.update()
        enemy.reset()
  
        treasure.reset()
        
        if sprite.collide_rect(player, treasure):
            window.blit(win, (200,200))
            finish = True
        if sprite.collide_rect(player, enemy) or sprite.collide_rect(player, wall_1) or sprite.collide_rect(player, wall_2) or sprite.collide_rect(player, wall_3) or sprite.collide_rect(player, wall_4):
            finish = True
    display.update()
    clock.tick(FPS)
    