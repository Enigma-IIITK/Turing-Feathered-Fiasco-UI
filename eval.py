import  pygame
import neat
import os
import pickle
import random
import math
from time import sleep
pygame.font.init()

WIN_WID = 500
WIN_HEIGHT = 700
SCORE = 0
IS_COLLECTED_COIN = None

image_folder = "Images"
STAR = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "coin_try6 (1).png")), (82, 70))


bird_image_path = os.path.join(image_folder, "Pebbles.png")
Bird_Img = pygame.transform.scale2x(pygame.image.load(bird_image_path))

pipe_image_path = os.path.join(image_folder, "Blue Pipe.jpg")
Pipe_Img = pygame.transform.scale2x(pygame.image.load(pipe_image_path))

base_image_path = os.path.join(image_folder, "Blue Base.png")
Base_Img = pygame.transform.scale2x(pygame.image.load(base_image_path))

bg_image_path = os.path.join(image_folder, "ICE BG.png")
BG_Img = pygame.transform.scale2x(pygame.image.load(bg_image_path))

Blue_Pipe_Img = pygame.transform.scale(pygame.image.load(os.path.join(image_folder, "Blue Pipe.jpg")), (100, 170))

Star_x,Star_y = 0,0

bird_img_scaled = pygame.transform.scale(Bird_Img, (Bird_Img.get_width() * 0.75, Bird_Img.get_height() * 0.75))
bird_Img = bird_img_scaled

Sat_Font = pygame.font.SysFont("timesnewroman",45)


class Bird:
    Img = Bird_Img
    Max_Rotation = 25
    Rot_Vel = 20
    Ani_time = 5

    def __init__(self,x,y): #Constructor to initialize the objects
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.alive_time = 0
        self.eval_fit = 0
        self.vel = 0
        self.height =  self.y
        self.img_count = 0
        self.img = self.Img

    def jumpup(self,dis):
        self.vel = -dis #To make the bird move up
        self.height = self.y
        self.tick_count = 0 #A counter to know when the last jump was made. It is similar to the time required while jumping 

    def jumpdown(self,dis):
        self.vel = dis
        self.height = self.y
        self.tick_count = 0

    def jump(self):
        self.vel = -6.5
        self.height = self.y
        self.tick_count = 0

    def move(self):
        self.tick_count += 1
        self.alive_time += 1
        d = -(self.vel*self.tick_count + 1.5*self.tick_count**2) #No.of pixels we are moving upwards

        if(d >= 16): #Terminal Velocity
            d = 16
        if(d < 0):
            d -= 2
        
        self.y = self.y + d
        if d < 0 or self.y < self.height + 50: #Tilt up
            if(self.tilt < self.Max_Rotation):
                self.tilt = self.Max_Rotation
            
        if(self.tilt > -90): #Tilt down
            self.tilt -= self.Rot_Vel
        
        self.eval_fit =  (self.alive_time * 0.00043 + SCORE * 2.5) * 10
        return self.eval_fit

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
    Gap = 300
    Velocity = 5

    def __init__(self,x):
        self.x = x
        self.height = 0
        self.gap = 160

        self.top = 0
        self.bottom = 0
        self.middle_up = 0
        self.middle_down = 0

        self.PIPE_TOP = pygame.transform.flip(Pipe_Img, False, True) # Pipe that is flipped
        self.PIPE_MIDDLE = Blue_Pipe_Img
        self.PIPE_Bottom = Pipe_Img
        self.r = random.choice(['up','down'])
            
        self.passed = False # If the bird has already passed the pipe
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,180)
        self.top = self.height - self.PIPE_TOP.get_height() 
        self.middle_up = self.height  + self.gap - 20
        self.middle_down = self.middle_up + 170
        self.bottom = self.middle_up + self.gap + 120

    def move(self):
        self.x -= self.Velocity#To move the pipe in each frame

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

        b_point = bird_mask.overlap(bottom_mask,bottom_offset)#Tells us how far the bird is from the Pipe
        t_point = bird_mask.overlap(top_mask,top_offset)#Both of these return None if they are not colliding
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

        #We are trying to create a circular pattern of 2 imgs of the baseto make us feel that the base is moving.
        if self.x1 + self.Width < 0: #If the 1st image os of the screen
            self.x1 = self.x2+self.Width
        
        if self.x2 + self.Width < 0:
            self.x2 = self.x1+self.Width
            
    def draw(self,win):
        win.blit(self.Img,(self.x1,self.y))
        win.blit(self.Img,(self.x2,self.y))

    
def draw_window(win,birds,pipes,base):
    win.blit(BG_Img,(0,0))
    for p in pipes:
        p.draw(win)

    text = Sat_Font.render("Score: "+str(SCORE),1,(0,255,255))
    win.blit(text, (WIN_WID  - 330 - text.get_width() , 10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()

def Score_Boost(bird):
    global Star_x, Star_y
    if(math.floor(math.sqrt(math.pow(Star_x - bird.x,2) + math.pow(Star_y - bird.y,2))) <= 30):
        IS_COLLECTED_COIN = True
        return True
    else:
        IS_COLLECTED_COIN = True
        return False




def main(genomes,config): #Fitness Function. Evaluates all birds
    global SCORE
    SCORE = 0
    global IS_COLLECTED_COIN
    final_eval_fit = 0
    pygame.init()
    birds = []
    nets = []
    gen = []
    with open("submission.pkl", "rb") as f:
        genome = pickle.load(f)
    genomes = [(1, genome)]
    #The indexes of all the 3 lists will point to the same bird
    for _,g in genomes:#We are traversing a tuple here
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        gen.append(g) #Append the genome into our list
    base = Base(630)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WID, WIN_HEIGHT))
    pygame.display.set_caption('Hopping Bird')
    clock = pygame.time.Clock()
    run = True
    add_pipe = False
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        pipe_index = 0
        if(len(birds) > 0):#If the bird passes the pipe we want to increase the pipe index   
            if(len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()):
                pipe_index = 1
        
        else:
            run = False
            return final_eval_fit
        
        for x,bird in enumerate(birds):
            final_eval_fit = bird.move() #Encouraging the bird to continue the game
            gen[x].fitness += 0.1 #It increases at a fast rate, so we set the increment low
            global Star_y,Star_x
            #Passing the bird position, top and bottom pillar position
            #output = nets[x].activate((bird.y ,abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].middle_up),abs(bird.y - pipes[pipe_index].middle_down), abs(bird.y - pipes[pipe_index].bottom)))
            distance = math.sqrt((Star_x-bird.x)**2 + (Star_y-bird.y)**2)
            displacement_x = (Star_x-bird.x)
            displacement_y = (Star_y-bird.y)
            output = nets[x].activate((bird.y,Star_y,abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].middle_up),abs(bird.y - pipes[pipe_index].middle_down), abs(bird.y - pipes[pipe_index].bottom)))
            #What if we get 2 outputs fromn the same neuron based on the position of the bird   
            #print(output)
            
            #det = output.index(max(output[:3]))
            
            det = output.index(max(output[:3]))
            
            # if output[0] > 0.9:
            #     bird.jumpup(abs(Star_y-bird.y))
            # elif output[0] < 0.3:
            #     bird.jumpdown(abs(Star_y-bird.y))
            if det == 0:
                pass
            else:
                bird.jump()

            

            
        rem = []        
        for pipe in pipes:
            for x,bird in enumerate(birds):
                if pipe.collide(bird):
                   gen[x].fitness -= 1
                   birds.pop(x)
                   nets.pop(x)
                   gen.pop(x)


                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)            

            if add_pipe:
                for g in gen:
                    g.fitness += 20  #We motivate the bird to fly into the Hole
                    print(Score_Boost(bird))
                    if Score_Boost(bird):
                        g.fitness += 20
                        SCORE += 1
                    
                    else:
                        g.fitness -= 50
                        return final_eval_fit
                        pygame.quit()


                pipes.append(Pipe(700))
                add_pipe = False
            
            for r in rem:
                pipes.remove(r)
            
            for x,bird in enumerate(birds):#Elimination of unworthy birds
                if bird.y + bird.img.get_height() >= 630 or bird.y < 0:
                    birds.pop(x)
                    nets.pop(x)
                    gen.pop(x)

            pipe.move()
        base.move()
        draw_window(win, birds,pipes,base)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    popu = neat.Population(config) #The population
    
    popu.add_reporter(neat.StdOutReporter(True)) #Just some statistical data()
    stats = neat.StatisticsReporter()
    popu.add_reporter(stats)

    return main([], config)#We could store this data into a pickle file so that we can use this parent in the forhtcoming processes

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config.txt")
    print(f"The Final Eval Fitness Of this submission is : {run(config_path)}")
    
