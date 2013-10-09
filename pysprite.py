from PIL import Image

#Soooo... This is just a dummy class.  The pyscratch module actually takes the imagefilename here and replaces the whole thing with a much more robust class that requires a Tk instance.  The only reason this exists is so that the convention of calling .move, etc. on sprite objects in the userscript sort of makes sense (as opposed to calling it on an image file name string, which absolutely doesn't)
class Sprite:

    def __init__(self, imagefilename):
        self.imagefilename = imagefilename
        self.imagefile = Image.open(imagefilename)

    def getImage(self):
        return self.imagefile
    
    

