# Square Tic Tac Toe

In Tic Tac Toe, a player wins by forming a line with three consecutive cells in any direction — horizontal, vertical or diagonal. In this modified version, a player has to form a square, i.e. four cells forming 90 degree angles and equidistant from each other.

A 3x3 grid would be too small a playing area, so 4x4 grid is used instead. Compared to 8 possible lines in Tic Tac Toe, this game has 20 possible squares. Can you spot all of them? Here's an illustration to help you:

![Types of Squares](https://learnbyexample.github.io/practice_python_projects/images/square_tic_tac_toe/types_of_squares.png)

# Screenshot

Terminal dimension should be at least 84x25 (characters x lines) for the game widgets to appear properly. When you run the app, you should get an initial screen similar to the one shown below:

![Square Tic Tac Toe initial screen](https://github.com/learnbyexample/TUI-apps/raw/main/SquareTicTacToe/square_tictactoe.png)

# Guide

* Click the **New Game** button to start a new game. Existing game, if any, will be abandoned.
* You can choose between **Easy** (default) and **Hard** modes by clicking those buttons.
    * In *Easy* mode, the AI will make the first move with a 50% chance and afterwards it will make a move randomly in response to user moves.
    * In *Hard* mode, the AI will always make the first move and at best you'll be able to TIE the game ;)
    * These choices will come into effect only after a new game is started.
* Press **d** key to toggle between light and dark themes.
* Press **q** key or **Ctrl+c** to quit the app.

User moves are denoted by the ⭕️ character and AI moves are denoted by the ✖️  character.

The text panel to the left of the game board displays the current status of the game. If the game ends with one of the players forming a valid square, the winning square will be highlighted.

