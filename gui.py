import pygame
from pygame.locals import *
from connect4 import *



pygame.init()

screen_width = 600
screen_height = 550

screen = pygame.display.set_mode((screen_width, screen_height))
#pygame.display.set_caption('Connect 4')

#define colours
bright_purple = (153, 0, 153)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255,255,0)
blue = (0,0,255)
dark_green=(0,200,0)
green=(0,255,0)
grey= (192, 192, 192)
dark_blue = (0, 0, 128)
bright_blue=(50, 150, 255)

#define labels
font = pygame.font.SysFont('Constantia', 30)
font1 = pygame.font.SysFont('monospace', 30)
titleFont = pygame.font.SysFont('Constantia', 60)
label = titleFont.render("Connect 4",1,bright_purple)
label2 = font.render("Alpha-Beta pruning",1,black)

#define global variable
clicked = False

class Screen():
    def __init__(self, title, width=screen_width,height=screen_height,fill=grey):
        self.title=title
        self.width=width
        self.height=height
        self.fill=fill
        self.current=False

    def makeCurrent(self):
        pygame.display.set_caption(self.title)
        self.current=True
        self.screen= pygame.display.set_mode((self.width,self.height))

    def endCurrent(self):
        self.current=False

    def checkUpdate(self):
        return self.current

    def screenUpdate(self):
        if(self.current):
            self.screen.fill(self.fill)

    def returnTitle(self):
        return self.screen			


class button():
        
    #colours for button and text
    #button_col = dark_blue
    hover_col = bright_blue
    click_col =bright_purple
    text_col = white
    #width = 180
    #height = 70

    def __init__(self, x, y, text,button_col,width,height):
        self.x = x
        self.y = y
        self.text = text
        self.button_col=button_col
        self.width = width
        self.height = height

    def draw_button(self):

        global clicked
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #create pygame Rect object for the button
        button_rect = Rect(self.x, self.y, self.width, self.height)
        
        #check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.click_col, button_rect)
             
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)
        
        #add shading to button
        pygame.draw.line(screen, black, (self.x, self.y), (self.x + self.width, self.y), 2)
        pygame.draw.line(screen, black, (self.x, self.y), (self.x, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x, self.y + self.height), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, black, (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), 2)

        #add text to button
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 25))
        return action



def text1(word,x,y):
    font = pygame.font.SysFont(None,30)
    text = font.render("{}".format(word), True,black)
    return screen.blit(text,(x,y))

def inpt():
    depth=None
    text1("Please enter the DEPTH: ",75,150) # asking for depth
    pygame.display.flip()
    #done = True
    #while done:
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_a:
                 #   word+=str(chr(event.key))
                if event.key == pygame.K_0:
                    depth=chr(event.key)
                if event.key == pygame.K_1:
                    depth=chr(event.key) 
                if event.key == pygame.K_2:
                    depth=chr(event.key) 
                if event.key == pygame.K_3:
                    depth=chr(event.key) 
                if event.key == pygame.K_4:
                    depth=chr(event.key) 
                if event.key == pygame.K_5:
                    depth=chr(event.key) 
                if event.key == pygame.K_6:
                    depth=chr(event.key) 
                if event.key == pygame.K_7:
                    depth=chr(event.key)                                
                if event.key == pygame.K_8:
                    depth=chr(event.key) 
                if event.key == pygame.K_9:
                    depth=chr(event.key)         
                if event.key == pygame.K_RETURN:
                    done=False  
                #events...
               
                #print(depth)
                text1(depth,330,150)
    return depth


#Buttons
multi = button(200, 200, 'Multiplayer',dark_blue,180,70)
single = button(200, 300, 'One-player',dark_blue,180,70)
yes = button(75, 250, 'With',dark_blue,180,70)
no = button(325, 250, 'Without',dark_blue,180,70)
play=button(200, 370, 'PLAY',blue,140,70)

#Screens
screen1=Screen("Menu Screen")
screen2=Screen("Window 2")
screen3=Screen("Connect 4")

window=screen1.makeCurrent()

run = True
depth=None
while run:
    screen1.screenUpdate()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RETURN:
                run=False
    #first window
    if screen1.checkUpdate():
        screen.blit(label, (150,40))
        if multi.draw_button():
            window=screen3.makeCurrent()
            screen1.endCurrent()
            game=Connect4()
            game.PlayerVsPlayer() 
  
        if single.draw_button():
            window=screen2.makeCurrent()
            screen1.endCurrent()
            screen2.screenUpdate()
   
    #second window
    elif screen2.checkUpdate():
        screen.blit(label, (150,40))
        
        while depth==None:
             depth=inpt() 
        screen.blit(label2, (75,200))     
        if yes.draw_button():
             yes = button(75, 250, 'With',bright_purple,180,70)
             pruning=True
             #print('With pruning')
        
        if no.draw_button():
             no = button(325, 250, 'Without',bright_purple,180,70)
             pruning=False
             #print('Without pruning')
           
        
        if play.draw_button():
             window=screen3.makeCurrent()
             screen2.endCurrent()
             game=Connect4()
             game.PlayerVsComputer(int(depth),pruning)
        
   
    pygame.display.update()

pygame.quit()

