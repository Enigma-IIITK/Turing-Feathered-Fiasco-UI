import  pygame
import os
import random
from time import sleep
pygame.font.init()

WIN_WID = 500
WIN_HEIGHT = 700
SCORE = 0

import pygame
import os

image_folder = "Images"

bird_image_path = os.path.join(image_folder, "Pebbles.png")
Bird_Img = pygame.transform.scale2x(pygame.image.load(bird_image_path))

pipe_image_path = os.path.join(image_folder, "Blue Pipe.jpg")
Pipe_Img = pygame.transform.scale2x(pygame.image.load(pipe_image_path))

base_image_path = os.path.join(image_folder, "Blue Base.png")
Base_Img = pygame.transform.scale2x(pygame.image.load(base_image_path))

bg_image_path = os.path.join(image_folder, "ICE BG.png")
BG_Img = pygame.transform.scale2x(pygame.image.load(bg_image_path))

Blue_Pipe_Img = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "Blue Pipe.jpg")), (100, 170))

STAR = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "coin_try6 (1).png")), (82, 70))

Star_x,Star_y = 0,0

bird_img_scaled = pygame.transform.scale(Bird_Img, (Bird_Img.get_width() * 0.75, Bird_Img.get_height() * 0.75))
bird_Img = bird_img_scaled

Sat_Font = pygame.font.SysFont("timesnewroman",45)


class Bird:
    Img = Bird_Img
    Max_Rotation = 25
    Rot_Vel = 20
    Ani_time = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height =  self.y
        self.img_count = 0
        self.img = self.Img

    def jump(self):
        self.vel = -8.5 
        self.height = self.y
        self.tick_count = 0 

    def move(self):
        self.tick_count += 1
        d = -(self.vel*self.tick_count + 1.5*self.tick_count**2) 

        if(d >= 16): 
            d = 16
        if(d < 0):
            d -= 2
        
        self.y = self.y + d
        if d < 0 or self.y < self.height + 50: 
            if(self.tilt < self.Max_Rotation):
                self.tilt = self.Max_Rotation
            
        if(self.tilt > -90): 
            self.tilt -= self.Rot_Vel

    def draw(self,win):
        self.img_count += 1
        if(self.img_count < self.Ani_time):
            self.img = self.Img
        elif(self.img_count == self.Ani_time*4 + 1):
            self.img = self.Img
            self.img_count = 0
        
        if(self.tilt <= -80):
            self.img = self.Img
            self.img_count = self.Ani_time*2
        
        rotated_image  = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    Gap = 250
    Velocity = 5

    def __init__(self,x):
        self.x = x
        self.height = 0
        self.gap = 160

        self.top = 0
        self.bottom = 0
        self.middle_up = 0
        self.middle_down = 0

        self.PIPE_TOP = pygame.transform.flip(Pipe_Img, False, True) 
        self.PIPE_MIDDLE = Blue_Pipe_Img
        self.PIPE_Bottom = Pipe_Img
        self.r = random.choice(['up','down'])
            
        self.passed = False 
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,180)
        self.top = self.height - self.PIPE_TOP.get_height() 
        self.middle_up = self.height  + self.gap - 20
        self.middle_down = self.middle_up + 170
        self.bottom = self.middle_up + self.gap + 120

    def move(self):
        self.x -= self.Velocity

    def draw(self,win):
        global STAR
        global Star_x,Star_y
        win.blit(self.PIPE_TOP, (self.x,self.top))
        win.blit(self.PIPE_Bottom, (self.x,self.bottom))
        win.blit(self.PIPE_MIDDLE, (self.x,self.middle_up))
        Star_x = self.x
        if(self.r == 'up'):
            Star_y = (self.middle_up - 100)
        else:
            Star_y = (self.bottom + self.middle_down - 60)//2
        win.blit(STAR,(self.x,Star_y))

    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        middle_mask = pygame.mask.from_surface(self.PIPE_MIDDLE)
        bottom_mask = pygame.mask.from_surface(self.PIPE_Bottom)
        
        top_offset = (self.x - bird.x , self.top - round(bird.y))
        middle_up_offset = (self.x - bird.x , self.middle_up - round(bird.y))
        middle_down_offset = (self.x - bird.x , self.middle_down + round(bird.y) + (self.middle_up - self.middle_down))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask,bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)
        mu_point = bird_mask.overlap(middle_mask,middle_up_offset)
        md_point = bird_mask.overlap(middle_mask,middle_down_offset)

        if b_point or t_point or mu_point or md_point:
            return True
        return False

class Base:
    Velo = 5
    Width = Base_Img.get_width()
    Img = Base_Img
    global SCORE

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.Width
    
    def move(self):
        self.x1 -= self.Velo
        self.x2 -= self.Velo

        
        if self.x1 + self.Width < 0: 
            self.x1 = self.x2+self.Width
        
        if self.x2 + self.Width < 0:
            self.x2 = self.x1+self.Width
            
    def draw(self,win):
        win.blit(self.Img,(self.x1,self.y))
        win.blit(self.Img,(self.x2,self.y))

    
def draw_window(win,bird,pipes,base):
    win.blit(BG_Img,(0,0))
    for p in pipes:
        p.draw(win)

    text = Sat_Font.render("Score: "+str(SCORE),1,(0,255,255))
    win.blit(text, (WIN_WID  - 330 - text.get_width() , 10))

    base.draw(win)
    
    bird.draw(win)
    pygame.display.update()

#Use this function to export the best gene into a pickle file.
'''def Export(gen):
    global SCORE
    if SCORE > 40 :
        with open("submission.pkl", "wb") as f:
            print("!!!!!!!!!!!Saved!!!!!!!!!!")
            pickle.dump(gen, f)
            f.close()
            exit()'''


def main(): 
    pygame.init()
    bird = Bird(230,350)
    base = Base(630)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WID, WIN_HEIGHT))
    pygame.display.set_caption('Hopping Bird')
    clock = pygame.time.Clock()
    run = True
    global SCORE
    
    add_pipe = False
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        rem = []
        for pipe in pipes:
            if pipe.collide(bird): #The game is made to terminate when the bird hits the pipe
                run = False
                pygame.quit()
                quit()

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x + bird.Img.get_width():
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe:
            if(SCORE <= 12):
                pipes.append(Pipe(700))
            elif(SCORE <= 24):
                pipes.append(Pipe(650))
            else:
                pipes.append(Pipe(600))
            add_pipe = False 

        for r in rem:
            pipes.remove(r)

        #bird.move() #Uncomment this statement to see the effect of inverted gravity on the bird.
        base.move()
        draw_window(win, bird, pipes, base)


main()
    
