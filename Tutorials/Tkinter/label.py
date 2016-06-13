from PIL import Image, ImageTk
from Tkinter import Tk, Frame, Label

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("Title")
        self.img = Image.open("./img/tatras.jpg")
        tatras = ImageTk.PhotoImage(self.img)
        label = Label(self, image=tatras)

        # Reference must be stored
        label.image = tatras

        label.pack()
        self.pack()

    def setGeometry(self):
        w, h = self.img.size
        self.parent.geometry("{}x{}+300+300".format(w,h))

def main():
    root = Tk()
    ex = Example(root)
    ex.setGeometry()
    root.mainloop()

if __name__ == "__main__":
    main()
