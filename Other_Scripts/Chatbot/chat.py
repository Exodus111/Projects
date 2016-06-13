from rivescript import RiveScript

def error_check(reply):
    if "[ERR:" in reply:
        return "I'm sorry, something went wrong."
    else:
        return reply

bot = RiveScript()
bot.load_directory("./Ania")
bot.sort_replies()

user = "localuser"

while True:
    msg = input('You> ')
    if msg == '/quit':
        quit()
    reply = bot.reply(user, msg)
    reply = error_check(reply)
    print("{}{}{}{}".format("\033[96m", "Ania> ", reply, "\033[0m"))


