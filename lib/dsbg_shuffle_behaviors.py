try:
    from dsbg_shuffle_utility import log
    
    behaviors = {
        "Armorer Dennis": ["Soul Flash", "Soul Greatsword", "Soul Spear Launch", "Soul Vortex", "Upward Slash"],
        "Fencer Sharron": ["Dual Sword Assault", "Dual Sword Slash", "Puzzling Stone Sword Charge", "Puzzling Stone Sword Whip", "Spider Fang Sword Charge", "Spider Fang Sword Strike", "Spider Fang Web Blast"],
        "Hungry Mimic": ["Aggressive Grab", "Charging Chomp", "Heavy Punch", "Leaping Spin Kick", "Raking Slash", "Stomping Kick", "Vicious Chomp"],
        "Invader Brylex": ["Blade Dervish", "Fire Surge", "Fire Whip", "Leaping Strike", "Trampling Charge"],
        "Kirk, Knight of Thorns": ["Barbed Sword Thrust", "Forward Roll", "Overhead Chop", "Shield Bash", "Shield Charge"],
        "Longfinger Kirk": ["Barbed Sword Strikes", "Cleave", "Crushing Blow", "Lunging Stab", "Rolling Barbs"],
        "Maldron the Assassin": ["Corrosive Urn Toss", "Double Lance Lunge", "Greatlance Lunge", "Jousting Charge", "Leaping Lance Strike"],
        "Maneater Mildred": ["Butcher Chop", "Butchery", "Death Blow", "Executioner Strike", "Guillotine"],
        "Marvelous Chester": ["Crossbow Snipe", "Crossbow Volley", "Spinning Low Kick", "Throwing Knife Flurry", "Throwing Knife Volley"],
        "Melinda the Butcher": ["Cleaving Strikes", "Double Smash", "Greataxe Sweep", "Jumping Cleave", "Sweeping Advance"],
        "Oliver the Collector": ["Bone Fist Punches", "Majestic Greatsword Slash", "Minotaur Helm Charge", "Puzzling Stone Sword Strike", "Ricard's Rapier Thrust", "Santier's Spear Lunge", "Smelter Hammer Whirlwind"],
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
        "Winged Knight": ["Backhand Shaft Strike", "Charging Assault", "Diagonal Uppercut", "Double Slash", "Overhand Smash", "Pillars of Light", "Sweeping Blade Swing", "Whirlwind"],
        "Artorias": ["Abyss Assault", "Abyss Sludge", "Charging Slash", "Heavy Thrust", "Leaping Fury", "Lunging Cleave", "Overhead Cleave", "Retreating Strike", "Somersault Slam", "Somersault Strike", "Spinning Slash", "Steadfast Leap", "Wrath of the Abyss"],
        "Crossbreed Priscilla": ["Backslash", "Blizzard", "Double Lunge", "Double Slash", "Double Strike", "Flanking Slash", "Icy Blast", "Mournful Gaze", "Scythe Slash", "Scythe Strike", "Scything Lunge", "Scything Withdrawal", "Snowstorm"],
        "Dancer of the Boreal Valley": ["Ash Cloud", "Backhand Blade Swipe", "Blade Dance", "Deadly Grasp", "Double Slash", "Flashing Blade", "Lunging Thrust", "Plunging Assault", "Plunging Attack", "Sweeping Blade Swipe", "Triple Slash", "Uppercut", "Whirling Blades"],
        "Gravelord Nito": ["Creeping Death", "Death Grip", "Death Wave", "Deathly Strike", "Deathly Thrust", "Death's Embrace", "Entropy", "Gravelord Greatsword", "Lunging Cleave", "Miasma", "Sword Slam", "Sword Sweep", "Toxicity"],
        "Great Grey Wolf Sif": ["Cyclone Strikes", "Dashing Slice", "Evasive Strike", "Feral Onslaught", "Limping Strike", "Pouncing Assault", "Savage Retreat", "Sidestep Cleave", "Sidestep Slash", "Slashing Assault", "Slashing Retreat", "Spinning Slash", "Sword Slam", "Upward Slash"],
        "Ornstein & Smough": ["Evasive Sweep & Trampling Charge", "Gliding Stab & Hammer Smash", "Lightning Bolt & Jumping Slam", "Spear Slam & Hammer Sweep", "Swiping Combo & Bonzai Drop", "Charged Bolt", "Charged Swiping Combo", "Electric Clash", "High Voltage", "Lightning Stab", "Charged Charge", "Electric Bonzai Drop", "Electric Hammer Smash", "Jumping Volt Slam", "Lightning Sweep"],
        "Sir Alonne": ["Charging Katana Lunge", "Charging Katana Slash", "Dark Wave", "Double Slash Combo", "Fast Katana Lunge", "Katana Plunge", "Left Sidestep Slash", "Life Drain", "Lunging Slash Combo", "Right Sidestep Slash", "Stab & Slash Combo", "Stabbing Slash Combo", "Triple Slash Combo"],
        "Smelter Demon": ["Double Sweep", "Fiery Blast", "Fiery Explosion", "Flame Wave", "Flaming Double Sweep", "Flaming Impalement Strike", "Flaming Lunging Strike", "Flaming Overhead Chop", "Flaming Sweeping Slash", "Leaping Impalement Strike", "Lunging Strike", "Overhead Chop", "Sweeping Slash"],
        "The Pursuer": ["Back Dash", "Cursed Impale", "Dark Magic", "Forward Dash", "Overhead Cleave", "Rising Blade Swing", "Shield Bash", "Shield Smash", "Stabbing Strike", "Wide Blade Swing"],
        "Black Dragon Kalameet": ["Conflagration", "Consuming Blaze", "Evasive Tail Whip", "Flame Feint", "Head Strike", "Hellfire Barrage", "Hellfire Blast", "Mark of Calamity", "Rising Inferno", "Rush Strike", "Sweeping Flame", "Swooping Charge", "Tail Sweep"],
        "Executioner Chariot": ["Advancing Back Kick", "Back Kick", "Charging Breath", "Charging Ram", "Deadly Breath", "Death Race", "Engulfing Darkness", "Headbutt", "Merciless Charge", "Rearing Charge", "Roiling Darkness", "Stomp Rush", "Trampling Charge"],
        "Gaping Dragon": ["Claw Swipe", "Corrosive Ooze (Front)", "Corrosive Ooze (Front Left)", "Corrosive Ooze (Front Right)", "Corrosive Ooze (Front Right Left)", "Crawling Charge", "Flying Smash", "Gorge", "Right Hook", "Stomach Slam", "Stomp Slam", "Tail Whip", "Triple Stomp"],
        "Guardian Dragon": ["Bite", "Cage Grasp Inferno", "Charging Flame", "Fire Breath", "Fire Sweep", "Fireball", "Leaping Breath", "Left Stomp", "Right Stomp", "Tail Sweep"],
        "Manus, Father of the Abyss": ["Abyss Cage", "Abyss Rain", "Back Swipe", "Catalyst Smash", "Catalyst Strike", "Crushing Palm", "Dark Orb Barrage", "Descending Darkness", "Diving Slam", "Extended Sweep", "Frenzied Attacks", "Ground Slam", "Ring of Darkfire", "Sweeping Strike"],
        "Old Iron King": ["Bash", "Double Fist Pound", "Double Swipe", "Fire Beam (Front)", "Fire Beam (Left)", "Fire Beam (Right)", "Firestorm", "Fist Pound", "Magma Blast", "Searing Blast", "Shockwave", "Swipe"],
        "Stray Demon": ["Crushing Leaps", "Delayed Hammer Drive", "Ground Pound", "Hammer Blast", "Hammer Drive", "Leaping Hammer Smash", "Lumbering Swings", "Mighty Hammer Smash", "Retreating Sweep", "Shockwave", "Sidestep Left Sweep", "Sidestep Right Sweep", "Sweeping Strikes"],
        "The Four Kings": ["Blazing Wrath", "Cautious Arrow Mass", "Downward Slash", "Evasive Abyss Arrow", "Evasive Slash", "Executioner's Slash", "Forward Thrust", "Homing Abyss Arrow", "Homing Arrow Mass", "Horizontal Slash", "Into the Abyss", "Lifedrain Death Grasp", "Lifedrain Grab", "Pinpoint Homing Arrows", "Precision Slash", "Shockwave", "Thrust & Retreat", "Unerring Thrust", "Upward Slash", "Wrath of the Kings"],
        "The Last Giant": ["Arm Club Backhand", "Arm Club Sweep", "Arm Smash", "Armed Swings", "Backhand Strike", "Backstep Stomp", "Beat You With It", "Clubbing Blow", "Falling Slam", "Heavy Swings", "Left Foot Stomp", "Overhead Smash", "Right Foot Stomp", "Stomp Rush", "Sweeping Strike", "Triple Stomp"],
        "Vordt of the Boreal Valley": ["Backhand Swipe", "Berserk Rush", "Berserk Trample", "Crushing Charge", "Double Swipe", "Frostbreath", "Hammerfist Combo", "Hammerfist", "Handle Slam", "Jump Rush", "Mace Thrust", "Retreating Sweep", "Shove Left", "Shove Right", "Tracking Charge", "Trampling Charge", "Wild Swings"],
        "Vordt of the Boreal Valley (move)": ["Berserk Rush", "Berserk Trample", "Crushing Charge", "Jump Rush", "Shove Left", "Shove Right", "Tracking Charge", "Trampling Charge"],
        "Vordt of the Boreal Valley (attack)": ["Backhand Swipe", "Double Swipe", "Hammerfist Combo", "Hammerfist", "Handle Slam", "Mace Thrust", "Retreating Sweep", "Wild Swings"]
    }

    behaviorDetail = {
        "Alonne Bow Knight": {
            "behavior": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "health": 1,
            "armor": 1,
            "resist": 1
        },
        "Alonne Knight Captain": {
            "behavior": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "health": 5,
            "armor": 2,
            "resist": 2
        },
        "Alonne Sword Knight": {
            "behavior": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 1,
            "armor": 2,
            "resist": 2
        },
        "Black Hollow Mage": {
            "behavior": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 4},
                "middle": {}
            },
            "health": 5,
            "armor": 2,
            "resist": 3
        },
        "Bonewheel Skeleton": {
            "behavior": {
                "dodge": 2,
                "left": {"type": "push", "damage": 4},
                "middle": {},
                "right": {"repeat": 2}
            },
            "health": 1,
            "armor": 1,
            "resist": 1
        },
        "Crossbow Hollow": {
            "behavior": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 3},
                "right": {}
            },
            "health": 1,
            "armor": 1,
            "resist": 0
        },
        "Crow Demon": {
            "behavior": {
                "dodge": 2,
                "left": {"type": "push", "damage": 6},
                "middle": {},
                "right": {}
            },
            "health": 5,
            "armor": 1,
            "resist": 2
        },
        "Demonic Foliage": {
            "behavior": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 1,
            "armor": 2,
            "resist": 1
        },
        "Engorged Zombie": {
            "behavior": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 4},
                "right": {}
            },
            "health": 1,
            "armor": 2,
            "resist": 2
        },
        "Falchion Skeleton": {
            "behavior": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 3},
                "right": {"effect": ["bleed"]}
            },
            "health": 1,
            "armor": 1,
            "resist": 1
        },
        "Firebomb Hollow": {
            "behavior": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 3},
                "right": {}
            },
            "health": 1,
            "armor": 1,
            "resist": 1
        },
        "Giant Skeleton Archer": {
            "behavior": {
                "dodge": 2,
                "left": {"type": "push", "damage": 2},
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 5,
            "armor": 1,
            "resist": 1
        },
        "Giant Skeleton Soldier": {
            "behavior": {
                "dodge": 1,
                "left": {"type": "push", "damage": 2},
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 5,
            "armor": 1,
            "resist": 1
        },
        "Hollow Soldier": {
            "behavior": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "health": 1,
            "armor": 1,
            "resist": 1
        },
        "Ironclad Soldier": {
            "behavior": {
                "dodge": 2,
                "left": {"type": "push", "damage": 5},
                "middle": {"effect": ["stagger"]},
                "right": {}
            },
            "health": 5,
            "armor": 3,
            "resist": 2
        },
        "Large Hollow Soldier": {
            "behavior": {
                "dodge": 1,
                "left": {"type": "push", "damage": 5},
                "middle": {},
                "right": {}
            },
            "health": 5,
            "armor": 1,
            "resist": 0
        },
        "Mushroom Child": {
            "behavior": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 5,
            "armor": 1,
            "resist": 2
        },
        "Mushroom Parent": {
            "behavior": {
                "dodge": 1,
                "left": {"type": "push", "damage": 6},
                "middle": {"effect": ["stagger"]},
                "right": {}
            },
            "health": 10,
            "armor": 1,
            "resist": 2
        },
        "Necromancer": {
            "behavior": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 3},
                "middle": {}
            },
            "health": 5,
            "armor": 1,
            "resist": 2
        },
        "Phalanx": {
            "behavior": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 5},
                "middle": {},
                "right": {}
            },
            "health": 5,
            "armor": 1,
            "resist": 1
        },
        "Phalanx Hollow": {
            "behavior": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 4},
                "middle": {},
                "right": {}
            },
            "health": 1,
            "armor": 1,
            "resist": 1
        },
        "Plow Scarecrow": {
            "behavior": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "health": 1,
            "armor": 1,
            "resist": 1
        },
        "Sentinel": {
            "behavior": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "health": 10,
            "armor": 2,
            "resist": 1
        },
        "Shears Scarecrow": {
            "behavior": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 3},
                "right": {"repeat": 2}
            },
            "health": 1,
            "armor": 1,
            "resist": 1
        },
        "Silver Knight Greatbowman": {
            "behavior": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 4},
                "middle": {}
            },
            "health": 1,
            "armor": 2,
            "resist": 0
        },
        "Silver Knight Spearman": {
            "behavior": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {},
                "right": {}
            },
            "health": 1,
            "armor": 2,
            "resist": 1
        },
        "Silver Knight Swordsman": {
            "behavior": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 1,
            "armor": 2,
            "resist": 1
        },
        "Skeleton Archer": {
            "behavior": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 4},
                "middle": {}
            },
            "health": 1,
            "armor": 1,
            "resist": 1
        },
        "Skeleton Beast": {
            "behavior": {
                "dodge": 2,
                "left": {"type": "push", "damage": 4},
                "middle": {},
                "right": {"repeat": 2}
            },
            "health": 5,
            "armor": 2,
            "resist": 2
        },
        "Skeleton Soldier": {
            "behavior": {
                "dodge": 1,
                "left": {"type": "push", "damage": 2},
                "middle": {"effect": ["bleed"]},
                "right": {}
            },
            "health": 1,
            "armor": 2,
            "resist": 1
        },
        "Snow Rat": {
            "behavior": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 3},
                "right": {"effect": ["poison"]}
            },
            "health": 1,
            "armor": 0,
            "resist": 1
        },
        "Stone Guardian": {
            "behavior": {
                "dodge": 1,
                "left": {"type": "push", "damage": 4},
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 5,
            "armor": 2,
            "resist": 3
        },
        "Stone Knight": {
            "behavior": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "health": 5,
            "armor": 3,
            "resist": 2
        },
        "Mimic": {
            "behavior": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "health": 5,
            "armor": 1,
            "resist": 1
        },
        "Hungry Mimic": {
            "Raking Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "health": 18,
            "heatup": 8,
            "armor": 1,
            "resist": 1,
            "Heavy Punch": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Leaping Spin Kick": {
                "dodge": 2,
                "left": {"type": "push", "damage": 5},
                "middle": {},
                "right": {}
            },
            "Stomping Kick": {
                "dodge": 1,
                "left": {"type": "push", "damage": 6},
                "middle": {},
                "right": {}
            },
            "Charging Chomp": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "Vicious Chomp": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {},
                "right": {}
            },
            "Aggressive Grab": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            }
        },
        "Voracious Mimic": {
            "Raking Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "health": 18,
            "heatup": 8,
            "armor": 2,
            "resist": 2,
            "Heavy Punch": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Leaping Spin Kick": {
                "dodge": 2,
                "left": {"type": "push", "damage": 5},
                "middle": {},
                "right": {}
            },
            "Stomping Kick": {
                "dodge": 1,
                "left": {"type": "push", "damage": 6},
                "middle": {},
                "right": {}
            },
            "Charging Chomp": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "Vicious Chomp": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {},
                "right": {}
            },
            "Aggressive Grab": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            }
        },
        "Armorer Dennis": {
            "Soul Spear Launch": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "health": 16,
            "heatup": 10,
            "armor": 1,
            "resist": 2,
            "Soul Greatsword": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 6},
                "middle": {"effect": ["stagger"]},
                "right": {}
            },
            "Soul Vortex": {
                "dodge": 1,
                "repeat": 2,
                "middle": {"type": "magic", "damage": 4},
                "right": {}
            },
            "Soul Flash": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 4},
                "right": {}
            },
            "Upward Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["stagger"]}
            }
        },
        "Fencer Sharron": {
            "Puzzling Stone Sword Charge": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 20,
            "heatup": 12,
            "armor": 1,
            "resist": 1,
            "Puzzling Stone Sword Whip": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 6},
                "middle": {}
            },
            "Spider Fang Sword Strike": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Spider Fang Sword Charge": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Spider Fang Web Blast": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 5},
                "middle": {}
            },
            "Dual Sword Assault": {
                "dodge": 1,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Dual Sword Slash": {
                "dodge": 2,
                "left": {"type": "push", "damage": 6},
                "middle": {"effect": ["stagger"]},
                "right": {}
            }
        },
        "Invader Brylex": {
            "Leaping Strike": {
                "dodge": 1,
                "left": {"type": "push", "damage": 7},
                "middle": {},
                "right": {}
            },
            "health": 15,
            "heatup": 8,
            "armor": 2,
            "resist": 2,
            "Trampling Charge": {
                "dodge": 1,
                "left": {"type": "push", "damage": 4},
                "middle": {},
                "right": {}
            },
            "Blade Dervish": {
                "dodge": 1,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Fire Surge": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "Fire Whip": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 6},
                "right": {}
            }
        },
        "Kirk, Knight of Thorns": {
            "Forward Roll": {
                "dodge": 1,
                "left": {"type": "push", "damage": 3},
                "middle": {},
                "right": {}
            },
            "health": 12,
            "heatup": 7,
            "armor": 1,
            "resist": 1,
            "Shield Bash": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "Shield Charge": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "Overhead Chop": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 4},
                "right": {"effect": ["bleed"]}
            },
            "Barbed Sword Thrust": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 5},
                "middle": {},
                "right": {}
            }
        },
        "Longfinger Kirk": {
            "Rolling Barbs": {
                "dodge": 1,
                "left": {"type": "push", "damage": 4},
                "middle": {"effect": ["bleed"]},
                "right": {}
            },
            "health": 14,
            "heatup": 8,
            "armor": 2,
            "resist": 2,
            "Lunging Stab": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["bleed"]}
            },
            "Cleave": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Crushing Blow": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["bleed"]}
            },
            "Barbed Sword Strikes": {
                "dodge": 2,
                "repeat": 2,
                "left": {"type": "physical", "damage": 5},
                "middle": {},
                "right": {}
            }
        },
        "Maldron the Assassin": {
            "Greatlance Lunge": {
                "dodge": 3,
                "left": {"type": "push", "damage": 4},
                "right": {}
            },
            "health": 8,
            "heatup": 5,
            "armor": 1,
            "resist": 1,
            "Double Lance Lunge": {
                "dodge": 2,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "Leaping Lance Strike": {
                "dodge": 2,
                "left": {"type": "push", "damage": 5},
                "right": {}
            },
            "Jousting Charge": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Corrosive Urn Toss": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 3},
                "middle": {"effect": ["poison"]}
            }
        },
        "Maneater Mildred": {
            "Death Blow": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 18,
            "heatup": 10,
            "armor": 0,
            "resist": 0,
            "Executioner Strike": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "Guillotine": {
                "dodge": 1,
                "left": {"type": "push", "damage": 5},
                "middle": {"effect": ["stagger"]},
                "right": {}
            },
            "Butcher Chop": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {"effect": ["stagger"]}
            },
            "Butchery": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {"effect": ["stagger"]}
            }
        },
        "Marvelous Chester": {
            "Crossbow Volley": {
                "dodge": 1,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 17,
            "heatup": 9,
            "armor": 1,
            "resist": 2,
            "Crossbow Snipe": {
                "dodge": 4,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Throwing Knife Volley": {
                "dodge": 2,
                "repeat": 2,
                "left": {"type": "physical", "damage": 4},
                "middle": {"effect": ["bleed"]}
            },
            "Throwing Knife Flurry": {
                "dodge": 1,
                "repeat": 3,
                "left": {"type": "physical", "damage": 3},
                "middle": {"effect": ["bleed"]}
            },
            "Spinning Low Kick": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 5}
            }
        },
        "Melinda the Butcher": {
            "Double Smash": {
                "dodge": 2,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 3},
                "right": {}
            },
            "health": 20,
            "heatup": 11,
            "armor": 0,
            "resist": 0,
            "Cleaving Strikes": {
                "dodge": 1,
                "repeat": 2,
                "left": {"type": "physical", "damage": 4},
                "middle": {}
            },
            "Jumping Cleave": {
                "dodge": 1,
                "repeat": 3,
                "left": {"type": "physical", "damage": 3},
                "middle": {}
            },
            "Greataxe Sweep": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["stagger"]}
            },
            "Sweeping Advance": {
                "dodge": 1,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            }
        },
        "Oliver the Collector": {
            "Bone Fist Punches": {
                "dodge": 2,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "health": 15,
            "heatup": 10,
            "armor": 1,
            "resist": 0,
            "Minotaur Helm Charge": {
                "dodge": 1,
                "left": {"type": "push", "damage": 5},
                "middle": {"effect": ["stagger"]},
                "right": {}
            },
            "Puzzling Stone Sword Strike": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "Majestic Greatsword Slash": {
                "dodge": 2,
                "left": {"type": "push", "damage": 4},
                "middle": {}
            },
            "Santier's Spear Lunge": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["stagger"]}
            },
            "Smelter Hammer Whirlwind": {
                "dodge": 1,
                "repeat": 3,
                "left": {"type": "physical", "damage": 4},
                "middle": {},
                "right": {}
            },
            "Ricard's Rapier Thrust": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 4},
                "middle": {}
            }
        },
        "Paladin Leeroy": {
            "Advancing Grant Slam": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["stagger"]}
            },
            "health": 14,
            "heatup": 8,
            "armor": 2,
            "resist": 1,
            "Grant Slam Withdrawal": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 6},
                "middle": {"effect": ["stagger"]}
            },
            "Sanctus Shield Slam": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Sanctus Shield Dash": {
                "dodge": 2,
                "left": {"type": "push", "damage": 4},
                "middle": {},
                "right": {}
            },
            "Wrath of the Gods": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 5},
                "middle": {},
                "right": {}
            }
        },
        "Xanthous King Jeremiah": {
            "Great Chaos Fireball": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "health": 14,
            "heatup": 8,
            "armor": 0,
            "resist": 1,
            "Chaos Fire Whip": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 4},
                "right": {}
            },
            "Chaos Storm": {
                "dodge": 2,
                "repeat": 2,
                "left": {"type": "magic", "damage": 3},
                "middle": {},
                "right": {}
            },
            "Fiery Retreat": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 4},
                "middle": {}
            },
            "Whiplash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 4},
                "right": {"effect": ["bleed"]}
            }
        },
        "Old Dragonslayer": {
            "Darkness Bolt": {
                "dodge": 3,
                "middle": {"type": "magic", "damage": 4},
                "right": {}
            },
            "health": 20,
            "armor": 2,
            "resist": 2,
            "Spear Lunge": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Leaping Darkness": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 4},
                "right": {}
            },
            "Skewering Charge": {
                "dodge": 1,
                "left": {"type": "push", "damage": 4},
                "middle": {},
                "right": {}
            },
            "Spear Sweep": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 4},
                "middle": {}
            },
            "Darkness Falls": {
                "dodge": 1,
                "right": {"type": "magic", "damage": 5},
                "heatup": True
            },
            "Massive Sweep": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "heatup": True
            },
            "Lunging Combo": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 5},
                "right": {"type": "physical", "damage": 5},
                "heatup": True
            }
        },
        "Asylum Demon": {
            "Mighty Hammer Smash": {
                "dodge": 1,
                "middle": {"type": "push", "damage": 5}
            },
            "health": 34,
            "heatup": 16,
            "armor": 1,
            "resist": 1,
            "Leaping Hammer Smash": {
                "dodge": 1,
                "left": {"type": "push", "damage": 4},
                "middle": {}
            },
            "Ground Pound": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["stagger"]}
            },
            "Delayed Hammer Drive": {
                "dodge": 1,
                "middle": {"type": "push", "damage": 5},
                "right": {"effect": ["stagger"]}
            },
            "Hammer Drive": {
                "dodge": 2,
                "left": {"type": "push", "damage": 4},
                "middle": {"effect": ["stagger"]},
                "right": {}
            },
            "Retreating Sweep": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 4},
                "middle": {}
            },
            "Lumbering Swings": {
                "dodge": 1,
                "repeat": 2,
                "right": {"type": "physical", "damage": 4},
                "heatup": True
            },
            "Sweeping Strikes": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {"type": "physical", "damage": 4},
                "heatup": True
            },
            "Crushing Leaps": {
                "dodge": 1,
                "left": {"type": "push", "damage": 5},
                "middle": {"type": "push", "damage": 5},
                "right": {},
                "heatup": True
            }
        },
        "Boreal Outrider Knight": {
            "Backhand Slashes": {
                "dodge": 2,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {"effect": ["frostbite"]}
            },
            "health": 26,
            "heatup": 13,
            "armor": 2,
            "resist": 3,
            "Overhand Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Sweeping Strike": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 5},
                "middle": {}
            },
            "Chilling Thrust": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 4},
                "right": {"effect": ["frostbite"]}
            },
            "Leaping Frost": {
                "dodge": 1,
                "repeat": 2,
                "left": {"type": "physical", "damage": 4},
                "middle": {"effect": ["frostbite"]}
            },
            "Lunging Triple Slash": {
                "dodge": 1,
                "repeat": 3,
                "middle": {"type": "physical", "damage": 4},
                "right": {},
                "heatup": True
            },
            "Uppercut Slam": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["frostbite"]},
                "heatup": True
            },
            "Frost Breath": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 6},
                "right": {"effect": ["frostbite"]},
                "heatup": True
            }
        },
        "Winged Knight": {
            "Backhand Shaft Strike": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 24,
            "heatup": 12,
            "armor": 3,
            "resist": 1,
            "Overhand Smash": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Double Slash": {
                "dodge": 2,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {},
                "heatup": True
            },
            "Whirlwind": {
                "dodge": 1,
                "repeat": 3,
                "middle": {"type": "physical", "damage": 4},
                "right": {},
                "heatup": True
            },
            "Pillars of Light": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 5},
                "middle": {},
                "right": {},
                "heatup": True
            },
            "Sweeping Blade Swing": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Diagonal Uppercut": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 5},
                "middle": {}
            },
            "Charging Assault": {
                "dodge": 2,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            }
        },
        "Black Knight": {
            "Overhead Swing": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 4},
                "middle": {}
            },
            "health": 20,
            "heatup": 10,
            "armor": 3,
            "resist": 2,
            "Heavy Slash": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 5},
                "middle": {"effect": ["stagger"]}
            },
            "Backswing": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 5},
                "middle": {"effect": ["stagger"]}
            },
            "Vicious Hack": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 5},
                "middle": {}
            },
            "Defensive Strike": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 5},
                "middle": {}
            },
            "Wide Swing": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 4},
                "middle": {"effect": ["stagger"]}
            },
            "Massive Swing": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 5},
                "middle": {},
                "heatup": True
            },
            "Hacking Slash": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 5},
                "middle": {"effect": ["stagger"]},
                "right": {"type": "push", "damage": 4},
                "heatup": True
            },
            "Charge": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {"effect": ["stagger"]},
                "heatup": True
            }
        },
        "Heavy Knight": {
            "Defensive Swipe": {
                "dodge": 3,
                "left": {"type": "physical", "damage": 4},
                "heatup": True
            },
            "health": 25,
            "heatup": 15,
            "armor": 2,
            "resist": 2,
            "Charging Chop": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "heatup": True
            },
            "Defensive Chop": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 5},
                "heatup": True
            },
            "Overhead Chop": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["stagger"]}
            },
            "Shield Swipe": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {"effect": ["stagger"]}
            },
            "Double Slash": {
                "dodge": 1,
                "repeat": 2,
                "left": {"type": "physical", "damage": 4},
                "middle": {"effect": ["stagger"]}
            },
            "Slashing Blade": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 4},
                "right": {"effect": ["stagger"]}
            },
            "Double Chop": {
                "dodge": 1,
                "repeat": 2,
                "left": {"type": "physical", "damage": 5},
                "middle": {"effect": ["stagger"]}
            },
            "Shield Smash": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 4},
                "right": {"effect": ["stagger"] }
            }
        },
        "Titanite Demon": {
            "Double Swing": {
                "dodge": 1,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "health": 22,
            "heatup": 10,
            "armor": 3,
            "resist": 2,
            "Tail Whip": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "Grab & Smash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Lightning Bolt": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "Vicious Swing": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Sweeping Strike": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {},
                "heatup": True
            },
            "Vaulting Slam": {
                "dodge": 2,
                "left": {"type": "push", "damage": 6},
                "right": {},
                "heatup": True
            },
            "Double Pole Crush": {
                "dodge": 1,
                "repeat": 2,
                "left": {"type": "physical", "damage": 5},
                "middle": {},
                "heatup": True
            }
        },
        "Gargoyle": {
            "Sweeping Strike": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 26,
            "heatup": 12,
            "armor": 2,
            "resist": 1,
            "Halberd Thrust": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Tail Sweep": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "Tail Whip": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 4},
                "middle": {}
            },
            "Electric Breath": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 4},
                "right": {}
            },
            "Flying Tail Whip": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {},
                "heatup": True
            },
            "Swooping Cleave": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {},
                "heatup": True
            },
            "Aerial Electric Breath": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 5},
                "right": {},
                "heatup": True
            }
        },
        "Smelter Demon": {
            "Double Sweep": {
                "dodge": 1,
                "repeat": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {}
            },
            "health": 22,
            "heatup": 11,
            "armor": 4,
            "resist": 3,
            "Overhead Chop": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["stagger"]}
            },
            "Fiery Blast": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 5},
                "middle": {},
                "right": {}
            },
            "Leaping Impalement Strike": {
                "dodge": 2,
                "left": {"type": "push", "damage": 4},
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "Sweeping Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Lunging Strike": {
                "dodge": 1,
                "right": {"type": "physical", "damage": 7}
            },
            "Flaming Impalement Strike": {
                "dodge": 2,
                "left": {"type": "push", "damage": 4},
                "middle": {"type": "magic", "damage": 4},
                "right": {},
                "heatup": True
            },
            "Fiery Explosion": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 6},
                "middle": {},
                "right": {},
                "heatup": True
            },
            "Flaming Double Sweep": {
                "dodge": 1,
                "repeat": 2,
                "left": {"type": "magic", "damage": 6},
                "middle": {},
                "heatup": True
            },
            "Flaming Sweeping Slash": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 6},
                "right": {},
                "heatup": True
            },
            "Flaming Overhead Chop": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 6},
                "right": {"effect": ["stagger"]},
                "heatup": True
            },
            "Flame Wave": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 5},
                "right": {},
                "heatup": True
            },
            "Flaming Lunging Strike": {
                "dodge": 1,
                "right": {"type": "magic", "damage": 7},
                "heatup": True
            }
        },
        "The Pursuer": {
            "Wide Blade Swing": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "health": 28,
            "heatup": 12,
            "armor": 3,
            "resist": 2,
            "Stabbing Strike": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Rising Blade Swing": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Overhead Cleave": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Cursed Impale": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "Dark Magic": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 4},
                "right": {}
            },
            "Shield Bash": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "Shield Smash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Forward Dash": {
                "dodge": 0
            },
            "Back Dash": {
                "dodge": 0
            }
        },
        "Crossbreed Priscilla": {
            "Icy Blast": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 5}
            },
            "health": 40,
            "heatup": 25,
            "armor": 2,
            "resist": 1,
            "Flanking Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["bleed"]}
            },
            "Scything Withdrawal": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 5},
                "middle": {"effect": ["bleed"]}
            },
            "Blizzard": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5}
            },
            "Scythe Strike": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["bleed"]}
            },
            "Scythe Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["bleed"]}
            },
            "Snowstorm": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 4}
            },
            "Backslash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["bleed"]}
            },
            "Mournful Gaze": {
                "dodge": 3,
                "middle": {"type": "magic", "damage": 3},
                "right": {"effect": ["frostbite"]}
            },
            "Scything Lunge": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {"effect": ["bleed"]}
            },
            "Double Lunge": {
                "dodge": 2,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["bleed"]},
                "heatup": True
            },
            "Double Strike": {
                "dodge": 2,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["bleed"]},
                "heatup": True
            },
            "Double Slash": {
                "dodge": 1,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["bleed"]},
                "heatup": True
            }
        },
        "Gravelord Nito": {
            "Gravelord Greatsword": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 4},
                "right": {}
            },
            "health": 30,
            "heatup": 15,
            "armor": 2,
            "resist": 2,
            "Death Wave": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "Miasma": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 3},
                "middle": {},
                "right": {}
            },
            "Sword Slam": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Sword Sweep": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Deathly Thrust": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["poison"]}
            },
            "Death Grip": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 5},
                "middle": {}
            },
            "Deathly Strike": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 5},
                "middle": {}
            },
            "Toxicity": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 4},
                "right": {"effect": ["poison"]}
            },
            "Entropy": {
                "dodge": 1,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 4},
                "right": {"effect": ["poison"]}
            },
            "Creeping Death": {
                "dodge": 1,
                "repeat": 3,
                "left": {"type": "push", "damage": 5},
                "middle": {"effect": ["poison"]},
                "heatup": True
            },
            "Death's Embrace": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 5},
                "middle": {"effect": ["poison"]},
                "heatup": True
            },
            "Lunging Cleave": {
                "dodge": 2,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["poison"]},
                "heatup": True
            }
        },
        "Great Grey Wolf Sif": {
            "Dashing Slice": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 7},
                "right": {}
            },
            "health": 36,
            "heatup": 19,
            "armor": 2,
            "resist": 3,
            "Spinning Slash": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 6},
                "middle": {},
                "right": {}
            },
            "Sword Slam": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["stagger"]}
            },
            "Evasive Strike": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 6},
                "middle": {}
            },
            "Upward Slash": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 7},
                "right": {}
            },
            "Pouncing Assault": {
                "dodge": 2,
                "left": {"type": "push", "damage": 6},
                "middle": {"effect": ["stagger"]},
                "right": {}
            },
            "Slashing Assault": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {"type": "physical", "damage": 5}
            },
            "Sidestep Cleave": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Sidestep Slash": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Slashing Retreat": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 5},
                "middle": {}
            },
            "Feral Onslaught": {
                "dodge": 2,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["stagger"]},
                "heatup": True
            },
            "Cyclone Strikes": {
                "dodge": 2,
                "repeat": 2,
                "left": {"type": "physical", "damage": 7},
                "middle": {"effect": ["stagger"]},
                "heatup": True
            },
            "Savage Retreat": {
                "dodge": 2,
                "repeat": 3,
                "left": {"type": "physical", "damage": 6},
                "middle": {"effect": ["stagger"]},
                "heatup": True
            },
            "Limping Strike": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 2},
                "right": {}
            }
        },
        "Ornstein & Smough": {
            "Ornstein": {
                "health": 20,
                "armor": 3,
                "resist": 3,
                "heatup": 0
            },
            "Smough": {
                "health": 30,
                "armor": 2,
                "resist": 2,
                "heatup": 0
            },
            "Gliding Stab & Hammer Smash": {
                "Gliding Stab": {
                    "dodge": 3,
                    "right": {"type": "physical", "damage": 5}
                },
                "Hammer Smash": {
                    "dodge": 1,
                    "right": {"type": "physical", "damage": 5}
                }
            },
            "Evasive Sweep & Trampling Charge": {
                "Evasive Sweep": {
                    "dodge": 2,
                    "right": {"type": "physical", "damage": 4}
                },
                "Trampling Charge": {
                    "dodge": 1,
                    "left": {"type": "push", "damage": 5},
                    "right": {}
                }
            },
            "Spear Slam & Hammer Sweep": {
                "Spear Slam": {
                    "dodge": 1,
                    "right": {"type": "physical", "damage": 5}
                },
                "Hammer Sweep": {
                    "dodge": 1,
                    "left": {"type": "physical", "damage": 5}
                }
            },
            "Swiping Combo & Bonzai Drop": {
                "Swiping Combo": {
                    "dodge": 1,
                    "repeat": 2,
                    "right": {"type": "physical", "damage": 5}
                },
                "Bonzai Drop": {
                    "dodge": 2,
                    "left": {"type": "push", "damage": 5},
                    "right": {}
                }
            },
            "Lightning Bolt & Jumping Slam": {
                "Lightning Bolt": {
                    "dodge": 1,
                    "left": {"type": "magic", "damage": 5},
                    "right": {}
                },
                "Jumping Slam": {
                    "dodge": 1,
                    "right": {"type": "physical", "damage": 6}
                }
            },
            "Charged Swiping Combo": {
                "dodge": 1,
                "repeat": 3,
                "middle": {"type": "magic", "damage": 5},
                "right": {},
                "heatup": "Ornstein"
            },
            "Charged Bolt": {
                "dodge": 3,
                "left": {"type": "magic", "damage": 6},
                "middle": {},
                "right": {},
                "heatup": "Ornstein"
            },
            "Electric Clash": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 6},
                "middle": {},
                "right": {},
                "heatup": "Ornstein"
            },
            "Lightning Stab": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 7},
                "right": {},
                "heatup": "Ornstein"
            },
            "High Voltage": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 6},
                "right": {},
                "heatup": "Ornstein"
            },
            "Electric Hammer Smash": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 6},
                "right": {},
                "heatup": "Smough"
            },
            "Lightning Sweep": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 6},
                "right": {},
                "heatup": "Smough"
            },
            "Jumping Volt Slam": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 5},
                "right": {},
                "heatup": "Smough"
            },
            "Electric Bonzai Drop": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 7},
                "right": {},
                "heatup": "Smough"
            },
            "Charged Charge": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 6},
                "right": {},
                "heatup": "Smough"
            }
        },
        "Dancer of the Boreal Valley": {
            "Uppercut": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 34,
            "heatup": 18,
            "armor": 2,
            "resist": 2,
            "Blade Dance": {
                "dodge": 1,
                "repeat": 2,
                "right": {"type": "physical", "damage": 5},
                "heatup": True
            },
            "Plunging Assault": {
                "dodge": 1,
                "repeat": 3,
                "left": {"type": "push", "damage": 6},
                "middle": {},
                "right": {},
                "heatup": True
            },
            "Whirling Blades": {
                "dodge": 1,
                "repeat": 4,
                "right": {"type": "physical", "damage": 6},
                "heatup": True
            },
            "Double Slash": {
                "dodge": 1,
                "repeat": 2,
                "right": {"type": "physical", "damage": 5}
            },
            "Plunging Attack": {
                "dodge": 2,
                "left": {"type": "push", "damage": 6},
                "middle": {},
                "right": {}
            },
            "Triple Slash": {
                "dodge": 1,
                "repeat": 3,
                "right": {"type": "physical", "damage": 5}
            },
            "Lunging Thrust": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Backhand Blade Swipe": {
                "dodge": 2,
                "right": {"type": "physical", "damage": 7}
            },
            "Flashing Blade": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Deadly Grasp": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 7},
                "right": {}
            },
            "Sweeping Blade Swipe": {
                "dodge": 2,
                "right": {"type": "physical", "damage": 7}
            },
            "Ash Cloud": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 6},
                "middle": {}
            }
        },
        "Artorias": {
            "Steadfast Leap": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 25,
            "heatup": 15,
            "armor": 3,
            "resist": 3,
            "Somersault Slam": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "Overhead Cleave": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["stagger"]}
            },
            "Charging Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Heavy Thrust": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Spinning Slash": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 5},
                "middle": {},
                "right": {}
            },
            "Abyss Sludge": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 6},
                "middle": {"effect": ["stagger"]}
            },
            "Wrath of the Abyss": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 6},
                "middle": {},
                "right": {}
            },
            "Somersault Strike": {
                "dodge": 2,
                "left": {"type": "push", "damage": 5},
                "middle": {},
                "right": {}
            },
            "Retreating Strike": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 5},
                "middle": {"effect": ["stagger"]}
            },
            "Abyss Assault": {
                "dodge": 2,
                "left": {"type": "push", "damage": 5},
                "middle": {"type": "magic", "damage": 5},
                "right": {},
                "heatup": True
            },
            "Leaping Fury": {
                "dodge": 2,
                "left": {"type": "push", "damage": 5},
                "middle": {"type": "push", "damage": 6},
                "right": {},
                "heatup": True
            },
            "Lunging Cleave": {
                "dodge": 2,
                "left": {"type": "push", "damage": 5},
                "middle": {"type": "physical", "damage": 6},
                "right": {},
                "heatup": True
            }
        },
        "Sir Alonne": {
            "Lunging Slash Combo": {
                "dodge": 2,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 6},
                "heatup": True
            },
            "health": 26,
            "heatup": 12,
            "armor": 3,
            "resist": 3,
            "Triple Slash Combo": {
                "dodge": 2,
                "repeat": 3,
                "middle": {"type": "physical", "damage": 5},
                "right": {},
                "heatup": True
            },
            "Stabbing Slash Combo": {
                "dodge": 2,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 6},
                "heatup": True
            },
            "Fast Katana Lunge": {
                "dodge": 2,
                "right": {"type": "physical", "damage": 5}
            },
            "Charging Katana Slash": {
                "dodge": 1,
                "right": {"type": "physical", "damage": 6}
            },
            "Charging Katana Lunge": {
                "dodge": 2,
                "right": {"type": "physical", "damage": 6}
            },
            "Dark Wave": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "Life Drain": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 7},
                "right": {}
            },
            "Double Slash Combo": {
                "dodge": 1,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "Left Sidestep Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Stab & Slash Combo": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {"type": "physical", "damage": 5}
            },
            "Right Sidestep Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Katana Plunge": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            }
        },
        "Stray Demon": {
            "Mighty Hammer Smash": {
                "dodge": 1,
                "middle": {"type": "push", "damage": 8},
                "right": {}
            },
            "health": 34,
            "heatup": 16,
            "armor": 4,
            "resist": 3,
            "Leaping Hammer Smash": {
                "dodge": 2,
                "left": {"type": "push", "damage": 6},
                "middle": {}
            },
            "Ground Pound": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 9},
                "right": {"effect": ["stagger"]}
            },
            "Delayed Hammer Drive": {
                "dodge": 1,
                "middle": {"type": "push", "damage": 8},
                "right": {"effect": ["stagger"]}
            },
            "Hammer Drive": {
                "dodge": 3,
                "left": {"type": "push", "damage": 6},
                "middle": {"effect": ["stagger"]},
                "right": {}
            },
            "Retreating Sweep": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {}
            },
            "Lumbering Swings": {
                "dodge": 1,
                "repeat": 2,
                "right": {"type": "physical", "damage": 7},
                "heatup": True
            },
            "Sweeping Strikes": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 7},
                "right": {"type": "physical", "damage": 7},
                "heatup": True
            },
            "Crushing Leaps": {
                "dodge": 2,
                "left": {"type": "push", "damage": 7},
                "middle": {"type": "push", "damage": 7},
                "right": {},
                "heatup": True
            },
            "Sidestep Right Sweep": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Sidestep Left Sweep": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Hammer Blast": {
                "dodge": 3,
                "left": {"type": "magic", "damage": 5},
                "middle": {},
                "right": {}
            },
            "Shockwave": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 8},
                "right": {}
            }
        },
        "Manus, Father of the Abyss": {
            "Ground Slam": {
                "dodge": 3,
                "left": {"type": "physical", "damage": 6},
                "middle": {}
            },
            "health": 48,
            "heatup": 28,
            "armor": 3,
            "resist": 3,
            "Diving Slam": {
                "dodge": 1,
                "left": {"type": "push", "damage": 7},
                "middle": {},
                "right": {}
            },
            "Sweeping Strike": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {}
            },
            "Extended Sweep": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {},
                "right": {}
            },
            "Back Swipe": {
                "dodge": 3,
                "left": {"type": "physical", "damage": 6},
                "middle": {}
            },
            "Frenzied Attacks": {
                "dodge": 1,
                "repeat": 3,
                "left": {"type": "physical", "damage": 5},
                "middle": {}
            },
            "Crushing Palm": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 7},
                "right": {}
            },
            "Catalyst Strike": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "Catalyst Smash": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 6},
                "right": {}
            },
            "Dark Orb Barrage": {
                "dodge": 3,
                "left": {"type": "magic", "damage": 5},
                "middle": {},
                "heatup": True
            },
            "Descending Darkness": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 6},
                "middle": {},
                "heatup": True
            },
            "Abyss Rain": {
                "dodge": 3,
                "left": {"type": "magic", "damage": 4},
                "middle": {},
                "heatup": True
            },
            "Abyss Cage": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 6},
                "middle": {},
                "heatup": True
            },
            "Ring of Darkfire": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 7},
                "middle": {},
                "heatup": True
            }
        },
        "The Four Kings": {
            "Horizontal Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {}
            },
            "health": 25,
            "armor": 2,
            "resist": 2,
            "Upward Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["stagger"]}
            },
            "Downward Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["stagger"]}
            },
            "Forward Thrust": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Wrath of the Kings": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 4},
                "middle": {},
                "right": {}
            },
            "Homing Arrow Mass": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 4}
            },
            "Homing Abyss Arrow": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5}
            },
            "Lifedrain Grab": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5},
                "right": {"effect": ["stagger"]}
            },
            "Evasive Slash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "heatup": 2
            },
            "Thrust & Retreat": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "heatup": 2
            },
            "Cautious Arrow Mass": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5},
                "heatup": 2
            },
            "Evasive Abyss Arrow": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 5},
                "heatup": 2
            },
            "Precision Slash": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 5},
                "right": {},
                "heatup": 3
            },
            "Unerring Thrust": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 6},
                "right": {},
                "heatup": 3
            },
            "Blazing Wrath": {
                "dodge": 3,
                "left": {"type": "magic", "damage": 4},
                "middle": {},
                "right": {},
                "heatup": 3
            },
            "Pinpoint Homing Arrows": {
                "dodge": 3,
                "middle": {"type": "magic", "damage": 4},
                "right": {},
                "heatup": 3
            },
            "Executioner's Slash": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["stagger"]},
                "heatup": 4
            },
            "Shockwave": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 5},
                "middle": {"effect": ["stagger"]},
                "right": {},
                "heatup": 4
            },
            "Into the Abyss": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 5},
                "right": {"effect": ["stagger"]},
                "heatup": 4
            },
            "Lifedrain Death Grasp": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 5},
                "right": {"effect": ["stagger"]},
                "heatup": 4
            }
        },
        "The Last Giant": {
            "Left Foot Stomp": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "health": 44,
            "heatup": 18,
            "armor": 3,
            "resist": 3,
            "Right Foot Stomp": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Stomp Rush": {
                "dodge": 1,
                "repeat": 3,
                "left": {"type": "push", "damage": 5},
                "middle": {},
                "right": {}
            },
            "Backstep Stomp": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {}
            },
            "Triple Stomp": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 5},
                "middle": {"type": "physical", "damage": 5},
                "right": {"type": "physical", "damage": 5}
            },
            "Sweeping Strike": {
                "dodge": 2,
                "right": {"type": "physical", "damage": 7},
                "arm": True
            },
            "Backhand Strike": {
                "dodge": 2,
                "right": {"type": "physical", "damage": 7},
                "arm": True
            },
            "Clubbing Blow": {
                "dodge": 2,
                "right": {"type": "physical", "damage": 7},
                "arm": True
            },
            "Heavy Swings": {
                "dodge": 1,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 6},
                "arm": True
            },
            "Overhead Smash": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["stagger"]},
                "arm": True
            },
            "Arm Club Sweep": {
                "dodge": 2,
                "right": {"type": "physical", "damage": 7},
                "heatup": True
            },
            "Arm Club Backhand": {
                "dodge": 2,
                "right": {"type": "physical", "damage": 7},
                "heatup": True
            },
            "Beat You With It": {
                "dodge": 2,
                "right": {"type": "physical", "damage": 7},
                "heatup": True
            },
            "Armed Swings": {
                "dodge": 1,
                "repeat": 2,
                "middle": {"type": "physical", "damage": 6},
                "heatup": True
            },
            "Arm Smash": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["stagger"]},
                "heatup": True
            },
            "Falling Slam": {
                "dodge": 1,
                "left": {"type": "push", "damage": 9},
                "middle": {},
                "right": {}
            }
        },
        "Guardian Dragon": {
            "Fireball": {
                "dodge": 3,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "health": 44,
            "heatup": 28,
            "armor": 3,
            "resist": 3,
            "Fire Breath": {
                "dodge": 1,
                "repeat": 2,
                "left": {"type": "magic", "damage": 5},
                "middle": {}
            },
            "Leaping Breath": {
                "dodge": 1,
                "repeat": 2,
                "left": {"type": "magic", "damage": 4},
                "middle": {}
            },
            "Fire Sweep": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 4},
                "middle": {"type": "magic", "damage": 4}
            },
            "Charging Flame": {
                "dodge": 2,
                "repeat": 2,
                "left": {"type": "magic", "damage": 5},
                "middle": {}
            },
            "Tail Sweep": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["stagger"]}
            },
            "Bite": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 8},
                "middle": {"effect": ["stagger"]},
                "right": {}
            },
            "Left Stomp": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {"effect": ["stagger"]}
            },
            "Right Stomp": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {"effect": ["stagger"]}
            },
            "Cage Grasp Inferno": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 5},
                "middle": {},
                "heatup": True
            }
        },
        "Gaping Dragon": {
            "Crawling Charge": {
                "dodge": 2,
                "middle": {"type": "push", "damage": 5}
            },
            "health": 46,
            "heatup": 26,
            "armor": 3,
            "resist": 2,
            "Stomach Slam": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 7}
            },
            "Right Hook": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["stagger"]}
            },
            "Triple Stomp": {
                "dodge": 2,
                "repeat": 3,
                "left": {"type": "physical", "damage": 6},
                "middle": {}
            },
            "Claw Swipe": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 7},
                "right": {}
            },
            "Tail Whip": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 7},
                "middle": {"effect": ["stagger"]}
            },
            "Flying Smash": {
                "dodge": 1,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Gorge": {
                "dodge": 3,
                "repeat": 3,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["stagger"]}
            },
            "Stomp Slam": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "right": {"type": "physical", "damage": 6}
            },
            "Corrosive Ooze (Front Right Left)": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 5},
                "middle": {"effect": ["corrosion"]},
                "right": {},
                "heatup": True
            },
            "Corrosive Ooze (Front Left)": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 6},
                "middle": {"effect": ["corrosion"]},
                "right": {},
                "heatup": True
            },
            "Corrosive Ooze (Front Right)": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 6},
                "middle": {"effect": ["corrosion"]},
                "right": {},
                "heatup": True
            },
            "Corrosive Ooze (Front)": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 7},
                "middle": {"effect": ["corrosion"]},
                "right": {},
                "heatup": True
            }
        },
        "Vordt of the Boreal Valley": {
            "Frostbreath": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 5},
                "middle": {"effect": ["frostbite"]},
                "right": {}
            },
            "health": 42,
            "heatup1": 14,
            "heatup2": 28,
            "armor": 3,
            "resist": 3,
            "Tracking Charge": {
                "dodge": 1,
                "right": {"type": "push", "damage": 5},
                "type": "move"
            },
            "Shove Right": {
                "dodge": 1,
                "left": {"type": "push", "damage": 5},
                "type": "move"
            },
            "Shove Left": {
                "dodge": 1,
                "right": {"type": "push", "damage": 5},
                "type": "move"
            },
            "Crushing Charge": {
                "dodge": 1,
                "left": {"type": "push", "damage": 5},
                "middle": {},
                "type": "move"
            },
            "Jump Rush": {
                "dodge": 1,
                "left": {"type": "push", "damage": 5},
                "middle": {},
                "type": "move"
            },
            "Trampling Charge": {
                "dodge": 1,
                "left": {"type": "push", "damage": 5},
                "type": "move"
            },
            "Berserk Rush": {
                "dodge": 2,
                "repeat": 3,
                "left": {"type": "push", "damage": 6},
                "middle": {},
                "type": "move",
                "heatup": True
            },
            "Berserk Trample": {
                "dodge": 2,
                "repeat": 2,
                "left": {"type": "push", "damage": 6},
                "middle": {},
                "type": "move",
                "heatup": True
            },
            "Double Swipe": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 5},
                "middle": {"type": "magic", "damage": 5},
                "right": {},
                "type": "attack"
            },
            "Mace Thrust": {
                "dodge": 3,
                "left": {"type": "physical", "damage": 6},
                "middle": {},
                "right": {},
                "type": "attack"
            },
            "Backhand Swipe": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 5},
                "middle": {},
                "right": {},
                "type": "attack"
            },
            "Retreating Sweep": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 5},
                "middle": {},
                "type": "attack"
            },
            "Hammerfist": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {},
                "right": {},
                "type": "attack"
            },
            "Handle Slam": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {},
                "right": {},
                "type": "attack"
            },
            "Wild Swings": {
                "dodge": 1,
                "repeat": 3,
                "left": {"type": "magic", "damage": 6},
                "middle": {},
                "type": "attack",
                "heatup": True
            },
            "Hammerfist Combo": {
                "dodge": 1,
                "repeat": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {},
                "type": "attack",
                "heatup": True
            }
        },
        "Black Dragon Kalameet": {
            "Mark of Calamity": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 4},
                "right": {"effect": ["calamity"]}
            },
            "health": 38,
            "heatup": 22,
            "armor": 4,
            "resist": 3,
            "Hellfire Blast": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 5}
            },
            "Sweeping Flame": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 6},
                "right": {}
            },
            "Consuming Blaze": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 6},
                "middle": {}
            },
            "Conflagration": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 6},
                "middle": {}
            },
            "Rising Inferno": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 7},
                "middle": {},
                "right": {}
            },
            "Flame Feint": {
                "dodge": 1,
                "right": {"type": "magic", "damage": 6}
            },
            "Head Strike": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["stagger"]}
            },
            "Tail Sweep": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 5},
                "middle": {}
            },
            "Rush Strike": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["stagger"]}
            },
            "Evasive Tail Whip": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 5},
                "middle": {}
            },
            "Swooping Charge": {
                "dodge": 2,
                "left": {"type": "push", "damage": 5},
                "middle": {"effect": ["stagger"]}
            },
            "Hellfire Barrage": {
                "dodge": 2,
                "middle": {"type": "magic", "damage": 6},
                "heatup": True
            }
        },
        "Old Iron King": {
            "Fist Pound": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {"effect": ["stagger"]},
                "right": {}
            },
            "health": 44,
            "heatup": 22,
            "armor": 3,
            "resist": 3,
            "Double Fist Pound": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {"effect": ["stagger"]},
                "right": {}
            },
            "Swipe": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 6},
                "middle": {},
                "right": {}
            },
            "Shockwave": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 5},
                "middle": {},
                "right": {}
            },
            "Bash": {
                "dodge": 3,
                "left": {"type": "physical", "damage": 6},
                "middle": {"effect": ["stagger"]},
                "right": {}
            },
            "Searing Blast": {
                "dodge": 1,
                "left": {"type": "magic", "damage": 6},
                "middle": {},
                "right": {}
            },
            "Double Swipe": {
                "dodge": 2,
                "left": {"type": "physical", "damage": 6},
                "middle": {"type": "physical", "damage": 6},
                "right": {},
                "heatup": True
            },
            "Firestorm": {
                "dodge": 2,
                "left": {"type": "magic", "damage": 5},
                "middle": {},
                "right": {},
                "heatup": True
            },
            "Magma Blast": {
                "dodge": 3,
                "left": {"type": "magic", "damage": 6},
                "middle": {},
                "right": {},
                "heatup": True
            },
            "Fire Beam (Left)": {
                "dodge": 1,
                "right": {"type": "magic", "damage": 5}
            },
            "Fire Beam (Right)": {
                "dodge": 1,
                "right": {"type": "magic", "damage": 5}
            },
            "Fire Beam (Front)": {
                "dodge": 1,
                "right": {"type": "magic", "damage": 6}
            }
        },
        "Executioner Chariot": {
            "Death Race": {
                "dodge": 1,
                "left": {"type": "physical", "damage": 7},
                "middle": {},
                "right": {}
            },
            "health": 24,
            "armor": 3,
            "resist": 3,
            "Charging Ram": {
                "dodge": 2,
                "middle": {"type": "physical", "damage": 6},
                "right": {}
            },
            "Roiling Darkness": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "Stomp Rush": {
                "dodge": 2,
                "repeat": 2,
                "left": {"type": "physical", "damage": 7},
                "middle": {},
                "heatup": True
            },
            "Trampling Charge": {
                "dodge": 2,
                "left": {"type": "push", "damage": 6},
                "middle": {},
                "right": {}
            },
            "Engulfing Darkness": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "Advancing Back Kick": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 6},
                "right": {"effect": ["stagger"]}
            },
            "Charging Breath": {
                "dodge": 1,
                "middle": {"type": "magic", "damage": 5},
                "right": {}
            },
            "Headbutt": {
                "dodge": 3,
                "middle": {"type": "physical", "damage": 5},
                "right": {"effect": ["stagger"]}
            },
            "Deadly Breath": {
                "dodge": 3,
                "middle": {"type": "magic", "damage": 6},
                "right": {},
                "heatup": True
            },
            "Rearing Charge": {
                "dodge": 2,
                "left": {"type": "push", "damage": 4},
                "middle": {"type": "push", "damage": 5},
                "right": {}
            },
            "Back Kick": {
                "dodge": 3,
                "left": {"type": "physical", "damage": 6},
                "middle": {"effect": ["stagger"]}
            },
            "Merciless Charge": {
                "dodge": 1,
                "middle": {"type": "push", "damage": 6},
                "right": {"type": "push", "damage": 6},
                "heatup": True
            }
        }
    }

except Exception as e:
    log(e, exception=True)
    raise