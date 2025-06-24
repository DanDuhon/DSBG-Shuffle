try:
    import datetime
    import errno
    import os
    import requests
    import sys
    import tkinter as tk
    import webbrowser
    from json import load
    from PIL import Image, ImageTk, UnidentifiedImageError
    from tkinter import ttk

    from dsbg_shuffle_behavior_decks import BehaviorDeckFrame
    from dsbg_shuffle_campaign import CampaignFrame
    from dsbg_shuffle_encounters import EncountersFrame
    from dsbg_shuffle_encounter_builder import EncounterBuilderFrame
    from dsbg_shuffle_enemies import enemyIds, enemiesDict, bosses
    from dsbg_shuffle_events import EventsFrame
    from dsbg_shuffle_settings import SettingsWindow
    from dsbg_shuffle_tooltip_reference import tooltipText
    from dsbg_shuffle_treasure import generate_treasure_soul_cost, populate_treasure_tiers, treasures
    from dsbg_shuffle_utility import CreateToolTip, PopupWindow, center, do_nothing, enable_binding, error_popup, log, set_display_bindings_by_tab, baseFolder, pathSep
    from dsbg_shuffle_variants import VariantsFrame


    class Application(ttk.Frame):
        def __init__(self, parent):
            try:
                log("Initiating application")

                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep)) as settingsFile:
                    self.settings = load(settingsFile)

                with open(baseFolder + "\\lib\\dsbg_shuffle_encounters.json".replace("\\", pathSep)) as encountersFile:
                    self.encounters = load(encountersFile)

                self.add_custom_encounters()

                self.selected = None
                self.forPrinting = False
                self.tooltips = []
                self.coreSets = {"Dark Souls The Board Game", "Painted World of Ariamis", "Tomb of Giants", "The Sunless City"}
                self.allExpansions = set([self.encounters[encounter]["expansion"] for encounter in self.encounters]) | set(["Phantoms"])
                self.level4Expansions = set([self.encounters[encounter]["expansion"] for encounter in self.encounters if self.encounters[encounter]["level"] == 4])
                self.availableExpansions = set(self.settings["availableExpansions"])
                self.v1Expansions = {"Dark Souls The Board Game", "Darkroot", "Executioner Chariot", "Explorers", "Iron Keep"}
                self.v2Expansions = (self.allExpansions - self.v1Expansions - self.level4Expansions)
                self.enabledEnemies = set([enemiesDict[enemy.replace(" (V1)", "")].id for enemy in self.settings["enabledEnemies"] if enemy not in self.allExpansions])
                self.charactersActive = set(self.settings["charactersActive"])
                self.numberOfCharacters = len(self.charactersActive)
                self.availableCoreSets = self.coreSets & self.availableExpansions

                self.allEnemies = {enemy: {} for enemy in enemiesDict}

                root.withdraw()

                progressMax = 1052
                # Variants
                if self.settings["variantEnable"] == "on":
                    progressMax += len(list(enemiesDict.keys()) + list(bosses.keys())) * 12
                if self.settings["treasureSwapOption"] in {"Similar Soul Cost", "Tier Based"}:
                    progressMax += len([t for t in treasures if not treasures[t]["character"] or treasures[t]["character"] in self.charactersActive])
                self.progress = PopupWindow(root, labelText="Starting up...", progressBar=True, progressMax=progressMax, loadingImage=True)

                # Delete images from staging
                folder = baseFolder + "\\lib\\dsbg_shuffle_image_staging".replace("\\", pathSep)
                for filename in os.listdir(folder):
                    filePath = os.path.join(folder, filename)

                    if os.path.isfile(filePath) and filePath[-4:] == ".png":
                        os.unlink(filePath)

                ttk.Frame.__init__(self)
                self.grid_rowconfigure(index=1, weight=1)
                self.grid_rowconfigure(index=2, weight=0)
                self.displayScrollbar = ttk.Scrollbar(root)
                self.displayScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                self.bind("<1>", lambda event: event.widget.focus_set())

                # Create images
                self.progress.label.config(text = "Loading images... ")
                # Enemies
                for enemy in self.allEnemies:
                    self.allEnemies[enemy]["imageOld"] = self.create_image(enemy + ".png", "enemyOld", progress=True)
                    self.allEnemies[enemy]["imageOldLevel4"] = self.create_image(enemy + ".png", "enemyOldLevel4", progress=True)
                    self.allEnemies[enemy]["imageNew"] = self.create_image(enemy + ".png", "enemyNew", progress=True)
                    self.allEnemies[enemy]["image text"] = self.create_image(enemy + ".png", "enemyText", progress=True)
                    self.allEnemies[enemy]["image text" if self.forPrinting else "photo image text"] = ImageTk.PhotoImage(self.create_image(enemy + ".png", "enemyText", progress=True))

                # Icons
                self.enemyNode2 = self.create_image("enemy_node_2.png", "enemyNode", progress=True)
                self.attack = {
                    "physical": {},
                    "magic": {},
                    "push": {}
                }
                for x in range(2, 14):
                    for y in ["physical", "magic", "push"]:
                        self.attack[y][x] = self.create_image("attack_" + y + "_" + str(x) + ".png", y if y == "push" else "attack", progress=True)
                self.bleed = self.create_image("bleed.png", "bleed", progress=True)
                self.frostbite = self.create_image("frostbite.png", "frostbite", progress=True)
                self.poison = self.create_image("poison.png", "poison", progress=True)
                self.stagger = self.create_image("stagger.png", "stagger", progress=True)
                self.corrosion = self.create_image("corrosion.png", "corrosion", progress=True)
                self.calamity = self.create_image("calamity.png", "calamity", progress=True)
                self.repeat = {}
                for x in range(2, 6):
                    self.repeat[x] = self.create_image("repeat_" + str(x) + ".png", "repeat", progress=True)
                self.sksMove = self.create_image("sks_move.png", "move", progress=True)
                self.phalanxMove = self.create_image("phalanx_move.png", "move", progress=True)
                self.aoeNode = self.create_image("aoe_node.png", "aoeNode", progress=True)
                self.destinationNode = self.create_image("destination_node.png", "destinationNode", progress=True)

                # Keywords
                self.barrage = self.create_image("barrage.png", "barrage", progress=True)
                self.bitterCold = self.create_image("bitter_cold.png", "bitterCold", progress=True)
                self.darkness = self.create_image("darkness.png", "darkness", progress=True)
                self.eerie = self.create_image("eerie.png", "eerie", progress=True)
                self.gangAlonne = self.create_image("gang_alonne.png", "gangAlonne", progress=True)
                self.gangHollow = self.create_image("gang_hollow.png", "gangHollow", progress=True)
                self.gangSilverKnight = self.create_image("gang_silver_knight.png", "gangSilverKnight", progress=True)
                self.gangSkeleton = self.create_image("gang_skeleton.png", "gangSkeleton", progress=True)
                self.gangAlonnePhoto = ImageTk.PhotoImage(self.gangAlonne)
                self.gangHollowPhoto = ImageTk.PhotoImage(self.gangHollow)
                self.gangSilverKnightPhoto = ImageTk.PhotoImage(self.gangSilverKnight)
                self.gangSkeletonPhoto = ImageTk.PhotoImage(self.gangSkeleton)
                self.hidden = self.create_image("hidden.png", "hidden", progress=True)
                self.illusion = self.create_image("illusion.png", "illusion", progress=True)
                self.mimic = self.create_image("mimic_keyword.png", "mimic", progress=True)
                self.onslaught = self.create_image("onslaught.png", "onslaught", progress=True)
                self.poisonMist = self.create_image("poison_mist.png", "poisonMist", progress=True)
                self.snowstorm = self.create_image("snowstorm.png", "snowstorm", progress=True)
                self.timer = self.create_image("timer.png", "timer", progress=True)
                self.trial = self.create_image("trial.png", "trial", progress=True)

                self.rewardsDrawIcon = self.create_image("custom_encounter_rewards_draw.png", "reward", 99, extensionProvided=True, progress=True)
                self.rewardsRefreshIcon = self.create_image("custom_encounter_rewards_refresh.png", "reward", 99, extensionProvided=True, progress=True)
                self.rewardsSearchIcon = self.create_image("custom_encounter_rewards_search.png", "reward", 99, extensionProvided=True, progress=True)
                self.rewardsShortcutIcon = self.create_image("custom_encounter_rewards_shortcut.png", "reward", 99, extensionProvided=True, progress=True)
                self.rewardsSoulsIcon = self.create_image("custom_encounter_rewards_souls.png", "reward", 99, extensionProvided=True, progress=True)
                self.rewardsSoulsPlayersIcon = self.create_image("custom_encounter_rewards_souls_players.png", "reward", 99, extensionProvided=True, progress=True)
                self.rewardsTrialIcon = self.create_image("custom_encounter_rewards_trial.png", "reward", 99, extensionProvided=True, progress=True)

                self.emptySetIcon = self.create_image("empty_set_icon.png", "levelIcon", 99, extensionProvided=True, progress=True)
                
                _, self.iconBg1PhotoImage = self.create_image("icon_background1.jpg", "iconBg1", 99, extensionProvided=True, progress=True)

                self.levelIcons = {
                    1: self.create_image("custom_encounter_level1_icon.png", "levelIcon", 99, extensionProvided=True, progress=True),
                    2: self.create_image("custom_encounter_level2_icon.png", "levelIcon", 99, extensionProvided=True, progress=True),
                    3: self.create_image("custom_encounter_level3_icon.png", "levelIcon", 99, extensionProvided=True, progress=True),
                    4: self.create_image("custom_encounter_level4_icon.png", "levelIcon", 99, extensionProvided=True, progress=True)
                    }

                startingHorizontal = self.create_image("custom_encounter_starting_nodes_horizontal.png", "nodesHorizontal", 99, extensionProvided=True, progress=True)
                startingVertical = self.create_image("custom_encounter_starting_nodes_vertical.png", "nodesVertical", 99, extensionProvided=True, progress=True)

                self.terrain = {
                    "Barrel": self.create_image("barrel.png", "terrain", 99, extensionProvided=True, progress=True),
                    "Envoy Banner": self.create_image("envoy_banner.png", "terrain", 99, extensionProvided=True, progress=True),
                    "Exit": self.create_image("exit.png", "terrain", 99, extensionProvided=True, progress=True),
                    "Fang Boar": self.create_image("fang_boar.png", "terrain", 99, extensionProvided=True, progress=True),
                    "Gravestone": self.create_image("gravestone.png", "terrain", 99, extensionProvided=True, progress=True),
                    "Lever": self.create_image("lever.png", "terrain", 99, extensionProvided=True, progress=True),
                    "Shrine": self.create_image("shrine.png", "terrain", 99, extensionProvided=True, progress=True),
                    "Torch": self.create_image("torch.png", "terrain", 99, extensionProvided=True, progress=True),
                    "Treasure Chest": self.create_image("treasure_chest.png", "terrain", 99, extensionProvided=True, progress=True)
                }

                self.iconsForCustom = {
                    "Aggro": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Barrel": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Bleed": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Calamity": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Character Count": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Closest": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Corrosion": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Die (Black)": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Die (Blue)": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Die (Orange)": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Dodge": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Enemy Node 1": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Enemy Node 2": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Enemy Node 3": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Enemy Node 4": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Envoy Banner": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Exit": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Fang Boar": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Frostbite": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Gravestone": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Leap": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Lever": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Magic": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Node Attack": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Painted World of Ariamis": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Poison": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Push": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Range": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Repeat": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Shaft": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Shift": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Shrine": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Stagger": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Terrain Node 1": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Terrain Node 2": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Terrain Node 3": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Terrain Node 4": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "The Sunless City": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Tomb of Giants": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Torch": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Treasure Chest": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Alonne Bow Knight": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Alonne Knight Captain": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Alonne Sword Knight": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Black Hollow Mage": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Bonewheel Skeleton": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Crossbow Hollow": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Crow Demon": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Demonic Foliage": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Engorged Zombie": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Falchion Skeleton": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Firebomb Hollow": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Giant Skeleton Archer": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Giant Skeleton Soldier": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Hollow Soldier": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Ironclad Soldier": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Large Hollow Soldier": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Mushroom Child": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Mushroom Parent": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Necromancer": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Phalanx": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Phalanx Hollow": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Plow Scarecrow": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Sentinel": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Shears Scarecrow": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Silver Knight Greatbowman": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Silver Knight Spearman": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Silver Knight Swordsman": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Skeleton Archer": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Skeleton Beast": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Skeleton Soldier": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Snow Rat": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Stone Guardian": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Stone Knight": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Mimic": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Armorer Dennis": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Fencer Sharron": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Invader Brylex": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Kirk, Knight of Thorns": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Longfinger Kirk": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Maldron the Assassin": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Maneater Mildred": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Marvelous Chester": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Melinda the Butcher": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Oliver the Collector": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Paladin Leeroy": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Xanthous King Jeremiah": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Hungry Mimic": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None},
                    "Voracious Mimic": {"image": None, "photoImage": None, "photoImageBg1": None, "photoImageBg2": None, "treeviewImage": None}
                }
                self.iconsForCustom["Aggro"]["image"], self.iconsForCustom["Aggro"]["photoImage"], self.iconsForCustom["Aggro"]["photoImageBg1"], self.iconsForCustom["Aggro"]["photoImageBg2"], self.iconsForCustom["Aggro"]["treeviewImage"] = self.create_image("aggro.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Barrel"]["image"], self.iconsForCustom["Barrel"]["photoImage"], self.iconsForCustom["Barrel"]["photoImageBg1"], self.iconsForCustom["Barrel"]["photoImageBg2"], self.iconsForCustom["Barrel"]["treeviewImage"] = self.create_image("barrel.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Bleed"]["image"], self.iconsForCustom["Bleed"]["photoImage"], self.iconsForCustom["Bleed"]["photoImageBg1"], self.iconsForCustom["Bleed"]["photoImageBg2"], self.iconsForCustom["Bleed"]["treeviewImage"] = self.create_image("bleed.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Calamity"]["image"], self.iconsForCustom["Calamity"]["photoImage"], self.iconsForCustom["Calamity"]["photoImageBg1"], self.iconsForCustom["Calamity"]["photoImageBg2"], self.iconsForCustom["Calamity"]["treeviewImage"] = self.create_image("calamity.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Character Count"]["image"], self.iconsForCustom["Character Count"]["photoImage"], self.iconsForCustom["Character Count"]["photoImageBg1"], self.iconsForCustom["Character Count"]["photoImageBg2"], self.iconsForCustom["Character Count"]["treeviewImage"] = self.create_image("character_count.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Closest"]["image"], self.iconsForCustom["Closest"]["photoImage"], self.iconsForCustom["Closest"]["photoImageBg1"], self.iconsForCustom["Closest"]["photoImageBg2"], self.iconsForCustom["Closest"]["treeviewImage"] = self.create_image("closest.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Corrosion"]["image"], self.iconsForCustom["Corrosion"]["photoImage"], self.iconsForCustom["Corrosion"]["photoImageBg1"], self.iconsForCustom["Corrosion"]["photoImageBg2"], self.iconsForCustom["Corrosion"]["treeviewImage"] = self.create_image("corrosion.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Die (Black)"]["image"], self.iconsForCustom["Die (Black)"]["photoImage"], self.iconsForCustom["Die (Black)"]["photoImageBg1"], self.iconsForCustom["Die (Black)"]["photoImageBg2"], self.iconsForCustom["Die (Black)"]["treeviewImage"] = self.create_image("die_black.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Die (Blue)"]["image"], self.iconsForCustom["Die (Blue)"]["photoImage"], self.iconsForCustom["Die (Blue)"]["photoImageBg1"], self.iconsForCustom["Die (Blue)"]["photoImageBg2"], self.iconsForCustom["Die (Blue)"]["treeviewImage"] = self.create_image("die_blue.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Die (Orange)"]["image"], self.iconsForCustom["Die (Orange)"]["photoImage"], self.iconsForCustom["Die (Orange)"]["photoImageBg1"], self.iconsForCustom["Die (Orange)"]["photoImageBg2"], self.iconsForCustom["Die (Orange)"]["treeviewImage"] = self.create_image("die_orange.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Dodge"]["image"], self.iconsForCustom["Dodge"]["photoImage"], self.iconsForCustom["Dodge"]["photoImageBg1"], self.iconsForCustom["Dodge"]["photoImageBg2"], self.iconsForCustom["Dodge"]["treeviewImage"] = self.create_image("dodge.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Enemy Node 1"]["image"], self.iconsForCustom["Enemy Node 1"]["photoImage"], self.iconsForCustom["Enemy Node 1"]["photoImageBg1"], self.iconsForCustom["Enemy Node 1"]["photoImageBg2"], self.iconsForCustom["Enemy Node 1"]["treeviewImage"] = self.create_image("enemy_node_1.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Enemy Node 2"]["image"], self.iconsForCustom["Enemy Node 2"]["photoImage"], self.iconsForCustom["Enemy Node 2"]["photoImageBg1"], self.iconsForCustom["Enemy Node 2"]["photoImageBg2"], self.iconsForCustom["Enemy Node 2"]["treeviewImage"] = self.create_image("enemy_node_2.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Enemy Node 3"]["image"], self.iconsForCustom["Enemy Node 3"]["photoImage"], self.iconsForCustom["Enemy Node 3"]["photoImageBg1"], self.iconsForCustom["Enemy Node 3"]["photoImageBg2"], self.iconsForCustom["Enemy Node 3"]["treeviewImage"] = self.create_image("enemy_node_3.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Enemy Node 4"]["image"], self.iconsForCustom["Enemy Node 4"]["photoImage"], self.iconsForCustom["Enemy Node 4"]["photoImageBg1"], self.iconsForCustom["Enemy Node 4"]["photoImageBg2"], self.iconsForCustom["Enemy Node 4"]["treeviewImage"] = self.create_image("enemy_node_4.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Envoy Banner"]["image"], self.iconsForCustom["Envoy Banner"]["photoImage"], self.iconsForCustom["Envoy Banner"]["photoImageBg1"], self.iconsForCustom["Envoy Banner"]["photoImageBg2"], self.iconsForCustom["Envoy Banner"]["treeviewImage"] = self.create_image("envoy_banner.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Exit"]["image"], self.iconsForCustom["Exit"]["photoImage"], self.iconsForCustom["Exit"]["photoImageBg1"], self.iconsForCustom["Exit"]["photoImageBg2"], self.iconsForCustom["Exit"]["treeviewImage"] = self.create_image("exit.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Fang Boar"]["image"], self.iconsForCustom["Fang Boar"]["photoImage"], self.iconsForCustom["Fang Boar"]["photoImageBg1"], self.iconsForCustom["Fang Boar"]["photoImageBg2"], self.iconsForCustom["Fang Boar"]["treeviewImage"] = self.create_image("fang_boar.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Frostbite"]["image"], self.iconsForCustom["Frostbite"]["photoImage"], self.iconsForCustom["Frostbite"]["photoImageBg1"], self.iconsForCustom["Frostbite"]["photoImageBg2"], self.iconsForCustom["Frostbite"]["treeviewImage"] = self.create_image("frostbite.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Gravestone"]["image"], self.iconsForCustom["Gravestone"]["photoImage"], self.iconsForCustom["Gravestone"]["photoImageBg1"], self.iconsForCustom["Gravestone"]["photoImageBg2"], self.iconsForCustom["Gravestone"]["treeviewImage"] = self.create_image("gravestone.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Leap"]["image"], self.iconsForCustom["Leap"]["photoImage"], self.iconsForCustom["Leap"]["photoImageBg1"], self.iconsForCustom["Leap"]["photoImageBg2"], self.iconsForCustom["Leap"]["treeviewImage"] = self.create_image("leap.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Lever"]["image"], self.iconsForCustom["Lever"]["photoImage"], self.iconsForCustom["Lever"]["photoImageBg1"], self.iconsForCustom["Lever"]["photoImageBg2"], self.iconsForCustom["Lever"]["treeviewImage"] = self.create_image("lever.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Magic"]["image"], self.iconsForCustom["Magic"]["photoImage"], self.iconsForCustom["Magic"]["photoImageBg1"], self.iconsForCustom["Magic"]["photoImageBg2"], self.iconsForCustom["Magic"]["treeviewImage"] = self.create_image("magic.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Node Attack"]["image"], self.iconsForCustom["Node Attack"]["photoImage"], self.iconsForCustom["Node Attack"]["photoImageBg1"], self.iconsForCustom["Node Attack"]["photoImageBg2"], self.iconsForCustom["Node Attack"]["treeviewImage"] = self.create_image("node_attack.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Poison"]["image"], self.iconsForCustom["Poison"]["photoImage"], self.iconsForCustom["Poison"]["photoImageBg1"], self.iconsForCustom["Poison"]["photoImageBg2"], self.iconsForCustom["Poison"]["treeviewImage"] = self.create_image("poison.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Push"]["image"], self.iconsForCustom["Push"]["photoImage"], self.iconsForCustom["Push"]["photoImageBg1"], self.iconsForCustom["Push"]["photoImageBg2"], self.iconsForCustom["Push"]["treeviewImage"] = self.create_image("push.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Range"]["image"], self.iconsForCustom["Range"]["photoImage"], self.iconsForCustom["Range"]["photoImageBg1"], self.iconsForCustom["Range"]["photoImageBg2"], self.iconsForCustom["Range"]["treeviewImage"] = self.create_image("range.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Repeat"]["image"], self.iconsForCustom["Repeat"]["photoImage"], self.iconsForCustom["Repeat"]["photoImageBg1"], self.iconsForCustom["Repeat"]["photoImageBg2"], self.iconsForCustom["Repeat"]["treeviewImage"] = self.create_image("repeat.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Shaft"]["image"], self.iconsForCustom["Shaft"]["photoImage"], self.iconsForCustom["Shaft"]["photoImageBg1"], self.iconsForCustom["Shaft"]["photoImageBg2"], self.iconsForCustom["Shaft"]["treeviewImage"] = self.create_image("shaft.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Shift"]["image"], self.iconsForCustom["Shift"]["photoImage"], self.iconsForCustom["Shift"]["photoImageBg1"], self.iconsForCustom["Shift"]["photoImageBg2"], self.iconsForCustom["Shift"]["treeviewImage"] = self.create_image("shift.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Shrine"]["image"], self.iconsForCustom["Shrine"]["photoImage"], self.iconsForCustom["Shrine"]["photoImageBg1"], self.iconsForCustom["Shrine"]["photoImageBg2"], self.iconsForCustom["Shrine"]["treeviewImage"] = self.create_image("shrine.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Stagger"]["image"], self.iconsForCustom["Stagger"]["photoImage"], self.iconsForCustom["Stagger"]["photoImageBg1"], self.iconsForCustom["Stagger"]["photoImageBg2"], self.iconsForCustom["Stagger"]["treeviewImage"] = self.create_image("stagger.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Terrain Node 1"]["image"], self.iconsForCustom["Terrain Node 1"]["photoImage"], self.iconsForCustom["Terrain Node 1"]["photoImageBg1"], self.iconsForCustom["Terrain Node 1"]["photoImageBg2"], self.iconsForCustom["Terrain Node 1"]["treeviewImage"] = self.create_image("terrain_node_1.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Terrain Node 2"]["image"], self.iconsForCustom["Terrain Node 2"]["photoImage"], self.iconsForCustom["Terrain Node 2"]["photoImageBg1"], self.iconsForCustom["Terrain Node 2"]["photoImageBg2"], self.iconsForCustom["Terrain Node 2"]["treeviewImage"] = self.create_image("terrain_node_2.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Terrain Node 3"]["image"], self.iconsForCustom["Terrain Node 3"]["photoImage"], self.iconsForCustom["Terrain Node 3"]["photoImageBg1"], self.iconsForCustom["Terrain Node 3"]["photoImageBg2"], self.iconsForCustom["Terrain Node 3"]["treeviewImage"] = self.create_image("terrain_node_3.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Terrain Node 4"]["image"], self.iconsForCustom["Terrain Node 4"]["photoImage"], self.iconsForCustom["Terrain Node 4"]["photoImageBg1"], self.iconsForCustom["Terrain Node 4"]["photoImageBg2"], self.iconsForCustom["Terrain Node 4"]["treeviewImage"] = self.create_image("terrain_node_4.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Torch"]["image"], self.iconsForCustom["Torch"]["photoImage"], self.iconsForCustom["Torch"]["photoImageBg1"], self.iconsForCustom["Torch"]["photoImageBg2"], self.iconsForCustom["Torch"]["treeviewImage"] = self.create_image("torch.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Treasure Chest"]["image"], self.iconsForCustom["Treasure Chest"]["photoImage"], self.iconsForCustom["Treasure Chest"]["photoImageBg1"], self.iconsForCustom["Treasure Chest"]["photoImageBg2"], self.iconsForCustom["Treasure Chest"]["treeviewImage"] = self.create_image("treasure_chest.png", "iconForCustom", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Alonne Bow Knight"]["image"], self.iconsForCustom["Alonne Bow Knight"]["photoImage"], self.iconsForCustom["Alonne Bow Knight"]["photoImageBg1"], self.iconsForCustom["Alonne Bow Knight"]["photoImageBg2"], self.iconsForCustom["Alonne Bow Knight"]["treeviewImage"] = self.create_image("Alonne Bow Knight.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Alonne Knight Captain"]["image"], self.iconsForCustom["Alonne Knight Captain"]["photoImage"], self.iconsForCustom["Alonne Knight Captain"]["photoImageBg1"], self.iconsForCustom["Alonne Knight Captain"]["photoImageBg2"], self.iconsForCustom["Alonne Knight Captain"]["treeviewImage"] = self.create_image("Alonne Knight Captain.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Alonne Sword Knight"]["image"], self.iconsForCustom["Alonne Sword Knight"]["photoImage"], self.iconsForCustom["Alonne Sword Knight"]["photoImageBg1"], self.iconsForCustom["Alonne Sword Knight"]["photoImageBg2"], self.iconsForCustom["Alonne Sword Knight"]["treeviewImage"] = self.create_image("Alonne Sword Knight.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Black Hollow Mage"]["image"], self.iconsForCustom["Black Hollow Mage"]["photoImage"], self.iconsForCustom["Black Hollow Mage"]["photoImageBg1"], self.iconsForCustom["Black Hollow Mage"]["photoImageBg2"], self.iconsForCustom["Black Hollow Mage"]["treeviewImage"] = self.create_image("Black Hollow Mage.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Bonewheel Skeleton"]["image"], self.iconsForCustom["Bonewheel Skeleton"]["photoImage"], self.iconsForCustom["Bonewheel Skeleton"]["photoImageBg1"], self.iconsForCustom["Bonewheel Skeleton"]["photoImageBg2"], self.iconsForCustom["Bonewheel Skeleton"]["treeviewImage"] = self.create_image("Bonewheel Skeleton.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Crossbow Hollow"]["image"], self.iconsForCustom["Crossbow Hollow"]["photoImage"], self.iconsForCustom["Crossbow Hollow"]["photoImageBg1"], self.iconsForCustom["Crossbow Hollow"]["photoImageBg2"], self.iconsForCustom["Crossbow Hollow"]["treeviewImage"] = self.create_image("Crossbow Hollow.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Crow Demon"]["image"], self.iconsForCustom["Crow Demon"]["photoImage"], self.iconsForCustom["Crow Demon"]["photoImageBg1"], self.iconsForCustom["Crow Demon"]["photoImageBg2"], self.iconsForCustom["Crow Demon"]["treeviewImage"] = self.create_image("Crow Demon.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Demonic Foliage"]["image"], self.iconsForCustom["Demonic Foliage"]["photoImage"], self.iconsForCustom["Demonic Foliage"]["photoImageBg1"], self.iconsForCustom["Demonic Foliage"]["photoImageBg2"], self.iconsForCustom["Demonic Foliage"]["treeviewImage"] = self.create_image("Demonic Foliage.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Engorged Zombie"]["image"], self.iconsForCustom["Engorged Zombie"]["photoImage"], self.iconsForCustom["Engorged Zombie"]["photoImageBg1"], self.iconsForCustom["Engorged Zombie"]["photoImageBg2"], self.iconsForCustom["Engorged Zombie"]["treeviewImage"] = self.create_image("Engorged Zombie.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Falchion Skeleton"]["image"], self.iconsForCustom["Falchion Skeleton"]["photoImage"], self.iconsForCustom["Falchion Skeleton"]["photoImageBg1"], self.iconsForCustom["Falchion Skeleton"]["photoImageBg2"], self.iconsForCustom["Falchion Skeleton"]["treeviewImage"] = self.create_image("Falchion Skeleton.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Firebomb Hollow"]["image"], self.iconsForCustom["Firebomb Hollow"]["photoImage"], self.iconsForCustom["Firebomb Hollow"]["photoImageBg1"], self.iconsForCustom["Firebomb Hollow"]["photoImageBg2"], self.iconsForCustom["Firebomb Hollow"]["treeviewImage"] = self.create_image("Firebomb Hollow.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Giant Skeleton Archer"]["image"], self.iconsForCustom["Giant Skeleton Archer"]["photoImage"], self.iconsForCustom["Giant Skeleton Archer"]["photoImageBg1"], self.iconsForCustom["Giant Skeleton Archer"]["photoImageBg2"], self.iconsForCustom["Giant Skeleton Archer"]["treeviewImage"] = self.create_image("Giant Skeleton Archer.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Giant Skeleton Soldier"]["image"], self.iconsForCustom["Giant Skeleton Soldier"]["photoImage"], self.iconsForCustom["Giant Skeleton Soldier"]["photoImageBg1"], self.iconsForCustom["Giant Skeleton Soldier"]["photoImageBg2"], self.iconsForCustom["Giant Skeleton Soldier"]["treeviewImage"] = self.create_image("Giant Skeleton Soldier.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Hollow Soldier"]["image"], self.iconsForCustom["Hollow Soldier"]["photoImage"], self.iconsForCustom["Hollow Soldier"]["photoImageBg1"], self.iconsForCustom["Hollow Soldier"]["photoImageBg2"], self.iconsForCustom["Hollow Soldier"]["treeviewImage"] = self.create_image("Hollow Soldier.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Ironclad Soldier"]["image"], self.iconsForCustom["Ironclad Soldier"]["photoImage"], self.iconsForCustom["Ironclad Soldier"]["photoImageBg1"], self.iconsForCustom["Ironclad Soldier"]["photoImageBg2"], self.iconsForCustom["Ironclad Soldier"]["treeviewImage"] = self.create_image("Ironclad Soldier.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Large Hollow Soldier"]["image"], self.iconsForCustom["Large Hollow Soldier"]["photoImage"], self.iconsForCustom["Large Hollow Soldier"]["photoImageBg1"], self.iconsForCustom["Large Hollow Soldier"]["photoImageBg2"], self.iconsForCustom["Large Hollow Soldier"]["treeviewImage"] = self.create_image("Large Hollow Soldier.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Mushroom Child"]["image"], self.iconsForCustom["Mushroom Child"]["photoImage"], self.iconsForCustom["Mushroom Child"]["photoImageBg1"], self.iconsForCustom["Mushroom Child"]["photoImageBg2"], self.iconsForCustom["Mushroom Child"]["treeviewImage"] = self.create_image("Mushroom Child.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Mushroom Parent"]["image"], self.iconsForCustom["Mushroom Parent"]["photoImage"], self.iconsForCustom["Mushroom Parent"]["photoImageBg1"], self.iconsForCustom["Mushroom Parent"]["photoImageBg2"], self.iconsForCustom["Mushroom Parent"]["treeviewImage"] = self.create_image("Mushroom Parent.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Necromancer"]["image"], self.iconsForCustom["Necromancer"]["photoImage"], self.iconsForCustom["Necromancer"]["photoImageBg1"], self.iconsForCustom["Necromancer"]["photoImageBg2"], self.iconsForCustom["Necromancer"]["treeviewImage"] = self.create_image("Necromancer.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Phalanx"]["image"], self.iconsForCustom["Phalanx"]["photoImage"], self.iconsForCustom["Phalanx"]["photoImageBg1"], self.iconsForCustom["Phalanx"]["photoImageBg2"], self.iconsForCustom["Phalanx"]["treeviewImage"] = self.create_image("Phalanx.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Phalanx Hollow"]["image"], self.iconsForCustom["Phalanx Hollow"]["photoImage"], self.iconsForCustom["Phalanx Hollow"]["photoImageBg1"], self.iconsForCustom["Phalanx Hollow"]["photoImageBg2"], self.iconsForCustom["Phalanx Hollow"]["treeviewImage"] = self.create_image("Phalanx Hollow.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Plow Scarecrow"]["image"], self.iconsForCustom["Plow Scarecrow"]["photoImage"], self.iconsForCustom["Plow Scarecrow"]["photoImageBg1"], self.iconsForCustom["Plow Scarecrow"]["photoImageBg2"], self.iconsForCustom["Plow Scarecrow"]["treeviewImage"] = self.create_image("Plow Scarecrow.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Sentinel"]["image"], self.iconsForCustom["Sentinel"]["photoImage"], self.iconsForCustom["Sentinel"]["photoImageBg1"], self.iconsForCustom["Sentinel"]["photoImageBg2"], self.iconsForCustom["Sentinel"]["treeviewImage"] = self.create_image("Sentinel.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Shears Scarecrow"]["image"], self.iconsForCustom["Shears Scarecrow"]["photoImage"], self.iconsForCustom["Shears Scarecrow"]["photoImageBg1"], self.iconsForCustom["Shears Scarecrow"]["photoImageBg2"], self.iconsForCustom["Shears Scarecrow"]["treeviewImage"] = self.create_image("Shears Scarecrow.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Silver Knight Greatbowman"]["image"], self.iconsForCustom["Silver Knight Greatbowman"]["photoImage"], self.iconsForCustom["Silver Knight Greatbowman"]["photoImageBg1"], self.iconsForCustom["Silver Knight Greatbowman"]["photoImageBg2"], self.iconsForCustom["Silver Knight Greatbowman"]["treeviewImage"] = self.create_image("Silver Knight Greatbowman.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Silver Knight Spearman"]["image"], self.iconsForCustom["Silver Knight Spearman"]["photoImage"], self.iconsForCustom["Silver Knight Spearman"]["photoImageBg1"], self.iconsForCustom["Silver Knight Spearman"]["photoImageBg2"], self.iconsForCustom["Silver Knight Spearman"]["treeviewImage"] = self.create_image("Silver Knight Spearman.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Silver Knight Swordsman"]["image"], self.iconsForCustom["Silver Knight Swordsman"]["photoImage"], self.iconsForCustom["Silver Knight Swordsman"]["photoImageBg1"], self.iconsForCustom["Silver Knight Swordsman"]["photoImageBg2"], self.iconsForCustom["Silver Knight Swordsman"]["treeviewImage"] = self.create_image("Silver Knight Swordsman.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Skeleton Archer"]["image"], self.iconsForCustom["Skeleton Archer"]["photoImage"], self.iconsForCustom["Skeleton Archer"]["photoImageBg1"], self.iconsForCustom["Skeleton Archer"]["photoImageBg2"], self.iconsForCustom["Skeleton Archer"]["treeviewImage"] = self.create_image("Skeleton Archer.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Skeleton Beast"]["image"], self.iconsForCustom["Skeleton Beast"]["photoImage"], self.iconsForCustom["Skeleton Beast"]["photoImageBg1"], self.iconsForCustom["Skeleton Beast"]["photoImageBg2"], self.iconsForCustom["Skeleton Beast"]["treeviewImage"] = self.create_image("Skeleton Beast.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Skeleton Soldier"]["image"], self.iconsForCustom["Skeleton Soldier"]["photoImage"], self.iconsForCustom["Skeleton Soldier"]["photoImageBg1"], self.iconsForCustom["Skeleton Soldier"]["photoImageBg2"], self.iconsForCustom["Skeleton Soldier"]["treeviewImage"] = self.create_image("Skeleton Soldier.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Snow Rat"]["image"], self.iconsForCustom["Snow Rat"]["photoImage"], self.iconsForCustom["Snow Rat"]["photoImageBg1"], self.iconsForCustom["Snow Rat"]["photoImageBg2"], self.iconsForCustom["Snow Rat"]["treeviewImage"] = self.create_image("Snow Rat.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Stone Guardian"]["image"], self.iconsForCustom["Stone Guardian"]["photoImage"], self.iconsForCustom["Stone Guardian"]["photoImageBg1"], self.iconsForCustom["Stone Guardian"]["photoImageBg2"], self.iconsForCustom["Stone Guardian"]["treeviewImage"] = self.create_image("Stone Guardian.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Stone Knight"]["image"], self.iconsForCustom["Stone Knight"]["photoImage"], self.iconsForCustom["Stone Knight"]["photoImageBg1"], self.iconsForCustom["Stone Knight"]["photoImageBg2"], self.iconsForCustom["Stone Knight"]["treeviewImage"] = self.create_image("Stone Knight.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Mimic"]["image"], self.iconsForCustom["Mimic"]["photoImage"], self.iconsForCustom["Mimic"]["photoImageBg1"], self.iconsForCustom["Mimic"]["photoImageBg2"], self.iconsForCustom["Mimic"]["treeviewImage"] = self.create_image("Mimic.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Armorer Dennis"]["image"], self.iconsForCustom["Armorer Dennis"]["photoImage"], self.iconsForCustom["Armorer Dennis"]["photoImageBg1"], self.iconsForCustom["Armorer Dennis"]["photoImageBg2"], self.iconsForCustom["Armorer Dennis"]["treeviewImage"] = self.create_image("Armorer Dennis.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Fencer Sharron"]["image"], self.iconsForCustom["Fencer Sharron"]["photoImage"], self.iconsForCustom["Fencer Sharron"]["photoImageBg1"], self.iconsForCustom["Fencer Sharron"]["photoImageBg2"], self.iconsForCustom["Fencer Sharron"]["treeviewImage"] = self.create_image("Fencer Sharron.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Invader Brylex"]["image"], self.iconsForCustom["Invader Brylex"]["photoImage"], self.iconsForCustom["Invader Brylex"]["photoImageBg1"], self.iconsForCustom["Invader Brylex"]["photoImageBg2"], self.iconsForCustom["Invader Brylex"]["treeviewImage"] = self.create_image("Invader Brylex.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Kirk, Knight of Thorns"]["image"], self.iconsForCustom["Kirk, Knight of Thorns"]["photoImage"], self.iconsForCustom["Kirk, Knight of Thorns"]["photoImageBg1"], self.iconsForCustom["Kirk, Knight of Thorns"]["photoImageBg2"], self.iconsForCustom["Kirk, Knight of Thorns"]["treeviewImage"] = self.create_image("Kirk, Knight of Thorns.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Longfinger Kirk"]["image"], self.iconsForCustom["Longfinger Kirk"]["photoImage"], self.iconsForCustom["Longfinger Kirk"]["photoImageBg1"], self.iconsForCustom["Longfinger Kirk"]["photoImageBg2"], self.iconsForCustom["Longfinger Kirk"]["treeviewImage"] = self.create_image("Longfinger Kirk.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Maldron the Assassin"]["image"], self.iconsForCustom["Maldron the Assassin"]["photoImage"], self.iconsForCustom["Maldron the Assassin"]["photoImageBg1"], self.iconsForCustom["Maldron the Assassin"]["photoImageBg2"], self.iconsForCustom["Maldron the Assassin"]["treeviewImage"] = self.create_image("Maldron the Assassin.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Maneater Mildred"]["image"], self.iconsForCustom["Maneater Mildred"]["photoImage"], self.iconsForCustom["Maneater Mildred"]["photoImageBg1"], self.iconsForCustom["Maneater Mildred"]["photoImageBg2"], self.iconsForCustom["Maneater Mildred"]["treeviewImage"] = self.create_image("Maneater Mildred.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Marvelous Chester"]["image"], self.iconsForCustom["Marvelous Chester"]["photoImage"], self.iconsForCustom["Marvelous Chester"]["photoImageBg1"], self.iconsForCustom["Marvelous Chester"]["photoImageBg2"], self.iconsForCustom["Marvelous Chester"]["treeviewImage"] = self.create_image("Marvelous Chester.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Melinda the Butcher"]["image"], self.iconsForCustom["Melinda the Butcher"]["photoImage"], self.iconsForCustom["Melinda the Butcher"]["photoImageBg1"], self.iconsForCustom["Melinda the Butcher"]["photoImageBg2"], self.iconsForCustom["Melinda the Butcher"]["treeviewImage"] = self.create_image("Melinda the Butcher.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Oliver the Collector"]["image"], self.iconsForCustom["Oliver the Collector"]["photoImage"], self.iconsForCustom["Oliver the Collector"]["photoImageBg1"], self.iconsForCustom["Oliver the Collector"]["photoImageBg2"], self.iconsForCustom["Oliver the Collector"]["treeviewImage"] = self.create_image("Oliver the Collector.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Paladin Leeroy"]["image"], self.iconsForCustom["Paladin Leeroy"]["photoImage"], self.iconsForCustom["Paladin Leeroy"]["photoImageBg1"], self.iconsForCustom["Paladin Leeroy"]["photoImageBg2"], self.iconsForCustom["Paladin Leeroy"]["treeviewImage"] = self.create_image("Paladin Leeroy.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Xanthous King Jeremiah"]["image"], self.iconsForCustom["Xanthous King Jeremiah"]["photoImage"], self.iconsForCustom["Xanthous King Jeremiah"]["photoImageBg1"], self.iconsForCustom["Xanthous King Jeremiah"]["photoImageBg2"], self.iconsForCustom["Xanthous King Jeremiah"]["treeviewImage"] = self.create_image("Xanthous King Jeremiah.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Hungry Mimic"]["image"], self.iconsForCustom["Hungry Mimic"]["photoImage"], self.iconsForCustom["Hungry Mimic"]["photoImageBg1"], self.iconsForCustom["Hungry Mimic"]["photoImageBg2"], self.iconsForCustom["Hungry Mimic"]["treeviewImage"] = self.create_image("Hungry Mimic.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)
                self.iconsForCustom["Voracious Mimic"]["image"], self.iconsForCustom["Voracious Mimic"]["photoImage"], self.iconsForCustom["Voracious Mimic"]["photoImageBg1"], self.iconsForCustom["Voracious Mimic"]["photoImageBg2"], self.iconsForCustom["Voracious Mimic"]["treeviewImage"] = self.create_image("Voracious Mimic.png", "iconForCustomEnemy", 99, extensionProvided=True, progress=True)

                if self.settings["variantEnable"] == "off" and self.settings["treasureSwapOption"] not in {"Similar Soul Cost", "Tier Based"}:
                    self.progress.label.config(text="Praising the Sun... ")

                self.tileNumbers = {}
                for x in range(1, 4):
                    s = str(x)
                    self.tileNumbers[x] = {
                        "starting": {
                            "traps": self.create_image("custom_encounter_starting_" + s + "_traps.png", "tileNum", 99, extensionProvided=True, progress=True),
                            "noTraps": self.create_image("custom_encounter_starting_" + s + "_no_traps.png", "tileNum", 99, extensionProvided=True, progress=True)
                        },
                        "notStarting": {
                            "traps": self.create_image("custom_encounter_not_starting_" + s + "_traps.png", "tileNum", 99, extensionProvided=True, progress=True),
                            "noTraps": self.create_image("custom_encounter_not_starting_" + s + "_no_traps.png", "tileNum", 99, extensionProvided=True, progress=True)
                        }
                    }

                self.tileLayouts = {
                    "1 Tile": {
                        "layout": self.create_image("custom_encounter_layout_1_tile.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": self.create_image("custom_encounter_1_tile_starting_nodes_horizontal.png", "nodes1TileHorizontal", 99, extensionProvided=True, progress=True),
                        "startingNodesVertical": self.create_image("custom_encounter_1_tile_starting_nodes_vertical.png", "nodes1TileVertical", 99, extensionProvided=True, progress=True),
                        "box": {
                            1: {
                                1: (59, 414),
                                2: (59, 555),
                                3: (59, 414),
                                4: (198, 414)
                                }
                            }
                        },
                    "1 Tile 4x4": {
                        "layout": self.create_image("custom_encounter_layout_1_tile_4x4.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": self.create_image("custom_encounter_4x4_starting_nodes_horizontal.png", "nodesLevel4Horizontal", 99, extensionProvided=True, progress=True),
                        "startingNodesVertical": self.create_image("custom_encounter_4x4_starting_nodes_vertical.png", "nodesLevel4Vertical", 99, extensionProvided=True, progress=True),
                        "box": {
                            1: {
                                1: (47, 403),
                                2: (47, 570),
                                3: (47, 403),
                                4: (212, 403)
                                }
                            }
                        },
                    "2 Tiles Horizontal": {
                        "layout": self.create_image("custom_encounter_layout_2_tiles_horizontal.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (44, 452),
                                2: (44, 524),
                                3: (44, 452),
                                4: (115, 452)
                                },
                            2: {
                                1: (152, 452),
                                2: (152, 524),
                                3: (152, 452),
                                4: (223, 452)
                                }
                            }
                        },
                    "2 Tiles Vertical": {
                        "layout": self.create_image("custom_encounter_layout_2_tiles_vertical.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (98, 402),
                                2: (98, 474),
                                3: (98, 402),
                                4: (169, 402)
                                },
                            2: {
                                1: (98, 509),
                                2: (98, 581),
                                3: (98, 509),
                                4: (169, 509)
                                }
                            }
                        },
                    "2 Tiles Illusion": {
                        "layout": self.create_image("custom_encounter_layout_2_tiles_illusion.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (98, 382),
                                2: (98, 454),
                                3: (98, 382),
                                4: (169, 382)
                                }
                            }
                        },
                    "2 Tiles Separated": {
                        "layout": self.create_image("custom_encounter_layout_2_tiles_separated.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (98, 382),
                                2: (98, 454),
                                3: (98, 382),
                                4: (169, 382)
                                },
                            2: {
                                1: (98, 522),
                                2: (98, 594),
                                3: (98, 522),
                                4: (169, 522)
                                }
                            }
                        },
                    "3 Tiles Vertical": {
                        "layout": self.create_image("custom_encounter_layout_3_tile_vertical.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (98, 347),
                                2: (98, 419),
                                3: (98, 347),
                                4: (169, 347)
                                },
                            2: {
                                1: (98, 455),
                                2: (98, 527),
                                3: (98, 455),
                                4: (169, 455)
                                },
                            3: {
                                1: (98, 562),
                                2: (98, 654),
                                3: (98, 562),
                                4: (169, 562)
                                }
                            }
                        },
                    "3 Tiles: 1 NE, 2 NW, 3 SW": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_NE_2_NW_3_SW.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (151, 402),
                                2: (151, 474),
                                3: (151, 402),
                                4: (222, 402)
                                },
                            2: {
                                1: (45, 402),
                                2: (45, 474),
                                3: (45, 402),
                                4: (116, 402)
                                },
                            3: {
                                1: (45, 509),
                                2: (45, 581),
                                3: (45, 509),
                                4: (116, 509)
                                }
                            }
                        },
                    "3 Tiles: 1 NW, 2 NE, 3 SW": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_NW_2_NE_3_SW.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (45, 402),
                                2: (45, 474),
                                3: (45, 402),
                                4: (116, 402)
                                },
                            2: {
                                1: (151, 402),
                                2: (151, 474),
                                3: (151, 402),
                                4: (222, 402)
                                },
                            3: {
                                1: (45, 509),
                                2: (45, 581),
                                3: (45, 509),
                                4: (116, 509)
                                }
                            }
                        },
                    "3 Tiles: 1 NW, 2 SW, 3 SE": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_NW_2_SW_3_SE.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (45, 402),
                                2: (45, 474),
                                3: (45, 402),
                                4: (116, 402)
                                },
                            2: {
                                1: (45, 509),
                                2: (45, 581),
                                3: (45, 509),
                                4: (116, 509)
                                },
                            3: {
                                1: (151, 509),
                                2: (151, 581),
                                3: (151, 509),
                                4: (222, 509)
                                }
                            }
                        },
                    "3 Tiles: 1 SE, 2 NE, 3 NW": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_SE_2_NE_3_NW.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (151, 509),
                                2: (151, 581),
                                3: (151, 509),
                                4: (222, 509)
                                },
                            2: {
                                1: (151, 402),
                                2: (151, 474),
                                3: (151, 402),
                                4: (222, 402)
                                },
                            3: {
                                1: (45, 402),
                                2: (45, 474),
                                3: (45, 402),
                                4: (116, 402)
                                }
                            }
                        },
                    "3 Tiles: 1 SW, 2 NW, 3 SE": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_SW_2_NW_3_SE.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (45, 509),
                                2: (45, 581),
                                3: (45, 509),
                                4: (116, 509)
                                },
                            2: {
                                1: (45, 402),
                                2: (45, 474),
                                3: (45, 402),
                                4: (116, 402)
                                },
                            3: {
                                1: (151, 509),
                                2: (151, 581),
                                3: (151, 509),
                                4: (222, 509)
                                }
                            }
                        },
                    "3 Tiles: 1 SW, 2 SE, 3 NE": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_SW_2_SE_3_NE.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (45, 509),
                                2: (45, 581),
                                3: (45, 509),
                                4: (116, 509)
                                },
                            2: {
                                1: (151, 509),
                                2: (151, 581),
                                3: (151, 509),
                                4: (222, 509)
                                },
                            3: {
                                1: (151, 402),
                                2: (151, 474),
                                3: (151, 402),
                                4: (222, 402)
                                }
                            }
                        },
                    "3 Tiles Illusion": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_illusion.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (38, 393),
                                2: (38, 465),
                                3: (38, 393),
                                4: (109, 393)
                                }
                            }
                        },
                    "3 Tiles Separated": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_separated.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (38, 393),
                                2: (38, 465),
                                3: (38, 393),
                                4: (109, 393)
                                }
                            }
                        },
                    "3 Tiles, Tile 1 Separated": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_separate.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (39, 393),
                                2: (39, 465),
                                3: (39, 393),
                                4: (110, 393)
                                },
                            2: {
                                1: (39, 514),
                                2: (39, 586),
                                3: (39, 514),
                                4: (110, 514)
                                },
                            3: {
                                1: (145, 514),
                                2: (145, 586),
                                3: (145, 514),
                                4: (216, 514)
                                }
                            }
                        },
                    "3 Tiles, Tile 3 Separated": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_3_separate.png", "layout", 99, extensionProvided=True, progress=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (38, 407),
                                2: (38, 479),
                                3: (38, 407),
                                4: (109, 407)
                                },
                            2: {
                                1: (38, 514),
                                2: (38, 586),
                                3: (38, 514),
                                4: (109, 514)
                                },
                            3: {
                                1: (158, 514),
                                2: (158, 586),
                                3: (158, 514),
                                4: (229, 514)
                                }
                            }
                        }
                }
                
                self.progress.label.config(text="Loading treasure...")
                if self.settings["treasureSwapOption"] in {"Similar Soul Cost", "Tier Based"}:
                    generate_treasure_soul_cost(self.availableExpansions, self.charactersActive, root, self.progress, self.settings["variantEnable"] == "off")
                
                if self.settings["treasureSwapOption"] == "Tier Based":
                    populate_treasure_tiers(self.availableExpansions, self.charactersActive)

                self.create_tabs()
                self.create_buttons()
                self.create_display_frame()
                self.create_menu()
                self.set_bindings_buttons_menus(True)

                root.state("zoomed")

                self.progress.destroy()
                root.deiconify()
            except Exception as e:
                error_popup(root, e)
                raise


        def on_frame_configure(self, canvas):
            """Reset the scroll region to encompass the inner frame"""
            canvas.configure(scrollregion=canvas.bbox("all"))


        def _bound_to_mousewheel(self, event):
            self.displayCanvas.bind_all("<MouseWheel>", self._on_mousewheel)


        def _unbound_to_mousewheel(self, event):
            self.displayCanvas.unbind_all("<MouseWheel>")


        def _on_mousewheel(self, event):
            self.displayCanvas.yview_scroll(int(-1*(event.delta/120)), "units")


        def create_tabs(self, event=None):
            """
            Create the tabs in the main window.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of create_tabs")

                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep)) as settingsFile:
                    self.settings = load(settingsFile)

                self.paned = ttk.PanedWindow(self)
                self.paned.bind("<1>", lambda event: event.widget.focus_set())
                self.paned.grid_rowconfigure(index=0, weight=1)
                self.paned.grid(row=1, column=0, pady=(5, 5), padx=(5, 5), sticky="nsew", columnspan=4)

                self.pane = ttk.Frame(self.paned, padding=5)
                self.pane.bind("<1>", lambda event: event.widget.focus_set())
                self.pane.grid_rowconfigure(index=0, weight=1)
                self.paned.add(self.pane, weight=1)

                self.notebook = ttk.Notebook(self.paned, width=600)
                self.notebook.bind("<1>", lambda event: event.widget.focus_set())
                self.notebook.bind('<<NotebookTabChanged>>', self.tab_change)
                self.notebook.pack(fill="both", expand=True)

                self.campaignTab = CampaignFrame(root=root, app=self)
                self.campaignTab.bind("<1>", lambda event: event.widget.focus_set())
                self.notebook.add(self.campaignTab, text="Campaign")
                
                self.eventTab = EventsFrame(root=root, app=self)
                self.eventTab.bind("<1>", lambda event: event.widget.focus_set())
                self.notebook.add(self.eventTab, text="Events")

                self.variantsTab = VariantsFrame(root=root, app=self)
                self.variantsTab.bind("<1>", lambda event: event.widget.focus_set())
                self.notebook.add(self.variantsTab, text="Behavior Variants")
                if self.settings["variantEnable"] == "off":
                    self.notebook.tab(2, state=tk.DISABLED)

                self.behaviorDeckTab = BehaviorDeckFrame(root=root, app=self)
                self.behaviorDeckTab.bind("<1>", lambda event: event.widget.focus_set())
                self.notebook.add(self.behaviorDeckTab, text="Behavior Decks")

                self.encounterBuilderTab = EncounterBuilderFrame(root=root, app=self)
                self.encounterBuilderTab.bind("<1>", lambda event: event.widget.focus_set())
                self.notebook.add(self.encounterBuilderTab, text="Encounter Builder")

                self.encounterTab = EncountersFrame(root=root, app=self)
                self.encounterTab.bind("<1>", lambda event: event.widget.focus_set())
                for index in [0, 1]:
                    self.encounterTab.columnconfigure(index=index, weight=1)
                    self.encounterTab.rowconfigure(index=index, weight=1)
                self.notebook.insert(0, self.encounterTab, text="Encounters")

                self.notebook.select(0)

                log("End of create_tabs")
            except Exception as e:
                error_popup(root, e)
                raise


        def tab_change(self, event=None):
            """
            Clear the current image and open the last selected image, if any.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of tab_change")

                if self.notebook.tab(self.notebook.select(), "text") == "Encounters" and self.encounterTab.treeviewEncounters.selection():
                    tree = self.encounterTab.treeviewEncounters
                    self.encounterTab.load_encounter(encounter=tree.item(tree.selection())["text"])
                elif self.notebook.tab(self.notebook.select(), "text") == "Campaign" and self.campaignTab.treeviewCampaign.selection():
                    self.campaignTab.load_campaign_card()
                elif self.notebook.tab(self.notebook.select(), "text") == "Events":
                    self.eventTab.load_event()
                elif self.notebook.tab(self.notebook.select(), "text") == "Behavior Decks" and self.behaviorDeckTab.treeviewDecks.selection():
                    self.behaviorDeckTab.display_deck_cards()
                elif self.notebook.tab(self.notebook.select(), "text") == "Behavior Variants":
                    if self.variantsTab.treeviewVariantsLocked.selection():
                        self.variantsTab.load_variant_card_locked(variant=self.variantsTab.treeviewVariantsLocked.selection()[0])
                    elif self.variantsTab.treeviewVariantsList.selection():
                        self.variantsTab.load_variant_card(variant=self.variantsTab.treeviewVariantsList.selection()[0])
                elif self.notebook.tab(self.notebook.select(), "text") == "Encounter Builder":
                    self.encounterBuilderTab.apply_changes()
                else:
                    log("End of tab_change (cleared image only)")
                    return
                
                set_display_bindings_by_tab(self)

                log("End of tab_change")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_display_frame(self):
            """
            Create the frame in which cards will be displayed.
            """
            try:
                log("Start of create_display_frame")

                self.displayCanvas = tk.Canvas(self, width=820, yscrollcommand=self.displayScrollbar.set)
                self.displayFrame = ttk.Frame(self.displayCanvas)
                self.displayFrame.columnconfigure(index=0, weight=1, minsize=410)
                self.displayCanvas.grid(row=0, column=4, padx=10, pady=(10, 0), sticky="nsew", rowspan=2)
                self.displayCanvas.create_window((0,0), window=self.displayFrame, anchor=tk.NW)
                self.displayScrollbar.config(command=self.displayCanvas.yview)
                self.displayFrame.bind("<Enter>", self._bound_to_mousewheel)
                self.displayFrame.bind("<Leave>", self._unbound_to_mousewheel)
                self.displayFrame.bind("<Configure>", lambda event, canvas=self.displayCanvas: self.on_frame_configure(canvas))

                self.displayTopLeft = ttk.Label(self.displayFrame)
                self.displayTopLeft.image = None
                self.displayTopLeft.grid(column=0, row=0, sticky="nsew")
                self.displayTopRight = ttk.Label(self.displayFrame)
                self.displayTopRight.image = None
                self.displayTopRight.grid(column=1, row=0, sticky="nsew", columnspan=2)
                self.displayBottomLeft = ttk.Label(self.displayFrame)
                self.displayBottomLeft.image = None
                self.displayBottomLeft.grid(column=0, row=1, sticky="nsew")
                self.displayBottomRight = ttk.Label(self.displayFrame)
                self.displayBottomRight.image = None
                self.displayBottomRight.grid(column=1, row=1, sticky="nsew", columnspan=2)

                # Frames for health trackers
                self.displayKing1 = ttk.Label(self.displayFrame)
                self.displayKing1.image = None
                self.displayKing2 = ttk.Label(self.displayFrame)
                self.displayKing2.image = None
                self.displayKing3 = ttk.Label(self.displayFrame)
                self.displayKing3.image = None
                self.displayKing4 = ttk.Label(self.displayFrame)
                self.displayKing4.image = None

                self.displayKing1.bind("<Button 1>", lambda event, x=1: app.behaviorDeckTab.lower_health_king(event=event, king=1, amount=x))
                self.displayKing1.bind("<Shift-Button 1>", lambda event, x=5: app.behaviorDeckTab.lower_health_king(event=event, king=1, amount=x))
                self.displayKing1.bind("<Button 3>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=1, amount=x))
                self.displayKing1.bind("<Shift-Button 3>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=1, amount=x))
                self.displayKing1.bind("<Control-1>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=1, amount=x))
                self.displayKing1.bind("<Shift-Control-1>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=1, amount=x))

                self.displayKing2.bind("<Button 1>", lambda event, x=1: app.behaviorDeckTab.lower_health_king(event=event, king=2, amount=x))
                self.displayKing2.bind("<Shift-Button 1>", lambda event, x=5: app.behaviorDeckTab.lower_health_king(event=event, king=2, amount=x))
                self.displayKing2.bind("<Button 3>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=2, amount=x))
                self.displayKing2.bind("<Shift-Button 3>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=2, amount=x))
                self.displayKing2.bind("<Control-1>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=2, amount=x))
                self.displayKing2.bind("<Shift-Control-1>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=2, amount=x))

                self.displayKing3.bind("<Button 1>", lambda event, x=1: app.behaviorDeckTab.lower_health_king(event=event, king=3, amount=x))
                self.displayKing3.bind("<Shift-Button 1>", lambda event, x=5: app.behaviorDeckTab.lower_health_king(event=event, king=3, amount=x))
                self.displayKing3.bind("<Button 3>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=3, amount=x))
                self.displayKing3.bind("<Shift-Button 3>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=3, amount=x))
                self.displayKing3.bind("<Control-1>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=3, amount=x))
                self.displayKing3.bind("<Shift-Control-1>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=3, amount=x))

                self.displayKing4.bind("<Button 1>", lambda event, x=1: app.behaviorDeckTab.lower_health_king(event=event, king=4, amount=x))
                self.displayKing4.bind("<Shift-Button 1>", lambda event, x=5: app.behaviorDeckTab.lower_health_king(event=event, king=4, amount=x))
                self.displayKing4.bind("<Button 3>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=4, amount=x))
                self.displayKing4.bind("<Shift-Button 3>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=4, amount=x))
                self.displayKing4.bind("<Control-1>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=4, amount=x))
                self.displayKing4.bind("<Shift-Control-1>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=4, amount=x))

                for enemy in [e for e in self.enabledEnemies if "Phantoms" not in enemyIds[e].expansions and enemyIds[e].name not in {"Hungry Mimic", "Voracious Mimic"}]:
                    self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"] = []
                    for _ in range(8):
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"].append(ttk.Label(self.displayFrame))
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].image = None
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].bind("<Button 1>", lambda event, x=1: app.behaviorDeckTab.lower_health_regular(event=event, amount=x))
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].bind("<Shift-Button 1>", lambda event, x=5: app.behaviorDeckTab.lower_health_regular(event=event, amount=x))
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].bind("<Button 3>", lambda event, x=1: app.behaviorDeckTab.raise_health_regular(event=event, amount=x))
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].bind("<Shift-Button 3>", lambda event, x=5: app.behaviorDeckTab.raise_health_regular(event=event, amount=x))
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].bind("<Control-1>", lambda event, x=1: app.behaviorDeckTab.raise_health_regular(event=event, amount=x))
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].bind("<Shift-Control-1>", lambda event, x=5: app.behaviorDeckTab.raise_health_regular(event=event, amount=x))

                self.displayImages = {
                    "encounters": {
                        self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                    },
                    "events": {
                        self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                    },
                    "variants": {
                        self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                    },
                    "variantsLocked": {
                        self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                    },
                    "behaviorDeck": {
                        self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                    }
                }

                log("End of create_display_frame")
            except Exception as e:
                error_popup(root, e)
                raise


        def add_custom_encounters(self):
            """
            Adds custom encounters to the list of all encounters.
            """
            try:
                log("Start of add_custom_encounters")
                    
                self.customEncounters = {tuple(e.split("_")) for e in set([os.path.splitext(f)[0] for f in os.listdir(baseFolder + "\\lib\\dsbg_shuffle_custom_encounters".replace("\\", pathSep)) if f.count("_") == 2 and ".jpg" in f])}
                self.customEncounters = self.customEncounters | {tuple(e.split("_")) for e in set([os.path.splitext(f)[0] for f in os.listdir(baseFolder + "\\lib\\dsbg_shuffle_custom_encounters".replace("\\", pathSep)) if f.count("_") == 2 and ".png" in f])}
                self.customEncounters = list(self.customEncounters)

                for enc in [enc for enc in self.customEncounters if "Custom - " + enc[1] + " (" + enc[0] + ")" not in self.encounters]:
                    self.encounters["Custom - " + enc[1] + " (" + enc[0] + ")"] = {
                        "name": "Custom - " + enc[1] + " (" + enc[0] + ")",
                        "expansion": enc[0],
                        "level": int(enc[2]),
                        "expansionCombos": {
                            "1": [[enc[0]]],
                            "2": [[enc[0]]],
                            "3": [[enc[0]]],
                            "4": [[enc[0]]]
                            },
                        "alts": {
                            "enemySlots": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            "alternatives": {enc[0]: []},
                            "original": []
                            }
                        }

                log("End of add_custom_encounters")
            except Exception as e:
                error_popup(root, e)
                raise


        def set_bindings_buttons_menus(self, enable):
            """
            Sets keybindings to the appropriate function.
            Enables or disables buttons and menu items.

            Required Parameters:
                enable: Boolean
                    Whether to enable to disable bindings.
            """
            try:
                log("Start of set_bindings_buttons_menus: enable=" + str(enable))

                if enable:
                    enable_binding("Control-Key-1", lambda x: self.keybind_call("1"), root)
                    enable_binding("Control-Key-2", lambda x: self.keybind_call("2"), root)
                    enable_binding("Control-Key-3", lambda x: self.keybind_call("3"), root)
                    enable_binding("Control-Key-4", lambda x: self.keybind_call("4"), root)
                    enable_binding("Control-s", self.encounterTab.shuffle_enemies, root)
                    enable_binding("Control-c", self.campaignTab.add_card_to_campaign, root)
                    enable_binding("Control-q", lambda x: self.keybind_call("q"), root)
                    self.fileMenu.entryconfig("Random Level 1 Encounter", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Random Level 2 Encounter", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Random Level 3 Encounter", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Random Level 4 Encounter", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Shuffle Enemies", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Add to Campaign", state=tk.NORMAL)
                else:
                    enable_binding("Key-1", do_nothing, root)
                    enable_binding("Key-2", do_nothing, root)
                    enable_binding("Key-3", do_nothing, root)
                    enable_binding("Key-4", do_nothing, root)
                    enable_binding("s", do_nothing, root)
                    enable_binding("c", do_nothing, root)
                    self.fileMenu.entryconfig("Random Level 1 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Random Level 2 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Random Level 3 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Random Level 4 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Shuffle Enemies", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Add to Campaign", state=tk.DISABLED)

                if "level4" not in self.settings["encounterTypes"]:
                    self.fileMenu.entryconfig("Random Level 4 Encounter", state=tk.DISABLED)

                if ["level4"] == self.settings["encounterTypes"]:
                    self.fileMenu.entryconfig("Random Level 1 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Random Level 2 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Random Level 3 Encounter", state=tk.DISABLED)

                log("End of set_bindings_buttons_menus")
            except Exception as e:
                error_popup(root, e)
                raise


        def open_wiki(self):
            """
            Opens the wiki to the appropriate page.
            """
            try:
                log("Start of open_wiki")

                tab = self.notebook.tab(self.notebook.select(), "text")
                log("Opening https://github.com/DanDuhon/DSBG-Shuffle/wiki/" + tab)
                webbrowser.open_new("https://github.com/DanDuhon/DSBG-Shuffle/wiki/" + tab)
                
                log("End of open_wiki")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_buttons(self):
            """
            Create the buttons on the main screen.
            """
            try:
                log("Start of create_buttons")

                self.buttonsFrame = ttk.Frame(self)
                self.buttonsFrame.grid(row=0, column=0, pady=(10, 0), sticky="nw")
                self.buttonsFrame.columnconfigure(index=0, weight=1)
                self.campaignButton = ttk.Button(self.buttonsFrame, text="Add to Campaign", width=16, command=self.campaignTab.add_card_to_campaign)
                self.campaignButton.grid(column=0, row=1, padx=5, pady=5)

                # Link to the wiki
                wikiLink = ttk.Button(self.buttonsFrame, text="Open the wiki", width=16, command=self.open_wiki)
                wikiLink.grid(column=3, row=1)
                
                log("End of create_buttons")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_menu(self):
            """
            Create the menu.
            """
            try:
                log("Start of create_menu")

                menuBar = tk.Menu()
                self.fileMenu = tk.Menu(menuBar, tearoff=0)
                self.fileMenu.add_command(label="Random Level 1 Encounter", command=lambda x=1: self.encounterTab.random_encounter(level=x), accelerator="Ctrl+1")
                self.fileMenu.add_command(label="Random Level 2 Encounter", command=lambda x=2: self.encounterTab.random_encounter(level=x), accelerator="Ctrl+2")
                self.fileMenu.add_command(label="Random Level 3 Encounter", command=lambda x=3: self.encounterTab.random_encounter(level=x), accelerator="Ctrl+3")
                self.fileMenu.add_command(label="Random Level 4 Encounter", command=lambda x=4: self.encounterTab.random_encounter(level=x), accelerator="Ctrl+4")
                self.fileMenu.add_command(label="Shuffle Enemies", command=self.encounterTab.shuffle_enemies, accelerator="Ctrl+S")
                self.fileMenu.add_command(label="Add to Campaign", command=self.campaignTab.add_card_to_campaign, accelerator="Ctrl+C")
                self.fileMenu.add_separator()
                self.fileMenu.add_command(label="Quit", command=root.quit, accelerator="Ctrl+Q")
                menuBar.add_cascade(label="File", menu=self.fileMenu)

                self.optionsMenu = tk.Menu(menuBar, tearoff=0)
                self.optionsMenu.add_command(label="View/Change Settings", command=self.settings_window)
                menuBar.add_cascade(label="Settings", menu=self.optionsMenu)

                root.config(menu=menuBar)

                log("End of create_menu")
            except Exception as e:
                error_popup(root, e)
                raise


        def keybind_call(self, call, event=None):
            """
            Keyboard shortcuts.

            Required Parameters:
                call: String
                    The keybind activated.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of keybind_call: call=" + call)

                if call == "1" and self.settings["encounterTypes"] != ["level4"]:
                    self.encounterTab.random_encounter(level=1)
                elif call == "2" and self.settings["encounterTypes"] != ["level4"]:
                    self.encounterTab.random_encounter(level=2)
                elif call == "3" and self.settings["encounterTypes"] != ["level4"]:
                    self.encounterTab.random_encounter(level=3)
                elif call == "4" and "level4" in self.settings["encounterTypes"]:
                    self.encounterTab.random_encounter(level=4)
                elif call == "s":
                    self.encounterTab.shuffle_enemies()
                elif call == "c":
                    self.campaignTab.add_card_to_campaign()
                elif call == "q":
                    root.quit()

                log("End of keybind_call")
            except Exception as e:
                error_popup(root, e)
                raise


        def settings_window(self):
            """
            Show the settings window, where a user can change what expansions are active and
            whether random self.encounters show old, new, or both kinds of self.encounters.
            """
            try:
                log("Start of settings_window")

                self.set_bindings_buttons_menus(False)

                oldSettings = {k:v for k, v in self.settings.items()}
                oldTreasureSwapOption = self.settings["treasureSwapOption"]
                oldCustomEnemyList = self.settings["customEnemyList"]
                oldVariantEnable = self.settings["variantEnable"]
                oldCharactersActive = self.settings["charactersActive"]
                oldAvailableExpansions = self.settings["availableExpansions"]

                s = SettingsWindow(app, root, self.coreSets)

                self.wait_window(s.top)

                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep)) as settingsFile:
                    self.settings = load(settingsFile)

                if self.settings != oldSettings:
                    self.selected = None
                    self.rewardTreasure = None
                    self.displayTopLeft.config(image="")
                    self.displayTopLeft.image=None
                    self.displayTopRight.config(image="")
                    self.displayTopRight.image=None
                    self.displayBottomLeft.config(image="")
                    self.displayBottomLeft.image=None
                    self.displayBottomRight.config(image="")
                    self.displayBottomRight.image=None

                    self.displayImages = {
                        "encounters": {
                            self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                        },
                        "events": {
                            self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                        },
                        "variants": {
                            self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                        },
                        "variantsLocked": {
                            self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                        },
                        "behaviorDeck": {
                            self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                        }
                    }

                    self.encounterTab.treeviewEncounters.pack_forget()
                    self.encounterTab.treeviewEncounters.destroy()
                    self.availableExpansions = set(self.settings["availableExpansions"])
                    self.availableCoreSets = self.coreSets & self.availableExpansions
                    self.expansionsForRandomEncounters = self.allExpansions & ((self.v1Expansions if "v1" in self.settings["encounterTypes"] else set()) | (self.v2Expansions if "v2" in self.settings["encounterTypes"] else set()))
                    self.charactersActive = set(self.settings["charactersActive"])
                    self.numberOfCharacters = len(self.charactersActive)
                    self.encounterTab.set_encounter_list()
                    self.encounterTab.create_encounters_treeview()
                    self.variantsTab.reset_treeview()
                    self.behaviorDeckTab.reset_treeview()

                    self.bossMenuItems = [
                        "Select Boss",
                        "--Mini Bosses--"
                        ]
                    for boss in [boss for boss in bosses if bosses[boss]["level"] == "Mini Boss" and bosses[boss]["expansions"] & self.availableExpansions]:
                        self.bossMenuItems.append(bosses[boss]["name"])

                    self.bossMenuItems.append("--Main Bosses--")
                    for boss in [boss for boss in bosses if bosses[boss]["level"] == "Main Boss" and bosses[boss]["expansions"] & self.availableExpansions]:
                        self.bossMenuItems.append(bosses[boss]["name"])

                    self.bossMenuItems.append("--Mega Bosses--")
                    for boss in [boss for boss in bosses if bosses[boss]["level"] == "Mega Boss" and bosses[boss]["expansions"] & self.availableExpansions]:
                        self.bossMenuItems.append(bosses[boss]["name"])

                    self.campaignTab.bossMenu["values"] = self.bossMenuItems

                    self.campaignTab.selectedBoss.set("Select Boss")

                    # Recalculate the average soul cost of treasure.
                    if (self.settings["treasureSwapOption"] in {"Similar Soul Cost", "Tier Based"}
                        and (oldTreasureSwapOption != self.settings["treasureSwapOption"]
                            or oldCharactersActive != self.settings["charactersActive"]
                            or oldAvailableExpansions != self.settings["availableExpansions"])
                        ):
                        i = 0
                        progress = PopupWindow(root, labelText="Reloading treasure...", progressBar=True, progressMax=len([t for t in treasures if not treasures[t]["character"] or treasures[t]["character"] in self.charactersActive]), loadingImage=True)
                        i = generate_treasure_soul_cost(self.availableExpansions, self.charactersActive, root, progress)
                        if self.settings["treasureSwapOption"] == "Tier Based":
                            populate_treasure_tiers(self.availableExpansions, self.charactersActive)
                        progress.destroy()
                        
                    if self.settings["variantEnable"] == "on" and self.settings["variantEnable"] != oldVariantEnable:
                        if not self.variantsTab.variants:
                            self.variantsTab.load_enemy_variants(root=root, i=0, fromSettings=True)
                        self.notebook.tab(3, state=tk.NORMAL)
                    elif self.settings["variantEnable"] == "off":
                        self.notebook.tab(3, state=tk.DISABLED)
                        self.notebook.select(0)
                        self.variantsTab.currentVariants = {}
                        self.variantsTab.lockedVariants = {}
                        self.variantsTab.selectedVariant = None
                    
                    if oldCustomEnemyList != self.settings["customEnemyList"] and self.settings["customEnemyList"]:
                        i = 0
                        progress = PopupWindow(root, labelText="Applying custom enemy list...", progressBar=True, progressMax=len(self.encounterTab.encounterList), loadingImage=True)
                        
                        self.enabledEnemies = set([enemiesDict[enemy.replace(" (V1)", "")].id for enemy in self.settings["enabledEnemies"] if enemy not in self.allExpansions])

                        self.encountersToRemove = set()
                        for encounter in self.encounterTab.encounterList:
                            i += 1
                            progress.progressVar.set(i)
                            root.update_idletasks()
                            self.encounterTab.load_encounter(encounter=encounter, customEnemyListCheck=True)
                            if all([not set(alt).issubset(self.enabledEnemies) for alt in self.selected["alternatives"]]):
                                self.encountersToRemove.add(encounter)

                        self.encounterTab.encounterList = list(set(self.encounterTab.encounterList) - self.encountersToRemove)
                        
                        self.encounterTab.treeviewEncounters.pack_forget()
                        self.encounterTab.treeviewEncounters.destroy()
                        self.encounterTab.create_encounters_treeview()

                        progress.destroy()

                self.set_bindings_buttons_menus(True)
                
                if "level4" not in self.settings["encounterTypes"]:
                    self.encounterTab.l4["state"] = "disabled"
                else:
                    self.encounterTab.l4["state"] = "enabled"
                
                if ["level4"] == self.settings["encounterTypes"]:
                    self.encounterTab.l1["state"] = "disabled"
                    self.encounterTab.l2["state"] = "disabled"
                    self.encounterTab.l3["state"] = "disabled"
                else:
                    self.encounterTab.l1["state"] = "enabled"
                    self.encounterTab.l2["state"] = "enabled"
                    self.encounterTab.l3["state"] = "enabled"

                # Reset all behavior decks
                for enemy in self.behaviorDeckTab.decks:
                    if (
                        ((enemy[:enemy.index(" (")] if "Vordt" in enemy else enemy) in bosses
                            and bosses[(enemy[:enemy.index(" (")] if "Vordt" in enemy else enemy)]["expansions"] & self.availableExpansions)
                        or (enemy in enemiesDict
                            and enemiesDict[enemy].expansions & self.availableExpansions)
                        ):
                        self.behaviorDeckTab.set_decks(enemy, skipClear=True)

                log("End of settings_window")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_image(self, imageFileName, imageType, level=None, expansion=None, pathProvided=False, extensionProvided=False, customEncounter=False, emptySetIcon=False, addToBg1=False, addToBg2=False, progress=False):
            """
            Create an image to be displayed in the encounter frame.

            Required Parameters:
                imageFileName: String
                    The file name of the image, including extension but excluding path.

                imageType: String
                    The type of image, which will determine the dimensions used.

            Optional Parameters:
                level: Integer
                    The level of an encounter, which also determines the dimensions used.
                    Default: None

                expansion: String
                    The expansion of the encounter, used to determine whether the image is and
                    old or new style encounter. Determines dimensions used.
                    Default: None
            """
            try:
                log("Start of create_image, imageFileName={}, imageType={}, level={}, expansion={}".format(str(imageFileName), str(imageType), str(level), str(expansion)))

                if progress:
                    self.progress.progressVar.set(self.progress.progressVar.get()+1)
                    root.update_idletasks()

                if imageType in {"encounter", "customEncounter"}:
                    if imageFileName == "Ornstein & Smough.jpg" or imageFileName == "Ornstein & Smough - data.jpg":
                        width = 305
                        height = 850
                    elif level < 4 and expansion in {"Dark Souls The Board Game", "Iron Keep", "Darkroot", "Explorers", "Executioner Chariot"}:
                        width = 200
                        height = 300
                    elif level == 4:
                        width = 305
                        height = 424
                    else:
                        width = 400
                        height = 685

                    fileName = imageFileName[:-4] if not extensionProvided else imageFileName
                    if expansion == "The Sunless City" and imageFileName[:-4] in set(["Broken Passageway", "Central Plaza"]):
                        fileName += " (TSC)"
                    fileName += ".jpg" if not extensionProvided else ""

                    if pathProvided:
                        imagePath = fileName
                    elif customEncounter:
                        key = fileName[:-4]
                        fileNameCustom = fileName[:fileName.index(" (")].replace("Custom - ", "")
                        imagePath = baseFolder + "\\lib\\dsbg_shuffle_custom_encounters\\".replace("\\", pathSep) + self.encounters[key]["expansion"] + "_" + fileNameCustom + "_" + str(self.encounters[key]["level"]) + ".png"
                        if not os.path.exists(imagePath) and os.path.exists(imagePath.replace(".png", ".jpg")):
                            p = PopupWindow(root, "PNG format not found, but JPG was found.\nPlease re-save this encounter in the encounter builder,\na recent update improved image quality!", firstButton="Ok")
                            root.wait_window(p)
                            imagePath = imagePath.replace(".png", ".jpg")
                    elif "custom_encounter_" in fileName:
                        imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\custom_encounters\\".replace("\\", pathSep) + fileName
                    else:
                        imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\encounters\\".replace("\\", pathSep) + fileName
                    log("\tOpening " + imagePath)
                    self.displayImage = Image.open(imagePath).resize((width, height), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.displayImage)
                elif imageType == "event":
                    width = 305
                    height = 424
                        
                    fileName = imageFileName[:-4] if not extensionProvided else imageFileName
                    fileName += ".jpg" if not extensionProvided else ""

                    if pathProvided:
                        imagePath = fileName
                    else:
                        imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\events\\".replace("\\", pathSep) + fileName
                    log("\tOpening " + imagePath)
                    self.displayImage = Image.open(imagePath).resize((width, height), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.displayImage)
                elif imageType == "enemyCard":
                    width = 305
                    height = 424
                        
                    fileName = imageFileName[:-4] if not extensionProvided else imageFileName
                    if "Death Race" not in fileName:
                        fileName = fileName.replace(" 1", "").replace(" 2", "").replace(" 3", "").replace(" 4", "")
                    fileName += ".jpg" if not extensionProvided else ""

                    if pathProvided:
                        imagePath = fileName
                    else:
                        imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\enemies\\".replace("\\", pathSep) + fileName
                    log("\tOpening " + imagePath)
                    self.displayImage = Image.open(imagePath).resize((width, height), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.displayImage)
                elif imageType == "enemyText":
                    imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\enemies\\".replace("\\", pathSep) + imageFileName[:-4] + " rule bg.jpg"
                    log("\tOpening " + imagePath)
                    image = Image.open(imagePath).resize((14, 14), Image.Resampling.LANCZOS)
                elif imageType == "healthTracker":
                    imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\enemies\\".replace("\\", pathSep) + imageFileName
                    log("\tOpening " + imagePath)
                    self.displayImage = Image.open(imagePath).resize((102, 55), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.displayImage)
                elif imageType == "fourKingsHealth":
                    imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\enemies\\".replace("\\", pathSep) + imageFileName
                    log("\tOpening " + imagePath)
                    self.displayImage = Image.open(imagePath).resize((155, 55), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.displayImage)
                else:
                    if pathProvided:
                        imagePath = imageFileName
                    else:
                        subfolder = None

                        if imageType in {
                            "enemyOld",
                            "enemyOldLevel4",
                            "enemyNew",
                            "move",
                            "iconForCustomEnemy"
                        }:
                            subfolder = "enemies\\"
                        elif imageType in {
                            "aoeNode",
                            "destinationNode",
                            "enemyNode",
                            "attack",
                            "repeat",
                            "push",
                            "bleed",
                            "frostbite",
                            "poison",
                            "stagger",
                            "calamity",
                            "corrosion",
                            "terrain",
                            "iconForCustom"
                        }:
                            subfolder = "icons\\"
                        elif imageType in {
                            "barrage",
                            "bitterCold",
                            "darkness",
                            "eerie",
                            "gangAlonne",
                            "gangHollow",
                            "gangSilverKnight",
                            "gangSkeleton",
                            "hidden",
                            "illusion",
                            "mimic",
                            "onslaught",
                            "poisonMist",
                            "snowstorm",
                            "timer",
                            "trial"
                        }:
                            subfolder = "encounters\\"
                        elif imageType in {
                            "emptySetIcon",
                            "tileLayout",
                            "tileLayout1Tile",
                            "nodesStartingHorizontal1Tile",
                            "nodesStartingVertical1Tile",
                            "tileLayoutLevel4",
                            "nodesStartingHorizontalLevel4",
                            "nodesStartingVerticalLevel4",
                            "levelIcon",
                            "reward",
                            "layout",
                            "nodesLevel4Vertical",
                            "nodesLevel4Horizontal",
                            "nodes1TileVertical",
                            "nodes1TileHorizontal",
                            "nodesHorizontal",
                            "nodesVertical",
                            "tileNum",
                            "iconBg1",
                            "iconBg2",
                            "iconBg3"
                        }:
                            subfolder = "custom_encounters\\"

                        if subfolder:
                            imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\" + subfolder.replace("\\", pathSep) + imageFileName
                        else:
                            imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\".replace("\\", pathSep) + imageFileName

                    log("\tOpening " + imagePath)

                    if imageType == "enemyOld":
                        image = Image.open(imagePath).resize((27, 27), Image.Resampling.LANCZOS)
                    elif imageType == "enemyOldLevel4":
                        if "Phantoms" in enemiesDict[imageFileName[:-4]].expansions:
                            image = Image.open(imagePath).resize((34, 34), Image.Resampling.LANCZOS)
                        else:
                            image = Image.open(imagePath).resize((32, 32), Image.Resampling.LANCZOS)
                    elif imageType == "enemyNew":
                        image = Image.open(imagePath).resize((22, 22), Image.Resampling.LANCZOS)
                    elif imageType == "aoeNode":
                        image = Image.open(imagePath).resize((90, 90), Image.Resampling.LANCZOS)
                    elif imageType == "destinationNode":
                        image = Image.open(imagePath).resize((44, 44), Image.Resampling.LANCZOS)
                    elif imageType == "enemyNode":
                        image = Image.open(imagePath).resize((12, 12), Image.Resampling.LANCZOS)
                    elif imageType == "attack":
                        image = Image.open(imagePath).resize((85, 91), Image.Resampling.LANCZOS)
                    elif imageType == "move":
                        image = Image.open(imagePath).resize((75, 75), Image.Resampling.LANCZOS)
                    elif imageType == "repeat":
                        image = Image.open(imagePath).resize((48, 48), Image.Resampling.LANCZOS)
                    elif imageType == "push":
                        image = Image.open(imagePath).resize((26, 32), Image.Resampling.LANCZOS)
                    elif imageType == "bleed":
                        image = Image.open(imagePath).resize((18, 20), Image.Resampling.LANCZOS)
                    elif imageType == "frostbite":
                        image = Image.open(imagePath).resize((20, 20), Image.Resampling.LANCZOS)
                    elif imageType == "poison":
                        image = Image.open(imagePath).resize((15, 20), Image.Resampling.LANCZOS)
                    elif imageType == "stagger":
                        image = Image.open(imagePath).resize((19, 20), Image.Resampling.LANCZOS)
                    elif imageType == "calamity":
                        image = Image.open(imagePath).resize((20, 20), Image.Resampling.LANCZOS)
                    elif imageType == "corrosion":
                        image = Image.open(imagePath).resize((20, 20), Image.Resampling.LANCZOS)
                    elif imageType == "barrage":
                        image = Image.open(imagePath).resize((41, 13), Image.Resampling.LANCZOS)
                    elif imageType == "bitterCold":
                        image = Image.open(imagePath).resize((56, 13), Image.Resampling.LANCZOS)
                    elif imageType == "darkness":
                        image = Image.open(imagePath).resize((48, 13), Image.Resampling.LANCZOS)
                    elif imageType == "eerie":
                        image = Image.open(imagePath).resize((27, 13), Image.Resampling.LANCZOS)
                    elif imageType == "gangAlonne":
                        image = Image.open(imagePath).resize((67, 13), Image.Resampling.LANCZOS)
                    elif imageType == "gangHollow":
                        image = Image.open(imagePath).resize((69, 13), Image.Resampling.LANCZOS)
                    elif imageType == "gangSilverKnight":
                        image = Image.open(imagePath).resize((96, 13), Image.Resampling.LANCZOS)
                    elif imageType == "gangSkeleton":
                        image = Image.open(imagePath).resize((73, 13), Image.Resampling.LANCZOS)
                    elif imageType == "hidden":
                        image = Image.open(imagePath).resize((38, 13), Image.Resampling.LANCZOS)
                    elif imageType == "illusion":
                        image = Image.open(imagePath).resize((36, 13), Image.Resampling.LANCZOS)
                    elif imageType == "mimic":
                        image = Image.open(imagePath).resize((33, 13), Image.Resampling.LANCZOS)
                    elif imageType == "onslaught":
                        image = Image.open(imagePath).resize((54, 13), Image.Resampling.LANCZOS)
                    elif imageType == "poisonMist":
                        image = Image.open(imagePath).resize((61, 13), Image.Resampling.LANCZOS)
                    elif imageType == "snowstorm":
                        image = Image.open(imagePath).resize((56, 13), Image.Resampling.LANCZOS)
                    elif imageType == "timer":
                        image = Image.open(imagePath).resize((31, 13), Image.Resampling.LANCZOS)
                    elif imageType == "trial":
                        image = Image.open(imagePath).resize((26, 13), Image.Resampling.LANCZOS)
                    elif imageType == "tileLayout":
                        image = Image.open(imagePath).resize((235, 329), Image.Resampling.LANCZOS)
                    elif imageType == "tileLayout1Tile":
                        image = Image.open(imagePath).resize((235, 329), Image.Resampling.LANCZOS)
                    elif imageType == "nodesStartingHorizontal1Tile":
                        image = Image.open(imagePath).resize((80, 11), Image.Resampling.LANCZOS)
                    elif imageType == "nodesStartingVertical1Tile":
                        image = Image.open(imagePath).resize((10, 83), Image.Resampling.LANCZOS)
                    elif imageType == "tileLayoutLevel4":
                        image = Image.open(imagePath).resize((235, 329), Image.Resampling.LANCZOS)
                    elif imageType == "nodesStartingHorizontalLevel4":
                        image = Image.open(imagePath).resize((80, 11), Image.Resampling.LANCZOS)
                    elif imageType == "nodesStartingVerticalLevel4":
                        image = Image.open(imagePath).resize((10, 83), Image.Resampling.LANCZOS)
                    elif imageType == "levelIcon":
                        image = Image.open(imagePath).resize((63, 63), Image.Resampling.LANCZOS)
                    elif imageType == "reward":
                        image = Image.open(imagePath).resize((112, 111), Image.Resampling.LANCZOS)
                    elif imageType == "layout":
                        image = Image.open(imagePath).resize((235, 329), Image.Resampling.LANCZOS)
                    elif imageType == "nodesLevel4Vertical":
                        image = Image.open(imagePath).resize((16, 182), Image.Resampling.LANCZOS)
                    elif imageType == "nodesLevel4Horizontal":
                        image = Image.open(imagePath).resize((182, 16), Image.Resampling.LANCZOS)
                    elif imageType == "nodes1TileVertical":
                        image = Image.open(imagePath).resize((20, 161), Image.Resampling.LANCZOS)
                    elif imageType == "nodes1TileHorizontal":
                        image = Image.open(imagePath).resize((159, 20), Image.Resampling.LANCZOS)
                    elif imageType == "nodesHorizontal":
                        image = Image.open(imagePath).resize((81, 9), Image.Resampling.LANCZOS)
                    elif imageType == "nodesVertical":
                        image = Image.open(imagePath).resize((9, 82), Image.Resampling.LANCZOS)
                    elif imageType == "tileNum":
                        image = Image.open(imagePath).resize((40, 60), Image.Resampling.LANCZOS)
                    elif imageType == "terrain":
                        image = Image.open(imagePath).resize((21, 24), Image.Resampling.LANCZOS)
                    elif imageType in {"iconForCustom", "iconForCustomEnemy"}:
                        i, pi = self.create_image(imagePath, "iconText", 99, pathProvided=True, extensionProvided=True, progress=progress)
                        _, pibg1 = self.create_image(imagePath, "iconText", 99, pathProvided=True, extensionProvided=True, addToBg1=True, progress=progress)
                        _, pibg2 = self.create_image(imagePath, "iconText", 99, pathProvided=True, extensionProvided=True, addToBg2=True, progress=progress)
                        ti = self.create_image(imagePath, "iconTreeview", 99, pathProvided=True, extensionProvided=True, progress=progress)
                        return i, pi, pibg1, pibg2, ti
                    elif imageType == "iconTreeview":
                        i = Image.open(imagePath)
                        width, height = i.size
                        if width > height:
                            mod = 20 / width
                        else:
                            mod = 20 / height
                        img, _ = self.create_image("icon_background3.jpg", "iconBg3", 99, extensionProvided=True, progress=progress)
                        im = Image.open(imagePath).resize((int(width * mod), int(height * mod)), Image.Resampling.LANCZOS)
                        bgW, bgH = img.size
                        iW, iH = im.size
                        offset = ((bgW - iW) // 2, (bgH - iH) // 2)
                        img.paste(im=im, box=offset, mask=im)
                        log("\tEnd of create_image")
                        return ImageTk.PhotoImage(img)
                    elif imageType == "iconText":
                        i = Image.open(imagePath)
                        width, height = i.size
                        if width > height:
                            mod = 13 / width
                        else:
                            mod = 13 / height
                        if addToBg1:
                            img, _ = self.create_image("icon_background1.jpg", "iconBg1", 99, extensionProvided=True, progress=progress)
                        elif addToBg2:
                            img, _ = self.create_image("icon_background2.jpg", "iconBg2", 99, extensionProvided=True, progress=progress)
                        else:
                            img = Image.new("RGBA", (13, 13), (0, 0, 0, 0))
                        im = Image.open(imagePath).resize((int(width * mod), int(height * mod)), Image.Resampling.LANCZOS)
                        bgW, bgH = img.size
                        iW, iH = im.size
                        offset = ((bgW - iW) // 2, (bgH - iH) // 2)
                        img.paste(im=im, box=offset, mask=im)
                        log("\tEnd of create_image")
                        return img, ImageTk.PhotoImage(img)
                    elif imageType == "iconEnemy":
                        i = Image.open(imagePath)
                        width, height = i.size
                        if width > height:
                            mod = 22 / width
                        else:
                            mod = 22 / height
                        if addToBg1:
                            img, _ = self.create_image("icon_background1.jpg", "iconBg1", 99, extensionProvided=True, progress=progress)
                        elif addToBg2:
                            img, _ = self.create_image("icon_background2.jpg", "iconBg2", 99, extensionProvided=True, progress=progress)
                        else:
                            img = Image.new("RGBA", (22, 22), (0, 0, 0, 0))
                        im = Image.open(imagePath).resize((int(width * mod), int(height * mod)), Image.Resampling.LANCZOS)
                        bgW, bgH = img.size
                        iW, iH = im.size
                        offset = ((bgW - iW) // 2, (bgH - iH) // 2)
                        img.paste(im=im, box=offset, mask=im)
                        log("\tEnd of create_image")
                        return img, ImageTk.PhotoImage(img)
                    elif imageType == "iconSet":
                        x = 55 if not emptySetIcon else 58
                        y = 56 if not emptySetIcon else 59
                        i = Image.open(imagePath)
                        width, height = i.size
                        if width > height:
                            mod = x / width
                        else:
                            mod = y / height
                        if addToBg1:
                            img, _ = self.create_image("icon_background1.jpg", "iconBg1", 99, extensionProvided=True, progress=progress)
                        elif addToBg2:
                            img, _ = self.create_image("icon_background2.jpg", "iconBg2", 99, extensionProvided=True, progress=progress)
                        else:
                            img = Image.new("RGBA", (x, y), (0, 0, 0, 0))
                        im = Image.open(imagePath).resize((int(width * mod), int(height * mod)), Image.Resampling.LANCZOS)
                        bgW, bgH = img.size
                        iW, iH = im.size
                        offset = ((bgW - iW) // 2, (bgH - iH) // 2)
                        img.paste(im=im, box=offset, mask=im)
                        log("\tEnd of create_image")
                        return img, ImageTk.PhotoImage(img)
                    elif imageType == "iconBg1":
                        image = Image.open(imagePath).resize((242, 143), Image.Resampling.LANCZOS)
                        return image, ImageTk.PhotoImage(image)
                    elif imageType == "iconBg2":
                        image = Image.open(imagePath).resize((74, 75), Image.Resampling.LANCZOS)
                        return image, ImageTk.PhotoImage(image)
                    elif imageType == "iconBg3":
                        image = Image.open(imagePath).resize((20, 20), Image.Resampling.LANCZOS)
                        return image, ImageTk.PhotoImage(image)

                log("\tEnd of create_image")

                return image
            except UnidentifiedImageError:
                p = PopupWindow(root, "Invalid image file chosen.", firstButton="Ok")
                root.wait_window(p)
                raise
            except EnvironmentError as err:
                if err.errno == errno.ENOENT: # ENOENT -> "no entity" -> "file not found"
                    if customEncounter:
                        p = PopupWindow(root, "Custom encounter file not found.\nWas it deleted?", firstButton="Ok")
                        root.wait_window(p)
                raise
            except Exception as e:
                error_popup(root, e)
                raise


        def create_tooltip(self, tooltipDict, x, y, right=False):
            """
            Create a label and tooltip that will be placed and later removed.
            """
            try:
                log("Start of create_tooltip, tooltipDict={}, x={}, y={}".format(str(tooltipDict), str(x), str(y)))

                if self.forPrinting:
                    convertedImage = tooltipDict["image"].convert("RGBA")
                    self.displayImage.paste(im=convertedImage, box=(x, y), mask=convertedImage)
                else:
                    x += 410 if right else 0
                    label = tk.Label(self.displayFrame, image=tooltipDict["photo image"], borderwidth=0, highlightthickness=0)
                    self.tooltips.append(label)
                    label.place(x=x, y=y)
                    CreateToolTip(label, tooltipText[tooltipDict["imageName"]])

                log("\tEnd of create_tooltip")
            except Exception as e:
                error_popup(root, e)
                raise


    root = tk.Tk()
    root.withdraw()
    root.attributes("-alpha", 0.0)
        
    root.title("DSBG-Shuffle")
    root.tk.call("source", baseFolder + "\\Azure-ttk-theme-main\\azure.tcl".replace("\\", pathSep))
    root.tk.call("set_theme", "dark")
    root.iconphoto(True, tk.PhotoImage(file=os.path.join(baseFolder, "bonfire.png")))

    # Check for a new version
    today = datetime.datetime.today()
    with open(baseFolder + "\\lib\\dsbg_shuffle_version.txt".replace("\\", pathSep)) as vFile:
        version = vFile.readlines()
    if int(version[1]) != today.month:
        version[1] = today.month
        with open(os.path.join(baseFolder, "lib\\dsbg_shuffle_version.txt".replace("\\", pathSep)), "w") as v:
            v.write("\n".join([str(line).replace("\n", "") for line in version]))

        response = requests.get("https://api.github.com/repos/DanDuhon/DSBG-Shuffle/releases/latest")
        if version[0].replace("\n", "") != response.json()["name"]:
            p = PopupWindow(root, "A new version of DSBG-Shuffle is available!\nCurrent:\t"
                            + version[0].replace("\n", "")
                            + "\nNew:\t"
                            + response.json()["name"]
                            + "\nCheck it out on Github!\n\nIf you don't want to see this notification anymore,\ndisable checking for updates in the settings.", firstButton="Ok", secondButton=True)
            root.wait_window(p)

    s = ttk.Style()

    app = Application(root)
    app.pack(fill="both", expand=True)

    root.option_add("*TCombobox*Listbox*Background", "#181818")
    root.option_add("*TCombobox*Listbox.selectForeground", "white")

    center(root)
    root.attributes("-alpha", 1.0)
    root.mainloop()
    log("Closing application")
    root.destroy()

except Exception as e:
    error = str(sys.exc_info())
    if "application has been destroyed" not in error:
        log(error, exception=True)
        raise
