import PySimpleGUI as sg
import random

# Player 1, 2
# Computer A.I not finished yet

compTurn = None
initializing = True # player 1 = X, player 2 = O
mode = None # 0 = vs computer, 1 = vs player
turn = 1 # 0 = O, 1 = X ( AND PLAYER 1 STARTS FIRST )
layout = [
    [sg.Text("Player 1 Chooses:", key="initText"),
     sg.Text("Select gamemode:", key="initText2", visible=False)
     ],
    [
    sg.Button("X", key="initButton", size=(4, 1)),
    sg.Button("O", key="initButton2", size=(4,1)),
    sg.Button("Player vs. Computer", key="initButton3", visible=False),
    sg.Button("Player vs. Player", key="initButton4", visible=False),
      ]
          ]
altLayout = [
    [sg.Text("", visible=False, key="winText")]
]
availableButtons = []
for a in range(0, 9, 3): # Make buttons for altLayout:
    row = []
    for b in range(1, 4):
        row.append(sg.Button(" ", size=(8,5), key=a+b, disabled_button_color=("White", "Transparent")))
        availableButtons.append(a+b)
    altLayout.append(row)

window = sg.Window("test", [[
    sg.Column(layout, key="layout"), sg.Column(altLayout, key="gameLayout", visible=False)
]])

grid = [
    "", "", "",
    "", "", "",
    "", "", ""
]

def winCheck(): # returns False if no one won, else returns symbol of winner if someone won
    for symbol in ["X", "O"]: # Check diagonal, horizontal, and vertical wins.
        for i in range(0, 9, 3): # Horizontal test:
            if "".join(grid[i:i+3]) == symbol*3: # XXX or OOO
                return symbol
        for i in range(0, 3): # Vertical test:
            if grid[i]+grid[i+3]+grid[i+6] == symbol*3:
                return symbol
        if grid[0]+grid[4]+grid[8] == symbol*3 or grid[2]+grid[4]+grid[6] == symbol*3: # Diagonal test
            return symbol
    return False # Overall uses a lot of loops but is a very readable function. Can change to be more efficient.
def potentialWinCheck(): # For offense just use winning move and for defense, look at winning move of opponent and move there (pretty clever).
    wins = {"X":[], "O":[]}  # Return dictionary with how each can win (wins as array since there can be more than 1)
    for symbol in ["X", "O"]:
        opposite = [s for s in ["X", "O"] if s != symbol][0]
        for i in range(0, 9, 3):
            currRow = grid[i:i+3]
            if currRow.count(symbol) == 2 and opposite not in currRow: # If 2/3 are covered by you, 1/3 is covered by nothing (win condition)
                wins[symbol].append(currRow.index("")+i) # adjust for what row you're at
        for i in range(0, 3):
            currRow = [grid[i], grid[i+3], grid[i+6]]
            if currRow.count(symbol) == 2 and opposite not in currRow:
                wins[symbol].append((currRow.index("")*3)+i) # Math, can explain if needed
        for i in range(0, 4, 2): # Will reach 0 and 2 only
            indexes = [i, i+(4-i), 4+(4-i)]
            currRow = [grid[i], grid[i+(4-i)], grid[4+(4-i)]]
            if currRow.count(symbol) == 2 and opposite not in currRow:
                wins[symbol].append(indexes[currRow.index("")])
    return wins

while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    if initializing is True:
        if event == "initButton" or event == "initButton2":
            if event == "initButton2": # Chose O
                turn = 0
            window["initText"].update(visible=False)
            window["initText2"].update(visible=True)

            window["initButton"].update(visible=False)
            window["initButton2"].update(visible=False)
            window["initButton3"].update(visible=True)
            window["initButton4"].update(visible=True)
        else:
            if event == "initButton3":
                mode = 0
                compTurn = [opposite for opposite in [0, 1] if opposite != turn][0] # Opposite of starting turn, AKA opposite of player 1
            if event == "initButton4":
                mode = 1
            print(mode)
            initializing = False
            window["layout"].update(visible=False)
            window["gameLayout"].update(visible=True)
    else: # When it's engaged in game mode:
        button = window[event]
        if button.get_text() == " ":
            availableButtons.remove(event)
            if turn == 0:
                button.update(text="O")
                grid[event-1] = "O" # Remember, event should be a num from 1-9 correlating to the position
                window[event].update(disabled=True)
                turn = 1
            elif turn == 1:
                button.update(text="X")
                grid[event-1] = "X"
                window[event].update(disabled=True)
                turn = 0
        winner = winCheck()
        if winner != False:
            window["winText"].update("{} WINS!".format(winner), visible=True)
            for i in range(1, 10): # Disable all buttons:
                window[i].update(disabled=True) # Make sure all of them are disabled:
            mode = 2 # Game over mode (no code for this kind of mode)
        if len("".join(grid)) == 9: # If all board spaces are filled up:
            window["winText"].update("Tie!", visible=True) # Go after player event has occurred
            mode = 2
        if mode == 0: # If it's Player vs Computer:
            s = "" # symbol
            if turn == 0:
                s = "O"
            if turn == 1:
                s = "X"
            opp = [x for x in ["X", "O"] if x != s][0]
            moves = potentialWinCheck()
            if moves[s] != []: # If you can win during your turn, take it.
                move = moves[s][0] # Index to win
                window[move+1].update(text=s, disabled=True)
                availableButtons.remove(move+1)
                grid[move] = s
            elif moves[opp] != []: # If you can't win but can stop a loss, stop it.
                move = moves[opp][0]
                window[move+1].update(text=s, disabled=True)
                availableButtons.remove(move+1)
                grid[move] = s
            else: # Otherwise, pick one of the buttons randomly.
                pick = random.choice(availableButtons)
                window[pick].update(text=s, disabled=True)
                availableButtons.remove(pick)
                grid[pick-1] = s
            turn = [o for o in [0, 1] if o != turn][0]
            for a in range(0, 9, 3):
                print(grid[a:a+3])
            print("\n")
        winner = winCheck()
        if winner != False:
            window["winText"].update("{} WINS!".format(winner), visible=True)
            for i in range(1, 10): # Disable all buttons:
                window[i].update(disabled=True) # Make sure all of them are disabled:
            mode = 2
        if len("".join(grid)) == 9: # If all board spaces are filled up:
            window["winText"].update("Tie!", visible=True) # Go after player event has occurred
            mode = 2
window.close()