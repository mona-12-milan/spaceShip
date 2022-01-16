# 2nd dummy game
import time
import time as T
from pygame import *
font.init()
mixer.init()

winner_text = ""

WIDTH, HEIGHT = 900,500
FPS = 60 # frame per sec is 60

SPACESHIP_WIDTH=55
SPACESHIP_HEIGHT=55
VEL=5

i=0

active = True

yellow_health = 10
red_health = 10

WIN = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Spaceship")


HEALTH_FONT = font.SysFont("comicsans",30)
WINNER_FONT = font.SysFont("comicsans",90)

BULLET_HIT_SOUND = mixer.Sound("Grenade+1.mp3")
BULLET_FIRE_SOUND = mixer.Sound("Gun+Silencer.mp3")

BORDER = Rect(WIDTH/2-5,0,10,HEIGHT)

MAX_BULLETS = 4

red = Rect(675, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
yellow = Rect(225, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

red_bullets = []
yellow_bullets = []



#creating our own event

RED_HIT = USEREVENT + 1
YELLOW_HIT = USEREVENT + 2

#importing images

YELLOW_SPACESHIP_IMAGE = image.load("spaceship_yellow.png")
RED_SPACESHIP_IMAGE = image.load("spaceship_red.png")
BACKGROUND = transform.scale(image.load("space.png"),(WIDTH,HEIGHT))

# resizing and rotating

YELLOW_SPACESHIP = transform.rotate(transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
RED_SPACESHIP = transform.rotate(transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)




def restart():

    global red_bullets
    global yellow_bullets

    red_bullets = []
    yellow_bullets = []

    red.x = 675
    red.y = 250
    yellow.x = 225
    yellow.y = 250

    global yellow_health
    yellow_health=10
    global red_health
    red_health = 10





def draw_winner(text,colour):
    draw_text = WINNER_FONT.render(text,1,colour)
    WIN.blit(draw_text,(WIDTH//2-draw_text.get_width()//2,HEIGHT//2-draw_text.get_height()//2))
    display.update()
    restart()



def draw_window(red, yellow, red_bullets, yellow_bullets,red_health,yellow_health):

    WIN.blit(BACKGROUND,(0,0))
    draw.rect(WIN,"black",BORDER)

    red_health_text = HEALTH_FONT.render("Health : " + str(red_health),1,"white")
    yellow_health_text = HEALTH_FONT.render("Health : " + str(yellow_health),1,"white")
    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))

    WIN.blit(YELLOW_SPACESHIP,(yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x, red.y))

    for bullets in red_bullets:
        bullets.draw()

    for bullets in yellow_bullets:
        bullets.draw()

    display.update()

def handle_yellow_movement(Keys,yellow):
    if Keys[K_a] and yellow.x>0:  # Left
        yellow.x -= VEL

    if Keys[K_w] and yellow.y>0:  # Up
        yellow.y -= VEL

    if Keys[K_d] and yellow.x<BORDER.x-SPACESHIP_WIDTH:  # Right
        yellow.x += VEL

    if Keys[K_s] and yellow.y<HEIGHT-SPACESHIP_HEIGHT:  # Down
        yellow.y += VEL

def handle_red_movement(Keys, red):
    if Keys[K_LEFT] and red.x>BORDER.x+BORDER.width:  # Left
        red.x -= VEL

    if Keys[K_UP] and red.y>0:  # Up
        red.y -= VEL

    if Keys[K_RIGHT] and red.x<WIDTH-SPACESHIP_WIDTH:  # Right
        red.x += VEL

    if Keys[K_DOWN] and red.y<HEIGHT-SPACESHIP_HEIGHT:  # Down
        red.y += VEL

#class for bullets
class Bullets:
    def __init__(self,x,y,w,h,c,f):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.colour=c
        self.facing=f
        self.vel= 10*f

    def draw(self):

        draw.rect(WIN,self.colour, Rect(self.x,self.y,self.w,self.h))



def  handle_bullets(yellow_bullets, red_bullets, red, yellow):

    global active

    for bullets in yellow_bullets:
        bullets.x+=bullets.vel
        if bullets.x > red.x and bullets.x < red.x+SPACESHIP_WIDTH and active:
            if bullets.y > red.y and bullets.y < red.y + SPACESHIP_HEIGHT:
                event.post(event.Event(RED_HIT))
                yellow_bullets.remove(bullets)
        if bullets.x>WIDTH:
            yellow_bullets.remove(bullets)

    for bullets in red_bullets:
        bullets.x+=bullets.vel
        if bullets.x > yellow.x and bullets.x < yellow.x+SPACESHIP_WIDTH and active:
            if bullets.y > yellow.y and bullets.y < yellow.y + SPACESHIP_HEIGHT:
                event.post(event.Event(YELLOW_HIT))
                red_bullets.remove(bullets)
        if bullets.x<0:
            red_bullets.remove(bullets)




def main():

    global yellow_health
    global red_health

    global red_bullets
    global yellow_bullets

    global active
    global i




    run = True

    while run:


        clock = time.Clock()
        clock.tick(FPS)


        for Event in event.get():
            if Event.type == QUIT:
                run = False


            if Event.type == KEYDOWN and active:
                if Event.key == K_LCTRL and len(yellow_bullets) < MAX_BULLETS :
                    bullet = Bullets(yellow.x+SPACESHIP_WIDTH//2 , yellow.y+SPACESHIP_HEIGHT//2,5,5,"yellow",1)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if Event.key == K_RCTRL and len(red_bullets) < MAX_BULLETS :
                    bullet = Bullets(red.x+SPACESHIP_WIDTH//2 , red.y+SPACESHIP_HEIGHT//2,5,5,"red",-1)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            #to reduce the health if collided
            if  Event.type == RED_HIT and active:
                red_health-=1
                BULLET_HIT_SOUND.play()

            if Event.type == YELLOW_HIT and active:
                yellow_health-=1
                BULLET_HIT_SOUND.play()




        if red_health <=0 :
            winner_text = "YELLOW WINS!!!"
            w="yellow"
            draw_winner(winner_text, w)
            active = False

        if yellow_health <= 0:
            winner_text = "RED WINS!!!"
            w="red"
            draw_winner(winner_text, w)
            active = False



        if not active and i<=200:
            draw_winner(winner_text, w)
            print(i)
            print(active)
            i+=1

        if i>=200:
            active = True
            i=0


        if active:
            Keys=key.get_pressed()
            handle_bullets(yellow_bullets,red_bullets,red,yellow)
            handle_yellow_movement(Keys,yellow)
            handle_red_movement(Keys, red)
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)


    quit()

# we can run the game only when we run from this file directly
if __name__ == "__main__":
    main()


