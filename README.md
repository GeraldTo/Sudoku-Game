# Sudoku-Game

 A sudoku game made in python with tkinter and uses backtracking to generate the board

Backend:
      The backend is gen.py. This file allows the creation of a sudoku board based on one of the 2 implemented difficulties.
   The board is stored in a 2d array of integer. is accomplised with the backtracking algorithm which checks evry possible number 
   until a valid solution is found. 
Frontend:
      The frontend is game.py. This file creates a gui for the user to play sudoku. This is done through the tkinter library which
   is a gui. There is the game class which has a switcher function the allows the user to switch frames/classes. The other classes
   represent different pages that the user can enter. There is the start screen, menu, game screen, and instruction page.
