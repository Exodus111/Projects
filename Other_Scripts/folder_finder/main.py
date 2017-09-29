from path import Path

def walk_folders(start, search):
    folder = Path(start)
    for f in folder.dirs("*{}*".format(search)):
        return f.abspath()
    for di in folder.dirs():
        print(di.abspath())
        walk_folders(di, search)

print(walk_folders("/home", "kivy"))
