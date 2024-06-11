try:
    from dsbg_shuffle_utility import log, baseFolder, pathSep


    enemies = []
    enemyIds = {}
    enemiesDict = {}
    reach = []


    class Enemy:
        def __init__(self, id, name, expansions, difficultyTiers, cards=1, health=None) -> None:
            enemiesDict[name] = self
            enemies.append(self)
            enemyIds[id] = self
            self.id = id
            self.name = name
            self.expansions = expansions
            self.cards = cards
            self.difficultyTiers = difficultyTiers
            
            self.imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\".replace("\\", pathSep) + name + ".png"
            
            if "Hollow" in self.name and health == 1:
                self.gang = "Hollow"
            elif "Alonne" in self.name and health == 1:
                self.gang = "Alonne"
            elif "Skeleton" in self.name and health == 1:
                self.gang = "Skeleton"
            elif "Silver Knight" in self.name and health == 1:
                self.gang = "Silver Knight"
            else:
                self.gang = None


    Enemy(id=1, name="Alonne Bow Knight", expansions=set(["Iron Keep"]), health=1, difficultyTiers={1: {"toughness": 6182, "difficulty": {1: 236.49, 2: 236.49, 3: 236.49, 4: 236.49}}, 2: {"toughness": 11917, "difficulty": {1: 48.25, 2: 48.25, 3: 48.25, 4: 48.25}}, 3: {"toughness": 36112, "difficulty": {1: 38.05, 2: 38.05, 3: 38.05, 4: 38.05}}})
    Enemy(id=2, name="Alonne Knight Captain", expansions=set(["Iron Keep"]), difficultyTiers={1: {"toughness": 718, "difficulty": {1: 1952.79, 2: 1952.79, 3: 1952.79, 4: 1952.79}}, 2: {"toughness": 1827, "difficulty": {1: 395.66, 2: 395.66, 3: 395.66, 4: 395.66}}, 3: {"toughness": 7683, "difficulty": {1: 136.11, 2: 136.11, 3: 136.11, 4: 136.11}}})
    Enemy(id=3, name="Alonne Sword Knight", expansions=set(["Iron Keep"]), health=1, difficultyTiers={1: {"toughness": 3070, "difficulty": {1: 435.98, 2: 435.98, 3: 435.98, 4: 435.98}}, 2: {"toughness": 6934, "difficulty": {1: 79.74, 2: 79.74, 3: 79.74, 4: 79.74}}, 3: {"toughness": 25200, "difficulty": {1: 38.3, 2: 38.3, 3: 38.3, 4: 38.3}}})
    Enemy(id=4, name="Black Hollow Mage", expansions=set(["Executioner Chariot"]), difficultyTiers={1: {"toughness": 679, "difficulty": {1: 2363.71, 2: 2363.71, 3: 2363.71, 4: 2363.71}}, 2: {"toughness": 1653, "difficulty": {1: 471.87, 2: 471.87, 3: 471.87, 4: 471.87}}, 3: {"toughness": 6893, "difficulty": {1: 222.56, 2: 222.56, 3: 222.56, 4: 222.56}}})
    Enemy(id=5, name="Bonewheel Skeleton", expansions=set(["Painted World of Ariamis"]), health=1, difficultyTiers={1: {"toughness": 6182, "difficulty": {1: 659.09, 2: 709.79, 3: 760.48, 4: 822.88}}, 2: {"toughness": 11917, "difficulty": {1: 134.48, 2: 144.82, 3: 155.17, 4: 167.9}}, 3: {"toughness": 36112, "difficulty": {1: 106.06, 2: 114.21, 3: 122.37, 4: 132.41}}})
    Enemy(id=6, name="Crossbow Hollow", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health=1, difficultyTiers={1: {"toughness": 7022, "difficulty": {1: 72.81, 2: 72.81, 3: 72.81, 4: 72.81}}, 2: {"toughness": 12712, "difficulty": {1: 18.37, 2: 18.37, 3: 18.37, 4: 18.37}}, 3: {"toughness": 37124, "difficulty": {1: 7.85, 2: 7.85, 3: 7.85, 4: 7.85}}})
    Enemy(id=7, name="Crow Demon", expansions=set(["Painted World of Ariamis"]), difficultyTiers={1: {"toughness": 1616, "difficulty": {1: 3045.01, 2: 3279.24, 3: 3513.48, 4: 3801.76}}, 2: {"toughness": 3634, "difficulty": {1: 656.19, 2: 706.66, 3: 757.14, 4: 819.27}}, 3: {"toughness": 13031, "difficulty": {1: 424.16, 2: 456.79, 3: 489.42, 4: 529.58}}})
    Enemy(id=8, name="Demonic Foliage", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 3786, "difficulty": {1: 353.53, 2: 353.53, 3: 353.53, 4: 353.53}}, 2: {"toughness": 7864, "difficulty": {1: 70.31, 2: 70.31, 3: 70.31, 4: 70.31}}, 3: {"toughness": 28785, "difficulty": {1: 33.53, 2: 33.53, 3: 33.53, 4: 33.53}}})
    Enemy(id=9, name="Engorged Zombie", expansions=set(["Painted World of Ariamis"]), difficultyTiers={1: {"toughness": 3070, "difficulty": {1: 206.2, 2: 206.2, 3: 206.2, 4: 206.2}}, 2: {"toughness": 6934, "difficulty": {1: 43.9, 2: 43.9, 3: 43.9, 4: 43.9}}, 3: {"toughness": 25200, "difficulty": {1: 16.38, 2: 16.38, 3: 16.38, 4: 16.38}}})
    Enemy(id=10, name="Falchion Skeleton", expansions=set(["Executioner Chariot"]), health=1, difficultyTiers={1: {"toughness": 6182, "difficulty": {1: 260.66, 2: 260.66, 3: 260.66, 4: 260.66}}, 2: {"toughness": 11917, "difficulty": {1: 80.62, 2: 80.62, 3: 80.62, 4: 80.62}}, 3: {"toughness": 36112, "difficulty": {1: 40.99, 2: 40.99, 3: 40.99, 4: 40.99}}})
    Enemy(id=11, name="Firebomb Hollow", expansions=set(["Explorers"]), health=1, difficultyTiers={1: {"toughness": 6182, "difficulty": {1: 81.73, 2: 88.01, 3: 94.3, 4: 102.04}}, 2: {"toughness": 11917, "difficulty": {1: 19.36, 2: 20.85, 3: 22.34, 4: 24.17}}, 3: {"toughness": 36112, "difficulty": {1: 7.98, 2: 8.59, 3: 9.2, 4: 9.96}}})
    Enemy(id=12, name="Giant Skeleton Archer", expansions=set(["Tomb of Giants"]), difficultyTiers={1: {"toughness": 1837, "difficulty": {1: 1373.94, 2: 1382.6, 3: 1391.26, 4: 1401.92}}, 2: {"toughness": 4019, "difficulty": {1: 277.9, 2: 279.78, 3: 281.65, 4: 283.96}}, 3: {"toughness": 14351, "difficulty": {1: 182.87, 2: 184.06, 3: 185.26, 4: 186.73}}})
    Enemy(id=13, name="Giant Skeleton Soldier", expansions=set(["Tomb of Giants"]), difficultyTiers={1: {"toughness": 1837, "difficulty": {1: 863.47, 2: 869.11, 3: 874.75, 4: 881.7}}, 2: {"toughness": 4019, "difficulty": {1: 159.93, 2: 160.76, 3: 161.59, 4: 162.6}}, 3: {"toughness": 14351, "difficulty": {1: 78.91, 2: 79.37, 3: 79.83, 4: 80.39}}})
    Enemy(id=14, name="Hollow Soldier", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health=1, difficultyTiers={1: {"toughness": 6182, "difficulty": {1: 94.59, 2: 94.59, 3: 94.59, 4: 94.59}}, 2: {"toughness": 11917, "difficulty": {1: 16.96, 2: 16.96, 3: 16.96, 4: 16.96}}, 3: {"toughness": 36112, "difficulty": {1: 10.25, 2: 10.25, 3: 10.25, 4: 10.25}}})
    Enemy(id=15, name="Ironclad Soldier", expansions=set(["Iron Keep"]), difficultyTiers={1: {"toughness": 272, "difficulty": {1: 7661.94, 2: 8251.32, 3: 8840.7, 4: 9566.09}}, 2: {"toughness": 626, "difficulty": {1: 1463.97, 2: 1576.58, 3: 1689.19, 4: 1827.8}}, 3: {"toughness": 3495, "difficulty": {1: 617.94, 2: 665.47, 3: 713.01, 4: 771.51}}})
    Enemy(id=16, name="Large Hollow Soldier", expansions=set(["Dark Souls The Board Game"]), difficultyTiers={1: {"toughness": 2128, "difficulty": {1: 620.81, 2: 668.56, 3: 716.32, 4: 775.09}}, 2: {"toughness": 4353, "difficulty": {1: 125.38, 2: 135.02, 3: 144.67, 4: 156.54}}, 3: {"toughness": 16023, "difficulty": {1: 59.46, 2: 64.03, 3: 68.6, 4: 74.23}}})
    Enemy(id=17, name="Mushroom Child", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 1616, "difficulty": {1: 578.16, 2: 578.16, 3: 578.16, 4: 578.16}}, 2: {"toughness": 3634, "difficulty": {1: 106.22, 2: 106.22, 3: 106.22, 4: 106.22}}, 3: {"toughness": 13031, "difficulty": {1: 51.7, 2: 51.7, 3: 51.7, 4: 51.7}}})
    Enemy(id=18, name="Mushroom Parent", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 624, "difficulty": {1: 2933.48, 2: 3159.14, 3: 3384.79, 4: 3662.51}}, 2: {"toughness": 1469, "difficulty": {1: 589.96, 2: 635.34, 3: 680.72, 4: 736.57}}, 3: {"toughness": 5890, "difficulty": {1: 246.54, 2: 265.51, 3: 284.47, 4: 307.81}}})
    Enemy(id=19, name="Necromancer", expansions=set(["Tomb of Giants"]), difficultyTiers={1: {"toughness": 1616, "difficulty": {1: 1347.58, 2: 1451.24, 3: 1554.89, 4: 1682.47}}, 2: {"toughness": 3634, "difficulty": {1: 395.45, 2: 425.86, 3: 456.27, 4: 493.73}}, 3: {"toughness": 13031, "difficulty": {1: 157.7, 2: 169.83, 3: 181.96, 4: 196.88}}})
    Enemy(id=20, name="Phalanx", expansions=set(["Painted World of Ariamis"]), difficultyTiers={1: {"toughness": 1837, "difficulty": {1: 888.17, 2: 932.03, 3: 975.88, 4: 1029.86}}, 2: {"toughness": 4019, "difficulty": {1: 164.68, 2: 172.97, 3: 181.25, 4: 191.44}}, 3: {"toughness": 14351, "difficulty": {1: 87.1, 2: 91.14, 3: 95.19, 4: 100.17}}})
    Enemy(id=21, name="Phalanx Hollow", expansions=set(["Painted World of Ariamis"]), health=1, difficultyTiers={1: {"toughness": 6182, "difficulty": {1: 106.02, 2: 106.02, 3: 106.02, 4: 106.02}}, 2: {"toughness": 11917, "difficulty": {1: 19.01, 2: 19.01, 3: 19.01, 4: 19.01}}, 3: {"toughness": 36112, "difficulty": {1: 11.49, 2: 11.49, 3: 11.49, 4: 11.49}}})
    Enemy(id=22, name="Plow Scarecrow", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 6182, "difficulty": {1: 233.69, 2: 233.69, 3: 233.69, 4: 233.69}}, 2: {"toughness": 11917, "difficulty": {1: 47.68, 2: 47.68, 3: 47.68, 4: 47.68}}, 3: {"toughness": 36112, "difficulty": {1: 37.6, 2: 37.6, 3: 37.6, 4: 37.6}}})
    Enemy(id=23, name="Sentinel", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), difficultyTiers={1: {"toughness": 474, "difficulty": {1: 3912.61, 2: 4213.58, 3: 4514.55, 4: 4884.98}}, 2: {"toughness": 1156, "difficulty": {1: 759.56, 2: 817.99, 3: 876.41, 4: 948.33}}, 3: {"toughness": 4941, "difficulty": {1: 297.76, 2: 320.66, 3: 343.57, 4: 371.76}}})
    Enemy(id=24, name="Shears Scarecrow", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 6182, "difficulty": {1: 182.7, 2: 196.76, 3: 210.81, 4: 228.11}}, 2: {"toughness": 11917, "difficulty": {1: 35.32, 2: 38.03, 3: 40.75, 4: 44.09}}, 3: {"toughness": 36112, "difficulty": {1: 28.35, 2: 30.53, 3: 32.71, 4: 35.4}}})
    Enemy(id=25, name="Silver Knight Greatbowman", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health=1, difficultyTiers={1: {"toughness": 4626, "difficulty": {1: 198.71, 2: 214, 3: 229.29, 4: 248.1}}, 2: {"toughness": 8659, "difficulty": {1: 36.69, 2: 39.51, 3: 42.34, 4: 45.81}}, 3: {"toughness": 29797, "difficulty": {1: 19.53, 2: 21.03, 3: 22.54, 4: 24.38}}})
    Enemy(id=26, name="Silver Knight Spearman", expansions=set(["Explorers"]), health=1, difficultyTiers={1: {"toughness": 3786, "difficulty": {1: 602.37, 2: 602.37, 3: 602.37, 4: 602.37}}, 2: {"toughness": 7864, "difficulty": {1: 140.53, 2: 140.53, 3: 140.53, 4: 140.53}}, 3: {"toughness": 28785, "difficulty": {1: 88.99, 2: 88.99, 3: 88.99, 4: 88.99}}})
    Enemy(id=27, name="Silver Knight Swordsman", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health=1, difficultyTiers={1: {"toughness": 3786, "difficulty": {1: 557.7, 2: 600.6, 3: 643.51, 4: 696.31}}, 2: {"toughness": 7864, "difficulty": {1: 118.07, 2: 127.15, 3: 136.23, 4: 147.41}}, 3: {"toughness": 28785, "difficulty": {1: 76.02, 2: 81.86, 3: 87.71, 4: 94.91}}})
    Enemy(id=28, name="Skeleton Archer", expansions=set(["Tomb of Giants"]), health=1, difficultyTiers={1: {"toughness": 6182, "difficulty": {1: 148.7, 2: 148.7, 3: 148.7, 4: 148.7}}, 2: {"toughness": 11917, "difficulty": {1: 26.66, 2: 26.66, 3: 26.66, 4: 26.66}}, 3: {"toughness": 36112, "difficulty": {1: 16.12, 2: 16.12, 3: 16.12, 4: 16.12}}})
    Enemy(id=29, name="Skeleton Beast", expansions=set(["Tomb of Giants"]), difficultyTiers={1: {"toughness": 718, "difficulty": {1: 5674.76, 2: 6111.28, 3: 6547.8, 4: 7085.05}}, 2: {"toughness": 1827, "difficulty": {1: 877.17, 2: 944.65, 3: 1012.12, 4: 1095.17}}, 3: {"toughness": 7683, "difficulty": {1: 498.49, 2: 536.84, 3: 575.18, 4: 622.38}}})
    Enemy(id=30, name="Skeleton Soldier", expansions=set(["Tomb of Giants"]), health=1, difficultyTiers={1: {"toughness": 3786, "difficulty": {1: 343.73, 2: 370.17, 3: 396.61, 4: 429.15}}, 2: {"toughness": 7864, "difficulty": {1: 110.4, 2: 118.89, 3: 127.38, 4: 137.84}}, 3: {"toughness": 28785, "difficulty": {1: 45.11, 2: 48.58, 3: 52.05, 4: 56.32}}})
    Enemy(id=31, name="Snow Rat", expansions=set(["Painted World of Ariamis"]), difficultyTiers={1: {"toughness": 6788, "difficulty": {1: 230.59, 2: 230.59, 3: 230.59, 4: 230.59}}, 2: {"toughness": 13374, "difficulty": {1: 69.29, 2: 69.29, 3: 69.29, 4: 69.29}}, 3: {"toughness": 39721, "difficulty": {1: 39.09, 2: 39.09, 3: 39.09, 4: 39.09}}})
    Enemy(id=32, name="Stone Guardian", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 665, "difficulty": {1: 3620, 2: 3898.46, 3: 4176.92, 4: 4519.64}}, 2: {"toughness": 1653, "difficulty": {1: 557.98, 2: 600.91, 3: 643.83, 4: 696.66}}, 3: {"toughness": 6893, "difficulty": {1: 238.19, 2: 256.51, 3: 274.83, 4: 297.38}}})
    Enemy(id=33, name="Stone Knight", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 373, "difficulty": {1: 2623.97, 2: 2623.97, 3: 2623.97, 4: 2623.97}}, 2: {"toughness": 778, "difficulty": {1: 648.59, 2: 648.59, 3: 648.59, 4: 648.59}}, 3: {"toughness": 4555, "difficulty": {1: 160.26, 2: 160.26, 3: 160.26, 4: 160.26}}})
    Enemy(id=34, name="Mimic", expansions=set(["The Sunless City"]), difficultyTiers={1: {"toughness": 1837, "difficulty": {1: 1720.54, 2: 1720.54, 3: 1720.54, 4: 1720.54}}, 2: {"toughness": 4019, "difficulty": {1: 381.1, 2: 381.1, 3: 381.1, 4: 381.1}}, 3: {"toughness": 14351, "difficulty": {1: 247.38, 2: 247.38, 3: 247.38, 4: 247.38}}})
    Enemy(id=35, name="Armorer Dennis", expansions=set(["Phantoms"]), cards=4, difficultyTiers={1: {"toughness": 484, "difficulty": {1: 4088.87, 2: 4228.3, 3: 4367.73, 4: 4539.33}}, 2: {"toughness": 1098.4, "difficulty": {1: 449.89, 2: 465.46, 3: 481.03, 4: 500.2}}, 3: {"toughness": 4143.8, "difficulty": {1: 93.2, 2: 96.1, 3: 99, 4: 102.57}}})
    Enemy(id=36, name="Fencer Sharron", expansions=set(["Phantoms"]), cards=5, difficultyTiers={1: {"toughness": 461.57, "difficulty": {1: 14740.26, 2: 14970.91, 3: 15201.57, 4: 15485.45}}, 2: {"toughness": 1037.29, "difficulty": {1: 1516.23, 2: 1540.31, 3: 1564.39, 4: 1594.03}}, 3: {"toughness": 3922, "difficulty": {1: 419.34, 2: 426.43, 3: 433.52, 4: 442.25}}})
    Enemy(id=37, name="Invader Brylex", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 243, "difficulty": {1: 39532.2, 2: 41207.45, 3: 42882.71, 4: 44944.56}}, 2: {"toughness": 647, "difficulty": {1: 3377, 2: 3519.2, 3: 3661.4, 4: 3836.41}}, 3: {"toughness": 2870, "difficulty": {1: 683.98, 2: 711.25, 3: 738.52, 4: 772.08}}})
    Enemy(id=38, name="Kirk, Knight of Thorns", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 809, "difficulty": {1: 4926.93, 2: 5093.36, 3: 5259.8, 4: 5464.65}}, 2: {"toughness": 1793, "difficulty": {1: 565.47, 2: 585.06, 3: 604.65, 4: 628.76}}, 3: {"toughness": 6574, "difficulty": {1: 135.38, 2: 139.67, 3: 143.95, 4: 149.23}}})
    Enemy(id=39, name="Longfinger Kirk", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 257, "difficulty": {1: 41717.95, 2: 42690, 3: 43662.04, 4: 44858.41}}, 2: {"toughness": 685, "difficulty": {1: 4077.99, 2: 4170.72, 3: 4263.45, 4: 4377.58}}, 3: {"toughness": 3114, "difficulty": {1: 1022.33, 2: 1042.04, 3: 1061.74, 4: 1085.99}}})
    Enemy(id=40, name="Maldron the Assassin", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 736, "difficulty": {1: 10897.77, 2: 11173, 3: 11448.24, 4: 11786.99}}, 2: {"toughness": 1653, "difficulty": {1: 1117.42, 2: 1144.46, 3: 1171.49, 4: 1204.76}}, 3: {"toughness": 6166, "difficulty": {1: 360.72, 2: 369.52, 3: 378.31, 4: 389.14}}})
    Enemy(id=41, name="Maneater Mildred", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 539.8, "difficulty": {1: 9249.26, 2: 9960.74, 3: 10672.22, 4: 11547.89}}, 2: {"toughness": 1238.6, "difficulty": {1: 766.43, 2: 825.38, 3: 884.34, 4: 956.9}}, 3: {"toughness": 4719.6, "difficulty": {1: 220.58, 2: 237.55, 3: 254.52, 4: 275.4}}})
    Enemy(id=42, name="Marvelous Chester", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 498, "difficulty": {1: 22633.74, 2: 22767.14, 3: 22900.55, 4: 23064.74}}, 2: {"toughness": 1141, "difficulty": {1: 2408.75, 2: 2422.85, 3: 2436.95, 4: 2454.31}}, 3: {"toughness": 4195, "difficulty": {1: 690.26, 2: 695.31, 3: 700.37, 4: 706.59}}})
    Enemy(id=43, name="Melinda the Butcher", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 794.6, "difficulty": {1: 4702.3, 2: 4900.97, 3: 5099.65, 4: 5344.17}}, 2: {"toughness": 1655.8, "difficulty": {1: 413.09, 2: 431.73, 3: 450.38, 4: 473.33}}, 3: {"toughness": 5673.8, "difficulty": {1: 128.67, 2: 134.4, 3: 140.14, 4: 147.2}}})
    Enemy(id=44, name="Oliver the Collector", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 673, "difficulty": {1: 8335.64, 2: 8639.14, 3: 8942.64, 4: 9316.19}}, 2: {"toughness": 1455.43, "difficulty": {1: 756.43, 2: 783.07, 3: 809.72, 4: 842.52}}, 3: {"toughness": 5516.71, "difficulty": {1: 198.14, 2: 204.2, 3: 210.26, 4: 217.71}}})
    Enemy(id=45, name="Paladin Leeroy", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 270, "difficulty": {1: 20568.05, 2: 21930.22, 3: 23292.39, 4: 24968.91}}, 2: {"toughness": 656, "difficulty": {1: 1940.78, 2: 2068.03, 3: 2195.28, 4: 2351.9}}, 3: {"toughness": 3026.2, "difficulty": {1: 426.57, 2: 452.9, 3: 479.24, 4: 511.65}}})
    Enemy(id=46, name="Xanthous King Jeremiah", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 4118.5, "difficulty": {1: 2962.7, 2: 3150.28, 3: 3337.87, 4: 3568.74}}, 2: {"toughness": 8824, "difficulty": {1: 339.59, 2: 361.11, 3: 382.63, 4: 409.12}}, 3: {"toughness": 14598, "difficulty": {1: 94.64, 2: 100.5, 3: 106.36, 4: 113.58}}})
    Enemy(id=47, name="Hungry Mimic", expansions=set(["Explorers"]), cards=4, difficultyTiers={1: {"toughness": 527, "difficulty": {1: 9931.96, 2: 10292.55, 3: 10653.15, 4: 11096.96}}, 2: {"toughness": 1213, "difficulty": {1: 937.57, 2: 971.39, 3: 1005.2, 4: 1046.81}}, 3: {"toughness": 4568, "difficulty": {1: 274.56, 2: 283.97, 3: 293.39, 4: 304.98}}})
    Enemy(id=48, name="Voracious Mimic", expansions=set(["Explorers"]), cards=4, difficultyTiers={1: {"toughness": 203, "difficulty": {1: 35862.17, 2: 37113.2, 3: 38364.22, 4: 39903.94}}, 2: {"toughness": 537, "difficulty": {1: 3260.64, 2: 3373.7, 3: 3486.75, 4: 3625.9}}, 3: {"toughness": 2460, "difficulty": {1: 771.94, 2: 797.13, 3: 822.33, 4: 853.34}}})

    bosses = {
        "Asylum Demon": {"name": "Asylum Demon", "type": "boss", "level": "Mini Boss", "expansions": set(["Asylum Demon"]), "cards": 4},
        "Black Knight": {"name": "Black Knight", "type": "boss", "level": "Mini Boss", "expansions": set(["Tomb of Giants"]), "cards": 4},
        "Boreal Outrider Knight": {"name": "Boreal Outrider Knight", "type": "boss", "level": "Mini Boss", "expansions": set(["Dark Souls The Board Game"]), "cards": 4},
        "Gargoyle": {"name": "Gargoyle", "type": "boss", "level": "Mini Boss", "expansions": set(["Dark Souls The Board Game"]), "cards": 4},
        "Heavy Knight": {"name": "Heavy Knight", "type": "boss", "level": "Mini Boss", "expansions": set(["Painted World of Ariamis"]), "cards": 4},
        "Old Dragonslayer": {"name": "Old Dragonslayer", "type": "boss", "level": "Mini Boss", "expansions": set(["Explorers"]), "cards": 4},
        "Titanite Demon": {"name": "Titanite Demon", "type": "boss", "level": "Mini Boss", "expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "cards": 4},
        "Winged Knight": {"name": "Winged Knight", "type": "boss", "level": "Mini Boss", "expansions": set(["Dark Souls The Board Game"]), "cards": 4},
        "Artorias": {"name": "Artorias", "type": "boss", "level": "Main Boss", "expansions": set(["Darkroot"]), "cards": 5},
        "Crossbreed Priscilla": {"name": "Crossbreed Priscilla", "type": "boss", "level": "Main Boss", "expansions": set(["Painted World of Ariamis"]), "cards": 5},
        "Dancer of the Boreal Valley": {"name": "Dancer of the Boreal Valley", "type": "boss", "level": "Main Boss", "expansions": set(["Dark Souls The Board Game"]), "cards": 5},
        "Gravelord Nito": {"name": "Gravelord Nito", "type": "boss", "level": "Main Boss", "expansions": set(["Tomb of Giants"]), "cards": 5},
        "Great Grey Wolf Sif": {"name": "Great Grey Wolf Sif", "type": "boss", "level": "Main Boss", "expansions": set(["Darkroot"]), "cards": 5},
        "Ornstein & Smough": {"name": "Ornstein & Smough", "type": "boss", "level": "Main Boss", "expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "cards": 5},
        "Sir Alonne": {"name": "Sir Alonne", "type": "boss", "level": "Main Boss", "expansions": set(["Iron Keep"]), "cards": 5},
        "Smelter Demon": {"name": "Smelter Demon", "type": "boss", "level": "Main Boss", "expansions": set(["Iron Keep"]), "cards": 5},
        "The Pursuer": {"name": "The Pursuer", "type": "boss", "level": "Main Boss", "expansions": set(["Explorers"]), "cards": 8},
        "Black Dragon Kalameet": {"name": "Black Dragon Kalameet", "type": "boss", "level": "Mega Boss", "expansions": set(["Black Dragon Kalameet"]), "cards": 6},
        "Executioner Chariot": {"name": "Executioner Chariot", "type": "boss", "level": "Mega Boss", "expansions": set(["Executioner Chariot"]), "cards": 5},
        "Gaping Dragon": {"name": "Gaping Dragon", "type": "boss", "level": "Mega Boss", "expansions": set(["Gaping Dragon"]), "cards": 6},
        "Guardian Dragon": {"name": "Guardian Dragon", "type": "boss", "level": "Mega Boss", "expansions": set(["Guardian Dragon"]), "cards": 5},
        "Manus, Father of the Abyss": {"name": "Manus, Father of the Abyss", "type": "boss", "level": "Mega Boss", "expansions": set(["Manus, Father of the Abyss"]), "cards": 5},
        "Old Iron King": {"name": "Old Iron King", "type": "boss", "level": "Mega Boss", "expansions": set(["Old Iron King"]), "cards": 6},
        "Stray Demon": {"name": "Stray Demon", "type": "boss", "level": "Mega Boss", "expansions": set(["Asylum Demon"]), "cards": 6},
        "The Four Kings": {"name": "The Four Kings", "type": "boss", "level": "Mega Boss", "expansions": set(["The Four Kings"]), "cards": 4},
        "The Last Giant": {"name": "The Last Giant", "type": "boss", "level": "Mega Boss", "expansions": set(["The Last Giant"]), "cards": 6},
        "Vordt of the Boreal Valley": {"name": "Vordt of the Boreal Valley", "type": "boss", "level": "Mega Boss", "expansions": set(["Vordt of the Boreal Valley"]), "cards": 0}
    }

except Exception as e:
    log(e, exception=True)
    raise