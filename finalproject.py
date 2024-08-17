import pygame
from pygame.locals import *

import random

pygame.init()

white = (255, 255, 255)
black = (  0,   0,   0)
red   = (255,   0,   0)
green = (  0, 255,   0)
blue = (0, 0, 150)
lightblue = (0, 0, 250)
orange = (255, 150, 0)
yellow = (255, 255, 0)
teal = (0, 200, 200)
purple = (255, 0, 255)

SQUARE_WIDTH = 25
SQUARE_HEIGHT = 25

screenwidth = 400
screenheight = 600
screensize = [screenwidth, screenheight]
screen = pygame.display.set_mode(screensize)
pygame.display.set_caption("Tetris!")

startx = int(screenwidth / 2)
starty = int(0)
color = white

BLANK = [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black]

score = 0

sound = pygame.mixer.Sound("gamemusic.mp3")
sound.play()

def to_color(clr_list):
    if clr_list == (0, 0, 0):
        return "-"
    else:
        return "B"

def debug_grid():
    print("########################################")
    for rowi in range(0,24):
        for coli in range(0,16):
            print("%s" % to_color(all_squares[rowi][coli]), end="")
        print()

def break_into_squares(block):
    global all_squares
    for square in block.squares:
        column = square.x // 25
        row = square.y // 25
#         print(row)
#         print(column)
#         print(len(all_squares))
#         print(len(all_squares[0]))
        all_squares[row][column] = block.color
    #debug_grid()
            
#         print("Adding at %d,%d: %s" % (row, column, all_squares[row][column]))

def check_row():
    global score
    removers = []
    for rowi in range(0,24):
        row_needs_deleted = True
        for coli in range(0,16):
            if all_squares[rowi][coli] == black:
                row_needs_deleted = False
        #found a row that needs eliminated
        if row_needs_deleted:
            removers.append(rowi)
            
    for i in range(len(removers) -1, -1, -1):
        print("Removing {}".format(removers[i]))
        all_squares.pop(removers[i])
    for x in removers:
        all_squares.insert(0, BLANK[:])
        score += 10
        
    if len(removers) > 0:
        check_floating_blocks()
        
            
def check_floating_blocks():
    for rowi in range(22, -1, -1):
        for coli in range(0,16):
            if all_squares[rowi][coli] != black and all_squares[rowi + 1][coli] == black:
                all_squares[rowi + 1][coli] = all_squares[rowi][coli]
                all_squares[rowi][coli] = black 


class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
  

class TetrisBlock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.squares = []
        self.color = color
        self.image = pygame.Surface([SQUARE_WIDTH*4, SQUARE_HEIGHT*4])
        #self.image.fill(white)
        self.rect = self.image.get_rect()
    
#     def beneath(self, block):
#         for mysquare in self.squares:
#             for theirsquare in block.squares:
#                 if mysquare.x == theirsquare.x and mysquare.y - SQUARE_HEIGHT == theirsquare.y:
#                     return True
#         return False

    def must_rest(self):
        for mysquare in self.squares:
            rowi = (mysquare.y + SQUARE_HEIGHT) // 25
            coli = mysquare.x // 25
            if rowi == 24:
                return True
            if all_squares[rowi][coli] != black:
                return True
        return False
    
    def at_bottom(self):
        for mysquare in self.squares:
            if mysquare.y + SQUARE_HEIGHT == screenheight:
                return True
        return False
    
    def left_of(self, block):
        for mysquare in self.squares:
            for theirsquare in block.squares:
                if mysquare.x == theirsquare.x - SQUARE_WIDTH and mysquare.y == theirsquare.y:
                    return True
        return False
    
    def right_of(self, block):
        for mysquare in self.squares:
            for theirsquare in block.squares:
                if mysquare.x == theirsquare.x + SQUARE_WIDTH and mysquare.y == theirsquare.y:
                    return True
        return False
    
    def drop(self):
        for square in self.squares:
            square.y += SQUARE_HEIGHT
 
    def move(self):
        keys = pygame.key.get_pressed()
        global other_blocks
        
        if keys[K_LEFT]:
#             for other in other_blocks:
#                 if self.right_of(other):
#                     return
            for square in self.squares:
                if square.x == 0:
                    return
                rowi = square.y // 25
                coli = square.x // 25
                if all_squares[rowi][coli-1] != black:
                    return
            for square in self.squares:
                square.x -= SQUARE_WIDTH
            
        if keys[K_RIGHT]:
#             for other in other_blocks:
#                 if self.left_of(other):
#                     return
            for square in self.squares:
                if square.x + SQUARE_WIDTH == 400:
                    return
                rowi = square.y // 25
                coli = square.x // 25
                if all_squares[rowi][coli+1] != black:
                    return
            for square in self.squares:
                square.x += SQUARE_WIDTH
            
#         if keys[K_DOWN]:
#             for square in self.squares:
#                 square.y += SQUARE_HEIGHT
        
        if keys[K_SPACE]:
            #self.image.rotation += 1
#             rotation = pygame.transform.rotate(self.image, 90)
#             self.image.get_rect()
            current_block.rotate()
        
    def draw(self, screen, color):
        for square in self.squares:
            pygame.draw.rect(screen, self.color, [square.x, square.y, SQUARE_WIDTH, SQUARE_HEIGHT], 0)
            pygame.draw.rect(screen, black, [square.x, square.y, SQUARE_WIDTH, SQUARE_HEIGHT], 1)
    
class LBlock(TetrisBlock):
    def __init__(self):
        super().__init__()
        self.color = orange
        nextx = startx
        nexty = starty
        self.level = 1
        self.squares = []
        for i in range(0,2):
            self.squares.append(Square(startx,nexty))
            nexty += SQUARE_HEIGHT
        for i in range(2,4):
            self.squares.append(Square(nextx,nexty))
            nextx += SQUARE_WIDTH
        
    def rotate(self):
        if self.level == 1:
            self.squares[0].x = self.squares[0].x + 25
            self.squares[0].y = self.squares[0].y + 25
            self.squares[2].x = self.squares[2].x - 25
            self.squares[2].y = self.squares[2].y - 25
            self.squares[3].x = self.squares[3].x - 50
            self.level = 2
        elif self.level == 2:
            self.squares[0].x = self.squares[0].x - 25
            self.squares[0].y = self.squares[0].y + 25
            self.squares[2].x = self.squares[2].x + 25
            self.squares[2].y = self.squares[2].y - 25
            self.squares[3].y = self.squares[3].y - 50
            self.level = 3
        elif self.level == 3:
            self.squares[0].x = self.squares[0].x - 25
            self.squares[0].y = self.squares[0].y - 25
            self.squares[2].x = self.squares[2].x + 25
            self.squares[2].y = self.squares[2].y + 25
            self.squares[3].x = self.squares[3].x + 50
            self.level = 4
        elif self.level == 4:
            self.squares[0].x = self.squares[0].x + 25
            self.squares[0].y = self.squares[0].y - 25
            self.squares[2].x = self.squares[2].x - 25
            self.squares[2].y = self.squares[2].y + 25
            self.squares[3].y = self.squares[3].y + 50
            self.level = 1
            
        
class IBlock(TetrisBlock):
    def __init__(self):
        super().__init__()
        nextx = startx
        self.color = lightblue
        self.level = 1
        self.squares = []
        for i in range(0, 4):
            self.squares.append(Square(nextx, 0))
            nextx += SQUARE_WIDTH
            
    def rotate(self):
        if self.level == 1:
            self.squares[1].x = self.squares[1].x - 25
            self.squares[1].y = self.squares[1].y - 25
            self.squares[2].x = self.squares[2].x - 50
            self.squares[2].y = self.squares[2].y - 50
            self.squares[3].x = self.squares[3].x - 75
            self.squares[3].y = self.squares[3].y - 75
            self.level = 2
        elif self.level == 2:
            self.squares[1].x = self.squares[1].x + 25
            self.squares[1].y = self.squares[1].y + 25
            self.squares[2].x = self.squares[2].x + 50
            self.squares[2].y = self.squares[2].y + 50
            self.squares[3].x = self.squares[3].x + 75
            self.squares[3].y = self.squares[3].y + 75
            self.level = 1
            

class ZBlock(TetrisBlock):
    def __init__(self):
        super().__init__()
        nextx = startx
        nexty = starty
        self.color = red
        self.level = 1
        self.squares = []
        for i in range(0,2):
            self.squares.append(Square(nextx, 0))
            nextx += SQUARE_WIDTH
        self.squares.append(Square(nextx - SQUARE_WIDTH, nexty + SQUARE_HEIGHT))
        self.squares.append(Square(nextx, nexty + SQUARE_HEIGHT))
        
    def rotate(self):
        if self.level == 1:
            self.squares[0].x = self.squares[0].x + 25
            self.squares[1].y = self.squares[1].y + 25
            self.squares[2].x = self.squares[2].x - 25
            self.squares[3].x = self.squares[3].x - 50
            self.squares[3].y = self.squares[3].y + 25
            self.level = 2
        elif self.level == 2:
            self.squares[0].x = self.squares[0].x - 25
            self.squares[1].y = self.squares[1].y - 25
            self.squares[2].x = self.squares[2].x + 25
            self.squares[3].x = self.squares[3].x + 50
            self.squares[3].y = self.squares[3].y - 25
            self.level = 1
                  

class SBlock(TetrisBlock):
    def __init__(self):
        super().__init__()
        self.color = green
        self.level = 1
        self.squares = []
        self.squares.append(Square(startx, 0))
        self.squares.append(Square(startx + SQUARE_WIDTH, 0))
        self.squares.append(Square(startx, starty + SQUARE_HEIGHT))
        self.squares.append(Square(startx - SQUARE_WIDTH, starty + SQUARE_HEIGHT))
    
    def rotate(self):
        if self.level == 1:
            self.squares[0].x = self.squares[0].x + 25
            self.squares[0].y = self.squares[0].y + 50
            self.squares[1].y = self.squares[1].y + 25
            self.squares[3].x = self.squares[3].x + 25
            self.squares[3].y = self.squares[3].y - 25
            self.level = 2
        elif self.level == 2:
            self.squares[0].x = self.squares[0].x - 25
            self.squares[0].y = self.squares[0].y - 50
            self.squares[1].y = self.squares[1].y - 25
            self.squares[3].x = self.squares[3].x - 25
            self.squares[3].y = self.squares[3].y + 25
            self.level = 1

class OBlock(TetrisBlock):
    def __init__(self):
        super().__init__()
        self.color = yellow
        self.squares = []
        self.squares.append(Square(startx, 0))
        self.squares.append(Square(startx + SQUARE_WIDTH, 0))
        self.squares.append(Square(startx, starty + SQUARE_HEIGHT))
        self.squares.append(Square(startx + SQUARE_WIDTH, starty + SQUARE_HEIGHT))
    
    def rotate(self):
        pass

class JBlock(TetrisBlock):
    def __init__(self):
        super().__init__()
        nextx = startx
        nexty = starty
        self.color = teal
        self.level = 1
        self.squares = []
        for i in range(0,2):
            self.squares.append(Square(startx,nexty))
            nexty += SQUARE_HEIGHT
        for i in range(2,4):
            self.squares.append(Square(nextx,nexty))
            nextx -= SQUARE_WIDTH
            
    def rotate(self):
        if self.level == 1:
            self.squares[0].x = self.squares[0].x + 25
            self.squares[0].y = self.squares[0].y + 25
            self.squares[2].x = self.squares[2].x - 25
            self.squares[2].y = self.squares[2].y - 25
            self.squares[3].y = self.squares[3].y - 50
            self.level = 2
        elif self.level == 2:
            self.squares[0].x = self.squares[0].x - 25
            self.squares[0].y = self.squares[0].y + 25
            self.squares[2].x = self.squares[2].x + 25
            self.squares[2].y = self.squares[2].y - 25
            self.squares[3].x = self.squares[3].x + 50
            self.level = 3
        elif self.level == 3:
            self.squares[0].x = self.squares[0].x - 25
            self.squares[0].y = self.squares[0].y - 25
            self.squares[2].x = self.squares[2].x + 25
            self.squares[2].y = self.squares[2].y + 25
            self.squares[3].y = self.squares[3].y + 50
            self.level = 4
        elif self.level == 4:
            self.squares[0].x = self.squares[0].x + 25
            self.squares[0].y = self.squares[0].y - 25
            self.squares[2].x = self.squares[2].x - 25
            self.squares[2].y = self.squares[2].y + 25
            self.squares[3].x = self.squares[3].x - 50
            self.level = 1

class TBlock(TetrisBlock):
    def __init__(self):
        super().__init__()
        self.color = purple
        self.level = 1
        self.squares = []
        self.squares.append(Square(startx, starty))
        nexty = starty + SQUARE_HEIGHT
        nextx = startx - SQUARE_WIDTH
        for i in range(0,3):
            self.squares.append(Square(nextx, nexty))
            nextx = nextx + SQUARE_WIDTH
            
    def rotate(self):
        if self.level == 1:
            self.squares[0].x = self.squares[0].x + 25
            self.squares[0].y = self.squares[0].y + 25
            self.squares[1].x = self.squares[1].x + 25
            self.squares[1].y = self.squares[1].y - 25
            self.squares[3].x = self.squares[3].x - 25
            self.squares[3].y = self.squares[3].y + 25
            self.level = 2
        elif self.level == 2:
            self.squares[0].x = self.squares[0].x - 25
            self.squares[0].y = self.squares[0].y + 25
            self.squares[1].x = self.squares[1].x + 25
            self.squares[1].y = self.squares[1].y + 25
            self.squares[3].x = self.squares[3].x - 25
            self.squares[3].y = self.squares[3].y - 25
            self.level = 3
        elif self.level == 3:
            self.squares[0].x = self.squares[0].x - 25
            self.squares[0].y = self.squares[0].y - 25
            self.squares[1].x = self.squares[1].x - 25
            self.squares[1].y = self.squares[1].y + 25
            self.squares[3].x = self.squares[3].x + 25
            self.squares[3].y = self.squares[3].y - 25
            self.level = 4
        elif self.level == 4:
            self.squares[0].x = self.squares[0].x + 25
            self.squares[0].y = self.squares[0].y - 25
            self.squares[1].x = self.squares[1].x - 25
            self.squares[1].y = self.squares[1].y - 25
            self.squares[3].x = self.squares[3].x + 25
            self.squares[3].y = self.squares[3].y + 25
            self.level = 1
        

def random_new_block():
    randomnumber = random.randint(0, 12)
    if randomnumber == 0 or randomnumber == 1:
        return LBlock()
    elif randomnumber == 2:
        return IBlock()
    elif randomnumber == 3 or randomnumber == 4:
        return ZBlock()
    elif randomnumber == 5 or randomnumber == 6:
        return SBlock()
    elif randomnumber == 7 or randomnumber == 8:
        return OBlock()
    elif randomnumber == 9 or randomnumber == 10:
        return JBlock()
    elif randomnumber == 11 or randomnumber == 12:
        return TBlock()
    

clock = pygame.time.Clock()

current_block = random_new_block()
#allsprites = pygame.sprite.Group()
other_blocks = pygame.sprite.Group()
all_squares = [[black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
               [black, black, black, black, black, black, black, black, black, black, black, black, black, black, black, black],
]


lose = False

done = False

while not done:
    # 1. Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    current_block.move()
    

    # 2. Program logic, change variables, etc.
    if current_block.must_rest():
#             other_blocks.add(current_block)
            # determine where square is and put it in correct list
        break_into_squares(current_block)
            # all_squares.append(square)   
        current_block = random_new_block()
            #allsprites.add(current_block)
        
            
    if current_block.at_bottom():
        #other_blocks.add(current_block)
        break_into_squares(current_block)
        current_block = random_new_block()
        
    check_row()
    current_block.drop()
    
    if all_squares[1][9] != black:
        lose = True
    
    # 3. Draw stuff
    #allsprites.draw(screen)
        
    if lose == True:
        screen.fill(red)
        losefont = pygame.font.Font(None, 40)
        losetext = losefont.render("You lost at", True, white)
        losetext2 = losefont.render("%d points :(" % score, True, white)
        screen.blit(losetext, [100, 250])
        screen.blit(losetext2, [100, 300])
        
        
    else:
        screen.fill(black)
        for rowi in range(0,24):
            for coli in range(0,16):
                pygame.draw.rect(screen, all_squares[rowi][coli], [coli * 25, rowi * 25, SQUARE_WIDTH, SQUARE_HEIGHT], 0)
                pygame.draw.rect(screen, black, [coli * 25, rowi * 25, SQUARE_WIDTH, SQUARE_HEIGHT], 1)
        
        current_block.draw(screen, color)
    
        font = pygame.font.Font(None, 40)
        text = font.render("Score: %d" % score, True, white)
        screen.blit(text, [10, 10])
    
#     for block in other_blocks:
#         block.draw(screen, color)
 

    pygame.display.flip()
    clock.tick(5)


pygame.quit()

