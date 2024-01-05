try:
    from math import floor
    from random import choice

    from dsbg_characters import mean_soul_cost, soulCost
    from dsbg_utility import log


    treasures = {
        "Adventurer's Armour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 14, "dexterity": 22, "intelligence": 14, "faith": 0},
        "Alonne Captain Armour": {"expansions": set(["Iron Keep"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 25, "dexterity": 0, "intelligence": 25, "faith": 0},
        "Alonne Greatbow": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 20, "intelligence": 0, "faith": 0},
        "Alonne Knight Armour": {"expansions": set(["Iron Keep"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 0, "intelligence": 20, "faith": 0},
        "Alva Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Assassin", "encounterLevels": set([2,3,4]), "strength": 24, "dexterity": 38, "intelligence": 24, "faith": 0},
        "Antiquated Robes": {"expansions": set(["Darkroot"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 20},
        "Archdeacon Robe": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "armor", "character": "Cleric", "encounterLevels": set([2,3,4]), "strength": 17, "dexterity": 0, "intelligence": 0, "faith": 35},
        "Atonement": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([2,3,4]), "strength": 25, "dexterity": 0, "intelligence": 0, "faith": 25},
        "Aural Decoy": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 22, "faith": 0},
        "Balder Side Sword": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([2,3,4]), "strength": 33, "dexterity": 23, "intelligence": 0, "faith": 0},
        "Bellowing Dragoncrest Ring": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Sorcerer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 30, "faith": 15},
        "Binoculars": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Deprived", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 20, "faith": 20},
        "Black Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 20, "intelligence": 20, "faith": 0},
        "Black Bow of Pharis": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 33, "intelligence": 0, "faith": 0},
        "Black Firebombs": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 20, "faith": 20},
        "Black Hand Armour (Thief)": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "armor", "character": "Thief", "encounterLevels": set([1,2]), "strength": 20, "dexterity": 20, "intelligence": 0, "faith": 0},
        "Black Hand Armour (non-Theif)": {"expansions": set(["Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 20, "intelligence": 20, "faith": 0},
        "Black Iron Armour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 18, "dexterity": 0, "intelligence": 0, "faith": 12},
        "Black Iron Greatshield": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "encounterLevels": set([2,3,4]), "strength": 27, "dexterity": 37, "intelligence": 17, "faith": 0},
        "Black Knight Armour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 26, "dexterity": 16, "intelligence": 0, "faith": 16},
        "Black Knight Greataxe": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 0, "intelligence": 20, "faith": 20},
        "Black Knight Shield": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "encounterLevels": set([2,3,4]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 20},
        "Black Knight Sword": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 23, "intelligence": 0, "faith": 0},
        "Black Leather Armour": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Mercenary", "encounterLevels": set([1,2]), "strength": 24, "dexterity": 30, "intelligence": 0, "faith": 0},
        "Blacksteel Katana": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 23, "intelligence": 0, "faith": 0},
        "Blessed Gem": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 25},
        "Blood Gem": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 15, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Bloodshield": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 16},
        "Blue Tearstone Ring": {"expansions": set(["Dark Souls The Board Game"]), "type": "upgrade", "character": "Knight", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 25, "intelligence": 0, "faith": 25},
        "Bonewheel Shield": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 25, "dexterity": 15, "intelligence": 0, "faith": 0},
        "Bountiful Light": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 35},
        "Bountiful Sunlight": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 20, "faith": 35},
        "Brass Armour": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Deprived", "encounterLevels": set([1,2]), "strength": 25, "dexterity": 0, "intelligence": 0, "faith": 20},
        "Brigand Axe": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 19, "dexterity": 0, "intelligence": 16, "faith": 0},
        "Broadsword": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "encounterLevels": set([1,2]), "strength": 30, "dexterity": 28, "intelligence": 0, "faith": 0},
        "Broken Straight Sword": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "encounterLevels": set([1,2]), "strength": 20, "dexterity": 20, "intelligence": 0, "faith": 0},
        "Buckler": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 20, "intelligence": 10, "faith": 0},
        "Caestus": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 0},
        "Carthus Curved Greatsword": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 30, "intelligence": 19, "faith": 0},
        "Carthus Curved Sword": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 35, "intelligence": 25, "faith": 0},
        "Carthus Flame Arc": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgrade", "character": "Pyromancer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 30, "faith": 0},
        "Carthus Milkring": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Deprived", "encounterLevels": set([2,3,4]), "strength": 24, "dexterity": 30, "intelligence": 0, "faith": 0},
        "Catarina Armour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 22, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Cathedral Knight Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Herald", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 18, "faith": 22},
        "Chloranthy Ring": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 18, "dexterity": 18, "intelligence": 18, "faith": 18},
        "Claws": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 20, "intelligence": 20, "faith": 0},
        "Claymore": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 30, "dexterity": 26, "intelligence": 0, "faith": 0},
        "Cleric Armour": {"expansions": set(["Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 24},
        "Cleric's Candlestick": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 21, "intelligence": 0, "faith": 29},
        "Composite Bow": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([1,2]), "strength": 15, "dexterity": 21, "intelligence": 0, "faith": 0},
        "Cornyx's Robes": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "armor", "character": "Pyromancer", "encounterLevels": set([1,2]), "strength": 21, "dexterity": 0, "intelligence": 21, "faith": 0},
        "Court Sorcerer Robes": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 17, "intelligence": 22, "faith": 0},
        "Covetous Gold Serpent Ring": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgrade", "character": "Thief", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 30, "intelligence": 25, "faith": 0},
        "Covetous Silver Serpent Ring": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgrade", "character": "Thief", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 31, "intelligence": 27, "faith": 0},
        "Crescent Moon Sword": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 17, "intelligence": 0, "faith": 17},
        "Cresent Axe": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 22, "dexterity": 17, "intelligence": 0, "faith": 15},
        "Crest Shield": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "encounterLevels": set([1,2]), "strength": 16, "dexterity": 22, "intelligence": 0, "faith": 0},
        "Crimson Robes": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 12, "intelligence": 22, "faith": 12},
        "Crystal Gem": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 25, "faith": 0},
        "Crystal Hail": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 25, "intelligence": 35, "faith": 0},
        "Crystal Magic Weapon": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Sorcerer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 30, "faith": 0},
        "Crystal Shield": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 18, "dexterity": 0, "intelligence": 0, "faith": 28},
        "Crystal Straight Sword": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 30, "intelligence": 21, "faith": 0},
        "Dark Armour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 20, "intelligence": 20, "faith": 0},
        "Dark Wood Grain Ring": {"expansions": set(["Explorers"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 26, "intelligence": 0, "faith": 0},
        "Deacon Robes": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 24},
        "Demon Titanite": {"expansions": set(["Painted World of Ariamis"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 10, "faith": 10},
        "Divine Blessing": {"expansions": set(["Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 22},
        "Dragon Crest Shield": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 21, "dexterity": 0, "intelligence": 0, "faith": 21},
        "Dragon Scale": {"expansions": set(["Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 10, "dexterity": 0, "intelligence": 0, "faith": 10},
        "Dragonrider Bow": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 34, "intelligence": 0, "faith": 0},
        "Dragonscale Armour": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Sorcerer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 23, "intelligence": 23, "faith": 0},
        "Dragonslayer Greatbow": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 23, "dexterity": 23, "intelligence": 0, "faith": 0},
        "Dragonslayer's Axe": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 15, "intelligence": 15, "faith": 15},
        "Drang Armour": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 18, "dexterity": 14, "intelligence": 0, "faith": 0},
        "Drang Hammers": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "encounterLevels": set([2,3,4]), "strength": 33, "dexterity": 35, "intelligence": 0, "faith": 0},
        "Dung Pie": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Dusk Crown Ring": {"expansions": set(["Darkroot"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 30, "faith": 0},
        "East-West Shield": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 28, "faith": 0},
        "Eastern Armour": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Mercenary", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 36, "intelligence": 26, "faith": 0},
        "Eastern Iron Shield": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 28, "intelligence": 0, "faith": 0},
        "Effigy Shield": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 10, "dexterity": 0, "intelligence": 0, "faith": 10},
        "Elite Knight Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Knight", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 15},
        "Elkhorn Round Shield": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([2,3,4]), "strength": 16, "dexterity": 34, "intelligence": 16, "faith": 0},
        "Embraced Armour of Favour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 13, "dexterity": 0, "intelligence": 0, "faith": 23},
        "Exile Armour": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 26, "dexterity": 0, "intelligence": 0, "faith": 16},
        "Exile Greatsword": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Falchion": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "encounterLevels": set([2,3,4]), "strength": 37, "dexterity": 30, "intelligence": 0, "faith": 23},
        "Fallen Knight Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Warrior", "encounterLevels": set([2,3,4]), "strength": 30, "dexterity": 0, "intelligence": 22, "faith": 0},
        "Faraam Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Knight", "encounterLevels": set([2,3,4]), "strength": 29, "dexterity": 0, "intelligence": 19, "faith": 0},
        "Faron Flashsword": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Sorcerer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 25, "faith": 15},
        "Fire Surge": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([1,2]), "strength": 22, "dexterity": 0, "intelligence": 26, "faith": 0},
        "Fire Whip": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 34, "faith": 18},
        "Fireball": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 23, "faith": 0},
        "Firebombs": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 15},
        "Firelink Armour": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 0, "intelligence": 15, "faith": 0},
        "Flameberge": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 35, "intelligence": 0, "faith": 0},
        "Force": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 12, "faith": 0},
        "Four-Pronged Plow": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 23, "dexterity": 0, "intelligence": 0, "faith": 23},
        "Giant's Halberd": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 27, "dexterity": 0, "intelligence": 0, "faith": 23},
        "Gold-Hemmed Black Robes": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 14, "intelligence": 14, "faith": 14},
        "Golden Ritual Spear": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 24, "faith": 21},
        "Golden Wing Crest Shield": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([1,2]), "strength": 26, "dexterity": 0, "intelligence": 0, "faith": 26},
        "Grass Crest Shield": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([2,3,4]), "strength": 28, "dexterity": 0, "intelligence": 0, "faith": 28},
        "Great Chaos Fireball": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 37, "faith": 27},
        "Great Club": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Great Combustion": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 26, "faith": 22},
        "Great Heal": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 40},
        "Great Mace": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 21, "dexterity": 0, "intelligence": 0, "faith": 28},
        "Great Machete": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([2,3,4]), "strength": 40, "dexterity": 35, "intelligence": 0, "faith": 0},
        "Great Magic Weapon": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 12, "faith": 12},
        "Great Scythe": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 32, "dexterity": 21, "intelligence": 0, "faith": 0},
        "Great Swamp Ring": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgrade", "character": "Pyromancer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 15, "intelligence": 20, "faith": 0},
        "Great Wooden Hammer": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([1,2]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Greataxe": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 32, "dexterity": 22, "intelligence": 0, "faith": 0},
        "Guardian Armour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 22, "intelligence": 22, "faith": 0},
        "Halberd": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 18, "dexterity": 0, "intelligence": 0, "faith": 31},
        "Hard Leather Armour": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 26, "dexterity": 26, "intelligence": 26, "faith": 0},
        "Havel's Armour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 23, "dexterity": 0, "intelligence": 23, "faith": 0},
        "Havel's Greatshield": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 35, "dexterity": 0, "intelligence": 13, "faith": 13},
        "Hawkwood's Shield": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "encounterLevels": set([2,3,4]), "strength": 23, "dexterity": 33, "intelligence": 0, "faith": 23},
        "Heal": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 23},
        "Heal Aid": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 13},
        "Heavy Gem": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 25, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Hollow Gem": {"expansions": set(["Darkroot"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 15},
        "Hollow Soldier Shield": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 16, "dexterity": 0, "intelligence": 0, "faith": 19},
        "Homing Crystal Soulmass": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 40, "faith": 0},
        "Hornet Ring": {"expansions": set(["Dark Souls The Board Game"]), "type": "upgrade", "character": "Assassin", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 30, "intelligence": 0, "faith": 0},
        "Hunter Armour": {"expansions": set(["Darkroot"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 34, "intelligence": 17, "faith": 0},
        "Immolation Tinder": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 28, "faith": 21},
        "Knight Slayer's Ring": {"expansions": set(["Dark Souls The Board Game"]), "type": "upgrade", "character": "Warrior", "encounterLevels": set([1,2]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Kukris": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 15, "intelligence": 0, "faith": 0},
        "Large Leather Shield": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "encounterLevels": set([2,3,4]), "strength": 17, "dexterity": 33, "intelligence": 0, "faith": 0},
        "Life Ring": {"expansions": set(["Iron Keep"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 30},
        "Lightning Gem": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 0},
        "Longbow": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 18, "intelligence": 0, "faith": 0},
        "Lothric Knight Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Knight", "encounterLevels": set([1,2]), "strength": 21, "dexterity": 0, "intelligence": 0, "faith": 15},
        "Lothric Knight Greatsword": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 20, "intelligence": 13, "faith": 13},
        "Lothric's Holy Sword": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([1,2]), "strength": 27, "dexterity": 0, "intelligence": 0, "faith": 31},
        "Lucerne": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 31, "intelligence": 31, "faith": 0},
        "Magic Barrier": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 12, "faith": 24},
        "Magic Shield": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 27, "faith": 14},
        "Magic Stoneplate Ring": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgrade", "character": "Cleric", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 32},
        "Man Serpent Hatchet": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 34, "intelligence": 0, "faith": 0},
        "Mannikin Claws": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 24, "intelligence": 24, "faith": 0},
        "Mask of the Child": {"expansions": set(["Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 19, "faith": 13},
        "Master's Attire": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 30, "intelligence": 18, "faith": 0},
        "Med Heal": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 30},
        "Mirrah Armour": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Deprived", "encounterLevels": set([2,3,4]), "strength": 27, "dexterity": 0, "intelligence": 0, "faith": 27},
        "Morion Blade": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 24, "dexterity": 24, "intelligence": 0, "faith": 0},
        "Morne's Great Hammer": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 35},
        "Morning Star": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 16, "dexterity": 0, "intelligence": 0, "faith": 19},
        "Murakumo": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 27, "intelligence": 17, "faith": 0},
        "Obscuring Ring": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgrade", "character": "Thief", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 28, "intelligence": 0, "faith": 20},
        "Old Ironclad Armour": {"expansions": set(["Iron Keep"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 34, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Onikiri And Ubadachi": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 36, "intelligence": 26, "faith": 0},
        "Painting Guardian Armour": {"expansions": set(["Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 32, "intelligence": 14, "faith": 0},
        "Painting Guardian Curved Sword": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 26, "intelligence": 26, "faith": 26},
        "Paladin Armour": {"expansions": set(["Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 24, "dexterity": 24, "intelligence": 0, "faith": 24},
        "Parrying Dagger": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 21, "intelligence": 21, "faith": 21},
        "Partizan": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([2,3,4]), "strength": 28, "dexterity": 17, "intelligence": 0, "faith": 35},
        "Phoenix Parma Shield": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 20},
        "Pierce Shield": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 16, "dexterity": 10, "intelligence": 0, "faith": 0},
        "Pike": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 23, "dexterity": 0, "intelligence": 0, "faith": 23},
        "Poison Gem": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 15, "intelligence": 0, "faith": 0},
        "Poison Mist": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 11, "intelligence": 16, "faith": 0},
        "Poison Throwing Knives": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 14, "intelligence": 14, "faith": 0},
        "Porcine Shield": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 24, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Rapier": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 21, "intelligence": 21, "faith": 0},
        "Rapport": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 36, "faith": 0},
        "Raw Gem": {"expansions": set(["Explorers"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Red and White Round Shield": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 22, "faith": 10},
        "Red Tearstone Ring": {"expansions": set(["Painted World of Ariamis"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 20},
        "Reinforced Club": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 23, "dexterity": 0, "intelligence": 0, "faith": 16},
        "Replenishment": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 25},
        "Ring of Favour": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Mercenary", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 21, "intelligence": 0, "faith": 21},
        "Rotten Ghru Dagger": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 17, "intelligence": 17, "faith": 0},
        "Rotten Ghru Spear": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 21, "intelligence": 12, "faith": 0},
        "Royal Dirk": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 31, "intelligence": 0, "faith": 31},
        "Sacred Oath": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 14, "faith": 30},
        "Saint Bident": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 35},
        "Scimitar": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 20, "intelligence": 18, "faith": 0},
        "Shadow Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Assassin", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 34, "intelligence": 0, "faith": 17},
        "Sharp Gem": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 25, "intelligence": 0, "faith": 0},
        "Shortsword": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 15, "dexterity": 23, "intelligence": 0, "faith": 0},
        "Shotel": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 29, "intelligence": 26, "faith": 0},
        "Silver Eagle Kite Shield": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 15, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Silver Knight Armour": {"expansions": set(["Explorers"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 26, "dexterity": 26, "intelligence": 0, "faith": 0},
        "Silver Knight Shield": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([1,2]), "strength": 31, "dexterity": 23, "intelligence": 0, "faith": 0},
        "Silver Knight Spear": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 22, "intelligence": 0, "faith": 26},
        "Silver Knight Straight Sword": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 20, "intelligence": 20, "faith": 20},
        "Simple Gem": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 15},
        "Skull Lantern": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 13, "intelligence": 14, "faith": 0},
        "Small Leather Shield": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "encounterLevels": set([1,2]), "strength": 15, "dexterity": 30, "intelligence": 0, "faith": 15},
        "Sorcerer's Staff": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 15, "dexterity": 0, "intelligence": 30, "faith": 0},
        "Soul Arrow": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 16, "faith": 0},
        "Soul Greatsword": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 35, "faith": 15},
        "Soul Spear": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 25, "faith": 15},
        "Soulstream": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 22, "faith": 0},
        "Spider Shield": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "encounterLevels": set([1,2]), "strength": 27, "dexterity": 0, "intelligence": 15, "faith": 0},
        "Spiked Mace": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([1,2]), "strength": 32, "dexterity": 0, "intelligence": 0, "faith": 22},
        "Spotted Whip": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 30, "intelligence": 23, "faith": 0},
        "Stone Greataxe": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Stone Greatshield": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Stone Greatsword": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 22, "dexterity": 0, "intelligence": 0, "faith": 22},
        "Stone Knight Armour": {"expansions": set(["Darkroot"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Stone Parama": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([2,3,4]), "strength": 15, "dexterity": 0, "intelligence": 35, "faith": 0},
        "Sun Princess Ring": {"expansions": set(["Dark Souls The Board Game"]), "type": "upgrade", "character": "Knight", "encounterLevels": set([1,2]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 25},
        "Sunless Armour": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 13, "dexterity": 0, "intelligence": 0, "faith": 13},
        "Sunlight Shield": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 30},
        "Sunset Armour": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 0, "intelligence": 0, "faith": 24},
        "Sunset Shield": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([1,2]), "strength": 15, "dexterity": 0, "intelligence": 0, "faith": 20},
        "Thorolund Talisman": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 31},
        "Thrall Axe": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 16, "dexterity": 16, "intelligence": 0, "faith": 0},
        "Throwing Knives": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 14, "intelligence": 12, "faith": 0},
        "Tiny Being's Ring": {"expansions": set(["Dark Souls The Board Game"]), "type": "upgrade", "character": "Herald", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 20},
        "Torch": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
        "Twin Dragon Greatshield": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 35, "intelligence": 15, "faith": 15},
        "Ughigatana": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 32, "intelligence": 0, "faith": 14},
        "Umbral Dagger": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 35, "intelligence": 35, "faith": 0},
        "Velka's Rapier": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 19, "intelligence": 27, "faith": 0},
        "Warden Twinblades": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "encounterLevels": set([1,2]), "strength": 17, "dexterity": 25, "intelligence": 17, "faith": 0},
        "Warpick": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 25, "intelligence": 0, "faith": 0},
        "Winged Spear": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 0, "intelligence": 0, "faith": 22},
        "Witch's Lock": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 31, "faith": 0},
        "Wolf Ring": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Mercenary", "encounterLevels": set([2,3,4]), "strength": 25, "dexterity": 35, "intelligence": 25, "faith": 0},
        "Worker Armour": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 12, "dexterity": 12, "intelligence": 12, "faith": 12},
        "Xanthous Robes": {"expansions": set(["Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 23, "faith": 20},
        "Zweihander": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 35, "dexterity": 25, "intelligence": 0, "faith": 0},
    }

    treasureSwapEncounters = {
        "Castle Break In": "Dragonslayer Greatbow",
        "Corvian Host": "Bloodshield",
        "Dark Resurrection": "Fireball",
        "Distant Tower": "Velka's Rapier",
        "Flooded Fortress": "Adventurer's Armour",
        "Frozen Revolutions": "Red Tearstone Ring",
        "Giant's Coffin": "Black Knight Greataxe",
        "Grave Matters": "Firebombs",
        "Hanging Rafters": "Dark Wood Grain Ring",
        "In Deep Water": "Thorolund Talisman",
        "Inhospitable Ground": "Pike",
        "Monstrous Maw": "Exile Greatsword",
        "No Safe Haven": "Throwing Knives",
        "Painted Passage": "Painting Guardian Armour",
        "Parish Church": "Titanite Shard",
        "Puppet Master": "Skull Lantern",
        "Rain of Filth": "Poison Mist",
        "Shattered Keep": "Poison Throwing Knives",
        "The Abandoned Chest": "Chloranthy Ring",
        "The Beast From the Depths": "Mask of the Child",
        "The Iron Golem": "Giant's Halberd",
        "The Locked Grave": "Dragon Scale",
        "The Skeleton Ball": "Divine Blessing",
        "Trophy Room": "Havel's Greatshield",
        "Undead Sanctum": "Silver Knight Straight Sword",
        "Unseen Scurrying": "Kukris",
        "Urns of the Fallen": "Bonewheel Shield",
        "Velka's Chosen": "Demon Titanite"
    }

    tiers = {
        "armor": {},
        "weapon": {},
        "upgrade": {}
    }


    def generate_treasure_soul_cost(setsAvailable, charactersActive):
        try:
            log("Start of generate_treasure_soul_cost")

            maxStr = max([len(soulCost[c]["strength"]) for c in charactersActive])
            maxDex = max([len(soulCost[c]["dexterity"]) for c in charactersActive])
            maxInt = max([len(soulCost[c]["intelligence"]) for c in charactersActive])
            maxFai = max([len(soulCost[c]["faith"]) for c in charactersActive])

            for t in [t for t in treasures if not treasures[t]["character"] or treasures[t]["character"] in charactersActive]:
                # Don't attempt to calculate soul cost for items that can't be equipped by anyone in the party.
                if any([
                    treasures[t]["strength"] > maxStr,
                    treasures[t]["dexterity"] > maxDex,
                    treasures[t]["intelligence"] > maxInt,
                    treasures[t]["faith"] > maxFai
                    ]):
                    continue
                treasures[t]["soulCost"] = mean_soul_cost(treasures[t], setsAvailable, charactersActive)

            log("End of generate_treasure_soul_cost")
        except Exception as e:
            log(e, exception=True)
            raise

        
    def populate_treasure_tiers(setsAvailable, charactersActive):
        try:
            log("Start of populate_treasure_tiers")

            # Generate the list of available treasures for each type.
            armor = sorted([t for t in treasures if (
                treasures[t]["type"] == "armor"
                and treasures[t]["expansions"] & setsAvailable
                and (not treasures[t]["character"] or treasures[t]["character"] in charactersActive)
                and "soulCost" in treasures[t])
                ], key=lambda x: treasures[x]["soulCost"])
            armorLen = len(armor)
            weapon = sorted([t for t in treasures if (
                treasures[t]["type"] == "weapon"
                and treasures[t]["expansions"] & setsAvailable
                and (not treasures[t]["character"] or treasures[t]["character"] in charactersActive)
                and "soulCost" in treasures[t])
                ], key=lambda x: treasures[x]["soulCost"])
            weaponLen = len(weapon)
            upgrade = sorted([t for t in treasures if (
                treasures[t]["type"] == "upgrade"
                and treasures[t]["expansions"] & setsAvailable
                and (not treasures[t]["character"] or treasures[t]["character"] in charactersActive)
                and "soulCost" in treasures[t])
                ], key=lambda x: treasures[x]["soulCost"])
            upgradeLen = len(upgrade)

            # Split the treasures into 3 nearly-equal tiers based on soul cost.
            tiers["armor"][1] = armor[:floor(armorLen/3)]
            tiers["armor"][2] = armor[floor(armorLen/3):floor(armorLen/3)*2]
            tiers["armor"][3] = armor[floor(armorLen/3)*2:]

            tiers["weapon"][1] = weapon[:floor(weaponLen/3)]
            tiers["weapon"][2] = weapon[floor(weaponLen/3):floor(weaponLen/3)*2]
            tiers["weapon"][3] = weapon[floor(weaponLen/3)*2:]

            tiers["upgrade"][1] = upgrade[:floor(upgradeLen/3)]
            tiers["upgrade"][2] = upgrade[floor(upgradeLen/3):floor(upgradeLen/3)*2]
            tiers["upgrade"][3] = upgrade[floor(upgradeLen/3)*2:]

            # Push the tier back to the treasure.
            for treasure in treasures:
                if any([treasure in set(tiers["armor"][1]), treasure in set(tiers["weapon"][1]), treasure in set(tiers["upgrade"][1])]):
                    treasures[treasure]["tier"] = 1
                elif any([treasure in set(tiers["armor"][2]), treasure in set(tiers["weapon"][2]), treasure in set(tiers["upgrade"][2])]):
                    treasures[treasure]["tier"] = 2
                else:
                    treasures[treasure]["tier"] = 3

            log("End of populate_treasure_tiers")
        except Exception as e:
            log(e, exception=True)
            raise


    def pick_treasure(treasureSwapOption, swapTreasure, lastPicked, encounterLevel, setsAvailable, charactersActive):
        try:
            log("Start of pick_treasure")

            if treasureSwapOption == "Similar Soul Cost":
                # If the treasure we're swapping out doesn't have a soul cost (because it's not in the active sets),
                # calculate it based on all characters instead of just the active ones.
                if "soulCost" not in treasures[swapTreasure]:
                    treasures[swapTreasure]["soulCost"] = mean_soul_cost(treasures[swapTreasure], setsAvailable, set([c for c in soulCost]))
                alts = []
                extraMod = 0

                # If there are fewer than 2 alternatives, increase the threshold until there are at least 2.
                while len(alts) < 2:
                    characterSoulCost = treasures[swapTreasure]["soulCost"]
                    modifier = 1 + extraMod if characterSoulCost * 0.1 + (extraMod / 10) < 1 else characterSoulCost * 0.1 + (extraMod / 10)
                    lower = characterSoulCost - modifier
                    upper = characterSoulCost + modifier
                    alts += [t for t in treasures if (
                        "soulCost" in treasures[t]
                        and lower <= treasures[t]["soulCost"] <= upper
                        and treasures[t]["type"] == treasures[swapTreasure]["type"]
                        and treasures[t]["expansions"] & setsAvailable
                        and (not treasures[t]["character"] or treasures[t]["character"] in charactersActive)
                        and encounterLevel in treasures[t]["encounterLevels"]
                        and t != lastPicked)]
                    alts = list(set(alts))
                    extraMod += 0.5
            elif treasureSwapOption == "Tier Based":
                alts = [t for t in treasures if (
                    treasures[t]["type"] == treasures[swapTreasure]["type"]
                    and treasures[t]["tier"] == treasures[swapTreasure]["tier"]
                        and encounterLevel in treasures[t]["encounterLevels"]
                    and t != lastPicked)]
            elif treasureSwapOption == "Generic Treasure":
                alts = [str(encounterLevel) + "x Treasure"]
            elif treasureSwapOption == "Original":
                alts = [swapTreasure]

            log("End of pick_treasure")
            return choice(alts)
        except Exception as e:
            log(e, exception=True)
            raise

except Exception as e:
    log(e, exception=True)
    raise