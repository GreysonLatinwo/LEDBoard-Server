import time
import board
import neopixel
import socket, select, os, sys
import numpy as np

HOST = ''
PORT = 6969


CONNECTION_LIST = []
RECV_BUFFER = 16000

serverSocket = socket.socket(socket.AF_INET, socket. SOCK_STREAM)

CONNECTION_LIST.append(serverSocket)

try:
	serverSocket.bind((HOST, PORT))
except socket.error as err:
	print("couldnt bind with the ip")
	serverSocket.close()
	sys.exit()
serverSocket.listen()

pixel_pin = board.D18


num_pixels = 400

ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False,
                           pixel_order=ORDER)

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

def server():
	while 1:
		read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
		for sock in read_sockets:
			if sock == serverSocket:
				sockfd, addr = serverSocket.accept()
				CONNECTION_LIST.append(sockfd)
				print ("Client (%s, %s) connected" % addr)
			else:
				try:
					data = sock.recv(RECV_BUFFER).decode()
					return data
				except:
					print ("Client Disconnected")
					CONNECTION_LIST.remove(sock)
			
	return data

def makeMatrix(givenMatrix):
	wordMatrix = []
	finalMatrix = []
	count = 0
	word = ""
	for c in givenMatrix:
		if(c != ' '):
			word += c
		else:
			count += 1
			wordMatrix = np.append(wordMatrix, word)
			word = ""
			if (count > 401):
				break
	#print(wordMatrix)
	if len(wordMatrix) == 0:
		serverSocket.close()
		sys.exit()
	if len(wordMatrix) != 400:
		print(len(wordMatrix))
		return wordMatrix
	finalMatrix = np.reshape(wordMatrix, (20, 20))
	return (finalMatrix)

def drawMap(Matrix):
	print("testing...")
	for x in range(20):
		for y in range(20):
			if(int(Matrix[x][y]) == -1):
				pixels[XY(19-y, x)] = ((0,0,0))
			elif(int(Matrix[x][y]) == -2):
				pixels[XY(19-y, x)] = ((255,255,255))
			else:
				brightness = 0.5
				pixels[XY(19-y, x)] = wheel(int(Matrix[x][y]))
	pixels.show()
idleTimeStart = time.time()
while 1:
	nullLoopCount = 0
	if(idleTimeStart - time.time() >= 1000):
		idleTimeStart = time.time()
	matrixString = server()
	Matrix = makeMatrix(matrixString)
	if nullLoopCount >= 5:
		serverSocket.close()
		sys.exit()
	if len(Matrix) == 0:
		nullLoopCount += 1
	if(len(Matrix) == 20):
		print(Matrix)
		drawMap(Matrix)
