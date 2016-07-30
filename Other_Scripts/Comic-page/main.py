from flask import Flask, render_template, url_for, redirect
from path import Path
from comics import Series
import os

#This is a hack for Atom, since it doesn't run your file from the files own directory.
here = Path(__file__).abspath().parent
if here != os.getcwd():
    print("Changing dir")
    here.chdir()

app = Flask(__name__)

@app.route("/")
def index(redir=False):
    global series
    if not redir:
        if series.layer != 0:
            series.set_thumbs(0)
    return render_template("index.html", thumbs=series.thumbs)

@app.route("/comic<int:cid>")
def set_page(cid):
    global series
    series.set_active(cid)
    if series.subfolder:
        series.set_thumbs(series.active_comic.folder_id)
        return redirect(url_for("index", redir=True))
    else:
        return redirect(url_for("get_page", num=0))

@app.route("/page<int:num>")
def get_page(num=0):
    global series
    image = series.active_comic.get_image(num)
    return render_template("pages.html", image=image, num=num)


if __name__ == "__main__":
    series = Series("./static/comics")
    app.run(debug=True)
