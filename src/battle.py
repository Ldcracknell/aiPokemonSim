import random
from colorama import init

# Initialize colorama
init()

# Type effectiveness chart
TYPE_CHART = {
    "Normal": {"Rock": 0.5, "Ghost": 0, "Steel": 0.5},
    "Fire": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 2, "Bug": 2, "Rock": 0.5, "Dragon": 0.5, "Steel": 2},
    "Water": {"Fire": 2, "Water": 0.5, "Grass": 0.5, "Ground": 2, "Rock": 2, "Dragon": 0.5},
    "Electric": {"Water": 2, "Electric": 0.5, "Grass": 0.5, "Ground": 0, "Flying": 2, "Dragon": 0.5},
    "Grass": {"Fire": 0.5, "Water": 2, "Grass": 0.5, "Poison": 0.5, "Ground": 2, "Flying": 0.5, "Bug": 0.5, "Rock": 2, "Dragon": 0.5, "Steel": 0.5},
    "Ice": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 0.5, "Ground": 2, "Flying": 2, "Dragon": 2, "Steel": 0.5},
    "Fighting": {"Normal": 2, "Ice": 2, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0, "Dark": 2, "Steel": 2, "Fairy": 0.5},
    "Poison": {"Grass": 2, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0, "Fairy": 2},
    "Ground": {"Fire": 2, "Electric": 2, "Grass": 0.5, "Poison": 2, "Flying": 0, "Bug": 0.5, "Rock": 2, "Steel": 2},
    "Flying": {"Electric": 0.5, "Grass": 2, "Fighting": 2, "Bug": 2, "Rock": 0.5, "Steel": 0.5},
    "Psychic": {"Fighting": 2, "Poison": 2, "Psychic": 0.5, "Dark": 0, "Steel": 0.5},
    "Bug": {"Fire": 0.5, "Grass": 2, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2, "Ghost": 0.5, "Dark": 2, "Steel": 0.5, "Fairy": 0.5},
    "Rock": {"Fire": 2, "Ice": 2, "Fighting": 0.5, "Ground": 0.5, "Flying": 2, "Bug": 2, "Steel": 0.5},
    "Ghost": {"Normal": 0, "Psychic": 2, "Ghost": 2, "Dark": 0.5},
    "Dragon": {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
    "Dark": {"Fighting": 0.5, "Psychic": 2, "Ghost": 2, "Dark": 0.5, "Fairy": 0.5},
    "Steel": {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2, "Rock": 2, "Steel": 0.5, "Fairy": 2},
    "Fairy": {"Fire": 0.5, "Fighting": 2, "Poison": 0.5, "Dragon": 2, "Dark": 2, "Steel": 0.5}
}

# Status effect descriptions
STATUS_DESCRIPTIONS = {
    "Burn": "burns and takes damage each turn",
    "Poison": "is poisoned and takes damage each turn",
    "Toxic": "is badly poisoned and takes increasing damage each turn",
    "Paralysis": "is paralyzed and may be unable to move",
    "Sleep": "fell asleep and can't move",
    "Freeze": "is frozen solid and can't move"
}

# Stat change descriptions
STAT_CHANGE_DESCRIPTIONS = {
    -3: "severely fell",
    -2: "harshly fell",
    -1: "fell",
    1: "rose",
    2: "rose sharply",
    3: "rose drastically"
}

class Battle:
    def __init__(self, player_pokemon, opponent_pokemon):
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = opponent_pokemon
        self.turn = 0
        self.is_player_turn = True
        
    def start_battle(self):
        print(f"\nA wild {self.opponent_pokemon.name} appeared!")
        print(f"\nGo, {self.player_pokemon.name}!")
        
        # Determine who goes first based on speed
        self.is_player_turn = self.player_pokemon.speed >= self.opponent_pokemon.speed
        
        # Battle loop
        while not self.is_battle_over():
            self.display_battle_status()
            
            if self.is_player_turn:
                self.player_turn()
            else:
                self.opponent_turn()
                
            # Switch turns
            self.is_player_turn = not self.is_player_turn
            self.turn += 1
            
        # Battle is over
        self.end_battle()
    
    def is_battle_over(self):
        return self.player_pokemon.is_fainted() or self.opponent_pokemon.is_fainted()
    
    def display_battle_status(self):
        print("\n" + "="*50)
        
        # Display opponent Pokemon
        opponent_type = f"{self.opponent_pokemon.type1}"
        if self.opponent_pokemon.type2:
            opponent_type += f"/{self.opponent_pokemon.type2}"
        
        print(f"\nWild {self.opponent_pokemon.name} ({opponent_type}) - Lv.{self.opponent_pokemon.level}")
        
        # Display status if any
        if self.opponent_pokemon.status:
            print(f"Status: {self.opponent_pokemon.status}")
            
        hp_percent = self.opponent_pokemon.current_hp / self.opponent_pokemon.max_hp
        hp_bar = "█" * int(hp_percent * 20)
        hp_bar = hp_bar.ljust(20)
            
        print(f"HP: {hp_bar} {self.opponent_pokemon.current_hp}/{self.opponent_pokemon.max_hp}")
        
        # Display player Pokemon
        player_type = f"{self.player_pokemon.type1}"
        if self.player_pokemon.type2:
            player_type += f"/{self.player_pokemon.type2}"
        
        print(f"\n{self.player_pokemon.name} ({player_type}) - Lv.{self.player_pokemon.level}")
        
        # Display status if any
        if self.player_pokemon.status:
            print(f"Status: {self.player_pokemon.status}")
            
        hp_percent = self.player_pokemon.current_hp / self.player_pokemon.max_hp
        hp_bar = "█" * int(hp_percent * 20)
        hp_bar = hp_bar.ljust(20)
            
        print(f"HP: {hp_bar} {self.player_pokemon.current_hp}/{self.player_pokemon.max_hp}")
        
    def player_turn(self):
        print(f"\nYour turn! Choose a move:")
        
        # Apply status effects at the start of turn
        status_effect_result = self.player_pokemon.apply_status_effects()
        if status_effect_result:
            print(status_effect_result)
            if self.player_pokemon.is_fainted():
                return
        
        # Check if Pokemon can move
        if not self.player_pokemon.can_move():
            print(f"Your {self.player_pokemon.name} is {self.player_pokemon.status} and couldn't move!")
            return
        
        # Display available moves
        for i, move in enumerate(self.player_pokemon.moves, 1):
            print(f"{i}. {move.name} ({move.type}) - {move.current_pp}/{move.max_pp} PP")
        
        # Get player choice
        choice = 0
        while choice < 1 or choice > len(self.player_pokemon.moves):
            try:
                choice = int(input("\nEnter move number: "))
                if choice < 1 or choice > len(self.player_pokemon.moves):
                    print(f"Invalid choice. Please enter a number between 1 and {len(self.player_pokemon.moves)}.")
            except ValueError:
                print(f"Please enter a valid number.")
        
        selected_move = self.player_pokemon.moves[choice - 1]
        
        # Use the move
        if selected_move.use():
            self.execute_move(self.player_pokemon, self.opponent_pokemon, selected_move)
        else:
            print(f"No PP left for this move!")
    
    def opponent_turn(self):
        # Apply status effects at the start of turn
        status_effect_result = self.opponent_pokemon.apply_status_effects()
        if status_effect_result:
            print(status_effect_result)
            if self.opponent_pokemon.is_fainted():
                return
        
        # Check if Pokemon can move
        if not self.opponent_pokemon.can_move():
            print(f"Wild {self.opponent_pokemon.name} is {self.opponent_pokemon.status} and couldn't move!")
            return
        
        # AI simply chooses a random move
        available_moves = [move for move in self.opponent_pokemon.moves if move.current_pp > 0]
        
        if not available_moves:
            print(f"\nWild {self.opponent_pokemon.name} has no moves left!")
            return
        
        selected_move = random.choice(available_moves)
        print(f"\nWild {self.opponent_pokemon.name} used {selected_move.name}!")
        
        selected_move.use()
        self.execute_move(self.opponent_pokemon, self.player_pokemon, selected_move)
    
    def execute_move(self, attacker, defender, move):
        # Check if move hits
        hit_chance = random.random() * 100
        
        # Calculate accuracy with modifiers
        accuracy = move.accuracy
        
        # Apply attacker's accuracy modifier
        accuracy_modifier = attacker.stat_modifiers.get("accuracy", 0)
        if accuracy_modifier > 0:
            accuracy *= (3 + accuracy_modifier) / 3
        elif accuracy_modifier < 0:
            accuracy *= 3 / (3 - accuracy_modifier)
            
        # Apply defender's evasion modifier
        evasion_modifier = defender.stat_modifiers.get("evasion", 0)
        if evasion_modifier > 0:
            accuracy *= 3 / (3 + evasion_modifier)
        elif evasion_modifier < 0:
            accuracy *= (3 - evasion_modifier) / 3
        
        if hit_chance > accuracy:
            print(f"The attack missed!")
            return
        
        # Calculate damage for damaging moves
        if move.category in ["Physical", "Special"]:
            # Get type effectiveness
            effectiveness = 1.0
            
            # Check defender's first type
            if defender.type1 in TYPE_CHART.get(move.type, {}):
                effectiveness *= TYPE_CHART[move.type][defender.type1]
            
            # Check defender's second type if it exists
            if defender.type2 and defender.type2 in TYPE_CHART.get(move.type, {}):
                effectiveness *= TYPE_CHART[move.type][defender.type2]
            
            # STAB (Same Type Attack Bonus)
            stab = 1.5 if move.type in [attacker.type1, attacker.type2] else 1.0
            
            # Random factor (0.85 to 1.0)
            random_factor = random.uniform(0.85, 1.0)
            
            # Calculate base damage
            if move.category == "Physical":
                attack_stat = attacker.get_modified_stat("attack") or attacker.attack
                defense_stat = defender.get_modified_stat("defense") or defender.defense
            else:  # Special
                attack_stat = attacker.get_modified_stat("sp_attack") or attacker.sp_attack
                defense_stat = defender.get_modified_stat("sp_defense") or defender.sp_defense
            
            # Damage formula
            damage = int(((2 * attacker.level / 5 + 2) * move.power * attack_stat / defense_stat / 50 + 2) * stab * effectiveness * random_factor)
            
            # Apply damage
            defender.take_damage(damage)
            
            # Display effectiveness message
            if effectiveness > 1:
                print(f"It's super effective!")
            elif effectiveness < 1 and effectiveness > 0:
                print(f"It's not very effective...")
            elif effectiveness == 0:
                print(f"It doesn't affect {defender.name}...")
                
            # Apply secondary effects if any
            if move.status_effect and random.random() * 100 <= move.effect_chance:
                if defender.apply_status(move.status_effect):
                    print(f"{defender.name} {STATUS_DESCRIPTIONS.get(move.status_effect, 'was affected')}!")
        
        # Handle status moves
        else:
            # Apply status effect if any
            if move.status_effect and random.random() * 100 <= move.effect_chance:
                if defender.apply_status(move.status_effect):
                    print(f"{defender.name} {STATUS_DESCRIPTIONS.get(move.status_effect, 'was affected')}!")
                else:
                    print(f"It failed! {defender.name} was unaffected.")
            
            # Handle special moves like Leech Seed
            if move.name == "Leech Seed":
                if defender.apply_leech_seed(attacker):
                    print(f"{defender.name} was seeded!")
                else:
                    print(f"It failed! {defender.name} was unaffected.")
            
            # Apply stat changes if any
            for stat, (change, chance) in move.stat_changes.items():
                if random.random() * 100 <= chance:
                    target = defender if change < 0 else attacker
                    stat_name = stat.replace("_", " ").title()
                    
                    if target.modify_stat(stat, change):
                        change_desc = STAT_CHANGE_DESCRIPTIONS.get(change, "changed")
                        print(f"{target.name}'s {stat_name} {change_desc}!")
    
    def end_battle(self):
        print("\n" + "="*50)
        
        if self.player_pokemon.is_fainted():
            print(f"\nYour {self.player_pokemon.name} fainted! You lost the battle.")
        else:
            print(f"\nThe wild {self.opponent_pokemon.name} fainted! You won the battle!")
            
        print("\n" + "="*50) 