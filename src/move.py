class Move:
    def __init__(self, name, type, category, power, accuracy, pp):
        self.name = name
        self.type = type
        self.category = category  # Physical, Special, or Status
        self.power = power
        self.accuracy = accuracy
        self.max_pp = pp
        self.current_pp = pp
        self.effect = None
        self.effect_chance = 0
        self.status_effect = None
        self.stat_changes = {}  # e.g., {"attack": -1, "defense": 2}
        
    def use(self):
        if self.current_pp > 0:
            self.current_pp -= 1
            return True
        return False
    
    def restore(self):
        self.current_pp = self.max_pp
        
    def set_status_effect(self, status, chance=100):
        """Set a status effect with a chance to apply"""
        self.status_effect = status
        self.effect_chance = chance
        
    def set_stat_change(self, stat, change, chance=100):
        """Set a stat change with a chance to apply"""
        self.stat_changes[stat] = (change, chance)
        
    def __str__(self):
        return f"{self.name} ({self.type}) - PP: {self.current_pp}/{self.max_pp}" 