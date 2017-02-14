#!/usr/bin/env python
import struct, string, math
from copy import deepcopy
from pprint import pprint

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""
  
    def __init__(self, size, board):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board

    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)
                                                                  
                                                                  
    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val
    
    return board
    
def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def solve(initial_board, forward_checking = False, MRV = False, Degree = False,
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    # print BoardArray
    # temp_board = deepcopy(initial_board)

    x=[[[a for a in range(1,size+1)] for b in range(size)] for c in range(size)]
    temp_board = deepcopy(initial_board)

    # x_temp=[[[a for a in range(1,size+1)] for b in range(size)] for c in range(size)]
    #Remove from domain existing entries
    domain =[[[]]]
    

    if(forward_checking==True and MRV ==False):
        print "Doing Forward Checking"
        for row in range(size):
            for column in range(size):            
                if (BoardArray[row][column]!=0):
                    x[row][column] =[]

                domain = initial_check(temp_board,row,column,x)

        done = for_prop(temp_board,domain)
        print "Did forward checking"
        temp_board.print_board()
        return done

    elif(forward_checking==True and MRV ==True):
        print "Doing MRV"
        for row in range(size):
            for column in range(size):            
                if (BoardArray[row][column]!=0):
                    x[row][column] =[]

                domain = initial_check(temp_board,row,column,x)

        done = MRV_prop(temp_board,domain)
        print "Did MRV"
        # print "Printing Board"
        # temp_board.print_board()
        return done
    
    else:
        print "Doing BackTrack"
        return back_track(temp_board,x,0,0)


def initial_check(board,row,column,temp):
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    temp_array1 =[]
    temp_array2 =[]
    temp_array3 =[]


    for r1 in range(size):
        if (BoardArray[r1][column]!=0):
            temp_array1.append(BoardArray[r1][column])
 
    for r in range(len(temp_array1)):
        if (temp_array1[r] in temp[row][column]):
            temp[row][column].remove(temp_array1[r])


    for c1 in range(size):
        if (BoardArray[row][c1]!=0):
            temp_array2.append(BoardArray[row][c1])
 

    for c in range(len(temp_array2)):
        # print temp[0][0]
        if (temp_array2[c] in temp[row][column]):
            temp[row][column].remove(temp_array2[c])

 
    a=row-(row%subsquare)
    b=column-(column%subsquare)

    for r in range(a,a+subsquare):
        for c in range(b,b+subsquare):
            if (BoardArray[r][c]!=0):
                temp_array3.append(BoardArray[r][c])

    for sub in range(len(temp_array3)):
        if (temp_array3[sub] in temp[row][column]):
            temp[row][column].remove(temp_array3[sub])
    
    # print "Function output is =================="
    # print temp 
    return temp



def for_check(board,row,column,value,x):
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    for r in range(size):
        if value in x[r][column]:
            x[r][column].remove(value)

        # for domain in x[r][column]:
        #     if(domain==value):

    for c in range(size):
        if value in x[row][c]:
            x[row][c].remove(value)
        # for domain in x[row][c]:
        #     if(domain==value):
        #         x[row][c].remove(value)

    a=row-(row%subsquare)
    b=column-(column%subsquare)

    for r in range(a,a+subsquare):
        for c in range(b,b+subsquare):
            if value in x[r][c]:
                x[r][c].remove(value)
            # for domain in x[r][c]:
            #     if(domain==value):
            #         x[r][c].remove(value)
    return x

def back_track(board,x,a,b):
    
    if is_complete(board):
        return board
    
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))
    
    a,b=findNext(board)
    for v in x[a][b]:
        if(isValid(board,a,b,v)):
            temp=deepcopy(board)
            tempboard=temp.CurrentGameBoard
            tempboard[a][b]=v
            temp.print_board()
            tempx=x
            # print x
            # if(forward_checking):
            #     tempx=for_check(temp,a,b,v,x)
                # print tempx
            # s = raw_input('--> ')
            result=back_track(temp,tempx,a,b)
            if(result!=False):
                return result
    return False

def for_prop(board, poss):
    # Get next unassigned cell
    row, col = findNext(board)
    if (row == col == -1): return True

    cell_poss = deepcopy(poss[row][col])

    for val in cell_poss:
        # Save original domain
        poss_copy = deepcopy(poss)

        if(isValid(board, row, col, val)):
            # Assign and recurse
            board.CurrentGameBoard[row][col] = val
            poss_updated = for_check(board, row, col, val, poss)
            if (for_prop(board,poss_updated)): return True

        # Restore the domain
        board.CurrentGameBoard[row][col] = 0
        poss = poss_copy

    return False


def findNext(board):
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    for x in range(size):
        for y in range(size):
            if (board.CurrentGameBoard[x][y]==0):
                return x,y
    return -1, -1


def MRV_coords(board, poss):
    BoardArray = board.CurrentGameBoard
    size = len(BoardArray)
    min_cords = 0, 0
    min_len = 100000
    for i in xrange(size):
        for j in xrange(size):
            if (((len(poss[i][j])) < min_len) and len(poss[i][j])>0):
                min_len = len(poss[i][j])
                min_cords = i, j
                # print "Min Cords are"
                # print min_cords 
    return min_cords


def MRV_prop(board, poss):
    # Get next unassigned cell
    row, col = MRV_coords(board,poss)
    # print row,col
    if (row == col == -1): return True
    
    # print poss
    cell_poss = deepcopy(poss[row][col])

    for val in cell_poss:
        # Save original domain
        poss_copy = deepcopy(poss)

        if(isValid(board, row, col, val)):
            # Assign and recurse
            board.CurrentGameBoard[row][col] = val
            poss_updated = for_check(board, row, col, val, poss)
            board.print_board()
            if (MRV_prop(board,poss_updated)): return True

        # Restore the domain
        board.CurrentGameBoard[row][col] = 0
        poss = poss_copy

    return False


# def findNext(board,a,b):
#     BoardArray = board.CurrentGameBoard
#     size = len(BoardArray)
#     for x in range(a,a+1):
#         for y in range(b,size):
#             if board.CurrentGameBoard[x][y]==0:
#                 return x,y
#     if a<size-1:
#         for x in range(a+1,size):
#             for y in range(0,size):
#                 if board.CurrentGameBoard[x][y]==0:
#                     return x,y
#     return -1,-1

def isValid(initial_board,row,column,value):

    BoardArray = initial_board.CurrentGameBoard
    size = len(BoardArray)
    #side length of board
    subsquare = int(math.sqrt(size))
    #side length of subsquare

    for r in range(size):
        if(BoardArray[r][column]==value):
            return False

    for c in range(size):
        if(BoardArray[row][c]==value):
            return False

    x=row-(row%subsquare)
    y=column-(column%subsquare)

    for r in range(x,x+subsquare):
        for c in range(y,y+subsquare):
            if(BoardArray[r][c]==value):
                return False
    return True