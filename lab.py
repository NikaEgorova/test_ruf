from pygame import *
 
#клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
 #конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
     # Викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
     #кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
 
     #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 #метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
 
class Player(GameSprite):
 #метод, у якому реалізовано управління спрайтом за кнопками стрілочкам клавіатури
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
     # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    
    ''' переміщає персонажа, застосовуючи поточну горизонтальну та вертикальну швидкість'''
    def update(self):
        # Спершу рух по горизонталі
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
 
#Створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Лабіринт")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223) # задаємо колір відповідно до колірної схеми RGB
 
#Створюємо стіни картинки
w1 = GameSprite('platform2.png',win_width/2 - win_width/3, win_height/2, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)
 
#створюємо спрайти
packman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
 
#ігровий цикл
run = True
while run:
 #цикл спрацьовує кожну 0.05 секунд
    time.delay(50)
    window.fill(back)#зафарбовуємо вікно кольором
 
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
 #малюємо об'єкти
    w1.reset()
    w2.reset()
    packman.reset()
 
    #включаємо рух
    packman.update()
 
    display.update()