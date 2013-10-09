import numpy

class Maze:

    def __init__(self, width, height):
        # Only odd shapes
        shape = ((height // 2) * 2 + 1, (width // 2) * 2 + 1)
        # Build actual maze
        self.maze = numpy.zeros(shape, dtype=bool)
        # Fill borders
        self.maze[0, :] = self.maze[-1, :] = 1
        self.maze[:, 0] = self.maze[:, -1] = 1
        
        # Default start and end
        self.startlocation = (1,1)
        self.finishlocation = (self.maze.shape[0]-2, self.maze.shape[1]-2)

    def getDimensions(self):
        return self.maze.shape

    def setWall(self, location):
        self.maze[location] = 1

    def removeWall(self, location):
        self.maze[location] = 0

    def setStart(self, location):
        self.startlocation = location

    def setFinish(self, location):
        self.finishlocation = location

def easyMaze():
    easymaze = Maze(7,7)
    for i in range(4):
        easymaze.setWall((2,i+1))
        easymaze.setWall((4,5-i))
    return easymaze

easymaze = easyMaze()

