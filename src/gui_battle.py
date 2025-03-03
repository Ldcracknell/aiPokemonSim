import tkinter as tk
from tkinter import ttk, font, messagebox
import random
import time
import threading

# Import our modules
from pokemon import Pokemon
from move import Move
from battle import Battle, STATUS_DESCRIPTIONS, STAT_CHANGE_DESCRIPTIONS, TYPE_CHART
from pokedex import get_all_pokemon

class GUIBattle(Battle):
    def __init__(self, player_pokemon, opponent_pokemon, master=None):
        super().__init__(player_pokemon, opponent_pokemon)
        self.master = master
        self.animation_in_progress = False
        
        # Create the main battle frame
        self.battle_frame = tk.Frame(master, width=800, height=600)
        self.battle_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the animation canvas
        self.animation_canvas = tk.Canvas(self.battle_frame, width=800, height=400, bg="#f0f0f0")
        self.animation_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create frames for Pokémon info
        self.player_info_frame = tk.Frame(self.animation_canvas, bg="#e0e0e0", bd=2, relief=tk.RAISED)
        self.player_info_frame.place(relx=0.05, rely=0.7, relwidth=0.4, relheight=0.25)
        
        self.opponent_info_frame = tk.Frame(self.animation_canvas, bg="#e0e0e0", bd=2, relief=tk.RAISED)
        self.opponent_info_frame.place(relx=0.55, rely=0.1, relwidth=0.4, relheight=0.25)
        
        # Create labels for Pokémon info
        self.player_name_label = tk.Label(self.player_info_frame, text=f"{self.player_pokemon.name}", font=("Arial", 12, "bold"), bg="#e0e0e0")
        self.player_name_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        self.player_hp_label = tk.Label(self.player_info_frame, text=f"HP: {self.player_pokemon.current_hp}/{self.player_pokemon.max_hp}", font=("Arial", 10), bg="#e0e0e0")
        self.player_hp_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        self.player_status_label = tk.Label(self.player_info_frame, text="", font=("Arial", 10), bg="#e0e0e0", fg="red")
        self.player_status_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        
        # Add stat modifier labels for player
        self.player_stat_frame = tk.Frame(self.player_info_frame, bg="#e0e0e0")
        self.player_stat_frame.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        
        self.player_stat_labels = {}
        for i, stat in enumerate(["attack", "defense", "sp_attack", "sp_defense", "speed"]):
            label = tk.Label(self.player_stat_frame, text="", font=("Arial", 8), bg="#e0e0e0")
            label.grid(row=0, column=i, padx=2)
            self.player_stat_labels[stat] = label
        
        self.opponent_name_label = tk.Label(self.opponent_info_frame, text=f"{self.opponent_pokemon.name}", font=("Arial", 12, "bold"), bg="#e0e0e0")
        self.opponent_name_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        self.opponent_hp_label = tk.Label(self.opponent_info_frame, text=f"HP: {self.opponent_pokemon.current_hp}/{self.opponent_pokemon.max_hp}", font=("Arial", 10), bg="#e0e0e0")
        self.opponent_hp_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        self.opponent_status_label = tk.Label(self.opponent_info_frame, text="", font=("Arial", 10), bg="#e0e0e0", fg="red")
        self.opponent_status_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        
        # Add stat modifier labels for opponent
        self.opponent_stat_frame = tk.Frame(self.opponent_info_frame, bg="#e0e0e0")
        self.opponent_stat_frame.grid(row=3, column=0, sticky="w", padx=5, pady=2)
        
        self.opponent_stat_labels = {}
        for i, stat in enumerate(["attack", "defense", "sp_attack", "sp_defense", "speed"]):
            label = tk.Label(self.opponent_stat_frame, text="", font=("Arial", 8), bg="#e0e0e0")
            label.grid(row=0, column=i, padx=2)
            self.opponent_stat_labels[stat] = label
        
        # Create HP bars
        self.player_hp_bar = ttk.Progressbar(self.player_info_frame, orient=tk.HORIZONTAL, length=150, mode='determinate', maximum=self.player_pokemon.max_hp, value=self.player_pokemon.current_hp)
        self.player_hp_bar.grid(row=4, column=0, padx=5, pady=2, sticky="w")
        
        self.opponent_hp_bar = ttk.Progressbar(self.opponent_info_frame, orient=tk.HORIZONTAL, length=150, mode='determinate', maximum=self.opponent_pokemon.max_hp, value=self.opponent_pokemon.current_hp)
        self.opponent_hp_bar.grid(row=4, column=0, padx=5, pady=2, sticky="w")
        
        # Create Pokémon images
        self.player_pokemon_img = self.create_pokemon_image(self.player_pokemon.name, is_player=True)
        self.opponent_pokemon_img = self.create_pokemon_image(self.opponent_pokemon.name, is_player=False)
        
        # Create battle log
        self.battle_log_frame = tk.Frame(self.battle_frame, bg="#ffffff", bd=2, relief=tk.SUNKEN)
        self.battle_log_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.battle_log = tk.Text(self.battle_log_frame, height=4, width=80, wrap=tk.WORD, state=tk.DISABLED)
        self.battle_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create move buttons in a 2x2 grid
        self.move_buttons_frame = tk.Frame(self.battle_frame)
        self.move_buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.move_buttons = []
        for i in range(4):
            row = i // 2
            col = i % 2
            move_name = self.player_pokemon.moves[i].name if i < len(self.player_pokemon.moves) else "---"
            move_type = self.player_pokemon.moves[i].type if i < len(self.player_pokemon.moves) else "Normal"
            
            button_color = self.get_type_color(move_type)
            
            button = tk.Button(
                self.move_buttons_frame,
                text=move_name,
                width=20,
                height=2,
                bg=button_color,
                command=lambda idx=i: self.execute_player_move(idx)
            )
            button.grid(row=row, column=col, padx=5, pady=5)
            self.move_buttons.append(button)
        
        # Display initial battle status
        self.display_battle_status()
        
        # Log initial message
        self.log_message(f"A wild {self.opponent_pokemon.name} appeared!")
        self.log_message(f"Go, {self.player_pokemon.name}!")

    def create_pokemon_image(self, pokemon_name, is_player=True):
        """Create a simple representation of a Pokémon"""
        # Position for player and opponent
        x_pos = 150 if is_player else 600
        y_pos = 300 if is_player else 150
        
        # Create oval for Pokémon
        pokemon_type = self.player_pokemon.type1 if is_player else self.opponent_pokemon.type1
        color = self.get_type_color(pokemon_type)
        
        oval = self.animation_canvas.create_oval(
            x_pos - 40, y_pos - 40, 
            x_pos + 40, y_pos + 40, 
            fill=color, outline="black", width=2
        )
        
        # Add name text
        self.animation_canvas.create_text(
            x_pos, y_pos, 
            text=pokemon_name, 
            fill="black", 
            font=("Arial", 10, "bold")
        )
        
        return oval

    def get_type_color(self, type_name):
        """Return color for Pokémon type"""
        type_colors = {
            "Normal": "#A8A878",
            "Fire": "#F08030",
            "Water": "#6890F0",
            "Electric": "#F8D030",
            "Grass": "#78C850",
            "Ice": "#98D8D8",
            "Fighting": "#C03028",
            "Poison": "#A040A0",
            "Ground": "#E0C068",
            "Flying": "#A890F0",
            "Psychic": "#F85888",
            "Bug": "#A8B820",
            "Rock": "#B8A038",
            "Ghost": "#705898",
            "Dragon": "#7038F8",
            "Dark": "#705848",
            "Steel": "#B8B8D0",
            "Fairy": "#EE99AC"
        }
        return type_colors.get(type_name, "#A8A878")  # Default to Normal type color

    def get_status_color(self, status):
        """Return color for status condition"""
        status_colors = {
            "Burn": "#FF4500",  # OrangeRed
            "Poison": "#800080",  # Purple
            "Toxic": "#660066",  # Dark Purple
            "Paralysis": "#FFD700",  # Gold
            "Sleep": "#808080",  # Gray
            "Freeze": "#00BFFF",  # Deep Sky Blue
            "": "#000000"  # Black (no status)
        }
        return status_colors.get(status, "#000000")

    def update_status_labels(self):
        """Update the status labels for both Pokémon"""
        if self.player_pokemon.status:
            self.player_status_label.config(
                text=f"Status: {self.player_pokemon.status}",
                fg=self.get_status_color(self.player_pokemon.status)
            )
        else:
            self.player_status_label.config(text="")
            
        if self.opponent_pokemon.status:
            self.opponent_status_label.config(
                text=f"Status: {self.opponent_pokemon.status}",
                fg=self.get_status_color(self.opponent_pokemon.status)
            )
        else:
            self.opponent_status_label.config(text="")

    def update_stat_labels(self):
        """Update the stat modifier labels for both Pokémon"""
        # Update player stat labels
        for stat, label in self.player_stat_labels.items():
            modifier = self.player_pokemon.stat_modifiers.get(stat, 0)
            if modifier != 0:
                label.config(
                    text=f"{stat.split('_')[-1][:3]}: {'+' if modifier > 0 else ''}{modifier}",
                    fg="#00AA00" if modifier > 0 else "#AA0000"
                )
            else:
                label.config(text="")
                
        # Update opponent stat labels
        for stat, label in self.opponent_stat_labels.items():
            modifier = self.opponent_pokemon.stat_modifiers.get(stat, 0)
            if modifier != 0:
                label.config(
                    text=f"{stat.split('_')[-1][:3]}: {'+' if modifier > 0 else ''}{modifier}",
                    fg="#00AA00" if modifier > 0 else "#AA0000"
                )
            else:
                label.config(text="")

    def display_battle_status(self):
        """Display the current battle status"""
        # Update HP labels and bars
        self.player_hp_label.config(text=f"HP: {self.player_pokemon.current_hp}/{self.player_pokemon.max_hp}")
        self.player_hp_bar["value"] = self.player_pokemon.current_hp
        
        self.opponent_hp_label.config(text=f"HP: {self.opponent_pokemon.current_hp}/{self.opponent_pokemon.max_hp}")
        self.opponent_hp_bar["value"] = self.opponent_pokemon.current_hp
        
        # Update status labels
        self.update_status_labels()
        
        # Update stat modifier labels
        self.update_stat_labels()
        
        # Update move buttons
        for i, button in enumerate(self.move_buttons):
            if i < len(self.player_pokemon.moves):
                move = self.player_pokemon.moves[i]
                button_color = self.get_type_color(move.type)
                button.config(
                    text=f"{move.name} ({move.current_pp}/{move.max_pp})",
                    bg=button_color,
                    state=tk.NORMAL if move.current_pp > 0 else tk.DISABLED
                )
            else:
                button.config(text="---", state=tk.DISABLED)

    def log_message(self, message):
        """Add a message to the battle log"""
        self.battle_log.config(state=tk.NORMAL)
        self.battle_log.insert(tk.END, message + "\n")
        self.battle_log.see(tk.END)
        self.battle_log.config(state=tk.DISABLED)
        self.master.update()

    def animate_attack(self, attacker_img, defender_img, move, is_player_attacking=True):
        """Animate an attack"""
        try:
            if not self.animation_canvas.winfo_exists():
                return  # Canvas no longer exists
                
            # Get original positions
            attacker_coords = self.animation_canvas.coords(attacker_img)
            defender_coords = self.animation_canvas.coords(defender_img)
            
            attacker_x = (attacker_coords[0] + attacker_coords[2]) / 2
            attacker_y = (attacker_coords[1] + attacker_coords[3]) / 2
            
            defender_x = (defender_coords[0] + defender_coords[2]) / 2
            defender_y = (defender_coords[1] + defender_coords[3]) / 2
            
            # Create move effect (a colored circle)
            move_color = self.get_type_color(move.type)
            effect = self.animation_canvas.create_oval(
                attacker_x - 10, attacker_y - 10,
                attacker_x + 10, attacker_y + 10,
                fill=move_color, outline="white", width=2
            )
            
            # Calculate direction vector
            dx = defender_x - attacker_x
            dy = defender_y - attacker_y
            distance = (dx**2 + dy**2)**0.5
            
            # Normalize direction
            if distance > 0:
                dx = dx / distance
                dy = dy / distance
            
            # Animation steps
            steps = 20
            step_size = distance / steps
            
            def animate_step(step=0):
                try:
                    if not self.animation_canvas.winfo_exists():
                        return  # Canvas no longer exists
                        
                    if step < steps:
                        # Move the effect toward the defender
                        self.animation_canvas.move(effect, dx * step_size, dy * step_size)
                        
                        # Schedule the next step
                        self.master.after(30, lambda: animate_step(step + 1))
                    else:
                        # Flash the defender to indicate hit
                        original_fill = self.animation_canvas.itemcget(defender_img, "fill")
                        self.animation_canvas.itemconfig(defender_img, fill="white")
                        
                        # Shake the defender
                        for i in range(5):
                            self.animation_canvas.move(defender_img, 5 if i % 2 == 0 else -5, 0)
                            self.master.update()
                            time.sleep(0.05)
                        
                        # Reset defender position and color
                        self.animation_canvas.coords(defender_img, defender_coords)
                        self.animation_canvas.itemconfig(defender_img, fill=original_fill)
                        
                        # Delete the effect
                        self.animation_canvas.delete(effect)
                        
                        # Animation is complete
                        self.animation_in_progress = False
                except tk.TclError:
                    # Handle case where widget was destroyed
                    self.animation_in_progress = False
            
            # Start the animation
            animate_step()
        except tk.TclError:
            # Handle case where widget was destroyed
            self.animation_in_progress = False

    def execute_player_move(self, move_index):
        """Execute the player's move"""
        if self.animation_in_progress:
            return
            
        if move_index >= len(self.player_pokemon.moves):
            return
            
        move = self.player_pokemon.moves[move_index]
        
        if move.current_pp <= 0:
            self.log_message(f"{move.name} has no PP left!")
            return
            
        # Apply status effects at the start of the turn
        status_effect_result = self.player_pokemon.apply_status_effects()
        if status_effect_result:
            self.log_message(status_effect_result)
            self.display_battle_status()
            
        # Check if the Pokémon can move
        if not self.player_pokemon.can_move():
            self.log_message(f"{self.player_pokemon.name} is unable to move!")
            self.display_battle_status()
            self.master.after(1000, self.opponent_turn)
            return
            
        self.log_message(f"{self.player_pokemon.name} used {move.name}!")
        
        # Use the move
        if not move.use():
            self.log_message(f"No PP left for {move.name}!")
            return
        
        # Animate the attack
        self.animation_in_progress = True
        self.animate_attack(
            self.player_pokemon_img, 
            self.opponent_pokemon_img, 
            move,
            is_player_attacking=True
        )
        
        # Wait for animation to complete
        def after_animation():
            # Execute the move
            old_hp = self.opponent_pokemon.current_hp
            self.battle.execute_move(move, self.player_pokemon, self.opponent_pokemon)
            damage_dealt = old_hp - self.opponent_pokemon.current_hp
            
            # Update the display
            self.display_battle_status()
            
            # Log the result
            self.log_message(f"It dealt {damage_dealt} damage!")
            
            # Check if the battle is over
            if self.is_battle_over():
                winner = self.get_winner()
                self.log_message(f"{winner.name} wins the battle!")
                return
                
            # Opponent's turn
            self.master.after(1500, self.opponent_turn)
        
        # Check animation status every 100ms
        def check_animation():
            if not self.animation_in_progress:
                after_animation()
            else:
                self.master.after(100, check_animation)
        
        check_animation()

    def opponent_turn(self):
        """Execute the opponent's turn"""
        if self.animation_in_progress:
            return
            
        # Apply status effects at the start of the turn
        status_effect_result = self.opponent_pokemon.apply_status_effects()
        if status_effect_result:
            self.log_message(status_effect_result)
            self.display_battle_status()
            
        # Check if the Pokémon can move
        if not self.opponent_pokemon.can_move():
            self.log_message(f"{self.opponent_pokemon.name} is unable to move!")
            self.display_battle_status()
            self.master.after(1000, lambda: self.check_battle_end())
            return
            
        # Choose a random move
        available_moves = [move for move in self.opponent_pokemon.moves if move.current_pp > 0]
        if not available_moves:
            self.log_message(f"{self.opponent_pokemon.name} has no moves left!")
            return
            
        move = random.choice(available_moves)
        self.log_message(f"{self.opponent_pokemon.name} used {move.name}!")
        
        # Use the move
        move.use()
        
        # Animate the attack
        self.animation_in_progress = True
        self.animate_attack(
            self.opponent_pokemon_img, 
            self.player_pokemon_img, 
            move,
            is_player_attacking=False
        )
        
        # Wait for animation to complete
        def after_animation():
            # Execute the move
            old_hp = self.player_pokemon.current_hp
            self.battle.execute_move(move, self.opponent_pokemon, self.player_pokemon)
            damage_dealt = old_hp - self.player_pokemon.current_hp
            
            # Update the display
            self.display_battle_status()
            
            # Log the result
            self.log_message(f"It dealt {damage_dealt} damage!")
            
            # Check if the battle is over
            if self.is_battle_over():
                winner = self.get_winner()
                self.log_message(f"{winner.name} wins the battle!")
        
        # Check animation status every 100ms
        def check_animation():
            if not self.animation_in_progress:
                after_animation()
            else:
                self.master.after(100, check_animation)
        
        check_animation()

    def execute_move(self, move, attacker, defender):
        """Execute a move and return the result message"""
        result_message = ""
        
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
        
        # Check if move hits
        hit_chance = random.random() * 100
        if hit_chance > accuracy:
            return "The attack missed!"
        
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
            
            # Debug information
            print(f"DEBUG - Damage Calculation:")
            print(f"  Attacker: {attacker.name}, Level: {attacker.level}")
            print(f"  Move: {move.name}, Power: {move.power}, Type: {move.type}, Category: {move.category}")
            print(f"  Attack Stat: {attack_stat}, Defense Stat: {defense_stat}")
            print(f"  STAB: {stab}, Effectiveness: {effectiveness}, Random Factor: {random_factor:.2f}")
            print(f"  Final Damage: {damage}")
            
            # Apply damage
            defender.take_damage(damage)
            
            # Build result message
            result_message = f"It dealt {damage} damage!"
            
            # Add effectiveness message
            if effectiveness > 1:
                result_message += " It's super effective!"
            elif effectiveness < 1 and effectiveness > 0:
                result_message += " It's not very effective..."
            elif effectiveness == 0:
                result_message = f"It doesn't affect {defender.name}..."
                
            # Apply secondary effects if any
            if move.status_effect and random.random() * 100 <= move.effect_chance:
                if defender.apply_status(move.status_effect):
                    result_message += f" {defender.name} {STATUS_DESCRIPTIONS.get(move.status_effect, 'was affected')}!"
        
        # Handle status moves
        else:
            result_message = "The move was used!"
            
            # Apply status effect if any
            if move.status_effect and random.random() * 100 <= move.effect_chance:
                if defender.apply_status(move.status_effect):
                    result_message = f"{defender.name} {STATUS_DESCRIPTIONS.get(move.status_effect, 'was affected')}!"
                else:
                    result_message = f"It failed! {defender.name} was unaffected."
            
            # Handle special moves like Leech Seed
            if move.name == "Leech Seed":
                if defender.apply_leech_seed(attacker):
                    result_message = f"{defender.name} was seeded!"
                else:
                    result_message = f"It failed! {defender.name} was unaffected."
            
            # Apply stat changes if any
            for stat, (change, chance) in move.stat_changes.items():
                if random.random() * 100 <= chance:
                    target = defender if change < 0 else attacker
                    stat_name = stat.replace("_", " ").title()
                    
                    if target.modify_stat(stat, change):
                        change_desc = STAT_CHANGE_DESCRIPTIONS.get(change, "changed")
                        result_message += f" {target.name}'s {stat_name} {change_desc}!"
        
        return result_message

    def is_battle_over(self):
        """Check if the battle is over"""
        return self.player_pokemon.is_fainted() or self.opponent_pokemon.is_fainted()
    
    def get_winner(self):
        """Get the winner of the battle"""
        if self.player_pokemon.is_fainted():
            return self.opponent_pokemon
        else:
            return self.player_pokemon

    def check_battle_end(self):
        """Check if the battle has ended and handle accordingly"""
        if self.is_battle_over():
            winner = self.get_winner()
            if winner == self.player_pokemon:
                self.log_message(f"You defeated {self.opponent_pokemon.name}!")
            else:
                self.log_message(f"Your {self.player_pokemon.name} was defeated!")
            return True
        return False

    def show_battle_end(self, player_won):
        """Show battle end dialog"""
        if player_won:
            message = f"Congratulations! You defeated the wild {self.opponent_pokemon.name}!"
            title = "Victory!"
        else:
            message = f"Your {self.player_pokemon.name} fainted! Better luck next time."
            title = "Defeat!"
            
        # Ask if player wants to play again
        play_again = messagebox.askyesno(
            title=title,
            message=message + "\n\nWould you like to battle again?"
        )
        
        if play_again:
            self.show_starter_selection()
        else:
            self.show_title_screen()

class PokemonBattleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokémon Battle Simulator")
        self.root.geometry("800x700")  # Increased height for more space
        self.root.resizable(False, False)
        
        # Set up fonts
        self.title_font = font.Font(family="Arial", size=24, weight="bold")
        self.header_font = font.Font(family="Arial", size=16, weight="bold")
        self.normal_font = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=12, weight="bold")
        
        # Game state variables
        self.pokemon_db = get_all_pokemon()
        self.player_pokemon = None
        self.opponent_pokemon = None
        self.battle = None
        self.battle_in_progress = False
        self.animation_in_progress = False
        
        # Create frames
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Start with the title screen
        self.show_title_screen()
    
    def clear_frame(self, frame):
        """Clear all widgets from a frame"""
        for widget in frame.winfo_children():
            widget.destroy()
    
    def show_title_screen(self):
        """Display the title screen"""
        self.clear_frame(self.main_frame)
        
        # Title
        title_label = tk.Label(self.main_frame, text="Pokémon Battle Simulator", font=self.title_font)
        title_label.pack(pady=(50, 30))
        
        # Start button
        start_button = tk.Button(
            self.main_frame, 
            text="Start New Game", 
            font=self.button_font,
            command=self.show_starter_selection,
            width=20,
            height=2
        )
        start_button.pack(pady=10)
        
        # Quit button
        quit_button = tk.Button(
            self.main_frame, 
            text="Quit", 
            font=self.button_font,
            command=self.root.quit,
            width=20,
            height=2
        )
        quit_button.pack(pady=10)
    
    def show_starter_selection(self):
        """Show the starter Pokémon selection screen"""
        self.clear_frame(self.main_frame)
        
        # Header
        header_label = tk.Label(
            self.main_frame, 
            text="Choose your starter Pokémon", 
            font=self.header_font
        )
        header_label.pack(pady=(20, 30))
        
        # Starters frame
        starters_frame = tk.Frame(self.main_frame)
        starters_frame.pack(pady=20)
        
        starters = ["Bulbasaur", "Charmander", "Squirtle"]
        
        # Create a button for each starter
        for i, name in enumerate(starters):
            pokemon = self.pokemon_db[name]
            
            # Create frame for this starter
            starter_frame = tk.Frame(starters_frame, padx=15, pady=15, borderwidth=2, relief="ridge")
            starter_frame.grid(row=0, column=i, padx=10)
            
            # Pokemon name
            name_label = tk.Label(starter_frame, text=name, font=self.header_font)
            name_label.pack(pady=(0, 5))
            
            # Pokemon type
            type_text = f"Type: {pokemon.type1}"
            if pokemon.type2:
                type_text += f"/{pokemon.type2}"
            type_label = tk.Label(starter_frame, text=type_text, font=self.normal_font)
            type_label.pack(pady=5)
            
            # Stats
            stats_text = f"HP: {pokemon.max_hp}\nAttack: {pokemon.attack}\nDefense: {pokemon.defense}\nSpeed: {pokemon.speed}"
            stats_label = tk.Label(starter_frame, text=stats_text, font=self.normal_font, justify=tk.LEFT)
            stats_label.pack(pady=5)
            
            # Select button
            select_button = tk.Button(
                starter_frame,
                text="Choose",
                font=self.button_font,
                command=lambda p=pokemon: self.select_starter(p),
                width=10
            )
            select_button.pack(pady=10)
    
    def select_starter(self, pokemon):
        """Handle starter selection"""
        self.player_pokemon = pokemon
        
        # Choose a random opponent
        self.opponent_pokemon = self.choose_opponent()
        
        # Start the battle
        self.battle = GUIBattle(self.player_pokemon, self.opponent_pokemon, self.main_frame)
        self.show_battle_screen()
    
    def choose_opponent(self):
        """Choose a random opponent Pokemon"""
        # Filter out the player's Pokemon
        available_pokemon = [name for name in self.pokemon_db.keys() if name != self.player_pokemon.name]
        opponent_name = random.choice(available_pokemon)
        
        return self.pokemon_db[opponent_name]
    
    def show_battle_screen(self):
        """Show the battle screen"""
        self.clear_frame(self.main_frame)
        self.battle_in_progress = True
        
        # Create battle frames
        battle_info_frame = tk.Frame(self.main_frame)
        battle_info_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Animation canvas
        animation_frame = tk.Frame(self.main_frame, padx=10, pady=5)
        animation_frame.pack(fill=tk.X, pady=(0, 5))
        
        animation_canvas = tk.Canvas(animation_frame, width=760, height=120)  # Reduced height
        animation_canvas.pack()
        
        # Draw battle field
        animation_canvas.create_rectangle(50, 100, 300, 140, fill="#a0a0a0", outline="")  # Player platform
        animation_canvas.create_rectangle(460, 60, 710, 100, fill="#a0a0a0", outline="")  # Opponent platform
        
        # Draw Pokemon representations (simple shapes for now)
        player_pokemon_oval = animation_canvas.create_oval(150, 60, 220, 130, fill=self.get_type_color(self.player_pokemon.type1), outline="black", width=2)
        opponent_pokemon_oval = animation_canvas.create_oval(560, 20, 630, 90, fill=self.get_type_color(self.opponent_pokemon.type1), outline="black", width=2)
        
        # Add Pokemon names
        animation_canvas.create_text(185, 95, text=self.player_pokemon.name, fill="black", font=self.normal_font)
        animation_canvas.create_text(595, 55, text=self.opponent_pokemon.name, fill="black", font=self.normal_font)
        
        opponent_frame = tk.Frame(self.main_frame, padx=10, pady=5)
        opponent_frame.pack(fill=tk.X, pady=(0, 5))
        
        player_frame = tk.Frame(self.main_frame, padx=10, pady=5)
        player_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Battle info
        turn_label = tk.Label(
            battle_info_frame, 
            text=f"Turn {self.battle.turn + 1}", 
            font=self.header_font
        )
        turn_label.pack(side=tk.LEFT, padx=10)
        
        # Status label for battle feedback
        status_label = tk.Label(
            battle_info_frame,
            text="Battle started! Choose your move.",
            font=self.normal_font,
            fg="blue"
        )
        status_label.pack(side=tk.RIGHT, padx=10)
        
        # Opponent info
        opponent_type = f"{self.opponent_pokemon.type1}"
        if self.opponent_pokemon.type2:
            opponent_type += f"/{self.opponent_pokemon.type2}"
            
        opponent_label = tk.Label(
            opponent_frame,
            text=f"Wild {self.opponent_pokemon.name} (Lv.{self.opponent_pokemon.level}) - {opponent_type}",
            font=self.header_font
        )
        opponent_label.pack(anchor=tk.W)
        
        # Opponent HP bar
        opponent_hp_frame = tk.Frame(opponent_frame)
        opponent_hp_frame.pack(fill=tk.X, pady=5)
        
        opponent_hp_label = tk.Label(
            opponent_hp_frame,
            text=f"HP: {self.opponent_pokemon.current_hp}/{self.opponent_pokemon.max_hp}",
            font=self.normal_font
        )
        opponent_hp_label.pack(side=tk.LEFT)
        
        opponent_hp_bar = ttk.Progressbar(
            opponent_hp_frame,
            orient=tk.HORIZONTAL,
            length=400,
            mode='determinate'
        )
        opponent_hp_bar.pack(side=tk.LEFT, padx=10)
        opponent_hp_bar['value'] = (self.opponent_pokemon.current_hp / self.opponent_pokemon.max_hp) * 100
        
        # Player info
        player_type = f"{self.player_pokemon.type1}"
        if self.player_pokemon.type2:
            player_type += f"/{self.player_pokemon.type2}"
            
        player_label = tk.Label(
            player_frame,
            text=f"{self.player_pokemon.name} (Lv.{self.player_pokemon.level}) - {player_type}",
            font=self.header_font
        )
        player_label.pack(anchor=tk.W)
        
        # Player HP bar
        player_hp_frame = tk.Frame(player_frame)
        player_hp_frame.pack(fill=tk.X, pady=5)
        
        player_hp_label = tk.Label(
            player_hp_frame,
            text=f"HP: {self.player_pokemon.current_hp}/{self.player_pokemon.max_hp}",
            font=self.normal_font
        )
        player_hp_label.pack(side=tk.LEFT)
        
        player_hp_bar = ttk.Progressbar(
            player_hp_frame,
            orient=tk.HORIZONTAL,
            length=400,
            mode='determinate'
        )
        player_hp_bar.pack(side=tk.LEFT, padx=10)
        player_hp_bar['value'] = (self.player_pokemon.current_hp / self.player_pokemon.max_hp) * 100
        
        # Battle log
        log_frame = tk.Frame(self.main_frame, padx=10, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        log_label = tk.Label(log_frame, text="Battle Log:", font=self.normal_font, anchor=tk.W)
        log_label.pack(anchor=tk.W)
        
        log_text = tk.Text(log_frame, height=5, width=70, font=self.normal_font)  # Reduced height
        log_text.pack(fill=tk.BOTH, expand=True)
        log_text.insert(tk.END, f"A wild {self.opponent_pokemon.name} appeared!\n")
        log_text.insert(tk.END, f"Go, {self.player_pokemon.name}!\n")
        log_text.config(state=tk.DISABLED)
        
        # Move buttons
        moves_frame = tk.Frame(self.main_frame, padx=10, pady=10)
        moves_frame.pack(fill=tk.X)
        
        moves_label = tk.Label(moves_frame, text="Choose a move:", font=self.normal_font)
        moves_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Create a grid for move buttons (2x2)
        move_grid = tk.Frame(moves_frame)
        move_grid.pack(fill=tk.X)
        
        # Configure grid columns to be equal width
        move_grid.columnconfigure(0, weight=1)
        move_grid.columnconfigure(1, weight=1)
        
        # Create a button for each move in a 2x2 grid
        move_buttons = []
        for i, move in enumerate(self.player_pokemon.moves):
            row = i // 2
            col = i % 2
            
            move_button = tk.Button(
                move_grid,
                text=f"{move.name}\n({move.type})\n{move.current_pp}/{move.max_pp} PP",
                font=self.normal_font,
                command=lambda m=move, btn_idx=i: self.execute_player_move(
                    m, log_text, opponent_hp_bar, opponent_hp_label, 
                    player_hp_bar, player_hp_label, turn_label, status_label,
                    animation_canvas, player_pokemon_oval, opponent_pokemon_oval,
                    move_buttons
                ),
                width=15,
                height=3,
                wraplength=120,
                justify=tk.CENTER
            )
            move_button.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")
            move_buttons.append(move_button)
        
        # Save references to update later
        self.battle_widgets = {
            'turn_label': turn_label,
            'status_label': status_label,
            'opponent_hp_bar': opponent_hp_bar,
            'opponent_hp_label': opponent_hp_label,
            'player_hp_bar': player_hp_bar,
            'player_hp_label': player_hp_label,
            'log_text': log_text,
            'animation_canvas': animation_canvas,
            'player_pokemon_oval': player_pokemon_oval,
            'opponent_pokemon_oval': opponent_pokemon_oval,
            'move_buttons': move_buttons
        }
    
    def get_type_color(self, type_name):
        """Get a color for a Pokémon type"""
        type_colors = {
            "Normal": "#A8A878",
            "Fire": "#F08030",
            "Water": "#6890F0",
            "Electric": "#F8D030",
            "Grass": "#78C850",
            "Ice": "#98D8D8",
            "Fighting": "#C03028",
            "Poison": "#A040A0",
            "Ground": "#E0C068",
            "Flying": "#A890F0",
            "Psychic": "#F85888",
            "Bug": "#A8B820",
            "Rock": "#B8A038",
            "Ghost": "#705898",
            "Dragon": "#7038F8",
            "Dark": "#705848",
            "Steel": "#B8B8D0",
            "Fairy": "#EE99AC"
        }
        return type_colors.get(type_name, "#A8A878")  # Default to Normal type color
    
    def execute_player_move(self, move, log_text, opponent_hp_bar, opponent_hp_label, 
                           player_hp_bar, player_hp_label, turn_label, status_label,
                           animation_canvas, player_pokemon_oval, opponent_pokemon_oval,
                           move_buttons):
        """Execute the player's move"""
        if not self.battle_in_progress or self.animation_in_progress:
            return
        
        # Update status
        status_label.config(text=f"You used {move.name}!", fg="green")
        
        # Enable editing of log
        log_text.config(state=tk.NORMAL)
        
        # Use the move
        if move.use():
            log_text.insert(tk.END, f"\nYou used {move.name}!\n")
            
            # Update move button text to show updated PP
            for i, m in enumerate(self.player_pokemon.moves):
                if m == move:
                    move_buttons[i].config(text=f"{move.name}\n({move.type})\n{move.current_pp}/{move.max_pp} PP")
            
            # Animate the attack
            self.animate_attack(
                animation_canvas, 
                player_pokemon_oval, 
                opponent_pokemon_oval, 
                move,
                is_player_attacking=True
            )
            
            # Execute the move
            old_hp = self.opponent_pokemon.current_hp
            self.battle.execute_move(move, self.player_pokemon, self.opponent_pokemon)
            damage_dealt = old_hp - self.opponent_pokemon.current_hp
            
            # Show damage feedback
            if damage_dealt > 0:
                log_text.insert(tk.END, f"It dealt {damage_dealt} damage!\n")
                
                # Gradually update opponent HP for visual effect
                current_hp_percent = (old_hp / self.opponent_pokemon.max_hp) * 100
                target_hp_percent = (self.opponent_pokemon.current_hp / self.opponent_pokemon.max_hp) * 100
                
                def update_hp_bar(current, target, step=0, max_steps=10):
                    try:
                        if not opponent_hp_bar.winfo_exists():
                            return  # Widget no longer exists
                            
                        if step < max_steps and current > target:
                            new_value = current - ((current - target) / max_steps)
                            opponent_hp_bar['value'] = new_value
                            self.root.after(50, lambda: update_hp_bar(new_value, target, step + 1, max_steps))
                        else:
                            opponent_hp_bar['value'] = target
                            if opponent_hp_label.winfo_exists():
                                opponent_hp_label.config(text=f"HP: {self.opponent_pokemon.current_hp}/{self.opponent_pokemon.max_hp}")
                            
                            # Check if battle is over
                            if self.opponent_pokemon.is_fainted():
                                if log_text.winfo_exists():
                                    log_text.insert(tk.END, f"\nThe wild {self.opponent_pokemon.name} fainted! You won!\n")
                                if status_label.winfo_exists():
                                    status_label.config(text=f"Victory! {self.opponent_pokemon.name} fainted!", fg="blue")
                                self.battle_in_progress = False
                                self.show_battle_end(True)
                                if log_text.winfo_exists():
                                    log_text.config(state=tk.DISABLED)
                                    log_text.see(tk.END)
                                return
                            
                            # If battle continues, let opponent take their turn
                            self.root.after(1000, lambda: self.opponent_turn(
                                log_text, opponent_hp_bar, opponent_hp_label, 
                                player_hp_bar, player_hp_label, turn_label, status_label,
                                animation_canvas, player_pokemon_oval, opponent_pokemon_oval
                            ))
                    except tk.TclError:
                        # Handle case where widget was destroyed
                        pass
                
                update_hp_bar(current_hp_percent, target_hp_percent)
            else:
                # If no damage was dealt (missed or ineffective)
                opponent_hp_label.config(text=f"HP: {self.opponent_pokemon.current_hp}/{self.opponent_pokemon.max_hp}")
                
                # Let opponent take their turn
                self.root.after(1000, lambda: self.opponent_turn(
                    log_text, opponent_hp_bar, opponent_hp_label, 
                    player_hp_bar, player_hp_label, turn_label, status_label,
                    animation_canvas, player_pokemon_oval, opponent_pokemon_oval
                ))
        else:
            log_text.insert(tk.END, f"\nNo PP left for {move.name}!\n")
            status_label.config(text=f"No PP left for {move.name}!", fg="red")
            log_text.config(state=tk.DISABLED)
            return
    
    def opponent_turn(self, log_text, opponent_hp_bar, opponent_hp_label, 
                     player_hp_bar, player_hp_label, turn_label, status_label,
                     animation_canvas, player_pokemon_oval, opponent_pokemon_oval):
        """Execute the opponent's turn"""
        if not self.battle_in_progress:
            return
        
        # Enable editing of log
        log_text.config(state=tk.NORMAL)
        
        # AI chooses a random move
        available_moves = [m for m in self.opponent_pokemon.moves if m.current_pp > 0]
        
        if not available_moves:
            log_text.insert(tk.END, f"\nWild {self.opponent_pokemon.name} has no moves left!\n")
            status_label.config(text=f"{self.opponent_pokemon.name} has no moves left!", fg="blue")
            
            # Update turn counter
            self.battle.turn += 1
            turn_label.config(text=f"Turn {self.battle.turn + 1}")
            
            # Disable editing of log
            log_text.config(state=tk.DISABLED)
            log_text.see(tk.END)
            return
        
        opponent_move = random.choice(available_moves)
        log_text.insert(tk.END, f"\nWild {self.opponent_pokemon.name} used {opponent_move.name}!\n")
        status_label.config(text=f"Wild {self.opponent_pokemon.name} used {opponent_move.name}!", fg="red")
        
        # Animate the attack
        self.animate_attack(
            animation_canvas, 
            opponent_pokemon_oval, 
            player_pokemon_oval, 
            opponent_move,
            is_player_attacking=False
        )
        
        # Use the move
        opponent_move.use()
        old_hp = self.player_pokemon.current_hp
        self.battle.execute_move(opponent_move, self.opponent_pokemon, self.player_pokemon)
        damage_dealt = old_hp - self.player_pokemon.current_hp
        
        # Show damage feedback
        if damage_dealt > 0:
            log_text.insert(tk.END, f"It dealt {damage_dealt} damage!\n")
            
            # Gradually update player HP for visual effect
            current_hp_percent = (old_hp / self.player_pokemon.max_hp) * 100
            target_hp_percent = (self.player_pokemon.current_hp / self.player_pokemon.max_hp) * 100
            
            def update_hp_bar(current, target, step=0, max_steps=10):
                try:
                    if not player_hp_bar.winfo_exists():
                        return  # Widget no longer exists
                        
                    if step < max_steps and current > target:
                        new_value = current - ((current - target) / max_steps)
                        player_hp_bar['value'] = new_value
                        self.root.after(50, lambda: update_hp_bar(new_value, target, step + 1, max_steps))
                    else:
                        player_hp_bar['value'] = target
                        if player_hp_label.winfo_exists():
                            player_hp_label.config(text=f"HP: {self.player_pokemon.current_hp}/{self.player_pokemon.max_hp}")
                        
                        # Check if battle is over
                        if self.player_pokemon.is_fainted():
                            if log_text.winfo_exists():
                                log_text.insert(tk.END, f"\nYour {self.player_pokemon.name} fainted! You lost!\n")
                            if status_label.winfo_exists():
                                status_label.config(text=f"Defeat! Your {self.player_pokemon.name} fainted!", fg="red")
                            self.battle_in_progress = False
                            self.show_battle_end(False)
                            if log_text.winfo_exists():
                                log_text.config(state=tk.DISABLED)
                                log_text.see(tk.END)
                            return
                        
                        # Update turn counter
                        self.battle.turn += 1
                        if turn_label.winfo_exists():
                            turn_label.config(text=f"Turn {self.battle.turn + 1}")
                        
                        # Reset status for next turn
                        if status_label.winfo_exists():
                            status_label.config(text="Your turn! Choose your move.", fg="blue")
                        
                        # Disable editing of log
                        if log_text.winfo_exists():
                            log_text.config(state=tk.DISABLED)
                            log_text.see(tk.END)
                except tk.TclError:
                    # Handle case where widget was destroyed
                    pass
            
            update_hp_bar(current_hp_percent, target_hp_percent)
        else:
            # If no damage was dealt (missed or ineffective)
            player_hp_label.config(text=f"HP: {self.player_pokemon.current_hp}/{self.player_pokemon.max_hp}")
            
            # Update turn counter
            self.battle.turn += 1
            turn_label.config(text=f"Turn {self.battle.turn + 1}")
            
            # Reset status for next turn
            status_label.config(text="Your turn! Choose your move.", fg="blue")
            
            # Disable editing of log
            log_text.config(state=tk.DISABLED)
            log_text.see(tk.END)
    
    def animate_attack(self, canvas, attacker_oval, defender_oval, move, is_player_attacking=True):
        """Animate an attack"""
        try:
            if not canvas.winfo_exists():
                return  # Canvas no longer exists
                
            self.animation_in_progress = True
            
            # Get original positions
            attacker_coords = canvas.coords(attacker_oval)
            defender_coords = canvas.coords(defender_oval)
            
            attacker_x = (attacker_coords[0] + attacker_coords[2]) / 2
            attacker_y = (attacker_coords[1] + attacker_coords[3]) / 2
            
            # Create move effect (a colored circle)
            move_color = self.get_type_color(move.type)
            effect = canvas.create_oval(
                attacker_x - 10, attacker_y - 10,
                attacker_x + 10, attacker_y + 10,
                fill=move_color, outline="white", width=2
            )
            
            # Determine direction of movement
            direction = 1 if is_player_attacking else -1
            
            # Animation steps
            def animate_step(step=0, max_steps=20):
                try:
                    if not canvas.winfo_exists():
                        return  # Canvas no longer exists
                        
                    if step < max_steps:
                        # Move the effect toward the defender
                        canvas.move(effect, direction * 20, direction * -2)
                        
                        # Schedule the next step
                        self.root.after(30, lambda: animate_step(step + 1, max_steps))
                    else:
                        # Flash the defender to indicate hit
                        original_fill = canvas.itemcget(defender_oval, "fill")
                        canvas.itemconfig(defender_oval, fill="white")
                        
                        # Shake the defender
                        for i in range(5):
                            canvas.move(defender_oval, 5 if i % 2 == 0 else -5, 0)
                            self.root.update()
                            time.sleep(0.05)
                        
                        # Reset defender position and color
                        canvas.coords(defender_oval, defender_coords)
                        canvas.itemconfig(defender_oval, fill=original_fill)
                        
                        # Delete the effect
                        canvas.delete(effect)
                        
                        # Animation is complete
                        self.animation_in_progress = False
                except tk.TclError:
                    # Handle case where widget was destroyed
                    self.animation_in_progress = False
            
            # Start the animation
            animate_step()
        except tk.TclError:
            # Handle case where widget was destroyed
            self.animation_in_progress = False

    def show_battle_end(self, player_won):
        """Show battle end dialog"""
        if player_won:
            message = f"Congratulations! You defeated the wild {self.opponent_pokemon.name}!"
            title = "Victory!"
        else:
            message = f"Your {self.player_pokemon.name} fainted! Better luck next time."
            title = "Defeat!"
            
        # Ask if player wants to play again
        play_again = messagebox.askyesno(
            title=title,
            message=message + "\n\nWould you like to battle again?"
        )
        
        if play_again:
            self.show_starter_selection()
        else:
            self.show_title_screen()

def main():
    root = tk.Tk()
    app = PokemonBattleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 