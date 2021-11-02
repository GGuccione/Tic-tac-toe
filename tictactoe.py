import PySimpleGUI as sg

# Player 1, 2
# Computer A.I not finished yet

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
for a in range(0, 9, 3): # Make buttons for altLayout:
    row = []
    for b in range(1, 4):
        row.append(sg.Button(" ", size=(8,5), key=a+b, disabled_button_color=("White", "Transparent")))
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
            if event == "Player vs. Computer":
                mode = 0
            if event == "Player vs. Player":
                mode = 1
            initializing = False
            window["layout"].update(visible=False)
            window["gameLayout"].update(visible=True)
    else: # When it's engaged in game mode:
        button = window[event]
        if button.get_text() == " ":
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
        if len("".join(grid)) == 9: # If all board spaces are filled up:
            window["winText"].update("Tie!", visible=True)


window.close()