""""
+------> y
|
|
v
x
"""


l=[]

for i in range(3):
    o=[]
    for j in range(3):
        o.append(0)
    l.append(o)

def printT(l):
    for i in l:
        print(i)

def win(l, p):
    for i in range(3):
        if l[i][0] == l[i][1] and l[i][1] == l[i][2]:
            if not l[i][0]==0:
                return True
    for j in range(3):
        if l[0][j] == l[1][j] and l[1][j] == l[2][j]:
            if not l[0][j]==0:
                return True
    if l[0][0] == l[1][1] and l[1][1] == l[2][2]:
            if not l[0][0]==0:
                return True
    if l[0][2] == l[1][1] and l[1][1] == l[2][0]:
            if not l[0][2]==0:
                return True
    return False

def play(l, x, y, p):
    if x>=0 and x<=2 and y>=0 and y<= 2:
        if l[x][y]==0:
            l[x][y]=p
            return True
        else:
            print("NAA déjà pris")
            return False
    else:
            print("NAA pas dans la map")
            return False

def nextTurn(turn):
    return ((turn+1)%2)+1

def askXY():
    x=int(input("x:"))
    y=int(input("y:"))
    return x, y

def game():
    turn=0
    playerTurn=0
    while not win(l, turn):
        printT(l)
        turn+=1
        playerTurn = nextTurn(turn)
        print("turn", turn , ": player", playerTurn)
        x, y = askXY()
        while not play(l, x, y, playerTurn):
            x, y = askXY()
        

    print("player", playerTurn, "win")

game()
