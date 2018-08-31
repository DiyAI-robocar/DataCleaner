import sys
import os
import json
from tkinter import *
from PIL import ImageTk, Image


class DataCleaner:
    def __init__(self, path = "."):
        self.path = path
        self.window = Tk()
        self.panel = Label(self.window)
        self.angle = Label(self.window)
        self.imagelist = list(filter( lambda x: x.find(".jpg")!=-1, os.listdir(path)))
        self.imageiter = iter(self.imagelist)
        self.nextImage()
        self.panel.pack()
        self.angle.pack()
        self.window.bind("<Key>", self.key)
        self.window.mainloop()
        
    def nextImage(self):
        self.loadImage(next(self.imageiter))
        self.updateAngle()
        
    def loadImage(self, imagePath):
        self.imagename = imagePath
        self.image = ImageTk.PhotoImage(Image.open(imagePath))
        self.panel.config (image = self.image)

    def updateAngle(self):
        jsonfile = "record_" + self.imagename[:self.imagename.find("_")] + ".json"
        with open(jsonfile) as json_data:
            d = json.load(json_data)
            self.angle.config(text = d["user/angle"])
            print(d)
    
    
    def key(self, event):
        print("pressed", repr(event.char))
        c = event.char
        if c is " ":
            print("Keep")
            self.keep()
        elif c is "n" or c is "m" or c is "b":
            changeDirection(0.0)
        else:
            try:
                direction = int(c)
                if direction == 0:
                    direction = 10
                if direction <= 5:
                    direction = -1.2 + direction * 0.2
                else:
                    direction = (direction-5) * 0.2
                print("New direction",direction)
                self.changeDirection(direction)
            except ValueError:
                print("Delete")
                self.delete()
        self.nextImage()

    def keep(self):
        f = open("keep.txt", "a+")
        f.write(self.imagename+"\n")
        f.close()
        
    def delete(self):
        f = open("delete.txt", "a+")
        f.write(self.imagename+"\n")
        f.close()
        
    def changeDirection(self, direction):
        f = open("change.txt", "a+")
        f.write(self.imagename + " " + str(direction) + "\n")
        f.close()
                    
                    
                
            
            

def main(argv):
    if len(argv)>0:
        gui = DataCleaner(argv[0])
    else:
        gui = DataCleaner()
    
if __name__ == "__main__":
   main(sys.argv[1:])
        