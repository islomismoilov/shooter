#Создай собственный Шутер!
from pygame import *
win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
clock = time.Clock()
display.set_caption('Shooter')
background =transform.scale(image.load('galaxy.jpg'),(win_width,win_height))

mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
# lost_music = mixer.Sound('mixkit-arcade-retro-changing-tab-206.wav')
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(
            image.load(player_image),(player_width,player_height)
        )
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys =key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -=self.speed
        if keys[K_RIGHT] and self.rect.x < win_width -65:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,15)
        bullets.add(bullet)
        
from random import randint
lost = 0
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height -80:
            lost +=1
            self.rect.y = 0
            self.rect.x = randint(80,win_width-80)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self .rect.y < 0:
            self.kill()
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80,win_width-80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

player = Player('rocket.png', win_width/2,win_height-100,60,100,10)
game = True
FPS = 60
score = 0
font.init()

while game:
    window.blit(background,(0,0))
    score_label = font.Font(None, 40).render(f'Счёт: {score}',
                                                1,(255,255,255))
    window.blit(score_label,(10,20))
    lost_label = font.Font(None, 40).render(f'Пропущено: {lost}',
                                                1,(255,255,255))
    window.blit(lost_label,(10,50))
    player.reset()
    player.update()
    monsters.update()
    monsters.draw(window)
    bullets.draw(window)
    bullets.update()
    collides = sprite.groupcollide(bullets, monsters, True, True)
    for c in collides:
        score += 1
        monster = Enemy('ufo.png',randint(80,win_width-80),-40, 80, 50, randint(1,5))
        monsters.add(monster)
    if score >= 20:
        finish = True
        win = font.Font(None,70).render('YOU WIN!',1,(255,255.255))
        window.blit(win,(200,200))
    if sprite.spritecollide(player, monsters, False) or lost >=5:
        finish = True
        lose = font.Font(None,70).render('YOU LOSE!',1,(255,100,100))
        window.blit(lose,(200,200))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type  == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    display.update()
    clock.tick(FPS)