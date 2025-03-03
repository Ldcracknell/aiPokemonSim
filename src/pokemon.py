import random

class Pokemon:
    def __init__(self, name, type1, type2=None, level=50):
        self.name = name
        self.type1 = type1
        self.type2 = type2
        self.level = level
        self.max_hp = 0
        self.current_hp = 0
        self.attack = 0
        self.defense = 0
        self.sp_attack = 0
        self.sp_defense = 0
        self.speed = 0
        self.moves = []
        self.status = None
        self.status_counter = 0
        self.leech_seed = False  # Track if the Pokemon is affected by Leech Seed
        self.leech_seed_target = None  # The Pokemon that will receive the leeched HP
        
        # Stat modifiers (range from -6 to +6)
        self.stat_modifiers = {
            "attack": 0,
            "defense": 0,
            "sp_attack": 0,
            "sp_defense": 0,
            "speed": 0,
            "accuracy": 0,
            "evasion": 0
        }
        
    def initialize_stats(self, base_hp, base_atk, base_def, base_sp_atk, base_sp_def, base_spd):
        # Simple formula to calculate stats based on level and base stats
        self.max_hp = int((2 * base_hp * self.level) / 100) + self.level + 10
        self.current_hp = self.max_hp
        self.attack = int((2 * base_atk * self.level) / 100) + 5
        self.defense = int((2 * base_def * self.level) / 100) + 5
        self.sp_attack = int((2 * base_sp_atk * self.level) / 100) + 5
        self.sp_defense = int((2 * base_sp_def * self.level) / 100) + 5
        self.speed = int((2 * base_spd * self.level) / 100) + 5
        
    def add_move(self, move):
        if len(self.moves) < 4:
            self.moves.append(move)
            return True
        return False
        
    def is_fainted(self):
        return self.current_hp <= 0
        
    def take_damage(self, damage):
        print(f"DEBUG - Taking Damage: {self.name}")
        print(f"  Current HP before: {self.current_hp}")
        print(f"  Damage amount: {damage}")
        self.current_hp = max(0, self.current_hp - damage)
        print(f"  Current HP after: {self.current_hp}")
        
    def heal(self, amount):
        self.current_hp = min(self.max_hp, self.current_hp + amount)
    
    def apply_status(self, status):
        """Apply a status effect to the Pokemon"""
        # Don't apply if already has a status
        if self.status is not None:
            return False
            
        # Check for type immunities
        if status == "Paralysis" and ("Electric" in [self.type1, self.type2] or "Ground" in [self.type1, self.type2]):
            return False
        if status == "Poison" and ("Poison" in [self.type1, self.type2] or "Steel" in [self.type1, self.type2]):
            return False
        if status == "Burn" and "Fire" in [self.type1, self.type2]:
            return False
            
        self.status = status
        self.status_counter = 0
        return True
    
    def remove_status(self):
        """Remove the current status effect"""
        self.status = None
        self.status_counter = 0
    
    def modify_stat(self, stat, change):
        """Modify a stat by the given amount (-6 to +6 range)"""
        if stat in self.stat_modifiers:
            self.stat_modifiers[stat] = max(-6, min(6, self.stat_modifiers[stat] + change))
            return True
        return False
    
    def get_modified_stat(self, stat):
        """Get the value of a stat after applying modifiers"""
        # Get the modifier with a default of 0 if not found
        modifier = self.stat_modifiers.get(stat, 0)
        multiplier = 1.0
        
        if modifier > 0:
            multiplier = (2 + modifier) / 2
        elif modifier < 0:
            multiplier = 2 / (2 - modifier)
            
        if stat == "attack":
            # Burn reduces Attack by 50%
            burn_multiplier = 0.5 if self.status == "Burn" else 1.0
            return int(self.attack * multiplier * burn_multiplier)
        elif stat == "defense":
            return int(self.defense * multiplier)
        elif stat == "sp_attack":
            return int(self.sp_attack * multiplier)
        elif stat == "sp_defense":
            return int(self.sp_defense * multiplier)
        elif stat == "speed":
            # Paralysis reduces Speed by 50%
            paralysis_multiplier = 0.5 if self.status == "Paralysis" else 1.0
            return int(self.speed * multiplier * paralysis_multiplier)
        elif stat == "accuracy" or stat == "evasion":
            # These stats don't have base values, just return the multiplier
            return multiplier
        
        # If we get here, it's an unknown stat
        return 0
    
    def apply_status_effects(self):
        """Apply effects of status conditions at the start of turn"""
        result_message = ""
        damage = 0
        
        # Handle regular status effects
        if self.status is not None:
            self.status_counter += 1
            
            if self.status == "Burn":
                # Burn deals damage and reduces Attack
                damage = max(1, int(self.max_hp / 16))
                self.take_damage(damage)
                result_message += f"{self.name} was hurt by its burn!"
                
            elif self.status == "Poison":
                # Poison deals increasing damage over time
                damage = max(1, int(self.max_hp / 16))
                self.take_damage(damage)
                result_message += f"{self.name} was hurt by poison!"
                
            elif self.status == "Toxic":
                # Toxic poison deals increasing damage over time
                damage = max(1, int(self.max_hp * self.status_counter / 16))
                self.take_damage(damage)
                result_message += f"{self.name} was hurt by toxic poison!"
                
            elif self.status == "Paralysis":
                # Paralysis has a 25% chance to prevent attacking
                # Speed reduction is handled in get_modified_stat
                pass
                
            elif self.status == "Sleep":
                # Sleep prevents attacking for 1-3 turns
                if self.status_counter >= random.randint(1, 3):
                    self.remove_status()
                    result_message += f"{self.name} woke up!"
                
            elif self.status == "Freeze":
                # Freeze prevents attacking with 20% chance to thaw each turn
                if random.random() < 0.2:
                    self.remove_status()
                    result_message += f"{self.name} thawed out!"
        
        # Handle Leech Seed effect
        if self.leech_seed and self.leech_seed_target and not self.is_fainted():
            leech_damage = max(1, int(self.max_hp / 8))
            self.take_damage(leech_damage)
            
            # Heal the target Pokemon
            heal_amount = min(leech_damage, self.leech_seed_target.max_hp - self.leech_seed_target.current_hp)
            if heal_amount > 0:
                self.leech_seed_target.heal(heal_amount)
                
            result_message += f"{self.name}'s health was sapped by Leech Seed!"
        
        return result_message
    
    def apply_leech_seed(self, target):
        """Apply Leech Seed effect to this Pokemon"""
        # Don't apply if already affected by Leech Seed
        if self.leech_seed:
            return False
            
        # Grass types are immune to Leech Seed
        if "Grass" in [self.type1, self.type2]:
            return False
            
        self.leech_seed = True
        self.leech_seed_target = target
        return True
        
    def remove_leech_seed(self):
        """Remove the Leech Seed effect"""
        self.leech_seed = False
        self.leech_seed_target = None
    
    def can_move(self):
        """Check if the Pokemon can move this turn"""
        if self.status == "Paralysis":
            return random.random() > 0.25  # 25% chance to be fully paralyzed
        elif self.status == "Sleep" or self.status == "Freeze":
            return False  # Can't move while asleep or frozen
        return True
        
    def __str__(self):
        return f"{self.name} (Lv.{self.level}) - HP: {self.current_hp}/{self.max_hp}" 