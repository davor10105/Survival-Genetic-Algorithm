import sys, pygame,random
pygame.init()

size = width, height = 600, 600

screen = pygame.display.set_mode(size)
clock=pygame.time.Clock()


blockSize=100

random.seed(69)

class Player():
    def __init__(self,name,color,position=(0,0)):
        self.name=name
        self.position=position
        self.color=color

        self.brainVector=[random.randint(0,6) for i in range(162)]
        self.score=0

        self.dead=False

def getScreenPos(gamePos):
    return (gamePos[1]*100+50,gamePos[0]*100+50)

def getNeighbourStates(currentState):
    neighbourStates=[]
    for i in [-1,1]:
        x=currentState[0]+i
        if x>=0 and x<width//100:
            newState=(x,currentState[1])
            neighbourStates.append(newState)
    for i in [-1,1]:
        y=currentState[1]+i
        if y>=0 and y<height//100:
            newState=(currentState[0],y)
            neighbourStates.append(newState)

    return neighbourStates

def getSurroundings(player):
    trenutna=0
    gore=0
    dolje=0
    lijevo=0
    desno=0
    
    for p in players:
        if p.position==player.position and player!=p and p.dead==False:
            trenutna=1
        if (player.position[0]-1,player.position[1])==p.position and p.dead==False:
            gore=1
        if (player.position[0]+1,player.position[1])==p.position and p.dead==False:
            dolje=1
        if (player.position[0],player.position[1]-1)==p.position and p.dead==False:
            lijevo=1
        if (player.position[0],player.position[1]+1)==p.position and p.dead==False:
            desno=1
            
    if player.position[0]-1<0:
        gore=2
    if player.position[0]+1>=height//100:
        dolje=2
    if player.position[1]-1<0:
        lijevo=2
    if player.position[1]+1>=width//100:
        desno=2

    return trenutna*81+gore*27+dolje*9+lijevo*3+desno

def updateScoreAndMove(player,move):

    if move==6:
        move=random.randint(2,5)

    #print(player.name,move)
    stayScore=-20
    walkScore=-5
    wallScore=-20
    eatScore=1000
    eatenScore=-50
    missScore=-15
    
    #dobar pomak
    if move==0:
        player.score+=stayScore
    if move==2:
        if (player.position[0]-1,player.position[1]) in getNeighbourStates(player.position):
            player.score+=walkScore
            player.position=(player.position[0]-1,player.position[1])
        else:
            player.score+=wallScore
    if move==3:
        if (player.position[0]+1,player.position[1]) in getNeighbourStates(player.position):
            player.score+=walkScore
            player.position=(player.position[0]+1,player.position[1])
        else:
            player.score+=wallScore
    if move==4:
        if (player.position[0],player.position[1]-1) in getNeighbourStates(player.position):
            player.score+=walkScore
            player.position=(player.position[0],player.position[1]-1)
        else:
            player.score+=wallScore
    if move==5:
        if (player.position[0],player.position[1]+1) in getNeighbourStates(player.position):
            player.score+=walkScore
            player.position=(player.position[0],player.position[1]+1)
        else:
            player.score+=wallScore
    #jede
    if move==1:
        pojeo=False
        for p in players:
            if player.position==p.position and player!=p and p.dead==False:
                player.score+=eatScore
                p.score+=eatenScore
                p.dead=True
                pojeo=True
        if pojeo==False:
            player.score+=missScore

def returnChildren(playerOne,playerTwo):
    childOneVector=[]
    childTwoVector=[]
    for i in range(162):
        if (random.randint(1,2)==1):
            childOneVector.append(playerOne.brainVector[i])
            childTwoVector.append(playerTwo.brainVector[i])
        else:
            childOneVector.append(playerTwo.brainVector[i])
            childTwoVector.append(playerOne.brainVector[i])

    for i in range(162):
        if random.randint(1,100)>90:
            childOneVector[i]=random.randint(0,6)
        if random.randint(1,100)>90:
            childTwoVector[i]=random.randint(0,6)

    return (childOneVector,childTwoVector)

red=Player("Red",pygame.Color(255,0,0),(random.randint(0,5),random.randint(0,5)))
blue=Player("Blue",pygame.Color(0,0,255),(random.randint(0,5),random.randint(0,5)))
orange=Player("Orange",pygame.Color(255,165,0),(random.randint(0,5),random.randint(0,5)))
violet=Player("Violet",pygame.Color(255,0,255),(random.randint(0,5),random.randint(0,5)))

players=[red,blue,orange,violet]



for iteration in range(10000):
    #every iteration 20 steps
    for step in range(30):

        #draw players

        for player in players:
            if player.dead==False:
                updateScoreAndMove(player,player.brainVector[getSurroundings(player)])


    #pick 2 best bois
    players.sort(key=lambda p:-p.score)

    print("iteration: ",iteration,[(p.name,p.score) for p in players])
    
    childOneVector,childTwoVector=returnChildren(players[0],players[1])

    players[2].brainVector=childOneVector
    players[3].brainVector=childTwoVector

    #reset
    for player in players:
        player.score=0
        player.dead=False
    players[0].position=(random.randint(0,5),random.randint(0,5))
    players[1].position=(random.randint(0,5),random.randint(0,5))
    players[2].position=(random.randint(0,5),random.randint(0,5))
    players[3].position=(random.randint(0,5),random.randint(0,5))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    #play one iteration
            
    #draw squares
    for i in range(height):
        for j in range(width):
            if j%blockSize==0 and i%blockSize==0:
                rect=pygame.Rect(j+1,i,blockSize-2,blockSize-2)
                pygame.draw.rect(screen,pygame.Color(255,255,255),rect)

    #draw players

    for player in players:
        print((player.name,player.dead,player.position,player.brainVector[getSurroundings(player)],player.score))
        if player.dead==False:
            updateScoreAndMove(player,player.brainVector[getSurroundings(player)])
            pygame.draw.circle(screen,player.color,getScreenPos(player.position),blockSize//2-10)
        else:
            pass
            #pygame.draw.circle(screen,player.color,getScreenPos(player.position),blockSize//2-20)

    clock.tick(1)
    pygame.display.update()


