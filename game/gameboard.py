from unicurses import mvaddstr
from engine.screenSetup import sh,sw,white,dark_gray,mediocre_gray, gray,brightorange,red,orange,dark_orange, yellow, ResetKey
from game.dialouge.leshy import leshyTalk
from time import sleep
from __main__ import Developer_Mode
from random import choice, uniform, shuffle, randint, choices

from engine.threadingEngine import threaded


from game.boardArt import *

from engine.soundEngine import PlaySound, StopLoopingSound

from array import *

BoardID = [
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"],#0
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"],#1
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"]#2
    ]

IsTutorial = False

actualDeck = [] # Users current GAME deck of cards
remainingDeck = [] # Users current GAME deck of cards
deck = [] # Users current GAME deck of cards
cardsDiscovered = []
LastEvent = "" #CardPlace{TYPE}, positionPlacement{TYPE},sacrifice,SelectCardFromDeck,BellPressed, BellSpawn

squirrelCount = 9 #Starting squirrel count

def startBoard(clearBoard=False):
    cardCentringOriginal = -38
    soundPositionOriginal = -0.15
    cardHeight = -15
    for cardRow in range(0,3):
        cardCentering = cardCentringOriginal
        soundPosition = soundPositionOriginal
        for card in range(0,4):
            #[mvaddstr(sh // 2 + cardHeight + x, sw // 2 + cardCentering, blankCardSpace[x], white) for x in range (0,12)]
            if cardRow == 0:
                [mvaddstr(sh // 2 + cardHeight + x, sw // 2 + cardCentering, blankCardSpaceArrow[x], mediocre_gray) for x in range(0, 12)]
            elif cardRow == 1:
                [mvaddstr(sh // 2 + cardHeight + x, sw // 2 + cardCentering, blankCardSpaceAttackDown[x], mediocre_gray) for x in range(0, 12)]
            elif cardRow == 2:
                [mvaddstr(sh // 2 + cardHeight + x, sw // 2 + cardCentering, blankCardSpaceAttackUp[x], mediocre_gray) for x in range(0, 12)]
            cardCentering += 20
            if not clearBoard:
                CardPlaySound("glow",(soundPosition, 0,1))
                soundPosition += 0.1
                sleep(0.15)

        cardHeight += 12
    global BoardID
    BoardID = [
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"],#0
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"],#1
        ["blankCardSpace", "blankCardSpace", "blankCardSpace", "blankCardSpace"]#2
    ]

    if Developer_Mode:
        #mvaddstr(22, 0, BoardID)
        mvaddstr(59,0,deck)

def StartGame(tutorial=False): # Only used once from cabin.py
    if tutorial:
        global IsTutorial
        IsTutorial = True
        actualDeck.append(["lobster", lobster[12], lobster[13], lobster[14]])  # type, attack, health, blood
        actualDeck.append(["wolf", wolf[12], wolf[13], wolf[14]])  # type, attack, health, blood
        actualDeck.append(["wolf", wolf[12], wolf[13], wolf[14]])  # type, attack, health, blood
        actualDeck.append(["riversnapper", wolf[12], wolf[13], wolf[14]])

        remainingDeck.append(["riversnapper", wolf[12], wolf[13], wolf[14]])
        deck.append(["squirrel", squirrel[12], squirrel[13], squirrel[14]])  # type, attack, health, blood #NOTE THIS IS THE ONLY TIME THAT THE DEFAULT NUMBERS ARE USED
        deck.append(["lobster", lobster[12], lobster[13], lobster[14]])  # type, attack, health, blood
        deck.append(["wolf", wolf[12], wolf[13], wolf[14]])  # type, attack, health, blood
        deck.append(["wolf", wolf[12], wolf[13], wolf[14]])  # type, attack, health, blood
        SelectCardFromDeck()
    else:
        BellObject(spawn=True)
        Scales(scaleSpawn=True)
        #Candles(spawn=True)
        #will replace with save file later
        cardsDiscovered.extend(("lobster","wolf","riversnapper","bullfrog"))
        actualDeck.append(["lobster", lobster[12], lobster[13], lobster[14]])  # type, attack, health, blood
        actualDeck.append(["wolf", wolf[12], wolf[13], wolf[14]])  # type, attack, health, blood
        actualDeck.append(["wolf", wolf[12], wolf[13], wolf[14]])  # type, attack, health, blood
        actualDeck.append(["riversnapper", wolf[12], wolf[13], wolf[14]])
        StopLoopingSound("cabin_ambience")
        PlaySound("stereo/cabin/gametable_ambience", 1, (0, 0, 0), "gametable_ambience")
        startNewRound()

reference = { # Reference for all strings to lists
    #misc
        "knife" : knife,
        "bell" : bell,
        "blankCardSpace" : blankCardSpace,
        "blankCardSpaceArrow" : blankCardSpaceArrow,
        "squirrelback": squirrelback,
        "powerback": powerback,
        "bigblank" : bigblank,
    #terrain
        "stump" : stump,
        "boulder" : boulder,
    #cards
        "lobster" : lobster,
        "lobster2": lobster2,
        "squirrel" : squirrel,
        "wolf" : wolf,
        "alpha" : alpha,
        "coyote" : coyote,
        "skunk" : skunk,
        "skink" : skink,
        "ant" : ant,
        "bee" : bee,
        "ringworm" : ringworm,
        "bullfrog"  : bullfrog,
        "riversnapper" : riversnapper,
        "cat" : cat,
        "wolfcub" : wolfcub,
        "sparrow" : sparrow,
        "pronghorn" : pronghorn,
        "elkcub" : elkcub,
        "elk" : elk,
        "otter" : otter,
        "porcupine" : porcupine,
        "adder" : adder,
    #bigcards
        "biglobster" : biglobster,
        "biglobster2": biglobster2,
        "bigsquirrel" : bigsquirrel,
        "bigwolf" : bigwolf,
        "bigalpha" : bigalpha,
        "bigcoyote": bigcoyote,
        "bigskunk": bigskunk,
        "bigskink": bigskink,
        "bigant" : bigant,
        "bigbee" : bigbee,
        "bigringworm" : bigringworm,
        "bigbullfrog" : bigbullfrog,
        "bigriversnapper" : bigriversnapper,
        "bigcat" : bigcat,
        "bigwolfcub" : bigwolfcub,
        "bigsparrow" : bigsparrow,
        "bigpronghorn" : bigpronghorn,
        "bigelkcub" : bigelkcub,
        "bigelk" : bigelk,
        "bigotter" : bigotter,
        "bigporcupine" : bigporcupine,
        "bigadder" : bigadder
    }


# End Game

bellEnabled = False
candlesDiscovered = False
roundOver = False

def endRound(victory):
    global scaleTip
    global roundOver
    global LastEvent
    global candlesDiscovered
    global candlesActive

    roundOver = True
    scaleTip = 0

    if victory:
        LastEvent = "PlayerWin"
        GameEvents()
        global IsTutorial
        if IsTutorial:
            IsTutorial = False
        Candles(relight=True)
    else:
        if not candlesDiscovered:
            candlesDiscovered = True
            LastEvent = "OpponentWinCandles"
        else:
            candlesActive -= 1
            if candlesActive > 0:
                LastEvent = "OpponentWin"
            else:
                LastEvent = "GameOver"
        GameEvents()

def endRoundChecker():
    if scaleTip <= -5: #opponent wins
        endRound(False)
    elif scaleTip >= 5: # player wins
        endRound(True)


#Pre-game

def mainStartingModule(): #Makes sure code doesn't stack
    while not roundOver:
        SelectCardFromDeck()
        if not roundOver: # SelectCardFromDeck may trigger round over therefore no new card should be drawn
            drawNewCard()  # Loop back to start
    else: #If continue rounds -
        startNewRound()

def startNewRound():
    global roundOver
    roundOver = False
    startBoard(True) # Clears board
    randomTerrainChoice() # Puts new terrain
    buildOpponentTurnPlan() #creates turn plan for opponent
    selectRandomPlayerCards() #Randomly chooses from actual deck
    Scales(scaleRefresh=True) #Refresh Scales
    drawNewCard(True) #Refresh New card textures
    opponentAI() #Play first turn
    mainStartingModule() # Begin match

from game.blueprints import grabRandomBlueprint

def buildOpponentTurnPlan():
    global TurnPlan
    global TurnTaken
    global cardsDiscovered
    blueprint = grabRandomBlueprint()
    TurnTaken = 0
    MaxNumOfTurns = len(blueprint) - 5  # -4 is the variables
    replacements = [x for x in blueprint[4] if x in cardsDiscovered]
    [cardsDiscovered.append(x) for x in blueprint[3] if x not in cardsDiscovered] # adds to cards discovered

    for _x_ in range(0,5): # Remove old data
        blueprint.pop(0)

    for x in replacements: # Add replacements
        selectedSlot = randint(0, len(blueprint)-1)
        blueprint[selectedSlot].append(x)
    # difficulty -> replacement count
    # -> add replacements
    TurnPlan = blueprint

def randomTerrainChoice():
    amountOfFoliage = randint(-2,3)
    if amountOfFoliage == 3:
        amountOfFoliage = choices([2,3], weights=(75,25), k=1)[0] # Low chance to select over 3
    if amountOfFoliage <= 0:
        return
    else:
        def boardGrabber(): # Grabs board info
            slots = [[], []] # Opponent then Player
            for cardPos in range(0, 4):  # Slots that are blocked up ahead
                if BoardID[1][cardPos] == "blankCardSpace": # Opponent
                    slots[0].append(cardPos)
                if BoardID[2][cardPos] == "blankCardSpace": # Player
                    slots[1].append(cardPos)
            shuffle(slots[0])
            shuffle(slots[1])
            return slots
        for terrainCard in range(0,amountOfFoliage):
            slots = boardGrabber()
            cardChoice = choice(["stump","boulder"])
            inPlayersPosition = choice([True,False])
            # Override if 2 cards are already present in the row
            if len(slots[1]) == 3 : # Only one card can be placed in players position
                inPlayersPosition = False
            elif len(slots[0]) == 2:
                inPlayersPosition = True
            #Execute
            counter = 0
            while not counter == 4:
                if inPlayersPosition:
                    if slots[1][counter] in slots[0]:
                        PlaceCardOrColorChange(slots[1][counter],2,[cardChoice,reference[cardChoice][12],reference[cardChoice][13],reference[cardChoice][14]])
                        slots[1].pop(0)
                        counter = 4
                    else:
                        counter += 1
                else:
                    if slots[0][counter] in slots[1]:
                        PlaceCardOrColorChange(slots[0][counter], 1,[cardChoice, reference[cardChoice][12], reference[cardChoice][13],reference[cardChoice][14]])
                        slots[0].pop(0)
                        counter = 4
                    else:
                        counter += 1
            sleep(0.3)


def selectRandomPlayerCards():
    global deck
    global remainingDeck
    global squirrelCount
    deck.clear()
    remainingDeck.clear()

    #Squirrel pickup
    deck.append(["squirrel", squirrel[12], squirrel[13], squirrel[14]])
    squirrelCount = 9

    #Shuffle 'match' deck
    remainingDeck = actualDeck.copy()
    shuffle(remainingDeck)
    selectedCardsToBeDrawn = []

    #Pickup 3 cards
    count = 0
    for x in remainingDeck:
        if not count == 3:
            selectedCardsToBeDrawn.append(x)
            count +=1
    for card in selectedCardsToBeDrawn:
        remainingDeck.remove(card)
        deck.append(card)


#During game opponent AI

TurnTaken = 0
MaxNumOfTurns = 0
TurnPlan = [] # <- nested turn plan ie: [[turn1data],[turn2data]]

def opponentAI():

    blockedSlots = []
    def findBlockedSlots():
        blockedSlots.clear()
        for cardPos in range(0, 4):  # Slots that are blocked up ahead
            if not BoardID[1][cardPos] == "blankCardSpace":
                blockedSlots.append(cardPos)

    #Plays next turn of cards
    def playQueuedCards():
        findBlockedSlots()
        global TurnTaken
        global TurnPlan
        avaliableSlots = []

        for cardPos in range(0, 4):  # Avaliable slots to place
            if BoardID[0][cardPos] == "blankCardSpace":
                avaliableSlots.append(cardPos)

        shuffle(avaliableSlots)  # makes sure it's always shuffled

        #Tries to place a card in a non-blocked position
        def blockCheck(count=0):
            if count == len(avaliableSlots):
                return avaliableSlots[0] # If everything is blocked ahead then place the card nonetheless
            elif avaliableSlots[count] in blockedSlots:
                return blockCheck(count + 1)
            else:
                return avaliableSlots[count]

        for card in TurnPlan[TurnTaken]:
            if not avaliableSlots == []:
                usingSlot = blockCheck()
                PlaceCardOrColorChange(usingSlot, 0, [card, reference[card][12], reference[card][13], reference[card][14]])
                avaliableSlots.remove(usingSlot)
                sleep(0.3)
            #Else it will -> break (No avaliable slots for placing - discards turn)
        TurnTaken += 1


    def moveCardsFoward():
        findBlockedSlots()
        for card in range(0,4):
            if not BoardID[0][card] == "blankCardSpace": # Opponent original position
                if not card in blockedSlots:
                    PlaceCardOrColorChange(card, 1,BoardID[0][card]) # New card pos
                    PlaceCardOrColorChange(card, 0, False, placingABlankCard=True) # Replace old pos
                    sleep(0.3)

    #Execute
    moveCardsFoward()
    if TurnTaken <= len(TurnPlan)-1:
        playQueuedCards()

def AttackPhase(): # After bell ring
    global LastEvent
    #Starts by attacking from the players perspective
    totalDirectDmg = AttackCard() # Player Attack
    LastEvent = "PlayerAttack"
    GameEvents()
    # Scale change
    Scales(scaleWeight=totalDirectDmg)
    LastEvent = "ScaleTipPlayerAttack"
    GameEvents(totalDirectDmg)

    endRoundChecker()

    if not roundOver:
        #Opponent moves forward and places cards
        if not IsTutorial:
            opponentAI() # Moves cards forward and plays queue

        #Opponent attacks
        totalDirectDmg = AttackCard(opponent=True)
        LastEvent = "OpponentAttack"
        GameEvents()
        #Scale change
        Scales(scaleWeight=totalDirectDmg) # ScaleChange
        LastEvent = "ScaleTipOpponentAttack"
        GameEvents(totalDirectDmg)

        endRoundChecker()

    if not roundOver: # Round isn't over
        LastEvent = "RoundNotOverCheck"
        GameEvents()
        #Goes back to mainStartingModule

def AttackCard(opponent=False):
    order = [] # Order that cards attack, left to right
    blockedAttack = [] # If attack is between creature vs creature
    directAttack = [] # Influences scales
    totalDirectDmg = 0

    def animationAttack(card): #Animation for attacking
        global BoardID
        if not opponent: #Player
            PlaceCardOrColorChange(card, 2, BoardID[2][card],False,brightorange) #changes players card to orange
            PlaceCardOrColorChange(card, 1, BoardID[1][card], False, red) #changes opponents card to red
            sleep(0.3)
            PlaceCardOrColorChange(card, 2, BoardID[2][card], False, white)  # changes players card to white
            try: # sometimes it's a BlankCardSpace, causes error
                if BoardID[1][card][2] <= 0: #checks if opponents card is dead
                    sleep(0.1)
                    PlaySound("mono/card/card_death", round(uniform(0.5, 0.6), 2), (-0.15 + (0.1 * card), 0, 1))
                    BoardID[1][card] = "blankCardSpace"
                    PlaceCardOrColorChange(card, 1, BoardID[1][card], False, red)  # updates blank space with red
                    sleep(0.2)
            except:
                pass
            PlaceCardOrColorChange(card, 1, BoardID[1][card], False, white)  # changes opponents card to white
        else: #Opponent
            PlaceCardOrColorChange(card, 1, BoardID[1][card], False, brightorange)  # changes opponents card to orange
            PlaceCardOrColorChange(card, 2, BoardID[2][card], False, red)  # changes players card to red
            sleep(0.3)
            PlaceCardOrColorChange(card, 1, BoardID[1][card], False, white)  # changes opponents card to white
            try:
                if BoardID[2][card][2] <= 0:  # checks if players card is dead
                    sleep(0.1)
                    PlaySound("mono/card/card_death", round(uniform(0.5, 0.6), 2), (-0.15 + (0.1 * card), 0, 1))
                    BoardID[2][card] = "blankCardSpace"
                    PlaceCardOrColorChange(card, 2, BoardID[2][card], False, red)  # updates blank space with red
                    sleep(0.2)
            except:
                pass
            PlaceCardOrColorChange(card, 2, BoardID[2][card], False, white)  # changes players card to white
    #Not animation
    if not opponent: #Player Attack
        #Detect spaces
        for card in range(0, 4):
            if not BoardID[2][card] == "blankCardSpace" and not BoardID[2][card][1] == 0: # Detect players row
                order.append(card)
                if BoardID[1][card] == "blankCardSpace": #Detect if blocked space (opponents card); Will beable to still attack stumps and boulders
                    directAttack.append(card)
                else: #Not blocked
                    blockedAttack.append(card)
        #Attacking
        for card in order:
            if card in directAttack:
                PlaySound("mono/card/card_attack_directly",round(uniform(0.5,0.6),2),(-0.15+(0.1*card),0,1))
                totalDirectDmg += BoardID[2][card][1] # total damage positive (player attacking)
            else: #blockedAttack
                PlaySound("mono/card/card_attack_creature", round(uniform(0.5, 0.6), 2),(-0.15 + (0.1 * card), 0, 1))
                BoardID[1][card][2] -= BoardID[2][card][1] #Opponents card's health - Players dmg
            animationAttack(card)
            sleep(0.3)

    else: # Opponent Attack
        #Detection
        for card in range(0, 4):
            if not BoardID[1][card] == "blankCardSpace" and not BoardID[1][card][1] == 0: # Detects Opponents row
                order.append(card)
                if BoardID[2][card] == "blankCardSpace": # Detect if blocked space (players card)
                    directAttack.append(card)
                else:
                    blockedAttack.append(card)
        # Attacking
        for card in order:
            if card in directAttack:
                PlaySound("mono/card/card_attack_directly", round(uniform(0.5, 0.6), 2),(-0.15 + (0.1 * card), 0, 1))
                totalDirectDmg -= BoardID[1][card][1] # totalDmg negative (opponent attacking)
            else:  # blockedAttack
                PlaySound("mono/card/card_attack_damage", round(uniform(0.5, 0.6), 2), (-0.15 + (0.1 * card), 0, 1))
                BoardID[2][card][2] -= BoardID[1][card][1]  # Players card's health - Opponent dmg
            animationAttack(card)
            sleep(0.3)
    return totalDirectDmg


#During 'quiet' time

def PlaceCardOrColorChange(cardNum, row, deckCardInfo, placement = True, color = white, placingABlankCard = False): #Updates to board
    global BoardID
    cardCentering = -38 + (20 * cardNum) #Centering; changes 1-4 to 0-3
    soundPosition = -0.15
    cardHeight = -15 + (12 * row) #Height; changes 1-3 to 0-2

    if deckCardInfo == "blankCardSpace" or not deckCardInfo:
        if color == white:
            color = mediocre_gray
        #[mvaddstr(sh // 2 + cardHeight + x, sw // 2 + cardCentering, blankCardSpace[x], color) for x in range(0, 12)]
        if row == 0:
            [mvaddstr(sh // 2 + x + cardHeight, sw // 2 + cardCentering, blankCardSpaceArrow[x], color) for x in range(0,12)]
        elif row == 1:
            [mvaddstr(sh // 2 + x + cardHeight, sw // 2 + cardCentering, blankCardSpaceAttackDown[x], color) for x in range(0, 12)]
        elif row == 2:
            [mvaddstr(sh // 2 + x + cardHeight, sw // 2 + cardCentering, blankCardSpaceAttackUp[x], color) for x in range(0, 12)]
    else:
        CardType = deckCardInfo[0]
        [mvaddstr(sh // 2 + cardHeight + x, sw // 2 + cardCentering, reference[CardType][x], color) for x in range(0, 12)]
        mvaddstr(sh // 2 + cardHeight + 10, sw // 2 + cardCentering + 2, f"{deckCardInfo[1]}†", color)  # Attack
        mvaddstr(sh // 2 + cardHeight + 10, sw // 2 + cardCentering + 13, f"{deckCardInfo[2]}♥", color)  # Attack
        if color == white:
            color = red
        if row == 2:
            mvaddstr(sh // 2 + cardHeight + 10, sw // 2 + cardCentering + 9 - deckCardInfo[3], "δ" * deckCardInfo[3],color)  # Attack
    if placingABlankCard:
        BoardID[row][cardNum] = "blankCardSpace"
    elif placement:
        CardPlaySound("normal",(soundPosition+(0.1*cardNum), 0, 1))
        BoardID[row][cardNum] = [CardType,deckCardInfo[1],deckCardInfo[2],deckCardInfo[3]]

def printSideBig(deckCardInfo, color, blank=False, positionInDeck = "TurnedOff"): # Prints preview of deck on right-hand side of screen
    if blank == True:
        [mvaddstr(sh // 2 - 18 + x, sw // 2 + 58, bigblank[0], color) for x in range (0,31)]
    else:
        portrait = f"big{deckCardInfo[0]}"
        if not positionInDeck == "TurnedOff": # "TurnedOff" is temporary as bool cannot be used due to '0' being a pos
            mvaddstr(sh // 2 - 19, sw // 2 + 76 - len(str(positionInDeck)), f"{positionInDeck+1}/{len(deck)}", color) # Status bar
        else:
            mvaddstr(sh // 2 - 19, sw // 2 + 76 - 3, f"               ", color) # disable status bar
        [mvaddstr(sh // 2 - 18 + x, sw // 2 + 58, reference[portrait][x], color) for x in range(0, 31)]
        mvaddstr(sh // 2 - 18 + 28, sw // 2 + 64, f"{deckCardInfo[1]}†", color) #Extras
        mvaddstr(sh // 2 - 18 + 28, sw // 2 + 90, f"{deckCardInfo[2]}♥", color)
        if color == white:
            color = red
        if not portrait == "bigriversnapper":
            mvaddstr(sh // 2 -16, sw // 2 + 90 - deckCardInfo[3], "δ" * deckCardInfo[3], color) # Accounting for double-line title
        else:
            mvaddstr(sh // 2 - 15, sw // 2 + 90 - deckCardInfo[3], "δ" * deckCardInfo[3], color)

def positionPlacement(oldSelect=0, spectating = False): # Position on one of the 4 avaliable places to put a card (Includes sacrifices)

    global LastEvent
    try:
        LastEvent = f"positionPlacement{deck[oldSelect][0]}"
    except:
        LastEvent = f"positionPlacementnone"
    GameEvents()

    placementCount = 0
    sacrificeRequired = False
    sacrificeMade = False
    bellSelected = False
    bellPressed = False
    placing = False
    SelectCardReturn = False # Return to selecting card

    sacrificeSpeechGiven=False # Makes sure Opponent only gives speech once while in this menu (stops spamming)

    wU = True # Looper
    from game.dialouge.dialouge import clearLine
    sacrifices = []
    posCenter = -30
    while wU:
        def changeOldCardToWhite(placement=BoardID[2][placementCount], cardNum = placementCount, ignoreCard=False):
            if not ignoreCard:
                PlaceCardOrColorChange(cardNum, 2, placement, False, white)
            if cardNum == -1:
                mvaddstr(sh // 2 + 13 + 9, sw // 2 - 66, " ", brightorange)
            else:
                mvaddstr(sh // 2 + 21, sw // 2 + posCenter + (20 * cardNum), " ", brightorange)

        ResetKey()
        try:
            if deck[oldSelect][3] > 0 and not sacrificeMade and not spectating and not bellSelected and not placementCount in sacrifices: # Checks if a sacrifice is being made
                sacrificeRequired = True
                PlaceCardOrColorChange(placementCount, 2, BoardID[2][placementCount], False, red)
            elif not bellSelected and not placementCount in sacrifices: # No sacrifice could be made
                PlaceCardOrColorChange(placementCount, 2, BoardID[2][placementCount], False, brightorange)
                placing = True
        except: # Empty deck exception
            if not bellSelected and not placementCount in sacrifices:
                PlaceCardOrColorChange(placementCount, 2, BoardID[2][placementCount], False, brightorange)
                placing = True
        if not placementCount == -1: #normal
            mvaddstr(sh // 2 + 21 ,sw // 2 + posCenter + (20 * placementCount),"^", brightorange)
        else: # bell
            mvaddstr(sh // 2 + 13 + 9, sw // 2 -66, "^", brightorange)


        checkInput = True
        while checkInput:
            from engine.screenSetup import key
            if not placementCount - 1 <= -1: # Not Bell
                if key in ["KEY_LEFT","a"]:
                    if not placementCount in sacrifices:
                        changeOldCardToWhite()
                    placementCount -= 1
                    checkInput = False
            else: # Bell
                if not placementCount -1 == -2 and bellEnabled and spectating: #cant go over bell
                    if key in ["KEY_LEFT","a"]:
                        changeOldCardToWhite()
                        bellSelected = True
                        placementCount -= 1
                        BellObject(white)
                        checkInput = False

            if not placementCount + 1 == 4:
                if key in ["KEY_RIGHT","d"]:
                    if not placementCount + 1 == 0: # cant go over board
                        if not placementCount in sacrifices:
                            changeOldCardToWhite()
                        placementCount += 1
                        checkInput = False
                    else: # If on bell, turn it off
                        changeOldCardToWhite(ignoreCard=True)
                        BellObject(gray)
                        bellSelected = False
                        placementCount += 1
                        checkInput = False

            if key in ["^[","x",'s',"KEY_DOWN"] and not sacrificeMade:
                if not sacrifices == []:
                    for position in sacrifices:
                        changeOldCardToWhite(BoardID[2][position], position)

                if not bellSelected:
                    changeOldCardToWhite()
                else:
                    changeOldCardToWhite(ignoreCard=True)
                SelectCardReturn = True
                checkInput = False
                wU = False
            if key in ["^J", 'z', ' ']:
                checkInput = False
                if bellSelected and spectating:
                    bellPressed = True
                    wU = False
                elif placing and BoardID[2][placementCount] == "blankCardSpace" and not spectating and not deck == []: # Will not continue if sacrifice is not made
                    wU = False
                if sacrificeRequired \
                        and not sacrificeMade \
                        and not BoardID[2][placementCount] == "blankCardSpace" \
                        and not BoardID[2][placementCount][0] in ["boulder","stump"] \
                        and not placementCount in sacrifices and not spectating:
                    sacrifices.append(placementCount) #appends position of sacrifice
                    #Sacrifice knife
                    #top
                    mvaddstr(sh // 2 + 10, sw // 2 + (-38 + (20 * placementCount)) + 8, reference["knife"][0], dark_gray)
                    mvaddstr(sh // 2 + 11, sw // 2 + (-38 + (20 * placementCount)) + 8, reference["knife"][1], dark_gray)
                    mvaddstr(sh // 2 + 12, sw // 2 + (-38 + (20 * placementCount)) + 6, reference["knife"][2], dark_gray)
                    mvaddstr(sh // 2 + 13, sw // 2 + (-38 + (20 * placementCount)) + 7, reference["knife"][3], dark_gray)
                    #mid
                    mvaddstr(sh // 2 + 14, sw // 2 + (-38 + (20 * placementCount)) + 7, reference["knife"][1], dark_gray)
                    mvaddstr(sh // 2 + 14, sw // 2 + (-38 + (20 * placementCount)) + 9, reference["knife"][1], dark_gray)

                    mvaddstr(sh // 2 + 15, sw // 2 + (-38 + (20 * placementCount)) + 7, reference["knife"][1], dark_gray)
                    mvaddstr(sh // 2 + 15, sw // 2 + (-38 + (20 * placementCount)) + 9, reference["knife"][1], dark_gray)
                    #bottom
                    mvaddstr(sh // 2 + 16, sw // 2 + (-38 + (20 * placementCount)) + 8, reference["knife"][0], dark_gray)
                    mvaddstr(sh // 2 + 17, sw // 2 + (-38 + (20 * placementCount)) + 8, reference["knife"][0], dark_gray)
                    mvaddstr(sh // 2 + 18, sw // 2 + (-38 + (20 * placementCount)) + 8, reference["knife"][0], dark_gray)

                    PlaySound("mono/card/sacrifice_mark",0.7,(-0.15+(0.1*placementCount),0,1))
                    if len(sacrifices) == deck[oldSelect][3]:
                        sleep(0.3)
                        for position in sacrifices:
                            PlaySound("mono/card/sacrifice_default", 0.7, (-0.15 + (0.1 * position), 0, 1))
                            BoardID[2][position] = "blankCardSpace"
                            changeOldCardToWhite(BoardID[2][position], position)
                            sleep(0.2)

                        LastEvent = "sacrifice"
                        GameEvents()

                        sacrifices.clear()
                        sacrificeMade = True
                        sacrificeRequired = False
                        placing = True
                elif sacrificeRequired and not sacrificeMade and BoardID[2][placementCount] == "blankCardSpace" and not sacrificeSpeechGiven:
                    leshyTalk(f"The {reference[deck[oldSelect][0]][15]} requires {deck[oldSelect][3]} blood.", skippable=True)
                    sacrificeSpeechGiven = True
    if SelectCardReturn: # Return to picking card
        mvaddstr(sh // 2 + 21 ,sw // 2 + posCenter + (20 * placementCount)," ")
        SelectCardFromDeck(oldSelect)
    else:
        if bellPressed:
            changeOldCardToWhite(ignoreCard=True)
            try:
                printSideBig(deck[0], gray)
            except:
                printSideBig(None, None, True)
            BellObject(pressed=True)
        else: # places card
            PlaceCardOrColorChange(placementCount, 2, deck[oldSelect])
            changeOldCardToWhite(ignoreCard=True)
            tempStoreOldTitle = deck[oldSelect][0]
            deck.pop(oldSelect)
            try:
                printSideBig(deck[0], gray)
            except:
                printSideBig(None, None, True)

            LastEvent = f"CardPlace{tempStoreOldTitle}"
            GameEvents()
            sleep(0.4)
            SelectCardFromDeck()

#First in the event of the players turn, allows a selection from their current deck.
def SelectCardFromDeck(count=0, turnOffArrows=False):
    if not turnOffArrows and not deck == []:

        canGoLeft = False
        canGoRight = False

        wU = True
        while wU:
            ResetKey()
            printSideBig(deck[count], white, positionInDeck = count)
            #Place marker indicating left/right avaliability
            if not count -1 == -1:
                mvaddstr(sh // 2 - 4, sw // 2 + 55, "<", brightorange)
                canGoLeft = True
            else:
                mvaddstr(sh // 2 - 4, sw // 2 + 55, "<", gray)
                canGoLeft = False
            try:
                if deck[count+1]:
                    mvaddstr(sh // 2 - 4, sw // 2 + 99, ">", brightorange)
                    canGoRight = True
            except:
                mvaddstr(sh // 2 - 4, sw // 2 + 99, ">", gray)
                canGoRight = False

            checkInput = True

            while checkInput == True:
                #Grab key
                from engine.screenSetup import key
                if canGoLeft and key in ["KEY_LEFT","a"]:
                    count -= 1
                    CardPlaySound("quick", volume = 0.2)
                    checkInput = False
                elif canGoRight and key in ["KEY_RIGHT","d"]:
                    count += 1
                    CardPlaySound("quick", volume = 0.2)
                    checkInput = False
                elif key in ["w","KEY_UP"]:
                    printSideBig(deck[count], gray)  # Gray's out the portrait to show selected
                    positionPlacement(spectating=True)  # Moves onto placement
                    checkInput = False
                    wU = False
                elif key in ["^J", 'z', ' ']:
                    printSideBig(deck[count], brightorange)  # Gray's out the portrait to show selected
                    positionPlacement(count, False)  # Moves onto placement
                    checkInput = False
                    wU = False

                global LastEvent
                LastEvent = "SelectCardFromDeck"
                GameEvents()


    else:
        mvaddstr(sh // 2 - 4, sw // 2 + 55, " ")
        mvaddstr(sh // 2 - 4, sw // 2 + 99, " ")
        printSideBig(None, None, True)
        positionPlacement(spectating=True)

def drawNewCard(spawn=False):
    cardCentering = 59
    cardHeight = 13
    selectingSquirrel = True
    wU = True
    global squirrelCount
    global LastEvent

    def printSquirrelCard(color=white):
        if not squirrelCount == 0:
            for line in range(0,12):
                mvaddstr(sh // 2 + cardHeight + line, sw // 2 + cardCentering, squirrelback[line], color)
        else:
            for line in range(0,12):
                mvaddstr(sh // 2 + cardHeight + line, sw // 2 + cardCentering, blankCardSpace[line], color)
        if not color in [white,gray]:
            mvaddstr(sh // 2 + cardHeight + 12, sw // 2 + cardCentering + 8, "^", color)
        else:
            mvaddstr(sh // 2 + cardHeight + 12, sw // 2 + cardCentering + 8, " ")
    def printPowerCard(color=white):
        if not len(remainingDeck) == 0:
            for line in range(0,12):
                mvaddstr(sh // 2 + cardHeight + line, sw // 2 + cardCentering + 20, powerback[line], color)
        else:
            for line in range(0,12):
                mvaddstr(sh // 2 + cardHeight + line, sw // 2 + cardCentering + 20, blankCardSpace[line], color)
        if not color in [white,gray]:
            mvaddstr(sh // 2 + cardHeight + 12, sw // 2 + cardCentering +  20 + 8, "^", color)
        else:
            mvaddstr(sh // 2 + cardHeight + 12, sw // 2 + cardCentering + 20 + 8, " ")

    if spawn:
        printSquirrelCard(gray)
        printPowerCard(gray)
    elif squirrelCount == 0 and len(remainingDeck) == 0:
        printSquirrelCard(gray)
        printPowerCard(gray)
        SelectCardFromDeck()
    else:
        printSquirrelCard(brightorange)
        printPowerCard()

        LastEvent = "DrawingCard"
        GameEvents()
        while wU:
            if selectingSquirrel:
                printSquirrelCard(brightorange)
                printPowerCard(white)
            else:
                printSquirrelCard()
                printPowerCard(brightorange)

            checkInput = True
            while checkInput:
                from engine.screenSetup import key
                if key in ["KEY_LEFT","a"]:
                    selectingSquirrel = True
                    checkInput = False
                elif key in ["KEY_RIGHT","d"]:
                    selectingSquirrel = False
                    checkInput = False
                elif key in ["^J",'z',' ']:
                    if selectingSquirrel and not squirrelCount == 0:
                        deck.append(["squirrel",squirrel[12],squirrel[13], squirrel[14]])
                        squirrelCount -= 1
                        LastEvent = "DrewSquirrel"
                        GameEvents()
                        wU = False
                        checkInput = False
                    elif not selectingSquirrel and not len(remainingDeck) == 0:
                        deckChoice = choice(remainingDeck)
                        deck.append(deckChoice)
                        remainingDeck.remove(deckChoice)
                        LastEvent = "DrewPower"
                        GameEvents()
                        wU = False
                        checkInput = False

        printSquirrelCard(gray)
        printPowerCard(gray)
        CardPlaySound("quick")


#Misc Features

scaleTip = 0

def Scales(color = gray, scaleWeight=0, scaleSpawn = False, scaleRefresh = False):
    global scaleTip
    scaleDictionary = {
        -5 : scaleneg5,
        -4 : scaleneg4,
        -3 : scaleneg3,
        -2 : scaleneg2,
        -1 : scaleneg1,
        0 : scale0,
        1 : scale1,
        2 : scale2,
        3 : scale3,
        4 : scale4,
        5 : scale5
    }

    def scalePrint(Weight):
        count = 0
        for _ in range(0, 22):
            mvaddstr(sh // 2 + count - 18, sw // 2 - 83, scaleDictionary[Weight][count], color)
            count += 1
        sleep(0.15)

    if scaleSpawn:
        PlaySound("mono/scale/scale_enter",0.6, (-0.2, 0, 0.6))
        color = dark_gray
        scalePrint(scaleWeight)
        color = mediocre_gray
        scalePrint(scaleWeight)
        color = gray
        scalePrint(scaleWeight)
    if scaleRefresh:
        scaleTip = scaleWeight
        scalePrint(scaleTip)
        PlaySound("mono/scale/scale_tick", round(uniform(0.6,0.7),2), (-0.2, 0, 0.6))
    elif not scaleWeight == 0:
        if scaleWeight > 0:
            pointSyntax = +1
            scaleWeightLen = scaleWeight
        else:
            pointSyntax = -1
            scaleWeightLen = -scaleWeight
        count = 0
        for point in range(0, scaleWeightLen): # add a point
            scaleTip += pointSyntax
            count += 1
            if not (scaleTip >= 6 or scaleTip <= -6): # not overboard, doesnt cause error
                scalePrint(scaleTip)
            else: # accounts for scale tip delay
                sleep(0.15)
            if scaleWeight < 0: # Turn pitch down if being attacked
                PlaySound("mono/scale/scale_tick", round(uniform(0.6,0.7),2), (-0.2, 0, 0.6), pitch= 1 - 0.05 * count)
            else: # Turn pitch up if attacking
                PlaySound("mono/scale/scale_tick", round(uniform(0.6,0.7),2), (-0.2, 0, 0.6), pitch= 1 + 0.05 * count)
            sleep(0.1)
        sleep(0.5)

def BellObject(color = gray, spawn=False, pressed = False):
    global LastEvent
    if spawn:

        LastEvent = "BellSpawn"
        GameEvents()

        PlaySound("mono/bell/combatbell_enter",0.8,(-0.3,0,0.8))
        def spawnBell():
            count = 0
            for _ in range(0,12):
                mvaddstr(sh // 2 + count + 9, sw // 2 -80, bell[count], color)
                count +=1
            count = 0
            sleep(0.15)
        color = dark_gray
        spawnBell()
        color = mediocre_gray
        spawnBell()
        color = gray
        spawnBell()
        global bellEnabled
        bellEnabled = True
    else:
        def NotPressed():
            [mvaddstr(sh // 2 + x + 9, sw // 2 -80, bell[x], color) for x in range(0,12)]
        @threaded
        def Pressed():
            count = 0
            mvaddstr(sh // 2 + count + 9, sw // 2 - 80, bell[13], color) # clear top
            mvaddstr(sh // 2 + count + 1 + 9, sw // 2 - 80, bell[count], color) #push
            count += 2
            for _ in range(0,10):
                mvaddstr(sh // 2 + count + 9, sw // 2 -80, bell[count], color) # rest of bell
                count +=1

        if pressed:

            color = gray
            Pressed()
            PlaySound("mono/bell/combatbell_ring",0.8,(-0.3,0,0.8))
            sleep(0.5)
            NotPressed()

            LastEvent = 'BellPressed'
            GameEvents()

            AttackPhase()
        else:
            NotPressed()

candlesActive = 2

def Candles(spawn=False, relight = False, snuffOut = False):
    global candlesActive

    @threaded
    def candleAnimation(status):
        if status == 'left':
            candleHeight = 8
            candleCentering = -88
        elif status == 'right':
            candleHeight = 10
            candleCentering = -95
        PlaySound("mono/candle/candle_gainLife",1,(-0.35,0,0.8))
        while (status == 'left' and candlesActive == 2) or (status == 'right' and candlesActive >= 1):
                mvaddstr(sh // 2 + candleHeight, sw // 2 + candleCentering, choice(["ϱ","ϭ","δ","∂"]), choice([brightorange, orange, dark_orange, yellow]))#│ϼ
                sleep(round(uniform(0.2,0.5),1))
        PlaySound("mono/candle/candle_loseLife", 1, (-0.35, 0, 0.8))
        mvaddstr(sh // 2 + candleHeight, sw // 2 + candleCentering, choice(["ϧ","ϩ"]),gray)  # │ϼ

    def printCandleBase(status='left', spawn = False, color = gray):
        if status == 'right':
            [mvaddstr(sh // 2 + 11 + x, sw // 2 -97, candleBaseShort[x], color) for x in range(0, 10)]
        else:
            [mvaddstr(sh // 2 + 9 + x, sw // 2 -90, candleBaseLong[x], color) for x in range(0, 12)]
    if relight: # Will try a re-light
        if candlesActive == 1:
            leshyTalk(choice(["Your lives are restored.","You will not perish quite yet.","Need a light?","Reignite.","Let me relight your candles."]))
            candlesActive = 2
            candleAnimation('left')
            candleAnimation('right')
    elif spawn:
        PlaySound("mono/candle/candle_place", 0.7, (-0.35, 0, 0.8))
        printCandleBase('right', color=dark_gray)
        printCandleBase(color=dark_gray)
        sleep(0.15)
        printCandleBase('right', color=mediocre_gray)
        printCandleBase(color=mediocre_gray)
        sleep(0.15)
        printCandleBase('right')
        printCandleBase()
        sleep(0.3)
        candleAnimation('left')
        sleep(0.2)
        candleAnimation('right')
    elif snuffOut:
        candlesActive -= 1


#Sounds

def CardPlaySound(tone="normal", position=(0,0,0), volume=0.7):
    if tone == "normal":
        normal = [
            "card#1",
            "card#2",
            "card#3",
            "card#4",
            "card#5",
            "card#6",
            "card#7",
            "card#8",
            "card#9",
            "card#10"
        ]
        PlaySound(f"mono/card/{choice(normal)}", volume, position)
    if tone == "quick":
        quick = [
            "cardquick#1",
            "cardquick#2",
            "cardquick#3",
            "cardquick#4"
        ]
        PlaySound(f"mono/card/{choice(quick)}", volume, position)
    if tone == "glow":
        glow = [
            "cardslot_glow#1",
            "cardslot_glow#2",
            "cardslot_glow#3",
            "cardslot_glow#4"
        ]
        PlaySound(f"mono/card/{choice(glow)}", volume, position)


from game.gameplayEvents import GameEvents # Game Events and triggers