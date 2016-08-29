import asyncore
import socket

class COLORS():
    BLACK="\033[30m" 
    RED  = "\033[31m"
    GREEN = "\033[32m"
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
specials= {}
specials["16:14"]="C1"
specials["10:11"]="C2"
specials["9:19"]="C3"
specials["22:3"]="C4"
specials["12:20"]="C5"
specials["0:0"]="C9"
"""
16,14 Start
10,11 First Junction
22,3  End north of first junction
9, 19 South of first junction
13,20 Before the rotation
21,26 Circle
28,10 Near the end
0, 0  The end
32,0  Near the end
"""
OFFSET = 8
maze = [[2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,0,1,2,1,0,1,0,1,0,0,1,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,1,0,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,0,1,0,0,1],
        [0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,0,1,0,1,0,1,1,1,1],
        [0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,1],
        [1,1,1,0,0,0,1,1,1,0,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,1],
        [1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
        [0,0,1,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,1,0,0,0,1,1,1,1,2,1,1,1,1,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,1,1,0,0,0,1,1,1,0,0,0,0,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1],
        [1,1,1,1,0,1,1,1,1,0,1,0,0,0,1,1,2,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1],
        [0,1,0,0,0,0,0,0,1,0,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0],
        [1,1,0,1,1,1,1,1,1,0,1,0,0,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1],
        [0,1,0,1,0,0,0,0,0,0,1,0,1,0,1,1,1,1,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0],
        [1,1,1,1,1,1,0,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1],
        [0,0,0,0,1,0,1,1,1,2,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1],
        [1,1,1,1,1,0,1,0,1,1,1,0,2,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1],
        [1,0,0,0,1,0,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [1,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0],
        [1,1,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0],
        [1,0,1,1,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,0],
        [1,0,1,0,0,0,0,1,0,0,1,0,0,1,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,1,0,0],
        [1,1,1,0,1,1,0,1,0,0,1,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,0,1,0,1],
        [1,0,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,1,1,1,0,1],
        [1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,0,0,1,0,1],
        [1,0,1,0,0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,1,0,1],
        [1,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1],
        [1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0]
    ]

def been():
    w=33
    h=33
    return [[0 for x in range(w)] for y in range(h)] 
    
def bfs(xx,yy,tox,toy):
    neighbours = []
    b = been()
    search = 150
    if [xx,yy] == [tox,toy]:
        return "",0
    x,y = xx,yy
    ind = 0
    if get_pos(x+1,y) != 0:
        neighbours.append([x+1,y,"R",1])
    if get_pos(x-1,y) != 0:
        neighbours.append([x-1,y,"L",1])
    if get_pos(x,y+1) != 0:
        neighbours.append([x,y+1,"D",1])
    if get_pos(x,y-1) != 0:
        neighbours.append([x,y-1,"U",1])

    while ind < neighbours.__len__():
        search=search-1
        if search < 0:
            return " ",a[3]
        a = neighbours[ind]
        x,y = a[0],a[1]
        if [x,y] == [tox,toy]:
            return a[2],a[3]

        if get_pos(x+1,y) != 0 and not b[y][x+1]:
            neighbours.append([x+1,y,a[2],a[3]+1])
            b[y][x+1]=1

        if x>= 0 and get_pos(x-1,y) != 0 and not b[y][x-1]:
            neighbours.append([x-1,y,a[2],a[3]+1])
            b[y][x-1]=1
        if get_pos(x,y+1) != 0 and not b[y+1][x]:
            neighbours.append([x,y+1,a[2],a[3]+1])
            b[y+1][x]=1
        if get_pos(x,y-1) != 0 and not b[y-1][x]:
            neighbours.append([x,y-1,a[2],a[3]+1])
            b[y-1][x]=1
        ind += 1
    return "", 10000

def get_pos(x,y):
    if x<0 and y==0:
        return 1
    if x >= 0  and x < maze[0].__len__():
        if y>= 0 and y < maze.__len__():
            return maze[y][x]
    return 0
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
        if x < -5:
            return [True, "END2",x,y]
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
        if xx is None:
            xx = x
            yy = y
        if i == "BOOK" or i =="B" or i=="b" or i =="book":
            return [True, "BOOK",xx,yy]

        if mvd:
            if get_pos(xx,yy) == 2  and not pl.found.get("{}:{}".format(xx,yy)):
                if specials.get("{}:{}".format(xx,yy)):
                    pl.found["{}:{}".format(xx,yy)]=True
                    return [True, specials.get("{}:{}".format(xx,yy)),xx,yy]        
            mv,dst = bfs(pl.mx,pl.my,pl.x,pl.y)
            mvd = False
            if mv =="L":
                pl.mx = pl.mx - 1
                mvd = True
            if mv =="R":
                pl.mx = pl.mx + 1
                mvd = True
            if mv =="U":
                pl.my = pl.my - 1
                mvd = True
            if mv =="D":
                pl.my = pl.my + 1
                mvd = True
            if dst <= 1:
                if pl.mstate != -34:
                    pl.mstate = -34

                    return [True, "MONSTER5",xx,yy]
            else:
                if mvd:
                    if pl.mstate == 0:
                        pl.mstate += 1
                        return [True, "MONSTER1",xx,yy]
                    if pl.mstate == 1 and dst < 50:
                        pl.mstate += 1
                        return [True, "MONSTER2",xx,yy]
                    if pl.mstate == 2 and dst < 5:
                        pl.mstate += 1
                        return [True, "MONSTER3",xx,yy]
                    if pl.mstate == 3 and dst < 2:
                        pl.mstate += 1
                        return [True, "MONSTER4",xx,yy]


            return [True, self.name,xx,yy]
        if self.transitions.get(i):
            return [True, self.transitions[i][2],xx,yy]
        else:
            return [False, self.name,xx,yy]
    def print_self (self, xx, yy, pl):
        strz= "\r\n"

        for y in range(yy-OFFSET, yy+OFFSET):
            for x in range(xx-OFFSET, xx+OFFSET):
                val = get_pos(x,y)
                char = " "
                if val == 0:
                    char = COLORS.BROWN+"#"+COLORS.WHITE
                if val == 2 and not pl.found.get("{}:{}".format(x,y)):
                    char = "?"

                if x == xx and y == yy:
                    char = "O"
                if pl.mx ==x and pl.my == y:
                    char = COLORS.RED+"M"+COLORS.WHITE

                strz += char
            strz += "\r\n"
        for key, value in self.transitions.items():
            if value[1]: strz += key+". "+COLORS.UNDERLINE+value[0]+COLORS.WHITE+"\r\n\r\n"
        return "\033[2J\033[0;0H"+self.state_name +"@{}:{}".format(xx,yy)+ strz


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
states["START"] = State("START",
" _____ _            _____ _                            _____            \r\n"+
"|_   _| |          /  __ \ |                          |  _  |           \r\n"+
"  | | | |__   ___  | /  \/ |__   ___  ___  ___ _ __   | | | |_ __   ___ \r\n"+
"  | | | '_ \\ / _ \\ | |   | '_ \\ / _ \\/ __|/ _ \\ '_ \\  | | | | '_ \\ / _ \\\r\n"+
"  | | | | | |  __/ | \__/\ | | | (_) \__ \  __/ | | | \ \_/ / | | |  __/\r\n"+
"  \_/ |_| |_|\___|  \____/_| |_|\___/|___/\___|_| |_|  \___/|_| |_|\___|\r\n"+
"\r\n\r\nA labyrinth text game created for Ludum Dare 35\r\nCopyright 2016, Nander                                                                        ")
states["START"].add_t("1","continue",True,"START2")
states["START2"] = State("START2", "\033[137mYou are the 'chosen' one.\r\nYou are destined to be food for the Minotaur, roaming this maze.\r\nSince you have no plans to be eaten, you should find a way to leave this maze.")
states["START2"].add_t("1","Controls",True,"CONTROLS")
states["CONTROLS"] = State("CONTROLS", "Use either W A S D, or N E S W, followed by a carriage return (Enter) to move.\r\n For obvious reasons you have to choose now.")
states["CONTROLS"].add_t("1","Start Game using WASD (Modern)",True,"MAP")
states["CONTROLS"].add_t("2","Start Game using NESW (Old-School)",True,"MAP")

states["MAP"] = MapState("MAP","Escape from the maze.")
states["MAP"].add_t("?","Controls", True, "CONTROLS")
states["C1"] = State("C1", "I.\r\n\r\nMy name is Theseus.\r\n I am {}the chosen one{}. I'm destined to either kill the Minotaur roaming in this labyrinth, or be killed by it.".format(COLORS.BOLD,COLORS.WHITE))
states["C1"].add_t("1","CONTINUE",True,"BOOKEXPLAIN")
states["C1"].story_id=0

states["C2"] = State("C2", "II.\r\n\r\nI found giant footsteps.\r\n I don't think I'll be able to fight this thing.")
states["C2"].add_t("1","CONTINUE",True,"MAP")
states["C2"].story_id=1

states["C3"] = State("C3", "III.\r\n\r\nI've run into a dead end. In the corner is a water fountain. The water looks fresh\r\nIt seems they don't want me to die before I encounter the minotaur.")
states["C3"].add_t("1","CONTINUE",True,"MAP")
states["C3"].story_id=2

states["C4"] = State("C4", "IV.\r\n\r\nI found a bed. It seems they don't want me to get tired. They want to give me a fair fight")
states["C4"].add_t("1","I slept in the bed",True,"C4A")
states["C4"].add_t("2","I decided to keep moving",True,"C4B")
states["C4"].story_id=3


states["C4A"] = State("C4A", "IV (2).\r\n\r\nAs I awoke, I noticed something. The sun hasn't moved an inch.\r\n Where am I?")
states["C4A"].add_t("1","CONTINUE",True,"MAP")
states["C4A"].story_id=4

states["C4B"] = State("C4B", "IV (2).\r\n\r\nSleeping in a labyrinth with a Minotaur in it seemed like a terrible idea.")
states["C4B"].add_t("1","CONTINUE",True,"MAP")
states["C4B"].story_id=4

states["C5"] = State("C1", "I see some hairs on the wall. I think they are Minotaur hairs.")
states["C5"].add_t("1","CONTINUE",True,"MAP")

states["C9"] = State("C9", "I managed to escape, together with the minotaur.")
states["C9"].add_t("1","Read book (Story segments in order)",True,"BOOK2")
states["C9"].add_t("2","Straight to credits",True,"END2")

states["BOOK"] = BookState("BOOK", "BOOK READING")
states["BOOK"].add_t("1","Return to game",True,"MAP")
states["BOOKEXPLAIN"] = State("BOOKEXPLAIN", "I keep the pages I find in a binder.\r\nI can bring up the binder by typing b.")
states["BOOKEXPLAIN"].add_t("1","CONTINUE",True,"MAP")

states["BOOK2"] = BookState("BOOK2", "BOOK READING")
states["BOOK2"].add_t("1","To final credits",True,"END2")
states["END2"] = State("END2", "Thanks for playing \r\n \r\n ~Nander")



states["MONSTER1"] = State("MONSTER1", "I hear footsteps. The Minotaur must have heard me approach. ")
states["MONSTER1"].add_t("1","Return to game",True,"MAP")

states["MONSTER2"] = State("MONSTER2", "The Minotaur is getting closer. The noise of it's footsteps is getting extremely loud.")
states["MONSTER2"].add_t("1","Return to game",True,"MAP")

states["MONSTER3"] = State("MONSTER3", "I can see the shadow of the minotaur projected on the wall. The minotaur must be nearby.. ")
states["MONSTER3"].add_t("1","Return to game",True,"MAP")

states["MONSTER4"] = State("MONSTER4", "I hear a loud growling noise: {}GRAWR{}. ".format(COLORS.RED,COLORS.WHITE)+
"I tremble and try to run.")
states["MONSTER4"].add_t("1","Run away",True,"MAP")

states["MONSTER5"] = State("MONSTER5",
    "V.\r\n\r\nThe Minotaur reached me, but to my surprise, it didn't attack."+
        "\r\nInstead, it said:"+'\r\n"'+COLORS.RED+
        'HELLO'+COLORS.WHITE+'"')
states["MONSTER5"].add_t("1","Hello?",True,"MONSTER6")
states["MONSTER5"].story_id=5
states["NONE"] = State("NONE","Sorry, the game fully crashed. Please reload")
states["MONSTER6"] = State("MONSTER6", "VI.\r\n\r\nThe Minotaur continued:"+ 
'\r\n"I\'m sorry if I frightened you, GRAWR means hello in my language."')
states["MONSTER6"].add_t("1",'I replied : "I could have died of fear"',True,"MONSTER7A")
states["MONSTER6"].add_t("2",'I sighed and said   : "You {}do{} sound frightning"'.format(COLORS.BOLD,COLORS.WHITE),True,"MONSTER7A")
states["MONSTER6"].add_t("3",'I replied : "I wasn\'t afraid"',True,"MONSTER7B")
states["MONSTER6"].story_id=6

states["MONSTER7A"] = State("MONSTER7A", "VII.\r\n"+
    "The Minotaur sighed and said:\r\n"+
'"Sorry, I can\'t help it. However: I think we can work something out. I\'ve found a way out."')
states["MONSTER7A"].add_t("1",'I asked: "Where is it?"',True,"MONSTER8")
states["MONSTER7A"].story_id=7
states["MONSTER7B"] = State("MONSTER7B", "VII.\r\n"+
    "The Minotaur didn't seem to believe me, but continued anyway:"+
"I think we can work something out. I've found a way out.")
states["MONSTER7B"].add_t("1","Good.",True,"MONSTER8")
states["MONSTER7B"].story_id=7
states["MONSTER8"] = State("MONSTER8", "VIII.\r\n\r\n"+
"The Minotaur thought for a moment and said:\r\n"+
'"Shit, I forgot the way.\r\n\r\nI do have a solution though:\r\nyou start looking for the exit, and I\'ll follow you"\r\n')
states["MONSTER8"].add_t("1",'I replied: "OK.".',True,"MAP")
states["MONSTER8"].story_id=8


def state(i):
    return states[i]
class MainServerSocket(asyncore.dispatcher):
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        self.x = 16
        self.y = 16
        self.mx = -10
        self.my = 0
        self.mstate = 0
        self.found={}
        self.story=["I.\r\n\r\n No Pages Yet",
        "","","","","","","","","","","","","","","","","","","","","","","","","",""]
        self.send(states[self.state].print_self(self.x,self.y,self))
        self.on_page = 0

    def handle_read(self):
        receivedData = self.recv(8192)
        if receivedData: 
            if hasattr(states.get(self.state,"NONE"),"story_id"):
                self.story[states[self.state].story_id] = states[self.state].state_name
            
            olen = receivedData.__len__()

            receivedData= receivedData.replace("\n", "").replace("\r","")
            olen = olen -  receivedData.__len__()
            if receivedData != "":
                if olen ==0:
                    self.buff = self.buff + receivedData
                else:
                    res = states.get(self.state,"NONE").handle_input(receivedData,self.x,self.y,self)
                    self.state=res[1]
                    if res.__len__()>2:
                        self.x = res[2]
                        self.y = res[3]
                    if res[0]:
                        self.send(states.get(self.state,"NONE").print_self(self.x,self.y,self))
                    else:
                        self.send(states.get(self.state,"NONE").print_self(self.x,self.y,self))

                        self.send("<"+receivedData + "> was not understood\r\n")
            elif self.buff != "":

                res = states.get(self.state,"NONE").handle_input(self.buff,self.x,self.y,self)
                self.state=res[1]
                if res.__len__()>2:
                    self.x = res[2]
                    self.y = res[3]
                if res[0]:
                    self.send(states.get(self.state,"NONE").print_self(self.x,self.y,self))
                else:

                    self.send(states.get(self.state,"NONE").print_self(self.x,self.y,self))

                    self.send("<"+self.buff + "> was not understood.\r\n")
                self.buff = ""
        else: self.close(  )
    def handle_close(self):
        print ("Disconnected from", self.getpeername(  ))

MainServerSocket(1337)
asyncore.loop(  )
