from tkinter import Toplevel, Text, Listbox
from tkinter.ttk import Frame, Label, Entry, Button
from collections import defaultdict


num = defaultdict(int)
def numerate(pre):
    """ A function for making unique IDs
        'pre' : string
        Returns a string combining the prefix
            with a unique number.
    """
    global num
    num[pre] += 1
    return "{}{}".format(pre, num[pre])

class Sticker(Frame):
    def __init__(self, parent, pos, name):
        Frame.__init__(self, parent)
        self.pack()
        self.parent = parent
        self.pos = pos
        self.name = name
        self.drawing = False
        self.w_id = None
        self.size = (250, 220)
        self.entries = []
        self.text = []
        self.my_lines = {}
        self.links = []
        self.rect_id = None
        self.bindings(self)

    def bindings(self, w):
        w.bind("<B1-Motion>", self.move)
        w.bind("<ButtonPress-3>", self.draw_line)
        w.bind("<ButtonRelease-3>", self.pair_boxes)
        w.bind("<B3-Motion>", self.move_line)


    def pair_boxes(self, e):
        if self.drawing:
            x,y = self.parent.mouse_coords()
            overlap = self.parent.find_overlapping(x-5, y-5, x+5, y+5)
            to_be_removed = True
            if len(overlap) >= 2:
                for sticky in self.parent.stickies:
                    if self.parent.stickies[sticky].w_id == overlap[0] and self.w_id != overlap[0]:
                        self.connect2box(sticky)
                        self.save_connect(sticky)
                        to_be_removed = False
            if to_be_removed:
                self.parent.delete(self.my_line)
            self.drawing = False

    def connect2box(self, other, load=False):
        coords = self.parent.stickies[other].pos
        if load:
            self.my_line = self.parent.create_line(self.pos[0], self.pos[1], coords[0], coords[1], fill="green", width=3)
        else:
            self.parent.coords(self.my_line, self.pos[0], self.pos[1], coords[0], coords[1])
        self.my_lines[self.my_line] = [self.pos[0], self.pos[1], coords[0], coords[1]]
        self.parent.stickies[other].my_lines[self.my_line] = [coords[0], coords[1], self.pos[0], self.pos[1]]

    def save_connect(self, other):
        if other not in self.links:
            self.links.append(other)
        if self.name not in self.parent.stickies[other].links:
            self.parent.stickies[other].links.append(self.name)

    def draw_line(self, e):
        self.drawing = True
        new_x, new_y = self.parent.mouse_coords()
        self.my_line = self.parent.create_line(self.pos[0], self.pos[1], new_x, new_y, fill="green", width=3)


    def move_line(self, e):
        if self.drawing:
            new_x, new_y = self.parent.mouse_coords()
            self.parent.coords(self.my_line, (self.pos[0], self.pos[1], new_x, new_y))

    def move(self, e):
        self.parent.move(self.w_id, e.x, e.y)
        self.parent.move(self.rect_id, e.x, e.y)
        self.pos = tuple([int(co) for co in self.parent.coords(self.w_id)])
        for line in self.my_lines.keys():
            self.parent.coords(line, self.pos[0], self.pos[1], self.my_lines[line][2], self.my_lines[line][3])
            for sticky in self.parent.stickies:
                if sticky != self.name:
                    if line in self.parent.stickies[sticky].my_lines.keys():
                        self.parent.stickies[sticky].my_lines[line][2] = int(self.pos[0])
                        self.parent.stickies[sticky].my_lines[line][3] = int(self.pos[1])



    def add_entry(self, text):
        entry = Entry(self)
        entry.insert(0, ",".join(text))
        entry.pack(fill="both", expand=True)
        entry.config(state="readonly")
        self.bindings(entry)
        self.entries.append(entry)

    def add_text(self, text):
        w, h = self.size
        field = Text2(self, width=w, height=h)
        field.pack()
        field.insert("1.0", text)
        field.config(state="disable")
        self.bindings(field)
        self.text.append(field)

    def add_buttons(self):
        frame = Frame(self)
        frame.pack(fill="x")
        edit = Button(frame, text="Edit", command=self.edit)
        edit.pack(side="right", padx=5, pady=5)
        delete = Button(frame, text="Del", command=self.delete_menu)
        delete.pack(side="right")

    def draw_box(self, color="green", box_id=None):
        x1 = self.pos[0]-(self.size[0]/2)
        y1 = self.pos[1]-(self.size[1]/2)
        x2 = x1 + self.size[0]
        y2 = y1 + self.size[1]
        ad = 27                          #<--Adjustment variable
        bbox = ((x1, y1-ad), (x2, y2+ad))
        if not box_id:
            self.rect_id = self.parent.create_rectangle(bbox, width=7., outline=color)
        else:
            self.parent.coords(box_id, (x1, y1-ad, x2, y2+ad))


    def edit(self):
        entries = [field.get() for field in self.entries]
        text = [text.get("1.0", "end-1c") for text in self.text]
        links = self.links
        node = self.parent.make_node(self.name, self.pos, (entries, text), links)

    def delete_menu(self):
        delmenu = Node(self, self.name, self.pos)
        item_list = ["This box: {}".format(self.name)]
        for lin in self.links:
            item_list.append("The line to: {}".format(lin))
        delmenu.insert_list(item_list)

    def delete_items(self, inx):
        for j in inx:
            if j == 0: #<---Selected the Box.
                self.parent.delete(self.rect_id)
                for link in self.links:
                    self.remove_line(link)
                for stick in self.parent.stickies:
                    if stick != self.name:
                        for link in self.parent.stickies[stick].links:
                            if link == self.name:
                                self.parent.stickies[stick].links.remove(link)
                del self.parent.stickies[self.name]
                self.destroy()
            else: #<---Selected a line.
                self.remove_line(self.links[j-1])
                self.links.remove(self.links[j-1])

    def remove_line(self, node):
        to_be_removed = []
        for stick in self.parent.stickies:
            if self.parent.stickies[stick].name == node:
                for link in self.parent.stickies[stick].links:
                    if link == self.name:
                        self.parent.stickies[stick].links.remove(link)
                for i in self.parent.stickies[stick].my_lines:
                    if i in self.my_lines.keys():
                        to_be_removed.append(i)
                for j in to_be_removed:
                    del self.parent.stickies[stick].my_lines[j]
        for h in to_be_removed:
            self.parent.delete(h)




class Node(Toplevel):
    """ This class is a catchall for all popup windows."""
    def __init__(self, parent, name, pos=(0,0)):
        Toplevel.__init__(self)
        self.parent = parent
        self.name = name
        self.pos = pos
        self.links = []
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
        self.parent.save_info(self.name, self.entries, self.pos, self.links)

    def ok_cancel_buttons(self, call=None):
        if not call:
            call = self.save
        button_frame = Frame(self.frame)
        ok_button = Button(button_frame, text="Ok", command=call)
        cancel_button = Button(button_frame, text="Cancel", command=self.destroy)
        button_frame.pack(fill="x")
        cancel_button.pack(side="right", padx=5, pady=5)
        ok_button.pack(side="right")

    def insert_list(self, items):
        frame = self.frame
        frame.pack(fill="y")
        lb = Listbox(frame, selectmode="multiple")
        for i in items:
            lb.insert("end", i)
        lb.pack()
        self.ok_cancel_buttons(call=lambda : self.del_items(lb.curselection()))

    def del_items(self, selection):
        self.parent.delete_items(selection)
        self.destroy()


    def insert_entry_field(self, txt, default=None, focus=False):
        frame = Frame(self.frame)
        frame.pack(fill="x")
        label = Label(frame, text=txt, width=6)
        label.pack(side="left", anchor="n", padx=5, pady=5)
        entry = Entry(frame)
        entry.pack(fill="x", padx=5, pady=5, expand=True)
        if default:
            for i in default:
                entry.insert("end", i)
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
            for i in default:
                entry.insert("end", i)
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

    def bindtags(self, *args, **kwargs):
        self.text_widget.bind(*args, **kwargs)

    def pack(self, *args, **kwargs):
        Frame.pack(self, *args, **kwargs)
        self.pack_propagate(False)

    def grid(self, *args, **kwargs):
        Frame.grid(self, *args, **kwargs)
        self.grid_propagate(False)
