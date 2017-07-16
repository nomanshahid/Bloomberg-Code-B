import socket
import sys
import time
import math


def run(user, password, * commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    #HOST, PORT = "localhost", 17429
    data = user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data, "utf-8"))
        sfile = sock.makefile()
        rline = sfile.readline()
        returnLine = ""
        while rline:
            returnLine += rline 
            print(rline.strip())
            rline = sfile.readline()
        return returnLine

def subscribe(user, password):
    HOST, PORT = "codebb.cloudapp.net", 17429
    data = user + " " + password + "\nSUBSCRIBE\n"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data, "utf-8"))
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            print(rline.strip())
            rline = sfile.readline()
        return rline

def runit(command):
    return run("beavers", "swaglord123", command)

def gotomine(currx, curry, minex, miney):
    
    # use status to get curr x y dx dy
    # currx = 1
    # curry = 1
    # currvx = -.52
    # currvy = 2.954

    # get direction of travel
    # minex - x , miney - y
    dirx = minex - currx
    diry = miney - curry
    magdir = math.sqrt((dirx**2) + (diry**2))
    unitx = dirx/magdir
    unity = diry/magdir
    
    # find angle of wanted by using inverses
    theta1 = math.acos(unitx)
    theta2 = math.asin(unity)
    #print(str(theta1) + " " + str(theta2))

    atheta = 0
    # if case to determine pos/neg angle
    if unitx > 0 and unity > 0:
        # quadrant 1
        atheta = abs(theta1)
    elif unitx < 0 and unity > 0:
        # quadrant 2
        atheta = math.pi - abs(theta2)
    elif unitx < 0 and unity < 0:
        # quadrant 3
        atheta = math.pi + abs(theta2)
    elif unitx > 0 and unity < 0:
        # quadrant 4
        atheta = 2*math.pi - abs(theta1)
    # going along the axes
    elif unitx == 0 and unity > 0:
        # move north
        atheta = math.pi/2
    elif unitx == 0 and unity < 0:
        # move south
        atheta = 2*math.pi - math.pi/2
    elif unitx > 0 and unity == 0:
        # move east
        atheta = 0
    elif unitx < 0 and unity == 0:
        # move west
        atheta = math.pi
    elif unitx == 0 and unity == 0:
        # at mine position
        print("at mine position")

    #atheta = 2*math.pi - atheta
    return atheta

##def gotomine(currx, curry, currvx, currvy, minex, miney):
##    
##    # use status to get curr x y dx dy
##    # currx = 1
##    # curry = 1
##    # currvx = -.52
##    # currvy = 2.954
##
##    # get direction of travel
##    # minex - x , miney - y
##    dirx = minex - currx
##    diry = miney - curry
##    magdir = math.sqrt((dirx**2) + (diry**2))
##    unitx = dirx/magdir
##    unity = diry/magdir
##
##    
##
##    # normalize current velocity
##    magcurrv = math.sqrt((currvx**2) + (currvy**2))
##    unitcurrx = currvx/magcurrv
##    unitcurry = currvy/magcurrv
##    
##    # wantedX = unitX - currUnitX
##    # wantedY = unitY - currUnitY
##    ax = unitx - unitcurrx
##    ay = unity - unitcurry
##
##    # normalize wanted
##    maga = math.sqrt((ax**2) + (ay**2))
##    unitax = ax/maga
##    unitay = ay/maga
##
##    # find angle of wanted by using inverses
##    theta1 = math.acos(unitax)
##    theta2 = math.asin(unitay)
##
##    atheta = 0
##    # if case to determine pos/neg angle
##    if unitax > 0 and unitay > 0:
##        # quadrant 1
##        atheta = abs(theta1)
##    elif unitax < 0 and unitay > 0:
##        # quadrant 2
##        atheta = math.pi - abs(theta1)
##    elif unitax < 0 and unitay < 0:
##        # quadrant 3
##        atheta = math.pi + abs(theta1)
##    elif unitax > 0 and unitay < 0:
##        # quadrant 4
##        atheta = 2*math.pi - abs(theta1)
##    # going along the axes
##    elif unitax == 0 and unitay > 0:
##        # move north
##        atheta = math.pi/2
##    elif unitax == 0 and unitay < 0:
##        # move south
##        atheta = 2*math.pi - math.pi/2
##    elif unitax > 0 and unitay == 0:
##        # move east
##        atheta = 0
##    elif unitax < 0 and unitay == 0:
##        # move west
##        atheta = math.pi
##    elif unitax == 0 and unitay == 0:
##        # at mine position
##        print("at mine position")
##
## #   atheta = 2*math.pi - atheta
##    return atheta

def callFunc(status, mine_x, mine_y):
    x = float(status[1])
    y = float(status[2])

    x = 0.01
    y = 0.01
    
    vel_x = float(status[3])
    vel_y = float(status[4])
    return gotomine(x,y,vel_x,vel_y,mine_x,mine_y)
    

#run("a","a","ACCELERATE 1.57 1") #down
#run("a","a","ACCELERATE 0 1") #right
#run("a","a","ACCELERATE 3.14 1") #left
#run("a","a","ACCELERATE 4.71 1") #up
runit("ACCELERATE 5.8 1") # test
#time.sleep(2)
while 1:
    
    status = runit("STATUS")
    booL = 1
    if status.find("MINES 0") == -1:
        status = runit("STATUS")
        status2 = status.split(" ")
        x = status2.index('MINES') + 3
        y = x + 1
        tempMine = []
        while status.find("MINES 0") == -1:
            #time.sleep(2)
            #run("a","a","ACCELERATE 0 1")
            #run("a","a","BOMB " + status2[x] + " " + status2[y] + " 20")
            runit("BRAKE") 
            tempMine = [status2[x], status2[y]]
 
            time.sleep(4.5)
            status = runit("STATUS")
            status2 = status.split(" ")
            atheta = gotomine(float(status2[1]), float(status2[2]), float(tempMine[0]), float(tempMine[1]))
            print(status2[1])
            print(status2[2])
            print(tempMine[0])
            print(tempMine[1])
            print(status2)
            print("Theta: " + str(atheta))
            runit("ACCELERATE " + str(atheta) + " 1")
            time.sleep(4)
            runit("ACCELERATE 5.2 1")
            time.sleep(3)
            status = runit("STATUS")
            status2 = status.split(" ")
            runit("BOMB " + status2[1] + " " + status2[2] + " 20")
            time.sleep(7)
            #run("a", "a", "BRAKE")
            booL = 0
            break
            #booL = 0
            print(tempMine)
            ##run("a", "a", "STATUS")
            #goToCoord(status2[x], status2[y])
        

    #if booL == 0:
#        break
