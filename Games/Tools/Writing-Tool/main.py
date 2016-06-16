from tkinter import Tk, Canvas, Menu, Toplevel, Text, Scrollbar, Listbox, StringVar
from tkinter.ttk import Frame, Label, Entry, Button, Style, LabelFrame

class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.info = {}
        self.window = None
        self.size = (640, 480)
        #self.parent.geometry("1400x900+150+150")
        self.fields = []
        self.init_ui()

    def init_ui(self):
        self.parent.title("Node Writer")
        self.style = Style()
        self.style.theme_use("alt")
        self.pack(fill="both", expand=True)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        menubar.add_command(label="New", command=self.onNew)
        menubar.add_command(label="Show Info", command=self.get_info)
        menubar.add_command(label="Exit", command=self.quit)

        self.canvas = Canvas(self, background="white", width=self.size[0], height=self.size[1])
        self.canvas.pack(fill="both", expand=1)
        self.canvas.bind("<Button-1>", self.move_boxes)

    def move_boxes(self, event):
        x, y = (event.x-1, event.y-1)
        x1, y1, x2, y2 = self.canvas.bbox("test")
        if x > x1 and y > y1 and x < x2 and y < y2:
            print("Hit")
        else:
            print("Missed")


    def onNew(self):
        new = Node(self, "Node_entry")
        label = new.insert_entry_field("Labels")
        label2 = new.insert_entry_field("Labels2")
        text = new.insert_text_field("Text")
        new.ok_cancel_buttons()

    def get_info(self):
        x, y = (self.size[0]/2, self.size[1]/2)
        for i in self.info:
            label_frame= LabelFrame(self, text="name")
            label_frame.pack(fill="y")
            for entry in self.info[i]["Entry"]:
                frame = Frame(label_frame)
                frame.pack(fill="x")
                label = Label(label_frame, text=self.info[i]["Entry"][entry], width=6)
                label.pack(side="left", anchor="n", padx=5, pady=5)
            for text in self.info[i]["Text"]:
                frame = Frame(label_frame)
                frame.pack(fill="x")
                label = Label(label_frame, text=self.info[i]["Text"][text], width=6)
                label.pack(side="left", anchor="n", padx=5, pady=5)
        window = self.canvas.create_window(x, y, window=label_frame, tag="test")


class Node(Toplevel):
    """ This class is a catchall for all popup windows."""
    def __init__(self, parent, name):
        Toplevel.__init__(self)
        self.parent = parent
        self.name = name
        self.entries = {"Entry":{}, "Text":{}}
        self.resizable(0,0)
        self.frame = Frame(self)
        self.init_ui()
        self.frame.pack(side="right", fill="y", expand=True)

    def init_ui(self):
        pass

    def ok_cancel_buttons(self):
        button_frame = Frame(self.frame)
        ok_button = Button(button_frame, text="Ok", command=self.save)
        cancel_button = Button(button_frame, text="Cancel", command=self.destroy)
        button_frame.pack(fill="x")
        cancel_button.pack(side="right", padx=5, pady=5)
        ok_button.pack(side="right")


    def save(self):
        for i in self.entries["Entry"]:
            self.entries["Entry"][i] = self.entries["Entry"][i].get()
        for i in self.entries["Text"]:
            self.entries["Text"][i] = self.entries["Text"][i].get("1.0", "end-1c")
        self.parent.info[self.name] = self.entries
        self.destroy()

    def insert_entry_field(self, txt):
        frame = Frame(self.frame)
        frame.pack(fill="x")
        label = Label(frame, text=txt, width=6)
        label.pack(side="left", anchor="n", padx=5, pady=5)
        entry = Entry(frame)
        entry.pack(fill="x", padx=5, pady=5, expand=True)
        self.entries["Entry"][txt] = entry

    def insert_text_field(self, txt):
        frame = Frame(self.frame)
        frame.pack(fill="x")
        label = Label(frame, text=txt, width=6)
        label.pack(side="left", anchor="n", padx=5, pady=5)
        entry = Text(frame)
        entry.pack(fill="both", pady=5, padx=5, expand=True)
        self.entries["Text"][txt] = entry

def main():
    root = Tk()
    app = Main(root)
    root.mainloop()

if __name__ == "__main__":
    main()
