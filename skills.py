import random

class CombatSkills():
    def __init__(self):
        self.chant_flag = False
        self.aim_flag = False
        self.eradicate_flag = False
        self.distance = random.randint(2,5)
        self.damage_modifiers = [0,0]
        
    
    def charge(self):
        if self.distance <= 2:
            self.distance = 1
            return "You lunge forward, tackling and knocking back the enemy in the process", random.randint(1,3)
        else:
            self.distance -= 2
            return "You lunge forward", 0

    def swing(self):
        if self.distance <= 2:
            return "You swing your sword with the intent of cleaving your opponent in half", random.randint(4,7)
        else:
            return "You swing, however you are too far away and miss", 0

    def block(self):
        self.damage_modifiers[1] = random.randint(-20,-10)
        return "You take a defensive stance and ready your shield to block", 0
    
    def aim(self):
        self.aim_flag = True
        return "You take aim, focusing on lining up your shot", 0
    
    def shoot(self):
        if self.aim_flag:
            self.aim_flag = False
            return "You released your arrow and hit your opponent", random.randint(10,20)
        else:
            self.aim_flag = False
            return "You released your arrow, hoping for the best", random.choice([0,0,0,2,3,4])
            
    def evade(self):
        self.distance += random.randint(1,3)
        return "You increased the gap between you and your opponent", 0
    
    def chant(self):
        self.chant_flag = True
        return "You begin chanting your spell.", 0
    
    def cast(self):
        if self.chant_flag:
            self.chant_flag = False
            return "You have casted fireball.", 25
        else:
            return "You didn't chant your spell! Nothing happened.", 0
    
    def reposition(self):
        self.distance += random.randint(3,5)
        return "You warp to another location, hoping to increase the distance", 0
    
    def imprison(self):
        self.distance = 3
        return "The enemy used Imprison. You are locked in place!", 5

    def eradicate(self):
        if self.eradicate_flag:
            self.eradicate_flag = False
            return "A blinding red light floods the room", 30
        else:
            self.eradicate_flag = True
            return "A glowing sigil appears behind the enemy...", 0
    
    def leer(self):
        self.damage_modifiers[0] = -5
        return "The enemy stares at you seductively. You feel uncomfortable.", 0
    
    def bites_lip(self):
        self.damage_modifiers[0] = 5
        return "The enemy bites their lip and squints. You start to feel annoyed", 0

    def rush(self):
        if self.distance <= 3:
            self.distance = 1
            return "The enemy tackles you", 5
        else:
            self.distance -= 3
            return "The enemy charges to you", 0

    def kick(self):
        if self.distance <= 2:
            return "The enemy powerfully kicks you with their hind legs", 10
        else:
            return "The enemy tries to kick you, but misses", 0
        
    def snarl(self):
        self.damage_modifiers[0] = -5
        self.damage_modifiers[1] = 5
        return "The enemy snarls loudly, you begin to feel a sense of fear...", 5

    def claw(self):
        if self.distance <= 3:
            return "The enemy nearly rips you into pieces with its claws", random.randint(10,16)
        else:
            return "The enemy attempts to shred you with its claws, but misses", 0
        
    def sidestep(self):
        self.distance += 1
        return "The enemy steps away", 0
    
    def shield(self):
        self.damage_modifiers[0] = random.randint(-5,-10)
        return "The enemy raises their shield to block", 0
    
    def cleave(self):
        if self.distance <= 2:
            return "The enemy lands a hit on you", random.randint(7,10)
        else:
            return "The enemy swings their blade, but misses", 0

    def idle(self):
        return "The enemy does nothing", 0
    