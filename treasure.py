from random import choice
from math import floor
from character import mean_soul_cost, soulCost


treasures = {
    "Adventurer's Armour": {"sets": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 14, "dexterity": 22, "intelligence": 14, "faith": 0},
    "Alonne Captain Armour": {"sets": set(["Iron Keep"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 25, "dexterity": 0, "intelligence": 25, "faith": 0},
    "Alonne Greatbow": {"sets": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 20, "intelligence": 0, "faith": 0},
    "Alonne Knight Armour": {"sets": set(["Iron Keep"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 0, "intelligence": 20, "faith": 0},
    "Alva Armour": {"sets": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Assassin", "encounterLevels": set([2,3,4]), "strength": 24, "dexterity": 38, "intelligence": 24, "faith": 0},
    "Antiquated Robes": {"sets": set(["Darkroot"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 20},
    "Archdeacon Robe": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "armor", "character": "Cleric", "encounterLevels": set([2,3,4]), "strength": 17, "dexterity": 0, "intelligence": 0, "faith": 35},
    "Atonement": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([2,3,4]), "strength": 25, "dexterity": 0, "intelligence": 0, "faith": 25},
    "Aural Decoy": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 22, "faith": 0},
    "Balder Side Sword": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([2,3,4]), "strength": 33, "dexterity": 23, "intelligence": 0, "faith": 0},
    "Bellowing Dragoncrest Ring": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Sorcerer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 30, "faith": 15},
    "Binoculars": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Deprived", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 20, "faith": 20},
    "Black Armour": {"sets": set(["Dark Souls The Board Game"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 20, "intelligence": 20, "faith": 0},
    "Black Bow of Pharis": {"sets": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 33, "intelligence": 0, "faith": 0},
    "Black Firebombs": {"sets": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 20, "faith": 20},
    "Black Hand Armour (Thief)": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "armor", "character": "Thief", "encounterLevels": set([1,2]), "strength": 20, "dexterity": 20, "intelligence": 0, "faith": 0},
    "Black Hand Armour (non-Theif)": {"sets": set(["Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 20, "intelligence": 20, "faith": 0},
    "Black Iron Armour": {"sets": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 18, "dexterity": 0, "intelligence": 0, "faith": 12},
    "Black Iron Greatshield": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "encounterLevels": set([2,3,4]), "strength": 27, "dexterity": 37, "intelligence": 17, "faith": 0},
    "Black Knight Armour": {"sets": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 26, "dexterity": 16, "intelligence": 0, "faith": 16},
    "Black Knight Greataxe": {"sets": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 0, "intelligence": 20, "faith": 20},
    "Black Knight Shield": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "encounterLevels": set([2,3,4]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Black Knight Sword": {"sets": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 23, "intelligence": 0, "faith": 0},
    "Black Leather Armour": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Mercenary", "encounterLevels": set([1,2]), "strength": 24, "dexterity": 30, "intelligence": 0, "faith": 0},
    "Blacksteel Katana": {"sets": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 23, "intelligence": 0, "faith": 0},
    "Blessed Gem": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 25},
    "Blood Gem": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 15, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Bloodshield": {"sets": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 16},
    "Blue Tearstone Ring": {"sets": set(["Dark Souls The Board Game"]), "type": "upgrade", "character": "Knight", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 25, "intelligence": 0, "faith": 25},
    "Bonewheel Shield": {"sets": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 25, "dexterity": 15, "intelligence": 0, "faith": 0},
    "Bountiful Light": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 35},
    "Bountiful Sunlight": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 20, "faith": 35},
    "Brass Armour": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Deprived", "encounterLevels": set([1,2]), "strength": 25, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Brigand Axe": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 19, "dexterity": 0, "intelligence": 16, "faith": 0},
    "Broadsword": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "encounterLevels": set([1,2]), "strength": 30, "dexterity": 28, "intelligence": 0, "faith": 0},
    "Broken Straight Sword": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "encounterLevels": set([1,2]), "strength": 20, "dexterity": 20, "intelligence": 0, "faith": 0},
    "Buckler": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 20, "intelligence": 10, "faith": 0},
    "Caestus": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 0},
    "Carthus Curved Greatsword": {"sets": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 30, "intelligence": 19, "faith": 0},
    "Carthus Curved Sword": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 35, "intelligence": 25, "faith": 0},
    "Carthus Flame Arc": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgrade", "character": "Pyromancer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 30, "faith": 0},
    "Carthus Milkring": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Deprived", "encounterLevels": set([2,3,4]), "strength": 24, "dexterity": 30, "intelligence": 0, "faith": 0},
    "Catarina Armour": {"sets": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 22, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Cathedral Knight Armour": {"sets": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Herald", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 18, "faith": 22},
    "Chloranthy Ring": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 18, "dexterity": 18, "intelligence": 18, "faith": 18},
    "Claws": {"sets": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 20, "intelligence": 20, "faith": 0},
    "Claymore": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 30, "dexterity": 26, "intelligence": 0, "faith": 0},
    "Cleric Armour": {"sets": set(["Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 24},
    "Cleric's Candlestick": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 21, "intelligence": 0, "faith": 29},
    "Composite Bow": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([1,2]), "strength": 15, "dexterity": 21, "intelligence": 0, "faith": 0},
    "Cornyx's Robes": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "armor", "character": "Pyromancer", "encounterLevels": set([1,2]), "strength": 21, "dexterity": 0, "intelligence": 21, "faith": 0},
    "Court Sorcerer Robes": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 17, "intelligence": 22, "faith": 0},
    "Covetous Gold Serpent Ring": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgrade", "character": "Thief", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 30, "intelligence": 25, "faith": 0},
    "Covetous Silver Serpent Ring": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgrade", "character": "Thief", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 31, "intelligence": 27, "faith": 0},
    "Crescent Moon Sword": {"sets": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 17, "intelligence": 0, "faith": 17},
    "Cresent Axe": {"sets": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 22, "dexterity": 17, "intelligence": 0, "faith": 15},
    "Crest Shield": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "encounterLevels": set([1,2]), "strength": 16, "dexterity": 22, "intelligence": 0, "faith": 0},
    "Crimson Robes": {"sets": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 12, "intelligence": 22, "faith": 12},
    "Crystal Gem": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 25, "faith": 0},
    "Crystal Hail": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 25, "intelligence": 35, "faith": 0},
    "Crystal Magic Weapon": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Sorcerer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 30, "faith": 0},
    "Crystal Shield": {"sets": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 18, "dexterity": 0, "intelligence": 0, "faith": 28},
    "Crystal Straight Sword": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 30, "intelligence": 21, "faith": 0},
    "Dark Armour": {"sets": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 20, "intelligence": 20, "faith": 0},
    "Dark Wood Grain Ring": {"sets": set(["Explorers"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 26, "intelligence": 0, "faith": 0},
    "Deacon Robes": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 24},
    "Demon Titanite": {"sets": set(["Painted World of Ariamis"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 10, "faith": 10},
    "Divine Blessing": {"sets": set(["Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 22},
    "Dragon Crest Shield": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 21, "dexterity": 0, "intelligence": 0, "faith": 21},
    "Dragon Scale": {"sets": set(["Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 10, "dexterity": 0, "intelligence": 0, "faith": 10},
    "Dragonrider Bow": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 34, "intelligence": 0, "faith": 0},
    "Dragonscale Armour": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Sorcerer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 23, "intelligence": 23, "faith": 0},
    "Dragonslayer Greatbow": {"sets": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 23, "dexterity": 23, "intelligence": 0, "faith": 0},
    "Dragonslayer's Axe": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 15, "intelligence": 15, "faith": 15},
    "Drang Armour": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 18, "dexterity": 14, "intelligence": 0, "faith": 0},
    "Drang Hammers": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "encounterLevels": set([2,3,4]), "strength": 33, "dexterity": 35, "intelligence": 0, "faith": 0},
    "Dung Pie": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Dusk Crown Ring": {"sets": set(["Darkroot"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 30, "faith": 0},
    "East-West Shield": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 28, "faith": 0},
    "Eastern Armour": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Mercenary", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 36, "intelligence": 26, "faith": 0},
    "Eastern Iron Shield": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 28, "intelligence": 0, "faith": 0},
    "Effigy Shield": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 10, "dexterity": 0, "intelligence": 0, "faith": 10},
    "Elite Knight Armour": {"sets": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Knight", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 15},
    "Elkhorn Round Shield": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([2,3,4]), "strength": 16, "dexterity": 34, "intelligence": 16, "faith": 0},
    "Embraced Armour of Favour": {"sets": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 13, "dexterity": 0, "intelligence": 0, "faith": 23},
    "Exile Armour": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 26, "dexterity": 0, "intelligence": 0, "faith": 16},
    "Exile Greatsword": {"sets": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Falchion": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "encounterLevels": set([2,3,4]), "strength": 37, "dexterity": 30, "intelligence": 0, "faith": 23},
    "Fallen Knight Armour": {"sets": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Warrior", "encounterLevels": set([2,3,4]), "strength": 30, "dexterity": 0, "intelligence": 22, "faith": 0},
    "Faraam Armour": {"sets": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Knight", "encounterLevels": set([2,3,4]), "strength": 29, "dexterity": 0, "intelligence": 19, "faith": 0},
    "Faron Flashsword": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Sorcerer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 25, "faith": 15},
    "Fire Surge": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([1,2]), "strength": 22, "dexterity": 0, "intelligence": 26, "faith": 0},
    "Fire Whip": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 34, "faith": 18},
    "Fireball": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 23, "faith": 0},
    "Firebombs": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 15},
    "Firelink Armour": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 0, "intelligence": 15, "faith": 0},
    "Flameberge": {"sets": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 35, "intelligence": 0, "faith": 0},
    "Force": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 12, "faith": 0},
    "Four-Pronged Plow": {"sets": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 23, "dexterity": 0, "intelligence": 0, "faith": 23},
    "Giant's Halberd": {"sets": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 27, "dexterity": 0, "intelligence": 0, "faith": 23},
    "Gold-Hemmed Black Robes": {"sets": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 14, "intelligence": 14, "faith": 14},
    "Golden Ritual Spear": {"sets": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 24, "faith": 21},
    "Golden Wing Crest Shield": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([1,2]), "strength": 26, "dexterity": 0, "intelligence": 0, "faith": 26},
    "Grass Crest Shield": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([2,3,4]), "strength": 28, "dexterity": 0, "intelligence": 0, "faith": 28},
    "Great Chaos Fireball": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 37, "faith": 27},
    "Great Club": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Great Combustion": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 26, "faith": 22},
    "Great Heal": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 40},
    "Great Mace": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 21, "dexterity": 0, "intelligence": 0, "faith": 28},
    "Great Machete": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([2,3,4]), "strength": 40, "dexterity": 35, "intelligence": 0, "faith": 0},
    "Great Magic Weapon": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 12, "faith": 12},
    "Great Scythe": {"sets": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 32, "dexterity": 21, "intelligence": 0, "faith": 0},
    "Great Swamp Ring": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgrade", "character": "Pyromancer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 15, "intelligence": 20, "faith": 0},
    "Great Wooden Hammer": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([1,2]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Greataxe": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 32, "dexterity": 22, "intelligence": 0, "faith": 0},
    "Guardian Armour": {"sets": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 22, "intelligence": 22, "faith": 0},
    "Halberd": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 18, "dexterity": 0, "intelligence": 0, "faith": 31},
    "Hard Leather Armour": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 26, "dexterity": 26, "intelligence": 26, "faith": 0},
    "Havel's Armour": {"sets": set(["Characters Expansion"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 23, "dexterity": 0, "intelligence": 23, "faith": 0},
    "Havel's Greatshield": {"sets": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 35, "dexterity": 0, "intelligence": 13, "faith": 13},
    "Hawkwood's Shield": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "encounterLevels": set([2,3,4]), "strength": 23, "dexterity": 33, "intelligence": 0, "faith": 23},
    "Heal": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 23},
    "Heal Aid": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 13},
    "Heavy Gem": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 25, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Hollow Gem": {"sets": set(["Darkroot"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 15},
    "Hollow Soldier Shield": {"sets": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 16, "dexterity": 0, "intelligence": 0, "faith": 19},
    "Homing Crystal Soulmass": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 40, "faith": 0},
    "Hornet Ring": {"sets": set(["Dark Souls The Board Game"]), "type": "upgrade", "character": "Assassin", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 30, "intelligence": 0, "faith": 0},
    "Hunter Armour": {"sets": set(["Darkroot"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 34, "intelligence": 17, "faith": 0},
    "Immolation Tinder": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 28, "faith": 21},
    "Knight Slayer's Ring": {"sets": set(["Dark Souls The Board Game"]), "type": "upgrade", "character": "Warrior", "encounterLevels": set([1,2]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Kukris": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 15, "intelligence": 0, "faith": 0},
    "Large Leather Shield": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "encounterLevels": set([2,3,4]), "strength": 17, "dexterity": 33, "intelligence": 0, "faith": 0},
    "Life Ring": {"sets": set(["Iron Keep"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 30},
    "Lightning Gem": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 0},
    "Longbow": {"sets": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 18, "intelligence": 0, "faith": 0},
    "Lothric Knight Armour": {"sets": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Knight", "encounterLevels": set([1,2]), "strength": 21, "dexterity": 0, "intelligence": 0, "faith": 15},
    "Lothric Knight Greatsword": {"sets": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 20, "intelligence": 13, "faith": 13},
    "Lothric's Holy Sword": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([1,2]), "strength": 27, "dexterity": 0, "intelligence": 0, "faith": 31},
    "Lucerne": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 31, "intelligence": 31, "faith": 0},
    "Magic Barrier": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 12, "faith": 24},
    "Magic Shield": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 27, "faith": 14},
    "Magic Stoneplate Ring": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgrade", "character": "Cleric", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 32},
    "Man Serpent Hatchet": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 34, "intelligence": 0, "faith": 0},
    "Mannikin Claws": {"sets": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 24, "intelligence": 24, "faith": 0},
    "Mask of the Child": {"sets": set(["Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 19, "faith": 13},
    "Master's Attire": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 30, "intelligence": 18, "faith": 0},
    "Med Heal": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 30},
    "Mirrah Armour": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Deprived", "encounterLevels": set([2,3,4]), "strength": 27, "dexterity": 0, "intelligence": 0, "faith": 27},
    "Morion Blade": {"sets": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 24, "dexterity": 24, "intelligence": 0, "faith": 0},
    "Morne's Great Hammer": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 35},
    "Morning Star": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 16, "dexterity": 0, "intelligence": 0, "faith": 19},
    "Murakumo": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 27, "intelligence": 17, "faith": 0},
    "Obscuring Ring": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgrade", "character": "Thief", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 28, "intelligence": 0, "faith": 20},
    "Old Ironclad Armour": {"sets": set(["Iron Keep"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 34, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Onikiri And Ubadachi": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 36, "intelligence": 26, "faith": 0},
    "Painting Guardian Armour": {"sets": set(["Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 32, "intelligence": 14, "faith": 0},
    "Painting Guardian Curved Sword": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 26, "intelligence": 26, "faith": 26},
    "Paladin Armour": {"sets": set(["Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 24, "dexterity": 24, "intelligence": 0, "faith": 24},
    "Parrying Dagger": {"sets": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 21, "intelligence": 21, "faith": 21},
    "Partizan": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([2,3,4]), "strength": 28, "dexterity": 17, "intelligence": 0, "faith": 35},
    "Phoenix Parma Shield": {"sets": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Pierce Shield": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 16, "dexterity": 10, "intelligence": 0, "faith": 0},
    "Pike": {"sets": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 23, "dexterity": 0, "intelligence": 0, "faith": 23},
    "Poison Gem": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 15, "intelligence": 0, "faith": 0},
    "Poison Mist": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 11, "intelligence": 16, "faith": 0},
    "Poison Throwing Knives": {"sets": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 14, "intelligence": 14, "faith": 0},
    "Porcine Shield": {"sets": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 24, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Rapier": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 21, "intelligence": 21, "faith": 0},
    "Rapport": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 36, "faith": 0},
    "Raw Gem": {"sets": set(["Explorers"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Red and White Round Shield": {"sets": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 22, "faith": 10},
    "Red Tearstone Ring": {"sets": set(["Painted World of Ariamis"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Reinforced Club": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 23, "dexterity": 0, "intelligence": 0, "faith": 16},
    "Replenishment": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 25},
    "Ring of Favour": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Mercenary", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 21, "intelligence": 0, "faith": 21},
    "Rotten Ghru Dagger": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 17, "intelligence": 17, "faith": 0},
    "Rotten Ghru Spear": {"sets": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 21, "intelligence": 12, "faith": 0},
    "Royal Dirk": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 31, "intelligence": 0, "faith": 31},
    "Sacred Oath": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 14, "faith": 30},
    "Saint Bident": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Herald", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 35},
    "Scimitar": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 20, "intelligence": 18, "faith": 0},
    "Shadow Armour": {"sets": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Assassin", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 34, "intelligence": 0, "faith": 17},
    "Sharp Gem": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 25, "intelligence": 0, "faith": 0},
    "Shortsword": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 15, "dexterity": 23, "intelligence": 0, "faith": 0},
    "Shotel": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 29, "intelligence": 26, "faith": 0},
    "Silver Eagle Kite Shield": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 15, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Silver Knight Armour": {"sets": set(["Explorers"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 26, "dexterity": 26, "intelligence": 0, "faith": 0},
    "Silver Knight Shield": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([1,2]), "strength": 31, "dexterity": 23, "intelligence": 0, "faith": 0},
    "Silver Knight Spear": {"sets": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 22, "intelligence": 0, "faith": 26},
    "Silver Knight Straight Sword": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 20, "intelligence": 20, "faith": 20},
    "Simple Gem": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgrade", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 15},
    "Skull Lantern": {"sets": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 13, "intelligence": 14, "faith": 0},
    "Small Leather Shield": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "encounterLevels": set([1,2]), "strength": 15, "dexterity": 30, "intelligence": 0, "faith": 15},
    "Sorcerer's Staff": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 15, "dexterity": 0, "intelligence": 30, "faith": 0},
    "Soul Arrow": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 16, "faith": 0},
    "Soul Greatsword": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 35, "faith": 15},
    "Soul Spear": {"sets": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 25, "faith": 15},
    "Soulstream": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 22, "faith": 0},
    "Spider Shield": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "encounterLevels": set([1,2]), "strength": 27, "dexterity": 0, "intelligence": 15, "faith": 0},
    "Spiked Mace": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([1,2]), "strength": 32, "dexterity": 0, "intelligence": 0, "faith": 22},
    "Spotted Whip": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 30, "intelligence": 23, "faith": 0},
    "Stone Greataxe": {"sets": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Stone Greatshield": {"sets": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Stone Greatsword": {"sets": set(["Darkroot"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 22, "dexterity": 0, "intelligence": 0, "faith": 22},
    "Stone Knight Armour": {"sets": set(["Darkroot"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Stone Parama": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Pyromancer", "encounterLevels": set([2,3,4]), "strength": 15, "dexterity": 0, "intelligence": 35, "faith": 0},
    "Sun Princess Ring": {"sets": set(["Dark Souls The Board Game"]), "type": "upgrade", "character": "Knight", "encounterLevels": set([1,2]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 25},
    "Sunless Armour": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 13, "dexterity": 0, "intelligence": 0, "faith": 13},
    "Sunlight Shield": {"sets": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 30},
    "Sunset Armour": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 0, "intelligence": 0, "faith": 24},
    "Sunset Shield": {"sets": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "encounterLevels": set([1,2]), "strength": 15, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Thorolund Talisman": {"sets": set(["Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 31},
    "Thrall Axe": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 16, "dexterity": 16, "intelligence": 0, "faith": 0},
    "Throwing Knives": {"sets": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 14, "intelligence": 12, "faith": 0},
    "Tiny Being's Ring": {"sets": set(["Dark Souls The Board Game"]), "type": "upgrade", "character": "Herald", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Torch": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "encounterLevels": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Twin Dragon Greatshield": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 35, "intelligence": 15, "faith": 15},
    "Ughigatana": {"sets": set(["Explorers"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 32, "intelligence": 0, "faith": 14},
    "Umbral Dagger": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "encounterLevels": set([2,3,4]), "strength": 0, "dexterity": 35, "intelligence": 35, "faith": 0},
    "Velka's Rapier": {"sets": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 19, "intelligence": 27, "faith": 0},
    "Warden Twinblades": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "encounterLevels": set([1,2]), "strength": 17, "dexterity": 25, "intelligence": 17, "faith": 0},
    "Warpick": {"sets": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Warrior", "encounterLevels": set([2,3,4]), "strength": 35, "dexterity": 25, "intelligence": 0, "faith": 0},
    "Winged Spear": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 20, "dexterity": 0, "intelligence": 0, "faith": 22},
    "Witch's Lock": {"sets": set(["Iron Keep"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 31, "faith": 0},
    "Wolf Ring": {"sets": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgrade", "character": "Mercenary", "encounterLevels": set([2,3,4]), "strength": 25, "dexterity": 35, "intelligence": 25, "faith": 0},
    "Worker Armour": {"sets": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 12, "dexterity": 12, "intelligence": 12, "faith": 12},
    "Xanthous Robes": {"sets": set(["Painted World of Ariamis"]), "type": "armor", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 0, "dexterity": 0, "intelligence": 23, "faith": 20},
    "Zweihander": {"sets": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "encounterLevels": set([1,2,3,4]), "strength": 35, "dexterity": 25, "intelligence": 0, "faith": 0},
}

tiers = {
    "armor": {},
    "weapon": {},
    "upgrade": {}
}


def generate_treasure_soul_cost(setsAvailable, charactersActive):
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

    
def populate_treasure_tiers(setsAvailable, charactersActive):
    # Generate the list of available treasures for each type.
    armor = sorted([t for t in treasures if (
        treasures[t]["type"] == "armor"
        and treasures[t]["sets"] & setsAvailable
        and (not treasures[t]["character"] or treasures[t]["character"] in charactersActive)
        and "soulCost" in treasures[t])
        ], key=lambda x: treasures[x]["soulCost"])
    armorLen = len(armor)
    weapon = sorted([t for t in treasures if (
        treasures[t]["type"] == "weapon"
        and treasures[t]["sets"] & setsAvailable
        and (not treasures[t]["character"] or treasures[t]["character"] in charactersActive)
        and "soulCost" in treasures[t])
        ], key=lambda x: treasures[x]["soulCost"])
    weaponLen = len(weapon)
    upgrade = sorted([t for t in treasures if (
        treasures[t]["type"] == "upgrade"
        and treasures[t]["sets"] & setsAvailable
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


def pick_treasure(treasureSwapOption, swapTreasure, lastPicked, encounterLevel, setsAvailable, charactersActive):
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
                and treasures[t]["sets"] & setsAvailable
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
    return choice(alts)
