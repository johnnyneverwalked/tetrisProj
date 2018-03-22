import Tkinter;
import data;
from Board import Board;
import winsound;
import math;


def leftKey(event,c):
    b.moveFallingPiece(0,-1,c);

def rightKey(event,c):
    b.moveFallingPiece(0,1,c);

def downKey(event,c):
    b.moveFallingPiece(1,0,c);

def upKey(event,c):
    b.rotatePiece(canvas);

def hardDrop(event,c):
    while b.moveFallingPiece(1,0,c):
        pass;

def fireTimer(c):
    global themeB;
    if not b.moveFallingPiece(1,0,c):
        if not b.freezePiece():
            winsound.PlaySound(None, winsound.SND_PURGE);
            themeB = True;
            c.itemconfig(gameover, text="GAME OVER");
            return;
        b.getNextPiece(c);
        b.clearRows(c);
        if b.lines>=150:
            if themeB:
                winsound.PlaySound("tetrisB.wav", winsound.SND_LOOP + winsound.SND_ASYNC);
                themeB = False;
        c.itemconfig(scoretext,  text="SCORE:\n%s\nLEVEL:\n%s" %(b.score,b.lines/10));
    b.drawFallingPiece(c,True);
    global timer;
    timer = root.after(getDelay(), lambda c=canvas: fireTimer(c));

def restart(event,c):
    if not muted:
        winsound.PlaySound("tetrisA.wav", winsound.SND_LOOP + winsound.SND_ASYNC);
    global timer;
    root.after_cancel(timer);
    b.redrawAll(c);
    c.itemconfig(scoretext, text="SCORE:\n%s\nLEVEL:\n%s" %(b.score,b.lines/10));
    c.itemconfig(gameover, text="");
    timer = root.after(getDelay(), lambda c=canvas: fireTimer(c));

def mute(event):
    global muted;
    if muted:
       if b.lines>=150:
           winsound.PlaySound("tetrisB.wav", winsound.SND_LOOP + winsound.SND_ASYNC);
       else:
           winsound.PlaySound("tetrisA.wav", winsound.SND_LOOP + winsound.SND_ASYNC);
       muted = False;
    else:
        winsound.PlaySound(None, winsound.SND_PURGE);
        muted = True;

def getDelay():
    if b.lines >= 310:
        return 35;
    return int(math.ceil(725 * 0.85**(b.lines/10) +(b.lines/10)));



#---main---

root = Tkinter.Tk();
root.resizable(0,0);
root.title("TETRIS");
winsound.PlaySound("tetrisA.wav", winsound.SND_LOOP + winsound.SND_ASYNC);
muted = False;
themeB = True;
canvas = Tkinter.Canvas(root, bg=data.BG, width=data.WIDTH+180, height=data.HEIGHT);
canvas.pack();

b=Board();
b.drawBoard(canvas);
b.getNextPiece(canvas);
b.drawFallingPiece(canvas,True);

root.bind("<Left>", lambda event, c=canvas: leftKey(event,c));
root.bind("<Right>",lambda event, c=canvas: rightKey(event,c));
root.bind("<Down>",lambda event, c=canvas: downKey(event,c));
root.bind("<Up>",lambda event, c=canvas: upKey(event,c));
root.bind("<r>",lambda event, c=canvas: restart(event,c));
root.bind("<m>",lambda event: mute(event));
root.bind("<space>", lambda event, c=canvas: hardDrop(event,c));
timer = root.after(getDelay(), lambda c=canvas: fireTimer(c));

canvas.create_rectangle(data.WIDTH+1, data.HEIGHT+10, data.WIDTH+10, -10, fill="gray");
canvas.create_text(data.WIDTH+90,9*data.HEIGHT/10,fill="gray",font="Courier 16 bold",
                        text="<r>-RESET\n<m>-MUTE");
canvas.create_text(data.WIDTH+75,4.5*data.HEIGHT/10,fill="gray",font="Courier 16 bold",
                        text="NEXT:");
scoretext = canvas.create_text(data.WIDTH+75,2*data.HEIGHT/10,fill="gray",font="Courier 20 bold",
                         text="SCORE:\n%s\nLEVEL:\n%s" %(b.score,b.lines/10))
gameover = canvas.create_text(data.WIDTH+95,7*data.HEIGHT/10,fill="gray",font="Courier 20 bold",
                         text="")
root.mainloop();
