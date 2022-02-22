import sys
import pygame
import numpy as np
from kalah import Kalah
from alphaBeta import chooseMove
from pygame.locals import QUIT

pygame.init()
pygame.font.init()
pygame.display.set_caption('Minimax Mancala')
clock = pygame.time.Clock()

board = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]

maxdepth = 3
gnode = Kalah(board, "B") # the player will always be B, the computer will also be A

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
LIGHT_TAN = (245, 240, 215)
DEEPER_TAN = (245, 222, 179)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

global mssg
mssg = ""
mssgfont = pygame.font.SysFont(None, 30)
mssgdisplay = mssgfont.render(mssg, True, (255, 255, 255))
nexttext = mssgfont.render(" ", True, (40, 40, 40))
screen.blit(nexttext, (483, 90))

def generateMarbles(num, xpos, ypos):
    positions = [(xpos+10, ypos-10), (xpos-10, ypos-10), (xpos-10, ypos+10), (xpos+10, ypos+10), (xpos, ypos), (xpos, ypos+20), (xpos,ypos-20), (xpos-20, ypos), (xpos+20, ypos), (xpos+20, ypos-20), (xpos-20, ypos-20), (xpos-20, ypos+20), (xpos+20, ypos+20), (xpos+10, ypos-30), (xpos-10, ypos-30), (xpos+10, ypos+30), (xpos-10, ypos+30), (xpos, ypos-40), (xpos, ypos+40), (xpos+20, ypos-40), (xpos-20, ypos-40), (xpos+20, ypos+40), (xpos-20, ypos+40), (xpos+30, ypos-10), (xpos-30, ypos-10), (xpos+30, ypos+10), (xpos-30, ypos+10), (xpos+10, ypos-50), (xpos-10, ypos-50), (xpos+10, ypos+50), (xpos-10, ypos+50), (xpos, ypos-60), (xpos, ypos+60), (xpos+30, ypos-30), (xpos-30, ypos-30), (xpos+30, ypos+30), (xpos-30, ypos+30), (xpos+20, ypos-60), (xpos-20, ypos-60), (xpos+20, ypos+60), (xpos-20, ypos+60)]
    for i in range(num):
        color = list(np.random.choice(range(256), size=3))
        pygame.draw.circle(screen, color, positions[i], 7)

def updatescreen(board):
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, DEEPER_TAN, pygame.Rect(160, 190, 690, 210))
    startx = 225
    starty = 340
    pygame.draw.ellipse(screen, LIGHT_TAN, (175, 215, 85, 160))
    pygame.draw.ellipse(screen, LIGHT_TAN, (750, 215, 85, 160))
    generateMarbles(board[0], 218, 297)
    compscore = board[0]
    playerscore = board[7]
    generateMarbles(board[7], 792, 297)
    for a in range(6):
        startx = startx + 80
        pygame.draw.circle(screen, LIGHT_TAN, (startx, starty), 35)
        generateMarbles(board[a+1], startx, starty)
    starty = starty - 90
    startx = 225
    for b in range(6):
        startx = startx + 80
        pygame.draw.circle(screen, LIGHT_TAN, (startx, starty), 35)
        generateMarbles(board[13 - b], startx, starty)
    numfont = pygame.font.SysFont(None, 25)
    uppernumbers = numfont.render('13             12            11            10              9              8', True, (0, 0, 0))
    lowernumbers = numfont.render('1              2              3              4               5              6', True, (0, 0, 0))
    screen.blit(uppernumbers, (295, 197))
    screen.blit(lowernumbers, (300, 377))

    compfont = pygame.font.SysFont(None, 50)
    computer = compfont.render('Computer: ' + str(compscore), True, (255, 255, 255))
    player = compfont.render('Player: ' + str(playerscore), True, (255, 255, 255))
    screen.blit(computer, (400, 135))
    screen.blit(player, (430, 425))

def click():
    x, y = pygame.mouse.get_pos()
    pot = 0
    if 470 < x < 540 and 80 < y < 120:
        if not gnode.over():
            if gnode.player == 'A':  # if the player is A
                chooseMove(Kalah, gnode, maxdepth)
                pygame.display.flip()
                gnode.move(gnode.bestMove)
                gnode.next = None
                updatescreen(gnode.board)
    if 270 < x < 340 and 305 < y < 385:
        pot = 1
    elif 345 < x < 415 and 305 < y < 385:
        pot = 2
    elif 420 < x < 490 and 305 < y < 385:
        pot = 3
    elif 495 < x < 565 and 305 < y < 385:
        pot = 4
    elif 570 < x < 640 and 305 < y < 385:
        pot = 5
    elif 645 < x < 715 and 305 < y < 385:
        pot = 6
    gnode.legalMoves()
    if pot in gnode.moves:
        if not gnode.over():
            if not gnode.player == 'A':
                gnode.move(pot)
                updatescreen(gnode.board)
                pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(0, 30, 1000, 40))
                pygame.display.flip()
                gnode.next = None

updatescreen(gnode.board)

while True:
    if not gnode.over():
        if gnode.player == 'A':
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(470, 80, 70, 40))
            chooseMove(Kalah, gnode, maxdepth)
            mssg = "Computer will play move %s" % gnode.bestMove
            nexttext = mssgfont.render("Next", True, (40, 40, 40))
        else:
            mssg = "Your moves are %s" % str(gnode.moves)
            nexttext = mssgfont.render(" ", True, (40, 40, 40))
            screen.blit(nexttext, (483, 90))
        mssgdisplay = mssgfont.render(mssg, True, (255, 255, 255))
        screen.blit(mssgdisplay, (380, 40))
        screen.blit(nexttext, (483, 90))
        pygame.display.update()
    else:
        if gnode.board[0] > gnode.board[7]:
            winningphrase = "The computer has won."
        else:
            winningphrase = "You have won!"
        mssg = "The game has ended. " + winningphrase
        mssgdisplay = mssgfont.render(mssg, True, (255, 255, 255))
        screen.blit(mssgdisplay, (300, 40))
        pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click()
    clock.tick(10)