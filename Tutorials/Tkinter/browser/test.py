from tkinter import Tk, IntVar, StringVar, Text
from tkinter.ttk import Frame, Label, Entry, Radiobutton, Button

def okbutton():
    print(mystring.get())

###### Start Tkinter #####
root = Tk()

###### Init our variables ###
myint = IntVar()
mystring = StringVar()

###### Make our Widgets ####
main_frame = Frame(root)
top_frame = Frame(main_frame)
mid_frame = Frame(main_frame)
bottom_frame = Frame(main_frame)

label = Label(top_frame, text="This is my Label")
entry = Entry(top_frame, textvariable=mystring)
radio = Radiobutton(top_frame, text="Enable", variable=myint, value=1)

text1 = Text(mid_frame)
text2 = Text(mid_frame)

ok_button = Button(bottom_frame, text="Ok", command=okbutton)
cancel_button = Button(bottom_frame, text="Cancel", command=exit)

###### Pack our Widgets #######
main_frame.pack()
top_frame.pack()
mid_frame.pack()
bottom_frame.pack(anchor="e")

label.pack(side="left")
entry.pack(side="left")
radio.pack(side="left")

text1.pack(side="left")
text2.pack(side="left")

cancel_button.pack(side="right", padx=5, pady=5)
ok_button.pack(side="right")


root.mainloop()
