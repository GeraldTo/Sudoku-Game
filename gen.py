
import random
from copy import copy, deepcopy

size = 9
cube = 3
sudo=[] # array to hold board that is eventually returned to the user

def init(puz): # initiallizes a board passed into it
    for i in range(9):  # loops through booard 
        scol = [] 
        for j in range(9): 
            scol.append(0)  # appends 0 at each position of row
        puz.append(scol)  # then appends row to the board

def fill_diag(puz): # fills board with random numbers 1-9, diagonally in 3x3 cubes
    for dig in range(3):    # requires no check and increases randomness of board
        k = 0
        while k < 9:    # puts current number in a radom position in cube by
            pos = random.randint(0,8)   # calling random and checking if its empty
            tempr = (dig*3)+int(pos/3)
            tempc = (dig*3)+int(pos%3)
            if puz[tempr][tempc] == 0:
                puz[tempr][tempc] = k+1
                k+=1
    
def printsudo(puz): # loops through board and prints board
    print("\n    Random Board") # used for testing purposes
    for i in range(9):
        if(i%3==0 and i>0):
            print('---------------------')  # prints a line for boarder
        for j in range(9):
            if(j%3==0 and j>0):
                print('|',end=' ') # prints a line for boarder
            if(puz[i][j]!=0 or puz[i][j]!=0):
                print(puz[i][j],end=' ')
            else:
                print(' ',end=' ')
        print()

def checkrow(puz,sol,r,c): # checks if sol is possibe within row
    for i in range(9):  # checks every position in row to see if sol ever appears
        if puz[r][i]==sol and i != c:
            return False 
    return True

def checkcol(puz,sol,r,c):  # checks if sol is possibe within column
    for i in range(9): # checks every position in column to see if sol ever appears
        if puz[i][c]==sol and i != r:
            return False
    return True

def checkcube(puz,sol,r,c): # checks if sol is possibe within cube
    ro = int(r/3)*3 # dividing by 3 as an int then multiplying
    co = int(c/3)*3 # by 3 gives 1st position within a cube
    for i in range(9): # loops within cube by geting divion and mod of 3 to get position
        if puz[ro+int(i/3)][co+int(i%3)] == sol and ro+int(i/3) != r and co+int(i%3) != c:
            return False
    return True

def checkall(puz,sol,r,c): # runs all the checks in one function
    if  checkcol(puz,sol,r,c) and checkrow(puz,sol,r,c) and checkcube(puz,sol,r,c):
        return True
    return False 

def backtrack(puz,r,c): # generates a completed board by looping through every possible board until a solution is found 
    if r>8: # a valid board is found when it loops through it all passed possibe rows
        return True
    rnew = r
    cnew = 0
    if c == 8: # resets column and increments row when it hits the last position of the row
        rnew = r+1
        cnew = 0
    else:
        cnew = c+1
    if puz[r][c]==0:   # when it has a empty space it puts a valid number within the spot
        for i in range(9):
            if checkall(puz,(i+1),r,c): # checks if valid
                puz[r][c] = (i+1)
                if backtrack(puz,r,c):  # recursively checks for position with new board
                    return True     # when one fails it tries the next position
        return False    # if there are no valid numbers that can go with in spot it backtracks to previous position
    else:   # when the spot is taken it recursively goes to the next postion
        if backtrack(puz,rnew,cnew):
            return True
        return False

def create_spaces(puz): # fills a board with white space and makes sure theres only one valid solution
    diff = 20 # runs removal 20 times
    while(diff>0): 
        i = random.randint(0,8)  # grabs a random position with random
        j = random.randint(0,8)
        save = puz[i][j] # saves number in position to use if fails
        puz[i][j] = 0
        temp = deepcopy(puz)
        if backtrack(temp,i,j): # runs back tracking to see if there is another possible solution
            if temp[i][j] != save:  # resets if position is not back up and reloops
                puz[i][j] = save
                diff-=1       

def count_spaces(puz):  # counts spaces by seeing which position is 0 
    spaces = 0
    for i in range(9):
        for j in range(9):
            if(puz[i][j]==0):
                spaces+=1
    return spaces

def create_board(diff): # generates a complted board to be used
    puz = []
    init(puz)
    fill_diag(puz)
    if backtrack(puz,0,0): # backtracks with initial diagonal board
        create_spaces(puz)  
        spaces = count_spaces(puz)
        global sudo
        if diff == 1:   # reloops until its in desired range
            if(spaces>36 and spaces <=42): # 42 48
                sudo = puz  # completes board
            else:
                create_board(diff)
        else:
            if diff == 2:
                if(spaces>52 and spaces <=58):
                    sudo = puz # completes board
                else:
                    create_board(diff)
    else:   # reloops if backtracking fails on intitial board
        create_board(diff)

def getBoard(diff): # return function of a fully generated board
    create_board(diff)
    global sudo
    return sudo

