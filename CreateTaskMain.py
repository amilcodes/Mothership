import random, os, sys, subprocess
import pygame
pygame.font.init()
PLANE_WIDTH = 1000
PLANE_HEIGHT = 600
BUY_PANEL_HEIGHT = 200
finalMissile = pygame.image.load("finalmissile.png")#http://www.pngmart.com/image/112684
finalMissileMax = pygame.transform.scale(finalMissile, (350,200))
finalMissileMed = pygame.transform.scale(finalMissile, (233,133))
finalMissileMin = pygame.transform.scale(finalMissile, (117,67))

#SOME CODE STRUCTURE FROM LINES 13-37 CITATION:
#***************************************************************************************
#*    Title: Pygame Tutorial - Creating Space Invaders (Space Invaders)
#*    Author: Tim Ruscica
#*    Date: 4/15/20
# *    Code version: Unknown
# *    Availability: YouTube, Link: https://www.youtube.com/watch?v=Q-__8Xw9KTM&ab_channel=TechWithTim
# *
# ***************************************************************************************/
class Missiles:#some code structure in Missiles class by Tim Ruscica at "Tech With Tim", formal citation above
    def __init__(self, x, y, health=2):
        self.x = x
        self.y = y
        self.health = health
        self.missilecooldown = 0
        if health == 3:
            self.missilepng = finalMissileMax
        elif health == 2:
            self.missilepng = finalMissileMed
        elif health == 1:
            self.missilepng = finalMissileMin
        self.mask = pygame.mask.from_surface(self.missilepng)

    def width(self):
        return self.missilepng.get_width()

    def height(self):
        return self.missilepng.get_height()

    def draw(self, screen):
        screen.blit(self.missilepng, (self.x, self.y))

    def move(self, vel):
        self.x += vel

def start():
    global mothership
    mothership = pygame.image.load("finalUFO.png")#https://pngimg.com/image/71661
    mothership = pygame.transform.rotate(mothership, 90)
    mothership = pygame.transform.scale(mothership, (300, 800))

def graphicsMain():
    global notStarted, screen, font, over, paused, points, lives
    over = False
    pygame.init()
    screen = pygame.display.set_mode((PLANE_WIDTH, PLANE_HEIGHT + BUY_PANEL_HEIGHT))
    font = pygame.font.SysFont("franklingothicheavy", 100)
    clock = pygame.time.Clock()
    timetracker = pygame.time.get_ticks() - 1500
    running = True
    paused = True
    difficulty = 1 #1-10        
    missiles = []
    missileSpeed = 15
    spawnfrequency = 600
    points = 0
    lives = 25
    startScreen()
    def updateMissiles():
        global paused
        screen.blit(pygame.image.load("unnamjghjed.png"), (0, 0))#http://wallpaperpulse.com/stars-desktop-wallpaper
        screen.blit(mothership, (800, 0))
        for missile in missiles:
            missile.draw(screen)
        for missile in missiles[:]:
            missile.move(missileSpeed)
            if missile.health == 0:
                missiles.remove(missile)
            checkifHit(missiles, 960)

        if lives < 1:
            paused = True
            endScreen()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and over == True:
                pygame.quit()
                subprocess.call(sys.executable + ' "' + os.path.realpath(__file__) + '"')#Line (this line) by Elad Avron
            else:
                if event.type == pygame.QUIT and paused == True:
                    running = False
                if event.type == pygame.QUIT and paused == False:
                    paused = True
                    endScreen()
                if event.type == pygame.MOUSEBUTTONDOWN and paused == True:
                    start()
                    paused = False
                if event.type == pygame.MOUSEBUTTONDOWN and paused == False:
                    clickX, clickY = pygame.mouse.get_pos()
                    checkifHit(missiles, clickX, clickY)
        if not paused:
            updateMissiles()
            drawCounters()

            cooldownchecker = pygame.time.get_ticks()
            if cooldownchecker - timetracker > spawnfrequency:
                timetracker = cooldownchecker
                missile = Missiles(0, random.randint(20, 610), random.randint(1,3))
                missiles.append(missile)
                if spawnfrequency < 600:
                    spawnfrequency -= 1
                else:
                    spawnfrequency -= 10 * difficulty
        pygame.display.flip()
        clock.tick(60)

def checkifHit(listToCheck, hitboxX, hitboxY=1000):
    global lives, points
    if hitboxY >= 1000:
        for missile in listToCheck:
            if missile.x + missile.width() >= hitboxX:
                listToCheck.remove(missile)
                lives -= missile.health
    else:
        for missile in listToCheck:
            hitbox = screen.blit(missile.missilepng, (missile.x, missile.y))
            if hitbox.collidepoint(hitboxX, hitboxY):
                missile.health -= 1
                points += 500
                if missile.health == 2:
                    missile.missilepng = finalMissileMed
                elif missile.health == 1:
                    missile.missilepng = finalMissileMin
                if missile.health != 0:
                    missile.x += 40
                    missile.y += 40

def drawCounters():
    counterFont = pygame.font.SysFont("franklingothicheavy", 40)
    livesCounter = counterFont.render('Lives: ' + str(lives), True, (255, 255, 255))
    pointsCounter = counterFont.render('Points: ' + str(points), True, (255, 255, 255))
    if paused == False:
        screen.blit(livesCounter, (780, 10))
        screen.blit(pointsCounter, (10, 10))

def startScreen():
    screen.blit(pygame.image.load("unnamjghjed.png"), (0, 0))  # http://wallpaperpulse.com/stars-desktop-wallpaper
    title = font.render('Missile Defender', True, (255, 255, 255))
    screen.blit(title, (100, 200))
    counterFont = pygame.font.SysFont("franklingothicheavy", 60)
    instFont = pygame.font.SysFont("Arial", 30)
    instructions = instFont.render('Click on the incoming missiles to destroy and stop them from hitting the ship. '
                                   , True, (255, 255, 255))
    instructions2 = instFont.render('You lose lives if they hit the ship.'
                                    ' The game slowly becomes more difficult! ', True, (255, 255, 255))
    Clicker = counterFont.render('Click to Begin!', True, (255, 255, 255))
    screen.blit(instructions, (80, 400))
    screen.blit(instructions2, (90, 450))
    screen.blit(Clicker, (280, 600))

def endScreen():
    global over
    over = True
    screen.blit(pygame.image.load("unnamjghjed.png"), (0, 0)) # http://wallpaperpulse.com/stars-desktop-wallpaper
    gameOver = font.render('Game Over!', True, (255, 255, 255))
    screen.blit(gameOver, (220, 200))
    instFont2 = pygame.font.SysFont("Arial", 35)
    pointsFont = pygame.font.SysFont("Arial", 70)
    pointsFinal = pointsFont.render('Points: ' + str(points), True, (255, 255, 255))
    screen.blit(pointsFinal, (400 - (12*len(str(points))), 350))
    instructions3 = instFont2.render('Click to play again, or hit the '
                                     'X at the top right to exit!', True, (255, 255, 255))
    screen.blit(instructions3, (175, 450))

if __name__ == '__main__':
    graphicsMain()