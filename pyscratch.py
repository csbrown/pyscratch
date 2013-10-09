from Tkinter import *
from PIL import Image, ImageTk
import sys
import pickle
import numpy
import userscript
import threading
import mazes

#This is a class to make a canvas with a background image.  A canvas can't be created outside of the context of a Tk instance,
#so it needs that and the appropriate background image
class SpriteCanvas:

    #Initializes 
    def __init__(self, backgroundfilename, tk):
        self.backgroundfilename = backgroundfilename
        self.background = Image.open(backgroundfilename)
        self.background_image= ImageTk.PhotoImage(self.background)

        self.size = self.background.size 

        self.drawing_area = Canvas(tk, width=self.size[0], height=self.size[1])
        self.drawing_area.create_image(0, 0, image=self.background_image, anchor='nw')

    def getCanvas(self):
        return self.drawing_area

class MazeCanvas:

    def __init__(self, maze, tk):
        self.maze = maze
        self.wallsize = (20,20)
        
        self.size = (self.wallsize[0]*(self.maze.getDimensions()[0]+1), self.wallsize[1]*(self.maze.getDimensions()[1]+1))

        self.drawing_area = Canvas(tk, width = self.size[0], height = self.size[1])
        for i in range(self.maze.getDimensions()[0]):
            for j in range(self.maze.getDimensions()[1]):
                if self.maze.maze[(i,j)]:
                    self.drawing_area.create_rectangle((self.wallsize[0]*i, self.wallsize[1]*j, self.wallsize[0]*(i+1), self.wallsize[1]*(j+1)), fill = 'black')

    def getCanvas(self):
        return self.drawing_area

class PySprite:

    def __init__(self, imagefile, canvas):

        self.imagefile = imagefile
        self.image = ImageTk.PhotoImage(self.imagefile)

        self.canvas = canvas

        self.location = (0,0)
        self.angle = 0

        self.spriteid = self.canvas.create_image((self.location[0],self.location[1]), image = self.image)

        self.maze = None
        self.mazelocation = None

    def getId(self):
        return self.spriteid

    def getCanvas(self):
        return self.canvas

    def move(self,howfar):
        self.getCanvas().move(
                         self.getId(), 
                         int(howfar*numpy.cos(self.angle*numpy.pi/180)), 
                         int(howfar*numpy.sin(self.angle*numpy.pi/180))
        )
        self.location = self.getCanvas().coords(self.getId())

    def moveTo(self, newlocation):
        self.location = self.getCanvas().coords(self.getId(),newlocation)
                  

    def rotate(self,angle):
        self.angle += angle

    def collidesWith(self, othersprite):
        bbox1 = self.canvas.bbox(self.getId())
        bbox2 = self.canvas.bbox(othersprite.getId())
        if bbox1[0] < bbox2[2] or bbox2[0] < bbox1[2] or bbox1[1] < bbox2[3] or bbox2[1] < bbox1[3]:
            return True
        else:
            return False

    def loadMaze(self, maze):
        self.maze = maze
        self.mazelocation = maze.startlocation
        self.goal = maze.finishlocation
        self.moveTo(self.mazeCoordsToCanvasCoords(self.mazelocation))
                
    def traverseMaze(self, direction):
        success = None
        mazeloc = list(self.mazelocation)
        if direction == "right" and not self.maze.maze[self.mazelocation[0] + 1, self.mazelocation[1]]:
            mazeloc[0] += 1
            success = "left"
        if direction == "up" and not self.maze.maze[self.mazelocation[0], self.mazelocation[1] - 1]:
            mazeloc[1] -= 1
            success = "down"
        if direction == "left" and not self.maze.maze[self.mazelocation[0] - 1, self.mazelocation[1]]:
            mazeloc[0] -= 1
            success = "right"
        if direction == "down" and not self.maze.maze[self.mazelocation[0], self.mazelocation[1] + 1]:
            mazeloc[1] += 1
            success = "up"
        if success:
            self.mazelocation = tuple(mazeloc)
            self.moveTo(self.mazeCoordsToCanvasCoords(self.mazelocation))
        return success
            
    def mazeCoordsToCanvasCoords(self, mazecoords):
        mazesize = (self.maze.getDimensions()[0]+1, self.maze.getDimensions()[1]+1)
        canvassize = (int(self.canvas.cget("width")), int(self.canvas.cget("height")))
        blocksize = (canvassize[0] / mazesize[0], canvassize[1] / mazesize[1])
        return (int((mazecoords[0] + 0.5) * blocksize[0]), int((mazecoords[1] + 0.5) * blocksize[1]))

    def checkGoal(self):
        if self.mazelocation == self.goal:
            return True
        return False


class SpriteTool(Tk):

    #background should be local
    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)
        
        #Flags and stuff
        self.scriptloaded = False
        self.userscriptfinished = False

        #TODO Change command to loadscript for ordinary sprite functionality!
        self.loadbutton = Button(self, text="Load Script", command=self.loadmaze, bg = 'purple')
        self.loadbutton.pack()

        self.runbutton = Button(self, text="RUN!", command=self.scriptrunner, bg = 'green')
        self.runbutton.pack()

    ############################################
    #EVENTS
    ###########################################

    #Runs user script
    def scriptrunner(self):
        if self.scriptloaded:

            mainthread = threading.Thread(target=userscript.main)
            mainthread.start()

            while mainthread.isAlive():
                self.canvas.getCanvas().update()
            
        else:
            print "load a script first!"


    def loadscript(self):
        import userscript
        reload(userscript)
        
        self.canvas = SpriteCanvas(userscript.canvas, self)
        self.canvas.getCanvas().pack()

        for sprite in userscript.sprites:
            userscript.sprites[sprite] = PySprite(userscript.sprites[sprite].getImage(), self.canvas.getCanvas())    

        self.scriptloaded = True 

    def loadmaze(self):

        import userscript
        reload(userscript)
        
        self.maze = mazes.easymaze
        self.canvas = MazeCanvas(self.maze, self)
        self.canvas.getCanvas().pack()

        for sprite in userscript.sprites:
            userscript.sprites[sprite] = PySprite(userscript.sprites[sprite].getImage().resize(self.canvas.wallsize, Image.ANTIALIAS), self.canvas.getCanvas())
            userscript.sprites[sprite].loadMaze(self.maze)

        self.scriptloaded = True
            
if __name__ == '__main__':
    tkmain = SpriteTool()
    tkmain.mainloop()

    
    
