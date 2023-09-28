import random

class combatSkills:
    def charge(self, distance):
        if distance <= 2:
            return "You lunge forward, tackling and knocking back the enemy in the process", random.randint(1,3)
        else:
            return "You lunge forward", distance-2, 0

    def swing(self, distance):
        if distance <= 2:
            return "You swing your sword with the intent of cleaving your opponent in half", distance, random.randint(4,7)
        else:
            return "You swing, however you are too far away and miss", distance, 0

    def block(self, distance):
        return "You take a defensive stance and ready your shield to block", distance, 0
    
    def aim(self, distance):
        return "You have selected aim."
    
    def shoot(self, distance):
        return "You have selected shoot."
    
    def evade(self, distance):
        return "You have selected evade."
    
    def chant(self, distance):
        return "You have selected chant."
    
    def cast(self, distance):
        return "You have selected cast."
    
    def reposition(self, distance):
        return "You have selected reposition."