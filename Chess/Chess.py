import graphics as g
import Pieces as Piece
import copy
"""
almost fully-functional verison of chess

things not implemented:
pawn promotion,
en passant captures,
checkmates (normal checks are in though),
stalemates

looking back i really should've separated the graphics library stuff from the actual chess logic
if i ever come back to this though i'll definitely rewrite a bunch of stuff

"""

class Square():
    """
    chess board consists of these square classes
    i didn't use a regular array because i needed each square
    to hold a reference to it's graphics.py stuff
    
    **i really should have separated those two things
    
    """
    def __init__(self,rectObject:g.Rectangle, contents=""):
        """
        contents are typically either an empty string to denote an empty square
        or an instance of a Piece object
        """
        
        self.rectObject = rectObject
        self.contents = contents
        self.color = ""
        
        self.highlighted = False
        self.highlightedColor = "red"
        
        self.displayObject = g.Text(rectObject.getCenter(),self.contents)
        if (self.contents != ""):
            self.displayObject = g.Text(rectObject.getCenter(),self.contents.pieceName)
            
        self.displayObject.setSize(36)
    
    def DrawContents(self,window):
        self.displayObject.undraw()
        self.displayObject.draw(window)
        
    def UpdateContents(self,contents):
        self.contents = contents
        if (self.contents != ""):
            self.displayObject.undraw()
            self.displayObject = g.Text(self.rectObject.getCenter(),contents.pieceName)
            self.displayObject.setSize(36)
            
        else:
            self.displayObject = g.Text(self.rectObject.getCenter(),contents)
            self.displayObject.setSize(36)
            
class ChessBoard():
    def __init__(self,boardWindow:g.GraphWin, boardSquares:list):
        """
        this class is so horribly messy that i barely understood it when i came back to it
        
        boardSquares is a list that contains all the square objects from the board window
        """
        self.boardWindow = boardWindow
        self.boardSquares = boardSquares
        self.selectedSquare = None
        
        #used these variables to get what index is currently selected        
        self.rowIndex = 0
        self.columnIndex = 0
        
        #all three of these are used to store info based on the current selected/stored piece
        #storedIndex being it's original position
        self.storedIndex = []
        self.storedSquare = None
        self.storedPiece = None
        
        
        self.whitePieces = []
        self.blackPieces = []
        
        self.highlightedSquares = []
        
    def SetPieces(self,piecePlacement:dict):
        """
        pulls pieces/starting positions from the piecePlacement dict
        and inserts them into their respective Square objects in the self.boardSquares tuple
        
        """
        
        #this for loop handles the placement of all pieces with their starting positions
        #given by the piecePlacement dict
        for row in range(8):
            columns = []
            for column in range(8):
                squareObj = self.boardSquares[row][column]
                
                #special exception here for just pawns cause i couldn't figure out how to work them into the
                #normal piece placement below
                if (row == 1 or row == 6):
                    topOrBottom = ""
                    team = ""
                    temp = dict(piecePlacement)
                    pawn = copy.deepcopy(temp["pawn"])
                    obj = ""

                    if (row == 1):
                        topOrBottom = "top"
                        team = "black"
                    elif (row == 6):
                        topOrBottom = "bot"
                        team = "white"
                    
                    #each new piece has two characters for it's name,
                    #one for the black team and the other for the white team
                    #this just takes away the character from the team that it isn't on
                    if (team == "white"):
                        obj = piecePlacement["pawn"].pieceName[0]
                    elif (team == "black"):
                        obj = piecePlacement["pawn"].pieceName[1]
                    
                    #the pawn's ability to move up or down is based on this variable
                    pawn.topOrBot = topOrBottom
                    
                    pawn.team = team
                    
                    #i think this function adds the double move thing to the pawn's available moves
                    pawn.DunnoWhatToNameThis()
                    
                    pawn.pieceName = obj
                    pawn.pos = [row,column]
                    
                    squareObj.UpdateContents(pawn)
                    squareObj.DrawContents(self.boardWindow)
                    
                    if (team == "white"): self.whitePieces.append(pawn)
                    else: self.blackPieces.append(pawn)
                    
#                     self.storedPieces.append(pawn)
                
                #down here is the placement of other non-pawn pieces
                elif (row == 0 or row == 7):
                    #pretty much the same as the pawn placement
                    #couldn't fit pawns in here cause i needed to call the pawn's 'DunnoWhatToNameThis'
                    #function so i could get their whole double move thing
                    #and i didn't want to write a default function with the same name
                    #that does nothing for the other pieces
                    
                    for pos in piecePlacement:
                        if str(column) in pos:
                            
                            piece = copy.deepcopy(piecePlacement[pos])
                            topOrBottom = ""
                            team = ""
                            obj = ""
                            
                            if (row == 0):
                                topOrBottom = "top"
                                team = "black"
                            elif (row == 7):
                                topOrBottom = "bot"
                                team = "white"
                            
                            if (team == "white"):
                                obj = piecePlacement[pos].pieceName[0]
                                
                            elif (team == "black"):
                                obj = piecePlacement[pos].pieceName[1]
                                

                            if (team == "white"): self.whitePieces.append(piece)
                            else: self.blackPieces.append(piece)
                            

                            piece.topOrBot = topOrBottom
                            piece.team = team
                            piece.pos = [row,column]
                            
                            piece.pieceName = obj

                            squareObj.UpdateContents(piece)
                            squareObj.DrawContents(self.boardWindow)
                            
   
                columns.append(squareObj)
                

            self.boardSquares.append(columns)
        
        #highlights a square by default so the cursor is shown when the game is started
        self.boardSquares[self.rowIndex][self.columnIndex].rectObject.setFill("blue")
    
    def IsKingInCheck(self) -> list:
        """
        goes through the validMoves attribute of first the white pieces
        and then the black pieces
        to try and find an instance of a King object in either one
        
        if found returns [true,reference to king object]
        """
        for piece in self.whitePieces:
            for move in piece.validMoves:
                square = self.boardSquares[move[0]][move[1]]
                if (isinstance(square.contents,Piece.King)):
                    if (square.contents.team != piece.team):
                        return [True,square.contents]
        
        for piece in self.blackPieces:
            for move in piece.validMoves:
                square = self.boardSquares[move[0]][move[1]]
                if (isinstance(square.contents,Piece.King)):
                    if (square.contents.team != piece.team):
                        return [True,square.contents]
                    
        return [False,Piece.Piece]
    
    def UpdateMoves(self):
        """
        just calls the default UpdateValidMoves function in each piece
        """
        for piece in self.whitePieces:
            piece.UpdateValidMoves(piece.pos,self.boardSquares)

        for piece in self.blackPieces:
            piece.UpdateValidMoves(piece.pos,self.boardSquares)
        
    def HighlightMoves(self,piece):
        """
        pulls valid moves from the given piece object
        and sets the squares at their indices color to the square object's
        highlighted color attribute
        
        also appends the highlighted squares to the self.highlightedSquares for a reference to them
        """
        for move in piece.validMoves:
            square = self.boardSquares[move[0]][move[1]]
            square.rectObject.setFill(square.highlightedColor)
            square.highlighted = True
            self.highlightedSquares.append(square)
    
    def UndoHighlightedSquares(self):
        """
        same as the one above but the other way around
        """
        for square in self.highlightedSquares:
            square.rectObject.setFill(square.color)
            square.highlighted = False
            
        self.highlightedSquares = []
    
    def StorePiece(self,currentSquare:Square,piece):
        """
        takes in a reference to the square that the piece was on originally
        and the piece
        and sets the corresponding stored variables to match the piece/square
        """
        if (isinstance(currentSquare.contents,Piece.Piece)):
            self.storedPiece = piece
            self.storedSquare = currentSquare
            self.HighlightMoves(self.storedPiece)
            self.storedIndex = [self.rowIndex,self.columnIndex]
#             print(piece.validMoves)
#             print(currentSquare.contents)
        else:
            print("no piece in this square")
            print(currentSquare.contents)
    
    
    def PlacePiece(self,currentSquare:Square,canvas:g.GraphWin):
        """
        attempts to place the board's stored piece constrained by the piece's limits/whether the king is in check or not
        """
        currentIndex = [self.rowIndex,self.columnIndex]
        self.UndoHighlightedSquares()
        found = False
        
        storedBoardSquares = self.boardSquares
        storedBoardWindow = self.boardWindow
        
        for move in self.storedPiece.validMoves:
            thing = [move[0],move[1]]
            if currentIndex == thing:
                found = True
                
        if (found):           
            #super ugly super long if statement
            #checks if there is either a piece that isn't on the same team on the square
            #or if the square is empty
            if (isinstance(currentSquare.contents,Piece.Piece) and currentSquare.contents.team != self.storedPiece.team or isinstance(currentSquare.contents,Piece.Piece) == False):           
                self.UpdateMoves()
#                 check = self.IsKingInCheck()
                contents = currentSquare.contents
                
                #another pawn specific thing here
                #checks if the intial two square pawn thing is available
                #and takes it away when a move is made by the pawn
                if (self.storedPiece.canPawn == True):
                    self.storedPiece.moveLimit.pop()
                    self.storedPiece.canPawn = False
                
                self.storedSquare.displayObject.undraw()
                self.storedSquare.UpdateContents("")
                
                storedIndex = self.storedPiece.pos
                self.storedPiece.pos = currentIndex
    #             print(self.storedIndex)
                
                #used later to revert contents if a move results in the king being placed in check
                storedContents = currentSquare.contents
                
                currentSquare.UpdateContents(self.storedPiece)
                currentSquare.displayObject.draw(canvas)
                self.storedPiece.hasMoved = True
                
                #if a piece is captured it removes the piece from the stored white/black pieces list                
                if (isinstance(storedContents,Piece.Piece) == True):
                    if (storedContents.team == "white"):
                        index = self.whitePieces.index(storedContents)
                        self.whitePieces.pop(index)
                        print("worked")
                        
                    elif (storedContents.team == "black"):
                        index = self.blackPieces.index(storedContents)
                        self.blackPieces.pop(index)
                        print("workedb")
                        
                castledIndex = None
                check = self.IsKingInCheck()
                if (isinstance(self.storedPiece,Piece.King) and check[0] == False):
                    for move in self.storedPiece.validMoves:
                        thing = [move[0],move[1]]
                        print(thing)
                        if currentIndex == thing:
                            print("here")
                            move[2][0](self,move[2][1],move[2][2],move[2][3])
                            castledIndex = [move[2][1],move[2][2],move[2][3]]
                            
                self.UpdateMoves()
#                 print(check)
#

                
                #checks if the king is in check after the move
                if (check[0] == True and self.storedPiece.team == check[1].team):
                    #if true, reverts the changed square back with the storedContents variable form above 
                    self.storedSquare.UpdateContents(self.storedPiece)
                    self.storedSquare.displayObject.draw(canvas)
                    self.storedPiece.hasMoved = False
                    self.storedPiece.pos = storedIndex
                    
                    currentSquare.displayObject.undraw()
                    currentSquare.UpdateContents(storedContents)
                    currentSquare.displayObject.draw(canvas)
                    
#                     if (castledIndex != None):
#                         index = [castledIndex[0],castledIndex[1]]
#                         rookObj = castledIndex[2]
#                         
#                         square = self.boardSquares[index[0],index[1]]
#                         rookObj.pos = 
                        
                    
                    #appends the removed piece from the captured thing from before
                    if (isinstance(storedContents,Piece.Piece)):
                        if (storedContents.team == "white"):
                            self.whitePieces.append(storedContents)
                            print("worked")
                            
                        elif (storedContents.team == "black"):
                            self.blackPieces.append(storedContents)
                            print("workedb")
                     
                    print("king in check")
#             if (isinstance(self.storedPiece,Piece.King)):
#                 for move in self.storedPiece.validMoves:
#                     thing = [move[0],move[1]]
#                     print(thing)
#                     if currentIndex == thing:
#                         move[2][0](self,move[2][1],move[2][2],move[2][3])
                    
                    
        #removes stored piece by default so you aren't locked into moving a piece
        #after selecting it
        self.storedPiece = None
        self.storedSquare = None
        self.storedIndex = []
        
        
    def GetSquare(self,direction:str) -> Square:
        """
        misleading name now that i think about it
        uses the direction passed in to navigate the boardSquares list
        also highlights the square at the selected index
        
        eg. 'Right' increments self.columnIndex by 1 and returns the square at the stored [rowIndex][columnIndex]
        """
        squareList = self.boardSquares

        selectedSquare = squareList[self.rowIndex][self.columnIndex]
        
        selectedSquare.rectObject.setFill("blue")
        if (direction == "Right"):
            if (selectedSquare.highlighted == False):
                selectedSquare.rectObject.setFill(selectedSquare.color)                
            else:
                selectedSquare.rectObject.setFill(selectedSquare.highlightedColor)
            self.columnIndex += 1
            
        elif (direction == "Left"):
            if (selectedSquare.highlighted == False):
                selectedSquare.rectObject.setFill(selectedSquare.color)
            else:
                selectedSquare.rectObject.setFill(selectedSquare.highlightedColor)
            self.columnIndex -= 1
        
        elif (direction == "Up"):
            if (selectedSquare.highlighted == False):
                selectedSquare.rectObject.setFill(selectedSquare.color)
            else:
                selectedSquare.rectObject.setFill(selectedSquare.highlightedColor)
            self.rowIndex -= 1
            
        elif (direction == "Down"):
            if (selectedSquare.highlighted == False):
                selectedSquare.rectObject.setFill(selectedSquare.color)
            else:
                selectedSquare.rectObject.setFill(selectedSquare.highlightedColor)
            self.rowIndex += 1
        
        self.rowIndex = Clamp(self.rowIndex,0,7)
        self.columnIndex = Clamp(self.columnIndex,0,7)
        selectedSquare = squareList[self.rowIndex][self.columnIndex]
#         print(self.rowIndex,self.columnIndex)
        return selectedSquare
    
    
def SetupBoard(screenX:float,screenY:float) -> ChessBoard:
    """
    sets up the graphwin canvas with screenX,screenY dimensions
    and also creates/returns it's respective ChessBoard object
    """
    
    #also used this to get an alternating thing
    num = 0
    boardSquares = []
     
    boardWindow = g.GraphWin("chess time",screenX,screenY,autoflush=False)
    
    squareWidth = screenX/8
    squareHeight = screenY/8
    
    #this for loop starts from 1 and not 0
    #because the starting square height has to be at least 1 full square's height
    for column in range(1,9):
        rowPos = []
        #the same problem doesn't matter with rows because it has to start at the
        #very left of the screen
        for row in range(8):

            #creates two points at the top left and bottom right of the square
            #with the position of those points being incremented by the for loops
            rectPoint1 = g.Point(squareWidth*row, squareHeight*(column-1))
            rectPoint2 = g.Point(squareWidth*(row+1), squareHeight*column)
            square = Square(g.Rectangle(rectPoint1,rectPoint2),"")
            rowPos.append(square)
            
            if (num % 2 == 0):
                square.rectObject.setFill("grey")
                square.color = "grey"
                num += 1 
            elif (num % 2 != 0):
                square.rectObject.setFill("white")
                square.color = "white"
                num +=1
            
            #i actually can't remember why this was here
            if (row == 7):
                num += 1

               
            square.rectObject.draw(boardWindow)
            
        boardSquares.append(rowPos)
        
    return ChessBoard(boardWindow,boardSquares)

def Clamp(originalNum:int, minNum:int, maxNum:int):
    """
    just used this for preventing selected square indices from going
    out of bounds
    
    """
    if (originalNum >= maxNum):
        return maxNum
    
    if (originalNum <= minNum):
        return minNum
    
    return originalNum


def Main():
    myBoard = SetupBoard(640,640)
    
    pieceInfo = {
            "pawn" : Piece.Pawn("♙♟",[[1,0]]),
            "0,7" : Piece.Rook("♖♜",[[1,0]]),
            "1,6" : Piece.Horse("♘♞",[[2,1]]),
            "2,5" : Piece.Bishop("♗♝",[[1,1]]),
            "4" : Piece.King("♔♚",[[1,1],[1,0]]),
            "3" : Piece.Queen("♕♛",[[1,1],[1,0]])
        }
    
    myBoard.SetPieces(pieceInfo)
    
    #initially updates the board after setting the pieces because it doesn't happen by default
    myBoard.UpdateMoves()

    teams = ["white","black"]
    storedBoardSquares = myBoard.boardSquares
    while True:
#         print(storedBoardSquares != myBoard.boardSquares)
        myBoard.UpdateMoves()
        currentPlayer = teams[0]
        
        selectInput = myBoard.boardWindow.getKey()
        
        currentSquare = myBoard.GetSquare(selectInput)
        currentSquare.rectObject.setFill("blue")
        highlightedPiece = currentSquare.displayObject
        
#         if (isinstance(currentSquare.contents,Piece.Piece)):
#             print(currentSquare.contents.validMoves)
#
#         print(myBoard.rowIndex,myBoard.columnIndex)
        if (selectInput == "Return"):
            contents = currentSquare.contents
            
            #if you have no stored piece, nothing happens
            if (isinstance(contents,Piece.Piece) == False and myBoard.storedPiece == None):
                continue
            
            #checks if the selected piece is the same team as the current player
            #and if you don't have a stored piece
            if (myBoard.storedPiece == None and contents.team == currentPlayer):                
                myBoard.StorePiece(currentSquare,contents)
              
            elif (myBoard.storedPiece != None):
                storedContents = currentSquare.contents
                myBoard.PlacePiece(currentSquare,myBoard.boardWindow)
                

                #alternates turn
                if (currentSquare.contents != storedContents):
                    teams.reverse()
            

Main()