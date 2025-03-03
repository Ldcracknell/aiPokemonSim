# Pokémon Battle Simulator

A Python-based Pokémon battle simulator with a graphical user interface built using Tkinter.

## Features

- Turn-based battle system similar to the classic Pokémon games
- Multiple starter Pokémon to choose from
- Various types of moves (Physical, Special, Status)
- Type effectiveness system
- Status effects (Burn, Poison, Paralysis, Sleep, Freeze)
- Stat modifications
- Special move effects like Leech Seed

## Requirements

- Python 3.6+
- Tkinter (usually comes with Python)
- Colorama (for terminal version)

## How to Run

```bash
python run_game.py
```

## Game Controls

1. Select your starter Pokémon
2. Choose an opponent
3. During battle, click on move buttons to attack
4. Defeat your opponent to win!

## Project Structure

- `src/` - Source code
  - `pokemon.py` - Pokémon class definition
  - `move.py` - Move class definition
  - `battle.py` - Battle logic for terminal version
  - `gui_battle.py` - Battle logic with GUI
  - `pokedex.py` - Pokémon and move databases
- `run_game.py` - Main entry point

## Future Improvements

- More Pokémon and moves
- Items and abilities
- Multiple battles in sequence
- Save/load functionality

## Credits

This is a simplified version of the Pokémon battle system for educational purposes. Pokémon and all related properties are owned by Nintendo, Game Freak, and The Pokémon Company.

## Status Effects

The game includes various status effects that can impact Pokémon during battle:

- **Burn**: Reduces Attack and causes damage each turn
- **Poison**: Causes damage each turn
- **Toxic**: Causes increasing damage each turn
- **Paralysis**: May prevent movement and reduces Speed
- **Sleep**: Prevents movement for a few turns
- **Freeze**: Prevents movement until thawed

## Stat Changes

Moves can also modify a Pokémon's stats during battle:

- Stats can be raised or lowered by different amounts
- Stat changes are visually displayed on the battle screen
- Affected stats include Attack, Defense, Special Attack, Special Defense, Speed, Accuracy, and Evasion
- Stat changes can stack up to +6 or down to -6

### Accuracy and Evasion

The battle system now includes accuracy and evasion modifiers:

- Moves like Sand Attack, Smokescreen, and Flash can lower the opponent's accuracy
- Moves like Double Team and Minimize can raise a Pokémon's evasion
- Accuracy and evasion modifiers affect the chance of moves hitting their target
- The formula uses a 3:3 ratio system similar to the main Pokémon games