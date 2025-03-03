from pokemon import Pokemon
from move import Move

def create_move_database():
    """Create a database of moves"""
    moves = {}
    
    # Fire moves
    moves["Flamethrower"] = Move("Flamethrower", "Fire", "Special", 90, 100, 15)
    moves["Flamethrower"].set_status_effect("Burn", 10)  # 10% chance to burn
    
    moves["Fire Blast"] = Move("Fire Blast", "Fire", "Special", 110, 85, 5)
    moves["Fire Blast"].set_status_effect("Burn", 30)  # 30% chance to burn
    
    moves["Ember"] = Move("Ember", "Fire", "Special", 40, 100, 25)
    moves["Ember"].set_status_effect("Burn", 10)  # 10% chance to burn
    
    # Water moves
    moves["Hydro Pump"] = Move("Hydro Pump", "Water", "Special", 110, 80, 5)
    
    moves["Surf"] = Move("Surf", "Water", "Special", 90, 100, 15)
    
    moves["Water Gun"] = Move("Water Gun", "Water", "Special", 40, 100, 25)
    
    # Grass moves
    moves["Solar Beam"] = Move("Solar Beam", "Grass", "Special", 120, 100, 10)
    
    moves["Razor Leaf"] = Move("Razor Leaf", "Grass", "Physical", 55, 95, 25)
    
    moves["Vine Whip"] = Move("Vine Whip", "Grass", "Physical", 45, 100, 25)
    
    # Electric moves
    moves["Thunderbolt"] = Move("Thunderbolt", "Electric", "Special", 90, 100, 15)
    moves["Thunderbolt"].set_status_effect("Paralysis", 10)  # 10% chance to paralyze
    
    moves["Thunder"] = Move("Thunder", "Electric", "Special", 110, 70, 10)
    moves["Thunder"].set_status_effect("Paralysis", 30)  # 30% chance to paralyze
    
    moves["Thunder Shock"] = Move("Thunder Shock", "Electric", "Special", 40, 100, 30)
    moves["Thunder Shock"].set_status_effect("Paralysis", 10)  # 10% chance to paralyze
    
    # Normal moves
    moves["Tackle"] = Move("Tackle", "Normal", "Physical", 40, 100, 35)
    
    moves["Quick Attack"] = Move("Quick Attack", "Normal", "Physical", 40, 100, 30)
    
    moves["Hyper Beam"] = Move("Hyper Beam", "Normal", "Special", 150, 90, 5)
    
    # Fighting moves
    moves["Karate Chop"] = Move("Karate Chop", "Fighting", "Physical", 50, 100, 25)
    
    moves["Submission"] = Move("Submission", "Fighting", "Physical", 80, 80, 20)
    
    # Psychic moves
    moves["Psychic"] = Move("Psychic", "Psychic", "Special", 90, 100, 10)
    moves["Psychic"].set_stat_change("sp_defense", -1, 10)  # 10% chance to lower Sp. Def
    
    moves["Confusion"] = Move("Confusion", "Psychic", "Special", 50, 100, 25)
    moves["Confusion"].set_stat_change("sp_defense", -1, 10)  # 10% chance to lower Sp. Def
    
    # Dragon moves
    moves["Dragon Rage"] = Move("Dragon Rage", "Dragon", "Special", 80, 100, 10)
    
    moves["Dragon Breath"] = Move("Dragon Breath", "Dragon", "Special", 60, 100, 20)
    moves["Dragon Breath"].set_status_effect("Paralysis", 30)  # 30% chance to paralyze
    
    # Status moves
    moves["Growl"] = Move("Growl", "Normal", "Status", 0, 100, 40)
    moves["Growl"].set_stat_change("attack", -1, 100)  # 100% chance to lower Attack
    
    moves["Tail Whip"] = Move("Tail Whip", "Normal", "Status", 0, 100, 30)
    moves["Tail Whip"].set_stat_change("defense", -1, 100)  # 100% chance to lower Defense
    
    moves["Leer"] = Move("Leer", "Normal", "Status", 0, 100, 30)
    moves["Leer"].set_stat_change("defense", -1, 100)  # 100% chance to lower Defense
    
    moves["String Shot"] = Move("String Shot", "Bug", "Status", 0, 95, 40)
    moves["String Shot"].set_stat_change("speed", -1, 100)  # 100% chance to lower Speed
    
    moves["Thunder Wave"] = Move("Thunder Wave", "Electric", "Status", 0, 90, 20)
    moves["Thunder Wave"].set_status_effect("Paralysis", 100)  # 100% chance to paralyze
    
    moves["Toxic"] = Move("Toxic", "Poison", "Status", 0, 90, 10)
    moves["Toxic"].set_status_effect("Toxic", 100)  # 100% chance to badly poison
    
    moves["Will-O-Wisp"] = Move("Will-O-Wisp", "Fire", "Status", 0, 85, 15)
    moves["Will-O-Wisp"].set_status_effect("Burn", 100)  # 100% chance to burn
    
    moves["Hypnosis"] = Move("Hypnosis", "Psychic", "Status", 0, 60, 20)
    moves["Hypnosis"].set_status_effect("Sleep", 100)  # 100% chance to sleep
    
    moves["Stun Spore"] = Move("Stun Spore", "Grass", "Status", 0, 75, 30)
    moves["Stun Spore"].set_status_effect("Paralysis", 100)  # 100% chance to paralyze
    
    moves["Sleep Powder"] = Move("Sleep Powder", "Grass", "Status", 0, 75, 15)
    moves["Sleep Powder"].set_status_effect("Sleep", 100)  # 100% chance to sleep
    
    moves["Poison Powder"] = Move("Poison Powder", "Poison", "Status", 0, 75, 35)
    moves["Poison Powder"].set_status_effect("Poison", 100)  # 100% chance to poison
    
    # Accuracy and Evasion modifying moves
    moves["Sand Attack"] = Move("Sand Attack", "Ground", "Status", 0, 100, 15)
    moves["Sand Attack"].set_stat_change("accuracy", -1, 100)  # 100% chance to lower Accuracy
    
    moves["Smokescreen"] = Move("Smokescreen", "Normal", "Status", 0, 100, 20)
    moves["Smokescreen"].set_stat_change("accuracy", -1, 100)  # 100% chance to lower Accuracy
    
    moves["Flash"] = Move("Flash", "Normal", "Status", 0, 100, 20)
    moves["Flash"].set_stat_change("accuracy", -1, 100)  # 100% chance to lower Accuracy
    
    moves["Double Team"] = Move("Double Team", "Normal", "Status", 0, 100, 15)
    moves["Double Team"].set_stat_change("evasion", 1, 100)  # 100% chance to raise Evasion
    
    moves["Minimize"] = Move("Minimize", "Normal", "Status", 0, 100, 10)
    moves["Minimize"].set_stat_change("evasion", 2, 100)  # 100% chance to sharply raise Evasion
    
    # Stat boosting moves
    moves["Swords Dance"] = Move("Swords Dance", "Normal", "Status", 0, 100, 20)
    moves["Swords Dance"].set_stat_change("attack", 2, 100)  # 100% chance to sharply raise Attack
    
    moves["Growth"] = Move("Growth", "Normal", "Status", 0, 100, 40)
    moves["Growth"].set_stat_change("sp_attack", 1, 100)  # 100% chance to raise Sp. Attack
    
    moves["Agility"] = Move("Agility", "Psychic", "Status", 0, 100, 30)
    moves["Agility"].set_stat_change("speed", 2, 100)  # 100% chance to sharply raise Speed
    
    return moves

def create_pokemon_database(move_db):
    """Create a database of Pokemon"""
    pokemon_db = {}
    
    # Starters
    bulbasaur = Pokemon("Bulbasaur", "Grass", "Poison")
    bulbasaur.initialize_stats(45, 49, 49, 65, 65, 45)
    bulbasaur.add_move(move_db["Tackle"])
    bulbasaur.add_move(move_db["Vine Whip"])
    bulbasaur.add_move(move_db["Razor Leaf"])
    bulbasaur.add_move(move_db["Leech Seed"])
    pokemon_db["Bulbasaur"] = bulbasaur
    
    charmander = Pokemon("Charmander", "Fire")
    charmander.initialize_stats(39, 52, 43, 60, 50, 65)
    charmander.add_move(move_db["Scratch"])
    charmander.add_move(move_db["Ember"])
    charmander.add_move(move_db["Flamethrower"])
    charmander.add_move(move_db["Growl"])
    pokemon_db["Charmander"] = charmander
    
    squirtle = Pokemon("Squirtle", "Water")
    squirtle.initialize_stats(44, 48, 65, 50, 64, 43)
    squirtle.add_move(move_db["Tackle"])
    squirtle.add_move(move_db["Water Gun"])
    squirtle.add_move(move_db["Bubble"])
    squirtle.add_move(move_db["Tail Whip"])
    pokemon_db["Squirtle"] = squirtle
    
    # Electric
    pikachu = Pokemon("Pikachu", "Electric")
    pikachu.initialize_stats(35, 55, 40, 50, 50, 90)
    pikachu.add_move(move_db["Thunder Shock"])
    pikachu.add_move(move_db["Quick Attack"])
    pikachu.add_move(move_db["Thunder Wave"])
    pikachu.add_move(move_db["Slam"])
    pokemon_db["Pikachu"] = pikachu
    
    # Normal
    rattata = Pokemon("Rattata", "Normal")
    rattata.initialize_stats(30, 56, 35, 25, 35, 72)
    rattata.add_move(move_db["Tackle"])
    rattata.add_move(move_db["Tail Whip"])
    rattata.add_move(move_db["Quick Attack"])
    rattata.add_move(move_db["Hyper Fang"])
    pokemon_db["Rattata"] = rattata
    
    # Psychic
    abra = Pokemon("Abra", "Psychic")
    abra.initialize_stats(25, 20, 15, 105, 55, 90)
    abra.add_move(move_db["Teleport"])
    abra.add_move(move_db["Confusion"])
    abra.add_move(move_db["Psychic"])
    abra.add_move(move_db["Flash"])
    pokemon_db["Abra"] = abra
    
    # Dragon
    dratini = Pokemon("Dratini", "Dragon")
    dratini.initialize_stats(41, 64, 45, 50, 50, 50)
    dratini.add_move(move_db["Wrap"])
    dratini.add_move(move_db["Leer"])
    dratini.add_move(move_db["Thunder Wave"])
    dratini.add_move(move_db["Dragon Rage"])
    pokemon_db["Dratini"] = dratini
    
    # Add Pokémon with accuracy/evasion moves
    pidgey = Pokemon("Pidgey", "Normal", "Flying")
    pidgey.initialize_stats(40, 45, 40, 35, 35, 56)
    pidgey.add_move(move_db["Tackle"])
    pidgey.add_move(move_db["Gust"])
    pidgey.add_move(move_db["Quick Attack"])
    pidgey.add_move(move_db["Sand Attack"])
    pokemon_db["Pidgey"] = pidgey
    
    gastly = Pokemon("Gastly", "Ghost", "Poison")
    gastly.initialize_stats(30, 35, 30, 100, 35, 80)
    gastly.add_move(move_db["Lick"])
    gastly.add_move(move_db["Confuse Ray"])
    gastly.add_move(move_db["Hypnosis"])
    gastly.add_move(move_db["Smokescreen"])
    pokemon_db["Gastly"] = gastly
    
    koffing = Pokemon("Koffing", "Poison")
    koffing.initialize_stats(40, 65, 95, 60, 45, 35)
    koffing.add_move(move_db["Tackle"])
    koffing.add_move(move_db["Sludge"])
    koffing.add_move(move_db["Smokescreen"])
    koffing.add_move(move_db["Poison Gas"])
    pokemon_db["Koffing"] = koffing
    
    return pokemon_db

# Add some missing moves that were referenced above
def add_missing_moves(move_db):
    move_db["Scratch"] = Move("Scratch", "Normal", "Physical", 40, 100, 35)
    
    move_db["Growl"] = Move("Growl", "Normal", "Status", 0, 100, 40)
    move_db["Growl"].set_stat_change("attack", -1, 100)  # 100% chance to lower Attack
    
    move_db["Tail Whip"] = Move("Tail Whip", "Normal", "Status", 0, 100, 30)
    move_db["Tail Whip"].set_stat_change("defense", -1, 100)  # 100% chance to lower Defense
    
    move_db["Bubble"] = Move("Bubble", "Water", "Special", 40, 100, 30)
    move_db["Bubble"].set_stat_change("speed", -1, 10)  # 10% chance to lower Speed
    
    move_db["Leech Seed"] = Move("Leech Seed", "Grass", "Status", 0, 90, 10)
    # Leech Seed effect would need special handling, simplified for now
    
    move_db["Thunder Wave"] = Move("Thunder Wave", "Electric", "Status", 0, 90, 20)
    move_db["Thunder Wave"].set_status_effect("Paralysis", 100)  # 100% chance to paralyze
    
    move_db["Slam"] = Move("Slam", "Normal", "Physical", 80, 75, 20)
    
    move_db["Hyper Fang"] = Move("Hyper Fang", "Normal", "Physical", 80, 90, 15)
    
    move_db["Teleport"] = Move("Teleport", "Psychic", "Status", 0, 100, 20)
    # Teleport effect would need special handling, simplified for now
    
    move_db["Reflect"] = Move("Reflect", "Psychic", "Status", 0, 100, 20)
    # Reflect effect would need special handling, simplified for now
    
    move_db["Wrap"] = Move("Wrap", "Normal", "Physical", 15, 90, 20)
    # Wrap effect would need special handling, simplified for now
    
    move_db["Leer"] = Move("Leer", "Normal", "Status", 0, 100, 30)
    move_db["Leer"].set_stat_change("defense", -1, 100)  # 100% chance to lower Defense
    
    # Accuracy and Evasion moves
    move_db["Sand Attack"] = Move("Sand Attack", "Ground", "Status", 0, 100, 15)
    move_db["Sand Attack"].set_stat_change("accuracy", -1, 100)  # 100% chance to lower Accuracy
    
    move_db["Double Team"] = Move("Double Team", "Normal", "Status", 0, 100, 15)
    move_db["Double Team"].set_stat_change("evasion", 1, 100)  # 100% chance to raise Evasion
    
    move_db["Smokescreen"] = Move("Smokescreen", "Normal", "Status", 0, 100, 20)
    move_db["Smokescreen"].set_stat_change("accuracy", -1, 100)  # 100% chance to lower Accuracy
    
    move_db["Flash"] = Move("Flash", "Normal", "Status", 0, 100, 20)
    move_db["Flash"].set_stat_change("accuracy", -1, 100)  # 100% chance to lower Accuracy
    
    # Add new moves
    move_db["Gust"] = Move("Gust", "Flying", "Special", 40, 100, 35)
    
    move_db["Lick"] = Move("Lick", "Ghost", "Physical", 30, 100, 30)
    move_db["Lick"].set_status_effect("Paralysis", 30)  # 30% chance to paralyze
    
    move_db["Confuse Ray"] = Move("Confuse Ray", "Ghost", "Status", 0, 100, 10)
    # Confusion effect would need special handling, simplified for now
    
    move_db["Sludge"] = Move("Sludge", "Poison", "Special", 65, 100, 20)
    move_db["Sludge"].set_status_effect("Poison", 30)  # 30% chance to poison
    
    move_db["Poison Gas"] = Move("Poison Gas", "Poison", "Status", 0, 90, 40)
    move_db["Poison Gas"].set_status_effect("Poison", 100)  # 100% chance to poison
    
    return move_db

def get_all_pokemon():
    """Get all available Pokemon"""
    moves = create_move_database()
    moves = add_missing_moves(moves)
    return create_pokemon_database(moves) 