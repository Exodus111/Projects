from collections import defaultdict
from tkinter import Tk, Canvas, Menu
from tkinter.ttk import Frame, Label, Entry, Button, Style
from load import Node, Sticker, Canv, TopMenuBar, numerate

class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.window = None
        self.size = (960, 480)
        self.width = self.size[0]
        self.height = self.size[1]
        self.num = defaultdict(int)
        self.canvasi = []
        self.db = {}
        self.init_ui()

    def init_ui(self):
        self.parent.title("Node Writer")
        self.style = Style(self)              # This doesn't seem to
        self.style.theme_use("alt")           # do anything in Windows.
        self.pack(fill="both", expand=True)

        self.menubar = TopMenuBar(self)
        self.parent.config(menu=self.menubar)

    def save(self):
        pass

    def load(self):
        pass

    def onNew(self):
        node = Node(self, numerate(self.num, "Name"))
        node.insert_entry_field("Name")
        node.ok_cancel_buttons()

    def save_info(self, name_id, entries, _):
        if "Name" in name_id:
            name = "".join(entries["Entry"]["Name"])
            self.db[name] = {}
            self.canvasi.append(Canv(self, name, self.size))
            self.canvas_switch(name)
            self.menubar.add_button("show", name, self.canvas_switch)

    def canvas_switch(self, name):
        for canv in self.canvasi:
            if name == canv.name:
                canv.pack(fill="both", expand=True)
            else:
                canv.pack_forget()


    # Test function, to be removed.
    def get_info(self):
        for can in self.canvasi:
            for node in can.info:
                self.db[can.name][node] = {
                "Header":can.info[node]["Entry"]["Header"],
                "Body":can.info[node]["Text"]["Body"],
                "Footer":can.info[node]["Entry"]["Footer"]
                    }
        print(self.db)

if __name__ == "__main__":
    root = Tk()
    root.state("zoomed")
    app = Main(root)
    root.mainloop()
