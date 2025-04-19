# Подключаем библиотеки
from pygame import *
from random import randint

# Создаем окно
win_width = 900
win_height = 700
window = display.set_mode((win_width,win_height))
display.set_caption("Space shooter")
# Запускаем музыку
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
shot = mixer.Sound('fire.ogg')
# Создаем фон
#background = image.load('galaxy.jpg')
#background = transform.scale(background, (win_width, win_height))


# Создаем объект часы для задания кадров
clock = time.Clock()
FPS = 60
#создаем переменные проекта
lost = 0
score = 0
#Создадим стиль шрифта для счетчиков
font.init()
font_game = font.SysFont("Arial", 32)
font_finish = font.SysFont("Arial", 80)
win = font_finish.render('П О Б Е Д А !', True, (255,255,255))
lose = font_finish.render('П О Р А Ж Е Н И Е !', True, (180,0,0))

#Создаем общий класс для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, 
                player_width, player_height, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), 
                                        (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Background():
    def __init__(self, picture, w_x, w_y, w_width, w_height):
        self.image = image.load(picture)
        self.image = transform.scale(self.image, (w_width, 2250))
        self.width = w_width
        self.height = w_height
        self.rect_1 = self.image.get_rect()
        self.rect_1.x = 0
        self.rect_1.y = 0
        self.rect_2 = self.image.get_rect()
        self.rect_2.x = 0
        self.rect_2.y = -w_height
        self.move = 2
    def update(self):
        self.rect_1.y += self.move
        if self.rect_1.y > self.height:
            self.rect_1.y = -self.height
        self.rect_2.y += self.move
        if self.rect_2.y > self.height:
            self.rect_2.y = -self.height
    def draw(self):
        window.blit(self.image, (self.rect_1.x, self.rect_1.y))
        window.blit(self.image, (self.rect_2.x, self.rect_2.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x < win_width - 85:
            self.rect.x += self.speed
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_width:
            self.rect.y = -50
            self.rect.x = randint(0, win_width - 80)
            lost += 1

class Bullet(GameSprite):
    def update(self):
       self.rect.y += self.speed
       if self.rect.y < 0:
           self.kill() 

# Загружаем персонажей
back = Background('galaxy_best1.jpg', 0, 0, win_width, win_height)
ship = Player('rocket.png', win_width // 2, win_height - 120, 80, 120, 10)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(0, win_width - 80), -50, 80, 50, randint(1,5))
    monsters.add(monster)
bullets = sprite.Group()

# Создаем игровой цикл
run = True
finish = False
while run:  
    # Проверка событий на выход
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                shot.play()
                ship.fire()
    
    if not finish:
        #window.blit(background, (0,0))
        back.update()
        back.draw()
        
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(0, win_width - 80), -50, 80, 50, randint(1,5))
            monsters.add(monster)
        
        if sprite.spritecollide(ship, monsters, False) or lost >= 5:
            finish = True
            window.blit(lose, (200,330))           

        if score >= 10:
            finish = True
            window.blit(win, (280,330))  

        text_score = font_game.render("Счет: " + str(score), True, (255,255,255))
        window.blit(text_score, (10,10))
        text_lost = font_game.render("Пропущено: " + str(lost), True, (255,255,255))
        window.blit(text_lost, (10,40))
    

    # Обновление экрана 
    display.update()
    clock.tick(FPS)

