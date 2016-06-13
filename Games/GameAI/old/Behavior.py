import random
import time

class Mob(object):
    """The individual Mobile NPC Unit"""
    def __init__(self, courage, name):
        self.courage = courage
        self.name = name
        self.combat = False
        self.choice = "Dont know"
        self.lastchoice = self.choice
        self.target = "His Buddy"
        self.state = {
            "charge":True,
            "attack":True,
            "defend":True,
            "flee":True
        }


    def courage_check(self):
        roll = random.randint(0, 100)
        if roll <= self.courage:
            self.choice = "attack"
            if self.state["charge"]:
                if roll < self.courage/2:
                    self.choice = "charge"
        else:
            self.choice = "defend"
            if self.state["flee"]:
                if roll > self.courage + (100 - self.courage)/2:
                    self.choice = "flee"

    def update(self, group):
        if self.choice != self.lastchoice:
            if self.combat:
                if self.choice == "charge":
                    group.broadcast("{} is charging.".format(self.name))
                elif self.choice == "attack":
                    group.broadcast("{} is attacking.".format(self.name))
                elif self.choice == "defend":
                    group.broadcast("{} is defending.".format(self.name))
                elif self.choice == "flee":
                    group.broadcast("{} is running away.".format(self.name))
                else:
                    group.broadcast("{}{}{}".format(self.name, self.choice, self.target))
            if not self.combat:
                if self.choice == "charge":
                    group.broadcast("{} goes on a patrol.".format(self.name))
                elif self.choice == "attack":
                    group.broadcast("{} is following {}.".format(self.name, self.target))
                elif self.choice == "defend":
                    group.broadcast("{} is guarding the area.".format(self.name))
                elif self.choice == "flee":
                    group.broadcast("{} is just hanging out.".format(self.name))
            self.lastchoice = self.choice

class Strategy(object):
    """A class to house and create our NPC Strategies"""
    def __init__(self):
        pass

    def _locate_leader(self, mobs):
        return random.choice(mobs)


    def initiate_combat(self, mobs):
        for mob in mobs:
            mob.combat = True
            mob.courage_check()

    def idle(self, mobs):
        for mob in mobs:
            if mob.combat == False:
                mob.courage_check()

    def everyone_charge(self, mobs):
        leader = self._locate_leader(mobs)
        leader.courage_check()
        if leader.choice == "charge" or leader.choice == "attack":
            leader.choice = " leads the charge on "
        for mob in mobs:
            mob.target = "the enemy"
            if mob != leader:
                mob.courage_check()
                if mob.choice == "charge" or mob.choice == "attack": 
                    if leader.choice == " leads the charge on ":
                        mob.choice = " joins in the charge on "


    def surround_him(self, mobs):
        leader = self._locate_leader(mobs)
        leader.courage_check()
        if leader.choice == "charge" or leader.choice == "attack":
            leader.choice = " leads the attack on "
        for mob in mobs:
            mob.target = "the enemy"
            if mob != leader:
                mob.courage_check()
                if mob.choice == "charge" or mob.choice == "attack": 
                    if leader.choice == " leads the attack on ":
                        mob.choice = " surrounds "

    def patrol(self, mobs):
            first = True
            patrol_leader = None
            for mob in mobs:
                mob.courage_check()
                if mob.choice == "charge" or mob.choice == "attack" and first:
                    patrol_leader = mob
                    patrol_leader.choice = "charge"
                    first = False
            for mob in mobs:
                if patrol_leader != None:
                    if mob != patrol_leader:
                        if mob.choice == "charge" or mob.choice == "attack":
                            mob.choice = "attack"
                            mob.target = patrol_leader.name

class MobGroup(object):
    """A class to control group behavior"""
    def __init__(self, amount, mobtype):
        self.amount = amount
        self.type = mobtype
        self.event = Events()
        self.strategy = Strategy()
        self.courage = self.courage_roll()
        self.moblist = self.create_mobs()

    def courage_roll(self):
        if self.type == "Goblin":
            return 25
        elif self.type == "Orc":
            return 50
        elif self.type == "Ogre":
            return 75
        elif self.type == "Human":
            return 50

    def create_mobs(self):
        counter = 1
        moblist = []
        for mob in xrange(self.amount):
            mob = Mob(self.courage, "{}{}".format(self.type, counter))
            moblist.append(mob)
            counter += 1
        return moblist

    def broadcast(self, action):
        print action

    def take_action(self, action):
        if action == "combat":
            self.strategy.initiate_combat(self.moblist)
        elif action == "idle":
            self.strategy.idle(self.moblist)
        elif action == "surround enemy":
            self.strategy.surround_him(self.moblist)
        elif action == "everyone charge":
            self.strategy.everyone_charge(self.moblist)
        elif action == "patrol":
            self.strategy.patrol(self.moblist)

    def decide_action(self):
        self.events.update()
        if self.events.current == "":
            pass
        elif self.events.current == "":
            pass
        elif self.events.current == "":
            pass
        elif self.events.current == "":
            pass
        elif self.events.current == "":
            pass



    def update(self):
        for mob in self.moblist:
            mob.update(self)

class Events(object):
    def __init__(self):
        self.current = []
        self.events = {
        "Enemy Spotted":False,
        "Enemy Hurt":False,
        "Enemy Charging":False,
        "Friend Dead":False,
        "Half of Friends Dead":False,
        "Only one left":False,
        "Enemy Overkill":False,
        "Friend Overkill":False
        }

    def update(self):
        self.current = []
        for event in self.events:
            if self.events[event] == True:
                self.current.append(event)
                self.events[event] = False

    def broadcast(self, message):
        if "spots" in message:
            self.events["Enemy Spotted"] = True:
        elif "damages" in message:
            self.events["Enemy Hurt"] = True:
        elif "enemy is charging" in message:
            self.events["Enemy Charging"] = True:
        elif "dies" in message:
            self.events["Friend Dead"] = True:
        elif "only one left" in message:
            self.events["Only one left"] = True
        elif "half of group is dead" in message:
            self.events["Half of Friends Dead"] = True:
        elif "enemy overkill" in message:
            self.events["Enemy Overkill"] = True:
        elif "friend overkill" in message:
            self.events["Friend Overkill"] = True:





if __name__ == "__main__":
    mymobs = MobGroup(8, "Goblin")
    #mymobs.take_action("combat")
    mymobs.take_action("patrol")
    mymobs.update()














