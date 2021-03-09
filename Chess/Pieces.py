class Piece():
    """
    default piece class that all pieces inherit from
    creates default UpdateValidMoves function so i can easily update all pieces moves at once
    """
    def __init__(self,pieceName:str,moveLimit:list):
        self.pieceName = pieceName
        self.moveLimit = moveLimit.copy()
        self.hasMoved = False
        self.topOrBot = ""
        self.validMoves = []
        self.pos = []
        self.canPawn = False
        
        #CHANGE THIS LATER
        self.team = ""
        
    def UpdateValidMoves(self,currentPos:list,board:list) -> None:
        pass
    
    def DunnoWhatToNameThis(self):
        if (self.topOrBot == 'bot'):
            self.moveLimit = [[-num for num in self.moveLimit[0]],[-num for num in self.moveLimit[1]]]
            
class King(Piece):
    def __init__(self,pieceName:str,moveLimit:list):
        super().__init__(pieceName,moveLimit)
        self.canCastle = False
    
    def Castle(self,board,castleY,castleX,rook):
        storedPiece = rook
        board.boardSquares[rook.pos[0]][rook.pos[1]].displayObject.undraw()
        board.boardSquares[rook.pos[0]][rook.pos[1]].UpdateContents("")
        board.boardSquares[rook.pos[0]][rook.pos[1]].DrawContents(board.boardWindow)   
        
        rook.pos = [castleY,castleX]
        board.boardSquares[castleY][castleX].UpdateContents(rook)
        board.boardSquares[castleY][castleX].DrawContents(board.boardWindow)
        
        self.canCastle = False
        
    def UpdateValidMoves(self,currentPos:list,board:list) -> None:
        self.validMoves = []
        currentY = currentPos[0]
        currentX = currentPos[1]
        finalList = []
        #check if castling is possible
        if (self.hasMoved == False):
            #check right rook
            for i in range(1,4):
                index = [self.pos[0],self.pos[1]+i]
                square = board[index[0]][index[1]]
                if (square.contents != "" and isinstance(square.contents,Rook) == False):
                    self.canCastle = False
                    break
                if (isinstance(square.contents,Rook) and i == 3 and square.contents.hasMoved == False):
                    self.canCastle = True
                    self.validMoves.append([index[0],index[1]-1,[self.Castle,index[0],index[1]-2,square.contents]])
#                     print("right rook")
                    break
                
            #check left rook
            for i in range(1,5):
                index = [self.pos[0],self.pos[1]-i]
                square = board[index[0]][index[1]]
                if (square.contents != "" and isinstance(square.contents,Rook) == False):
                    self.canCastle = False
                    break
                if (isinstance(square.contents,Rook) and i == 4 and square.contents.hasMoved == False):
                    self.canCastle = True
                    self.validMoves.append([index[0],index[1]+2,[self.Castle,index[0],index[1]+3,square.contents]])
#                     print("left rook")
                    break
            
        else:
            self.canCastle = False
        
        #get normal moves
        for limit in self.moveLimit:
            for x in range(2):
                upRight = []
                downLeft = []
                upLeft = []
                downRight = []          
                
                yAhead = limit[0]
                xAhead = limit[1]
                
                indexUpRight = [currentY+yAhead,currentX+xAhead]
                indexDownLeft = [currentY-yAhead,currentX-xAhead]
                indexUpLeft = [currentY+yAhead,currentX-xAhead]
                indexDownRight = [currentY-yAhead,currentX+xAhead]
                    
                upRight.append(indexUpRight)
                downLeft.append(indexDownLeft)
                upLeft.append(indexUpLeft)
                downRight.append(indexDownRight)
                    
                directionList = [upRight,downLeft,upLeft,downRight]
                finalList = []
                for direction in directionList:
                    for index in direction:
                        if (index[0] < 0 or index[0] > 7):
                            break
                        if (index[1] < 0 or index[1] > 7):
                            break
                        square = board[index[0]][index[1]]
                        if (isinstance(square.contents,Piece) and square.contents.team != self.team):
                            finalList.append(index)
                            break
                        if (isinstance(square.contents,Piece) and square.contents.team == self.team):
                            break
                        
                        finalList.append(index)
                
                for move in finalList:
                    self.validMoves.append(move)
                    
                limit.reverse()

class Queen(Piece):
    def __init__(self,pieceName:str,moveLimit:list):
        super().__init__(pieceName,moveLimit)
     
    def UpdateValidMoves(self,currentPos:list,board:list) -> None:
        self.validMoves = []
        currentY = currentPos[0]
        currentX = currentPos[1]
        finalList = []
        for limit in self.moveLimit:
            for x in range(2):
                upRight = []
                downLeft = []
                upLeft = []
                downRight = []          
                for i in range(1,8):
                    yAhead = limit[0] * i
                    xAhead = limit[1] * i
                    
                    indexUpRight = [currentY+yAhead,currentX+xAhead]
                    indexDownLeft = [currentY-yAhead,currentX-xAhead]
                    indexUpLeft = [currentY+yAhead,currentX-xAhead]
                    indexDownRight = [currentY-yAhead,currentX+xAhead]
                        
                    upRight.append(indexUpRight)
                    downLeft.append(indexDownLeft)
                    upLeft.append(indexUpLeft)
                    downRight.append(indexDownRight)
                    
                directionList = [upRight,downLeft,upLeft,downRight]
                finalList = []
                for direction in directionList:
                    for index in direction:
                        if (index[0] < 0 or index[0] > 7):
                            break
                        if (index[1] < 0 or index[1] > 7):
                            break
                        square = board[index[0]][index[1]]
                        if (isinstance(square.contents,Piece) and square.contents.team != self.team):
                            finalList.append(index)
                            break
                        if (isinstance(square.contents,Piece) and square.contents.team == self.team):
                            break
                        
                        finalList.append(index)
                
                for move in finalList:
                    self.validMoves.append(move)
                    
                limit.reverse()


class Pawn(Piece):
    def __init__(self,pieceName:str,moveLimit:list):
        super().__init__(pieceName,moveLimit)
        self.canPawn = True
        self.firstUpdate = True
        self.attackAxis = [[self.moveLimit[0][0],1]]
        self.moveLimit.append([2*self.moveLimit[0][0],0])
    
    def Promote():
        pass
    
    def UpdateValidMoves(self,currentPos:list,board:list) -> None:
        y = currentPos[0]
        x = currentPos[1]
        self.validMoves = []
        
        for limit in self.moveLimit:
            yAhead = currentPos[0]+limit[0]
            xAhead = currentPos[1]+limit[1]
            
            #Check left diagonal for attack
            try:
                if (self.pos[1] >= 0 and self.pos[1] <= 7):
                    y = self.moveLimit[0][0]+currentPos[0]
                    x = -self.moveLimit[0][0]+currentPos[1]
                    square = board[y][x]
                    if (isinstance(square.contents,Piece) and square.contents.team != self.team):
                        self.validMoves.append([y,x])
            except:
                pass
            
            #Check right diagonal for attack
            try:
                if (self.pos[1] >= 0 and self.pos[1] <= 7):
                    y = self.moveLimit[0][0]+currentPos[0]
                    x = self.moveLimit[0][0]+currentPos[1]
                    square = board[y][x]
                    
                    if (isinstance(square.contents,Piece) and square.contents.team != self.team):
                        self.validMoves.append([y,x])
            except:
                pass
            
            if (isinstance(board[yAhead][xAhead].contents,Piece)):
                continue
                        
            move = [yAhead,xAhead]
            self.validMoves.append(move)
            

class Horse(Piece):
    def __init__(self,pieceName:str,moveLimit:list):
        super().__init__(pieceName,moveLimit)
    
    def UpdateValidMoves(self,currentPos:list,board:list) -> None:
        currentY = currentPos[0]
        currentX = currentPos[1]
        self.validMoves = []
#         print(currentPos)
#         for limit in self.moveLimit:
        limit = self.moveLimit[0]
        for i in range(2):
            index1 = [currentY + limit[0],currentX + limit[1]]
            index2 = [currentY - limit[0],currentX - limit[1]]
            index3 = [currentY + limit[0],currentX - limit[1]]
            index4 = [currentY - limit[0],currentX + limit[1]]
            
            indexList = [index1,index2,index3,index4]
            
            finalList = []
            someNum = 0
            remove = False
            for index in indexList:
                for num in index:
                    if num < 0 or num > 7:
                        remove = True
                        break
                
                if (remove == True):
                    remove = False
                    continue
                
                finalList.append(index)

            for index in finalList:
                square = board[index[0]][index[1]]
                if (isinstance(square.contents,Piece) and square.contents.team == self.team):
                    continue

                self.validMoves.append(index)
                
            limit.reverse()          

class Bishop(Piece):
    def __init__(self,pieceName:str,moveLimit:list):
        super().__init__(pieceName,moveLimit)
    
    def UpdateValidMoves(self,currentPos:list,board:list) -> None:
        currentY = currentPos[0]
        currentX = currentPos[1]
        self.validMoves = []
        for limit in self.moveLimit:
            upRight = []
            downLeft = []
            upLeft = []
            downRight = []
            for i in range(1,8):
                yAhead = limit[0] * i
                xAhead = limit[1] * i
                
                indexUpRight = [currentY+yAhead,currentX+xAhead]
                indexDownLeft = [currentY-yAhead,currentX-xAhead]
                indexUpLeft = [currentY+yAhead,currentX-xAhead]
                indexDownRight = [currentY-yAhead,currentX+xAhead]
                    
                upRight.append(indexUpRight)
                downLeft.append(indexDownLeft)
                upLeft.append(indexUpLeft)
                downRight.append(indexDownRight)
            
            directionList = [upRight,downLeft,upLeft,downRight]
            finalList = []
            for direction in directionList:
                for index in direction:
                    if (index[0] < 0 or index[0] > 7):
                        break
                    if (index[1] < 0 or index[1] > 7):
                        break
                    square = board[index[0]][index[1]]
                    if (isinstance(square.contents,Piece) and square.contents.team != self.team):
                        finalList.append(index)
                        break
                    if (isinstance(square.contents,Piece) and square.contents.team == self.team):
                        break
                    
                    finalList.append(index)
            
            for move in finalList:
                self.validMoves.append(move)
                

class Rook(Piece):
    def __init__(self,pieceName:str,moveLimit:list):
        super().__init__(pieceName,moveLimit)
    
    def UpdateValidMoves(self,currentPos:list,board:list) -> None:
        self.validMoves = []
        currentY = currentPos[0]
        currentX = currentPos[1]
        finalList = []
        for limit in self.moveLimit:
            for x in range(2):
                upRight = []
                downLeft = []
                upLeft = []
                downRight = []          
                for i in range(1,8):
                    yAhead = limit[0] * i
                    xAhead = limit[1] * i
                    
                    indexUpRight = [currentY+yAhead,currentX+xAhead]
                    indexDownLeft = [currentY-yAhead,currentX-xAhead]
                    indexUpLeft = [currentY+yAhead,currentX-xAhead]
                    indexDownRight = [currentY-yAhead,currentX+xAhead]
                        
                    upRight.append(indexUpRight)
                    downLeft.append(indexDownLeft)
                    upLeft.append(indexUpLeft)
                    downRight.append(indexDownRight)
                    
                directionList = [upRight,downLeft,upLeft,downRight]
                finalList = []
                for direction in directionList:
                    for index in direction:
                        if (index[0] < 0 or index[0] > 7):
                            break
                        if (index[1] < 0 or index[1] > 7):
                            break
                        square = board[index[0]][index[1]]
                        if (isinstance(square.contents,Piece) and square.contents.team != self.team):
                            finalList.append(index)
                            break
                        if (isinstance(square.contents,Piece) and square.contents.team == self.team):
                            break
                        
                        finalList.append(index)
                
                for move in finalList:
                    self.validMoves.append(move)
                    
                limit.reverse()

