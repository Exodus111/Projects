import random
from groupthink import *

class Player(object):
    name = "Human"
    hp = 100

class TestGame(object):
    def __init__(self):
        self.player = Player()
        self.enemy = random.choice(["Goblin", "Orc", "Ogre"])
        self.amount = random.randint(2, 10)
        self.game = True
        self.mymobs = GroupThink(self.amount, self.enemy)

    def interface(self, message, *opts):
        print "\n"
        print message
        print "\n"
        print self.enemy_state
        print "What do you do?"
        print "1: {}".format(opts[0])
        print "2: {}".format(opts[1])
        print "3: {}".format(opts[2])
        return raw_input()

    def status(self):
        attacking = 0
        defending = 0
        running = 0
        status = "There are {} {}'s before you. They have not spotted you.".format(self.amount, self.enemy)
        if not self.mymobs.log.empty:
            mylog = self.mymobs.log.log
            for l in mylog:
                if "stands his ground" in mylog[l]["msg"]:
                    defending += 1
                elif "attacks" in mylog[l]["msg"]:
                    attacking += 1
                elif "runs" in mylog[l]["msg"]:
                    running += 1
            _s = self._status_format(attacking, running, defending)
            status = "{}{}{}".format(_s[0], _s[1], _s[2])
        return status

    def _status_format(self, attacking, running, defending):
        string1 = string2 = string3 = ""
        if attacking:
            string1 = "{} {}'s are attacking you".format(attacking, self.enemy)
        else:
            string1 = "None of the {}'s' attack you".format(self.enemy)
        if running:
            string2 = ", {} are running away".format(running)
        if defending:
            string3 = ", and {} are standing their ground.".format(defending)
        return [string1, string2, string3]


    def solve(self, scene, answer):
        if scene == 1:
            self.mymobs.group_events["Enemy_spotted"][0] = True
            self.mymobs.group_events["Enemy_spotted"][2] = [self.mymobs.mobs[0], self.player]
        if scene > 1:
            self.mymobs.group_events["Surround_enemy"][0] = True
            self.mymobs.group_events["Surround_enemy"][2] = [self.mymobs.mobs[0], self.player]
        if scene > 2:
            self.game = False

    def combat(self):
        pass

    def run(self):
        message = "Welcome Adventurer"
        options = ["Attack", "Hide", "Taunt them"]
        scene = 0
        while self.game:
            scene += 1
            self.enemy_state = self.status()
            answer = self.interface(message, *options)
            self.solve(scene, answer)
            self.mymobs.update()
            message = "Now what?"
            options = ["Keep Fighting", "Run Away", "Try to negotiate"]
        self.mymobs.log.output()

game = TestGame()
game.run()




