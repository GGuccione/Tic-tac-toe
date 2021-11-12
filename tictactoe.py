import PySimpleGUI as sg
import random

# Player 1, 2

symbols = {1: None, 2: None}  # P1, P2. If X is player 1 then 1:"X". If X is player 2 then 2:"X". Player 2 is also COM.
initializing = True
chosenMode = None
mode = None  # 0 = vs computer, 1 = vs player
startingTurn = "X"
turn = "X"  # Placeholder value
hintID = None
record = [0, 0, 0] # [W, L, T] (Player has won W times, lost L times and tied T times)
layout = [
    [sg.Text("Player 1 Chooses:", key="initText"),
     sg.Text("Select gamemode:", key="initText2", visible=False)
     ],
    [
        sg.Button("X", key="initButton", size=(4, 1)),
        sg.Button("O", key="initButton2", size=(4, 1)),
        sg.Button("Player vs. Computer", key="initButton3", visible=False),
        sg.Button("Player vs. Player", key="initButton4", visible=False),
    ]
]
altLayout = [
    [sg.Text("", visible=False, key="winText")]
]
availableButtons = []
for a in range(0, 9, 3):  # Make buttons for altLayout:
    row = []
    for b in range(1, 4):
        row.append(sg.Button(" ", size=(8, 5), key=a + b, disabled_button_color=("White", "Transparent"),
                             button_color="Dark Blue"))
        availableButtons.append(a + b)
    altLayout.append(row)
altLayout[0].append(sg.Text("X:{} O:{} Ties:{}".format(record[0], record[1], record[2]), key="recordText"))
altLayout[1].append(sg.Button("Retry", key="retryButton", size=(7, 2)))
altLayout[2].append(sg.Button("Hint", key="hintButton", size=(7, 2)))
altLayout[3].append(sg.Button("Exit", key="exitButton", size=(7, 2)))
altLayout.append([sg.Text("{} to move".format(startingTurn), key="turnText", font=("Arial", 11))])
window = sg.Window("test", [[
    sg.Column(layout, key="layout"), sg.Column(altLayout, key="gameLayout", visible=False)
]])

grid = [
    "", "", "",
    "", "", "",
    "", "", ""
]

def winCheck():  # returns False if no one won, else returns symbol of winner if someone won
    for symbol in ["X", "O"]:  # Check diagonal, horizontal, and vertical wins.
        for i in range(0, 9, 3):  # Horizontal test:
            if "".join(grid[i:i + 3]) == symbol * 3:  # XXX or OOO
                return symbol
        for i in range(0, 3):  # Vertical test:
            if grid[i] + grid[i + 3] + grid[i + 6] == symbol * 3:
                return symbol
        if grid[0] + grid[4] + grid[8] == symbol * 3 or grid[2] + grid[4] + grid[6] == symbol * 3:  # Diagonal test
            return symbol
    return False  # Overall uses a lot of loops but is a very readable function. Can change to be more efficient.

def potentialWinCheck():  # For offense just use winning move and for defense, look at winning move of opponent and move there (pretty clever).
    wins = {"X": [], "O": []}  # Return dictionary with how each can win (wins as array since there can be more than 1)
    for symbol in ["X", "O"]:
        opposite = [s for s in ["X", "O"] if s != symbol][0]
        for i in range(0, 9, 3):
            currRow = grid[i:i + 3]
            if currRow.count(symbol) == 2 and opposite not in currRow:  # If 2/3 are covered by you, 1/3 is covered by nothing (win condition)
                wins[symbol].append(currRow.index("") + i)  # adjust for what row you're at
        for i in range(0, 3):
            currRow = [grid[i], grid[i + 3], grid[i + 6]]
            if currRow.count(symbol) == 2 and opposite not in currRow:
                wins[symbol].append((currRow.index("") * 3) + i)  # Math, can explain if needed
        for i in range(0, 4, 2):  # Will reach 0 and 2 only
            indexes = [i, i + (4 - i), 4 + (4 - i)]
            currRow = [grid[i], grid[i + (4 - i)], grid[4 + (4 - i)]]
            if currRow.count(symbol) == 2 and opposite not in currRow:
                wins[symbol].append(indexes[currRow.index("")])
    return wins

def move(index, symbol):
    button = window[index + 1]  # Remember button IDs are 1-9, idxes are 0-8
    print(f"{symbol} moved to {index}")
    button.update(text=symbol, disabled=True, button_color=("Dark Blue"))
    grid[index] = symbol  # Remember, event should be a num from 1-9 correlating to the position
    availableButtons.remove(index + 1)

def computerMove(computerSymbol, playerSymbol):  # Keep writing, FIX RANDOM ERRORS
    moves = potentialWinCheck()
    if moves[computerSymbol] != []:  # If you can win during your turn, take it.
        m = moves[computerSymbol][0]  # Index to win, m instead of move in order to preserve function
        move(m, computerSymbol)
    elif moves[playerSymbol] != []:
        m = moves[playerSymbol][0]
        move(m, computerSymbol)
    else:
        corners = [0, 2, 6, 8]
        availableCorners = [corner for corner in corners if corner+1 in availableButtons] # Corner + 1 because corner is counting from 0 and up, buttons are counting from 1 and up
        if len("".join(grid)) == 1:  # If only 1 move has been made(start of game)
            if grid.index(playerSymbol) in corners:  # If the opponent moved to any of these positions (corners)
                m = 4
            else:
                m = random.choice([corner for corner in corners if corner in availableButtons])
            move(m, computerSymbol)
        elif len("".join(grid)) == 3 and computerSymbol == grid[4]:  # If you have moved once (P1, COM, P1) in the middle
            safe = [i for i in (1, 3, 5, 7) if grid[i] == ""]  # Checks if spaces are occupied
            m = random.choice(safe)
            move(m, computerSymbol)
        else:
            if availableCorners != []: # Move to a corner if you can, if you can't then just move randomly
                move(random.choice(availableCorners), computerSymbol) # No -1 bc availableCorners is stored as indexes
            else:
                move(random.choice(availableButtons)-1, computerSymbol)
    #printGrid()
    #print(availableButtons, [corner for corner in [0, 2, 6, 8] if corner+1 in availableButtons])

def proceduralWinCheck():
    global mode  # Make sure we can reassign even from within a function
    winner = winCheck()
    if winner != False:
        window["winText"].update("{} WINS!".format(winner), visible=True)
        for i in range(1, 10):  # Disable all buttons:
            window[i].update(disabled=True)  # Make sure all of them are disabled:
        if winner == "X":
            record[0] += 1 # update record
        if winner == "O":
            record[1] += 1
            mode = 2
    if len("".join(grid)) == 9:  # If all board spaces are filled up:
        window["winText"].update("Tie!", visible=True)  # Go after player event has occurred
        record[2] += 1 # Add one tie to the record
        mode = 2 # Game over mode (no code for this kind of mode)
    window["recordText"].update("X:{} O:{} Ties:{}".format(record[0], record[1], record[2]))

def printGrid():
    for a in range(0, 9, 3):
        print(grid[a:a + 3])
    print("\n")

def hint(player, opponent):
    moves = potentialWinCheck()
    if moves[player] != []:
        id = moves[player][0] + 1
        # print(hintID, hintID in availableButtons)
        button = window[id]
        button.update(button_color=("green"))
    elif moves[opponent] != []:
        id = moves[opponent][0] + 1
        button = window[id]
        button.update(button_color="red")
    else:
        availableCorners = [corner for corner in [0, 2, 6, 8] if corner + 1 in availableButtons]
        if availableCorners != []:
            id = random.choice(availableCorners) + 1
            button = window[id]
            button.update(button_color="yellow")
        else:
            id = random.choice(availableButtons)
            button = window[id]
            button.update(button_color="yellow")
    return id

while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    if initializing is True:
        if event == "initButton" or event == "initButton2":  # Player 1 chooses symbol
            if event == "initButton2":  # Chose O
                symbols[1] = "O"
                symbols[2] = "X"
                turn = "O"
                startingTurn = "O"
            else:
                symbols[2] = "O"
                symbols[1] = "X"


            window["initText"].update(visible=False)
            window["initText2"].update(visible=True)

            window["initButton"].update(visible=False)
            window["initButton2"].update(visible=False)
            window["initButton3"].update(visible=True)
            window["initButton4"].update(visible=True)
        else:
            if event == "initButton3":  # Chose Player v. Computer
                mode = 0  # COM mode
            if event == "initButton4":  # Chose Player v. Player
                mode = 1
            chosenMode = mode
            # print(mode)
            initializing = False
            window["layout"].update(visible=False)
            window["gameLayout"].update(visible=True)
    else:  # When it's engaged in game mode: (Player will move)
        opponent = [s for s in ["X", "O"] if s != turn][0]
        if (event == "hintButton" or event == "exitButton" or event =="retryButton"): # Stacked all of them to make it cleaner
            if event == "hintButton" and mode != 2:
                hintID = hint(turn, opponent)
            if event == "exitButton":
                window.close()
            if event == "retryButton":
                #print("Retry")
                grid = ["" for x in range(0, 9)]
                for button in range(1, 10):
                    window[button].update(text=" ", disabled=False, button_color="Dark Blue")
                    #print(button)
                mode = chosenMode
                window["winText"].update("")
                availableButtons = [x for x in range(1, 10)]
                turn = startingTurn


            #print(grid, mode, chosenMode)


        else:
            print(turn)
            if window[event].get_text() == " ":  # if the text is not X or O (empty):
                if turn == "O":
                    move(event - 1, "O")
                elif turn == "X":
                    move(event - 1, "X")
            if hintID != None:
                window[hintID].update(button_color="Dark Blue") # Reset hint to original color
                hintID = None
            turn = opponent
            window["turnText"].update("{} to move".format(turn))  # update turn text
            print(turn)
            printGrid()
            proceduralWinCheck()  # Check if someone has won
            if mode == 0:  # If it's Player vs Computer: (COM moves after player)
                computerSymbol = symbols[2]  # Remember, COM is player 2 (if it's player v. COM)
                playerSymbol = symbols[1]  # Player 1's symbol
                computerMove(computerSymbol, playerSymbol)
                turn = [o for o in ["X", "O"] if o != turn][0]
                printGrid()
                proceduralWinCheck()
window.close()