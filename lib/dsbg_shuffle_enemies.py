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


    Enemy(id=1, name="Alonne Bow Knight", expansions=set(["Iron Keep"]), health=1, difficultyTiers={1: {"toughness": 15490, "difficulty": {1: 183.96, 2: 183.96, 3: 183.96, 4: 183.96}}, 2: {"toughness": 17507, "difficulty": {1: 34.46, 2: 34.46, 3: 34.46, 4: 34.46}}, 3: {"toughness": 110587, "difficulty": {1: 32.63, 2: 32.63, 3: 32.63, 4: 32.63}}})
    Enemy(id=2, name="Alonne Knight Captain", expansions=set(["Iron Keep"]), difficultyTiers={1: {"toughness": 1619, "difficulty": {1: 1644.92, 2: 1644.92, 3: 1644.92, 4: 1644.92}}, 2: {"toughness": 1546, "difficulty": {1: 568.26, 2: 568.26, 3: 568.26, 4: 568.26}}, 3: {"toughness": 19912, "difficulty": {1: 179.05, 2: 179.05, 3: 179.05, 4: 179.05}}})
    Enemy(id=3, name="Alonne Sword Knight", expansions=set(["Iron Keep"]), health=1, difficultyTiers={1: {"toughness": 7310, "difficulty": {1: 358.16, 2: 358.16, 3: 358.16, 4: 358.16}}, 2: {"toughness": 6191, "difficulty": {1: 102.9, 2: 102.9, 3: 102.9, 4: 102.9}}, 3: {"toughness": 71161, "difficulty": {1: 44.62, 2: 44.62, 3: 44.62, 4: 44.62}}})
    Enemy(id=4, name="Black Hollow Mage", expansions=set(["Executioner Chariot"]), difficultyTiers={1: {"toughness": 1018, "difficulty": {1: 2923.69, 2: 2923.69, 3: 2923.69, 4: 2923.69}}, 2: {"toughness": 1290, "difficulty": {1: 690.78, 2: 690.78, 3: 690.78, 4: 690.78}}, 3: {"toughness": 17423, "difficulty": {1: 225.79, 2: 225.79, 3: 225.79, 4: 225.79}}})
    Enemy(id=5, name="Bonewheel Skeleton", expansions=set(["Painted World of Ariamis"]), health=1, difficultyTiers={1: {"toughness": 15490, "difficulty": {1: 512.71, 2: 552.14, 3: 591.58, 4: 640.12}}, 2: {"toughness": 17507, "difficulty": {1: 96.04, 2: 103.43, 3: 110.82, 4: 119.91}}, 3: {"toughness": 110587, "difficulty": {1: 90.94, 2: 97.94, 3: 104.93, 4: 113.54}}})
    Enemy(id=6, name="Crossbow Hollow", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health=1, difficultyTiers={1: {"toughness": 16816, "difficulty": {1: 57.22, 2: 57.22, 3: 57.22, 4: 57.22}}, 2: {"toughness": 22377, "difficulty": {1: 12.48, 2: 12.48, 3: 12.48, 4: 12.48}}, 3: {"toughness": 112566, "difficulty": {1: 6.86, 2: 6.86, 3: 6.86, 4: 6.86}}})
    Enemy(id=7, name="Crow Demon", expansions=set(["Painted World of Ariamis"]), difficultyTiers={1: {"toughness": 2462, "difficulty": {1: 3849.92, 2: 4146.07, 3: 4442.21, 4: 4806.7}}, 2: {"toughness": 3440, "difficulty": {1: 753.09, 2: 811.02, 3: 868.95, 4: 940.25}}, 3: {"toughness": 35402, "difficulty": {1: 479.34, 2: 516.21, 3: 553.08, 4: 598.46}}})
    Enemy(id=8, name="Demonic Foliage", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 13640, "difficulty": {1: 191.95, 2: 191.95, 3: 191.95, 4: 191.95}}, 2: {"toughness": 12274, "difficulty": {1: 51.9, 2: 51.9, 3: 51.9, 4: 51.9}}, 3: {"toughness": 80188, "difficulty": {1: 39.6, 2: 39.6, 3: 39.6, 4: 39.6}}})
    Enemy(id=9, name="Engorged Zombie", expansions=set(["Painted World of Ariamis"]), difficultyTiers={1: {"toughness": 7310, "difficulty": {1: 163.78, 2: 163.78, 3: 163.78, 4: 163.78}}, 2: {"toughness": 6191, "difficulty": {1: 60.5, 2: 60.5, 3: 60.5, 4: 60.5}}, 3: {"toughness": 71161, "difficulty": {1: 17.81, 2: 17.81, 3: 17.81, 4: 17.81}}})
    Enemy(id=10, name="Falchion Skeleton", expansions=set(["Executioner Chariot"]), health=1, difficultyTiers={1: {"toughness": 15490, "difficulty": {1: 188.95, 2: 188.95, 3: 188.95, 4: 188.95}}, 2: {"toughness": 17507, "difficulty": {1: 48.82, 2: 48.82, 3: 48.82, 4: 48.82}}, 3: {"toughness": 110587, "difficulty": {1: 37.26, 2: 37.26, 3: 37.26, 4: 37.26}}})
    Enemy(id=11, name="Firebomb Hollow", expansions=set(["Explorers"]), health=1, difficultyTiers={1: {"toughness": 15490, "difficulty": {1: 61.38, 2: 66.1, 3: 70.83, 4: 76.64}}, 2: {"toughness": 17507, "difficulty": {1: 15.77, 2: 16.98, 3: 18.19, 4: 19.69}}, 3: {"toughness": 110587, "difficulty": {1: 6.9, 2: 7.43, 3: 7.96, 4: 8.61}}})
    Enemy(id=12, name="Giant Skeleton Archer", expansions=set(["Tomb of Giants"]), difficultyTiers={1: {"toughness": 4224, "difficulty": {1: 1159.97, 2: 1167.56, 3: 1175.15, 4: 1184.5}}, 2: {"toughness": 5288, "difficulty": {1: 222.64, 2: 223.82, 3: 225, 4: 226.46}}, 3: {"toughness": 39379, "difficulty": {1: 186.63, 2: 187.59, 3: 188.55, 4: 189.73}}})
    Enemy(id=13, name="Giant Skeleton Soldier", expansions=set(["Tomb of Giants"]), difficultyTiers={1: {"toughness": 4224, "difficulty": {1: 736.9, 2: 741.88, 3: 746.86, 4: 752.98}}, 2: {"toughness": 5288, "difficulty": {1: 137.67, 2: 138.21, 3: 138.75, 4: 139.41}}, 3: {"toughness": 39379, "difficulty": {1: 92.45, 2: 92.84, 3: 93.22, 4: 93.7}}})
    Enemy(id=14, name="Hollow Soldier", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health=1, difficultyTiers={1: {"toughness": 15490, "difficulty": {1: 74.36, 2: 74.36, 3: 74.36, 4: 74.36}}, 2: {"toughness": 17507, "difficulty": {1: 13.16, 2: 13.16, 3: 13.16, 4: 13.16}}, 3: {"toughness": 110587, "difficulty": {1: 9.74, 2: 9.74, 3: 9.74, 4: 9.74}}})
    Enemy(id=15, name="Ironclad Soldier", expansions=set(["Iron Keep"]), difficultyTiers={1: {"toughness": 388, "difficulty": {1: 10391.21, 2: 11190.53, 3: 11989.86, 4: 12973.64}}, 2: {"toughness": 513, "difficulty": {1: 1921.69, 2: 2069.52, 3: 2217.34, 4: 2399.27}}, 3: {"toughness": 7710, "difficulty": {1: 800.17, 2: 861.72, 3: 923.27, 4: 999.02}}})
    Enemy(id=16, name="Large Hollow Soldier", expansions=set(["Dark Souls The Board Game"]), difficultyTiers={1: {"toughness": 5306, "difficulty": {1: 487.03, 2: 524.49, 3: 561.96, 4: 608.07}}, 2: {"toughness": 7316, "difficulty": {1: 85.95, 2: 92.56, 3: 99.17, 4: 107.31}}, 3: {"toughness": 43681, "difficulty": {1: 71.75, 2: 77.27, 3: 82.79, 4: 89.58}}})
    Enemy(id=17, name="Mushroom Child", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 2462, "difficulty": {1: 742.33, 2: 742.33, 3: 742.33, 4: 742.33}}, 2: {"toughness": 3440, "difficulty": {1: 129.27, 2: 129.27, 3: 129.27, 4: 129.27}}, 3: {"toughness": 35402, "difficulty": {1: 62.61, 2: 62.61, 3: 62.61, 4: 62.61}}})
    Enemy(id=18, name="Mushroom Parent", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 717, "difficulty": {1: 4973.74, 2: 5356.34, 3: 5738.94, 4: 6209.82}}, 2: {"toughness": 1185, "difficulty": {1: 842.74, 2: 907.57, 3: 972.39, 4: 1052.18}}, 3: {"toughness": 12166, "difficulty": {1: 435.52, 2: 469.02, 3: 502.52, 4: 543.75}}})
    Enemy(id=19, name="Necromancer", expansions=set(["Tomb of Giants"]), difficultyTiers={1: {"toughness": 2462, "difficulty": {1: 899.74, 2: 968.96, 3: 1038.17, 4: 1123.35}}, 2: {"toughness": 3440, "difficulty": {1: 263.87, 2: 284.16, 3: 304.48, 4: 329.44}}, 3: {"toughness": 35402, "difficulty": {1: 159.32, 2: 171.58, 3: 183.85, 4: 198.94}}})
    Enemy(id=20, name="Phalanx", expansions=set(["Painted World of Ariamis"]), difficultyTiers={1: {"toughness": 4224, "difficulty": {1: 735.05, 2: 772.36, 3: 809.67, 4: 855.58}}, 2: {"toughness": 5288, "difficulty": {1: 138.52, 2: 145.77, 3: 153.02, 4: 161.94}}, 3: {"toughness": 39379, "difficulty": {1: 95.85, 2: 100.71, 3: 105.56, 4: 111.53}}})
    Enemy(id=21, name="Phalanx Hollow", expansions=set(["Painted World of Ariamis"]), health=1, difficultyTiers={1: {"toughness": 15490, "difficulty": {1: 83.35, 2: 83.35, 3: 83.35, 4: 83.35}}, 2: {"toughness": 17507, "difficulty": {1: 14.75, 2: 14.75, 3: 14.75, 4: 14.75}}, 3: {"toughness": 110587, "difficulty": {1: 10.92, 2: 10.92, 3: 10.92, 4: 10.92}}})
    Enemy(id=22, name="Plow Scarecrow", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 15490, "difficulty": {1: 181.79, 2: 181.79, 3: 181.79, 4: 181.79}}, 2: {"toughness": 17507, "difficulty": {1: 34.05, 2: 34.05, 3: 34.05, 4: 34.05}}, 3: {"toughness": 110587, "difficulty": {1: 32.25, 2: 32.25, 3: 32.25, 4: 32.25}}})
    Enemy(id=23, name="Sentinel", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), difficultyTiers={1: {"toughness": 1701, "difficulty": {1: 2124.1, 2: 2287.49, 3: 2450.89, 4: 2651.99}}, 2: {"toughness": 1769, "difficulty": {1: 571.95, 2: 615.95, 3: 659.95, 4: 714.1}}, 3: {"toughness": 13061, "difficulty": {1: 411.01, 2: 442.63, 3: 474.24, 4: 513.16}}})
    Enemy(id=24, name="Shears Scarecrow", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 15490, "difficulty": {1: 144.33, 2: 155.43, 3: 166.53, 4: 180.19}}, 2: {"toughness": 17507, "difficulty": {1: 23.88, 2: 25.72, 3: 27.55, 4: 29.81}}, 3: {"toughness": 110587, "difficulty": {1: 21.27, 2: 22.9, 3: 24.54, 4: 26.55}}})
    Enemy(id=25, name="Silver Knight Greatbowman", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health=1, difficultyTiers={1: {"toughness": 14966, "difficulty": {1: 121, 2: 130.3, 3: 139.61, 4: 151.06}}, 2: {"toughness": 17144, "difficulty": {1: 21.13, 2: 22.76, 3: 24.38, 4: 26.38}}, 3: {"toughness": 82167, "difficulty": {1: 20.61, 2: 22.2, 3: 23.78, 4: 25.74}}})
    Enemy(id=26, name="Silver Knight Spearman", expansions=set(["Explorers"]), health=1, difficultyTiers={1: {"toughness": 13640, "difficulty": {1: 322.06, 2: 322.06, 3: 322.06, 4: 322.06}}, 2: {"toughness": 12274, "difficulty": {1: 97.82, 2: 97.82, 3: 97.82, 4: 97.82}}, 3: {"toughness": 80188, "difficulty": {1: 98.08, 2: 98.08, 3: 98.08, 4: 98.08}}})
    Enemy(id=27, name="Silver Knight Swordsman", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health=1, difficultyTiers={1: {"toughness": 13640, "difficulty": {1: 299.47, 2: 322.51, 3: 345.55, 4: 373.9}}, 2: {"toughness": 12274, "difficulty": {1: 81.38, 2: 87.63, 3: 93.89, 4: 101.6}}, 3: {"toughness": 80188, "difficulty": {1: 77.95, 2: 83.94, 3: 89.94, 4: 97.32}}})
    Enemy(id=28, name="Skeleton Archer", expansions=set(["Tomb of Giants"]), health=1, difficultyTiers={1: {"toughness": 15490, "difficulty": {1: 116.9, 2: 116.9, 3: 116.9, 4: 116.9}}, 2: {"toughness": 17507, "difficulty": {1: 20.69, 2: 20.69, 3: 20.69, 4: 20.69}}, 3: {"toughness": 110587, "difficulty": {1: 15.32, 2: 15.32, 3: 15.32, 4: 15.32}}})
    Enemy(id=29, name="Skeleton Beast", expansions=set(["Tomb of Giants"]), difficultyTiers={1: {"toughness": 1619, "difficulty": {1: 4905.38, 2: 5282.72, 3: 5660.05, 4: 6124.47}}, 2: {"toughness": 1546, "difficulty": {1: 1087.6, 2: 1171.26, 3: 1254.92, 4: 1357.89}}, 3: {"toughness": 19912, "difficulty": {1: 505.08, 2: 543.93, 3: 582.78, 4: 630.6}}})
    Enemy(id=30, name="Skeleton Soldier", expansions=set(["Tomb of Giants"]), health=1, difficultyTiers={1: {"toughness": 13640, "difficulty": {1: 169.64, 2: 182.69, 3: 195.74, 4: 211.8}}, 2: {"toughness": 12274, "difficulty": {1: 60.89, 2: 65.57, 3: 70.26, 4: 76.02}}, 3: {"toughness": 80188, "difficulty": {1: 45.84, 2: 49.37, 3: 52.9, 4: 57.24}}})
    Enemy(id=31, name="Snow Rat", expansions=set(["Painted World of Ariamis"]), difficultyTiers={1: {"toughness": 16036, "difficulty": {1: 190.03, 2: 190.03, 3: 190.03, 4: 190.03}}, 2: {"toughness": 18843, "difficulty": {1: 55.96, 2: 55.96, 3: 55.96, 4: 55.96}}, 3: {"toughness": 114936, "difficulty": {1: 58.96, 2: 58.96, 3: 58.96, 4: 58.96}}})
    Enemy(id=32, name="Stone Guardian", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 1004, "difficulty": {1: 4704.84, 2: 5066.75, 3: 5428.66, 4: 5874.09}}, 2: {"toughness": 1290, "difficulty": {1: 820.36, 2: 883.47, 3: 946.57, 4: 1024.24}}, 3: {"toughness": 17423, "difficulty": {1: 295.28, 2: 317.99, 3: 340.71, 4: 368.66}}})
    Enemy(id=33, name="Stone Knight", expansions=set(["Darkroot"]), difficultyTiers={1: {"toughness": 1268, "difficulty": {1: 1466.09, 2: 1466.09, 3: 1466.09, 4: 1466.09}}, 2: {"toughness": 728, "difficulty": {1: 842.39, 2: 842.39, 3: 842.39, 4: 842.39}}, 3: {"toughness": 10873, "difficulty": {1: 228.89, 2: 228.89, 3: 228.89, 4: 228.89}}})
    Enemy(id=34, name="Mimic", expansions=set(["The Sunless City"]), difficultyTiers={1: {"toughness": 4224, "difficulty": {1: 1441.31, 2: 1441.31, 3: 1441.31, 4: 1441.31}}, 2: {"toughness": 5288, "difficulty": {1: 314.67, 2: 314.67, 3: 314.67, 4: 314.67}}, 3: {"toughness": 39379, "difficulty": {1: 276.79, 2: 276.79, 3: 276.79, 4: 276.79}}})
    Enemy(id=35, name="Armorer Dennis", expansions=set(["Phantoms"]), cards=4, difficultyTiers={1: {"toughness": 679.2, "difficulty": {1: 1411.68, 2: 1460.45, 3: 1509.22, 4: 1569.26}}, 2: {"toughness": 991.4, "difficulty": {1: 299.06, 2: 309.72, 3: 320.39, 4: 333.52}}, 3: {"toughness": 10553.4, "difficulty": {1: 120.17, 2: 124.14, 3: 128.1, 4: 132.98}}})
    Enemy(id=36, name="Fencer Sharron", expansions=set(["Phantoms"]), cards=5, difficultyTiers={1: {"toughness": 1030.14, "difficulty": {1: 3617.78, 2: 3710.87, 3: 3803.96, 4: 3918.54}}, 2: {"toughness": 1325, "difficulty": {1: 706.6, 2: 721.8, 3: 737, 4: 755.71}}, 3: {"toughness": 10568.14, "difficulty": {1: 489.24, 2: 499.25, 3: 509.27, 4: 521.59}}})
    Enemy(id=37, name="Invader Brylex", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 548, "difficulty": {1: 8485.75, 2: 8848.51, 3: 9211.26, 4: 9657.72}}, 2: {"toughness": 541, "difficulty": {1: 2317.25, 2: 2414.91, 3: 2512.57, 4: 2632.77}}, 3: {"toughness": 7366, "difficulty": {1: 879.77, 2: 917.64, 3: 955.5, 4: 1002.1}}})
    Enemy(id=38, name="Kirk, Knight of Thorns", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 1877, "difficulty": {1: 1006.46, 2: 1040.4, 3: 1074.33, 4: 1116.1}}, 2: {"toughness": 2368, "difficulty": {1: 209.37, 2: 216.48, 3: 223.6, 4: 232.35}}, 3: {"toughness": 18452, "difficulty": {1: 136.42, 2: 140.8, 3: 145.18, 4: 150.58}}})
    Enemy(id=39, name="Longfinger Kirk", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 584, "difficulty": {1: 8642.13, 2: 8844.27, 3: 9046.42, 4: 9295.21}}, 2: {"toughness": 574, "difficulty": {1: 2392.82, 2: 2448.26, 3: 2503.71, 4: 2571.95}}, 3: {"toughness": 7925, "difficulty": {1: 1066.76, 2: 1089.18, 3: 1111.6, 4: 1139.2}}})
    Enemy(id=40, name="Maldron the Assassin", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 1714, "difficulty": {1: 2254.85, 2: 2312.08, 3: 2369.32, 4: 2439.76}}, 2: {"toughness": 2200, "difficulty": {1: 446.55, 2: 457.33, 3: 468.11, 4: 481.37}}, 3: {"toughness": 16827, "difficulty": {1: 371.25, 2: 380.17, 3: 389.08, 4: 400.05}}})
    Enemy(id=41, name="Maneater Mildred", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 950.6, "difficulty": {1: 3242.97, 2: 3492.43, 3: 3741.89, 4: 4048.92}}, 2: {"toughness": 1370.2, "difficulty": {1: 431.71, 2: 464.91, 3: 498.12, 4: 538.99}}, 3: {"toughness": 11086.6, "difficulty": {1: 275.34, 2: 296.51, 3: 317.69, 4: 343.76}}})
    Enemy(id=42, name="Marvelous Chester", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 755, "difficulty": {1: 7115.38, 2: 7157.84, 3: 7200.29, 4: 7252.55}}, 2: {"toughness": 1072, "difficulty": {1: 1287.02, 2: 1294.87, 3: 1302.72, 4: 1312.38}}, 3: {"toughness": 11461, "difficulty": {1: 688.88, 2: 693.89, 3: 698.91, 4: 705.08}}})
    Enemy(id=43, name="Melinda the Butcher", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 1695.6, "difficulty": {1: 1300.68, 2: 1365.4, 3: 1430.11, 4: 1509.76}}, 2: {"toughness": 2285.4, "difficulty": {1: 190.55, 2: 200.45, 3: 210.35, 4: 222.53}}, 3: {"toughness": 15295.2, "difficulty": {1: 139.21, 2: 146.28, 3: 153.36, 4: 162.07}}})
    Enemy(id=44, name="Oliver the Collector", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 1673.14, "difficulty": {1: 2300.43, 2: 2393.11, 3: 2485.79, 4: 2599.86}}, 2: {"toughness": 2152.71, "difficulty": {1: 361.78, 2: 376.06, 3: 390.34, 4: 407.91}}, 3: {"toughness": 14312.43, "difficulty": {1: 237.04, 2: 245.2, 3: 253.37, 4: 263.42}}})
    Enemy(id=45, name="Paladin Leeroy", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 789, "difficulty": {1: 4973.25, 2: 5327.09, 3: 5680.92, 4: 6116.41}}, 2: {"toughness": 869.6, "difficulty": {1: 974.45, 2: 1042, 3: 1109.55, 4: 1192.68}}, 3: {"toughness": 7418.6, "difficulty": {1: 545.41, 2: 580.63, 3: 615.85, 4: 659.19}}})
    Enemy(id=46, name="Xanthous King Jeremiah", expansions=set(["Phantoms"]), cards=3, difficultyTiers={1: {"toughness": 4584, "difficulty": {1: 917.1, 2: 975.25, 3: 1033.4, 4: 1104.97}}, 2: {"toughness": 9069, "difficulty": {1: 173.4, 2: 184.35, 3: 195.3, 4: 208.77}}, 3: {"toughness": 21573.5, "difficulty": {1: 92.92, 2: 98.74, 3: 104.56, 4: 111.73}}})
    Enemy(id=47, name="Hungry Mimic", expansions=set(["Explorers"]), cards=4, difficultyTiers={1: {"toughness": 1234, "difficulty": {1: 2060.71, 2: 2135.56, 3: 2210.41, 4: 2302.53}}, 2: {"toughness": 1604, "difficulty": {1: 386.34, 2: 400.47, 3: 414.61, 4: 432}}, 3: {"toughness": 12513, "difficulty": {1: 292.5, 2: 302.94, 3: 313.37, 4: 326.22}}})
    Enemy(id=48, name="Voracious Mimic", expansions=set(["Explorers"]), cards=4, difficultyTiers={1: {"toughness": 462, "difficulty": {1: 7620.35, 2: 7886.49, 3: 8152.62, 4: 8480.17}}, 2: {"toughness": 446, "difficulty": {1: 2160.05, 2: 2235.93, 3: 2311.81, 4: 2405.21}}, 3: {"toughness": 6277, "difficulty": {1: 949.09, 2: 981.42, 3: 1013.74, 4: 1053.53}}})

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

except Exception as e:
    log(e, exception=True)
    raise