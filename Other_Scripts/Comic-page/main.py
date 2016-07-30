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
        thumbs = series.toplayer_thumbs
    else:
        thumbs = series.subfolder_thumbs[series.act_fold_id]
    return render_template("index.html", thumbs=thumbs)

@app.route("/comic<int:cid>")
def set_page(cid):
    global series
    series.set_active(cid)
    if series.act_fold_id == 0:
        return redirect(url_for("get_page", num=0))
    else:
        return redirect(url_for("index", redir=True))

@app.route("/page<int:num>")
def get_page(num=0):
    global series
    image = series.active_comic.get_image(num)
    return render_template("pages.html", image=image, num=num)


if __name__ == "__main__":
    series = Series("./static/comics")
    app.run(debug=True)
