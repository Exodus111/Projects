#!/usr/bin/python3
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory as ASFH
from prompt_toolkit.contrib.completers import WordCompleter

collection = WordCompleter(["Test", "abc", "party", "Google", "hey", "Trump"], ignore_case=True)

while True:
    inp = prompt(">> ", history=FileHistory("history.txt"), auto_suggest=ASFH(),
                completer=collection)
    if inp in ("q", "x", "exit"): break
    print(inp)
