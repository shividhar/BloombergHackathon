import socket
import sys
import time
import math

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST, PORT = "codebb.cloudapp.net", 17429
sock.connect((HOST, PORT))

sock.sendall("4geese gee4se \n")

def config():
    print(run("CONFIGURATIONS"))


class Player:
    def __init__(self):
        status = run("STATUS")
        status = status.split(" ")
        self.x = float(status[1])
        self.y = float(status[2])
        self.speedX = float(status[3])
        self.speedY = float(status[4])
        self.statusMines = []
        self.scanMines = []
        self.startTime = time.time()

        mineIndex = len(status) - status[::-1].index("MINES") - 1

        currentIndex = mineIndex+2
        for i in range(0,int(status[mineIndex+1])):
            self.statusMines.append([status[currentIndex+1], status[currentIndex+2]])
            currentIndex += 3
    def update(self):
        status = run("STATUS")
        status = status.split(" ")
        self.x = float(status[1])
        self.y = float(status[2])
        self.speedX = float(status[3])
        self.speedY = float(status[4])
    def accelerate(self, angle, magnitude):
        run("ACCELERATE " + str(angle) + " " + str(magnitude))
    def brake(self):
        run("BRAKE")
    def dropBomb(self, x, y, t):
        run("BOMB " + str(x) + " " + str(y) + " " + str(t))
    def addMine(self, owner, x, y):
        self.minesOwned.append([owner, float(x), float(y)])
    def updateStatusMines(self):
        # status = ["A", "B", "MINES", "3", "0", "0", "0", "1", "1", "1", "2", "2", "2"]
        status = run("STATUS")
        status = status.split(" ")
        mineIndex = len(status) - status[::-1].index("MINES") - 1

        currentIndex = mineIndex+2

        mineFoundStatus = False
        for i in range(0,int(status[mineIndex+1])):
            try:
                mineFoundIndex = self.statusMines.index([status[currentIndex], float(status[currentIndex+1]),float(status[currentIndex+2])])
                self.statusMines.append(self.statusMines[mineFoundIndex])
                del self.statusMines[mineFoundIndex]
            except ValueError:
                self.statusMines.append([status[currentIndex], float(status[currentIndex+1]),float(status[currentIndex+2])])
            mineFoundStatus = True
            currentIndex += 3
        return mineFoundStatus
    # def updateScanMines(self, x, y):
    #     scan = run("SCAN " + str(x) + " " + str(y))
    #     if scan != "ERROR Scanning too soon":
    #         scan = scan.split(" ")

    #         mineIndex = len(scan) - scan[::-1].index("MINES") - 1

    #         currentIndex = mineIndex+2

    #         mineFoundStatus = False
    #         for i in range(0,int(scan[mineIndex+1])):
    #             try:
    #                 mineFoundIndex = self.scanMines.index([scan[currentIndex], float(status[currentIndex+1]),float(status[currentIndex+2])])
    #                 self.scanMines.append([scan[currentIndex], float(scan[currentIndex+1]),float(scan[currentIndex+2])])
    #                 del self.scanMines[mineFoundIndex]
    #             except ValueError:
    #                 self.scanMines.append([scan[currentIndex], float(scan[currentIndex+1]),float(scan[currentIndex+2])])
    #             mineFoundStatus = True
    #             currentIndex += 3
    #         return mineFoundStatus
    #     else:
    #         print("SCANNING TOO SOON")
    def scanMineLocation(self, x, y):
        scan = run("SCAN " + x + " " + y + " " + index)
        if scan != "ERROR Scanning too soon":
            scan = scan.split(" ")

            mineIndex = len(scan) - scan[::-1].index("MINES") - 1

            currentIndex = mineIndex+2
            for i in range(0,int(scan[mineIndex+1])):
                try:
                    scanX = float(status[currentIndex+1])
                    scanY = float(status[currentIndex+2])

                    statusMineIndex = self.statusMines.index([scan[currentIndex], scanX, scanY])
                    scanMineLocation = self.scanMines.index([scan[currentIndex], scanX, scanY])
                    if self.statusMines[mineIndex][0] != "4geese":
                        self.scanMines.append([scan[currentIndex], scanX, scanY, math.sqrt((self.x-scanX)**2) + (self.y-scanY)**2])
                    elif self.scanMines[scanMineLocation][0] == "4geese":
                        del self.scanMines[scanMineLocation]
                except ValueError:

            sorted(self.scanMines,key=lambda x: (x[3]))
            return True
        else:
            return False

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
    player1.updateStatusMines()
    print(mx, my, player1.statusMines)
    for i in range(0, len(player1.statusMines)):
        if (mx == player1.statusMines[i][1] and my == player1.statusMines[i][2]):
            return player1.statusMines[i][0]
    return ""

def takeMine(mx, my):
    player1 = Player()
    player1.brake()
    while True:
        player1.update()
        if(math.fabs(float(player1.speedX)) < 0.5 and math.fabs(float(player1.speedY)) < 0.5):
            break

    while True:
        angle = math.atan2(my - float(player1.y), mx - float(player1.x))
        #print(getMineOwner(mx, my, player1))
        player1.accelerate(angle, 0.8)
        if player1.updateStatusMines():
            break
        if str(getMineOwner(mx, my, player1)) == "4geese":
            print("WTFEBVDJBVJDH ACCELERATE MOTHERFUCKER")
            return [mx, my]
    return [-1, -1]

def scanVisitedMines(playerObject):




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

statusListIndex = 0

while True:
    player1 = Player()
    #print("blah", float(player1.x), float(x)+300)

    if player1.updateStatusMines():
        print("IM FUCKING CLOSE")
        if str(getMineOwner(player1.statusMines[-1][1], player1.statusMines[-1][2], player1)) != "4geese":
            print("it's not our")
            takeMine(player1.statusMines[-1][1], player1.statusMines[-1][2])

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

    if hzr and float(player1.x) < float(x):
        x = player1.x
        y = player1.y

    if hzl and float(player1.x) > float(x):
        x = player1.x
        y = player1.y

    if vu and float(player1.y) > float(y):
        x = player1.x
        y = player1.y

    if vd and float(player1.y) < float(y):
        x = player1.x
        y = player1.y

    if vd and (not player1.updateStatusMines() or (player1.updateStatusMines() and str(getMineOwner(player1.statusMines[-1][1], player1.statusMines[-1][2], player1)) == "4geese")):
        player1.dropBomb(float(player1.x), float(player1.y) - 4, 25)
    if vu and (not player1.updateStatusMines() or (player1.updateStatusMines() and str(getMineOwner(player1.statusMines[-1][1], player1.statusMines[-1][2], player1)) == "4geese")):
        player1.dropBomb(float(player1.x), float(player1.y) + 4, 25)
    if hzl and (not player1.updateStatusMines() or (player1.updateStatusMines() and str(getMineOwner(player1.statusMines[-1][1], player1.statusMines[-1][2], player1)) == "4geese")):
        player1.dropBomb(float(player1.x) + 4, float(player1.y), 25)
    if hzr and (not player1.updateStatusMines() or (player1.updateStatusMines() and str(getMineOwner(player1.statusMines[-1][1], player1.statusMines[-1][2], player1)) == "4geese")):
        player1.dropBomb(float(player1.x) - 4, float(player1.y), 25)

    if statusListIndex < len(player1.statusMines) and len(player1.statusMines) > 6:
        scanStatus = player1.scanMineLocation(player1.statusMines[statusListIndex])
        if scanStatus == True:
            statusListIndex += 1
    else:
        statusListIndex = 0


try:
	sock.sendall("CLOSE_CONNECTION\n")
finally:
	sock.close()
