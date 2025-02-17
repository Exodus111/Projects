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

@app.route("/template<int:num>")
def temps(num):
    if num == 1:
        return render_template("temp1.html")
    elif num == 2:
        return render_template("temp2.html")
    elif num == 3:
        return render_template("temp3.html")
    else:
        return "Nothing here, sorry."

if __name__ == "__main__":
    app.run()
