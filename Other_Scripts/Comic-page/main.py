#!/usr/bin/python3
# WebComic App by Exodus111
# www.github.com/exodus111
# Use freely, but credit me.

from flask import Flask, render_template, url_for, redirect
from path import Path
from comics import FolderManager
import os

#This is a hack for Atom, since it doesn't run your file from the files own directory.
here = Path(__file__).abspath().parent
if here != os.getcwd():
    print("Changing dir")
    here.chdir()

app = Flask(__name__)

@app.route("/")
def index():
    """
    Our entry point, and Home destination.
    Thumbs is a dictionary where the keys are url routes and the values image src.
    Series is an object that handles all the Comic Objects.
    """
    global fm
    return render_template("index.html", issues=fm.folderdict)

@app.route("/folder<int:fid>")
def pick_folder(fid):
    """
    The user has selected a subfolder.
    `fid` : (int) The Folder ID number.
    We call our method to get the correct thumbnail dictionary.
    """
    global fm
    thumbs = fm.pick_folder(fid)
    return render_template("issues.html", thumbs=fm.series.coverdict)

@app.route("/issue<int:cid>")
def set_page(cid):
    """
    The user has requested an issue, and we call the method to select his issue.
    `cid` : (int) The Comic ID number.
    We redirect to the `get_page` function.
    """
    global fm
    fm.series.set_current("issue" + str(cid))
    return redirect(url_for("get_page", num=0))


@app.route("/page<int:num>")
def get_page(num=0):
    """
    A simple page turner. Num is the page we are on, it enumerates from 0.
    """
    global fm
    image = fm.series.get_image(num)
    return render_template("pages.html", image=image, num=num)


if __name__ == "__main__":
    fm = FolderManager("/home/aurelio/Pictures/comics", "./static/extracted")
    app.run(host='0.0.0.0')
