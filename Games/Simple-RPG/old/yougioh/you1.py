#!/usr/bin/python

import itertools
import random

import sys
import os

import pygame
from pygame.locals import *
from you2 import *

#implements n! where 'n' is an integer
def factorial(n):
        if(n == 1 or n == 0):
                return 1
        else:
                return n*factorial(n-1)

#implements nCk where n and k are integers
def combination(n, k):
        num = factorial(n)
        denom = factorial(n-k)*factorial(k)
        return num/denom


def isFlush(hand):
        if(hand[0][1] == hand[1][1] == hand[2][1] == hand[3][1] == hand[4][1]):
                return True
        else:
                return False

def isStraight(hand):
        nums = []

        for i in range(0,len(hand)):
                nums.append(hand[i][0])

        nums.sort()

        isStraight = False
        for i in range(0,len(hand)-1):
                if(nums[i] == nums[i+1]-1):
                        isStraight = True
                else:
                        isStraight = False
                        break

        #special case of 10,J,Q,K,A
        if(nums[0] == 1 and nums[1] == 10 and nums[2] == 11 and nums[3] == 12 and nums[4] == 13):
                isStraight = True

        return isStraight


def isStraightFlush(hand):
        if(isFlush(hand) and isStraight(hand)):
                return True
        else:
                return False



#initialize the current dealt hand and modify the deck
def init_hand():
    global KaibaDeck
    global hand
    global all_possible_holds
    global user_holds
    global index

    del KaibaDeck[:]
    del hand[:]
    del all_possible_holds[:]
    del user_holds[:]
    index = 0
    #current deck
    for c in allcards:
        KaibaDeck.append(c)

    #dealt hand based on random numbers
    while (len(hand) < 2):
        r = random.randint(0, len(allcards)-1)
        if allcards[r] not in hand:
            hand.append(allcards[r])
            KaibaDeck.remove(allcards[r])

    #dealt hand based on hardcoded input
        '''hand = [(8,4),(3,4),(6,1),(5,3),(9,2)]
        for each_card in hand:
                deck.remove(each_card)'''


'''
        the core function
        - evaluates the correct hold strategy for the given hand
        - compares whether user hold strategy matches or not
        - updates the stats
'''

#modified by me
def drawCard(KaibaDeck, hand):
    #global KaibaDeck
    #global hand
    #del KaibaDeck[:]
    #del hand[:]
    #current deck
    #for c in allcards:
    #    KaibaDeck.append(c)

    #draw based on random numbers
    if len(KaibaDeck)>0:
        r = random.randint(0, len(KaibaDeck)-1)
        #if allcards[r] not in hand:
        dCard = KaibaDeck[r]
        hand.append(dCard)
        KaibaDeck.remove(dCard)
    else:
        print "can't draw, no cards in deck"


#mouse input coordinates - check for button click / card click
def user_input(coordinate, KaibaDeck, handp):
#coordinate is mouse coordinates
    global hand
    global MTslot
    global user_holds
    global isActivate
    #global KaibaDeck

    x = int((coordinate[0]-START_X)/IMAGE_WIDTH)
    y = int((coordinate[1]-START_Y)/IMAGE_HEIGHT)

    if((x == 0 or x == 1 or x == 2 or x == 3 or x == 4 or x==5 or x==6) and y == 0): #get the card selected according to mouse coordinate
        if hand[x] in user_holds:
            user_holds.remove(hand[x])
        else:
            user_holds.append(hand[x])
    #SUMMON_BTN[0] is x, [1] is y, [2] is width, [3] is height
    if(coordinate[0] > SUMMON_BTN[0] and coordinate[0] < (SUMMON_BTN[0]+SUMMON_BTN[2]) and coordinate[1] > SUMMON_BTN[1] and coordinate[1] < (SUMMON_BTN[1]+SUMMON_BTN[3])):
    #SUMMON button clicked
        if(isActivate):
            aCard = user_holds[0]
            summon(aCard)
            isActivate = False
    elif(coordinate[0] > ACTIVATE_BTN[0] and coordinate[0] < ACTIVATE_BTN[0]+SUMMON_BTN[2] and coordinate[1] > ACTIVATE_BTN[1] and coordinate[1] < ACTIVATE_BTN[1]+ACTIVATE_BTN[3]):
    #ACTIVATE button clicked
        aCard = user_holds[0]
        hand.remove(aCard)
        MTslot.append(aCard)
        activate(aCard)
        isActivate = True

    elif(coordinate[0] > FS_X+(6*IMAGE_WIDTH) and coordinate[0] < FS_X+(7*IMAGE_WIDTH) and coordinate[1] > FS_Y+(3*IMAGE_HEIGHT) and coordinate[1] < FS_Y+(4*IMAGE_HEIGHT)):
    #FIELD_SLOT[3][6]  clicked
        print "mouse over deck"
        drawCard(KaibaDeck, handp)
        isActivate = True

def activate(aCard):
    print "activate funct"
    aCard.funct


def leftTopCoordsOfBox(boxx, boxy):
    # Convert box coordinates to pixel coordinates
        #where (3,2) refers to box in 4th row, 3rd column
    left = boxx * (BOXWIDTH + GAPSIZE) + XMARGIN
    top = boxy * (BOXHEIGHT + GAPSIZE) + YMARGIN
    return (left, top)

def getBoxAtPixel(x, y):
#converts from pixel to box coordinates
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXWIDTH, BOXHEIGHT)
            if boxRect.collidepoint(x, y):
            #if collidepoint is true, then the box clicked on or moved over a box
                return (boxx, boxy)
    return (None, None)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(screen, WHITE, (left, top, BOXWIDTH, BOXHEIGHT), 3)


def input(events, KaibaDeck, handp):
    """ scan user inputs and decide on action

   """
    global isActivate
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN:
                if event.key == K_RETURN: #enter button on keyboard
                        #if(isDeal):
                        summon()
                        #isDeal = False
                elif event.key == K_SPACE:     #spacebar. K_TAB means tab button on keyboard
                        drawCard(KaibaDeck, handp)
                        #isDeal = True
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            #returns x,y coordinates of the box that the mouse is over
            if boxx != None and boxy != None:
                # The mouse is currently over a box.
                drawHighlightBox(boxx, boxy)
                #whenever mouse is over box to insert card, draw blue highlight around the box
                #to inform the player that he can insert the card there
        elif event.type == MOUSEBUTTONDOWN:
            user_input(pygame.mouse.get_pos(), KaibaDeck, handp)
            mousex, mousey = event.pos
            boxx, boxy = getBoxAtPixel(mousex, mousey)
            #if boxx==6 and boxy==3:
                #drawCard(KaibaDeck, handp)

#displays all objects
def display():
    screen.fill((34,139,34))
    #boundary of payout table
    #pygame.draw.rect(screen,BROWN,(70,70,600,300))
    background_image = pygame.image.load('field.png')
    background_position=(0,0)
    #window.blit(background_image, background_position)
    #pygame.draw.rect(screen, color,(left, top, BOXWIDTH, BOXHEIGHT))

    #Activate,eval buttons
    pygame.draw.rect(screen,WHITE,SUMMON_BTN) #default thickness=0
    pygame.draw.rect(screen,BLUE,SUMMON_BTN,5) #thickness=2
    pygame.draw.rect(screen,WHITE,ACTIVATE_BTN)
    pygame.draw.rect(screen,BLUE,ACTIVATE_BTN,5)

    #field slots
    #field_slots = (fs00, fs01, fs10, fs11)
    #FIELD_SLOT = (FS_X,FS_Y, IMAGE_WIDTH, IMAGE_HEIGHT)
    for i in range(0,4):
        for j in range(0,7):
            pygame.draw.rect(screen,BROWN, (FS_X+(j*IMAGE_WIDTH), FS_Y+(i*IMAGE_HEIGHT), IMAGE_WIDTH, IMAGE_HEIGHT))
            pygame.draw.rect(screen,BLUE, (FS_X+(j*IMAGE_WIDTH), FS_Y+(i*IMAGE_HEIGHT), IMAGE_WIDTH, IMAGE_HEIGHT), 2)

    btn_font_surface_e = btn_font.render("SUMMON",2,BLACK)
    screen.blit(btn_font_surface_e, (SUMMON_X, SUMMON_Y))
    btn_font_surface_d = btn_font.render("ACTIVATE",2,BLACK)
    screen.blit(btn_font_surface_d, (ACTIVATE_X, ACTIVATE_Y))

    #key info
    info_font_surface = info_font.render("[Click on card to hold] [Space to Activate new hand] [Enter to summon hold]",2,(0,0,255))
    screen.blit(info_font_surface, (50, 370))

    stat_font_surface_total =   stat_font.render( "LIFE POINTS: "+str(no_of_deals), 2, BLACK )

    screen.blit(stat_font_surface_total, (550,10))

    #DISPLAY CARDS IN HAND
    x = START_X
    y = START_Y
    for item in hand:
        screen.blit(display_dict[item],(x,y))
        #display HIGHLIGHTED cards
        if(item in user_holds):
            pygame.draw.rect(screen,HIGHLIGHTCOLOR,(x,y,IMAGE_WIDTH,IMAGE_HEIGHT),3)
        x += IMAGE_WIDTH
    for item in MTslot:
        screen.blit(display_dict[item],(x,FS_Y+(3*IMAGE_HEIGHT)))
        x += IMAGE_WIDTH


    x = 50
    y = 200
    if len(all_possible_holds) > 0:
        for item in all_possible_holds[index]:
            if item in display_dict.keys():
                screen.blit(display_dict[item],(x,y))
            x += IMAGE_WIDTH
        if match_flag:
            pygame.draw.circle(screen, GREEN, (240,30), 10)
            pygame.draw.circle(screen, RED, (270,30), 10)
        else:
            pygame.draw.circle(screen, GREEN, (240,30), 10)
            pygame.draw.circle(screen, RED, (270,30), 10)
    pygame.display.flip()

def PotFunct(KaibaDeck, hand):
    print "Draw 2 cards from your deck"
    drawCard(KaibaDeck, hand)

def BladeKnightFunct():
    print "BladeKnightFunct"

def BEWDFunct():
    print "BEWDFunct"

def VirusCannonFunct():
    print "VirusCannonFunct"

def VampireLordFunct():
    print "VampireLordFunct"

allcards =[]

#initialize the 52 cards
#modified by me for c in color:
#       for v in value:
#               card.append((v,c))
KaibaDeck = []          #current KaibaDeck
hand = []       #dealt hand
MTslot = []

BlueEyesWhiteDragon = Monster('BLUEEYESWHITEDRAGON', BEWDFunct, 3000,2500, 8)
BladeKnight = Monster('BLADEKNIGHT', BladeKnightFunct, 1600,1000, 4)
PotOfGreed = Magic('POTOFGREED', PotFunct(KaibaDeck, hand))

VirusCannon = Trap('VIRUSCANNON', VirusCannonFunct)
VampireLord = Monster('VAMPIRELORD', 2000, 1500, 5, VampireLordFunct)
allcards.extend([BladeKnight, BlueEyesWhiteDragon, PotOfGreed, VirusCannon, VampireLord])

all_possible_holds = []
user_holds = []
index = 0
match_flag = False

no_of_deals = 0
match_cnt = 0

isActivate = True

#for displaying graphics
display_dict = {}

init_hand()

#print PotOfGreed.Name
#print "funct is"
#PotOfGreed.funct()

print "dealt hand: "
for i in range(0, len(hand)):
    #print print_num[hand[i][0]], modified by me
    #print print_color[hand[i][1]],
    #print ' ',
    print hand[i].Name #modified by me
    print hand[i].funct
#print ''

BROWN = (160,82,45)
GREEN = (0, 255, 0)
WHITE = (255,255,255)
BLUE = (0, 0, 128)
RED = (255,0,0)
BLACK = (0, 0, 0)
HIGHLIGHTCOLOR = BLUE

SCREEN_X = 850
SCREEN_Y = 600

IMAGE_WIDTH = 75
IMAGE_HEIGHT = 90

START_X = 10
START_Y = 500

SUMMON_X = 60
ACTIVATE_X = SUMMON_X +150
SUMMON_Y= 450
ACTIVATE_Y = SUMMON_Y
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 20
SUMMON_BTN = (SUMMON_X,SUMMON_Y,BUTTON_WIDTH,BUTTON_HEIGHT)
ACTIVATE_BTN = (ACTIVATE_X,ACTIVATE_Y,BUTTON_WIDTH,BUTTON_HEIGHT)
FS_X = 10
FS_Y = 50


BOXWIDTH = 120
BOXHEIGHT = 120
GAPSIZE = 0 # size of gap between boxes in pixels
WINDOWWIDTH = 640 # size of window's width in pixels
WINDOWHEIGHT = 480 # size of windows' height in pixels
BOARDWIDTH = 7 # number of columns of icons
BOARDHEIGHT = 4 # number of rows of icons
XMARGIN = FS_X#int((SCREEN_X - (BOARDWIDTH * (BOXWIDTH + GAPSIZE))) / 2)
YMARGIN = FS_Y#int((SCREEN_Y - (BOARDHEIGHT * (BOXHEIGHT + GAPSIZE))) / 2)

bet_val = 1.00 #1$

#start
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

window = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
#window is same as DISPLAYSURF, which is the display SURFACE
pygame.display.set_caption("PokerStrat")
screen = pygame.display.get_surface()

'''
        initializing all card image files
'''
IMG_FILES = []
for i in range(0,len(allcards)):
        inx = allcards[i].Name#i+1
        inx_file = str(inx)+".png"
        IMG_FILES.append(inx_file)

'''
        initializing all card image objects
'''

#store images of all cards in display_dict
img_objs = []
for image_file in IMG_FILES:
        #img_objs.append(pygame.image.load(image_file).convert())
    img_card = pygame.image.load(image_file)
    img_card = pygame.transform.scale(img_card, (IMAGE_WIDTH, IMAGE_HEIGHT))#(45,70))
    img_objs.append(img_card.convert())

for i in range(0, len(img_objs)):
        display_dict[allcards[i]] = img_objs[i]

'''
        fonts
'''
stat_font = pygame.font.Font('freesansbold.ttf', 32)
fontObj = pygame.font.Font('freesansbold.ttf', 32)
pay_font = pygame.font.Font( 'freesansbold.ttf', 26)
btn_font = pygame.font.Font( 'freesansbold.ttf', 20)
info_font = pygame.font.Font( 'freesansbold.ttf', 20)

display()

while True:
    input(pygame.event.get(), KaibaDeck, hand)
    display()
