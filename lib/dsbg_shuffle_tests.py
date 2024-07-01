from json import load
from collections import Counter
from random import choice
import types

from dsbg_shuffle_behaviors import behaviorDetail
from dsbg_shuffle_enemies import enemyIds, enemiesDict, bosses
from dsbg_shuffle_utility import baseFolder, pathSep
from dsbg_shuffle_variants import modIdLookup


with open(baseFolder + "\\lib\\dsbg_shuffle_enemies.json".replace("\\", pathSep)) as enemiesFile:
    enemies = load(enemiesFile)

with open(baseFolder + "\\lib\\dsbg_shuffle_invaders_standard.json".replace("\\", pathSep)) as invadersStandardFile:
    invadersStandard = load(invadersStandardFile)

with open(baseFolder + "\\lib\\dsbg_shuffle_invaders_advanced.json".replace("\\", pathSep)) as invadersAdvancedFile:
    invadersAdvanced = load(invadersAdvancedFile)

with open(baseFolder + "\\lib\\dsbg_shuffle_encounters.json".replace("\\", pathSep)) as encountersFile:
    encounters = load(encountersFile)

osBehaviorLookup = {
    "Gliding Stab": "Gliding Stab & Hammer Smash",
    "Hammer Smash": "Gliding Stab & Hammer Smash",
    "Evasive Sweep": "Evasive Sweep & Trampling Charge",
    "Trampling Charge": "Evasive Sweep & Trampling Charge",
    "Spear Slam": "Spear Slam & Hammer Sweep",
    "Hammer Sweep": "Spear Slam & Hammer Sweep",
    "Swiping Combo": "Swiping Combo & Bonzai Drop",
    "Bonzai Drop": "Swiping Combo & Bonzai Drop",
    "Lightning Bolt": "Lightning Bolt & Jumping Slam",
    "Jumping Slam": "Lightning Bolt & Jumping Slam",
    "Charged Swiping Combo": "Charged Swiping Combo",
    "Charged Bolt": "Charged Bolt",
    "Electric Clash": "Electric Clash",
    "Lightning Stab": "Lightning Stab",
    "High Voltage": "High Voltage",
    "Electric Hammer Smash": "Electric Hammer Smash",
    "Lightning Sweep": "Lightning Sweep",
    "Jumping Volt Slam": "Jumping Volt Slam",
    "Electric Bonzai Drop": "Electric Bonzai Drop",
    "Charged Charge": "Charged Charge"
}


class Tester():
    def __init__(self):
        self.allEnemies = enemies | invadersStandard | invadersAdvanced
        self.selected = None
        self.newEnemies = []
        self.newTiles = dict()
        self.variants = {}
        self.currentVariants = {}
        skip = True
        
        for enemy in list(enemiesDict.keys()) + list(bosses.keys()):
            with open(baseFolder + "\\lib\\dsbg_shuffle_difficulty\\dsbg_shuffle_difficulty_" + enemy + ".json", "r") as f:
                enemyDifficulty = load(f)

            self.variants[enemy] = {1: {}, 2: {}, 3: {}, 4: {}}
            for x in range(1, 5):
                for diffInc in enemyDifficulty[str(x)]:
                    self.variants[enemy][x][float(diffInc)] = {}
                    for defKey in enemyDifficulty[str(x)][diffInc]:
                        self.variants[enemy][x][float(diffInc)][frozenset([""] if not defKey else [int(k) for k in defKey.split(",")])] = enemyDifficulty[str(x)][diffInc][defKey]

                self.variants[enemy][x] = {k: self.variants[enemy][x][k] for k in sorted(self.variants[enemy][x])}

        for enemy in self.variants:
            # if "Ornstein" not in enemy:
            #     continue
            # if "Guardian Dragon" in enemy:
            #     skip = False
            # if skip:
            #     continue
            print(enemy)
            for x in range(1, 5):
                for diff in self.variants[enemy][x]:
                    for defKey in self.variants[enemy][x][diff]:
                        for behavior in self.variants[enemy][x][diff][defKey]:
                            # if behavior in {"Feral Onslaught", "Savage Retreat"}:
                            #     continue
                            for variant in self.variants[enemy][x][diff][defKey][behavior]:
                                self.load_variant(enemy, behavior, defKey, variant)

        for encounter in encounters:
            # if encounter != "Deathly Freeze":
            #     continue
            # if encounter == "Pitch Black":
            #     skip = False
            # if skip:
            #     continue
            for charCnt in range(1, 5):
                self.load_encounter(charCnt, encounter)
                for _ in range(100):
                    self.shuffle_enemies()


    def shuffle_enemies(self):
        self.rewardTreasure = None

        oldEnemies = [e for e in self.newEnemies]
        self.newEnemies = choice(self.selected["alternatives"])
        if len(set([tuple(a) for a in self.selected["alternatives"]])) > 1:
            while self.newEnemies == oldEnemies:
                self.newEnemies = choice(self.selected["alternatives"])

        self.edit_encounter_card(self.selected["name"], self.selected["expansion"], self.selected["level"], self.selected["enemySlots"])


    def load_encounter(self, charCnt, encounter=None):
        """
        Loads an encounter from file data for display.

        Optional Parameters:
            event: tkinter.Event
                The tkinter Event that is the trigger.
                Default: None

            encounter: String
                The name of the encounter.
                Default: None
        """
        encounterName = encounter
            
        self.numberOfCharacters = charCnt
        self.selected = encounters[encounterName]
        self.selected["difficultyMod"] = {}
        self.selected["restrictRanged"] = {}

        # Get the possible alternative enemies from the encounter's file.
        with open(baseFolder + "\\lib\\dsbg_shuffle_encounters\\" + encounterName + str(self.numberOfCharacters) + ".json") as alternativesFile:
            alts = load(alternativesFile)

        self.selected["alternatives"] = []
        self.selected["enemySlots"] = alts["enemySlots"]

        for expansionCombo in alts["alternatives"]:
            self.selected["alternatives"] += alts["alternatives"][expansionCombo]
            
        x = len(self.selected["alternatives"])
        print(encounter + " (" + str(x) + ")")

        self.newTiles = dict()

        gen = type(self.selected["alternatives"]) == types.GeneratorType
        a = []
        for alt in self.selected["alternatives"]:
            self.newEnemies = alt
            self.edit_encounter_card(self.selected["name"], self.selected["expansion"], self.selected["level"], self.selected["enemySlots"])
            if gen and len(a) < 500000:
                a.append(alt)
            if len(a) == 500000:
                break

        if gen:
            self.selected["alternatives"] = a


    def edit_encounter_card(self, name, expansion, level, enemySlots):
        """
        Modify the encounter card image with the new enemies and treasure reward, if applicable.

        Required Parameters:
            name: String
                The name of the encounter.

            expansion: String
                The expansion of the encounter.

            level: Integer
                The level of the encounter.

            enemySlots: List
                The slots on the card in which enemies are found.
        """
        self.newTiles = {
            1: [[], [], [], []],
            2: [[], []],
            3: [[], []]
            }
                
        # Determine where enemies should be placed determined by whether this is an old or new style encounter,
        # the level of the encounter, and where on the original encounter card enemies were found.
        s = 0
        for slotNum, slot in enumerate(enemySlots):
            # These are the slot numbers for spawns. Skip over these enemies.
            if slotNum in {4, 7, 10}:
                s += slot
                continue
            for e in range(slot):
                self.newTiles[1 if slotNum < 4 else 2 if slotNum < 7 else 3][slotNum - (0 if slotNum < 4 else 5 if slotNum < 7 else 8)].append(enemyIds[self.newEnemies[s]].name)
                if level == 4:
                    x = 116 + (43 * e) - (3 if "Phantoms" in enemyIds[self.newEnemies[s]].expansions else 0)
                    y = 78 + (47 * slotNum) - ((1 * (4 - slotNum)) if "Phantoms" in enemyIds[self.newEnemies[s]].expansions else 0)
                elif expansion in {"Dark Souls The Board Game", "Iron Keep", "Darkroot", "Explorers", "Executioner Chariot"}:
                    x = 67 + (40 * e)
                    y = 66 + (46 * slotNum)
                else:
                    x = 300 + (29 * e)
                    y = 323 + (29 * (slotNum - (0 if slotNum < 4 else 5 if slotNum < 7 else 8))) + (((1 if slotNum < 4 else 2 if slotNum < 7 else 3) - 1) * 122)

                s += 1

        # These are new encounters that have text referencing specific enemies.
        if name == "Abandoned and Forgotten":
            self.abandoned_and_forgotten()
        elif name == "Aged Sentinel":
            self.aged_sentinel()
        elif (name == "Central Plaza" or name == "Central Plaza (TSC)") and expansion == "The Sunless City":
            self.central_plaza()
        elif name == "Cloak and Feathers":
            self.cloak_and_feathers()
        elif name == "Cold Snap":
            self.cold_snap()
        elif name == "Corvian Host":
            self.corvian_host()
        elif name == "Corrupted Hovel":
            self.corrupted_hovel()
        elif name == "Dark Alleyway":
            self.dark_alleyway()
        elif name == "Deathly Freeze":
            self.deathly_freeze()
        elif name == "Deathly Magic":
            self.deathly_magic()
        elif name == "Deathly Tolls":
            self.deathly_tolls()
        elif name == "Depths of the Cathedral":
            self.depths_of_the_cathedral()
        elif name == "Distant Tower":
            self.distant_tower()
        elif name == "Eye of the Storm":
            self.eye_of_the_storm()
        elif name == "Flooded Fortress":
            self.flooded_fortress()
        elif name == "Frozen Revolutions":
            self.frozen_revolutions()
        elif name == "Giant's Coffin":
            self.giants_coffin()
        elif name == "Gleaming Silver":
            self.gleaming_silver()
        elif name == "Gnashing Beaks":
            self.gnashing_beaks()
        elif name == "Grim Reunion":
            self.grim_reunion()
        elif name == "In Deep Water":
            self.in_deep_water()
        elif name == "Lakeview Refuge":
            self.lakeview_refuge()
        elif name == "Monstrous Maw":
            self.monstrous_maw()
        elif name == "No Safe Haven":
            self.no_safe_haven()
        elif name == "Parish Church":
            self.parish_church()
        elif name == "Parish Gates":
            self.parish_gates()
        elif name == "Pitch Black":
            self.pitch_black()
        elif name == "Puppet Master":
            self.puppet_master()
        elif name == "Shattered Keep":
            self.shattered_keep()
        elif name == "Skeletal Spokes":
            self.skeletal_spokes()
        elif name == "Skeleton Overlord":
            self.skeleton_overlord()
        elif name == "Tempting Maw":
            self.tempting_maw()
        elif name == "The Abandoned Chest":
            self.the_abandoned_chest()
        elif name == "The Beast From the Depths":
            self.the_beast_from_the_depths()
        elif name == "The Bell Tower":
            self.the_bell_tower()
        elif name == "The First Bastion":
            self.the_first_bastion()
        elif name == "The Fountainhead":
            self.the_fountainhead()
        elif name == "The Grand Hall":
            self.the_grand_hall()
        elif name == "The Iron Golem":
            self.the_iron_golem()
        elif name == "The Last Bastion":
            self.the_last_bastion()
        elif name == "The Locked Grave":
            self.the_locked_grave()
        elif name == "The Shine of Gold":
            self.the_shine_of_gold()
        elif name == "The Skeleton Ball":
            self.the_skeleton_ball()
        elif name == "Trecherous Tower":
            self.trecherous_tower()
        elif name == "Trophy Room":
            self.trophy_room()
        elif name == "Twilight Falls":
            self.twilight_falls()
        elif name == "Undead Sanctum":
            self.undead_sanctum()
        elif name == "Velka's Chosen":
            self.velkas_chosen()


    def abandoned_and_forgotten(self):
        spawn1 = enemyIds[self.newEnemies[0]].name
        spawn2 = enemyIds[self.newEnemies[1]].name
        spawn3 = enemyIds[self.newEnemies[2]].name


    def aged_sentinel(self):
        target = self.newTiles[1][1][0]


    def central_plaza(self):
        target = enemyIds[self.newEnemies[4]].name


    def cloak_and_feathers(self):
        target = self.newTiles[1][0][0]


    def cold_snap(self):
        target = self.newTiles[2][0][1]


    def corrupted_hovel(self):
        target = [enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1] if (self.newTiles[1][0] + self.newTiles[1][1]).count(enemy) == 2][0]


    def corvian_host(self):
        target = self.newTiles[1][1][0]


    def dark_alleyway(self):
        target = self.newTiles[1][0][0]


    def deathly_freeze(self):
        deathlyFreezeTile1 = [enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1]]
        deathlyFreezeTile2 = [enemy for enemy in self.newTiles[2][0] + self.newTiles[2][1]]
        overlap = set(deathlyFreezeTile1) & set(deathlyFreezeTile2)
        target = sorted([enemy for enemy in overlap if deathlyFreezeTile1.count(enemy) + deathlyFreezeTile2.count(enemy) == 2], key=lambda x: (-enemiesDict[x].difficultyTiers[self.selected["level"]]["toughness"], enemiesDict[x].difficultyTiers[self.selected["level"]]["difficulty"][self.numberOfCharacters]), reverse=True)[0]


    def deathly_magic(self):
        target = sorted([enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1] if (self.newTiles[1][0] + self.newTiles[1][1]).count(enemy) == 1], key=lambda x: enemiesDict[x].difficultyTiers[self.selected["level"]]["difficulty"][self.numberOfCharacters], reverse=True)[0]


    def deathly_tolls(self):
        target = enemyIds[self.newEnemies[7]].name
        
        gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
        if gang not in ["Alonne", "Hollow", "Silver Knight", "Skeleton"]:
            raise


    def depths_of_the_cathedral(self):
        gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
        if gang not in ["Alonne", "Hollow", "Silver Knight", "Skeleton"]:
            raise


    def distant_tower(self):
        target = self.newTiles[3][0][0]


    def eye_of_the_storm(self):
        fourTarget = [enemyIds[enemy].name for enemy in self.newEnemies if self.newEnemies.count(enemy) == 4]
        targets = list(set([enemyIds[enemy].name for enemy in self.newEnemies if self.newEnemies.count(enemy) == 2]))
        target = enemyIds[self.newEnemies[5]].name


    def flooded_fortress(self):
        gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
        if gang not in ["Alonne", "Hollow", "Silver Knight", "Skeleton"]:
            raise


    def frozen_revolutions(self):
        target = self.newTiles[3][0][0]


    def giants_coffin(self):
        target = enemyIds[self.newEnemies[4]].name
        target = enemyIds[self.newEnemies[5]].name


    def gleaming_silver(self):
        targets = [enemyIds[enemy].name for enemy in list(set(sorted(self.newEnemies, key=lambda x: enemyIds[x].difficultyTiers[self.selected["level"]]["difficulty"][self.numberOfCharacters])[1:-1]))]
        target = enemyIds[self.newEnemies[5]].name


    def gnashing_beaks(self):
        target = enemyIds[self.newEnemies[2]].name
        target = enemyIds[self.newEnemies[3]].name
        target = enemyIds[self.newEnemies[4]].name


    def grim_reunion(self):
        target = enemyIds[self.newEnemies[10]].name


    def in_deep_water(self):
        target = enemyIds[self.newEnemies[4]].name
        target = enemyIds[self.newEnemies[5]].name


    def lakeview_refuge(self):
        target = enemyIds[self.newEnemies[-(self.numberOfCharacters + 1)]].name
        for i, enemy in enumerate(self.newEnemies[-self.numberOfCharacters:]):
            target = enemyIds[enemy].name


    def monstrous_maw(self):
        target = self.newTiles[1][1][0]


    def no_safe_haven(self):
        target = self.newTiles[2][0][0]


    def parish_church(self):
        target = enemyIds[self.newEnemies[10]].name


    def parish_gates(self):
        target = enemyIds[self.newEnemies[3]].name
        target = enemyIds[self.newEnemies[4]].name


    def pitch_black(self):
        tile1Enemies = self.newTiles[1][0] + self.newTiles[1][1]
        tile2Enemies = self.newTiles[2][0] + self.newTiles[2][1]
        target = sorted([enemy for enemy in tile1Enemies if tile1Enemies.count(enemy) == 1], key=lambda x: enemiesDict[x].difficultyTiers[self.selected["level"]]["difficulty"][self.numberOfCharacters], reverse=True)[0]
        target = sorted([enemy for enemy in tile2Enemies if tile2Enemies.count(enemy) == 1], key=lambda x: enemiesDict[x].difficultyTiers[self.selected["level"]]["difficulty"][self.numberOfCharacters], reverse=True)[0]


    def puppet_master(self):
        target = self.newTiles[1][0][1]
        target = self.newTiles[1][0][0]


    def shattered_keep(self):
        targets = set([self.newTiles[1][0][1], self.newTiles[1][1][0], self.newTiles[1][1][1]])


    def skeletal_spokes(self):
        target = self.newTiles[2][0][0]


    def skeleton_overlord(self):
        target = enemyIds[self.newEnemies[1]].name
        target = enemyIds[self.newEnemies[2]].name
        target = self.newTiles[1][0][0]


    def tempting_maw(self):
        target = enemyIds[self.newEnemies[4]].name


    def the_abandoned_chest(self):
        target = enemyIds[self.newEnemies[4]].name
        target = enemyIds[self.newEnemies[5]].name


    def the_beast_from_the_depths(self):
        target = self.newTiles[1][0][0]


    def the_bell_tower(self):
        target = enemyIds[self.newEnemies[2]].name
        target = enemyIds[self.newEnemies[3]].name


    def the_first_bastion(self):
        targets = sorted([enemyIds[enemy].name for enemy in self.newEnemies[-3:]], key=lambda x: (-enemiesDict[x].difficultyTiers[self.selected["level"]]["toughness"], enemiesDict[x].difficultyTiers[self.selected["level"]]["difficulty"][self.numberOfCharacters]))


    def the_fountainhead(self):
        gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
        if gang not in ["Alonne", "Hollow", "Silver Knight", "Skeleton"]:
            raise


    def the_grand_hall(self):
        target = enemyIds[self.newEnemies[7]].name


    def the_iron_golem(self):
        target = self.newTiles[1][1][0]


    def the_last_bastion(self):
        target = sorted([enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1]], key=lambda x: enemiesDict[x].difficultyTiers[self.selected["level"]]["difficulty"][self.numberOfCharacters])[0]


    def the_locked_grave(self):
        target = enemyIds[self.newEnemies[7]].name


    def the_shine_of_gold(self):
        target = self.newTiles[1][1][0]
        target = self.newTiles[1][0][0]


    def the_skeleton_ball(self):
        target = self.newTiles[1][0][0]
        target = self.newTiles[3][1][0]


    def trecherous_tower(self):
        spawn1 = enemyIds[self.newEnemies[2]].name
        spawn2 = enemyIds[self.newEnemies[3]].name
        spawn3 = enemyIds[self.newEnemies[4]].name


    def trophy_room(self):
        target = set([self.newTiles[2][0][0], self.newTiles[2][1][0]])


    def twilight_falls(self):
        gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
        if gang not in ["Alonne", "Hollow", "Silver Knight", "Skeleton"]:
            raise


    def undead_sanctum(self):
        gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
        if gang not in ["Alonne", "Hollow", "Silver Knight", "Skeleton"]:
            raise


    def velkas_chosen(self):
        target = sorted([enemy for enemy in self.newTiles[2][0] + self.newTiles[2][1]], key=lambda x: enemiesDict[x].difficultyTiers[self.selected["level"]]["difficulty"][self.numberOfCharacters], reverse=True)[0]


    def load_variant(self, enemy, behavior, defKey, variant):
        self.currentVariants[enemy] = {"defKey": defKey, behavior: [variant]}
        self.load_variant_card(enemy, behavior, variant)
    
    
    def load_variant_card(self, enemy, behavior, variant):
        if "Ornstein & Smough" in enemy:
            self.edit_variant_card_os(enemy, behavior, variant)
        else:
            self.edit_variant_card(enemy, behavior, variant)


    def edit_variant_card(self, enemy, behavior, variant):
        self.edit_variant_card_data(enemy, variant)
        self.edit_variant_card_behavior(enemy, behavior, variant)


    def edit_variant_card_os(self, enemy, behavior, variant):
        self.edit_variant_card_data_os(enemy, variant)
        self.edit_variant_card_behavior_os(enemy, behavior, variant)


    def edit_variant_card_data(self, enemy, variant):
        healthAddition = 0
        health = behaviorDetail[enemy]["health"]
        armor = behaviorDetail[enemy]["armor"]
        resist = behaviorDetail[enemy]["resist"]
        heatup = []
        if "heatup1" in behaviorDetail[enemy]:
            heatup.append(behaviorDetail[enemy]["heatup1"])
            heatup.append(behaviorDetail[enemy]["heatup2"])
        elif "heatup" in behaviorDetail[enemy]:
            heatup.append(behaviorDetail[enemy]["heatup"])

        mods = [modIdLookup[m] for m in variant if m]
        for mod in mods:
            healthAddition = int(mod[-1]) if "health" in mod else 0
            health += healthAddition
            armor += int(mod[-1]) if "armor" in mod else 0
            resist += int(mod[-1]) if "resist" in mod else 0
            if healthAddition:
                heatup = [h + healthAddition for h in heatup]

        if health - behaviorDetail[enemy]["health"] != max([0] + [int(mod[-1]) if "health" in mod else 0 for mod in mods]):
            raise
        if behaviorDetail[enemy]["armor"] + max([0] + [int(mod[-1]) if "armor" in mod else 0 for mod in mods]) != armor:
            raise
        if behaviorDetail[enemy]["resist"] + max([0] + [int(mod[-1]) if "resist" in mod else 0 for mod in mods]) != resist:
            raise


    def edit_variant_card_data_os(self, enemy, variant):
        healthAddition = 0
        healthO = behaviorDetail["Ornstein & Smough"]["Ornstein"]["health"]
        armorO = behaviorDetail["Ornstein & Smough"]["Ornstein"]["armor"]
        resistO = behaviorDetail["Ornstein & Smough"]["Ornstein"]["resist"]
        healthS = behaviorDetail["Ornstein & Smough"]["Smough"]["health"]
        armorS = behaviorDetail["Ornstein & Smough"]["Smough"]["armor"]
        resistS = behaviorDetail["Ornstein & Smough"]["Smough"]["resist"]

        mods = [modIdLookup[m] for m in variant if m]
        for mod in mods:
            healthAddition = int(mod[-1]) if "health" in mod else 0
            healthO += healthAddition
            armorO += int(mod[-1]) if "armor" in mod else 0
            resistO += int(mod[-1]) if "resist" in mod else 0
            healthS += healthAddition
            armorS += int(mod[-1]) if "armor" in mod else 0
            resistS += int(mod[-1]) if "resist" in mod else 0

        if healthO - behaviorDetail[enemy]["Ornstein"]["health"] != max([0] + [int(mod[-1]) if "health" in mod else 0 for mod in mods]):
            raise
        if behaviorDetail[enemy]["Ornstein"]["armor"] + max([0] + [int(mod[-1]) if "armor" in mod else 0 for mod in mods]) != armorO:
            raise
        if behaviorDetail[enemy]["Ornstein"]["resist"] + max([0] + [int(mod[-1]) if "resist" in mod else 0 for mod in mods]) != resistO:
            raise
        if healthS - behaviorDetail[enemy]["Smough"]["health"] != max([0] + [int(mod[-1]) if "health" in mod else 0 for mod in mods]):
            raise
        if behaviorDetail[enemy]["Smough"]["armor"] + max([0] + [int(mod[-1]) if "armor" in mod else 0 for mod in mods]) != armorS:
            raise
        if behaviorDetail[enemy]["Smough"]["resist"] + max([0] + [int(mod[-1]) if "resist" in mod else 0 for mod in mods]) != resistS:
            raise


    def edit_variant_card_behavior(self, enemy, behavior, variant):
        mods = [modIdLookup[m] for m in variant if m]
        if behavior == "":
            behavior = "behavior"

        dodge = behaviorDetail[enemy][behavior]["dodge"]
        repeat = behaviorDetail[enemy][behavior].get("repeat", 1)
        actions = {}
        for position in ["left", "middle", "right"]:
            if position in behaviorDetail[enemy][behavior]:
                if "effect" in behaviorDetail[enemy][behavior][position]:
                    actions[position] = {"effect": []}
                    actions[position]["effect"] = [e for e in behaviorDetail[enemy][behavior][position]["effect"]]
                else:
                    actions[position] = behaviorDetail[enemy][behavior][position].copy()

        dodge, repeat, actions = self.apply_mods_to_actions(enemy, behavior, dodge, repeat, actions, variant)

        if (
            behaviorDetail[enemy][behavior]["dodge"] + max([0] + [int(mod[-1]) if "dodge" in mod else 0 for mod in mods]) != dodge
            or behaviorDetail[enemy][behavior].get("repeat", 1) + max([0] + [1 if "repeat" in mod else 0 for mod in mods]) != repeat
        ):
            raise
        if {"bleed", "frostbite", "poison", "stagger"} & set(mods) and not any(["effect" in actions[position] for position in actions]):
            raise
        if "bleed" in mods and not any(["bleed" in actions[position]["effect"] for position in actions if "effect" in actions[position]]):
            raise
        if "frostbite" in mods and not any(["frostbite" in actions[position]["effect"] for position in actions if "effect" in actions[position]]):
            raise
        if "poison" in mods and not any(["poison" in actions[position]["effect"] for position in actions if "effect" in actions[position]]):
            raise
        if "stagger" in mods and not any(["stagger" in actions[position]["effect"] for position in actions if "effect" in actions[position]]):
            raise
        if any([len(actions[position]["effect"]) > 2 for position in actions if "effect" in actions[position]]):
            raise
        for position in ["left", "middle", "right"]:
            if position in actions:
                if (
                    "type" in actions[position]
                    and actions[position]["type"] != "push"
                    and set(mods) & {"physical", "magic"}
                    and actions[position]["type"] != list(set(mods) & {"physical", "magic"})[0]
                    ):
                    raise
                if (
                    "damage" in actions[position]
                    and "damage" in set([mod[:-1] for mod in mods])
                    and behaviorDetail[enemy][behavior][position]["damage"] + max([0] + [int(mod[-1]) if "damage" in mod else 0 for mod in mods]) != actions[position]["damage"]
                    ):
                    raise


    def edit_variant_card_behavior_os(self, enemy, behavior, variant):
        behaviorOs = osBehaviorLookup[behavior]

        mods = [modIdLookup[m] for m in variant if m]
    
        if "&" in behaviorOs:
            dodge = behaviorDetail[enemy][behaviorOs][behavior]["dodge"]
            repeat = behaviorDetail[enemy][behaviorOs][behavior].get("repeat", 1)
        else:
            dodge = behaviorDetail[enemy][behaviorOs]["dodge"]
            repeat = behaviorDetail[enemy][behaviorOs].get("repeat", 1)
        actions = {}
        for position in ["left", "right"]:
            if "&" in behaviorOs:
                if position in behaviorDetail[enemy][behaviorOs][behavior]:
                    actions[position] = behaviorDetail[enemy][behaviorOs][behavior][position].copy()
            else:
                if position in behaviorDetail[enemy][behaviorOs]:
                    actions[position] = behaviorDetail[enemy][behaviorOs][position].copy()

        dodge, repeat, actions = self.apply_mods_to_actions_os(enemy, behaviorOs, behavior, dodge, repeat, actions, variant)

        if "&" in behaviorOs:
            if (
                behaviorDetail[enemy][behaviorOs][behavior]["dodge"] + max([0] + [int(mod[-1]) if "dodge" in mod else 0 for mod in mods]) != dodge
                or behaviorDetail[enemy][behaviorOs][behavior].get("repeat", 1) + max([0] + [1 if "repeat" in mod else 0 for mod in mods]) != repeat
            ):
                raise
        else:
            if (
                behaviorDetail[enemy][behaviorOs]["dodge"] + max([0] + [int(mod[-1]) if "dodge" in mod else 0 for mod in mods]) != dodge
                or behaviorDetail[enemy][behaviorOs].get("repeat", 1) + max([0] + [1 if "repeat" in mod else 0 for mod in mods]) != repeat
            ):
                raise
        if {"bleed", "frostbite", "poison", "stagger"} & set(mods) and not any(["effect" in actions[position] for position in actions]):
            raise
        if "bleed" in mods and not any(["bleed" in actions[position]["effect"] for position in actions if "effect" in actions[position]]):
            raise
        if "frostbite" in mods and not any(["frostbite" in actions[position]["effect"] for position in actions if "effect" in actions[position]]):
            raise
        if "poison" in mods and not any(["poison" in actions[position]["effect"] for position in actions if "effect" in actions[position]]):
            raise
        if "stagger" in mods and not any(["stagger" in actions[position]["effect"] for position in actions if "effect" in actions[position]]):
            raise
        if any([len(actions[position]["effect"]) > 2 for position in actions if "effect" in actions[position]]):
            raise
        for position in ["left", "middle", "right"]:
            if position in actions:
                if (
                    "type" in actions[position]
                    and actions[position]["type"] != "push"
                    and set(mods) & {"physical", "magic"}
                    and actions[position]["type"] != list(set(mods) & {"physical", "magic"})[0]
                    ):
                    raise
                if "&" in behaviorOs:
                    if (
                        "damage" in actions[position]
                        and "damage" in set([mod[:-1] for mod in mods])
                        and behaviorDetail[enemy][behaviorOs][behavior][position]["damage"] + max([0] + [int(mod[-1]) if "damage" in mod else 0 for mod in mods]) != actions[position]["damage"]
                        ):
                        raise
                else:
                    if (
                        "damage" in actions[position]
                        and "damage" in set([mod[:-1] for mod in mods])
                        and behaviorDetail[enemy][behavior][position]["damage"] + max([0] + [int(mod[-1]) if "damage" in mod else 0 for mod in mods]) != actions[position]["damage"]
                        ):
                        raise


    def apply_mods_to_actions(self, enemy, behavior, dodge, repeat, actions, variant=None):
        behavior = "" if behavior == "behavior" else behavior

        mods = [modIdLookup[m] for m in variant if m]

        for mod in mods:
            dodge += int(mod[-1]) if "dodge" in mod else 0
            repeat += 1 if "repeat" in mod else 0
            newConditionAdded = False

            # For behaviors that do not already cause a condition.
            if (
                mod in {"bleed", "frostbite", "poison", "stagger"}
                and "effect" not in actions.get("middle", {})
                and "effect" not in actions.get("right", {})
                ):
                for position in ["middle", "right"]:
                    if position in actions and not actions[position]:
                        actions[position]["effect"] = [mod]
                        newConditionAdded = True
                        break

            if newConditionAdded:
                continue

            repeatAdded = False if behavior == "" else True
            if any(["repeat" in actions[position] for position in actions]):
                repeatAdded = True

            for position in ["left", "middle", "right"]:
                if position in actions:
                    if "damage" in actions[position]:
                        actions[position]["damage"] += int(mod[-1]) if "damage" in mod else 0
                        actions[position]["type"] = mod if mod in {"physical", "magic"} and actions[position]["type"] != "push" else actions[position]["type"]
                    elif "repeat" in actions[position] and "repeat" in mod:
                        actions[position]["repeat"] += 1
                    # For behaviors that already cause a condition.
                    elif "effect" in actions[position] and mod in {"bleed", "frostbite", "poison", "stagger"} and mod not in actions[position]["effect"]:
                        actions[position]["effect"].append(mod)
                    elif actions[position]:
                        continue
                    elif not actions[position] and "repeat" in mod and not repeatAdded:
                        # These enemies have their move shifted if they get a repeat.
                        if enemy in {"Phalanx", "Phalanx Hollow", "Silver Knight Spearman"} and position == "middle":
                            continue
                        actions[position] = {"repeat": repeat}
                        repeatAdded = True

        return dodge, repeat, actions


    def apply_mods_to_actions_os(self, enemy, behavior, b, dodge, repeat, actions, variant=None):
        mods = [modIdLookup[m] for m in variant if m]

        for mod in mods:
            dodge += int(mod[-1]) if "dodge" in mod else 0
            repeat += 1 if "repeat" in mod else 0
            newConditionAdded = False

            # For behaviors that do not already cause a condition.
            if (
                mod in {"bleed", "frostbite", "poison", "stagger"}
                and "effect" not in actions.get("right", {})
                ):
                if "right" in actions and not actions["right"]:
                    actions["right"]["effect"] = [mod]
                    newConditionAdded = True

            if newConditionAdded:
                continue

            for position in ["left", "right"]:
                if position in actions:
                    if "damage" in actions[position]:
                        actions[position]["damage"] += int(mod[-1]) if "damage" in mod else 0
                    if "type" in actions[position]:
                        actions[position]["type"] = mod if mod in {"physical", "magic"} else actions[position]["type"]
                    # For behaviors that already cause a condition.
                    elif "effect" in actions[position] and mod in {"bleed", "frostbite", "poison", "stagger"} and mod not in actions[position]["effect"]:
                        actions[position]["effect"].append(mod)

        return dodge, repeat, actions



a = Tester()