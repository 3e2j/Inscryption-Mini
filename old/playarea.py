# Test Program for Card Game
from old.dialouge import *

tutorial = True
EnticedToPlay = True
characterX = 1
characterY = 1
characterPosition = "| A |"
characterPlacementPiece = "| X |"
blank = "|   |"
dialougeChoice = "blank"
gameEnd = False
firstPlace = True
win = False
firstGame = True

placement = False  # Auto turn placement on

board = [[blank for a in range(4)] for b in range(3)]

# Initalise the Player Postion
board[characterY][characterX] = characterPosition
boardActual = []
boardActual = board


# Drawing A Card
def cardDraw(placement):
    dialouge = "Draw a card"
    if tutorial == True:
        # tutorialCard()
        dialouge = "Draw your first card."

    card = False
    while card == False:
        cardDisplay(dialouge)
        if tutorial == False and firstPlace == False:
            print("W to see the board.")
        card = input("Choice: ").upper()

        if tutorial == True and card == "W":
            dialouge = "We will get to that later..."
            card = False
        elif card == "W":
            boardPrinter(board, "...", "open")
            input("Press any key to return")
            card = False  # Starts the loop again
        # elif card != "S" or card != "P":
        # dialouge = "That is not a card."
        # card = False
    return card


cardDraw(placement)  # Start with card draw
placement = True

tutorial = False
while EnticedToPlay == True:
    while gameEnd != True and placement == True:
        # global boardActual

        boardPrinter(board, dialougeChoice, False)
        dialougeChoice = "blank"  # Reset the Choice Until Changed
        for i in board:
            def directionCheck(x):
                '''
                A Direction Check to make sure that the player cannot exit the board's boundies.
                X is defined as the player input as a str (WASD)
                '''
                check = True
                if x == "W" and characterY - 1 < 0:
                    check = False
                elif x == "S" and characterY + 1 > 2:
                    check = False
                elif x == "A" and characterX - 1 < 0:
                    check = False
                elif x == "D" and characterX + 1 > 3:
                    check = False
                return check

        print("\nInstructions:\nWASD to move placement point.\nP to interact.")
        keyboard = input("Input: ").upper()
        if directionCheck(keyboard) == True:  # Check Boundies
            if boardActual[characterY][characterX] != characterPlacementPiece:
                board[characterY][characterX] = blank

            if keyboard == "W":
                characterY -= 1
            elif keyboard == "S":
                characterY += 1
            elif keyboard == "A":
                characterX -= 1
            elif keyboard == "D":
                characterX += 1
            board[characterY][characterX] = characterPosition
        else:
            dialougeChoice = "nogo"
        if keyboard == "P":
            board[characterY][characterX] = characterPlacementPiece
            boardPrinter(board, "placed", False)

            # toggle placement to Seize board updates
            placement = False

    firstPlace = False

    placementDialouge(board)
    boardActual = board

    ### To do: Add updated placement of his piece here

    gameEnd = True  # End the game

    if gameEnd == False:
        placement = True
        cardDraw(placement)

endGameDialouge(win, firstGame)

firstGame = False
continueToPlay = input("Y or N: ").upper()
while continueToPlay not in "YN":  # Search for Valid.
    quitDialouge(False)
    continueToPlay = input("Y or N: ").upper()
if continueToPlay == "N":  # Switch off Game
    EnticedToPlay = False
if continueToPlay == "Y":  # Restart
    placement = True
    gameEnd = False

quitDialouge(True)
exit()