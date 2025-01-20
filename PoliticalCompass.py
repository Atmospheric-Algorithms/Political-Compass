#PoliticalCompass: Finds center of balance of political beliefs.
#Original Compass by freedom-lover727, see post https://www.reddit.com/r/PoliticalCompass/comments/pg3vr8/made_my_own_political_compass_bingo/

#Modules to import: tkinter for GUI, PIL (Pillow) for image handling, sys for directory maneuvering
import tkinter
import PIL.Image, PIL.ImageTk
import sys
import os

wd=sys.path[0] #working directory

textspiel1="Political Compass: Finds center of balance of political beliefs. Code by Atmospheric Algorithms.\nOriginal Compass by freedom-lover727, see post https://www.reddit.com/r/PoliticalCompass/comments/pg3vr8/made_my_own_political_compass_bingo/\n"

textspiel2="Instructions: click boxes that you believe in to mark.\n Red '(X)' represents your political center of mass."

print(textspiel1,"\n", textspiel2)

squarepix=40 #Number of pixels alloted per box in compass
xoffset=20 #X Offset for Xs
yoffset=20 #Y offset for Xs

xfont=("Arial",30) #Default font for Xs

def main():
    root = tkinter.Tk() #Tkinter instance window
    root.title("The Political Compass, But it's an Interactive GUI")

    #Main Frame: Encompasses whole screen
    mainframe=tkinter.Frame(root, width=1000, height=1200, bg="black", bd=0)
    mainframe.pack()

    #Textlabel: Main title
    textlabel=tkinter.Label(mainframe, width=150, height=5, bg="gray70", anchor="n", text=textspiel1 + textspiel2, bd=0)
    textlabel.place(x=0, y=0)

    #Original Political Compass image
    image = PIL.Image.open("PolComp.png") #see function resource_path
    #Bigger image for zoom window
    biggerimage=image.resize((squarepix*17*2, squarepix*17*2))
    biggerimg=PIL.ImageTk.PhotoImage(biggerimage)

    #Smaller Image for main window
    smallimage=image.resize((squarepix*17,squarepix*17))
    smallimg = PIL.ImageTk.PhotoImage(smallimage)


    #Main Political Compass image
    imagecanvas=tkinter.Canvas(mainframe, bd=0, width=17*squarepix, height=17*squarepix)
    imagecanvas.place(x=40, y=90)
    imagecanvas.create_image(0, 0, image=smallimg, anchor="nw")

    #Zoomed image displayer
    zoomcanvas=tkinter.Canvas(mainframe, width=4*squarepix, height=4*squarepix, bg="purple")
    imagelabel=tkinter.Label(zoomcanvas, image=biggerimg)
    imagelabel.place(x=-500, y=-500)
    zoomcanvas.place(x=780,y=360)

    #Creates an array of text
    squarelabels=[] #2D array, holds the square labels
    squaredata=[] #2D array, holds the square label data
    for a in range(17): #iterates through x coordinates
        for b in range(17): #iterates through y coordinates
            #initiates a new column for the 2D lists
            if b==0: 
                squaredata.append([pcsquare(a,b,0)])
                squarelabels.append([imagecanvas.create_text(a*squarepix+xoffset, b*squarepix+yoffset, text=" ", font=xfont)])
            #continues filling out a column for the 2D lists
            else: 
                squaredata[a].append(pcsquare(a,b,0))
                squarelabels[a].append(imagecanvas.create_text(a*squarepix+xoffset, b*squarepix+yoffset, text=" ", font=xfont))

    #Also create marker for centerofbalance
    centerofbalance=imagecanvas.create_text(8*squarepix+xoffset, 8*squarepix+yoffset, text="(+)", fill="red", font=xfont)

    #Mouse-over and clicking events on chart
    imagecanvas.bind('<Motion>', lambda event, imagelabel=imagelabel: motion(event, imagelabel))
    imagecanvas.bind('<Button-1>', lambda event, squaredata=squaredata, squarelabels=squarelabels, imagecanvas=imagecanvas, centerofbalance=centerofbalance: click(event, squaredata, squarelabels, imagecanvas, centerofbalance))

    root.mainloop() #GUI mainloop
    #End of main

class pcsquare: #the data for the on/off pc squares all along the compass. 
    def __init__(self,x,y,status): #initiates a pcsquare
        self.x=x #x: how many squares across, 0-16
        self.y=y #y: how many squares down, 0-16
        self.status=status #0 for off, 1 for on
    def toggle(self): #toggles a pcsquare
        if self.status==0: self.status=1
        else: self.status=0

def motion(event, imagelabel): #movement on the canvas updates the zoom object
    x, y = event.x, event.y
    imagelabel.place_configure(x=-2*x+2*squarepix, y=-2*y+2*squarepix)

def click(event, squaredata, squarelabels, imagecanvas, centerofbalance): #click on canvas selects option
#toggles box and updates center of balance

    x, y=event.x, event.y
    a=int(x/squarepix) #converts pixels into political squares
    b=int(y/squarepix)

    #Toggle box to check/uncheck
    squaredata[a][b].toggle()
    if squaredata[a][b].status==1:
        imagecanvas.itemconfig(squarelabels[a][b],text="X")
    else:
        imagecanvas.itemconfig(squarelabels[a][b],text=" ")

    #Finds and updates Center of Balance
    xtally=0 #xtally: totals x coordinates of all checked boxes
    ytally=0 #ytally: totals y coordinates of all checked boxes
    tally=0 #tally: tallies all checked boxes

    for a  in range(len(squaredata)): #iterates through xs
        for b in range(len(squaredata)): #iterates through ys
            if squaredata[a][b].status==1:
                xtally += a
                ytally += b
                tally += 1
    if tally==0:
        cobx=8
        coby=8
    else:
        cobx=xtally/tally #final x center of balance
        coby=ytally/tally #final y center of balance
    
    #Moves center of balance marker
    print("New Center of Balance: ",cobx-8,",",8-coby)
    imagecanvas.moveto(centerofbalance, squarepix*cobx-5, squarepix*coby-2)


    
main()
