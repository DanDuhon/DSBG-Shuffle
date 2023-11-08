from os import path


baseFolder = path.dirname(__file__)
enemies = []
enemyIds = {}
enemiesDict = {}
reach = []


class Enemy:
    def __init__(self, name, health, difficulty) -> None:
        enemiesDict[name] = self
        enemies.append(self)
        self.name = name
        self.health = health
        self.difficulty = difficulty
        
        self.imagePath = baseFolder + "\\images\\" + name.replace(" (TSC)", "") + ".png"
        
        if "Hollow" in self.name and self.health == 1:
            self.gang = "Hollow"
        elif "Alonne" in self.name and self.health == 1:
            self.gang = "Alonne"
        elif "Skeleton" in self.name and self.health == 1:
            self.gang = "Skeleton"
        elif "Scarecrow" in self.name:
            self.gang = "Scarecrow"
        else:
            self.gang = None
        
        if "Hollow" in self.name:
            self.group = "Hollow"
        elif "Alonne" in self.name:
            self.group = "Alonne"
        elif "Skeleton" in self.name:
            self.group = "Skeleton"
        elif "Scarecrow" in self.name:
            self.group = "Scarecrow"
        elif "Silver Knight" in self.name:
            self.group = "Silver Knight"
        else:
            self.group = None


Enemy(name="Alonne Bow Knight", health=1, difficulty=111.75)
Enemy(name="Alonne Knight Captain", health=5, difficulty=479.48)
Enemy(name="Alonne Sword Knight", health=1, difficulty=130.05)
Enemy(name="Black Hollow Mage", health=5, difficulty=557.57)
Enemy(name="Bonewheel Skeleton", health=1, difficulty=100.49)
Enemy(name="Crossbow Hollow", health=1, difficulty=45.02)
Enemy(name="Crow Demon", health=5, difficulty=591.94)
Enemy(name="Demonic Foliage", health=1, difficulty=113.27)
Enemy(name="Engorged Zombie", health=1, difficulty=115.2)
Enemy(name="Falchion Skeleton", health=1, difficulty=56.02)
Enemy(name="Firebomb Hollow", health=1, difficulty=47.65)
Enemy(name="Giant Skeleton Archer", health=5, difficulty=414.31)
Enemy(name="Giant Skeleton Soldier", health=5, difficulty=253.87)
Enemy(name="Hollow Soldier", health=1, difficulty=34.76)
Enemy(name="Ironclad Soldier", health=5, difficulty=464.27)
Enemy(name="Large Hollow Soldier", health=5, difficulty=114.11)
Enemy(name="Mushroom Child", health=5, difficulty=145.01)
Enemy(name="Mushroom Parent", health=10, difficulty=341.81)
Enemy(name="Necromancer", health=5, difficulty=205.7)
Enemy(name="Phalanx", health=5, difficulty=233.09)
Enemy(name="Phalanx Hollow", health=1, difficulty=34.76)
Enemy(name="Plow Scarecrow", health=1, difficulty=109.08)
Enemy(name="Sentinel", health=10, difficulty=778.12)
Enemy(name="Shears Scarecrow", health=1, difficulty=60.49)
Enemy(name="Silver Knight Greatbowman", health=1, difficulty=90.76)
Enemy(name="Silver Knight Spearman", health=1, difficulty=113.69)
Enemy(name="Silver Knight Swordsman", health=1, difficulty=161.85)
Enemy(name="Skeleton Archer", health=1, difficulty=77.34)
Enemy(name="Skeleton Beast", health=5, difficulty=431.7)
Enemy(name="Skeleton Soldier", health=1, difficulty=21.69)
Enemy(name="Snow Rat", health=1, difficulty=63.61)
Enemy(name="Stone Guardian", health=5, difficulty=412.2)
Enemy(name="Stone Knight", health=5, difficulty=737.67)
Enemy(name="Standard Invader", health=10, difficulty=0)
Enemy(name="Advanced Invader", health=10, difficulty=0)
Enemy(name="Mimic", health=5, difficulty=513.34)
Enemy(name="Crossbow Hollow (TSC)", health=1, difficulty=45.02)
Enemy(name="Hollow Soldier (TSC)", health=1, difficulty=34.76)
Enemy(name="Sentinel (TSC)", health=1, difficulty=778.12)
Enemy(name="Silver Knight Greatbowman (TSC)", health=1, difficulty=90.76)
Enemy(name="Silver Knight Swordsman (TSC)", health=1, difficulty=161.85)

for i, enemy in enumerate(enemiesDict):
    enemyIds[i] = enemiesDict[enemy]
    enemiesDict[enemy].id = i