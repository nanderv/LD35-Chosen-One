import asyncore
import socket

class COLORS():
    BLACK="\033[30m" 
    RED  = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    BROWN = "\033[33m"
    WHITE = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

"""
Brown/Orange 0;33     Yellow        1;33
Blue         0;34     Light Blue    1;34
Purple       0;35     Light Purple  1;35
Cyan         0;36     Light Cyan    1;36
Light Gray   0;37     White         1;37
"""

OFFSET = 8
from math import *

from random import *
    

SEED = 15
overrides={}
def get_pos(x,y):
    num = sin(SEED*x*y )+sin(SEED*0.5+x*x)+cos(-SEED+y*y)
    num = num%1
    if overrides.get("{}:{}".format(x,y)):
        a =  overrides.get("{}:{}".format(x,y))
        if a == 5:
            return 0
        return a
    if abs(num) <0.1:
        return 3
    if abs(num) <0.2:
        return 0
    if abs(num) >0.9:
        return 4        
    if abs(num) >0.88:
        return 6  
    return 1
class State():

    def __init__ (self,i, state_name):
        self.name = i
        self.state_name = state_name
        self.transitions = {}

    def add_t(self,i,string,visible,to):
        self.transitions[i] =[string,visible,to]

    def handle_input(self, i,x=0,y=0,pl=None):
        if self.name == "CONTROLS":
            if i=="1":
                pl.controls="WASD"
            else:
                pl.controls="NESW"
        if self.transitions.get(i):
            return [True, self.transitions[i][2]]
        else:
            return [False, self.name]
    def print_self (self,x=0,y=0,pl=None):
        strz= "\r\n"
        for key, value in self.transitions.items():
            if value[1]: strz += key+". "+COLORS.UNDERLINE+value[0]+COLORS.WHITE+"\r\n"
        return self.state_name+ strz
DICKS = ["dick", "schlong", "penis"]
BODY = ["head", "butt", "heart", "skin", "eyes"]
KILLING = ["stomped", "kicked", "shot", "petted"]
FOODS = ["apples", "pears", "potatoes", "cows"]
DRINKS = ["apple juice", "water", "beer", COLORS.RED+"The Blood of Virgins"+COLORS.WHITE]
FS = ["you voided it's warranty.","it is no more.", "it is meeting it's maker."]
class DEADState():

    def __init__ (self,i, state_name):
        self.name = i
        self.state_name = state_name
        self.transitions = {}

    def add_t(self,i,string,visible,to):
        self.transitions[i] =[string,visible,to]

    def handle_input(self, i,x=0,y=0,pl=None):
        if self.name == "CONTROLS":
            if i=="1":
                pl.controls="WASD"
            else:
                pl.controls="NESW"
        if self.transitions.get(i):
            return [True, self.transitions[i][2]]
        else:
            return [False, self.name]
    def print_self (self,x=0,y=0,pl=None):
        strz= "\r\n"
        if not hasattr(pl,"a"):
            pl.a = 1
        pl.a=pl.a +1
        for key, value in self.transitions.items():
            if value[1]: strz += key+". "+COLORS.UNDERLINE+value[0]+COLORS.WHITE+"\r\n"
        line1= "You found a {}{}, but {} it, so now it's dead.".format(
            DICKS[randrange(0,3)],
            BODY[randrange(0,4)],
            KILLING[randrange(0,4)])
        line2= "It used to love eating {}, and drinking {}.".format(FOODS[randrange(0,4)],DRINKS[randrange(0,4)])
        line3= "It's weight was {} kg, and it was {} cm tall.".format(randrange(3,15)*randrange(3,15),randrange(5,25)*randrange(5,25))
        line4= "You're pretty sure {}".format(FS[randrange(0,FS.__len__())])
        return line1+"\r\n"+line2+"\r\n"+line3+"\r\n"+line4+"\r\n"+ strz

def try_to_move(x,y):
    if get_pos(x,y) == 0:
         return None, None

    return x,y
class MapState():
    def __init__ (self,i, state_name):
        self.name = i
        self.state_name = state_name
        self.transitions = {}

    def add_t(self,i,string,visible,to):
        self.transitions[i] =[string,visible,to]

    def handle_input(self, i,x,y,pl):
        mvd = False
        xx=None
        if pl.controls =="NESW":
            if i == "N" or i == "n":
                mvd = True
                xx,yy = try_to_move(x,y-1)
            if i == "E" or i == "e":
                xx,yy = try_to_move(x+1,y)
                mvd = True
            if i == "S" or i == "s":
                xx,yy =  try_to_move(x,y+1)
                mvd = True
            if i == "W" or i == "w":
                xx,yy = try_to_move(x-1,y)
                mvd = True
        else:
            if i == "W" or i == "w":
                mvd = True
                xx,yy = try_to_move(x,y-1)
            if i == "D" or i == "d":
                xx,yy = try_to_move(x+1,y)
                mvd = True
            if i == "S" or i == "s":
                xx,yy =  try_to_move(x,y+1)
                mvd = True
            if i == "A" or i == "a":
                xx,yy = try_to_move(x-1,y)
                mvd = True
        if get_pos(x,y) ==3:
            pl.water = pl.water+10
            overrides["{}:{}".format(x,y)]=1
        elif get_pos(x,y) ==4:
            pl.food = pl.food+10
            overrides["{}:{}".format(x,y)]=1
        if i == "M" or i == "m":
            
            if get_pos(x+1,y) ==0:
                pl.food = pl.food - 1
                pl.water = pl.water - 1
                overrides["{}:{}".format(x+1,y)]=1
                pl.blocks = pl.blocks+1
                
            if get_pos(x-1,y) ==0:    
                pl.food = pl.food - 1
                pl.water = pl.water - 1
                overrides["{}:{}".format(x-1,y)]=1
                pl.blocks = pl.blocks+1
                
            if get_pos(x,y+1) ==0:
                pl.food = pl.food - 1
                pl.water = pl.water - 1
                
                overrides["{}:{}".format(x,y+1)]=1
                pl.blocks = pl.blocks+1
                
            if get_pos(x,y-1) ==0:
                pl.food = pl.food - 1
                pl.water = pl.water - 1
                mined = 1
                overrides["{}:{}".format(x,y-1)]=1
                pl.blocks = pl.blocks+1
            


            return [True, self.name,x,y]
        if i == "P" or i == "p" and pl.blocks > 0 and get_pos(x,y)!=0:
            overrides["{}:{}".format(x,y)]=5
            pl.blocks -= 1
            return [True, self.name,x,y]
        if xx is None:
            xx = x
            yy = y
        if get_pos(xx,yy) ==6:
           overrides["{}:{}".format(xx,yy)]=1
           return [True, "DEAD",x,y]



        if mvd:
            pl.food = pl.food  -1
            pl.water = pl.water-1
            if pl.food < 0:
                pl.x = pl.startx+randrange(-10,10)
                pl.y = pl.starty+randrange(-10,10)
                pl.water = 40
                pl.food = 40
                return [True, "NOFOOD",xx,yy]
            if pl.water < 0:
                pl.x = pl.startx+randrange(-10,10)
                pl.y = pl.starty+randrange(-10,10)
                pl.water = 40
                pl.food = 40
                return [True, "NOWATER",xx,yy]        
                

            if get_pos(xx,yy) == 2  and not pl.found.get("{}:{}".format(xx,yy)):
                if specials.get("{}:{}".format(xx,yy)):
                    pl.found["{}:{}".format(xx,yy)]=True
                    return [True, specials.get("{}:{}".format(xx,yy)),xx,yy]        



            return [True, self.name,xx,yy]
        if self.transitions.get(i):
            return [True, self.transitions[i][2],xx,yy]
        else:
            return [False, self.name,xx,yy]
    def print_self (self, xx, yy, pl):
        strz= "\r\n"
        cur = ""
        animals = []
        for y in range(yy-OFFSET, yy+OFFSET):
            for x in range(xx-OFFSET, xx+OFFSET):
                val = get_pos(x,y)
                char = " "
                if val == 0:
                    char = COLORS.BROWN+"#"+COLORS.WHITE
                if val == 2 and not pl.found.get("{}:{}".format(x,y)):
                    char = "?"
                if val == 3:
                    char = COLORS.BLUE+"#"+COLORS.WHITE
                if val == 4:
                    char = COLORS.GREEN+"#"+COLORS.WHITE
                if x == xx and y == yy:
                    cur = char
                    char = "O"
                if pl.mx ==x and pl.my == y:
                    char = COLORS.RED+"M"+COLORS.WHITE
                if val == 6:
                    char = "^"
                    direction = randrange(1,8)
                    if direction == 1 and get_pos(x+1,y)==1:
                       overrides["{}:{}".format(x,y)]=1
                       animals.append([x+1,y])
                    if direction == 2 and get_pos(x-1,y)==1:
                       overrides["{}:{}".format(x,y)]=1
                       animals.append([x-1,y])
                    if direction == 3 and get_pos(x,y+1)==1:
                       overrides["{}:{}".format(x,y)]=1
                       animals.append([x,y+1])
                    if direction == 4 and get_pos(x,y-1)==1:
                       overrides["{}:{}".format(x,y)]=1
                       animals.append([x,y-1])
                strz += char
            strz += "\r\n"

        for i in range(0,animals.__len__()):
            a = animals[i]
            overrides["{}:{}".format(a[0],a[1])]=6

        for key, value in self.transitions.items():
            if value[1]: strz += key+". "+COLORS.UNDERLINE+value[0]+COLORS.WHITE+"\r\n\r\n"
        
        return "\033[2J\033[0;0H"+self.state_name +"@{}:{}\r\nFood: {} Water: {} Blocks: {} Ground: {}\n\r? for help:".format(xx,yy,pl.food,pl.water,pl.blocks,cur)+ strz


class BookState():
    def __init__ (self,i, state_name):
        self.name = i
        self.state_name = state_name
        self.transitions = {}


    def add_t(self,i,string,visible,to):
        self.transitions[i] =[string,visible,to]

    def handle_input(self, ii,x,y,pl):
        pl.on_page = pl.on_page+1


        while pl.on_page < pl.story.__len__() and pl.story[pl.on_page] =="":
            pl.on_page = pl.on_page+1
        last_page=True
        for i in range(pl.on_page,pl.story.__len__()):
            if pl.story[i] != "":
                last_page = False
        if ii == "2" or last_page:
            pl.on_page = 0
            return [True, self.transitions["1"][2],x,y]
        return [True, self.name,x,y]
        
    def print_self (self, xx, yy, pl):
        strz= "\r\n"
        page = pl.story[pl.on_page]


        strz = strz + page
        last_page=True
        for i in range(pl.on_page+1,pl.story.__len__()):
            if pl.story[i] != "":
                last_page = False
        if last_page:
            strz=strz+COLORS.UNDERLINE+"\r\n\r\n1. Close book"+COLORS.WHITE
        else:
            strz=strz+COLORS.UNDERLINE+"\r\n\r\n1. Next Page"+COLORS.WHITE
            strz=strz+COLORS.UNDERLINE+"\r\n2. Close Book"+COLORS.WHITE
        return "\033[2J\033[0;0H"+self.state_name + strz
states = {}
states["START"] = State("START", "\033[137mWelcome to No Man's Land. This is a game about exploration of an infinite world.\r\tThis game is big, really big. Walk into food and water tiles to consume them.\r\t This game has limited inventory management by not having an inventory.\r\n You kan kill monsters in this game, kill pirates etc.\r\nAlso, this game has multiplayer.")
states["START"].add_t("1","Controls",True,"CONTROLS")
states["CONTROLS"] = State("CONTROLS", "Use either W A S D, or N E S W, followed by a carriage return (Enter) to move.\r\n For obvious reasons you have to choose now.\r\nAdditional controls: H to harvest, M to mine, P to place blocks\r\nMining mines adjecent blocks and takes one food and one water per block mined.\r\n You can only place blocks on empty tiles, otherwise the command will return as not understood.")
states["CONTROLS"].add_t("1","Start Game using WASD (Modern)",True,"MAP")
states["CONTROLS"].add_t("2","Start Game using NESW (Old-School)",True,"MAP")

states["NOFOOD"] = State("NOFOOD", "\033[137mYou died of starvation")
states["NOFOOD"].add_t("1","Controls",True,"START")
states["NOWATER"] = State("NOFOOD", "\033[137mYou died of dehydration")
states["NOWATER"].add_t("1","Controls",True,"START")
states["MAP"] = MapState("MAP","No mans land.")
states["MAP"].add_t("?","Controls",True,"CONTROLS")

states["DEAD"] = DEADState("DEAD","\033[2J\033[0;0H\033[137mYou found a, but stomped it and now it's dead.")
states["DEAD"].add_t("1","Continue on",True,"MAP")
states["DEAD"].add_t("2","Mourn",True,"MOURN")
states["MOURN"] = State("MOURN","\033[137mYou should have thought about that before killing such an innocent creature.")
states["MOURN"].add_t("1","Continue on",True,"MAP")
def state(i):
    return states[i]
class MainServerSocket(asyncore.dispatcher):
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('',port))
        self.listen(5)
    def handle_accept(self):
        newSocket, address = self.accept(  )
        print ("Connected from", address)
        sock = SecondaryServerSocket(newSocket)
        sock.start()

class SecondaryServerSocket(asyncore.dispatcher_with_send):
    def start(self):
        self.state="START"
        self.buff = ""
        self.x =  randrange(-20,20)
        self.y =  randrange(-20,20)
        self.startx = self.x
        self.starty = self.y
        self.mx = -10
        self.my = 0
        self.mstate = 0
        self.food=60
        self.water=60
        self.blocks = 0
        


        self.found={}
        self.story=["I.\r\n\r\n No Pages Yet",
        "","","","","","","","","","","","","","","","","","","","","","","","","",""]
        self.send(states[self.state].print_self(self.x,self.y,self))
        self.on_page = 0

    def handle_read(self):
        receivedData = self.recv(8192)
        if receivedData: 
            if hasattr(states[self.state],"story_id"):
                self.story[states[self.state].story_id] = states[self.state].state_name
            
            olen = receivedData.__len__()

            receivedData= receivedData.replace("\n", "").replace("\r","")
            olen = olen -  receivedData.__len__()
            if receivedData != "":
                if olen ==0:
                    self.buff = self.buff + receivedData
                else:
                    res = states[self.state].handle_input(receivedData,self.x,self.y,self)
                    self.state=res[1]
                    if res.__len__()>2:
                        self.x = res[2]
                        self.y = res[3]
                    if res[0]:
                        self.send(states[self.state].print_self(self.x,self.y,self))
                    else:
                        self.send(states[self.state].print_self(self.x,self.y,self))

                        self.send("<"+receivedData + "> was not understood\r\n")
            elif self.buff != "":

                res = states[self.state].handle_input(self.buff,self.x,self.y,self)
                self.state=res[1]
                if res.__len__()>2:
                    self.x = res[2]
                    self.y = res[3]
                if res[0]:
                    self.send(states[self.state].print_self(self.x,self.y,self))
                else:

                    self.send(states[self.state].print_self(self.x,self.y,self))

                    self.send("<"+self.buff + "> was not understood.\r\n")
                self.buff = ""
        else: self.close(  )
    def handle_close(self):
        print ("Disconnected from", self.getpeername(  ))

MainServerSocket(8944)
asyncore.loop(  )
