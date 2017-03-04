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
        self.minesOwned = []
        self.statusMines = []
        self.scanMines = []

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
    def dropBomb(x, y, t):
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
                mineFoundIndex = self.statusMines.index([scan[currentIndex], float(status[currentIndex+1]),float(status[currentIndex+2])])
                self.statusMines.append(self.statusMines[mineFoundIndex])
                del self.statusMines[mineFoundIndex]
            except ValueError:
                self.statusMines.append([scan[currentIndex], float(status[currentIndex+1]),float(status[currentIndex+2])])
            mineFoundStatus = True
            currentIndex += 3
        return mineFoundStatus
    def updateScanMines(self, x, y):
        scan = run("SCAN " + str(x) + " " + str(y))
        if scan != "ERROR Scanning too soon":
            scan = scan.split(" ")

            mineIndex = len(scan) - scan[::-1].index("MINES") - 1

            currentIndex = mineIndex+2

            mineFoundStatus = False
            for i in range(0,int(scan[mineIndex+1])):
                try:
                    mineFoundIndex = self.scanMines.index([scan[currentIndex], float(status[currentIndex+1]),float(status[currentIndex+2])])
                    self.scanMines.append([scan[currentIndex], float(scan[currentIndex+1]),float(scan[currentIndex+2])])
                    del self.scanMines[mineFoundIndex]
                except ValueError:
                    self.scanMines.append([scan[currentIndex], float(scan[currentIndex+1]),float(scan[currentIndex+2])])
                mineFoundStatus = True
                currentIndex += 3
            return mineFoundStatus
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
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        # while rline:
        #    print(rline.strip())
        #    rline = sfile.readline()
    finally:
        print("Request complete")
    return rline

player1 = Player()
print(run("BOMB " + str(player1.x) + " " + str(player1.y)))
print(run("BOMB " + str(player1.x) + " " + str(player1.y)))

try:
    sock.sendall("CLOSE_CONNECTION\n")
finally:
    sock.close()