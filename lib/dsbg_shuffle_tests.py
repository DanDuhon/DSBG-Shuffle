from os import path
from json import load
from itertools import product
from collections import Counter
from random import choice
import types
import platform

from dsbg_enemies import enemyIds, enemiesDict

if platform.system() == "Windows":
    pathSep = "\\"
else:
    pathSep = "/"

baseFolder = path.dirname(__file__).replace("\\lib".replace("\\", pathSep), "")

with open(baseFolder + "\\lib\\dsbg_shuffle_enemies.json".replace("\\", pathSep)) as enemiesFile:
    enemies = load(enemiesFile)

with open(baseFolder + "\\lib\\dsbg_shuffle_invaders_standard.json".replace("\\", pathSep)) as invadersStandardFile:
    invadersStandard = load(invadersStandardFile)

with open(baseFolder + "\\lib\\dsbg_shuffle_invaders_advanced.json".replace("\\", pathSep)) as invadersAdvancedFile:
    invadersAdvanced = load(invadersAdvancedFile)

with open(baseFolder + "\\lib\\dsbg_shuffle_encounters.json".replace("\\", pathSep)) as encountersFile:
    encounters = load(encountersFile)


class Tester():
    def __init__(self):
        self.allEnemies = enemies | invadersStandard | invadersAdvanced
        self.selected = None
        self.newEnemies = []
        self.newTiles = dict()

        for encounter in encounters:
            self.load_encounter(encounter)
            for _ in range(100):
                self.shuffle_enemies()


    def shuffle_enemies(self):
        self.rewardTreasure = None

        oldEnemies = [e for e in self.newEnemies]
        if "1" in self.selected["alternatives"]:
            self.newEnemies = (
                choice(self.selected["alternatives"]["1"])
                + (choice(self.selected["alternatives"]["2"]) if "2" in self.selected["alternatives"] else [])
                + (choice(self.selected["alternatives"]["3"]) if "3" in self.selected["alternatives"] else []))
        else:
            self.newEnemies = choice(self.selected["alternatives"])
        if len(set([tuple(a) for a in self.selected["alternatives"]])) > 1:
            while self.newEnemies == oldEnemies:
                if "1" in self.selected["alternatives"]:
                    self.newEnemies = (
                        choice(self.selected["alternatives"]["1"])
                        + (choice(self.selected["alternatives"]["2"]) if "2" in self.selected["alternatives"] else [])
                        + (choice(self.selected["alternatives"]["3"]) if "3" in self.selected["alternatives"] else []))
                else:
                    self.newEnemies = choice(self.selected["alternatives"])

        self.edit_encounter_card(self.selected["name"], self.selected["expansion"], self.selected["level"], self.selected["enemySlots"])


    def load_encounter(self, encounter=None):
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
            
        self.selected = encounters[encounterName]
        self.selected["difficultyMod"] = {}
        self.selected["restrictRanged"] = {}

        # Get the possible alternative enemies from the encounter's file.
        with open(baseFolder + "\\lib\\dsbg_shuffle_encounters\\" + encounterName + ".json") as alternativesFile:
            alts = load(alternativesFile)

        self.selected["alternatives"] = []
        self.selected["enemySlots"] = alts["enemySlots"]

        if "3" in alts["alternatives"]:
            toCombine1 = []
            toCombine2 = []
            toCombine3 = []
            for expansionCombo in alts["alternatives"]["1"]:
                toCombine1 += alts["alternatives"]["1"][expansionCombo]
            for expansionCombo in alts["alternatives"]["2"]:
                toCombine2 += alts["alternatives"]["2"][expansionCombo]
            for expansionCombo in alts["alternatives"]["3"]:
                toCombine3 += alts["alternatives"]["3"][expansionCombo]
            self.selected["alternatives"] = (p[0] + p[1] + p[2] for p in product(toCombine1, toCombine2, toCombine3))
            print(encounter + " (" + str(len(toCombine1) * len(toCombine2) * len(toCombine3)) + ")")
        elif "2" in alts["alternatives"]:
            toCombine1 = []
            toCombine2 = []
            for expansionCombo in alts["alternatives"]["1"]:
                toCombine1 += alts["alternatives"]["1"][expansionCombo]
            for expansionCombo in alts["alternatives"]["2"]:
                toCombine2 += alts["alternatives"]["2"][expansionCombo]
            self.selected["alternatives"] = (p[0] + p[1] for p in product(toCombine1, toCombine2))
            print(encounter + " (" + str(len(toCombine1) * len(toCombine2)) + ")")
        else:
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
            if gen and len(a) < 5000000:
                a.append(alt)

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
            for e in range(slot):
                self.newTiles[1 if slotNum < 4 else 2 if slotNum < 6 else 3][slotNum - (0 if slotNum < 4 else 4 if slotNum < 6 else 6)].append(enemyIds[self.newEnemies[s]].name)
                if level == 4:
                    x = 116 + (43 * e) - (3 if enemyIds[self.newEnemies[s]].name == "Advanced Invader" else 0)
                    y = 78 + (47 * slotNum)
                elif expansion in {"Dark Souls The Board Game", "Iron Keep", "Darkroot", "Explorers", "Executioner Chariot"}:
                    x = 67 + (40 * e)
                    y = 66 + (46 * slotNum)
                else:
                    x = 300 + (29 * e)
                    y = 323 + (29 * (slotNum - (0 if slotNum < 4 else 4 if slotNum < 6 else 6))) + (((1 if slotNum < 4 else 2 if slotNum < 6 else 3) - 1) * 122)

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
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name


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
        deathlyFreezeTile1 = [enemy.replace(" (TSC)", "") for enemy in self.newTiles[1][0] + self.newTiles[1][1]]
        deathlyFreezeTile2 = [enemy.replace(" (TSC)", "") for enemy in self.newTiles[2][0] + self.newTiles[2][1]]
        overlap = set(deathlyFreezeTile1) & set(deathlyFreezeTile2)
        target = sorted([enemy for enemy in overlap if deathlyFreezeTile1.count(enemy) + deathlyFreezeTile2.count(enemy) > 1], key=lambda x: enemiesDict[x].difficulty, reverse=True)[0]


    def deathly_magic(self):
        target = sorted([enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1] if (self.newTiles[1][0] + self.newTiles[1][1]).count(enemy) == 1], key=lambda x: enemiesDict[x].difficulty, reverse=True)[0]


    def deathly_tolls(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name
        
        gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
        if gang not in ["Alonne", "Hollow", "Scarecrow", "Skeleton"]:
            raise


    def depths_of_the_cathedral(self):
        gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
        if gang not in ["Alonne", "Hollow", "Scarecrow", "Skeleton"]:
            raise


    def distant_tower(self):
        target = self.newTiles[3][0][0]


    def eye_of_the_storm(self):
        fourTarget = [enemyIds[enemy].name for enemy in self.newEnemies if self.newEnemies.count(enemy) == 4]
        targets = list(set([enemyIds[enemy].name for enemy in self.newEnemies if self.newEnemies.count(enemy) == 2]))
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name


    def flooded_fortress(self):
        gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
        if gang not in ["Alonne", "Hollow", "Scarecrow", "Skeleton"]:
            raise


    def frozen_revolutions(self):
        target = self.newTiles[3][0][0]


    def giants_coffin(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])+1]].name


    def gleaming_silver(self):
        targets = list(set([enemyIds[enemy].name for enemy in self.newEnemies if self.newEnemies.count(enemy) == 2]))
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name


    def gnashing_beaks(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])+1]].name


    def grim_reunion(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name


    def in_deep_water(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name


    def lakeview_refuge(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])+1]].name


    def monstrous_maw(self):
        target = self.newTiles[1][1][0]


    def no_safe_haven(self):
        target = self.newTiles[2][0][0]


    def parish_church(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name


    def parish_gates(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name


    def pitch_black(self):
        tile1Enemies = self.newTiles[1][0] + self.newTiles[1][1]
        tile2Enemies = self.newTiles[2][0] + self.newTiles[2][1]
        target = sorted([enemy for enemy in tile1Enemies if tile1Enemies.count(enemy) == 1], key=lambda x: enemiesDict[x].difficulty, reverse=True)[0]
        target = sorted([enemy for enemy in tile2Enemies if tile2Enemies.count(enemy) == 1], key=lambda x: enemiesDict[x].difficulty, reverse=True)[0]


    def puppet_master(self):
        target = self.newTiles[1][0][1]
        target = self.newTiles[1][0][0]


    def shattered_keep(self):
        target = self.newTiles[1][1][0]


    def skeletal_spokes(self):
        target = self.newTiles[2][0][0]


    def skeleton_overlord(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name
        target = self.newTiles[1][0][0]


    def tempting_maw(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name


    def the_abandoned_chest(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])+1]].name


    def the_beast_from_the_depths(self):
        target = self.newTiles[1][0][0]


    def the_bell_tower(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name


    def the_first_bastion(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])+1]].name
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])+2]].name


    def the_fountainhead(self):
        gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
        if gang not in ["Alonne", "Hollow", "Scarecrow", "Skeleton"]:
            raise


    def the_grand_hall(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name


    def the_iron_golem(self):
        target = self.newTiles[1][1][0]


    def the_last_bastion(self):
        target = sorted([enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1]], key=lambda x: enemiesDict[x].difficulty)[0]


    def the_locked_grave(self):
        target = enemyIds[self.newEnemies[sum(self.selected["enemySlots"])]].name


    def the_shine_of_gold(self):
        target = self.newTiles[1][1][0]


    def the_skeleton_ball(self):
        target = self.newTiles[1][0][0]
        target = self.newTiles[3][1][0]


    def trecherous_tower(self):
        spawn1 = enemyIds[self.newEnemies[2]].name
        spawn2 = enemyIds[self.newEnemies[3]].name
        spawn3 = enemyIds[self.newEnemies[4]].name


    def trophy_room(self):
        target = self.newTiles[2][0][0]


    def twilight_falls(self):
        gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
        if gang not in ["Alonne", "Hollow", "Scarecrow", "Skeleton"]:
            raise


    def undead_sanctum(self):
        gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
        if gang not in ["Alonne", "Hollow", "Scarecrow", "Skeleton"]:
            raise


    def velkas_chosen(self):
        target = sorted([enemy for enemy in self.newTiles[2][0] + self.newTiles[2][1]], key=lambda x: enemiesDict[x].difficulty, reverse=True)[0]



a = Tester()