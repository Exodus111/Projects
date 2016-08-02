from collections import defaultdict
from tkinter import Tk, Canvas, Menu
from tkinter.ttk import Frame, Label, Entry, Button, Style
from load import Node, Sticker

class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.info = defaultdict(dict)
        self.num = defaultdict(int)
        self.window = None
        self.size = (960, 480)
        self.sticky_size = (250, 220)
        self.fields = []
        self.init_ui()

    def init_ui(self):
        self.parent.title("Node Writer")
        self.style = Style(self)              # Doesnt seem to
        self.style.theme_use("alt")           # do anything in Windows.
        self.pack(fill="both", expand=True)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        menubar.add_command(label="New", command=self.onNew)
        menubar.add_command(label="Show Info", command=self.get_info)
        menubar.add_command(label="Exit", command=self.quit)

        self.canvas = Canvas(self, background="white", width=self.size[0], height=self.size[1])
        self.canvas.pack(fill="both", expand=1)
        self.canvas.bind("<Button-1>", self.insert_node)

    def _numerate(self, pre):
        self.num[pre] += 1
        return "{}{}".format(pre, self.num[pre])

    def onNew(self):
        node = Node(self, self._numerate("Name"))
        node.insert_entry_field("Name")
        node.ok_cancel_buttons()

    def save_info(self, title, entries, pos):
        if "Node" in title:
            txtdict = {
            "header":entries["Entry"]["Header"],
            "body":entries["Text"]["Body"],
            "footer":entries["Entry"]["Footer"]
            }
            if pos != (0,0):
                self.make_sticky(txtdict, pos)
        self.info[title] = entries

    def make_sticky(self, txt, pos):
        sticky = Sticker(self, self.sticky_size, txt)
        sticky.id = self.canvas.create_window(pos.x, pos.y, window=sticky)
        tl, br = self.extrapolate_rect(pos, (self.sticky_size[0]-45, self.sticky_size[1]+10))
        sticky.rect_id = self.canvas.create_rectangle(tl, br, fill="black")

    def extrapolate_rect(self, pos, size):
        tl = pos.x - (size[0]/2), pos.y - (size[1]/2)
        br = pos.x + (size[0]/2), pos.y + (size[1]/2)
        return tl, br

    def get_info(self):
        for i in self.info:
            print(i, self.info[i], sep="\t")

    def insert_node(self, pos):
        node = Node(self, self._numerate("Node"), pos)
        node.insert_entry_field("Header")
        node.insert_text_field("Body")
        node.insert_entry_field("Footer")
        node.ok_cancel_buttons()

if __name__ == "__main__":
    root = Tk()
    app = Main(root)
    root.mainloop()
