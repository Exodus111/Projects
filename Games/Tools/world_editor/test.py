from path import Path

myfolder = Path("./")

for d in myfolder.dirs():
    for f in d.files():
        print(f.basename())
