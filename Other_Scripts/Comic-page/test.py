#!/usr/bin/python3
import os
from path import Path

#This is a hack for Atom, since it doesn't run your file from the files own directory.
here = Path(__file__).abspath().parent
if here != os.getcwd():
    print("Changing dir")
    here.chdir()

FILELIST = []
STARTFOLDER = "./testfolder"

def find_files(p):
    global FILELIST
    for f in p.files():
        FILELIST.append(f)
    if p.dirs() != []:
        for sub in p.dirs():
            find_files(sub)

if __name__ == "__main__":
    find_files(Path(STARTFOLDER))
    for fi in FILELIST:
        print(fi.abspath())
