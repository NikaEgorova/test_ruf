import pygame
import math
import random

pygame.init()

screenw = 1000
screenh = 700

bg = pygame.image.load('asteroidsPics/background.jpg')
playerRocket = pygame.image.load('asteroidsPics/rocket.png')
star = pygame.image.load('asteroidsPics/R2D2.png')
star_ship = pygame.image.load('asteroidsPics/star_ship.png')
star_det = pygame.image.load('asteroidsPics/star_det1.png')
star_det1 = pygame.image.load('asteroidsPics/star_det.png')
hp = pygame.image.load('asteroidsPics/HP.png')

shoot = pygame.mixer.Sound('sounds/laser.wav')
bangLargeSound = pygame.mixer.Sound('sounds/banglarge.wav')
bangSmallSound = pygame.mixer.Sound('sounds/bangSmall.wav')
shoot.set_volume(.20)
bangLargeSound.set_volume(.20)
bangSmallSound.set_volume(.20)

pygame.display.set_caption('Star Wars')
win = pygame.display.set_mode((screenw, screenh))
clock = pygame.time.Clock()

gameover = False
lives = 3
score = 0
rapidFire = False
rfStart = -1
isSoundOn = True
highScore = 0


class Player(object):
    def __init__(self):
        self.img = playerRocket
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = screenw//2
        self.y = screenh//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def draw(self, win):
        win.blit(self.rotatedSurf, self.rotatedRect)

    def turnLeft(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def turnRight(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def moveForward(self):
        self.x += self.cosine * 5
        self.y -= self.sine * 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def updateLocation(self):
        if self.x > screenw + 5:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = screenw
        elif self.y < -50:
            self.y = screenh
        elif self.y > screenh + 50:
            self.y = 0

class Bullet(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0),[self.x, self.y, 3, 3]) 

    def checkOffScreen(self):
        if self.x < -50 or self.x > screenw or self.y > screenh or self.y < -50:
            return True

class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = star_ship
        elif self.rank == 2:
            self.image = star_det1
        else:
            self.image = star_det
        self.w = 30 * rank
        self.h = 30 * rank
        self.ranPoint = random.choice([(random.randrange(0, screenw-self.w), random.choice([-1*self.h - 5, screenh + 5])), (random.choice([-1*self.w - 5, screenw + 5]), random.randrange(0, screenw - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < screenw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < screenh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1,4)
        self.yv = self.ydir * random.randrange(1,4)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

class Star(object):
    def __init__(self):
        self.img = star
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, screenw - self.w), random.choice([-1 * self.h - 5, screenh + 5])),
                                       (random.choice([-1 * self.w - 5, screenw + 5]), random.randrange(0, screenh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < screenw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < screenh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


def redrawGameWindow():
    win.blit(bg, (0,0))
    font = pygame.font.SysFont('arial',30)
    font2 = pygame.font.SysFont('arial',60)
    livesText = font.render(str(lives), 1, (255, 255, 255))
    win.blit(hp, (10,10))
    playAgainText = font2.render('Натисни E, щоб продовжити.', 1, (255,255,255))
    playExitText = font2.render('Натисни Q або ESCAPE, щоб вийти.', 1, (255,255,255))
    highScoreText = font.render('Очки: ' + str(score), 1, (255, 255, 255))

    player.draw(win)
    for a in asteroids:
        a.draw(win)
    for b in playerBullets:
        b.draw(win)
    for s in stars:
        s.draw(win)


    if gameover:
        win.blit(playAgainText, (200,100))
        win.blit(playExitText,(100,200))
        
    win.blit(livesText, (70, 25))
    win.blit(highScoreText,(20, 75))
    pygame.display.update()



player = Player()
playerBullets = []
asteroids = []
count = 0
stars = []
run = True

while run:
    clock.tick(60)
    count += 1
    if not gameover:
        if score >= 0 and count % 50 == 0:
            ran = random.choice([1,1,1])
            asteroids.append(Asteroid(ran))
        if score >= 150 and count % 150 ==0:
            ran = random.choice([2,2])
            asteroids.append(Asteroid(ran))
        if score >= 500 and count % 500 == 0:
            ran = random.choice([3])
            asteroids.append(Asteroid(ran))
            
        if score == 1000 and count % 2000 == 0:
            stars.append(Star()) 
        

            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    #if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        #aliens.pop(i)
                        if isSoundOn:
                            bangLargeSound.play()
                        score += 50
                        break

        

        player.updateLocation()
        for b in playerBullets:
            b.move()
            if b.checkOffScreen():
                playerBullets.pop(playerBullets.index(b))


        for a in asteroids:
            a.x += a.xv
            a.y += a.yv

            if (a.x >= player.x - player.w//2 and a.x <= player.x + player.w//2) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
                if(a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or (a.y  +a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    if isSoundOn:
                        bangLargeSound.play()
                    break

            
            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        if a.rank == 3:
                            if isSoundOn:
                                bangLargeSound.play()
                            score += 10
                            na1 = Asteroid(2)
                            na2 = Asteroid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            if isSoundOn:
                                bangSmallSound.play()
                            score += 20
                            na1 = Asteroid(1)
                            na2 = Asteroid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score += 30
                            if isSoundOn:
                                bangSmallSound.play()
                        asteroids.pop(asteroids.index(a))
                        playerBullets.pop(playerBullets.index(b))
                        break

        for s in stars:
            s.x += s.xv
            s.y += s.yv
            if s.x < -100 - s.w or s.x > screenw + 100 or s.y > screenh + 100 or s.y < -100 - s.h:
                stars.pop(stars.index(s))
                break
            for b in playerBullets:
                if (b.x >= s.x and b.x <= s.x + s.w) or b.x + b.w >= s.x and b.x + b.w <= s.x + s.w:
                    if (b.y >= s.y and b.y <= s.y + s.h) or b.y + b.h >= s.y and b.y + b.h <= s.y + s.h:
                        rapidFire = True
                        rfStart = count
                        stars.pop(stars.index(s))
                        playerBullets.pop(playerBullets.index(b))
                        break

        if lives <= 0:
            gameover = True

        if rfStart != -1:
            if count - rfStart > 500:
                rapidFire = False
                rfStart = -1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
            run = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.turnLeft()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.turnRight()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.moveForward()
        if keys[pygame.K_SPACE]:
            if rapidFire:
                playerBullets.append(Bullet())
                if isSoundOn:
                    shoot.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    if not rapidFire:
                        playerBullets.append(Bullet())
                        if isSoundOn:
                            shoot.play()
            
            if event.key == pygame.K_e:
                if gameover:
                    gameover = False
                    lives = 3
                    asteroids.clear()
                    stars.clear()
                    if score > highScore:
                        highScore = score
                    score = 0
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                run = False       

    redrawGameWindow()
pygame.quit()
pygame.Surface