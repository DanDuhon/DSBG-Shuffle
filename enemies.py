from json import dump
from os import path


baseFolder = path.dirname(__file__)
enemies = []
enemyIds = {}
enemiesDict = {}
reach = []


class Enemy:
    def __init__(self, name, expansion, numberOfModels, health, armor, resist, attacks, attackType, dodge, move, attackRange, attackEffect=[], difficulty=0) -> None:
        enemiesDict[name] = self
        enemies.append(self)
        self.name = name
        self.expansion = expansion
        self.numberOfModels = numberOfModels
        self.health = health
        self.armor = armor
        self.resist = resist
        self.attacks = attacks
        self.attackType = attackType
        self.dodge = dodge
        self.move = move
        self.attackRange = attackRange
        self.attackEffect = attackEffect
        self.difficulty = difficulty

        self.bleeding = False
        self.deaths = 0
        self.damageDone = 0
        self.bleedDamage = 0
        self.damagingAttacks = 0
        self.totalAttacks = 0
        self.loadoutDamage = {}
        self.imagePath = baseFolder + "\\images\\" + name + ".png"

        for i, m in enumerate(self.move):
            reach.append(m + self.attackRange[i])


    def reset(self):
        with open(baseFolder + "\\enemies\\" + self.name + ".json", "w") as enemyFile:
            dump({"deaths": 0, "totalAttacks": 0, "damagingAttacks": 0, "damageDone": 0, "bleedDamage": 0, "loadoutDamage": {}}, enemyFile)


Enemy(name="Alonne Bow Knight", expansion="Iron Keep", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=2, move=[0], attackRange=[4], difficulty=71.92)
Enemy(name="Alonne Knight Captain", expansion="Iron Keep", numberOfModels=3, health=5, armor=2, resist=2, attacks=[5], attackType=["magic"], dodge=1, move=[2], attackRange=[0], difficulty=314.70)
Enemy(name="Alonne Sword Knight", expansion="Iron Keep", numberOfModels=3, health=1, armor=2, resist=2, attacks=[5], attackType=["physical"], dodge=1, move=[2], attackRange=[0], difficulty=84.89)
Enemy(name="Black Hollow Mage", expansion="Executioner Chariot", numberOfModels=2, health=5, armor=2, resist=3, attacks=[4], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficulty=486.22)
Enemy(name="Bonewheel Skeleton", expansion="The Painted World of Ariamis", numberOfModels=2, health=1, armor=1, resist=1, attacks=[4,4], attackType=["physical", "physical"], dodge=2, move=[1, 1], attackRange=[0, 0], difficulty=64.69)
Enemy(name="Crossbow Hollow", expansion="Dark Souls The Board Game", numberOfModels=3, health=1, armor=1, resist=0, attacks=[3], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficulty=30.21)
Enemy(name="Crow Demon", expansion="The Painted World of Ariamis", numberOfModels=2, health=5, armor=1, resist=2, attacks=[6], attackType=["physical"], dodge=2, move=[4], attackRange=[0], difficulty=377.33)
Enemy(name="Demonic Foliage", expansion="Darkroot", numberOfModels=2, health=1, armor=2, resist=1, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=73.93)
Enemy(name="Engorged Zombie", expansion="The Painted World of Ariamis", numberOfModels=2, health=1, armor=2, resist=2, attacks=[4], attackType=["magic"], dodge=1, move=[1], attackRange=[0], difficulty=76.08)
Enemy(name="Falchion Skeleton", expansion="Executioner Chariot", numberOfModels=2, health=1, armor=1, resist=1, attacks=[3], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[2], attackRange=[0], difficulty=61.68)
Enemy(name="Firebomb Hollow", expansion="Explorers", numberOfModels=3, health=1, armor=1, resist=1, attacks=[3], attackType=["magic"], dodge=1, move=[1], attackRange=[2], difficulty=31.98)
Enemy(name="Giant Skeleton Archer", expansion="The Tomb of Giants", numberOfModels=2, health=5, armor=1, resist=1, attacks=[2,5], attackType=["physical", "physical"], dodge=2, move=[0, 0], attackRange=[0, 4], difficulty=264.29)
Enemy(name="Giant Skeleton Soldier", expansion="The Tomb of Giants", numberOfModels=2, health=5, armor=1, resist=1, attacks=[2,5], attackType=["physical", "physical"], dodge=1, move=[1, 1], attackRange=[0, 1], difficulty=165.89)
Enemy(name="Hollow Soldier", expansion="Dark Souls The Board Game", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=22.81)
Enemy(name="Ironclad Soldier", expansion="Iron Keep", numberOfModels=3, health=5, armor=3, resist=2, attacks=[5], attackType=["physical"], dodge=2, move=[1], attackRange=[0], difficulty=298.46)
Enemy(name="Large Hollow Soldier", expansion="Dark Souls The Board Game", numberOfModels=2, health=5, armor=1, resist=0, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=74.73)
Enemy(name="Mushroom Child", expansion="Darkroot", numberOfModels=1, health=5, armor=1, resist=2, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=94.66)
Enemy(name="Mushroom Parent", expansion="Darkroot", numberOfModels=1, health=10, armor=1, resist=2, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=221.77)
Enemy(name="Necromancer", expansion="The Tomb of Giants", numberOfModels=2, health=5, armor=1, resist=2, attacks=[3], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficulty=252.17)
Enemy(name="Phalanx", expansion="The Painted World of Ariamis", numberOfModels=1, health=5, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=1, move=[0], attackRange=[1], difficulty=152.19)
Enemy(name="Phalanx Hollow", expansion="The Painted World of Ariamis", numberOfModels=5, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[1], difficulty=22.81)
Enemy(name="Plow Scarecrow", expansion="Darkroot", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=2, move=[2], attackRange=[1], difficulty=70.22)
Enemy(name="Sentinel", expansion="Dark Souls The Board Game", numberOfModels=2, health=10, armor=2, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=505.84)
Enemy(name="Shears Scarecrow", expansion="Darkroot", numberOfModels=3, health=1, armor=1, resist=1, attacks=[3,3], attackType=["physical", "physical"], dodge=2, move=[1, 1], attackRange=[0, 0], difficulty=39.51)
Enemy(name="Silver Knight Greatbowman", expansion="Dark Souls The Board Game", numberOfModels=3, health=1, armor=2, resist=0, attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[4], difficulty=59.56)
Enemy(name="Silver Knight Spearman", expansion="Explorers", numberOfModels=3, health=1, armor=2, resist=1, attacks=[6], attackType=["physical"], dodge=2, move=[0], attackRange=[1], difficulty=72.46)
Enemy(name="Silver Knight Swordsman", expansion="Dark Souls The Board Game", numberOfModels=3, health=1, armor=2, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[0], difficulty=103.53)
Enemy(name="Skeleton Archer", expansion="The Tomb of Giants", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[4], difficulty=50.75)
Enemy(name="Skeleton Beast", expansion="The Tomb of Giants", numberOfModels=1, health=5, armor=2, resist=2, attacks=[4,4], attackType=["physical", "physical"], dodge=2, move=[1, 1], attackRange=[0, 0], difficulty=278.10)
Enemy(name="Skeleton Soldier", expansion="The Tomb of Giants", numberOfModels=3, health=1, armor=2, resist=1, attacks=[2], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[1], attackRange=[0], difficulty=52.59)
Enemy(name="Snow Rat", expansion="The Painted World of Ariamis", numberOfModels=2, health=1, armor=0, resist=1, attacks=[3], attackType=["physical"], attackEffect=["poison"], dodge=1, move=[4], attackRange=[0], difficulty=52.27)
Enemy(name="Stone Guardian", expansion="Darkroot", numberOfModels=2, health=5, armor=2, resist=3, attacks=[4,5], attackType=["physical", "physical"], dodge=1, move=[1, 1], attackRange=[0, 0], difficulty=270.11)
Enemy(name="Stone Knight", expansion="Darkroot", numberOfModels=2, health=5, armor=3, resist=2, attacks=[5], attackType=["magic"], dodge=1, move=[1], attackRange=[0], difficulty=486.23)
Enemy(name="Standard Invader/Hungry Mimic", expansion=None, numberOfModels=0, health=0, armor=0, resist=0, attacks=[0], attackType=["physical"], dodge=0, move=[0], attackRange=[0], difficulty=0)
Enemy(name="Advanced Invader/Voracious Mimic", expansion=None, numberOfModels=0, health=0, armor=0, resist=0, attacks=[0], attackType=["physical"], dodge=0, move=[0], attackRange=[0], difficulty=0)

for i, enemy in enumerate(enemiesDict):
    enemyIds[i] = enemiesDict[enemy]
    enemiesDict[enemy].id = i