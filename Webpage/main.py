import os
from path import Path
from flask import Flask, render_template, request

#This is a hack for Atom, since it doesn't run your file from the files own directory.
here = Path(__file__).abspath().parent
if here != os.getcwd():
    print("Changing dir")
    here.chdir()

app = Flask(__name__)

@app.route("/")
def index():
    print(request)
    text = "Welcome to the Index page."
    return render_template("index.html", text=text)


if __name__ == "__main__":
    app.run()
