try:
    from dsbg_shuffle_utility import log, baseFolder, pathSep


    enemies = []
    enemyIds = {}
    enemiesDict = {}
    reach = []


    class Enemy:
        def __init__(self, id, name, expansions, difficultyTiers, cards=1, health=None, threat=None) -> None:
            enemiesDict[name] = self
            enemies.append(self)
            enemyIds[id] = self
            self.id = id
            self.name = name
            self.expansions = expansions
            self.cards = cards
            self.difficultyTiers = difficultyTiers
            self.threat = threat
            
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


    Enemy(id=1, name="Alonne Bow Knight", expansions=set(["Iron Keep"]), threat=2, health=1, difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 75.66, 2: 75.66, 3: 75.66, 4: 75.66}}, 2: {"toughness": 42968, "difficulty": {1: 14.04, 2: 14.04, 3: 14.04, 4: 14.04}}, 3: {"toughness": 88396, "difficulty": {1: 40.82, 2: 40.82, 3: 40.82, 4: 40.82}}})
    Enemy(id=2, name="Alonne Knight Captain", expansions=set(["Iron Keep"]), threat=8, difficultyTiers={1: {"toughness": 3975, "difficulty": {1: 669.97, 2: 669.97, 3: 669.97, 4: 669.97}}, 2: {"toughness": 4949, "difficulty": {1: 177.52, 2: 177.52, 3: 177.52, 4: 177.52}}, 3: {"toughness": 17101, "difficulty": {1: 208.48, 2: 208.48, 3: 208.48, 4: 208.48}}})
    Enemy(id=3, name="Alonne Sword Knight", expansions=set(["Iron Keep"]), threat=5, health=1, difficultyTiers={1: {"toughness": 17854, "difficulty": {1: 146.64, 2: 146.64, 3: 146.64, 4: 146.64}}, 2: {"toughness": 17195, "difficulty": {1: 37.05, 2: 37.05, 3: 37.05, 4: 37.05}}, 3: {"toughness": 57021, "difficulty": {1: 55.69, 2: 55.69, 3: 55.69, 4: 55.69}}})
    Enemy(id=4, name="Black Hollow Mage", expansions=set(["Executioner Chariot"]), threat=8, difficultyTiers={1: {"toughness": 2505, "difficulty": {1: 1188.15, 2: 1188.15, 3: 1188.15, 4: 1188.15}}, 2: {"toughness": 4306, "difficulty": {1: 206.95, 2: 206.95, 3: 206.95, 4: 206.95}}, 3: {"toughness": 15121, "difficulty": {1: 260.16, 2: 260.16, 3: 260.16, 4: 260.16}}})
    Enemy(id=5, name="Bonewheel Skeleton", expansions=set(["Painted World of Ariamis"]), threat=7, health=1, difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 156.91, 2: 168.98, 3: 181.05, 4: 195.91}}, 2: {"toughness": 42968, "difficulty": {1: 29.12, 2: 31.36, 3: 33.6, 4: 36.36}}, 3: {"toughness": 88396, "difficulty": {1: 84.67, 2: 91.18, 3: 97.69, 4: 105.71}}})
    Enemy(id=6, name="Crossbow Hollow", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), threat=2, health=1, difficultyTiers={1: {"toughness": 40923, "difficulty": {1: 23.51, 2: 23.51, 3: 23.51, 4: 23.51}}, 2: {"toughness": 54957, "difficulty": {1: 5.08, 2: 5.08, 3: 5.08, 4: 5.08}}, 3: {"toughness": 89972, "difficulty": {1: 8.58, 2: 8.58, 3: 8.58, 4: 8.58}}})
    Enemy(id=7, name="Crow Demon", expansions=set(["Painted World of Ariamis"]), threat=9, difficultyTiers={1: {"toughness": 6001, "difficulty": {1: 1579.49, 2: 1700.99, 3: 1822.48, 4: 1972.02}}, 2: {"toughness": 9397, "difficulty": {1: 275.69, 2: 296.89, 3: 318.1, 4: 344.2}}, 3: {"toughness": 30671, "difficulty": {1: 553.28, 2: 595.84, 3: 638.4, 4: 690.78}}})
    Enemy(id=8, name="Demonic Foliage", expansions=set(["Darkroot"]), threat=3, difficultyTiers={1: {"toughness": 33314, "difficulty": {1: 78.59, 2: 78.59, 3: 78.59, 4: 78.59}}, 2: {"toughness": 32175, "difficulty": {1: 19.8, 2: 19.8, 3: 19.8, 4: 19.8}}, 3: {"toughness": 64201, "difficulty": {1: 49.46, 2: 49.46, 3: 49.46, 4: 49.46}}})
    Enemy(id=9, name="Engorged Zombie", expansions=set(["Painted World of Ariamis"]), threat=8, difficultyTiers={1: {"toughness": 17854, "difficulty": {1: 51.96, 2: 51.96, 3: 51.96, 4: 51.96}}, 2: {"toughness": 17195, "difficulty": {1: 11.9, 2: 11.9, 3: 11.9, 4: 11.9}}, 3: {"toughness": 57021, "difficulty": {1: 13.47, 2: 13.47, 3: 13.47, 4: 13.47}}})
    Enemy(id=10, name="Falchion Skeleton", expansions=set(["Executioner Chariot"]), threat=4, health=1, difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 133.9, 2: 133.9, 3: 133.9, 4: 133.9}}, 2: {"toughness": 42968, "difficulty": {1: 40.48, 2: 40.48, 3: 40.48, 4: 40.48}}, 3: {"toughness": 88396, "difficulty": {1: 114.45, 2: 114.45, 3: 114.45, 4: 114.45}}})
    Enemy(id=11, name="Firebomb Hollow", expansions=set(["Explorers"]), threat=2, health=1, difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 25.24, 2: 27.19, 3: 29.13, 4: 31.52}}, 2: {"toughness": 42968, "difficulty": {1: 6.42, 2: 6.92, 3: 7.41, 4: 8.02}}, 3: {"toughness": 88396, "difficulty": {1: 8.63, 2: 9.29, 3: 9.95, 4: 10.77}}})
    Enemy(id=12, name="Giant Skeleton Archer", expansions=set(["Tomb of Giants"]), threat=1, difficultyTiers={1: {"toughness": 10311, "difficulty": {1: 475.19, 2: 478.3, 3: 481.41, 4: 485.24}}, 2: {"toughness": 13939, "difficulty": {1: 84.46, 2: 84.91, 3: 85.36, 4: 85.91}}, 3: {"toughness": 33839, "difficulty": {1: 217.19, 2: 218.3, 3: 219.42, 4: 220.79}}})
    Enemy(id=13, name="Giant Skeleton Soldier", expansions=set(["Tomb of Giants"]), threat=2, difficultyTiers={1: {"toughness": 10311, "difficulty": {1: 301.88, 2: 303.92, 3: 305.96, 4: 308.47}}, 2: {"toughness": 13939, "difficulty": {1: 52.23, 2: 52.43, 3: 52.64, 4: 52.89}}, 3: {"toughness": 33839, "difficulty": {1: 107.59, 2: 108.04, 3: 108.49, 4: 109.04}}})
    Enemy(id=14, name="Hollow Soldier", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), threat=5, health=1, difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 23.54, 2: 23.54, 3: 23.54, 4: 23.54}}, 2: {"toughness": 42968, "difficulty": {1: 2.46, 2: 2.46, 3: 2.46, 4: 2.46}}, 3: {"toughness": 88396, "difficulty": {1: 7.52, 2: 7.52, 3: 7.52, 4: 7.52}}})
    Enemy(id=15, name="Ironclad Soldier", expansions=set(["Iron Keep"]), threat=6, difficultyTiers={1: {"toughness": 945, "difficulty": {1: 3350.13, 2: 3607.83, 3: 3865.53, 4: 4182.7}}, 2: {"toughness": 1614, "difficulty": {1: 304.04, 2: 327.43, 3: 350.82, 4: 379.61}}, 3: {"toughness": 6644, "difficulty": {1: 606.29, 2: 652.93, 3: 699.56, 4: 756.96}}})
    Enemy(id=16, name="Large Hollow Soldier", expansions=set(["Dark Souls The Board Game"]), threat=6, difficultyTiers={1: {"toughness": 12952, "difficulty": {1: 155.65, 2: 167.62, 3: 179.59, 4: 194.33}}, 2: {"toughness": 18934, "difficulty": {1: 16.24, 2: 17.49, 3: 18.74, 4: 20.28}}, 3: {"toughness": 37265, "difficulty": {1: 53.36, 2: 57.46, 3: 61.57, 4: 66.62}}})
    Enemy(id=17, name="Mushroom Child", expansions=set(["Darkroot"]), threat=2, difficultyTiers={1: {"toughness": 6001, "difficulty": {1: 237.58, 2: 237.58, 3: 237.58, 4: 237.58}}, 2: {"toughness": 9397, "difficulty": {1: 23.15, 2: 23.15, 3: 23.15, 4: 23.15}}, 3: {"toughness": 30671, "difficulty": {1: 45.85, 2: 45.85, 3: 45.85, 4: 45.85}}})
    Enemy(id=18, name="Mushroom Parent", expansions=set(["Darkroot"]), threat=1, difficultyTiers={1: {"toughness": 1756, "difficulty": {1: 1596.95, 2: 1719.8, 3: 1842.64, 4: 1993.83}}, 2: {"toughness": 3363, "difficulty": {1: 153.01, 2: 164.79, 3: 176.56, 4: 191.04}}, 3: {"toughness": 10340, "difficulty": {1: 334.12, 2: 359.82, 3: 385.52, 4: 417.15}}})
    Enemy(id=19, name="Necromancer", expansions=set(["Tomb of Giants"]), threat=7, difficultyTiers={1: {"toughness": 6001, "difficulty": {1: 477.83, 2: 514.59, 3: 551.34, 4: 596.58}}, 2: {"toughness": 9397, "difficulty": {1: 118.83, 2: 127.95, 3: 137.11, 4: 148.35}}, 3: {"toughness": 30671, "difficulty": {1: 345.71, 2: 372.31, 3: 398.9, 4: 431.61}}})
    Enemy(id=20, name="Phalanx", expansions=set(["Painted World of Ariamis"]), threat=4, difficultyTiers={1: {"toughness": 10311, "difficulty": {1: 234.16, 2: 246.09, 3: 258.01, 4: 272.68}}, 2: {"toughness": 13939, "difficulty": {1: 25.77, 2: 27.12, 3: 28.46, 4: 30.12}}, 3: {"toughness": 33839, "difficulty": {1: 71.87, 2: 75.45, 3: 79.04, 4: 83.45}}})
    Enemy(id=21, name="Phalanx Hollow", expansions=set(["Painted World of Ariamis"]), threat=4, health=1, difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 26.39, 2: 26.39, 3: 26.39, 4: 26.39}}, 2: {"toughness": 42968, "difficulty": {1: 2.76, 2: 2.76, 3: 2.76, 4: 2.76}}, 3: {"toughness": 88396, "difficulty": {1: 8.43, 2: 8.43, 3: 8.43, 4: 8.43}}})
    Enemy(id=22, name="Plow Scarecrow", expansions=set(["Darkroot"]), threat=4, difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 74.76, 2: 74.76, 3: 74.76, 4: 74.76}}, 2: {"toughness": 42968, "difficulty": {1: 13.87, 2: 13.87, 3: 13.87, 4: 13.87}}, 3: {"toughness": 88396, "difficulty": {1: 40.34, 2: 40.34, 3: 40.34, 4: 40.34}}})
    Enemy(id=23, name="Sentinel", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), threat=9, difficultyTiers={1: {"toughness": 4192, "difficulty": {1: 861.9, 2: 928.2, 3: 994.5, 4: 1076.1}}, 2: {"toughness": 5068, "difficulty": {1: 199.64, 2: 215, 3: 230.36, 4: 249.26}}, 3: {"toughness": 11264, "difficulty": {1: 476.58, 2: 513.24, 3: 549.9, 4: 595.02}}})
    Enemy(id=24, name="Shears Scarecrow", expansions=set(["Darkroot"]), threat=8, difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 52.18, 2: 56.19, 3: 60.2, 4: 65.14}}, 2: {"toughness": 42968, "difficulty": {1: 7.02, 2: 7.56, 3: 8.1, 4: 8.77}}, 3: {"toughness": 88396, "difficulty": {1: 21.56, 2: 23.21, 3: 24.87, 4: 26.91}}})
    Enemy(id=25, name="Silver Knight Greatbowman", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), threat=3, health=1, difficultyTiers={1: {"toughness": 36573, "difficulty": {1: 49.51, 2: 53.32, 3: 57.13, 4: 61.82}}, 2: {"toughness": 44164, "difficulty": {1: 8.2, 2: 8.83, 3: 9.46, 4: 10.24}}, 3: {"toughness": 65777, "difficulty": {1: 25.75, 2: 27.73, 3: 29.71, 4: 32.15}}})
    Enemy(id=26, name="Silver Knight Spearman", expansions=set(["Explorers"]), threat=8, health=1, difficultyTiers={1: {"toughness": 33314, "difficulty": {1: 104.37, 2: 104.37, 3: 104.37, 4: 104.37}}, 2: {"toughness": 32175, "difficulty": {1: 19.47, 2: 19.47, 3: 19.47, 4: 19.47}}, 3: {"toughness": 64201, "difficulty": {1: 81.92, 2: 81.92, 3: 81.92, 4: 81.92}}})
    Enemy(id=27, name="Silver Knight Swordsman", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), threat=7, health=1, difficultyTiers={1: {"toughness": 33314, "difficulty": {1: 122.62, 2: 132.05, 3: 141.48, 4: 153.09}}, 2: {"toughness": 32175, "difficulty": {1: 31.04, 2: 33.43, 3: 35.82, 4: 38.76}}, 3: {"toughness": 64201, "difficulty": {1: 97.36, 2: 104.85, 3: 112.34, 4: 121.55}}})
    Enemy(id=28, name="Skeleton Archer", expansions=set(["Tomb of Giants"]), threat=3, health=1, difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 48.08, 2: 48.08, 3: 48.08, 4: 48.08}}, 2: {"toughness": 42968, "difficulty": {1: 8.43, 2: 8.43, 3: 8.43, 4: 8.43}}, 3: {"toughness": 88396, "difficulty": {1: 19.16, 2: 19.16, 3: 19.16, 4: 19.16}}})
    Enemy(id=29, name="Skeleton Beast", expansions=set(["Tomb of Giants"]), threat=6, difficultyTiers={1: {"toughness": 3975, "difficulty": {1: 1319.55, 2: 1421.05, 3: 1522.55, 4: 1647.48}}, 2: {"toughness": 4949, "difficulty": {1: 185.8, 2: 200.09, 3: 214.39, 4: 231.98}}, 3: {"toughness": 17101, "difficulty": {1: 358.06, 2: 385.61, 3: 413.15, 4: 447.05}}})
    Enemy(id=30, name="Skeleton Soldier", expansions=set(["Tomb of Giants"]), threat=5, health=1, difficultyTiers={1: {"toughness": 33314, "difficulty": {1: 105.83, 2: 113.97, 3: 122.11, 4: 132.13}}, 2: {"toughness": 32175, "difficulty": {1: 29.7, 2: 31.98, 3: 34.27, 4: 37.08}}, 3: {"toughness": 64201, "difficulty": {1: 106.85, 2: 115.07, 3: 123.29, 4: 133.4}}})
    Enemy(id=31, name="Snow Rat", expansions=set(["Painted World of Ariamis"]), threat=1, difficultyTiers={1: {"toughness": 38873, "difficulty": {1: 78.39, 2: 78.39, 3: 78.39, 4: 78.39}}, 2: {"toughness": 46157, "difficulty": {1: 22.85, 2: 22.85, 3: 22.85, 4: 22.85}}, 3: {"toughness": 91859, "difficulty": {1: 73.77, 2: 73.77, 3: 73.77, 4: 73.77}}})
    Enemy(id=32, name="Stone Guardian", expansions=set(["Darkroot"]), threat=6, difficultyTiers={1: {"toughness": 2472, "difficulty": {1: 1910.86, 2: 2057.85, 3: 2204.84, 4: 2385.75}}, 2: {"toughness": 4306, "difficulty": {1: 245.77, 2: 264.67, 3: 283.58, 4: 306.84}}, 3: {"toughness": 15121, "difficulty": {1: 340.23, 2: 366.41, 3: 392.58, 4: 424.79}}})
    Enemy(id=33, name="Stone Knight", expansions=set(["Darkroot"]), threat=7, difficultyTiers={1: {"toughness": 3123, "difficulty": {1: 465.88, 2: 465.88, 3: 465.88, 4: 465.88}}, 2: {"toughness": 2471, "difficulty": {1: 137.13, 2: 137.13, 3: 137.13, 4: 137.13}}, 3: {"toughness": 9691, "difficulty": {1: 161.67, 2: 161.67, 3: 161.67, 4: 161.67}}})
    Enemy(id=34, name="Mimic", expansions=set(["The Sunless City"]), threat=4, difficultyTiers={1: {"toughness": 10311, "difficulty": {1: 590.45, 2: 590.45, 3: 590.45, 4: 590.45}}, 2: {"toughness": 13939, "difficulty": {1: 119.38, 2: 119.38, 3: 119.38, 4: 119.38}}, 3: {"toughness": 33839, "difficulty": {1: 322.1, 2: 322.1, 3: 322.1, 4: 322.1}}})
    Enemy(id=35, name="Armorer Dennis", expansions=set(["Phantoms"]), threat=10, cards=4, difficultyTiers={1: {"toughness": 1677, "difficulty": {1: 572.22, 2: 592, 3: 611.78, 4: 636.12}}, 2: {"toughness": 2987.6, "difficulty": {1: 99.41, 2: 102.96, 3: 106.51, 4: 110.88}}, 3: {"toughness": 8811.4, "difficulty": {1: 143.95, 2: 148.69, 3: 153.44, 4: 159.29}}})
    Enemy(id=36, name="Fencer Sharron", expansions=set(["Phantoms"]), threat=10, cards=5, difficultyTiers={1: {"toughness": 2534, "difficulty": {1: 1475.48, 2: 1513.74, 3: 1552, 4: 1599.08}}, 2: {"toughness": 3749.14, "difficulty": {1: 248.86, 2: 254.15, 3: 259.44, 4: 265.95}}, 3: {"toughness": 8927.57, "difficulty": {1: 580.44, 2: 592.43, 3: 604.42, 4: 619.17}}})
    Enemy(id=37, name="Invader Brylex", expansions=set(["Phantoms"]), threat=10, cards=3, difficultyTiers={1: {"toughness": 1360, "difficulty": {1: 3419.26, 2: 3565.43, 3: 3711.59, 4: 3891.49}}, 2: {"toughness": 1839, "difficulty": {1: 681.69, 2: 710.42, 3: 739.15, 4: 774.51}}, 3: {"toughness": 6374, "difficulty": {1: 1016.7, 2: 1060.45, 3: 1104.21, 4: 1158.06}}})
    Enemy(id=38, name="Kirk, Knight of Thorns", expansions=set(["Phantoms"]), threat=10, cards=3, difficultyTiers={1: {"toughness": 4599, "difficulty": {1: 416.57, 2: 430.66, 3: 444.75, 4: 462.08}}, 2: {"toughness": 6715, "difficulty": {1: 81.22, 2: 84.03, 3: 86.84, 4: 90.31}}, 3: {"toughness": 15341, "difficulty": {1: 199.7, 2: 206.4, 3: 213.1, 4: 221.35}}})
    Enemy(id=39, name="Longfinger Kirk", expansions=set(["Phantoms"]), threat=10, cards=3, difficultyTiers={1: {"toughness": 1455, "difficulty": {1: 3502.85, 2: 3584.84, 3: 3666.82, 4: 3767.73}}, 2: {"toughness": 1919, "difficulty": {1: 761.74, 2: 779.51, 3: 797.27, 4: 819.14}}, 3: {"toughness": 6851, "difficulty": {1: 1394.78, 2: 1424.45, 3: 1454.11, 4: 1490.63}}})
    Enemy(id=40, name="Maldron the Assassin", expansions=set(["Phantoms"]), threat=10, cards=3, difficultyTiers={1: {"toughness": 3032, "difficulty": {1: 1274.67, 2: 1307.03, 3: 1339.38, 4: 1379.2}}, 2: {"toughness": 3551, "difficulty": {1: 276.66, 2: 283.34, 3: 290.01, 4: 298.23}}, 3: {"toughness": 6733, "difficulty": {1: 927.83, 2: 950.11, 3: 972.38, 4: 999.81}}})
    Enemy(id=41, name="Maneater Mildred", expansions=set(["Phantoms"]), threat=10, cards=3, difficultyTiers={1: {"toughness": 2315.6, "difficulty": {1: 1352.88, 2: 1456.94, 3: 1561.01, 4: 1689.09}}, 2: {"toughness": 3787, "difficulty": {1: 158.18, 2: 170.35, 3: 182.52, 4: 197.49}}, 3: {"toughness": 9182, "difficulty": {1: 339.16, 2: 365.25, 3: 391.34, 4: 423.45}}})
    Enemy(id=42, name="Marvelous Chester", expansions=set(["Phantoms"]), threat=10, cards=3, difficultyTiers={1: {"toughness": 1874, "difficulty": {1: 2890.28, 2: 2907.39, 3: 2924.49, 4: 2945.55}}, 2: {"toughness": 3216, "difficulty": {1: 453.92, 2: 456.53, 3: 459.15, 4: 462.37}}, 3: {"toughness": 9666, "difficulty": {1: 912.77, 2: 918.71, 3: 924.65, 4: 931.97}}})
    Enemy(id=43, name="Melinda the Butcher", expansions=set(["Phantoms"]), threat=10, cards=3, difficultyTiers={1: {"toughness": 4139.6, "difficulty": {1: 535.55, 2: 562.29, 3: 589.02, 4: 621.93}}, 2: {"toughness": 6151, "difficulty": {1: 70.07, 2: 73.69, 3: 77.31, 4: 81.76}}, 3: {"toughness": 12534.8, "difficulty": {1: 169.97, 2: 178.61, 3: 187.25, 4: 197.89}}})
    Enemy(id=44, name="Oliver the Collector", expansions=set(["Phantoms"]), threat=10, cards=3, difficultyTiers={1: {"toughness": 4095.71, "difficulty": {1: 947.49, 2: 985.25, 3: 1023.01, 4: 1069.49}}, 2: {"toughness": 5825.71, "difficulty": {1: 131.73, 2: 136.83, 3: 141.93, 4: 148.21}}, 3: {"toughness": 12000, "difficulty": {1: 283.54, 2: 293.1, 3: 302.66, 4: 314.42}}})
    Enemy(id=45, name="Paladin Leeroy", expansions=set(["Phantoms"]), threat=10, cards=3, difficultyTiers={1: {"toughness": 1686, "difficulty": {1: 2308.82, 2: 2472.96, 3: 2637.1, 4: 2839.11}}, 2: {"toughness": 2047.4, "difficulty": {1: 404.6, 2: 432.54, 3: 460.48, 4: 494.86}}, 3: {"toughness": 4575.8, "difficulty": {1: 888.4, 2: 945.88, 3: 1003.36, 4: 1074.1}}})
    Enemy(id=46, name="Xanthous King Jeremiah", expansions=set(["Phantoms"]), threat=10, cards=3, difficultyTiers={1: {"toughness": 4931, "difficulty": {1: 566.08, 2: 601.98, 3: 637.89, 4: 682.08}}, 2: {"toughness": 7695, "difficulty": {1: 108.34, 2: 115.2, 3: 122.07, 4: 130.53}}, 3: {"toughness": 17992, "difficulty": {1: 201.81, 2: 214.57, 3: 227.32, 4: 243.03}}})
    Enemy(id=47, name="Hungry Mimic", expansions=set(["Explorers"]), threat=10, cards=4, difficultyTiers={1: {"toughness": 3032, "difficulty": {1: 838.69, 2: 869.16, 3: 899.62, 4: 937.11}}, 2: {"toughness": 4505, "difficulty": {1: 137.56, 2: 142.59, 3: 147.62, 4: 153.81}}, 3: {"toughness": 10513, "difficulty": {1: 348.15, 2: 360.57, 3: 372.99, 4: 388.28}}})
    Enemy(id=48, name="Voracious Mimic", expansions=set(["Explorers"]), threat=10, cards=4, difficultyTiers={1: {"toughness": 1139, "difficulty": {1: 3150.4, 2: 3262.92, 3: 3375.44, 4: 3513.93}}, 2: {"toughness": 1569, "difficulty": {1: 625.8, 2: 648.28, 3: 670.76, 4: 698.42}}, 3: {"toughness": 5421, "difficulty": {1: 1121.31, 2: 1160.46, 3: 1199.62, 4: 1247.8}}})

    bosses = {
        "Asylum Demon": {"name": "Asylum Demon", "type": "boss", "level": "Mini Boss", "encounters": [1, 1, 1, 2], "expansions": set(["Asylum Demon"]), "cards": 4},
        "Black Knight": {"name": "Black Knight", "type": "boss", "level": "Mini Boss", "encounters": [1, 1, 1, 2], "expansions": set(["Tomb of Giants"]), "cards": 4},
        "Boreal Outrider Knight": {"name": "Boreal Outrider Knight", "type": "boss", "level": "Mini Boss", "encounters": [1, 1, 2, 2], "expansions": set(["Dark Souls The Board Game"]), "cards": 4},
        "Gargoyle": {"name": "Gargoyle", "type": "boss", "level": "Mini Boss", "encounters": [1, 1, 1, 2], "expansions": set(["Dark Souls The Board Game"]), "cards": 4},
        "Heavy Knight": {"name": "Heavy Knight", "type": "boss", "level": "Mini Boss", "encounters": [1, 1, 1, 2], "expansions": set(["Painted World of Ariamis"]), "cards": 4},
        "Old Dragonslayer": {"name": "Old Dragonslayer", "type": "boss", "level": "Mini Boss", "encounters": [1, 1, 1, 2], "expansions": set(["Explorers"]), "cards": 4},
        "Titanite Demon": {"name": "Titanite Demon", "type": "boss", "level": "Mini Boss", "encounters": [1, 2, 2, 2], "expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "cards": 4},
        "Winged Knight": {"name": "Winged Knight", "type": "boss", "level": "Mini Boss", "encounters": [1, 1, 2, 2], "expansions": set(["Dark Souls The Board Game"]), "cards": 4},
        "Artorias": {"name": "Artorias", "type": "boss", "level": "Main Boss", "encounters": [3, 3, 3, 3], "expansions": set(["Darkroot"]), "cards": 5},
        "Crossbreed Priscilla": {"name": "Crossbreed Priscilla", "type": "boss", "level": "Main Boss", "encounters": [2, 2, 3, 3], "expansions": set(["Painted World of Ariamis"]), "cards": 5},
        "Dancer of the Boreal Valley": {"name": "Dancer of the Boreal Valley", "type": "boss", "level": "Main Boss", "encounters": [2, 2, 3, 3], "expansions": set(["Dark Souls The Board Game"]), "cards": 5},
        "Gravelord Nito": {"name": "Gravelord Nito", "type": "boss", "level": "Main Boss", "encounters": [2, 2, 3, 3], "expansions": set(["Tomb of Giants"]), "cards": 5},
        "Great Grey Wolf Sif": {"name": "Great Grey Wolf Sif", "type": "boss", "level": "Main Boss", "encounters": [2, 3, 3, 3], "expansions": set(["Darkroot"]), "cards": 5},
        "Ornstein & Smough": {"name": "Ornstein & Smough", "type": "boss", "level": "Main Boss", "encounters": [2, 3, 3, 3], "expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "cards": 5},
        "Sir Alonne": {"name": "Sir Alonne", "type": "boss", "level": "Main Boss", "encounters": [2, 2, 2, 3], "expansions": set(["Iron Keep"]), "cards": 5},
        "Smelter Demon": {"name": "Smelter Demon", "type": "boss", "level": "Main Boss", "encounters": [2, 2, 3, 3], "expansions": set(["Iron Keep"]), "cards": 5},
        "The Pursuer": {"name": "The Pursuer", "type": "boss", "level": "Main Boss", "encounters": [2, 3, 3, 3], "expansions": set(["Explorers"]), "cards": 8},
        "Black Dragon Kalameet": {"name": "Black Dragon Kalameet", "type": "boss", "level": "Mega Boss", "encounters": [4], "expansions": set(["Black Dragon Kalameet"]), "cards": 6},
        "Executioner Chariot": {"name": "Executioner Chariot", "type": "boss", "level": "Mega Boss", "encounters": [4], "expansions": set(["Executioner Chariot"]), "cards": 5},
        "Gaping Dragon": {"name": "Gaping Dragon", "type": "boss", "level": "Mega Boss", "encounters": [4], "expansions": set(["Gaping Dragon"]), "cards": 6},
        "Guardian Dragon": {"name": "Guardian Dragon", "type": "boss", "level": "Mega Boss", "encounters": [4], "expansions": set(["Guardian Dragon"]), "cards": 5},
        "Manus, Father of the Abyss": {"name": "Manus, Father of the Abyss", "type": "boss", "level": "Mega Boss", "encounters": [4], "expansions": set(["Manus, Father of the Abyss"]), "cards": 5},
        "Old Iron King": {"name": "Old Iron King", "type": "boss", "level": "Mega Boss", "encounters": [4], "expansions": set(["Old Iron King"]), "cards": 6},
        "Stray Demon": {"name": "Stray Demon", "type": "boss", "level": "Mega Boss", "encounters": [4], "expansions": set(["Asylum Demon"]), "cards": 6},
        "The Four Kings": {"name": "The Four Kings", "type": "boss", "level": "Mega Boss", "encounters": [4], "expansions": set(["The Four Kings"]), "cards": 4},
        "The Last Giant": {"name": "The Last Giant", "type": "boss", "level": "Mega Boss", "encounters": [4], "expansions": set(["The Last Giant"]), "cards": 6},
        "Vordt of the Boreal Valley": {"name": "Vordt of the Boreal Valley", "type": "boss", "level": "Mega Boss", "encounters": [4], "expansions": set(["Vordt of the Boreal Valley"]), "cards": 0}
    }

    enemyNames = sorted([e.name for e in enemies], key=lambda x: (1 if enemiesDict[x].cards == 1 else 2, enemiesDict[x].expansions if enemiesDict[x].cards > 1 else {"a",}, enemiesDict[x].name))

except Exception as e:
    log(e, exception=True)
    raise