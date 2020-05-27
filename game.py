import gen
import tkinter as tk
from copy import copy, deepcopy
import pickle

class Game(tk.Tk): # initial window for the game
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.top()
        self.switcher(StartGame)

    def space(self,num,prev):   # used to create a row of white space by creating an empty label
        mess = tk.Label(prev, height=num)
        mess.grid() # places space

    def switcher(self, frame_class,info=None):  # switches pages by clearing current frame 
        new_frame = frame_class(self,info)      # and uses a new one to replace it
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame             
        self._frame.grid()  # places new pages

    def switchPages(self,txt,newPage):  # this switches pages based on previous page
        if txt == "Easy" or txt == "Hard" or txt == "Resume":
            self.switcher(newPage,txt)
        else:
            self.switcher(newPage)
    
    def button(self,new_page,prev,txt,puz=None):    # generates buttons that are used to switch pages and are uniform
        pos = tk.Button(prev, text=txt,bg="lightgray",height=2,width=12, font="Verdana 16", command=lambda: [self.switchPages(txt,new_page)])
        pos.grid(columnspan=20) 
        self.space(1,prev)

    def top(self):  # prints logo by creating a lable
        self.space(1,self)
        mess = tk.Label(self,text="SUDOKU",bg="white", height=2, width=20,relief="solid", font="Verdana 24 bold")
        mess.grid() # places logo on top
        self.space(1,self)

class StartGame(tk.Frame):  # start space of game
    def __init__(self, master,info=None):
        tk.Frame.__init__(self, master) # places everything on master which is the  game application
        master.space(5,self)
        master.button(Menu,self,"Play") # asks user to press play to go to menu
        master.space(7,self)

class Menu(tk.Frame):   # menu page displays options for game by listing multiple pages to go to
    def __init__(self, master,info=None):
        tk.Frame.__init__(self, master) 
        master.button(Sudoku,self,"Resume")
        master.button(Sudoku,self,"Easy")
        master.button(Sudoku,self,"Hard")
        master.button(HowTo,self,"How To")
        master.space(1,self)

class HowTo(tk.Frame):  # how to page lists the instruction onn how to play
    def __init__(self, master,info=None):
        tk.Frame.__init__(self, master)
        f = open("howto.txt", "r")  # loops through text document that has instructions
        rules = tk.Text(self,height=20,width=75, font="Verdana 14") 
        temp = "\n"
        for x in f: 
            temp = temp + (x + "\n")
        rules.insert("1.0", temp)
        rules.config(state="disabled")
        rules.grid()    # places instructions in a lable on screen
        master.space(1,self)
        master.button(Menu,self,"Menu")
        master.space(1,self)

class Sudoku(tk.Frame):
    squares = 81
    def __init__(self, master,info=None):
        tk.Frame.__init__(self, master)
        original = []   # stores an origional copy of the initial sudoku
        change = [] # stores orional copy and changes made to it
        if info == "Resume":    # either generates a new board or uses a previous one
            try:    # uses a previous one by uses a pickled copy to open and generates the new screen
                pickle_or = open("original.pickle","rb")
                original = pickle.load(pickle_or)
                pickle_or.close()
                pickle_ch = open("change.pickle","rb")
                change = pickle.load(pickle_ch)
                pickle_ch.close()
                if change != []:
                    self.screen(original,change,master)
                else:
                    self.noBoard(master)
            except:
                self.noBoard(master)
        else:   # generates a new board then generates the screen for it
            if info == "Easy":
                original = gen.getBoard(1)
            elif info == "Hard":
                original = gen.getBoard(2)
            change = deepcopy(original)     
            self.screen(original,change,master)   
        master.space(1,self)
        txt = "Exit"   # creates a button that exits and saves with pickling
        pos = tk.Button(self, text=txt,bg="lightgray",height=2,width=12, font="Verdana 16", command=lambda: [master.switchPages(txt,Menu),self.save(txt,original,change)])
        pos.grid(columnspan=20)
        master.space(1,self) 

    def screen(self,original,change,master):
        board = [] # creates an array of entry widgets for user to edit
        self.gridBoard(original,board,change,master) # generates an interative board
        self.inputToBoard(original,change,board) # makes sure only valid entries enter
        

    def noBoard(self,master): # if there is no game to resume it prompts user to create a new one
        rules = tk.Label(self,height=18,width=35, text="No game to resume.\n Create a new game",font="Verdana 24")
        rules.grid(row=0,columnspan=20,rowspan=16)  # forced to go to menu

    def save(self,txt,puz1,puz2): #saves the 2 arrays in a file by pickling
        pickle_out = open("original.pickle","wb")
        pickle.dump(puz1, pickle_out)
        pickle_out.close()
        pickle_out = open("change.pickle","wb")
        pickle.dump(puz2, pickle_out)
        pickle_out.close()

    def squaresLeft(self,board): # displays the number of spaces left to finish the game
        left = tk.Label(self,height=1, font="Verdana 24")   # uses a lable and a global variable counter
        left.grid(row = 0,columnspan=20)
        if self.squares!=0: 
            left.config(text = " "+ str(self.squares)+ " squares left ")
        else:   # once there is no more spaces left declare the user a winner
            left.config(bg = "gray",text = "Winner! Start a new game.")
            for y in board:
                for z in y:
                    z.config(state="disabled",fg="gray")

    def inputToBoard(self,original,change,board): # dictates what the user is allowed to input
        for r in range(9):
            for c in range(9):
                def userInput(inp,wid): # defines a function of valid input
                    total=""
                    widArr = wid.split(".")
                    for c in widArr[2]: # uses the name of the widget to determine the current postion by grabing the last number
                        if c.isdigit(): 
                            total=total+c
                    if total == "": total = "1"
                    tempc = (int(total)%9)-1    # translates the number into coordinates
                    if(tempc==-1):tempc = 8
                    tempr = int(int(total)/9)
                    if(tempc==8):tempr = tempr-1
                    if inp.isdigit() and int(inp)>0 and int(inp)<10:    # input has to be blank or number 1-9 to be valid
                        if gen.checkall(change,int(inp),tempr,tempc): # once validated it determines wheather it follows sudoku rules 
                            change[tempr][tempc]=int(inp)               # by checking row column and square 
                            self.squares -= 1                       # once valid it sets value to change array and decrements counter
                            self.squaresLeft(board)
                        else:   # if it doesnt follow sudoku rules the user can enter it but its marked as red and doesnt decrement counter
                            board[tempr][tempc].config(bg="red")
                        return True
                    elif inp == "": # if the user removes an input the square becomes white annd its removed from the changed array
                        board[tempr][tempc].config(bg="white")  
                        if change[tempr][tempc] != 0:   # increases counter if user removes a number in changed array
                            self.squares += 1 
                            self.squaresLeft(board)
                            change[tempr][tempc] = 0
                        return True
                    else:
                        return False
                reg = board[r][c].register(userInput)   
                board[r][c].config(validate="key",validatecommand=(reg,'%P','%W')) # if input is invalid it cant be inputed

    def boarder(self,r,c,loc):  # creates boarders for the sudoku board with labels
        if loc == "top":    # determines type of boarder
            top=tk.Label(self,bg="black",width=18,height=1,relief="solid", font="Verdana 4")
            top.grid(row=r,column=c)
        if loc == "side":
            side=tk.Label(self,bg="black",width=1,height=4,relief="solid", font="Verdana 8")
            side.grid(row=r,column=c)

    def gridBoard(self,original,board,change,master): # creates initial board for user on screen
        for r in range(11): # 11 is used because each side has 9 boxes plus the 2 boarders for the seperation into squares
            boardRow = []
            for c in range(11):
                if(c==3 or c==7):self.boarder(r+1,c,"side") # at the 3rd and 7th spot it inputs a boarder widget
                if(r==3 or r==7):self.boarder(r+1,c,"top")
                if(r<9 and c<9): # grabs from the chnage and origional array and inputs it into the entry array
                    boardRow.append(tk.Entry(self,width=2,relief="solid", font="Verdana 32",justify="center")) 
                    if(original[r][c]!=0):  # if its from the orional array the user cant edit
                        boardRow[c].insert(0,str(original[r][c]))
                        self.squares -= 1 
                        boardRow[c].config(state="disabled",fg="gray")
                    elif change != None:
                        if (change[r][c]!=0):
                            boardRow[c].insert(0,str(change[r][c])) 
                            self.squares -= 1 
                    tempc = deepcopy(c) # this is used to determine where it goes on the screen by accounting for the widgets
                    tempr = deepcopy(r+1)
                    if c>=6:
                        tempc=tempc+2
                    elif c>=3:
                        tempc=tempc+1
                    if r>=6:
                        tempr=tempr+2
                    elif r>=3:
                        tempr=tempr+1
                    boardRow[c].grid(row=tempr,column=tempc)
            board.append(boardRow)
        self.squaresLeft(board) 
        if self.squares == 0: # if there are no squares left on the start that means the board has been completed 
            self.noBoard(master)    # the user is prompted to create a new game

root = Game() # creates an instance of the game
root.title("Sudoku")
root.mainloop() # loops game until the user exits


