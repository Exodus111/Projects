"""
This is an improved version of the tutorial I gave
 on Aug 14th, 2015
 I had made the same mistake with packing to nonetype objects
  making all the frames useless. This fixes that.
"""
from tkinter import *

def ok_func():
    print("ok")

# first we declare our root widget.
root = Tk()

# Then we make our Widgets.
main_frame = Frame(root)
label = Label(main_frame, text="This is our label")

text_frame = Frame(main_frame)
text1 = Text(text_frame)
text2 = Text(text_frame)

button_frame = Frame(main_frame)
ok_button = Button(button_frame, text="Ok", command=ok_func)
cancel_button = Button(button_frame, text="Cancel", command=exit)

# And now we pack.
main_frame.pack()
label.pack()

text_frame.pack(fill="x", padx=10)
text1.pack(side="right")
text2.pack(side="right")

button_frame.pack(side="bottom", anchor="e")
cancel_button.pack(side="right", padx=5, pady=5)
ok_button.pack(side="right")

root.mainloop()
