from collections import defaultdict
from functools import partial
from tkinter import Tk, Toplevel, Text, Message, Canvas, Menu
from tkinter.ttk import Frame, Label, Entry, Button

def numerate(num, pre):
    """ A function for making unique IDs
        `num` : defaultdict(int)
        'pre' : string
        Returns a string combining the prefix
            with a unique number.
    """
    num[pre] += 1
    return "{}{}".format(pre, num[pre])

class Sticker(Frame):
    def __init__(self, parent, pos, tag):
        Frame.__init__(self, parent)
        self.pack()
        self.parent = parent
        self.pos = pos
        self.tag = tag
        self.size = (250, 220)
        self.entries = []
        self.text_fields = []
        self.rect_id = None

    def add_entry(self, text):
        entry = Entry(self)
        entry.insert(0, "".join(text))
        entry.pack(fill="both", expand=True)
        entry.config(state="disable")
        self.entries.append(entry)

    def add_text(self, text):
        w, h = self.size
        field = Text2(self, width=w, height=h)
        field.pack()
        field.insert("1.0", text)
        field.config(state="disable")
        self.text_fields.append(field)

    def draw_box(self, color=None):
        x1 = self.pos[0]-(self.size[0]/2)
        y1 = self.pos[1]-(self.size[1]/2)
        x2 = x1 + self.size[0]
        y2 = y1 + self.size[1]
        bbox = ((x1, y1), (x2, y2))
        self.parent.create_rectangle(bbox)

class Canv(Canvas):
    def __init__(self, parent, name, size):
        Canvas.__init__(self, parent)
        self.parent = parent
        self.name = name
        self.background = "white"
        self.size = size
        self.width = size[0]
        self.height = size[1]
        self.info = defaultdict(dict)
        self.num = defaultdict(int)
        self.sticky_size = (250, 220)
        self.stickies = []
        self.lines = {}
        self.bind("<ButtonPress-1>", self.smark)
        self.bind("<B1-Motion>", self.sdrag)
        self.bind("<Button-3>", self.insert_node)

    def smark(self, pos):
        self.scan_mark(pos.x, pos.y)

    def sdrag(self, pos):
        self.scan_dragto(pos.x, pos.y, 5)

    def insert_node(self, e):
        pos = (e.x, e.y)
        node = Node(self, numerate(self.num, "Node"), pos)
        node.insert_entry_field("tags", focus=True)
        node.insert_text_field("text")
        node.ok_cancel_buttons()

    def save_info(self, name, entries, pos):
        if "Node" in name:
            node = {name:{"tags":entries["Entry"]["tags"],
                        "text":entries["Text"]["text"]}}
            self.parent.db.add_nodes(self.name, node)
            self.insert_sticker(name, node, pos)

    def insert_sticker(self, name, node, pos):
        sticker = Sticker(self, pos, "sticker")
        sticker.add_entry(node[name]["tags"])
        print(node[name]["tags"])
        sticker.add_text(node[name]["text"])
        w_id = self.create_window(pos, window=sticker)
        sticker.draw_box()


class Node(Toplevel):
    """ This class is a catchall for all popup windows."""
    def __init__(self, parent, name, pos=(0,0)):
        Toplevel.__init__(self)
        self.parent = parent
        self.name = name
        self.pos = pos
        self.entries = {"Entry":{}, "Text":{}}
        self.resizable(0,0)
        self.frame = Frame(self)
        self.frame.pack(side="right", fill="y", expand=True)

    def save(self):
        for i in self.entries["Entry"]:
            entry = self.entries["Entry"][i].get()
            entr_list = entry.split(",")
            self.entries["Entry"][i] = entr_list
        for i in self.entries["Text"]:
            self.entries["Text"][i] = self.entries["Text"][i].get("1.0", "end-1c")
        self.destroy()
        self.parent.save_info(self.name, self.entries, self.pos)

    def ok_cancel_buttons(self, call=None):
        if not call:
            call = self.save
        button_frame = Frame(self.frame)
        ok_button = Button(button_frame, text="Ok", command=call)
        cancel_button = Button(button_frame, text="Cancel", command=self.destroy)
        button_frame.pack(fill="x")
        cancel_button.pack(side="right", padx=5, pady=5)
        ok_button.pack(side="right")

    def insert_entry_field(self, txt, default=None, focus=False):
        frame = Frame(self.frame)
        frame.pack(fill="x")
        label = Label(frame, text=txt, width=6)
        label.pack(side="left", anchor="n", padx=5, pady=5)
        entry = Entry(frame)
        entry.pack(fill="x", padx=5, pady=5, expand=True)
        if default:
            entry.insert("end", default)
        if focus:
            entry.focus_force()
        self.entries["Entry"][txt] = entry

    def insert_text_field(self, txt, default=None):
        frame = Frame(self.frame)
        frame.pack(fill="x")
        label = Label(frame, text=txt, width=6)
        label.pack(side="left", anchor="n", padx=5, pady=5)
        entry = Text(frame)
        entry.pack(fill="both", pady=5, padx=5, expand=True)
        if default:
            entry.insert("end", default)
        self.entries["Text"][txt] = entry

class Text2(Frame):
    def __init__(self, master, width=0, height=0, sid=None, **kwargs):
        Frame.__init__(self, master, width=width, height=height)
        self.master = master
        self.width = width
        self.height = height
        self.sid = sid
        self.text_widget = Text(self, **kwargs)
        self.text_widget.pack(expand=True, fill="both")

    def insert(self, *args, **kwargs):
        self.text_widget.insert(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.text_widget.delete(*args, **kwargs)

    def config(self, *args, **kwargs):
        self.text_widget.config(*args, **kwargs)

    def get(self, *args, **kwargs):
        return self.text_widget.get(*args, **kwargs)

    def bind(self, *args, **kwargs):
        self.text_widget.bind(*args, **kwargs)

    def pack(self, *args, **kwargs):
        Frame.pack(self, *args, **kwargs)
        self.pack_propagate(False)

    def grid(self, *args, **kwargs):
        Frame.grid(self, *args, **kwargs)
        self.grid_propagate(False)

class TopMenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)
        self.parent = parent
        self.newmenu = Menu(self)
        self.showmenu = Menu(self)
        self.newmenu.add_command(label="NPC", command=self.parent.onNew)
        self.newmenu.add_separator()
        self.newmenu.add_command(label="Save", command=self.parent.save)
        self.newmenu.add_command(label="Load", command=self.parent.load)
        self.showmenu.add_command(label="Info", command=self.parent.get_info)
        self.newmenu.add_separator()
        self.showmenu.add_separator()
        self.add_cascade(label="New", menu=self.newmenu)
        self.add_cascade(label="Show", menu=self.showmenu)
        self.add_command(label="Exit", command=self.parent.quit)

    def add_button(self, menu, name, call):
        func = partial(call, name)
        if menu == "new":
            self.newmenu.add_command(label=name, command=func)
        elif menu == "show":
            self.showmenu.add_command(label=name, command=func)


if __name__ == "__main__":
    pass    #<--- For testing!
