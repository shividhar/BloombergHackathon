import socket
import sys
import time
import math
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Player:
    def __init__(self):
        status = run("STATUS")
        status = status.split(" ")
        self.x = status[1]
        self.y = status[2]
        self.speedX = status[3]
        self.speedY = status[4]
        self.minesOwned = []
    def update(self):
        status = run("4geese", "gee4se")
        self.x = status[1]
        self.y = status[2]
        self.speedX = status[3]
        self.speedY = status[4]
    def accelerate(self, angle, magnitude):
        run("ACCELERATE " + str(angle) + " " + str(magnitude))
    def brake(self):
        run("BRAKE")
    def addMine(self, x, y):
        self.minesOwned.append([x, y])

class Mines:
    def __init__(self):
        self.mines = []
    def addMine(self, x,y):
        self.mines.append([x, y])
class Bombs:
    def __init__(self):
        self.bombs = []
        status = run("STATUS")
        status = status.split(" ")

        bombsIndex = len(status) - status[::-1].index("BOMBS") - 1

        currentIndex = bombsIndex+1
        for i in range(0,status[bombsIndex+1]):
            self.bombs([currentIndex, currentIndex+1])
            currentIndex += 2
    def update(self):
        status = run("STATUS")
        status = status.split(" ")

        bombsIndex = len(status) - status[::-1].index("BOMBS") - 1

        currentIndex = bombsIndex+1
        for i in range(0,status[bombsIndex+1]):
            self.bombs([currentIndex, currentIndex+1])
            currentIndex += 2


def run(commands):

    #data= "4geese gee4se \n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"
    data = commands + "\n"
    # HOST, PORT = "localhost", 17429
    # data= "a a \n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"
    rline = ""
    try:
#        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        #while rline:
            #print(rline.strip())
            #rline = sfile.readline()
    finally:
        print("Request complete")
        #print(rline)
        #sock.close()

    return rline

HOST, PORT = "codebb.cloudapp.net", 17429
sock.connect((HOST, PORT))
sock.sendall("4geese gee4se \n")


player1 = Player()
#player1.accelerate(-1.57, 1)
player1.brake()
#player1.accelerate(0, 0.3)
#print("stop")
x = player1.x
y = player1.y
n=0
d = 1
hz = True;
a = [-math.pi/2, math.pi, math.pi/2, 0]
while True:
    player1 = Player()
    #print("blah", float(player1.x), float(x)+300)
    if hz and math.fabs(float(player1.x) - float(x) - 300*d) < 100:
        print("STOPX")
        x = player1.x
        y = player1.y
        if n%2 == 0:
            d *= 2;
        run("BRAKE")
        player1.accelerate(a[n%4], 0.3)
        hz = False
        n+=1
        print(n, hz, x, y)

    if not(hz) and math.fabs( - float(player1.y) + float(y) - 300*d) < 100:
        print("STOPY")
        x = player1.x
        y = player1.y
        if n%2 == 0:
            d *= 2;
        run("BRAKE")
        player1.accelerate(a[n%4], 0.3)
        hz = True
        n+=1

print(player1.x, player1.y)
#print(player1.speedY)

try:
	sock.sendall("CLOSE_CONNECTION\n")
finally:
	sock.close()
