from itertools import cycle

with open('input.dat', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

class GameBoard():

    def __init__(self, pieceShapeSequence : list) -> None:
        self.pieceShapeSequence = pieceShapeSequence
        self.currentPieceNumber = 0
        self.boardWidth = 7

        self.frozenPieces = []
        self.activePiece = None

        # generate first piece and make active
        self.generateNewPiece()
    

    def generateNewPiece(self):
        
        # create the new piece
        piece = Piece(self, self.pieceShapeSequence[self.currentPieceNumber % len(self.pieceShapeSequence)])

        # place the new piece
        piece.position = ((2, 3 + self.calcMaxHeight()))
        
        # add to piece list and make active
        self.activePiece = piece
        self.currentPieceNumber += 1

    # returns true if the piece is currently colliding 
    def checkCollisions(self, piece):
        
        # check collisions with walls
        pieceXCoordinates = [x for x, _ in piece.getAbsoluteShape()]
        pieceYCoordinates = [y for _, y in piece.getAbsoluteShape()]
        LB, RB = min(pieceXCoordinates), max(pieceXCoordinates)

        if LB < 0 or RB > self.boardWidth - 1:
            return True

        # check collision with floor
        if min(pieceYCoordinates) < 0:
            return True

        # check collisions with other pieces
        for otherPiece in self.frozenPieces:
            if piece.isCollidingWith(otherPiece):
                return True

        return False

    def calcMaxHeight(self):
        if self.frozenPieces == []:
            return 0

        return 1 + max([max([y for _, y in frozenPiece.getAbsoluteShape()]) for frozenPiece in self.frozenPieces])
        
    def freezePiece(self, piece):
        self.frozenPieces.append(piece)
        self.activePiece = None

    def drawBoard(self):
        # get max heights
        maxHeight = self.calcMaxHeight() + 7
        frozenCoordinates = [(x,y) for frozenPiece in self.frozenPieces for x, y in frozenPiece.getAbsoluteShape()]
        activeCorrdinates = [(x,y) for x,y in self.activePiece.getAbsoluteShape()]

        # draw from top to bottom
        for y in reversed(range(0, maxHeight)):
            print("|", end="")
            for x in range(self.boardWidth):

                if (x, y) in frozenCoordinates:
                    print("#", end="")
                elif (x, y) in activeCorrdinates:
                    print("@", end="")
                else:
                    print(" ", end="")
                
            print("|")

        # draw floor
        print("+" + "-"*self.boardWidth + "+", end="\n\n")


class Piece():
    def __init__(self, gameBoard : GameBoard, shape : list) -> None:
        self.shape = shape
        self.gameBoard = gameBoard

        self.position = None

    def moveDown(self):
        # move down by 1
        self.position = (self.position[0], self.position[1] - 1)

        # if this is not a valid move, move back & freeze piece
        if gameBoard.checkCollisions(self):
            self.position = (self.position[0], self.position[1] + 1)
            self.gameBoard.freezePiece(self)
            
            # generate a new piece
            self.gameBoard.generateNewPiece()
        
    def jetMove(self, jet):
        
        prevPos = self.position

        if jet == ">":
            self.position = (self.position[0] + 1, self.position[1])

        else:
            self.position = (self.position[0] - 1, self.position[1])
        
        if gameBoard.checkCollisions(self):
            self.position = prevPos
    
    # returns shape coordinates in absolute coordinates
    def getAbsoluteShape(self):
        return [(self.position[0] + x, self.position[1] + y) for (x,y) in self.shape]

    # check if piece is colliding with another piece
    def isCollidingWith(self, otherPiece):
        # first check if 4x4 square is colliding
        if 5 < ((self.position[0] - otherPiece.position[0]) ** 2 + (self.position[1] - otherPiece.position[1]) ** 2) ** 0.5:
            return False
        
        # now check for every single "pixel" of the pieces

        for pSelf in self.getAbsoluteShape():
            for pOther in otherPiece.getAbsoluteShape():
                if pSelf == pOther:
                    return True
        
        return False


# create piece shapes
p1 = [(0,0), (1,0), (2,0), (3,0)]
p2 = [(1,0), (0,1), (1,1), (2,1), (1,2)]
p3 = [(0,0), (1,0), (2,0), (2,1), (2,2)]
p4 = [(0,0), (0,1), (0,2), (0,3)]
p5 = [(0,0), (1,0), (0,1), (1,1)]

gameBoard = GameBoard([p1, p2, p3, p4, p5])
jets = lines[0]

#-------
# PART1
#-------

# loop over jet sequence infinitely
#for jet in cycle(jets):
#    gameBoard.activePiece.jetMove(jet)
#    gameBoard.activePiece.moveDown()
#
#    if len(gameBoard.frozenPieces) == 10:
#        break
#
#gameBoard.drawBoard()
#print(gameBoard.calcMaxHeight())

#-------
# PART2
#-------

movesPerRockCount = []
moveCount = 0
frozenPieceCount = 0
for jet in cycle(jets):
    gameBoard.activePiece.jetMove(jet)
    gameBoard.activePiece.moveDown()

    if len(gameBoard.frozenPieces) != frozenPieceCount:
        movesPerRockCount.append(moveCount)
        moveCount = 0
    
    frozenPieceCount = len(gameBoard.frozenPieces)

    moveCount += 1
    
    if len(gameBoard.frozenPieces) == 12:
        break

print(movesPerRockCount)
