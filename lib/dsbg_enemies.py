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

    modIdLookup = {
    1: "dodge1",
    2: "dodge2",
    3: "damage1",
    4: "damage2",
    5: "damage3",
    6: "damage4",
    7: "armor1",
    8: "armor2",
    9: "resist1",
    10: "resist2",
    11: "health1",
    12: "health2",
    13: "health3",
    14: "health4",
    15: "repeat",
    16: "magic",
    17: "bleed",
    18: "frostbite",
    19: "poison",
    20: "stagger",
    21: "physical"
}


    class Enemy:
        def __init__(self, id, name, expansions, difficulty, health=None, toughness=0) -> None:
            enemiesDict[name] = self
            enemies.append(self)
            enemyIds[id] = self
            self.id = id
            self.name = name
            self.expansions = expansions
            self.difficulty = difficulty
            # Lower is better
            self.toughness = toughness
            
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


    Enemy(id=1, name="Alonne Bow Knight", expansions=set(["Iron Keep"]), health=1, toughness=243160, difficulty={1: 4.59, 2: 4.59, 3: 4.59, 4: 4.59})
    Enemy(id=2, name="Alonne Knight Captain", expansions=set(["Iron Keep"]), toughness=57099, difficulty={1: 17.92, 2: 17.92, 3: 17.92, 4: 17.92})
    Enemy(id=3, name="Alonne Sword Knight", expansions=set(["Iron Keep"]), health=1, toughness=183940, difficulty={1: 4.98, 2: 4.98, 3: 4.98, 4: 4.98})
    Enemy(id=4, name="Black Hollow Mage", expansions=set(["Executioner Chariot"]), toughness=51913, difficulty={1: 24.09, 2: 24.09, 3: 24.09, 4: 24.09})
    Enemy(id=5, name="Bonewheel Skeleton", expansions=set(["Painted World of Ariamis"]), health=1, toughness=243160, difficulty={1: 5.84, 2: 6.29, 3: 6.73, 4: 7.29})
    Enemy(id=6, name="Crossbow Hollow", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health=1, toughness=251760, difficulty={1: 1.38, 2: 1.38, 3: 1.38, 4: 1.38})
    Enemy(id=7, name="Crow Demon", expansions=set(["Painted World of Ariamis"]), toughness=90742, difficulty={1: 30.44, 2: 32.78, 3: 35.12, 4: 38})
    Enemy(id=8, name="Demonic Foliage", expansions=set(["Darkroot"]), toughness=203535, difficulty={1: 4.5, 2: 4.5, 3: 4.5, 4: 4.5})
    Enemy(id=9, name="Engorged Zombie", expansions=set(["Painted World of Ariamis"]), toughness=183940, difficulty={1: 1.82, 2: 1.82, 3: 1.82, 4: 1.82})
    Enemy(id=10, name="Falchion Skeleton", expansions=set(["Executioner Chariot"]), health=1, toughness=243160, difficulty={1: 4.76, 2: 4.76, 3: 4.76, 4: 4.76})
    Enemy(id=11, name="Firebomb Hollow", expansions=set(["Explorers"]), health=1, toughness=243160, difficulty={1: 1.39, 2: 1.5, 3: 1.6, 4: 1.74})
    Enemy(id=12, name="Giant Skeleton Archer", expansions=set(["Tomb of Giants"]), toughness=243160, difficulty={1: 18.89, 2: 18.9, 3: 18.91, 4: 18.93})
    Enemy(id=13, name="Giant Skeleton Soldier", expansions=set(["Tomb of Giants"]), toughness=100540, difficulty={1: 11.18, 2: 11.21, 3: 11.24, 4: 11.27})
    Enemy(id=14, name="Hollow Soldier", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health=1, toughness=243160, difficulty={1: 1.17, 2: 1.17, 3: 1.17, 4: 1.17})
    Enemy(id=15, name="Ironclad Soldier", expansions=set(["Iron Keep"]), toughness=24945, difficulty={1: 34.01, 2: 36.63, 3: 39.24, 4: 42.46})
    Enemy(id=16, name="Large Hollow Soldier", expansions=set(["Dark Souls The Board Game"]), toughness=110052, difficulty={1: 4.55, 2: 4.9, 3: 5.25, 4: 5.68})
    Enemy(id=17, name="Mushroom Child", expansions=set(["Darkroot"]), toughness=90742, difficulty={1: 5.52, 2: 5.52, 3: 5.52, 4: 5.52})
    Enemy(id=18, name="Mushroom Parent", expansions=set(["Darkroot"]), toughness=40011, difficulty={1: 18.73, 2: 20.17, 3: 21.61, 4: 23.39})
    Enemy(id=19, name="Necromancer", expansions=set(["Tomb of Giants"]), toughness=90742, difficulty={1: 11.86, 2: 12.78, 3: 13.7, 4: 14.81})
    Enemy(id=20, name="Phalanx", expansions=set(["Painted World of Ariamis"]), toughness=100540, difficulty={1: 8.49, 2: 8.87, 3: 9.25, 4: 9.73})
    Enemy(id=21, name="Phalanx Hollow", expansions=set(["Painted World of Ariamis"]), health=1, toughness=243160, difficulty={1: 1.17, 2: 1.17, 3: 1.17, 4: 1.17})
    Enemy(id=22, name="Plow Scarecrow", expansions=set(["Darkroot"]), toughness=243160, difficulty={1: 4.48, 2: 4.48, 3: 4.48, 4: 4.48})
    Enemy(id=23, name="Sentinel", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), toughness=36549, difficulty={1: 37.5, 2: 40.39, 3: 43.27, 4: 46.82})
    Enemy(id=24, name="Shears Scarecrow", expansions=set(["Darkroot"]), toughness=243160, difficulty={1: 2.69, 2: 2.9, 3: 3.11, 4: 3.36})
    Enemy(id=25, name="Silver Knight Greatbowman", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health=1, toughness=212135, difficulty={1: 2.99, 2: 3.22, 3: 3.46, 4: 3.74})
    Enemy(id=26, name="Silver Knight Spearman", expansions=set(["Explorers"]), health=1, toughness=203535, difficulty={1: 6.1, 2: 6.1, 3: 6.1, 4: 6.1})
    Enemy(id=27, name="Silver Knight Swordsman", expansions=set(["The Sunless City", "Dark Souls The Board Game"]), health=1, toughness=203535, difficulty={1: 7.62, 2: 8.21, 3: 8.8, 4: 9.52})
    Enemy(id=28, name="Skeleton Archer", expansions=set(["Tomb of Giants"]), health=1, toughness=243160, difficulty={1: 2.61, 2: 2.61, 3: 2.61, 4: 2.61})
    Enemy(id=29, name="Skeleton Beast", expansions=set(["Tomb of Giants"]), toughness=57099, difficulty={1: 24.86, 2: 26.77, 3: 28.68, 4: 31.03})
    Enemy(id=30, name="Skeleton Soldier", expansions=set(["Tomb of Giants"]), health=1, toughness=203535, difficulty={1: 2.68, 2: 2.89, 3: 3.1, 4: 3.35})
    Enemy(id=31, name="Snow Rat", expansions=set(["Painted World of Ariamis"]), toughness=255460, difficulty={1: 3.33, 2: 3.33, 3: 3.33, 4: 3.33})
    Enemy(id=32, name="Stone Guardian", expansions=set(["Darkroot"]), toughness=51748, difficulty={1: 23.21, 2: 25, 3: 26.78, 4: 28.98})
    Enemy(id=33, name="Stone Knight", expansions=set(["Darkroot"]), toughness=33619, difficulty={1: 16.64, 2: 16.64, 3: 16.64, 4: 16.64})
    Enemy(id=34, name="Mimic", expansions=set(["The Sunless City"]), toughness=100540, difficulty={1: 26.82, 2: 26.82, 3: 26.82, 4: 26.82})
    Enemy(id=35, name="Armorer Dennis", expansions=set(["Phantoms"]), difficulty={1: 48.3, 2: 50, 3: 51.71, 4: 53.81})
    Enemy(id=36, name="Fencer Sharron", expansions=set(["Phantoms"]), difficulty={1: 50.37, 2: 50.84, 3: 51.31, 4: 51.88})
    Enemy(id=37, name="Invader Brylex", expansions=set(["Phantoms"]), difficulty={1: 86.16, 2: 89.76, 3: 93.35, 4: 97.77})
    Enemy(id=38, name="Kirk, Knight of Thorns", expansions=set(["Phantoms"]), difficulty={1: 24.05, 2: 24.89, 3: 25.73, 4: 26.76})
    Enemy(id=39, name="Longfinger Kirk", expansions=set(["Phantoms"]), difficulty={1: 128.96, 2: 131.83, 3: 134.71, 4: 138.25})
    Enemy(id=40, name="Maldron the Assassin", expansions=set(["Phantoms"]), difficulty={1: 37.15, 2: 37.82, 3: 38.49, 4: 39.32})
    Enemy(id=41, name="Maneater Mildred", expansions=set(["Phantoms"]), difficulty={1: 17.93, 2: 19.31, 3: 20.69, 4: 22.39})
    Enemy(id=42, name="Marvelous Chester", expansions=set(["Phantoms"]), difficulty={1: 144.66, 2: 145.15, 3: 145.64, 4: 146.24})
    Enemy(id=43, name="Melinda the Butcher", expansions=set(["Phantoms"]), difficulty={1: 15.36, 2: 15.97, 3: 16.57, 4: 17.32})
    Enemy(id=44, name="Oliver the Collector", expansions=set(["Phantoms"]), difficulty={1: 23, 2: 23.74, 3: 24.49, 4: 25.41})
    Enemy(id=45, name="Paladin Leeroy", expansions=set(["Phantoms"]), difficulty={1: 45.25, 2: 47.21, 3: 49.16, 4: 51.57})
    Enemy(id=46, name="Xanthous King Jeremiah", expansions=set(["Phantoms"]), difficulty={1: 22.77, 2: 24.23, 3: 25.69, 4: 27.49})
    Enemy(id=47, name="Hungry Mimic", expansions=set(["Phantoms"]), difficulty={1: 31.35, 2: 32.43, 3: 33.51, 4: 34.84})
    Enemy(id=48, name="Voracious Mimic", expansions=set(["Phantoms"]), difficulty={1: 82.86, 2: 85.67, 3: 88.47, 4: 91.92})

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
        "Ornstein & Smough": {"name": "Ornstein & Smough", "type": "boss", "level": "Main Boss", "expansions": set(["Dark Souls The Board Game", "The Sunless City"])},
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

    behaviors = {
        "Armorer Dennis": ["Soul Flash", "Soul Greatsword", "Soul Spear Launch", "Soul Vortex", "Upward Slash"],
        "Fencer Sharron": ["Dual Sword Assault", "Dual Sword Slash", "Puzzling Stone Sword Charge", "Puzzling Stone Sword Whip", "Spider Fang Sword Charge", "Spider Fan Sword Strike", "Spider Fang Web Blast"],
        "Hungry Mimic": ["Aggressive Grab", "Charging Chomp", "Heavy Punch", "Leaping Spin Kick", "Raking Slash", "Stomping Kick", "Vicious Chomp"],
        "Invader Brylex": ["Blade Dervish", "Fire Surge", "Fire Whip", "Leaping Strike", "Trampling Charge"],
        "Kirk, Knight of Thorns": ["Barbed Sword Thrust", "Forward Roll", "Overhead Chop", "Shield Bash", "Shield Charge"],
        "Longfinger Kirk": ["Barbed Sword Strikes", "Cleave", "Crushing Blow", "Lunging Stab", "Rolling Barbs"],
        "Maldron the Assassin": ["Corrosive Urn Toss", "Double Lance Lunge", "Greatlance Lunge", "Jousting Charge", "Leaping Lance Strike"],
        "Maneater Mildred": ["Butcher Chop", "Butchery", "Death Blow", "Executioner Strike", "Guillotine"],
        "Marvelous Chester": ["Crossbow Snipe", "Crossbow Volley", "Spinning Low Kick", "Throwing Knife Flurry", "Throwing Knife Volley"],
        "Melinda the Butcher": ["Cleaving Strikes", "Double Smash", "Greataxe Sweep", "Jumping Cleave", "Sweeping Advance"],
        "Oliver the Collector": ["Bone Fish Punches", "Majestic Greatsword Slash", "Minotaur Helm Charge", "Puzzling Stone Sword Strike", "Ricard's Rapier Thrust", "Santier's Spear Lunge", "Smelter Hammer Whirlwind"],
        "Paladin Leeroy": ["Advancing Grant Slam", "Grant Slam Withdrawal", "Sanctus Shield Dash", "Sanctus Shield Slam", "Wrath of the Gods"],
        "Voracious Mimic": ["Aggressive Grab", "Charging Chomp", "Heavy Punch", "Leaping Spin Kick", "Raking Slash", "Stomping Kick", "Vicious Chomp"],
        "Xanthous King Jeremiah": ["Chaos Fire Whip", "Chaos Storm", "Fiery Retreat", "Great Chaos Fireball", "Whiplash"],
        "Asylum Demon": ["Crushing Leaps", "Delayed Hammer Drive", "Ground Pound", "Hammer Drive", "Leaping Hammer Smash", "Lumbering Swings", "Mighty Hammer Smash", "Retreating Sweep", "Sweeping Strikes"],
        "Black Knight": ["Backswing", "Charge", "Defensive Strike", "Hacking Slash", "Heavy Slash", "Massive Swing", "Overhead Swing", "Vicious Hack", "Wide Swing"],
        "Boreal Outrider Knight": ["Backhand Slashes", "Chilling Thrust", "Frost Breath", "Leaping Frost", "Lunging Triple Slash", "Overhand Slash", "Sweeping Strike", "Uppercut Slam"],
        "Gargoyle": ["Aerial Electric Breath", "Electric Breath", "Flying Tail Whip", "Halberd Thrust", "Sweeping Strike", "Swooping Cleave", "Tail Sweep", "Tail Whip"],
        "Heavy Knight": ["Charging Chop", "Defensive Chop", "Defensive Swipe", "Double Chop", "Double Slash", "Overhead Chop", "Shield Smash", "Shield Swipe", "Slashing Blade"],
        "Old Dragonslayer": ["Darkness Bolt", "Darkness Falls", "Leaping Darkness", "Lunging Combo", "Massive Sweep", "Skewering Charge", "Spear Lunge", "Spear Sweep"],
        "Titanite Demon": ["Double Pole Crush", "Double Swing", "Grab & Smash", "Lightning Bolt", "Sweeping Strike", "Tail Whip", "Vaulting Slam", "Vicious Swing"],
        "Winged Knight": ["Backhand Shaft Strike", "Charging Assault", "Diagonal Uppercut", "Double Slash", "Overhand Strike", "Pillars of Light", "Sweeping Blade Swing", "Whirlwind"],
        "Artorias": ["Abyss Assault", "Abyss Sludge", "Charging Slash", "Heavy Thrust", "Leaping Fury", "Lunging Cleave", "Overhead Cleave", "Retreating Strike", "Somersault Slam", "Somersault Strike", "Spinning Slash", "Steadfast Leap", "Wrath of the Abyss"],
        "Crossbreed Priscilla": ["Backslash", "Blizzard", "Double Lunge", "Double Slash", "Double Strike", "Flanking Slash", "Icy Blast", "Mournful Gaze", "Scythe Slash", "Scythe Strike", "Scything Lunge", "Scything Withdrawal", "Snowstorm"],
        "Dancer of the Boreal Valley": ["Ash Cloud", "Backhand Blade Swipe", "Blade Dance", "Deadly Grasp", "Double Slash", "Flashing Blade", "Lunging Thrust", "Plunging Assault", "Plunging Attack", "Sweeping Blade Swipe", "Triple Slash", "Uppercut", "Whirling Blades"],
        "Gravelord Nito": ["Creeping Death", "Death Grip", "Death Wave", "Deathly Strike", "Deathly Thrust", "Death's Embrace", "Entrophy", "Gravelord Greatsword", "Lunging Cleave", "Miasma", "Sword Slam", "Sword Sweep", "Toxicity"],
        "Great Grey Wolf Sif": ["Cyclone Strikes", "Dashing Slice", "Evasive Strike", "Feral Onslaught", "Limping Strike", "Pouncing Assault", "Saveage Retreat", "Sidestep Cleave", "Sidestep Slash", "Slashing Assault", "Slashing Retreat", "Spinning Slash", "Sword Slam", "Upward Slash"],
        "Ornstein & Smough": ["Evasive Sweep & Trampling Charge", "Gliding Stab & Hammer Smash", "Lightning Bolt & Jumping Slam", "Spear Slam & Hammer Sweep", "Swiping Combo & Bonzai Drop", "Charged Swiping Combo", "Electric Clash", "High Voltage", "Lightning Stab", "Charged Charge", "Electric Bonzai Drop", "Electric Hammer Smash", "Jumping Volt Slam", "Lightning Sweep"],
        "Sir Alonne": ["Charging Katana Lunge", "Charging Katana Slash", "Dark Wave", "Double Slash Combo", "Fast Katana Lunge", "Katana Plunge", "Left Sidestep Slash", "Life Drain", "Lunging Slash Combo", "Right Sidestep Slash", "Stab & Slash Combo", "Stabbing Slash Combo", "Triple Slash Combo"],
        "Smelter Demon": ["Double Sweep", "Fiery Blast", "Fiery Explosion", "Flame Wave", "Flaming Double Sweep", "Flaming Impalement Strike", "Flaming Overhead Chop", "Flaming Sweeping Slash", "Leaping Impalement Strike", "Lunging Strike", "Overhead Chop", "Sweeping Slash"],
        "The Pursuer": ["Cursed Impale", "Dark Magic", "Overhead Cleave", "Rising Blade Swing", "Shield Bash", "Shield Smash", "Stabbing Strike", "Wide Blade Swing"],
        "Black Dragon Kalameet": ["Conflagration", "Consuming Blaze", "Evasive Tail Whip", "Flame Feint", "Head Strike", "Hellfire Barrage", "Hellfire Blast", "Mark of Calamity", "Rising Inferno", "Rush Strike", "Sweeping Flame", "Swooping Charge", "Tail Sweep"],
        "Executioner Chariot": ["Advancing Back Kick", "Back Kick", "Charging Breath", "Charging Ram", "Deadly Breath", "Engulfing Darkness", "Headbutt", "Merciless Charge", "Rearing Charge", "Roiling Darkness", "Stomp Rush", "Trampling Charge"],
        "Gaping Dragon": ["Claw Swipe", "Corrosive Ooze (Front)", "Corrosive Ooze (Front Left)", "Corrosive Ooze (Front Right)", "Corrosive Ooze (Front Right Left)", "Crawling Charge", "Flying Smash", "Gorge", "Right Hook", "Stomach Slam", "Stomp Slam", "Tail Whip", "Triple Stomp"],
        "Guardian Dragon": ["Cage Grasp Inferno", "Charging Flame", "Fire Breath", "Fire Sweep", "Fireball", "Leaping Breath", "Left Stomp", "Right Stomp", "Tail Sweep"],
        "Manus, Father of the Abyss": ["Abyss Cage", "Abyss Rain", "Back Swipe", "Catalyst Smash", "Catalyst Strike", "Crushing Palm", "Dark Orb Barrage", "Descending Darkness", "Diving Slam", "Extended Sweep", "Frenzied Attacks", "Ground Slam", "Ring of Darkfire", "Sweeping Strike"],
        "Old Iron King": ["Bash", "Double Fist Pound", "Double Swipe", "Fire Beam (Front)", "Fire Beam (Left)", "Fire Beam (Right)", "Firestorm", "Fist Pound", "Magma Blast", "Searing Blast", "Shockwave", "Swipe"],
        "Stray Demon": ["Crushing Leaps", "Delayed Hammer Drive", "Ground Pound", "Hammer Blast", "Hammer Drive", "Leaping Hammer Smash", "Lumbering Swings", "Mighty Hammer Smash", "Retreating Sweep", "Shockwave", "Sidestep Left Sweep", "Sidestep Right Sweep", "Sweeping Strikes"],
        "The Four Kings": ["Blazing Wrath", "Cautious Arrow Mass", "Downward Slash", "Evasive Abyss Arrow", "Evasive Slash", "Executioner's Slash", "Forward Thrust", "Homing Arrow Mass", "Horizontal Slash", "Into the Abyss", "Lifedrain Death Grasp", "Lifedrain Grab", "Pinpoint Homing Arrows", "Precision Slash", "Shockwave", "Thrust & Retreat", "Unerring Thrust", "Upward Slash", "Wrath of the Kings"],
        "The Last Giant": ["Arm Club Backhand", "Arm Club Sweep", "Arm Smash", "Armed Swings", "Backhand Strike", "Backstep Stomp", "Beat You With It", "Clubbing Blow", "Falling Slam", "Heavy Swings", "Left Foot Stomp", "Overhead Smash", "Right Foot Stomp", "Stomp Rush", "Sweeping Strike", "Triple Stomp"],
        "Vordt of the Boreal Valley": ["Backhand Swipe", "Berserk Rush", "Berserk Trample", "Crushing Charge", "Double Swipe", "Frostbreath", "Hammerfist Combo", "Hammerfist", "Handle Slam", "Jump Rush", "Mace Thrust", "Retreating Sweep", "Shove Left", "Shove Right", "Tracking Charge", "Trampling Charge", "Wild Swings"]
    }
except Exception as e:
    log(e, exception=True)
    raise