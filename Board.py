import data;
import random;
import numpy;

class Board():

   
    def __init__(self):

        self.emptyColor=data.BoardColor;
        self.fallingPiece=None;
        self.nextPiece=random.choice(data.tetrisPieces.keys());
        self.fallingColor=None;
        self.fallingRow=None;
        self.fallingColor=None;
        self.board={};
        self.createBoard();
        self.newFallingPiece();
        self.score = 0;
        self.lines = 0;


    def createBoard(self):
        for row in range(data.ROWS):
            for col in range(data.COLUMNS):
                self.board[row,col]=self.emptyColor;
        for i in range(data.COLUMNS):
            self.board[-1,i]=self.board[-2,i]=self.emptyColor;

    def clearRows(self,canvas):
        score=0;
        board = {};
        for row in range(data.ROWS):
            clearRow = True;
            for col in range(data.COLUMNS):
                if self.board[row,col]==self.emptyColor:
                    clearRow = False;
                    break;
            if clearRow:
                for nrow in range(row,-1,-1):
                    for col1 in range(data.COLUMNS):
                        self.board[nrow,col1]=self.board[nrow-1,col1];
                score+=1;

        self.drawBoard(canvas);
        self.lines += score;
        self.score+= (score**2)*100*(self.lines/10+1)        
      


    def drawCell(self,canvas,row,col,color):
       x0=data.WIDTH*col/data.COLUMNS;
       x1=data.WIDTH*(col+1)/data.COLUMNS;
       y0=data.HEIGHT*row/data.ROWS;
       y1=data.HEIGHT*(row+1)/data.ROWS;
       
       canvas.create_rectangle(x0, y0, x1, y1, fill="black");
       canvas.create_rectangle(x0+1, y0+1, x1-1, y1-1, fill=color);

    def drawBoard(self,canvas):
        for row in range(data.ROWS):
            for col in range(data.COLUMNS):
                self.drawCell(canvas,row,col,self.board[row,col]);

    def getNextPiece(self,canvas):
        self.nextPiece=random.choice(data.tetrisPieces.keys());
        for i in range(2):
            for j in range(4):
                self.drawCell(canvas,data.ROWS/2 + i,data.COLUMNS+2 + j,data.BG);

        row=0;
        for item in data.tetrisPieces[self.nextPiece][0]:
            col=0;
            for cell in item:
                if cell:
                    self.drawCell(canvas,data.ROWS/2 + row, data.COLUMNS+2 + col,data.tetrisPieces[self.nextPiece][1]);                       
                col+=1;
            row+=1;

    
    def newFallingPiece(self):
        self.fallingPiece = data.tetrisPieces[self.nextPiece][0];
        self.fallingColor = data.tetrisPieces[self.nextPiece][1];
        self.fallingRow=0;
        self.fallingCol=data.COLUMNS/2-2;
        return self.legalMove(self.fallingRow,self.fallingCol,self.fallingPiece);

    def drawFallingPiece(self,canvas,c):
        row=0;
        for item in self.fallingPiece:
            col=0;
            for cell in item:
                if cell:
                    if c:
                        self.drawCell(canvas,self.fallingRow + row,self.fallingCol + col,self.fallingColor);
                    else:
                        self.drawCell(canvas,self.fallingRow + row,self.fallingCol + col,self.emptyColor);                       
                col+=1;
            row+=1;

    def moveFallingPiece(self,drow,dcol,canvas):
        if self.legalMove(self.fallingRow+drow,self.fallingCol+dcol,self.fallingPiece):
            self.drawFallingPiece(canvas,False);
            self.fallingCol=self.fallingCol+dcol;
            self.fallingRow=self.fallingRow+drow;
            self.drawFallingPiece(canvas,True);
            return True;
        return False;

    def rotatePiece(self,canvas):
        oldCRow = newCRow = self.fallingRow + len(self.fallingPiece)/2;
        newRow = oldCRow - len(self.fallingPiece[0])/2;
        oldCCol = newCCol = self.fallingCol + len(self.fallingPiece[0])/2;
        newCol = oldCCol - len(self.fallingPiece)/2;

        newPiece = numpy.rot90(numpy.array(self.fallingPiece),1,(0,1)).tolist();
        if self.legalMove(newRow,newCol,newPiece):
            self.drawFallingPiece(canvas,False);
            self.fallingPiece=newPiece;
            self.drawFallingPiece(canvas,True);


    def freezePiece(self):
            row=0;
            for item in self.fallingPiece:
                col=0;
                for cell in item:
                    if cell:
                        self.board[self.fallingRow + row,self.fallingCol +col] = self.fallingColor;               
                    col+=1;
                row+=1;
            return self.newFallingPiece();


    def legalMove(self,drow,dcol,piece):
        row=0;
        for item in piece:
            col=0;
            for cell in item:
                if cell:
                    if (drow+row)>=data.ROWS or (drow+row)<-2 or (dcol+col)>=data.COLUMNS or (dcol+col)<0:
                        return False;
                    if self.board[drow + row, dcol + col]!=self.emptyColor:
                        return False;
                col+=1;
            row+=1;
        return True;

    def redrawAll(self,canvas):
        self.createBoard();
        self.drawBoard(canvas);
        self.getNextPiece(canvas);
        self.newFallingPiece();
        self.getNextPiece(canvas);
        self.drawFallingPiece(canvas,True);
        self.score = 0;
        self.lines = 0;
            



