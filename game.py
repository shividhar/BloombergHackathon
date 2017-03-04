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
    def dropBomb(x, y, t):
        run("BOMB " + str(x) + " " + str(y) + " " + str(t))
    def addMine(self, owner, x, y):
        self.minesOwned.append([owner, float(x), float(y)])

class Mines:
    def __init__(self):
        self.statusMines = []
        self.scanMines = []

        status = run("STATUS")
        status = status.split(" ")

        mineIndex = len(status) - status[::-1].index("MINES") - 1

        currentIndex = mineIndex+2

        for i in range(0,int(status[mineIndex+1])):
            self.statusMines.append([status[currentIndex+1], status[currentIndex+2]])
            currentIndex += 3
    def updateStatusMines(self):
    	# status = ["A", "B", "MINES", "3", "0", "0", "0", "1", "1", "1", "2", "2", "2"]
        status = run("STATUS")
        status = status.split(" ")
    	mineIndex = len(status) - status[::-1].index("MINES") - 1

        currentIndex = mineIndex+2
        mineFound = False
        for i in range(0,int(status[mineIndex+1])):
            self.statusMines.append([float(status[currentIndex+1]),float(status[currentIndex+2])])
            currentIndex += 3
            mineFound = True
        return mineFound
    def updateScanMines(self, x, y):
	    scan = run("SCAN " + str(x) + " " + str(y))
	    if scan != "ERROR Scanning too soon":
	    	scan = scan.split(" ")

	    	mineIndex = len(scan) - scan[::-1].index("MINES") - 1

	    	currentIndex = mineIndex+2
            mineFound = False
	    	for i in range(0,int(scan[mineIndex+1])):
	            self.scanMines.append([scan[currentIndex], float(scan[currentIndex+1]),float(scan[currentIndex+2])])
	            currentIndex += 3
                mineFound = True
            return mineFound
	    else:
	    	print("SCANNING TOO SOON")

class Bombs:
    def __init__(self):
        self.bombs = []
        status = run("STATUS")
        status = status.split(" ")

        bombIndex = len(status) - status[::-1].index("BOMBS") - 1

        currentIndex = bombIndex+2

        for i in range(0,int(status[bombIndex+1])):
            self.bombs.append([float(status[currentIndex]),float(status[currentIndex+1])])
            currentIndex += 2
    def update(self):
        status = run("STATUS")
        status = status.split(" ")

        bombIndex = len(status) - status[::-1].index("BOMBS") - 1

        currentIndex = bombsIndex+1

        for i in range(0,int(status[bombIndex+1])):
            self.bombs.append([float(status[currentIndex]),float(status[currentIndex+1])])
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


def getMineOwner(mx, my, player1):

    for i in range(0, len(player1.mines)):
        if mx == player1.mines[i][1] and my == player1.mines[i][2]
            return player1.mines[i][0]
    return ""
def takeMine(mx, my):
    player1 = new Player()
    player1.brake()
    while True:
        angle = math.atan2(my - player1.y, mx - player2.x)
        player1.accelerate(0.1, -angle)
        if getMineOwner(mx, my) == "4geese":
            return [mx, my]

    return [-1, -1]

HOST, PORT = "codebb.cloudapp.net", 17429
sock.connect((HOST, PORT))
sock.sendall("4geese gee4se \n")


player1 = Player()
#player1.accelerate(-1.57, 1)
player1.accelerate(0, 0.8)
#print("stop")
x = player1.x
y = player1.y
n=0
d = 1
hzr = True
hzl = False
vu = False
vd = False
a = [-math.pi/2, math.pi, math.pi/2, 0]
while True:
    player1 = Player()
    #print("blah", float(player1.x), float(x)+300)
    if hzr and math.fabs(float(player1.x) - float(x) - 300*d) < 100:
        print("STOPXR")
        x = player1.x
        y = player1.y
        if n%2 == 0:
            d *= 2;
        player1.brake()
        player1.accelerate(a[n%4], 0.8)
        hzr = False
        vu = True
        n+=1
        #print(n, hz, x, y)

    if vu and math.fabs( - float(player1.y) + float(y) - 300*d) < 100:
        print("STOPY")
        x = player1.x
        y = player1.y
        if n%2 == 0:
            d *= 2;
        player1.brake()
        player1.accelerate(a[n%4], 0.8)
        vu = False
        hzl = True
        n+=1

    if hzl and math.fabs(-float(player1.x) + float(x) - 300*d) < 100:
        print("STOPX")
        x = player1.x
        y = player1.y
        if n%2 == 0:
            d *= 2;
        player1.brake()
        player1.accelerate(a[n%4], 0.8)
        hzl = False
        vd = True
        n+=1
        #print(n, hz, x, y)

    if vd and math.fabs( float(player1.y) - float(y) - 300*d) < 100:
        print("STOPY")
        x = player1.x
        y = player1.y
        if n%2 == 0:
            d *= 2;
        player1.brake()
        player1.accelerate(a[n%4], 0.8)
        vd = False
        hzr = True
        n+=1

print(player1.x, player1.y)
#print(player1.speedY)

try:
	sock.sendall("CLOSE_CONNECTION\n")
finally:
	sock.close()
