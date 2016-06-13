#
# This is a simple template file to run any command on every file
# in a directory. Simply fill out the rest.
#

from path import Path
import subprocess

root = Path(".")
for f in root.files("*.MOV"):
    subprocess.Popen("") # <---Command goes here.
