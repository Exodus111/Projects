
player = "rock"

AI = "paper"

win = ["rockscissor", "scissorpaper", "paperrock"]

if player + AI in win:
    print("You win!")
elif player == AI:
    print("Draw!")
else:
    print("You lose!")
