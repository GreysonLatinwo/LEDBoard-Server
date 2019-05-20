import time
import board
import neopixel
import Server
import sys, os, select
import numpy as np

pixel_pin = board.D18

num_pixels = 400

ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False,
                           pixel_order=ORDER)
print("Started")
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (0, r, g, b)

def XY(x, y):
        if(y & 0x01):
                reverseX = (20 -1) - x
                i = (y* 20)+reverseX
        else:
                i = (y * 20) + x
        return i


def makeMatrix(givenMatrix):
        wordMatrix = []
        finalMatrix = []
        count = 0
        word = ""
        #print(givenMatrix)
        for c in givenMatrix:
                if(c != ' '):
                        word += c
                else:
                        count += 1
                        wordMatrix = np.append(wordMatrix, word)
                        word = ""
                        if (count > 400):
                                break
        #print(wordMatrix)
        if len(wordMatrix) == 0:
                sys.exit()
        if len(wordMatrix) != 400:
                print(len(wordMatrix))
                return wordMatrix
        finalMatrix = np.reshape(wordMatrix, (20, 20))
        print("matrix created")
        return (finalMatrix)

def updateBoard(Matrix):
        for x in range(20):
                for y in range(20):
                        if(int(Matrix[x][y]) == -1):
                                pixels[XY(19-y, x)] = ((0,0,0))
                        elif(int(Matrix[x][y]) == -2):
                                pixels[XY(19-y, x)] = ((255,255,255))
                        elif(int(Matrix[x][y]) == -3):
                                pixels[XY(19-y, x)] = ((32,32,32))
                        elif(int(Matrix[x][y]) == -4):
                                pixels[XY(19-y, x)] = ((64,64,64))
                        elif(int(Matrix[x][y]) == -5):
                                pixels[XY(19-y, x)] = ((96,96,96))
                        elif(int(Matrix[x][y]) == -6):
                                pixels[XY(19-y, x)] = ((128,128,128))
                        elif(int(Matrix[x][y]) == -7):
                                pixels[XY(19-y, x)] = ((160,160,160))
                        elif(int(Matrix[x][y]) == -8):
                                pixels[XY(19-y, x)] = ((192,192,192))
                        elif(int(Matrix[x][y]) == -9):
                                pixels[XY(19-y, x)] = ((224,224,224))
                        else:
                                pixels[XY(19-y, x)] = wheel(int(Matrix[x][y]))
        pixels.show()

def drawMatrix(Matrix):
        for x in range(20):
                for y in range(20):
                        print(Matrix[x][y], end='')
                print( )

while 1:
        server = Server.socketServer()
        matrixString = server.startServer()
        Matrix = makeMatrix(matrixString)
        if(len(Matrix) == 20):
                drawMatrix(Matrix)
                updateBoard(Matrix)