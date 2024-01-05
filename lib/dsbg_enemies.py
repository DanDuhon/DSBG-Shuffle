try:
    import platform
    from os import path
    
    from dsbg_utility import log


    if platform.system() == "Windows":
        pathSep = "\\"
    else:
        pathSep = "/"

    baseFolder = path.dirname(__file__).replace("\\lib".replace("\\", pathSep), "")
    enemies = []
    enemyIds = {}
    enemiesDict = {}
    reach = []


    class Enemy:
        def __init__(self, name, expansions, difficulty, health = None) -> None:
            enemiesDict[name] = self
            enemies.append(self)
            self.name = name
            self.expansions = expansions
            self.difficulty = difficulty
            
            self.imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\".replace("\\", pathSep) + name + ".png"
            
            if "Hollow" in self.name and health == 1:
                self.gang = "Hollow"
            elif "Alonne" in self.name and health == 1:
                self.gang = "Alonne"
            elif "Skeleton" in self.name and health == 1:
                self.gang = "Skeleton"
            elif "Scarecrow" in self.name:
                self.gang = "Scarecrow"
            else:
                self.gang = None


    Enemy(name="Alonne Bow Knight", expansions=set(["Iron Keep"]), health = 1, difficulty=111.75)
    Enemy(name="Alonne Knight Captain", expansions=set(["Iron Keep"]), difficulty=479.48)
    Enemy(name="Alonne Sword Knight", expansions=set(["Iron Keep"]), health = 1, difficulty=130.05)
    Enemy(name="Black Hollow Mage", expansions=set(["Executioner Chariot"]), difficulty=557.57)
    Enemy(name="Bonewheel Skeleton", expansions=set(["Painted World of Ariamis"]), health = 1, difficulty=100.49)
    Enemy(name="Crossbow Hollow", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health = 1, difficulty=45.02)
    Enemy(name="Crow Demon", expansions=set(["Painted World of Ariamis"]), difficulty=591.94)
    Enemy(name="Demonic Foliage", expansions=set(["Darkroot"]), difficulty=113.27)
    Enemy(name="Engorged Zombie", expansions=set(["Painted World of Ariamis"]), difficulty=115.2)
    Enemy(name="Falchion Skeleton", expansions=set(["Executioner Chariot"]), health = 1, difficulty=56.02)
    Enemy(name="Firebomb Hollow", expansions=set(["Explorers"]), health = 1, difficulty=47.65)
    Enemy(name="Giant Skeleton Archer", expansions=set(["Tomb of Giants"]), difficulty=414.31)
    Enemy(name="Giant Skeleton Soldier", expansions=set(["Tomb of Giants"]), difficulty=253.87)
    Enemy(name="Hollow Soldier", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health = 1, difficulty=34.76)
    Enemy(name="Ironclad Soldier", expansions=set(["Iron Keep"]), difficulty=464.27)
    Enemy(name="Large Hollow Soldier", expansions=set(["Dark Souls The Board Game"]), difficulty=114.11)
    Enemy(name="Mushroom Child", expansions=set(["Darkroot"]), difficulty=145.01)
    Enemy(name="Mushroom Parent", expansions=set(["Darkroot"]), difficulty=341.81)
    Enemy(name="Necromancer", expansions=set(["Tomb of Giants"]), difficulty=205.7)
    Enemy(name="Phalanx", expansions=set(["Painted World of Ariamis"]), difficulty=233.09)
    Enemy(name="Phalanx Hollow", expansions=set(["Painted World of Ariamis"]), health = 1, difficulty=34.76)
    Enemy(name="Plow Scarecrow", expansions=set(["Darkroot"]), difficulty=109.08)
    Enemy(name="Sentinel", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), difficulty=778.12)
    Enemy(name="Shears Scarecrow", expansions=set(["Darkroot"]), difficulty=60.49)
    Enemy(name="Silver Knight Greatbowman", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), difficulty=90.76)
    Enemy(name="Silver Knight Spearman", expansions=set(["Explorers"]), difficulty=113.69)
    Enemy(name="Silver Knight Swordsman", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), difficulty=161.85)
    Enemy(name="Skeleton Archer", expansions=set(["Tomb of Giants"]), health = 1, difficulty=77.34)
    Enemy(name="Skeleton Beast", expansions=set(["Tomb of Giants"]), difficulty=431.7)
    Enemy(name="Skeleton Soldier", expansions=set(["Tomb of Giants"]), health = 1, difficulty=21.69)
    Enemy(name="Snow Rat", expansions=set(["Painted World of Ariamis"]), difficulty=63.61)
    Enemy(name="Stone Guardian", expansions=set(["Darkroot"]), difficulty=412.2)
    Enemy(name="Stone Knight", expansions=set(["Darkroot"]), difficulty=737.67)
    Enemy(name="Standard Invader", expansions=set(["Phantoms"]), difficulty=0)
    Enemy(name="Advanced Invader", expansions=set(["Phantoms"]), difficulty=0)
    Enemy(name="Mimic", expansions=set(["The Sunless City"]), difficulty=513.34)

    for i, enemy in enumerate(enemiesDict):
        enemyIds[i] = enemiesDict[enemy]
        enemiesDict[enemy].id = i

    bosses = {
        "Asylum Demon": {"name": "Asylum Demon", "type": "boss", "level": "Mini Boss", "expansions": set(["Asylum Demon"])},
        "Black Knight": {"name": "Black Knight", "type": "boss", "level": "Mini Boss", "expansions": set(["Tomb of Giants"])},
        "Boreal Outrider Knight": {"name": "Boreal Outrider Knight", "type": "boss", "level": "Mini Boss", "expansions": set(["Dark Souls The Board Game"])},
        "Gargoyle": {"name": "Gargoyle", "type": "boss", "level": "Mini Boss", "expansions": set(["Dark Souls The Board Game"])},
        "Heavy Knight": {"name": "Heavy Knight", "type": "boss", "level": "Mini Boss", "expansions": set(["Painted World of Ariamis"])},
        "Old Dragonslayer": {"name": "Old Dragonslayer", "type": "boss", "level": "Mini Boss", "expansions": set(["Explorers"])},
        "Titanite Demon": {"name": "Titanite Demon", "type": "boss", "level": "Mini Boss", "expansions": set(["Dark Souls The Board Game", "The Sunless City"])},
        "Winged Knight": {"name": "Winged Knight", "type": "boss", "level": "Mini Boss", "expansions": set(["Dark Souls The Board Game"])},
        "Artorias": {"name": "Artorias", "type": "boss", "level": "Main Boss", "expansions": set(["Darkroot"])},
        "Crossbreed Priscilla": {"name": "Crossbreed Priscilla", "type": "boss", "level": "Main Boss", "expansions": set(["Painted World of Ariamis"])},
        "Dancer of the Boreal Valley": {"name": "Dancer of the Boreal Valley", "type": "boss", "level": "Main Boss", "expansions": set(["Dark Souls The Board Game"])},
        "Gravelord Nito": {"name": "Gravelord Nito", "type": "boss", "level": "Main Boss", "expansions": set(["Tomb of Giants"])},
        "Great Grey Wolf Sif": {"name": "Great Grey Wolf Sif", "type": "boss", "level": "Main Boss", "expansions": set(["Darkroot"])},
        "Ornstein and Smough": {"name": "Ornstein and Smough", "type": "boss", "level": "Main Boss", "expansions": set(["Dark Souls The Board Game", "The Sunless City"])},
        "Sir Alonne": {"name": "Sir Alonne", "type": "boss", "level": "Main Boss", "expansions": set(["Iron Keep"])},
        "Smelter Demon": {"name": "Smelter Demon", "type": "boss", "level": "Main Boss", "expansions": set(["Iron Keep"])},
        "The Pursuer": {"name": "The Pursuer", "type": "boss", "level": "Main Boss", "expansions": set(["Explorers"])},
        "Black Dragon Kalameet": {"name": "Black Dragon Kalameet", "type": "boss", "level": "Mega Boss", "expansions": set(["Black Dragon Kalameet"])},
        "Executioner Chariot": {"name": "Executioner Chariot", "type": "boss", "level": "Mega Boss", "expansions": set(["Executioner Chariot"])},
        "Gaping Dragon": {"name": "Gaping Dragon", "type": "boss", "level": "Mega Boss", "expansions": set(["Gaping Dragon"])},
        "Guardian Dragon": {"name": "Guardian Dragon", "type": "boss", "level": "Mega Boss", "expansions": set(["Guardian Dragon"])},
        "Manus, Father of the Abyss": {"name": "Manus, Father of the Abyss", "type": "boss", "level": "Mega Boss", "expansions": set(["Manus, Father of the Abyss"])},
        "Old Iron King": {"name": "Old Iron King", "type": "boss", "level": "Mega Boss", "expansions": set(["Old Iron King"])},
        "Stray Demon": {"name": "Stray Demon", "type": "boss", "level": "Mega Boss", "expansions": set(["Asylum Demon"])},
        "The Four Kings": {"name": "The Four Kings", "type": "boss", "level": "Mega Boss", "expansions": set(["The Four Kings"])},
        "The Last Giant": {"name": "The Last Giant", "type": "boss", "level": "Mega Boss", "expansions": set(["The Last Giant"])},
        "Vordt of the Boreal Valley": {"name": "Vordt of the Boreal Valley", "type": "boss", "level": "Mega Boss", "expansions": set(["Vordt of the Boreal Valley"])}
    }
except Exception as e:
    log(e, exception=True)
    raise