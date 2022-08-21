import time
import random
import os

eyesclosed = 0


def eyeSwitcher(eyeChoice):  # Random Eye Choice or will use given choice
    if eyeChoice == False:
        eyeChoice = random.choice(["closed", "open"])
        global eyesclosed  # Eyes not closed beyond one turn (blinking effect)
        if eyesclosed == 1:
            eyeChoice = "open"
            eyesclosed = 0
        if eyeChoice == "closed":
            eyesclosed = 1
    return eyeChoice


def boardPrinter(theBoard, x, eyeChoice):
    os.system("cls")
    lineCount = 1
    for i in theBoard:  # Setting Up the basic board + Putting Player down
        if lineCount == 2:
            print("----- ----- ----- -----" + f"       \033[0;31;49m{eyes(eyeSwitcher(eyeChoice))}\033[0;37;49m")
            print(" ".join(i) + f"  {dialouge(x)}")
        else:
            print("----- ----- ----- -----")
            print(" ".join(i))
        print("----- ----- ----- -----")
        lineCount += 1


def cardDisplay(dialouge):  # Basic Default Card Choice
    os.system("cls")
    print("----------- -----------")
    for x in range(0, 2):
        print("|         | |         |")
    print("|         | |         |       \033[0;31;49m꩜  ꩜\033[0;37;49m")
    print(f"|    P    | |    S    | {dialouge}")
    for x in range(0, 3):
        print("|         | |         |")
    print("----------- -----------")


def eyes(x):  # Eye Choices
    switcher = {
        "open": "꩜  ꩜",
        "closed": "-  -",
        "none": ""
    }
    return switcher.get(x, "nothing")


def dialouge(x):  # Common Dialouge
    switcher = {
        "blank": "Make a placement",
        "nogo": "You cannot go outside your play area",
        "placed": "You have placed a peice",
    }
    return switcher.get(x, x)  # Will Either return a found common value or return the original value


def placementDialouge(board):  # Scripted Placing
    time.sleep(random.randint(2, 3))
    boardPrinter(board, "Hmm....", "closed")
    time.sleep(random.randint(3, 4))
    boardPrinter(board, "A moment please...", "open")
    time.sleep(random.randint(2, 3))
    boardPrinter(board, "That should do the trick", "open")
    time.sleep(5)


def tutorialCard():  # Tutorial
    os.system("cls")
    switcher = {
        0: "Welcome to the Tutorial",
        1: "Begin with a basic card selection",
        2: "There are two cards.",
        3: "Both have their own benifits"
    }
    switchCounter = 0
    for count in range(0, 3):
        print("----------- -----------")
        for x in range(0, 2):
            print("|         | |         |")
        print("|         | |         |       \033[0;31;49m꩜  ꩜\033[0;37;49m")
        print(f"|    P    | |    S    | {switcher.get(switchCounter)}")
        for x in range(0, 3):
            print("|         | |         |")
        print("----------- -----------")
        time.sleep(3)
        switchCounter += 1
        os.system("cls")


def endGameDialouge(x, firstGame):
    switcher = {
        0: "Hm, it seems you have bested me.",
        1: "A good first match",
        2: "You have played well...",
        3: "Another?",
        4: "Well played.",
        5: "That was an intense rematch.",
        6: "Perhaps another?",
        7: "It seems I have bested you.",
        8: "There is always a chance at another round",
        9: "Would you like to try again?",
        10: "I have beaten you.",
        11: "You can't win every game.",
        12: "Perhaps another round?"
    }
    if x == True and firstGame == True:
        dialougeMax = 4
        switchCount = 0
    if x == True and firstGame == False:
        switchCount = 4
        dialougeMax = 7
    if x == False and firstGame == True:
        switchCount = 7
        dialougeMax = 10
    if x == False and firstGame == False:
        switchCount = 10
        dialougeMax = 13
    while switchCount != dialougeMax:
        os.system("cls")
        print("                   \033[0;31;49m꩜  ꩜\033[0;37;49m")
        print(f"                        {switcher.get(switchCount)}")
        switchCount += 1
        time.sleep(random.randint(2, 3))


def quitDialouge(x):
    if x == True:
        os.system("cls")
        print("                              \033[0;31;49m꩜  ꩜\033[0;37;49m")
        print(f"                        Goodbye.")
        time.sleep(3)
        os.system("cls")
        print("                              \033[0;31;49m-  -\033[0;37;49m")
        time.sleep(3)
        os.system("cls")
    else:
        os.system("cls")
        print("                              \033[0;31;49m꩜  ꩜\033[0;37;49m")
        print(f"                        I will require a valid answer")
