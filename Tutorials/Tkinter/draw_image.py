from Tkinter import Tk, Canvas, Frame, BOTH, NW
import Image, ImageTk

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("High Tatras")
        self.pack(fill=BOTH, expand=1)

        self.img = Image.open("./img/tatras.jpg")
        self.tatras = ImageTk.PhotoImage(self.img)

        canvas = Canvas(self, width=self.img.size[0]+20, height=self.img.size[1]+20)
        canvas.create_image(10, 10, anchor=NW, image=self.tatras)
        canvas.pack(fill=BOTH, expand=1)

def main():
    root = Tk()
    ex = Example(root)
    root.mainloop()

main()
