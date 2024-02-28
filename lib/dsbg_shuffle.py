try:
    import datetime
    import os
    import platform
    import requests
    import sys
    import tkinter as tk
    from collections import Counter
    from fpdf import FPDF
    from json import load, dump
    from PIL import Image, ImageTk, ImageFont, ImageDraw
    from os import path
    from random import choice, shuffle
    from tkinter import filedialog, ttk

    from dsbg_enemies import enemyIds, enemiesDict, bosses
    from dsbg_events import events
    from dsbg_settings import SettingsWindow
    from dsbg_tooltip_reference import tooltipText
    from dsbg_treasure import generate_treasure_soul_cost, populate_treasure_tiers, pick_treasure, treasureSwapEncounters, treasures
    from dsbg_utility import CreateToolTip, HelpWindow, PopupWindow, enable_binding, center, do_nothing, log, error_popup


    if platform.system() == "Windows":
        pathSep = "\\"
    else:
        pathSep = "/"

    baseFolder = path.dirname(__file__).replace("\\lib".replace("\\", pathSep), "")
    if platform.system() == "Windows":
        font = ImageFont.truetype(baseFolder + "\\lib\\Adobe Caslon Pro Semibold.ttf", 12)
    else:
        font = ImageFont.truetype("./Adobe Caslon Pro Semibold.ttf", 12)

    allEnemies = {enemy: {} for enemy in enemiesDict}

    with open(baseFolder + "\\lib\\dsbg_shuffle_encounters.json".replace("\\", pathSep)) as encountersFile:
        encounters = load(encountersFile)


    class Application(ttk.Frame):
        def __init__(self, parent):
            try:
                log("Initiating application")

                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep)) as settingsFile:
                    self.settings = load(settingsFile)

                if self.settings["theme"] == "light":
                    root.tk.call("set_theme", "light")

                self.selected = None
                self.allExpansions = set([encounters[encounter]["expansion"] for encounter in encounters]) | set(["Phantoms"])
                self.level4Expansions = set([encounters[encounter]["expansion"] for encounter in encounters if encounters[encounter]["level"] == 4])
                self.availableExpansions = set(self.settings["availableExpansions"])
                self.enabledEnemies = set([enemiesDict[enemy.replace(" (V1)", "")].id for enemy in self.settings["enabledEnemies"] if enemy not in self.allExpansions])
                if "Phantoms" in self.availableExpansions:
                    self.enabledEnemies = self.enabledEnemies.union(set([enemy for enemy in enemyIds if "Phantoms" in enemyIds[enemy].expansions]))
                self.charactersActive = set(self.settings["charactersActive"])
                self.numberOfCharacters = len(self.charactersActive)
                self.availableCoreSets = coreSets & self.availableExpansions

                self.v1Expansions = {"Dark Souls The Board Game", "Darkroot", "Executioner Chariot", "Explorers", "Iron Keep"}
                self.v2Expansions = (self.allExpansions - self.v1Expansions - self.level4Expansions)
                self.expansionsForRandomEncounters = ((self.v1Expansions if "v1" in self.settings["encounterTypes"] else set()) | (self.v2Expansions if "v2" in self.settings["encounterTypes"] else set()) | (self.level4Expansions if "Level 4 Encounters" in self.settings["availableExpansions"] else set())) & self.allExpansions
                self.set_encounter_list()

                root.withdraw()
                i = 0
                progress = PopupWindow(root, labelText="Praising the sun...", progressBar=True, progressMax=(len(allEnemies)*5) + len([t for t in treasures if not treasures[t]["character"] or treasures[t]["character"] in self.charactersActive]) + (len(self.encounterList) if self.settings["customEnemyList"] else 0), loadingImage=True)

                # Delete images from staging
                folder = baseFolder + "\\lib\\dsbg_shuffle_image_staging".replace("\\", pathSep)
                for filename in os.listdir(folder):
                    filePath = os.path.join(folder, filename)

                    if os.path.isfile(filePath) and filePath[-4:] == ".png":
                        os.unlink(filePath)

                ttk.Frame.__init__(self)
                self.grid_rowconfigure(index=1, weight=1)
                self.grid_rowconfigure(index=2, weight=0)
                self.encounterScrollbar = ttk.Scrollbar(root)
                self.encounterScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                self.bossMenu = [
                    "Select Boss",
                    "--Mini Bosses--"
                    ]
                for boss in [boss for boss in bosses if bosses[boss]["level"] == "Mini Boss"]:
                    self.bossMenu.append(bosses[boss]["name"])

                self.bossMenu.append("--Main Bosses--")
                for boss in [boss for boss in bosses if bosses[boss]["level"] == "Main Boss"]:
                    self.bossMenu.append(bosses[boss]["name"])

                self.bossMenu.append("--Mega Bosses--")
                for boss in [boss for boss in bosses if bosses[boss]["level"] == "Mega Boss"]:
                    self.bossMenu.append(bosses[boss]["name"])

                self.selectedBoss = tk.StringVar()
                
                self.currentEvent = None
                self.currentEventNum = 0
                self.eventDeck = []
                
                progress.label.config(text="Loading treasure...")
                if self.settings["treasureSwapOption"] in {"Similar Soul Cost", "Tier Based"}:
                    generate_treasure_soul_cost(self.availableExpansions, self.charactersActive, root, progress)
                i = len([t for t in treasures if not treasures[t]["character"] or treasures[t]["character"] in self.charactersActive])
                if self.settings["treasureSwapOption"] == "Tier Based":
                    populate_treasure_tiers(self.availableExpansions, self.charactersActive)

                self.create_buttons()
                self.create_tabs()
                self.scrollbarTreeviewEncounters = ttk.Scrollbar(self.encounterTab)
                self.scrollbarTreeviewEncounters.pack(side="right", fill="y")
                self.create_encounters_treeview()
                self.scrollbarTreeviewCampaign = ttk.Scrollbar(self.campaignTabTreeviewFrame)
                self.scrollbarTreeviewCampaign.pack(side="right", fill="y")
                self.create_campaign_treeview()
                self.scrollbarTreeviewEventList = ttk.Scrollbar(self.eventTabEventListTreeviewFrame)
                self.scrollbarTreeviewEventList.pack(side="right", fill="y")
                self.scrollbarTreeviewEventDeck = ttk.Scrollbar(self.eventTabEventDeckTreeviewFrame)
                self.scrollbarTreeviewEventDeck.pack(side="right", fill="y")
                self.create_event_treeviews()
                self.create_encounter_frame()
                self.create_menu()
                self.set_bindings_buttons_menus(True)

                self.forPrinting = False
                self.encountersToPrint = []

                self.campaign = []

                # Create images
                progress.label.config(text = "Loading images... ")
                # Enemies
                for enemy in allEnemies:
                    i += 5
                    progress.progressVar.set(i)
                    root.update_idletasks()
                    allEnemies[enemy]["imageOld"] = self.create_image(enemy + ".png", "enemyOld")
                    allEnemies[enemy]["imageOldLevel4"] = self.create_image(enemy + ".png", "enemyOldLevel4")
                    allEnemies[enemy]["imageNew"] = self.create_image(enemy + ".png", "enemyNew")
                    allEnemies[enemy]["image text"] = self.create_image(enemy + ".png", "enemyText")
                    allEnemies[enemy]["image text" if self.forPrinting else "photo image text"] = ImageTk.PhotoImage(self.create_image(enemy + ".png", "enemyText"))

                # If specific enemies (rather than just expansions) are toggled on or off, do extra work
                # to make sure all encounters are still valid.
                if self.settings["customEnemyList"]:
                    progress.label.config(text = "Applying custom enemy list...")
                    encountersToRemove = set()
                    for encounter in self.encounterList:
                        i += 1
                        progress.progressVar.set(i)
                        root.update_idletasks()
                        self.load_encounter(encounter=encounter, customEnemyListCheck=True)
                        if all([not set(alt).issubset(self.enabledEnemies) for alt in self.selected["alternatives"]]):
                            encountersToRemove.add(encounter)

                    self.encounterList = list(set(self.encounterList) - encountersToRemove)
                    
                    self.treeviewEncounters.pack_forget()
                    self.treeviewEncounters.destroy()
                    self.create_encounters_treeview()
                    self.scrollbarTreeviewCampaign = ttk.Scrollbar(self.campaignTabTreeviewFrame)
                    self.scrollbarTreeviewCampaign.pack(side="right", fill="y")

                progress.destroy()
                root.deiconify()

                # Icons
                self.enemyNode2 = self.create_image("enemy_node_2.png", "enemyNode")
                self.bleed = self.create_image("bleed.png", "condition")

                # Keywords
                self.barrage = self.create_image("barrage.png", "barrage")
                self.bitterCold = self.create_image("bitter_cold.png", "bitterCold")
                self.darkness = self.create_image("darkness.png", "darkness")
                self.eerie = self.create_image("eerie.png", "eerie")
                self.gangAlonne = self.create_image("gang_alonne.png", "gangAlonne")
                self.gangHollow = self.create_image("gang_hollow.png", "gangHollow")
                self.gangSilverKnight = self.create_image("gang_silver_knight.png", "gangSilverKnight")
                self.gangSkeleton = self.create_image("gang_skeleton.png", "gangSkeleton")
                self.gangAlonnePhoto = ImageTk.PhotoImage(self.gangAlonne)
                self.gangHollowPhoto = ImageTk.PhotoImage(self.gangHollow)
                self.gangSilverKnightPhoto = ImageTk.PhotoImage(self.gangSilverKnight)
                self.gangSkeletonPhoto = ImageTk.PhotoImage(self.gangSkeleton)
                self.hidden = self.create_image("hidden.png", "hidden")
                self.illusion = self.create_image("illusion.png", "illusion")
                self.mimic = self.create_image("mimic_keyword.png", "mimic")
                self.onslaught = self.create_image("onslaught.png", "onslaught")
                self.poisonMist = self.create_image("poison_mist.png", "poisonMist")
                self.snowstorm = self.create_image("snowstorm.png", "snowstorm")
                self.timer = self.create_image("timer.png", "timer")
                self.trial = self.create_image("trial.png", "trial")

                self.tooltips = []

                # What encounter have what special rules
                self.encounterTooltips = {
                    ("A Trusty Ally", "Tomb of Giants"): [
                        {"image": self.onslaught, "photo image": ImageTk.PhotoImage(self.onslaught), "imageName": "onslaught"}
                        ],
                    ("Abandoned and Forgotten", "Painted World of Ariamis"): [
                        {"image": self.eerie, "photo image": ImageTk.PhotoImage(self.eerie), "imageName": "eerie"}
                        ],
                    ("Aged Sentinel", "The Sunless City"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("Altar of Bones", "Tomb of Giants"): [
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"}
                        ],
                    ("Archive Entrance", "The Sunless City"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("Broken Passageway (TSC)", "The Sunless City"): [
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"},
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"}
                        ],
                    ("Castle Break In", "The Sunless City"): [
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"},
                        {},
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"}
                        ],
                    ("Central Plaza", "Painted World of Ariamis"): [
                        {"image": self.barrage, "photo image": ImageTk.PhotoImage(self.barrage), "imageName": "barrage"}
                        ],
                    ("Cold Snap", "Painted World of Ariamis"): [
                        {"image": self.snowstorm, "photo image": ImageTk.PhotoImage(self.snowstorm), "imageName": "snowstorm"},
                        {"image": self.bitterCold, "photo image": ImageTk.PhotoImage(self.bitterCold), "imageName": "bitterCold"},
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("Corrupted Hovel", "Painted World of Ariamis"): [
                        {"image": self.poisonMist, "photo image": ImageTk.PhotoImage(self.poisonMist), "imageName": "poisonMist"},
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("Corvian Host", "Painted World of Ariamis"): [
                        {"image": self.poisonMist, "photo image": ImageTk.PhotoImage(self.poisonMist), "imageName": "poisonMist"}
                        ],
                    ("Dark Resurrection", "Tomb of Giants"): [
                        {"image": self.darkness, "photo image": ImageTk.PhotoImage(self.darkness), "imageName": "darkness"}
                        ],
                    ("Deathly Freeze", "Painted World of Ariamis"): [
                        {"image": self.snowstorm, "photo image": ImageTk.PhotoImage(self.snowstorm), "imageName": "snowstorm"},
                        {"image": self.bitterCold, "photo image": ImageTk.PhotoImage(self.bitterCold), "imageName": "bitterCold"}
                        ],
                    ("Deathly Tolls", "The Sunless City"): [
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"},
                        {"image": self.mimic, "photo image": ImageTk.PhotoImage(self.mimic), "imageName": "mimic"},
                        {"image": self.onslaught, "photo image": ImageTk.PhotoImage(self.onslaught), "imageName": "onslaught"}
                        ],
                    ("Depths of the Cathedral", "The Sunless City"): [
                        {"image": self.mimic, "photo image": ImageTk.PhotoImage(self.mimic), "imageName": "mimic"}
                        ],
                    ("Distant Tower", "Painted World of Ariamis"): [
                        {"image": self.barrage, "photo image": ImageTk.PhotoImage(self.barrage), "imageName": "barrage"},
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("Eye of the Storm", "Painted World of Ariamis"): [
                        {"image": self.hidden, "photo image": ImageTk.PhotoImage(self.hidden), "imageName": "hidden"}
                        ],
                    ("Far From the Sun", "Tomb of Giants"): [
                        {"image": self.darkness, "photo image": ImageTk.PhotoImage(self.darkness), "imageName": "darkness"}
                        ],
                    ("Flooded Fortress", "The Sunless City"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("Frozen Revolutions", "Painted World of Ariamis"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("Frozen Sentries", "Painted World of Ariamis"): [
                        {"image": self.snowstorm, "photo image": ImageTk.PhotoImage(self.snowstorm), "imageName": "snowstorm"}
                        ],
                    ("Giant's Coffin", "Tomb of Giants"): [
                        {"image": self.onslaught, "photo image": ImageTk.PhotoImage(self.onslaught), "imageName": "onslaught"},
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"},
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"}
                        ],
                    ("Gleaming Silver", "The Sunless City"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"},
                        {"image": self.mimic, "photo image": ImageTk.PhotoImage(self.mimic), "imageName": "mimic"}
                        ],
                    ("Gnashing Beaks", "Painted World of Ariamis"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("Grim Reunion", "The Sunless City"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("Hanging Rafters", "The Sunless City"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"},
                        {"image": self.onslaught, "photo image": ImageTk.PhotoImage(self.onslaught), "imageName": "onslaught"}
                        ],
                    ("Illusionary Doorway", "The Sunless City"): [
                        {"image": self.illusion, "photo image": ImageTk.PhotoImage(self.illusion), "imageName": "illusion"}
                        ],
                    ("In Deep Water", "Tomb of Giants"): [
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"}
                        ],
                    ("Inhospitable Ground", "Painted World of Ariamis"): [
                        {"image": self.snowstorm, "photo image": ImageTk.PhotoImage(self.snowstorm), "imageName": "snowstorm"}
                        ],
                    ("Kingdom's Messengers", "The Sunless City"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("Lakeview Refuge", "Tomb of Giants"): [
                        {"image": self.onslaught, "photo image": ImageTk.PhotoImage(self.onslaught), "imageName": "onslaught"},
                        {"image": self.darkness, "photo image": ImageTk.PhotoImage(self.darkness), "imageName": "darkness"},
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("Last Rites", "Tomb of Giants"): [
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"}
                        ],
                    ("Last Shred of Light", "Tomb of Giants"): [
                        {"image": self.darkness, "photo image": ImageTk.PhotoImage(self.darkness), "imageName": "darkness"}
                        ],
                    ("No Safe Haven", "Painted World of Ariamis"): [
                        {"image": self.poisonMist, "photo image": ImageTk.PhotoImage(self.poisonMist), "imageName": "poisonMist"}
                        ],
                    ("Painted Passage", "Painted World of Ariamis"): [
                        {"image": self.snowstorm, "photo image": ImageTk.PhotoImage(self.snowstorm), "imageName": "snowstorm"}
                        ],
                    ("Parish Church", "The Sunless City"): [
                        {"image": self.mimic, "photo image": ImageTk.PhotoImage(self.mimic), "imageName": "mimic"},
                        {"image": self.illusion, "photo image": ImageTk.PhotoImage(self.illusion), "imageName": "illusion"},
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("Pitch Black", "Tomb of Giants"): [
                        {"image": self.darkness, "photo image": ImageTk.PhotoImage(self.darkness), "imageName": "darkness"}
                        ],
                    ("Promised Respite", "Painted World of Ariamis"): [
                        {"image": self.snowstorm, "photo image": ImageTk.PhotoImage(self.snowstorm), "imageName": "snowstorm"}
                        ],
                    ("Skeleton Overlord", "Tomb of Giants"): [
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"}
                        ],
                    ("Snowblind", "Painted World of Ariamis"): [
                        {"image": self.snowstorm, "photo image": ImageTk.PhotoImage(self.snowstorm), "imageName": "snowstorm"},
                        {"image": self.bitterCold, "photo image": ImageTk.PhotoImage(self.bitterCold), "imageName": "bitterCold"},
                        {"image": self.hidden, "photo image": ImageTk.PhotoImage(self.hidden), "imageName": "hidden"}
                        ],
                    ("Tempting Maw", "The Sunless City"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("The Beast From the Depths", "Tomb of Giants"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("The First Bastion", "Painted World of Ariamis"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("The Grand Hall", "The Sunless City"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"},
                        {"image": self.mimic, "photo image": ImageTk.PhotoImage(self.mimic), "imageName": "mimic"}
                        ],
                    ("The Last Bastion", "Painted World of Ariamis"): [
                        {"image": self.snowstorm, "photo image": ImageTk.PhotoImage(self.snowstorm), "imageName": "snowstorm"},
                        {"image": self.bitterCold, "photo image": ImageTk.PhotoImage(self.bitterCold), "imageName": "bitterCold"},
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("The Locked Grave", "Tomb of Giants"): [
                        {"image": self.trial, "photo image": ImageTk.PhotoImage(self.trial), "imageName": "trial"}
                        ],
                    ("The Mass Grave", "Tomb of Giants"): [
                        {"image": self.onslaught, "photo image": ImageTk.PhotoImage(self.onslaught), "imageName": "onslaught"},
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"},
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"},
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"}
                        ],
                    ("The Shine of Gold", "The Sunless City"): [
                        {"image": self.timer, "photo image": ImageTk.PhotoImage(self.timer), "imageName": "timer"}
                        ],
                    ("Trecherous Tower", "Painted World of Ariamis"): [
                        {"image": self.snowstorm, "photo image": ImageTk.PhotoImage(self.snowstorm), "imageName": "snowstorm"},
                        {"image": self.bitterCold, "photo image": ImageTk.PhotoImage(self.bitterCold), "imageName": "bitterCold"},
                        {"image": self.onslaught, "photo image": ImageTk.PhotoImage(self.eerie), "imageName": "eerie"}
                        ],
                    ("Twilight Falls", "The Sunless City"): [
                        {"image": self.illusion, "photo image": ImageTk.PhotoImage(self.illusion), "imageName": "illusion"}
                        ],
                    ("Undead Sanctum", "The Sunless City"): [
                        {"image": self.onslaught, "photo image": ImageTk.PhotoImage(self.onslaught), "imageName": "onslaught"}
                        ],
                    ("Unseen Scurrying", "Painted World of Ariamis"): [
                        {"image": self.hidden, "photo image": ImageTk.PhotoImage(self.hidden), "imageName": "hidden"}
                        ]
                }

                self.newEnemies = []
                self.newTiles = dict()
                self.rewardTreasure = None
            except Exception as e:
                error_popup(root, e)
                raise


        def on_frame_configure(self, canvas):
            """Reset the scroll region to encompass the inner frame"""
            canvas.configure(scrollregion=canvas.bbox("all"))


        def _bound_to_mousewheel(self, event):
            self.encounterCanvas.bind_all("<MouseWheel>", self._on_mousewheel)


        def _unbound_to_mousewheel(self, event):
            self.encounterCanvas.unbind_all("<MouseWheel>")


        def _on_mousewheel(self, event):
            self.encounterCanvas.yview_scroll(int(-1*(event.delta/120)), "units")


        def add_card_to_campaign(self, event=None):
            """
            Adds an encounter card to the campaign, visible in the campaign treeview.
            """
            try:
                log("Start of add_card_to_campaign")

                if self.notebook.tab(self.notebook.select(), "text") == "Events":
                    if not self.treeviewEventDeck.selection() and not self.treeviewEventList.selection():
                        log("End of add_card_to_campaign (nothing done)")
                        return
                    
                    eventToAdd = self.treeviewEventDeck.selection() if self.treeviewEventDeck.selection() else self.treeviewEventList.selection()
                    
                    # The underscore is used to denote multiple instances. Only the expansion parents don't have these.
                    # Also do nothing if you have multiple cards selected.
                    if len(eventToAdd) > 1 or "_" not in eventToAdd[0]:
                        log("End of add_card_to_campaign (nothing done)")
                        return
                    
                    eventToAdd = eventToAdd[0]

                    # Multiples need a different iid in the treeview, so append a number.
                    if eventToAdd + "_0" not in self.treeviewCampaign.get_children():
                        self.treeviewCampaign.insert(parent="", iid=eventToAdd + "_0", values=(eventToAdd[:eventToAdd.index("_")], "Event", ""), index="end")
                        iidSuffix = "_0"
                    else:
                        i = max([int(item[item.rindex("_") + 1:]) for item in self.treeviewCampaign.get_children() if item[:item.rindex("_")] == eventToAdd])
                        self.treeviewCampaign.insert(parent="", iid=eventToAdd + "_" + str(i+1), values=(eventToAdd[:eventToAdd.index("_")], "Event", ""), index="end")
                        iidSuffix = "_" + str(i+1)

                    # Build the dictionary that will be saved to JSON if this campaign is saved.
                    card = {
                        "type": "event",
                        "name": eventToAdd[:eventToAdd.index("_")],
                        "level": " ",
                        "iid": eventToAdd + iidSuffix
                    }

                    self.campaign.append(card)
                else:
                    if not self.selected:
                        log("End of add_card_to_campaign (nothing done)")
                        return

                    # Multiples need a different iid in the treeview, so append a number.
                    if self.selected["name"] + "_0" not in self.treeviewCampaign.get_children():
                        self.treeviewCampaign.insert(parent="", iid=self.selected["name"] + "_0", values=(self.selected["name"], "Encounter", self.selected["level"]), index="end")
                        iidSuffix = "_0"
                    else:
                        i = max([int(item[item.rindex("_") + 1:]) for item in self.treeviewCampaign.get_children() if item[:item.rindex("_")] == self.selected["name"]])
                        self.treeviewCampaign.insert(parent="", iid=self.selected["name"] + "_" + str(i+1), values=(self.selected["name"], "Encounter", self.selected["level"]), index="end")
                        iidSuffix = "_" + str(i+1)

                    # Build the dictionary that will be saved to JSON if this campaign is saved.
                    card = {
                        "type": "encounter",
                        "name": self.selected["name"] + (" (TSC)" if self.selected["expansion"] == "The Sunless City" and self.selected["name"] in set(["Broken Passageway", "Central Plaza"]) else ""),
                        "expansion": self.selected["expansion"],
                        "level": self.selected["level"],
                        "enemies": self.newEnemies,
                        "rewardTreasure": self.rewardTreasure,
                        "iid": self.selected["name"] + iidSuffix
                    }

                    self.campaign.append(card)

                log("End of add_card_to_campaign")
            except Exception as e:
                error_popup(root, e)
                raise


        def add_boss_to_campaign(self):
            """
            Adds a boss to the campaign, visible in the campaign treeview.
            """
            try:
                log("Start of add_boss_to_campaign")

                # If a menu item that isn't a boss (e.g. --Mini Boss--) is selected in the combobox, don't do anything.
                if self.selectedBoss.get() not in bosses:
                    log("End of add_boss_to_campaign (nothing done)")
                    return

                # Multiples need a different iid in the treeview, so append a number.
                if self.selectedBoss.get() + "_0" not in self.treeviewCampaign.get_children():
                    self.treeviewCampaign.insert(parent="", iid=self.selectedBoss.get() + "_0", values=(self.selectedBoss.get(), "Boss", bosses[self.selectedBoss.get()]["level"]), index="end")
                    iidSuffix = "_0"
                else:
                    i = max([int(item[item.rindex("_") + 1:]) for item in self.treeviewCampaign.get_children() if item[:item.rindex("_")] == self.selectedBoss.get()])
                    self.treeviewCampaign.insert(parent="", iid=self.selectedBoss.get() + "_" + str(i+1), values=(self.selectedBoss.get(), "Boss", bosses[self.selectedBoss.get()]["level"]), index="end")
                    iidSuffix = "_" + str(i+1)

                # Build the dictionary that will be saved to JSON if this campaign is saved.
                card = {
                    "name": self.selectedBoss.get(),
                    "type": "boss",
                    "level": bosses[self.selectedBoss.get()]["level"],
                    "iid": self.selectedBoss.get() + iidSuffix
                }

                self.campaign.append(card)

                log("End of add_boss_to_campaign")
            except Exception as e:
                error_popup(root, e)
                raise


        def delete_card_from_campaign(self, event=None):
            """
            Delete a card from the campaign.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of delete_card_from_campaign")

                # If the button is clicked with no selection, do nothing.
                if not self.treeviewCampaign.selection():
                    log("End of delete_card_from_campaign (nothing done)")
                    return

                # Remove the deleted cards from the campaign list and treeview.
                for item in self.treeviewCampaign.selection():
                    self.campaign = [c for c in self.campaign if c["iid"] != item]
                    self.treeviewCampaign.delete(item)

                # Remove the image displaying a deleted card.
                self.encounter.config(image="")

                log("End of delete_card_from_campaign")
            except Exception as e:
                error_popup(root, e)
                raise


        def save_campaign(self):
            """
            Save the campaign to a JSON file that can be loaded later.
            """
            try:
                log("Start of save_campaign")

                # Prompt user to save the file.
                campaignName = filedialog.asksaveasfile(mode="w", initialdir=baseFolder + "\\lib\\dsbg_shuffle_saved_campaigns".replace("\\", pathSep), defaultextension=".json")

                # If they canceled it, do nothing.
                if not campaignName:
                    log("End of save_campaign (nothing done)")
                    return

                with open(campaignName.name, "w") as campaignFile:
                    dump(self.campaign, campaignFile)

                log("End of save_campaign (saved to " + str(campaignFile) + ")")
            except Exception as e:
                error_popup(root, e)
                raise


        def load_campaign(self):
            """
            Load a campaign from a JSON file, clearing the current campaign treeview and replacing
            it with the data from the JSON file.
            """
            try:
                log("Start of load_campaign")

                # Prompt the user to find the campaign file.
                campaignFile = filedialog.askopenfilename(initialdir=baseFolder + "\\lib\\dsbg_shuffle_saved_campaigns".replace("\\", pathSep), filetypes = [(".json", ".json")])

                # If the user did not select a file, do nothing.
                if not campaignFile:
                    log("End of load_campaign (file dialog canceled)")
                    return

                # If the user did not select a JSON file, notify them that that was an invalid file.
                if os.path.splitext(campaignFile)[1] != ".json":
                    self.set_bindings_buttons_menus(False)
                    PopupWindow(self.master, labelText="Invalid DSBG-Shuffle campaign file.", firstButton="Ok")
                    self.set_bindings_buttons_menus(True)
                    log("End of load_campaign (invalid file)")
                    return

                log("Loading file " + campaignFile)

                with open(campaignFile, "r") as f:
                    self.campaign = load(f)

                # Check to see if there are any invalid names or levels in the JSON file.
                # This is about as sure as I can be that you can't load random JSON into the app.
                if any([(item["name"] not in encounters and item["name"] not in bosses and item["name"] not in events) or item["type"] not in set(["encounter", "boss", "event"]) or item["level"] not in set([1, 2, 3, 4, "Mini Boss", "Main Boss", "Mega Boss", " "]) for item in self.campaign]):
                    self.set_bindings_buttons_menus(False)
                    PopupWindow(self.master, labelText="Invalid DSBG-Shuffle campaign file.", firstButton="Ok")
                    self.set_bindings_buttons_menus(True)
                    self.campaign = []
                    log("End of load_campaign (invalid file)")
                    return

                # Remove existing campaign elements.
                for item in self.treeviewCampaign.get_children():
                    self.treeviewCampaign.delete(item)

                # Create the campaign from the campaign list.
                for item in self.campaign:
                    self.treeviewCampaign.insert(parent="", iid=item["iid"], values=(item["name"], item["type"][0].upper() + item["type"][1:], item["level"]), index="end")

                log("End of load_campaign (loaded from " + str(campaignFile) + ")")
            except Exception as e:
                error_popup(root, e)
                raise


        def move_up(self):
            """
            Move an item up in the campaign treeview, with corresponding movement in the campaign list.
            """
            try:
                log("Start of move_up")

                leaves = self.treeviewCampaign.selection()
                for i in leaves:
                    self.treeviewCampaign.move(i, self.treeviewCampaign.parent(i), self.treeviewCampaign.index(i) - 1)
                    self.campaign.insert(self.treeviewCampaign.index(i) + 1, self.campaign.pop(self.treeviewCampaign.index(i)))

                log("End of move_up")
            except Exception as e:
                error_popup(root, e)
                raise


        def move_down(self):
            """
            Move an item down in the campaign treeview, with corresponding movement in the campaign list.
            """
            try:
                log("Start of move_down")

                leaves = self.treeviewCampaign.selection()
                for i in reversed(leaves):
                    self.treeviewCampaign.move(i, self.treeviewCampaign.parent(i), self.treeviewCampaign.index(i) + 1)
                    self.campaign.insert(self.treeviewCampaign.index(i) - 1, self.campaign.pop(self.treeviewCampaign.index(i)))

                log("End of move_down")
            except Exception as e:
                error_popup(root, e)
                raise


        def load_campaign_card(self, event=None):
            """
            When an encounter in the campaign is clicked on, display the encounter
            and enemies that were originally saved.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of load_campaign_card")

                self.selected = None
                self.rewardTreasure = None
                self.encounter.unbind("<Button 1>")

                tree = event.widget

                # Don't update the image shown if you've selected more than one card.
                if len(tree.selection()) != 1:
                    log("End of load_campaign_card (not updating image)")
                    return
                
                # Remove keyword tooltips from the previous card shown, if there are any.
                for tooltip in self.tooltips:
                    tooltip.destroy()

                # Get the card selected.
                campaignCard = [e for e in self.campaign if e["iid"] == tree.selection()[0]][0]

                if campaignCard["type"] == "encounter":
                    self.rewardTreasure = campaignCard.get("rewardTreasure")

                    log("\tOpening " + baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + campaignCard["name"] + str(self.numberOfCharacters) + ".json")

                    # Get the enemy slots for this card.
                    with open(baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + campaignCard["name"] + str(self.numberOfCharacters) + ".json") as alternativesFile:
                        alts = load(alternativesFile)

                    # Create the encounter card with saved enemies and tooltips.
                    self.newEnemies = campaignCard["enemies"]
                    self.edit_encounter_card(campaignCard["name"], campaignCard["expansion"], campaignCard["level"], alts["enemySlots"])
                elif campaignCard["type"] == "boss":
                    # Create and display the boss image.
                    self.create_image(campaignCard["name"] + ".jpg", "encounter", 4)
                    self.encounterPhotoImage = ImageTk.PhotoImage(self.encounterImage)
                    self.encounter.image = self.encounterPhotoImage
                    self.encounter.config(image=self.encounterPhotoImage)
                elif campaignCard["type"] == "event":
                    self.load_event(campaign=True)

                log("End of load_campaign_card")
            except Exception as e:
                error_popup(root, e)
                raise


        def save_event_deck(self):
            """
            Save the event deck to a JSON file that can be loaded later.
            """
            try:
                log("Start of save_event_deck")

                # Prompt user to save the file.
                deckName = filedialog.asksaveasfile(mode="w", initialdir=baseFolder + "\\lib\\dsbg_shuffle_saved_event_decks".replace("\\", pathSep), defaultextension=".json")

                # If they canceled it, do nothing.
                if not deckName:
                    log("End of save_event_deck (nothing done)")
                    return
                
                deckData = [self.treeviewEventDeck.item(event) for event in self.treeviewEventDeck.get_children()]
                eventDeckCopy = [event for event in self.eventDeck]

                for item in deckData:
                    i = [event[:event.index("_")] for event in eventDeckCopy].index(item["values"][0])
                    item["eventDeckEntry"] = eventDeckCopy.pop(i)

                with open(deckName.name, "w") as deckFile:
                    dump(deckData, deckFile)

                log("End of save_event_deck (saved to " + str(deckFile) + ")")
            except Exception as e:
                error_popup(root, e)
                raise


        def load_event_deck(self):
            """
            Load an event deck from a JSON file, clearing the current deck treeview and replacing
            it with the data from the JSON file.
            """
            try:
                log("Start of load_event_deck")

                # Prompt the user to find the campaign file.
                deckFile = filedialog.askopenfilename(initialdir=baseFolder + "\\lib\\dsbg_shuffle_saved_event_decks".replace("\\", pathSep), filetypes = [(".json", ".json")])

                # If the user did not select a file, do nothing.
                if not deckFile:
                    log("End of load_event_deck (file dialog canceled)")
                    return
                
                # If the user did not select a JSON file, notify them that that was an invalid file.
                if os.path.splitext(deckFile)[1] != ".json":
                    self.set_bindings_buttons_menus(False)
                    PopupWindow(self.master, labelText="Invalid DSBG-Shuffle event deck file.", firstButton="Ok")
                    self.set_bindings_buttons_menus(True)
                    log("End of load_event_deck (invalid file)")
                    return
                
                log("Loading file " + deckFile)

                with open(deckFile, "r") as f:
                    self.deckData = load(f)

                # Check to see if there are any invalid names or levels in the JSON file.
                # This is about as sure as I can be that you can't load random JSON into the app.
                if any([
                    any([item["eventDeckEntry"][:item["eventDeckEntry"].index("_")] not in events for item in self.deckData]),
                    any([item["values"][0] not in events for item in self.deckData])
                    ]):
                    self.set_bindings_buttons_menus(False)
                    PopupWindow(self.master, labelText="Invalid DSBG-Shuffle event deck file.", firstButton="Ok")
                    self.set_bindings_buttons_menus(True)
                    log("End of load_event_deck (invalid file)")
                    return
                
                # Remove existing event deck elements.
                for item in self.treeviewEventDeck.get_children():
                    self.treeviewEventDeck.delete(item)

                # Create the event deck.
                self.eventDeck = [item["eventDeckEntry"] for item in self.deckData]
                for item in self.deckData:
                    self.treeviewEventDeck.insert(parent="", iid=item["eventDeckEntry"], values=item["values"], index="end")
                    if item["values"][1] and item["values"][1] > self.currentEventNum:
                        self.currentEventNum = item["values"][1]

                log("End of load_event_deck (loaded from " + str(deckFile) + ")")
            except Exception as e:
                error_popup(root, e)
                raise


        def sort_event_deck_treeview(self):
            try:
                log("Start of sort_event_deck_treeview")

                # Sort the event deck so that cards that have been drawn are at the top,
                # in order of most recently drawn.
                l = [(0 if not self.treeviewEventDeck.item(k)["values"][1] else self.treeviewEventDeck.item(k)["values"][1], k) for k in self.treeviewEventDeck.get_children()]
                l.sort(key=lambda x: (-x[0], x[1]))
                for index, (val, k) in enumerate(l):
                    self.treeviewEventDeck.move(k, "", index)

                log("End of sort_event_deck_treeview")
            except Exception as e:
                error_popup(root, e)
                raise


        def add_event_to_deck(self, event=None):
            """
            Adds an event card to the event deck, visible in the event deck treeview.
            """
            try:
                log("Start of add_event_to_deck")
                
                for selection in list(self.treeviewEventList.selection()):
                    eventSelected = self.treeviewEventList.item(selection)["values"][1 if self.treeviewEventList.item(selection)["values"][1] else 0]

                    # If an expansion is selected, add the events under that expansion.
                    if eventSelected in coreSets:
                        for event in self.treeviewEventList.get_children(eventSelected):
                            # Add an event for each copy of the card that exists.
                            for x in range(events[event[:event.index("_")]]["count"]):
                                if self.treeviewEventDeck.exists(event[:event.index("_")] + "_" + str(x)):
                                    continue
                                self.treeviewEventDeck.insert(parent="", iid=event[:event.index("_")] + "_" + str(x), values=(event[:event.index("_")], ""), index="end", tags=False)
                                self.eventDeck.append(event[:event.index("_")] + "_" + str(x))
                    else:
                        # Add an event for each copy of the card that exists.
                        for x in range(events[eventSelected]["count"]):
                            if self.treeviewEventDeck.exists(eventSelected + "_" + str(x)):
                                continue
                            self.treeviewEventDeck.insert(parent="", iid=eventSelected + "_" + str(x), values=(eventSelected, ""), index="end", tags=False)
                            self.eventDeck.append(eventSelected + "_" + str(x))

                self.sort_event_deck_treeview()

                shuffle(self.eventDeck)

                log("End of add_event_to_deck")
            except Exception as e:
                error_popup(root, e)
                raise


        def delete_event_from_deck(self, event=None):
            """
            Delete an event from the event deck.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of delete_event_from_deck")
                
                # If the button is clicked with no selection, do nothing.
                if not self.treeviewEventDeck.selection():
                    log("End of delete_event_from_deck (nothing done)")
                    return
                
                # Remove the deleted encounters from the treeview.
                for item in self.treeviewEventDeck.selection():
                    if self.treeviewEventDeck.item(item)["values"][1]:
                        self.currentEventNum -= 1
                        for event in self.treeviewEventDeck.get_children():
                            if self.treeviewEventDeck.item(event)["values"][1] and self.treeviewEventDeck.item(event)["values"][1] > self.treeviewEventDeck.item(item)["values"][1]:
                                self.treeviewEventDeck.item(event, values=(self.treeviewEventDeck.item(event)["values"][0], self.treeviewEventDeck.item(event)["values"][1] - 1))

                    self.treeviewEventDeck.delete(item)
                    self.eventDeck.remove(item)

                # Remove the image displaying a deleted encounter.
                self.encounter.config(image="")

                shuffle(self.eventDeck)

                log("End of delete_event_from_deck")
            except Exception as e:
                error_popup(root, e)
                raise


        def reset_event_deck(self, event=None):
            """
            Essentially shuffles all drawn cards back into the deck.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of reset_event_deck")
                
                # Set events to not be drawn yet.
                for item in self.treeviewEventDeck.get_children():
                    self.treeviewEventDeck.item(item, values=(self.treeviewEventDeck.item(item)["values"][0], ""))

                self.sort_event_deck_treeview()

                # Remove the image displaying a deleted encounter.
                self.encounter.config(image="")
                
                self.currentEvent = None
                self.currentEventNum = 0

                shuffle(self.eventDeck)

                log("End of reset_event_deck")
            except Exception as e:
                error_popup(root, e)
                raise


        def draw_from_event_deck(self, event=None):
            """
            "Draw" the top card from the virtual deck and display it.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of draw_from_event_deck")
                
                # If the button is clicked with no drawn event card, do nothing.
                if not self.eventDeck or not [eventCard for eventCard in self.eventDeck if not self.treeviewEventDeck.item(eventCard)["values"][1]]:
                    log("End of draw_from_event_deck (nothing done)")
                    return

                self.currentEvent = [eventCard for eventCard in self.eventDeck if not self.treeviewEventDeck.item(eventCard)["values"][1]][0]
                self.currentEventNum += 1
                self.load_event()
                self.treeviewEventDeck.item(self.currentEvent, values=(self.treeviewEventDeck.item(self.currentEvent)["values"][0], self.currentEventNum))

                self.sort_event_deck_treeview()

                log("End of draw_from_event_deck")
            except Exception as e:
                error_popup(root, e)
                raise


        def return_event_card_to_deck(self, event=None):
            """
            Shuffles the selected card back into the deck.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of return_event_card_to_deck")
                
                # If the button is clicked with no event card selected, do nothing.
                if not self.treeviewEventDeck.selection() or len(self.treeviewEventDeck.selection()) > 1:
                    log("End of return_event_card_to_deck (nothing done)")
                    return
                
                card = self.treeviewEventDeck.selection()[0]
                
                # If the button is clicked with no event card selected, do nothing.
                if not self.treeviewEventDeck.item(card)["values"][1]:
                    log("End of return_event_card_to_deck (nothing done)")
                    return

                shuffle(self.eventDeck)
                self.encounter.config(image="")
                # Reduce the Drawn Order value of more recently drawn cards by 1.
                for eventCard in self.treeviewEventDeck.get_children():
                    if self.treeviewEventDeck.item(eventCard)["values"][1] and self.treeviewEventDeck.item(eventCard)["values"][1] > self.treeviewEventDeck.item(card)["values"][1]:
                        self.treeviewEventDeck.item(eventCard, values=(self.treeviewEventDeck.item(eventCard)["values"][0], self.treeviewEventDeck.item(eventCard)["values"][1]-1))
                self.treeviewEventDeck.item(card, values=(self.treeviewEventDeck.item(card)["values"][0], ""))
                self.currentEvent = None
                self.currentEventNum -= 1

                self.sort_event_deck_treeview()

                shuffle(self.eventDeck)

                log("End of return_event_card_to_deck")
            except Exception as e:
                error_popup(root, e)
                raise


        def return_event_card_to_bottom(self, event=None):
            """
            Puts the selected card on the bottom of the virtual deck.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of return_event_card_to_bottom")
                
                # If the button is clicked with no event card selected, do nothing.
                if not self.treeviewEventDeck.selection() or len(self.treeviewEventDeck.selection()) > 1:
                    log("End of return_event_card_to_bottom (nothing done)")
                    return
                
                card = self.treeviewEventDeck.selection()[0]
                
                # If the button is clicked with no event card selected, do nothing.
                if not self.treeviewEventDeck.item(card)["values"][1]:
                    log("End of return_event_card_to_deck (nothing done)")
                    return

                self.eventDeck.remove(card)
                self.eventDeck.append(card)
                self.encounter.config(image="")
                # Reduce the Drawn Order value of more recently drawn cards by 1.
                for eventCard in self.treeviewEventDeck.get_children():
                    if self.treeviewEventDeck.item(eventCard)["values"][1] and self.treeviewEventDeck.item(eventCard)["values"][1] > self.treeviewEventDeck.item(card)["values"][1]:
                        self.treeviewEventDeck.item(eventCard, values=(self.treeviewEventDeck.item(eventCard)["values"][0], self.treeviewEventDeck.item(eventCard)["values"][1]-1))
                self.treeviewEventDeck.item(card, values=(self.treeviewEventDeck.item(card)["values"][0], ""))
                self.currentEvent = None
                self.currentEventNum -= 1

                self.sort_event_deck_treeview()

                log("End of return_event_card_to_bottom")
            except Exception as e:
                error_popup(root, e)
                raise

        def return_event_card_to_top(self, event=None):
            """
            Puts the selected card on the top of the virtual deck.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of return_event_card_to_top")
                
                # If the button is clicked with no event card selected, do nothing.
                if not self.treeviewEventDeck.selection() or len(self.treeviewEventDeck.selection()) > 1:
                    log("End of return_event_card_to_top (nothing done)")
                    return
                
                card = self.treeviewEventDeck.selection()[0]
                
                # If the button is clicked with no event card selected, do nothing.
                if not self.treeviewEventDeck.item(card)["values"][1]:
                    log("End of return_event_card_to_deck (nothing done)")
                    return

                self.eventDeck.remove(card)
                self.eventDeck.insert(0, card)
                self.encounter.config(image="")
                # Reduce the Drawn Order value of more recently drawn cards by 1.
                for eventCard in self.treeviewEventDeck.get_children():
                    if self.treeviewEventDeck.item(eventCard)["values"][1] and self.treeviewEventDeck.item(eventCard)["values"][1] > self.treeviewEventDeck.item(card)["values"][1]:
                        self.treeviewEventDeck.item(eventCard, values=(self.treeviewEventDeck.item(eventCard)["values"][0], self.treeviewEventDeck.item(eventCard)["values"][1]-1))
                self.treeviewEventDeck.item(card, values=(self.treeviewEventDeck.item(card)["values"][0], ""))
                self.currentEvent = None
                self.currentEventNum -= 1

                self.sort_event_deck_treeview()

                log("End of return_event_card_to_top")
            except Exception as e:
                error_popup(root, e)
                raise


        def print_encounters(self):
            """
            Export campaign encounters to a PDF.
            """
            try:
                log("Start of print_encounters")

                self.forPrinting = True
                self.encountersToPrint = []
                campaignEncounters = [e for e in self.campaign if e["name"] not in bosses]

                for encounter in campaignEncounters:
                    # Skip event cards
                    if encounter["type"] != "encounter":
                        continue

                    # These are the card sizes in mm
                    if encounter["expansion"] in {
                        "Dark Souls The Board Game",
                        "Darkroot",
                        "Executioner Chariot",
                        "Explorers",
                        "Iron Keep",
                        "Asylum Demon",
                        "Black Dragon Kalameet",
                        "Gaping Dragon",
                        "Guardian Dragon",
                        "Manus, Father of the Abyss",
                        "Old Iron King",
                        "The Four Kings",
                        "The Last Giant",
                        "Vordt of the Boreal Valley"}:
                        if encounter["level"] == 4:
                            encounter["width"] = 63
                            encounter["height"] = 88
                        else:
                            encounter["width"] = 42
                            encounter["height"] = 63
                    else:
                        encounter["width"] = 70
                        encounter["height"] = 120

                # Add cards to a list associated with their type/size.
                encounterCount = 0
                eCount = 0
                v1Normal = []
                l = [e for e in campaignEncounters if e["type"] == "encounter" and e["width"] == 42]
                for i in range(0, len(l), 18):
                    v1Normal.append(l[i:i+18])
                    encounterCount += len(l[i:i+18])

                v1Level4 = []
                l = [e for e in campaignEncounters if e["type"] == "encounter" and e["width"] == 63]
                for i in range(0, len(l), 9):
                    v1Level4.append(l[i:i+9])
                    encounterCount += len(l[i:i+9])

                v2 = []
                l = [e for e in campaignEncounters if e["type"] == "encounter" and e["width"] == 70]
                for i in range(0, len(l), 6):
                    v2.append(l[i:i+6])
                    encounterCount += len(l[i:i+6])

                encountersToPrint = [v1Normal, v1Level4, v2]

                buffer = 5
                pdf = FPDF(unit="mm")
                pdf.set_margins(buffer, buffer, buffer)

                progress = PopupWindow(root, labelText="Creating a PDF...", progressBar=True, progressMax=encounterCount, loadingImage=True)

                # Loop through the card lists and add them to pages.
                for e, encounterList in enumerate(encountersToPrint):
                    if e == 0:
                        standardCards = 11
                        columnBreaks = {3, 7, 11}
                    elif e == 1:
                        standardCards = 8
                        columnBreaks = {2, 5}
                    elif e == 2:
                        standardCards = 1
                        columnBreaks = {1}
                        buffer = 3

                    for page in encounterList:
                        pdf.add_page()
                        x = buffer
                        y = buffer
                        pdf.set_x(x)
                        pdf.set_y(y)

                        for i, encounter in enumerate(page):
                            # Get the encounter.
                            campaignEncounter = [e for e in self.campaign if e["name"] == encounter["name"]]
                            self.rewardTreasure = campaignEncounter[0].get("rewardTreasure")

                            log("\tOpening " + baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + campaignEncounter[0]["name"] + str(self.numberOfCharacters) + ".json")
                            # Get the enemy slots for this encounter.
                            with open(baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + campaignEncounter[0]["name"] + str(self.numberOfCharacters) + ".json") as alternativesFile:
                                alts = load(alternativesFile)

                            # Create the encounter card with saved enemies and tooltips.
                            self.newEnemies = campaignEncounter[0]["enemies"]
                            self.edit_encounter_card(campaignEncounter[0]["name"], campaignEncounter[0]["expansion"], campaignEncounter[0]["level"], alts["enemySlots"])

                            # Stage the encounter image
                            log("\tStaging " + encounter["name"] + ", level " + str(encounter["level"]) + " from " + encounter["expansion"])
                            imageStage = ImageTk.getimage(self.encounterPhotoImage)

                            if i > standardCards:
                                imageStage = imageStage.rotate(90, Image.NEAREST, expand=1)
                            imageStage.save(baseFolder + "\\lib\\dsbg_shuffle_image_staging\\".replace("\\", pathSep) + encounter["name"] + ".png")

                            log("\tAdding " + encounter["name"] + " to PDF at (" + str(x) + ", " + str(y) + ") with width of " + str(encounter["width" if not i > standardCards else "height"]))
                            pdf.image(baseFolder + "\\lib\\dsbg_shuffle_image_staging\\".replace("\\", pathSep) + encounter["name"] + ".png", x=x, y=y, type="PNG", w=encounter["width" if not i > standardCards else "height"])

                            if i < standardCards:
                                if i in columnBreaks:
                                    x += encounter["width"] + buffer
                                    y = buffer
                                else:
                                    y += encounter["height"] + buffer
                            elif i == standardCards:
                                x += encounter["width"] + buffer
                                y = buffer
                            else:
                                y += encounter["width"] + buffer

                            eCount += 1
                            progress.progressVar.set(eCount)
                            root.update_idletasks()

                progress.destroy()

                # Prompt user to save the file.
                pdfOutput = filedialog.asksaveasfile(mode="w", initialdir=baseFolder + "\\lib\\dsbg_shuffle_pdfs".replace("\\", pathSep), defaultextension=".pdf")

                # If they canceled it, do nothing.
                if not pdfOutput:
                    log("End of print_encounters (nothing done)")
                    return
                
                progress = PopupWindow(root, labelText="Saving PDF, please wait...", loadingImage=True)

                pdf.output(pdfOutput.name)

                progress.destroy()

                self.forPrinting = False

                log("End of print_encounters")
            except Exception as e:
                error_popup(root, e)
                raise


        def set_encounter_list(self):
            """
            Sets of the list of available encounters in the encounter tab based on what
            the user selected in the settings.
            """
            try:
                log("Start of set_encounter_list")

                # Set the list of encounters based on available expansions.
                self.encounterList = [encounter for encounter in encounters if (
                    all([
                        any([frozenset(expCombo).issubset(self.availableExpansions) for expCombo in encounters[encounter]["expansionCombos"]["1"]]),
                        any([frozenset(expCombo).issubset(self.availableExpansions) for expCombo in encounters[encounter]["expansionCombos"]["2"]]),
                        True if "3" not in encounters[encounter]["expansionCombos"] else any([frozenset(expCombo).issubset(self.availableExpansions) for expCombo in encounters[encounter]["expansionCombos"]["3"]]),
                        encounters[encounter]["expansion"] in ((self.v1Expansions if "v1" in self.settings["encounterTypes"] else set()) | (self.v2Expansions if "v2" in self.settings["encounterTypes"] else set()) | (self.level4Expansions if "level4" in self.settings["encounterTypes"] else set()))
                            ]))]

                log("End of set_encounter_list")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_tabs(self, event=None):
            """
            Create the encounter and campaign tabs in the main window.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of create_tabs")

                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep)) as settingsFile:
                    self.settings = load(settingsFile)

                self.paned = ttk.PanedWindow(self)
                self.paned.grid_rowconfigure(index=0, weight=1)
                self.paned.grid(row=1, column=0, pady=(5, 5), padx=(5, 5), sticky="nsew", columnspan=4)

                self.pane = ttk.Frame(self.paned, padding=5)
                self.pane.grid_rowconfigure(index=0, weight=1)
                self.paned.add(self.pane, weight=1)

                self.notebook = ttk.Notebook(self.paned)
                self.notebook.pack(fill="both", expand=True)

                self.encounterTab = ttk.Frame(self.notebook)
                for index in [0, 1]:
                    self.encounterTab.columnconfigure(index=index, weight=1)
                    self.encounterTab.rowconfigure(index=index, weight=1)
                self.notebook.add(self.encounterTab, text="Encounters")

                self.campaignTab = ttk.Frame(self.notebook)
                self.notebook.add(self.campaignTab, text="Campaign")
                self.campaignTabButtonsFrame = ttk.Frame(self.campaignTab)
                self.campaignTabButtonsFrame.pack()
                self.campaignTabButtonsFrame2 = ttk.Frame(self.campaignTab)
                self.campaignTabButtonsFrame2.pack()
                self.campaignTabTreeviewFrame = ttk.Frame(self.campaignTab)
                self.campaignTabTreeviewFrame.pack(fill="both", expand=True)

                self.deleteButton = ttk.Button(self.campaignTabButtonsFrame, text="Remove Card", width=16, command=self.delete_card_from_campaign)
                self.deleteButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.printEncounters = ttk.Button(self.campaignTabButtonsFrame, text="Export to PDF", width=16, command=self.print_encounters)
                self.printEncounters.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.moveUpButton = ttk.Button(self.campaignTabButtonsFrame, text="Move Up", width=16, command=self.move_up)
                self.moveUpButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.moveDownButton = ttk.Button(self.campaignTabButtonsFrame, text="Move Down", width=16, command=self.move_down)
                self.moveDownButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

                self.loadButton = ttk.Button(self.campaignTabButtonsFrame2, text="Load Campaign", width=16, command=self.load_campaign)
                self.loadButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.saveButton = ttk.Button(self.campaignTabButtonsFrame2, text="Save Campaign", width=16, command=self.save_campaign)
                self.saveButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.bossMenu = ttk.Combobox(self.campaignTabButtonsFrame2, state="readonly", values=self.bossMenu, textvariable=self.selectedBoss)
                self.bossMenu.current(0)
                self.bossMenu.config(width=17)
                self.bossMenu.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.addBossButton = ttk.Button(self.campaignTabButtonsFrame2, text="Add Boss", width=16, command=self.add_boss_to_campaign)
                self.addBossButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                
                self.eventTab = ttk.Frame(self.notebook)
                self.notebook.add(self.eventTab, text="Events")
                self.eventTabButtonsFrame = ttk.Frame(self.eventTab)
                self.eventTabButtonsFrame.pack()
                self.eventTabEventListTreeviewFrame = ttk.Frame(self.eventTab)
                self.eventTabEventListTreeviewFrame.pack(fill="both", expand=True)
                self.eventTabButtonsFrame2 = ttk.Frame(self.eventTab)
                self.eventTabButtonsFrame2.pack()
                self.eventTabButtonsFrame3 = ttk.Frame(self.eventTab)
                self.eventTabButtonsFrame3.pack()
                self.eventTabEventDeckTreeviewFrame = ttk.Frame(self.eventTab)
                self.eventTabEventDeckTreeviewFrame.pack(fill="both", expand=True)
                self.eventTabDeckFrame = ttk.Frame(self.eventTab)
                self.eventTabDeckFrame.pack(fill="both", expand=True)
                
                self.addEventButton = ttk.Button(self.eventTabButtonsFrame, text="Add Event(s)", width=16, command=self.add_event_to_deck)
                self.addEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

                self.deleteEventButton = ttk.Button(self.eventTabButtonsFrame2, text="Remove Event", width=16, command=self.delete_event_from_deck)
                self.deleteEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.resetEventButton = ttk.Button(self.eventTabButtonsFrame2, text="Reset Event Deck", width=16, command=self.reset_event_deck)
                self.resetEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.loadEventDeckButton = ttk.Button(self.eventTabButtonsFrame2, text="Load Event Deck", width=16, command=self.load_event_deck)
                self.loadEventDeckButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.saveEventDeckButton = ttk.Button(self.eventTabButtonsFrame2, text="Save Event Deck", width=16, command=self.save_event_deck)
                self.saveEventDeckButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                
                self.drawEventButton = ttk.Button(self.eventTabButtonsFrame3, text="Draw Event Card", width=16, command=self.draw_from_event_deck)
                self.drawEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.shuffleEventButton = ttk.Button(self.eventTabButtonsFrame3, text="Shuffle Into Deck", width=16, command=self.return_event_card_to_deck)
                self.shuffleEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.bottomEventButton = ttk.Button(self.eventTabButtonsFrame3, text="Return To Bottom", width=16, command=self.return_event_card_to_bottom)
                self.bottomEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.topEventButton = ttk.Button(self.eventTabButtonsFrame3, text="Return To Top", width=16, command=self.return_event_card_to_top)
                self.topEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

                log("End of create_tabs")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_encounters_treeview(self):
            """
            Create the encounters treeview, where a user can select an encounter
            and shuffle the enemies in it.
            """
            try:
                log("Start of create_encounters_treeview")

                self.treeviewEncounters = ttk.Treeview(
                    self.encounterTab,
                    selectmode="browse",
                    columns=("Name"),
                    yscrollcommand=self.scrollbarTreeviewEncounters.set,
                    height=29 if root.winfo_screenheight() > 1000 else 20
                )

                self.treeviewEncounters.pack(expand=True, fill="both")
                self.scrollbarTreeviewEncounters.config(command=self.treeviewEncounters.yview)

                self.treeviewEncounters.column("#0", anchor="w")
                self.treeviewEncounters.heading("#0", text="  Name", anchor="w")

                # Sort encounters by:
                # 1. Encounters that have more than just level 4 encounters first
                # 2. New core sets first
                # 3. V2 non-core sets
                # 4. Original core set
                # 5. Executioner Chariot at the top of the mega bosses list because it has non-level 4 encounters
                # 6. By level
                # 7. Alphabetically
                encountersSorted = [encounter for encounter in sorted(self.encounterList, key=lambda x: (
                    1 if encounters[x]["level"] == 4 else 0,
                    0 if encounters[x]["expansion"] in coreSets and encounters[x]["expansion"] in self.v2Expansions else 1,
                    0 if encounters[x]["expansion"] in self.v2Expansions else 1,
                    1 if encounters[x]["expansion"] == "Executioner Chariot" else 0,
                    encounters[x]["expansion"],
                    encounters[x]["level"],
                    encounters[x]["name"]))]
                tvData = []
                tvParents = dict()
                x = 0
                for e in encountersSorted:
                    if encounters[e]["expansion"] not in [t[2] for t in tvData]:
                        tvData.append(("", x, encounters[e]["expansion"], False))
                        tvParents[encounters[e]["expansion"]] = {"exp": tvData[-1][1]}
                        x += 1

                    if encounters[e]["expansion"] == "Executioner Chariot" and encounters[e]["level"] < 4 and "v1"not in self.settings["encounterTypes"]:
                        continue

                    if encounters[e]["level"] == 4 and "level4" not in self.settings["encounterTypes"]:
                        continue
                    
                    if encounters[e]["level"] < 4 and ["level4"] == self.settings["encounterTypes"]:
                        continue

                    if encounters[e]["level"] not in tvParents[encounters[e]["expansion"]]:
                        tvData.append((tvParents[encounters[e]["expansion"]]["exp"], x, "Level " + str(encounters[e]["level"]), False))
                        tvParents[encounters[e]["expansion"]][encounters[e]["level"]] = tvData[-1][1]
                        x += 1

                    tvData.append((tvParents[encounters[e]["expansion"]][encounters[e]["level"]], x, e, True))
                    x += 1

                for item in tvData:
                    self.treeviewEncounters.insert(parent=item[0], index="end", iid=item[1], text=item[2], tags=item[3])

                    if item[0] == "":
                        self.treeviewEncounters.item(item[1], open=True)

                self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)

                log("End of create_encounters_treeview")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_campaign_treeview(self):
            """
            Create the campaign treeview where users can see saved encounters they've selected.
            """
            try:
                log("Start of create_campaign_treeview")

                self.treeviewCampaign = ttk.Treeview(
                    self.campaignTabTreeviewFrame,
                    selectmode="extended",
                    columns=("Name", "Type", "Level"),
                    yscrollcommand=self.scrollbarTreeviewCampaign.set,
                    height=29 if root.winfo_screenheight() > 1000 else 20,
                    show=["headings"]
                )

                self.treeviewCampaign.pack(expand=True, fill="both")
                self.scrollbarTreeviewCampaign.config(command=self.treeviewCampaign.yview)

                self.treeviewCampaign.column("Name", anchor="w")
                self.treeviewCampaign.heading("Name", text="Name", anchor="w")
                self.treeviewCampaign.column("Type", anchor="w")
                self.treeviewCampaign.heading("Type", text="Type", anchor="w")
                self.treeviewCampaign.column("Level", anchor="w")
                self.treeviewCampaign.heading("Level", text="Level", anchor="w")

                self.treeviewCampaign.bind("<<TreeviewSelect>>", self.load_campaign_card)
                self.treeviewCampaign.bind("<Control-a>", lambda *args: self.treeviewCampaign.selection_add(self.treeviewCampaign.get_children()))

                log("End of create_campaign_treeview")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_event_treeviews(self):
            """
            Create the event list and event deck treeviews where users can see event cards.
            """
            try:
                log("Start of create_event_treeviews")
                
                self.treeviewEventList = ttk.Treeview(
                    self.eventTabEventListTreeviewFrame,
                    selectmode="extended",
                    columns=("Event List", "Name", "Count"),
                    yscrollcommand=self.scrollbarTreeviewEventList.set,
                    height=12 if root.winfo_screenheight() > 1000 else 10
                )
                
                self.treeviewEventList.pack(expand=True, fill="both")
                self.scrollbarTreeviewEventList.config(command=self.treeviewEventList.yview)

                minwidth = self.treeviewEventList.column('#0', option='minwidth')
                self.treeviewEventList.column('#0', width=minwidth)

                self.treeviewEventList.heading("Event List", text="Event List", anchor=tk.W)
                self.treeviewEventList.heading("Name", text="Name", anchor=tk.W)
                self.treeviewEventList.heading("Count", text="Count", anchor=tk.W)
                self.treeviewEventList.column("Event List", anchor=tk.W, width=150)
                self.treeviewEventList.column("Name", anchor=tk.W, width=180)
                self.treeviewEventList.column("Count", anchor=tk.W, width=98)
                
                self.treeviewEventList.bind("<<TreeviewSelect>>", self.load_event)
                self.treeviewEventList.bind("<Control-a>", lambda *args: self.treeviewEventList.selection_add(self.treeviewEventList.get_children()))

                for coreSet in sorted(coreSets - set(["Dark Souls The Board Game"])):
                    self.treeviewEventList.insert(parent="", iid=coreSet, values=(coreSet, "", ""), index="end", tags=False)
                    for event in [event for event in events if coreSet in events[event]["expansions"]]:
                        self.treeviewEventList.insert(parent=coreSet, iid=event + "_" + coreSet, values=("", event, events[event]["count"]), index="end", tags=True)
                
                self.treeviewEventDeck = ttk.Treeview(
                    self.eventTabEventDeckTreeviewFrame,
                    selectmode="extended",
                    columns=("Event Deck", "Drawn Order"),
                    yscrollcommand=self.scrollbarTreeviewEventDeck.set,
                    height=12 if root.winfo_screenheight() > 1000 else 10
                )
                
                self.treeviewEventDeck.pack(expand=True, fill="both")
                self.scrollbarTreeviewEventDeck.config(command=self.treeviewEventDeck.yview)

                minwidth = self.treeviewEventDeck.column('#0', option='minwidth')
                self.treeviewEventDeck.column('#0', width=minwidth)

                self.treeviewEventDeck.heading("Event Deck", text="Event Deck", anchor=tk.W)
                self.treeviewEventDeck.heading("Drawn Order", text="Drawn Order", anchor=tk.W)
                self.treeviewEventDeck.column("Event Deck", anchor=tk.W, width=180)
                self.treeviewEventDeck.column("Drawn Order", anchor=tk.W, width=248)
                
                self.treeviewEventDeck.bind("<<TreeviewSelect>>", self.load_event)
                self.treeviewEventDeck.bind("<Control-a>", lambda *args: self.treeviewEventDeck.selection_add(self.treeviewEventDeck.get_children()))

                log("End of create_event_treeviews")
            except Exception as e:
                error_popup(root, e)
                raise


        def load_event(self, event=None, campaign=False):
            try:
                log("Start of load_event")
                
                # Get the event selected.
                if event:
                    tree = event.widget

                    # Don't update the image shown if you've selected more than one encounter.
                    if len(tree.selection()) != 1:
                        log("End of load_event (not updating image)")
                        return
                    
                    if tree == self.treeviewEventList and len(self.treeviewEventDeck.selection()) > 0:
                        for selection in self.treeviewEventDeck.selection():
                            self.treeviewEventDeck.selection_remove(selection)
                    elif tree == self.treeviewEventDeck and len(self.treeviewEventList.selection()) > 0:
                        for selection in self.treeviewEventList.selection():
                            self.treeviewEventList.selection_remove(selection)
                    
                    eventSelected = tree.selection()[0]
                elif campaign:
                    eventSelected = self.treeviewCampaign.selection()[0]
                else:
                    eventSelected = self.currentEvent

                if "_" in eventSelected:
                    eventSelected = eventSelected[:eventSelected.index("_")]

                if eventSelected not in events:
                    log("End of load_event (core set selected)")
                    return

                # Remove keyword tooltips from the previous image shown, if there are any.
                for tooltip in self.tooltips:
                    tooltip.destroy()

                # Create and display the event image.
                self.create_image(events[eventSelected]["name"] + ".jpg", "encounter", 4)
                self.encounterPhotoImage = ImageTk.PhotoImage(self.encounterImage)
                self.encounter.image = self.encounterPhotoImage
                self.encounter.config(image=self.encounterPhotoImage)

                log("End of load_event")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_encounter_frame(self):
            """
            Create the frame in which encounters will be displayed.
            """
            try:
                log("Start of create_encounter_frame")

                self.encounterCanvas = tk.Canvas(self, width=410, yscrollcommand=self.encounterScrollbar.set)
                self.encounterFrame = ttk.Frame(self.encounterCanvas)
                self.encounterFrame.columnconfigure(index=0, weight=1, minsize=410)
                self.encounterCanvas.grid(row=0, column=4, padx=10, pady=(10, 0), sticky="nsew", rowspan=2)
                self.encounterCanvas.create_window((0,0), window=self.encounterFrame, anchor=tk.NW)
                self.encounterScrollbar.config(command=self.encounterCanvas.yview)
                self.encounterFrame.bind("<Enter>", self._bound_to_mousewheel)
                self.encounterFrame.bind("<Leave>", self._unbound_to_mousewheel)
                self.encounterFrame.bind("<Configure>", lambda event, canvas=self.encounterCanvas: self.on_frame_configure(canvas))

                self.encounter = ttk.Label(self.encounterFrame)
                self.encounter.grid(column=0, row=0, sticky="nsew")

                log("End of create_encounter_frame")
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
                    enable_binding("Key-1", lambda x: self.keybind_call("1"), root)
                    enable_binding("Key-2", lambda x: self.keybind_call("2"), root)
                    enable_binding("Key-3", lambda x: self.keybind_call("3"), root)
                    enable_binding("Key-4", lambda x: self.keybind_call("4"), root)
                    enable_binding("s", self.shuffle_enemies, root)
                    enable_binding("c", self.add_card_to_campaign, root)
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


        def create_buttons(self):
            """
            Create the buttons on the main screen.
            """
            try:
                log("Start of create_buttons")

                self.buttonsFrame = ttk.Frame(self)
                self.buttonsFrame.grid(row=0, column=0, pady=(10, 0), sticky="nw")
                self.buttonsFrame.columnconfigure(index=0, weight=1)

                self.buttons = set()
                self.l1 = ttk.Button(self.buttonsFrame, text="Random Level 1", width=16, command=lambda x=1: self.random_encounter(level=x))
                self.l2 = ttk.Button(self.buttonsFrame, text="Random Level 2", width=16, command=lambda x=2: self.random_encounter(level=x))
                self.l3 = ttk.Button(self.buttonsFrame, text="Random Level 3", width=16, command=lambda x=3: self.random_encounter(level=x))
                self.l4 = ttk.Button(self.buttonsFrame, text="Random Level 4", width=16, command=lambda x=4: self.random_encounter(level=x))
                if "level4" not in self.settings["encounterTypes"]:
                    self.l4["state"] = "disabled"
                if ["level4"] == self.settings["encounterTypes"]:
                    self.l1["state"] = "disabled"
                    self.l2["state"] = "disabled"
                    self.l3["state"] = "disabled"
                self.l5 = ttk.Button(self.buttonsFrame, text="Add to Campaign", width=16, command=self.add_card_to_campaign)
                self.buttons.add(self.l1)
                self.buttons.add(self.l2)
                self.buttons.add(self.l3)
                self.buttons.add(self.l4)
                self.buttons.add(self.l5)
                self.l1.grid(column=0, row=0, padx=5)
                self.l2.grid(column=1, row=0, padx=5)
                self.l3.grid(column=2, row=0, padx=5)
                self.l4.grid(column=3, row=0, padx=5)
                self.l5.grid(column=0, row=1, padx=5, pady=5)

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
                self.fileMenu.add_command(label="Random Level 1 Encounter", command=lambda x=1: self.random_encounter(level=x), accelerator="1")
                self.fileMenu.add_command(label="Random Level 2 Encounter", command=lambda x=2: self.random_encounter(level=x), accelerator="2")
                self.fileMenu.add_command(label="Random Level 3 Encounter", command=lambda x=3: self.random_encounter(level=x), accelerator="3")
                self.fileMenu.add_command(label="Random Level 4 Encounter", command=lambda x=4: self.random_encounter(level=x), accelerator="4")
                self.fileMenu.add_command(label="Shuffle Enemies", command=self.shuffle_enemies, accelerator="s")
                self.fileMenu.add_command(label="Add to Campaign", command=self.add_card_to_campaign, accelerator="c")
                self.fileMenu.add_separator()
                self.fileMenu.add_command(label="Quit", command=root.quit, accelerator="Ctrl+Q")
                menuBar.add_cascade(label="File", menu=self.fileMenu)

                self.optionsMenu = tk.Menu(menuBar, tearoff=0)
                self.optionsMenu.add_command(label="View/Change Settings", command=self.settings_window)
                menuBar.add_cascade(label="Settings", menu=self.optionsMenu)

                self.helpMenu = tk.Menu(menuBar, tearoff=0)
                self.helpMenu.add_command(label="How to use ", command=self.help_window)
                menuBar.add_cascade(label="Help", menu=self.helpMenu)

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
                    self.random_encounter(level=1)
                elif call == "2" and self.settings["encounterTypes"] != ["level4"]:
                    self.random_encounter(level=2)
                elif call == "3" and self.settings["encounterTypes"] != ["level4"]:
                    self.random_encounter(level=3)
                elif call == "4" and "level4" in self.settings["encounterTypes"]:
                    self.random_encounter(level=4)
                elif call == "s":
                    self.shuffle_enemies()
                elif call == "c":
                    self.add_card_to_campaign()
                elif call == "q":
                    root.quit()

                log("End of keybind_call")
            except Exception as e:
                error_popup(root, e)
                raise


        def settings_window(self):
            """
            Show the settings window, where a user can change what expansions are active and
            whether random encounters show old, new, or both kinds of encounters.
            """
            try:
                log("Start of settings_window")

                self.set_bindings_buttons_menus(False)

                oldSettings = {k:v for k, v in self.settings.items()}
                oldTreasureSwapOption = self.settings["treasureSwapOption"]
                oldCustomEnemyList = self.settings["customEnemyList"]

                s = SettingsWindow(root, coreSets)

                self.wait_window(s.top)

                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep)) as settingsFile:
                    self.settings = load(settingsFile)

                if self.settings != oldSettings and self.treeviewEncounters.winfo_exists():
                    self.selected = None
                    self.rewardTreasure = None
                    self.encounter.config(image="")
                    self.treeviewEncounters.pack_forget()
                    self.treeviewEncounters.destroy()
                    self.availableExpansions = set(self.settings["availableExpansions"])
                    self.availableCoreSets = coreSets & self.availableExpansions
                    self.expansionsForRandomEncounters = self.allExpansions & ((self.v1Expansions if "v1" in self.settings["encounterTypes"] else set()) | (self.v2Expansions if "v2" in self.settings["encounterTypes"] else set()))
                    self.charactersActive = set(self.settings["charactersActive"])
                    self.numberOfCharacters = len(self.charactersActive)
                    self.set_encounter_list()
                    self.create_encounters_treeview()

                    # Recalculate the average soul cost of treasure.
                    if (oldTreasureSwapOption != self.settings["treasureSwapOption"] and self.settings["treasureSwapOption"] in {"Similar Soul Cost", "Tier Based"}) or (oldCustomEnemyList != self.settings["customEnemyList"] and self.settings["customEnemyList"]):
                        i = 0
                        progress = PopupWindow(root, labelText="Reloading treasure...", progressBar=True, progressMax=(len([t for t in treasures if not treasures[t]["character"] or treasures[t]["character"] in self.charactersActive]) if oldTreasureSwapOption != self.settings["treasureSwapOption"] and self.settings["treasureSwapOption"] in {"Similar Soul Cost", "Tier Based"} else 0) + (len(self.encounterList) if oldCustomEnemyList != self.settings["customEnemyList"] and self.settings["customEnemyList"] else 0), loadingImage=True)
                        if oldTreasureSwapOption != self.settings["treasureSwapOption"] and self.settings["treasureSwapOption"] in {"Similar Soul Cost", "Tier Based"}:
                            i = generate_treasure_soul_cost(self.availableExpansions, self.charactersActive, root, progress)
                            if self.settings["treasureSwapOption"] == "Tier Based":
                                populate_treasure_tiers(self.availableExpansions, self.charactersActive)
                    
                        if oldCustomEnemyList != self.settings["customEnemyList"] and self.settings["customEnemyList"]:
                            progress.label.config(text = "Applying custom enemy list...")

                            self.enabledEnemies = set([enemiesDict[enemy.replace(" (V1)", "")].id for enemy in self.settings["enabledEnemies"] if enemy not in self.allExpansions])
                            if "Phantoms" in self.availableExpansions:
                                self.enabledEnemies = self.enabledEnemies.union(set([enemy for enemy in enemyIds if "Phantoms" in enemyIds[enemy].expansions]))

                            encountersToRemove = set()
                            for encounter in self.encounterList:
                                i += 1
                                progress.progressVar.set(i)
                                root.update_idletasks()
                                self.load_encounter(encounter=encounter, customEnemyListCheck=True)
                                if all([not set(alt).issubset(self.enabledEnemies) for alt in self.selected["alternatives"]]):
                                    encountersToRemove.add(encounter)

                            self.encounterList = list(set(self.encounterList) - encountersToRemove)
                            
                            self.treeviewEncounters.pack_forget()
                            self.treeviewEncounters.destroy()
                            self.create_encounters_treeview()
                            self.scrollbarTreeviewCampaign = ttk.Scrollbar(self.campaignTabTreeviewFrame)
                            self.scrollbarTreeviewCampaign.pack(side="right", fill="y")

                        progress.destroy()

                self.set_bindings_buttons_menus(True)
                
                if "level4" not in self.settings["encounterTypes"]:
                    self.l4["state"] = "disabled"
                else:
                    self.l4["state"] = "enabled"
                
                if ["level4"] == self.settings["encounterTypes"]:
                    self.l1["state"] = "disabled"
                    self.l2["state"] = "disabled"
                    self.l3["state"] = "disabled"
                else:
                    self.l1["state"] = "enabled"
                    self.l2["state"] = "enabled"
                    self.l3["state"] = "enabled"

                log("End of settings_window")
            except Exception as e:
                error_popup(root, e)
                raise


        def help_window(self):
            """
            Display the help window, which shows basic usage information.
            """
            try:
                log("Start of settings_window")

                self.set_bindings_buttons_menus(False)
                h = HelpWindow(root)
                self.wait_window(h.top)
                self.set_bindings_buttons_menus(True)

                log("End of settings_window")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_image(self, imageFileName, imageType, level=None, expansion=None):
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
                log("Start of create_image")

                if imageType == "encounter":
                    if imageFileName == "Ornstein and Smough.jpg":
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

                    fileName = imageFileName[:-4]
                    if expansion == "The Sunless City" and imageFileName[:-4] in set(["Broken Passageway", "Central Plaza"]):
                        fileName += " (TSC)"
                    fileName += ".jpg"

                    imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\".replace("\\", pathSep) + fileName
                    log("\tOpening " + imagePath)
                    self.encounterImage = Image.open(imagePath).resize((width, height), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.encounterImage)
                elif imageType == "enemyText":
                    imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\".replace("\\", pathSep) + imageFileName[:-4] + " rule bg.jpg"
                    log("\tOpening " + imagePath)
                    image = Image.open(imagePath).resize((14, 14), Image.Resampling.LANCZOS)
                else:
                    imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\".replace("\\", pathSep) + imageFileName
                    log("\tOpening " + imagePath)

                    if imageType == "enemyOld":
                        image = Image.open(imagePath).resize((27, 27), Image.Resampling.LANCZOS)
                    elif imageType == "enemyOldLevel4":
                        if "Phantoms" in enemiesDict[imageFileName[:-4]].expansions:
                            image = Image.open(imagePath).resize((38, 38), Image.Resampling.LANCZOS)
                        else:
                            image = Image.open(imagePath).resize((32, 32), Image.Resampling.LANCZOS)
                    elif imageType == "enemyNew":
                        image = Image.open(imagePath).resize((22, 22), Image.Resampling.LANCZOS)
                    elif imageType == "resurrection":
                        image = Image.open(imagePath).resize((9, 17), Image.Resampling.LANCZOS)
                    elif imageType == "playerCount":
                        image = Image.open(imagePath).resize((12, 12), Image.Resampling.LANCZOS)
                    elif imageType == "enemyNode":
                        image = Image.open(imagePath).resize((12, 12), Image.Resampling.LANCZOS)
                    elif imageType == "condition":
                        image = Image.open(imagePath).resize((13, 13), Image.Resampling.LANCZOS)
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

                log("\tEnd of create_image")

                return image
            except Exception as e:
                error_popup(root, e)
                raise


        def random_encounter(self, event=None, level=None):
            """
            Picks a random encounter from the list of available encounters and displays it.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
                    Default: None

                level: Integer
                    The level of the encounter.
                    Default: None
            """
            try:
                log("Start of random_encounter")

                self.load_encounter(encounter=choice([encounter for encounter in self.encounterList if (
                    encounters[encounter]["level"] == level
                    and (encounters[encounter]["expansion"] in self.expansionsForRandomEncounters
                        or encounters[encounter]["level"] == 4))]))

                log("\tEnd of random_encounter")
            except Exception as e:
                error_popup(root, e)
                raise


        def load_encounter(self, event=None, encounter=None, customEnemyListCheck=False):
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
            try:
                log("Start of load_encounter")

                if not customEnemyListCheck:
                    self.treeviewEncounters.unbind("<<TreeviewSelect>>")

                # If this encounter was clicked on, get that information.
                if event:
                    tree = event.widget
                    if not tree.item(tree.selection())["tags"][0]:
                        log("\tNo encounter selected")
                        self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)
                        log("\tEnd of load_encounter")
                        return
                    encounterName = tree.item(tree.selection())["text"]
                else:
                    encounterName = encounter

                    # If the encounter clicked on is already displayed, no need to load it again,
                    # just shuffle the enemies.
                    if encounters[encounterName] == self.selected:
                        self.shuffle_enemies()
                        self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)
                        log("\tEnd of load_encounter")
                        return

                self.selected = encounters[encounterName]

                # Get the possible alternative enemies from the encounter's file.
                log("\tOpening " + baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + encounterName + str(self.numberOfCharacters) + ".json")
                with open(baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + encounterName + str(self.numberOfCharacters) + ".json") as alternativesFile:
                    alts = load(alternativesFile)

                self.selected["alternatives"] = []
                self.selected["enemySlots"] = alts["enemySlots"]

                # Use only alternative enemies for expansions and enemies the user has activated in the settings.
                if "1" in alts["alternatives"]:
                    if "1" in alts["alternatives"]:
                        self.selected["alternatives"] = {"1": []}
                        for expansionCombo in alts["alternatives"]["1"]:
                            if set(expansionCombo.split(",")).issubset(self.availableExpansions):
                                self.selected["alternatives"]["1"] += [alt for alt in alts["alternatives"]["1"][expansionCombo] if set(alt).issubset(self.enabledEnemies) and [enemyIds[a].expansions for a in alt].count(set(["Phantoms"])) <= self.settings["maxInvaders"]]
                    if "2" in alts["alternatives"]:
                        self.selected["alternatives"]["2"] = []
                        for expansionCombo in alts["alternatives"].get("2", []):
                            if set(expansionCombo.split(",")).issubset(self.availableExpansions):
                                self.selected["alternatives"]["2"] += [alt for alt in alts["alternatives"]["2"][expansionCombo] if set(alt).issubset(self.enabledEnemies) and [enemyIds[a].expansions for a in alt].count(set(["Phantoms"])) <= self.settings["maxInvaders"]]
                    if "3" in alts["alternatives"]:
                        self.selected["alternatives"]["3"] = []
                        for expansionCombo in alts["alternatives"].get("3", []):
                            if set(expansionCombo.split(",")).issubset(self.availableExpansions):
                                self.selected["alternatives"]["3"] += [alt for alt in alts["alternatives"]["3"][expansionCombo] if set(alt).issubset(self.enabledEnemies) and [enemyIds[a].expansions for a in alt].count(set(["Phantoms"])) <= self.settings["maxInvaders"]]
                else:
                    for expansionCombo in alts["alternatives"]:
                        if set(expansionCombo.split(",")).issubset(self.availableExpansions):
                            self.selected["alternatives"] += [alt for alt in alts["alternatives"][expansionCombo] if set(alt).issubset(self.enabledEnemies) and [enemyIds[a].expansions for a in alt].count(set(["Phantoms"])) <= self.settings["maxInvaders"]]

                self.newTiles = dict()

                if not customEnemyListCheck:
                    self.shuffle_enemies()
                    self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)
                    self.encounter.bind("<Button 1>", self.shuffle_enemies)

                log("\tEnd of load_encounter")
            except Exception as e:
                error_popup(root, e)
                raise


        def shuffle_enemies(self, event=None):
            """
            Pick a new set of enemies to display in the encounter.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
                    Default: None
            """
            try:
                log("Start of shuffle_enemies")

                self.encounter.bind("<Button 1>", do_nothing)
                if not self.selected:
                    log("\tNo encounter loaded - nothing to shuffle")
                    self.encounter.bind("<Button 1>", self.shuffle_enemies)
                    log("\tEnd of shuffle_enemies")
                    return

                self.rewardTreasure = None

                # Make sure a new set of enemies is chosen each time, otherwise it
                # feels like the program isn't doing anything.
                oldEnemies = [e for e in self.newEnemies]
                if "1" in self.selected["alternatives"]:
                    tile1Enemies = choice(self.selected["alternatives"]["1"])
                    tile2Enemies = choice([alt for alt in self.selected["alternatives"]["2"] if not set([a for a in alt if enemyIds[a].expansions == set(["Phantoms"])]) & set(tile1Enemies)])
                    tile3Enemies = choice([alt for alt in self.selected["alternatives"]["3"] if not set([a for a in alt if enemyIds[a].expansions == set(["Phantoms"])]) & set(tile1Enemies) and  not set([a for a in alt if enemyIds[a].expansions == set(["Phantoms"])]) & set(tile2Enemies)])

                    self.newEnemies = tile1Enemies + tile2Enemies + tile3Enemies
                else:
                    self.newEnemies = choice(self.selected["alternatives"])
                # Check to see if there are multiple alternatives.
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

                log("\tEnd of shuffle_enemies")
            except Exception as e:
                error_popup(root, e)
                raise


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
            try:
                log("Start of edit_encounter_card")

                self.encounterPhotoImage = self.create_image(name + ".jpg", "encounter", level, expansion)

                self.newTiles = {
                    1: [[], [], [], []],
                    2: [[], []],
                    3: [[], []]
                    }

                log("New enemies: " + str(self.newEnemies))

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
                            imageType = "imageOldLevel4"
                        elif expansion in {"Dark Souls The Board Game", "Iron Keep", "Darkroot", "Explorers", "Executioner Chariot"}:
                            x = 67 + (40 * e)
                            y = 66 + (46 * slotNum)
                            imageType = "imageOld"
                        else:
                            x = 300 + (29 * e)
                            y = 323 + (29 * (slotNum - (0 if slotNum < 4 else 5 if slotNum < 7 else 8))) + (((1 if slotNum < 4 else 2 if slotNum < 7 else 3) - 1) * 122)
                            imageType = "imageNew"
                            
                        image = allEnemies[enemyIds[self.newEnemies[s]].name][imageType]

                        log("Pasting " + enemyIds[self.newEnemies[s]].name + " image onto encounter at " + str((x, y)) + ".")
                        self.encounterImage.paste(im=image, box=(x, y), mask=image)
                        s += 1

                self.apply_keyword_tooltips(name, expansion)

                # These are new encounters that have text referencing specific enemies.
                if name == "Abandoned and Forgotten":
                    self.abandoned_and_forgotten()
                elif name == "Aged Sentinel":
                    self.aged_sentinel()
                elif name == "Castle Break In":
                    self.castle_break_in()
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
                elif name == "Dark Resurrection":
                    self.dark_resurrection()
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
                elif name == "Grave Matters":
                    self.grave_matters()
                elif name == "Grim Reunion":
                    self.grim_reunion()
                elif name == "Hanging Rafters":
                    self.hanging_rafters()
                elif name == "In Deep Water":
                    self.in_deep_water()
                elif name == "Inhospitable Ground":
                    self.inhospitable_ground()
                elif name == "Lakeview Refuge":
                    self.lakeview_refuge()
                elif name == "Monstrous Maw":
                    self.monstrous_maw()
                elif name == "No Safe Haven":
                    self.no_safe_haven()
                elif name == "Painted Passage":
                    self.painted_passage()
                elif name == "Parish Church":
                    self.parish_church()
                elif name == "Parish Gates":
                    self.parish_gates()
                elif name == "Pitch Black":
                    self.pitch_black()
                elif name == "Puppet Master":
                    self.puppet_master()
                elif name == "Rain of Filth":
                    self.rain_of_filth()
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
                elif name == "Unseen Scurrying":
                    self.unseen_scurrying()
                elif name == "Urns of the Fallen":
                    self.urns_of_the_fallen()
                elif name == "Velka's Chosen":
                    self.velkas_chosen()

                self.encounterPhotoImage = ImageTk.PhotoImage(self.encounterImage)
                self.encounter.image = self.encounterPhotoImage
                if not self.forPrinting:
                    self.encounter.config(image=self.encounterPhotoImage)
                self.encounter.bind("<Button 1>", self.shuffle_enemies)

                log("\tEnd of edit_encounter_card")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_tooltip(self, tooltipDict, x, y):
            """
            Create a label and tooltip that will be placed and later removed.
            """
            try:
                log("Start of create_tooltip")

                if self.forPrinting:
                    convertedImage = tooltipDict["image"].convert("RGBA")
                    self.encounterImage.paste(im=convertedImage, box=(x, y), mask=convertedImage)
                else:
                    label = tk.Label(self.encounterFrame, image=tooltipDict["photo image"], borderwidth=0, highlightthickness=0)
                    self.tooltips.append(label)
                    label.place(x=x, y=y)
                    CreateToolTip(label, tooltipText[tooltipDict["imageName"]])

                log("\tEnd of create_tooltip")
            except Exception as e:
                error_popup(root, e)
                raise


        def apply_keyword_tooltips(self, name, set):
            """
            If the encounter card has keywords, create an image of the word imposed over
            the original word and create a tooltip that shows up when mousing over the keyword image.
            """
            try:
                log("Start of apply_keyword_tooltips")

                for tooltip in self.tooltips:
                    tooltip.destroy()

                if not self.selected and not self.treeviewCampaign.focus():
                    log("\tEnd of apply_keyword_tooltips (removed tooltips only)")
                    return

                for i, tooltip in enumerate(self.encounterTooltips.get((name, set), [])):
                    if not tooltip:
                        continue
                    self.create_tooltip(tooltipDict=tooltip, x=142, y=int(199 + (15.5 * i)))

                log("\tEnd of apply_keyword_tooltips")
            except Exception as e:
                error_popup(root, e)
                raise


        def new_treasure_name(self, newTreasure):
            treasureLines = {}
            if newTreasure.count(" ") > 2:
                breakIdx = newTreasure.rfind(" ", 0, newTreasure.rfind(" ") - 1)
                treasureLines[0] = newTreasure[:breakIdx]
                treasureLines[1] = newTreasure[breakIdx+1:]
            elif newTreasure.count(" ") > 0 and len(newTreasure) >= 15:
                lastSpaceIdx = newTreasure.rfind(" ")
                treasureLines[0] = newTreasure[:lastSpaceIdx]
                treasureLines[1] = newTreasure[lastSpaceIdx+1:]
            else:
                treasureLines[0] = newTreasure

            return treasureLines


        def abandoned_and_forgotten(self):
            try:
                log("Start of abandoned_and_forgotten")

                spawn1 = enemyIds[self.newEnemies[0]].name
                spawn2 = enemyIds[self.newEnemies[1]].name
                spawn3 = enemyIds[self.newEnemies[2]].name

                self.encounterImage.paste(im=allEnemies[spawn1]["imageNew"], box=(285, 218), mask=allEnemies[spawn1]["imageNew"])
                self.encounterImage.paste(im=allEnemies[spawn2]["imageNew"], box=(285, 248), mask=allEnemies[spawn2]["imageNew"])
                self.encounterImage.paste(im=allEnemies[spawn3]["imageNew"], box=(285, 280), mask=allEnemies[spawn3]["imageNew"])

                log("\tEnd of abandoned_and_forgotten")
            except Exception as e:
                error_popup(root, e)
                raise


        def aged_sentinel(self):
            try:
                log("Start of aged_sentinel")

                target = self.newTiles[1][1][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=65, y=147)
                self.create_tooltip(tooltipDict=tooltipDict, x=143, y=231)
                self.create_tooltip(tooltipDict=tooltipDict, x=203, y=255)

                log("\tEnd of aged_sentinel")
            except Exception as e:
                error_popup(root, e)
                raise


        def castle_break_in(self):
            try:
                log("Start of castle_break_in")

                imageWithText = ImageDraw.Draw(self.encounterImage)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 255), newTreasureLines[0], "black", font)
                imageWithText.text((21, 266), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of castle_break_in")
            except Exception as e:
                error_popup(root, e)
                raise


        def central_plaza(self):
            try:
                log("Start of central_plaza")

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=143, y=262)

                log("\tEnd of central_plaza")
            except Exception as e:
                error_popup(root, e)
                raise


        def cloak_and_feathers(self):
            try:
                log("Start of cloak_and_feathers")

                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=65, y=147)

                log("\tEnd of cloak_and_feathers")
            except Exception as e:
                error_popup(root, e)
                raise


        def cold_snap(self):
            try:
                log("Start of cold_snap")

                target = self.newTiles[2][0][1]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=216, y=227)

                log("\tEnd of cold_snap")
            except Exception as e:
                error_popup(root, e)
                raise


        def corrupted_hovel(self):
            try:
                log("Start of corrupted_hovel")

                target = [enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1] if (self.newTiles[1][0] + self.newTiles[1][1]).count(enemy) == 2][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=146, y=250)

                log("\tEnd of corrupted_hovel")
            except Exception as e:
                error_popup(root, e)
                raise


        def corvian_host(self):
            try:
                log("Start of corvian_host")

                target = self.newTiles[1][1][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=161, y=238)
                self.create_tooltip(tooltipDict=tooltipDict, x=263, y=238)
                self.create_tooltip(tooltipDict=tooltipDict, x=261, y=251)
                self.create_tooltip(tooltipDict=tooltipDict, x=189, y=276)
                self.create_tooltip(tooltipDict=tooltipDict, x=145, y=288)

                imageWithText = ImageDraw.Draw(self.encounterImage)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of corvian_host")
            except Exception as e:
                error_popup(root, e)
                raise


        def dark_alleyway(self):
            try:
                log("Start of dark_alleyway")

                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=65, y=147)

                log("\tEnd of dark_alleyway")
            except Exception as e:
                error_popup(root, e)
                raise


        def dark_resurrection(self):
            try:
                log("Start of dark_resurrection")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 235), newTreasureLines[0], "black", font)
                imageWithText.text((21, 246), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of dark_resurrection")
            except Exception as e:
                error_popup(root, e)
                raise


        def deathly_freeze(self):
            try:
                log("Start of deathly_freeze")

                deathlyFreezeTile1 = [enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1]]
                deathlyFreezeTile2 = [enemy for enemy in self.newTiles[2][0] + self.newTiles[2][1]]
                overlap = set(deathlyFreezeTile1) & set(deathlyFreezeTile2)
                target = sorted([enemy for enemy in overlap if deathlyFreezeTile1.count(enemy) + deathlyFreezeTile2.count(enemy) == 2], key=lambda x: (-enemiesDict[x].toughness, enemiesDict[x].difficulty[self.numberOfCharacters]), reverse=True)[0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=141, y=242)

                log("\tEnd of deathly_freeze")
            except Exception as e:
                error_popup(root, e)
                raise


        def deathly_magic(self):
            try:
                log("Start of deathly_magic")

                target = sorted([enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1] if (self.newTiles[1][0] + self.newTiles[1][1]).count(enemy) == 1], key=lambda x: enemiesDict[x].difficulty[self.numberOfCharacters], reverse=True)[0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=65, y=147)
                self.create_tooltip(tooltipDict=tooltipDict, x=274, y=196)

                log("\tEnd of deathly_magic")
            except Exception as e:
                error_popup(root, e)
                raise


        def deathly_tolls(self):
            try:
                log("Start of deathly_tolls")

                target = enemyIds[self.newEnemies[7]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=180, y=212)

                gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
                if gang == "Alonne":
                    tooltipDict = {"image" if self.forPrinting else "image" if self.forPrinting else "photo image": self.gangAlonne if self.forPrinting else self.gangAlonnePhoto, "imageName": "gang"}
                elif gang == "Hollow":
                    tooltipDict = {"image" if self.forPrinting else "image" if self.forPrinting else "photo image": self.gangHollow if self.forPrinting else self.gangHollowPhoto, "imageName": "gang"}
                elif gang == "Silver Knight":
                    tooltipDict = {"image" if self.forPrinting else "image" if self.forPrinting else "photo image": self.gangSilverKnight if self.forPrinting else self.gangSilverKnightPhoto, "imageName": "gang"}
                elif gang == "Skeleton":
                    tooltipDict = {"image" if self.forPrinting else "image" if self.forPrinting else "photo image": self.gangSkeleton if self.forPrinting else self.gangSkeletonPhoto, "imageName": "gang"}

                self.create_tooltip(tooltipDict=tooltipDict, x=142, y=245)

                log("\tEnd of deathly_tolls")
            except Exception as e:
                error_popup(root, e)
                raise


        def depths_of_the_cathedral(self):
            try:
                log("Start of depths_of_the_cathedral")

                gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
                if gang == "Alonne":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangAlonne if self.forPrinting else self.gangAlonnePhoto, "imageName": "gang"}
                elif gang == "Hollow":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangHollow if self.forPrinting else self.gangHollowPhoto, "imageName": "gang"}
                elif gang == "Silver Knight":
                    tooltipDict = {"image" if self.forPrinting else "image" if self.forPrinting else "photo image": self.gangSilverKnight if self.forPrinting else self.gangSilverKnightPhoto, "imageName": "gang"}
                elif gang == "Skeleton":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangSkeleton if self.forPrinting else self.gangSkeletonPhoto, "imageName": "gang"}

                self.create_tooltip(tooltipDict=tooltipDict, x=142, y=214)

                log("\tEnd of depths_of_the_cathedral")
            except Exception as e:
                error_popup(root, e)
                raise


        def distant_tower(self):
            try:
                log("Start of distant_tower")

                target = self.newTiles[3][0][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=217, y=213)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 283), newTreasureLines[0], "black", font)
                imageWithText.text((21, 294), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of distant_tower")
            except Exception as e:
                error_popup(root, e)
                raise


        def eye_of_the_storm(self):
            try:
                log("Start of eye_of_the_storm")

                imageWithText = ImageDraw.Draw(self.encounterImage)
                fourTarget = [enemyIds[enemy].name for enemy in self.newEnemies if self.newEnemies.count(enemy) == 4]
                targets = list(set([enemyIds[enemy].name for enemy in self.newEnemies if self.newEnemies.count(enemy) == 2]))
                text1 = "Increase        "
                if fourTarget:
                    tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[fourTarget[0]]["image text" if self.forPrinting else "photo image text"], "imageName": fourTarget[0]}
                    self.create_tooltip(tooltipDict=tooltipDict, x=187, y=255)
                else:
                    tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[targets[0]]["image text" if self.forPrinting else "photo image text"], "imageName": targets[0]}
                    self.create_tooltip(tooltipDict=tooltipDict, x=187, y=255)
                    tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[targets[1]]["image text" if self.forPrinting else "photo image text"], "imageName": targets[1]}
                    self.create_tooltip(tooltipDict=tooltipDict, x=232, y=255)
                    text1 += " and        "
                text1 += "block and resistance"
                text2 = "values by 1. Once these enemies have been"
                text3 = "killed, spawn the        on      , on tile 3."

                target = enemyIds[self.newEnemies[5]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=65, y=147)
                self.create_tooltip(tooltipDict=tooltipDict, x=228, y=281)
                self.encounterImage.paste(im=self.enemyNode2, box=(263, 281), mask=self.enemyNode2)
                imageWithText.text((140, 255), text1, "black", font)
                imageWithText.text((140, 268), text2, "black", font)
                imageWithText.text((140, 282), text3, "black", font)

                log("\tEnd of eye_of_the_storm")
            except Exception as e:
                error_popup(root, e)
                raise


        def flooded_fortress(self):
            try:
                log("Start of flooded_fortress")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
                if gang == "Alonne":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangAlonne if self.forPrinting else self.gangAlonnePhoto, "imageName": "gang"}
                elif gang == "Hollow":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangHollow if self.forPrinting else self.gangHollowPhoto, "imageName": "gang"}
                elif gang == "Silver Knight":
                    tooltipDict = {"image" if self.forPrinting else "image" if self.forPrinting else "photo image": self.gangSilverKnight if self.forPrinting else self.gangSilverKnightPhoto, "imageName": "gang"}
                elif gang == "Skeleton":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangSkeleton if self.forPrinting else self.gangSkeletonPhoto, "imageName": "gang"}

                self.create_tooltip(tooltipDict=tooltipDict, x=142, y=215)

                log("\tEnd of flooded_fortress")
            except Exception as e:
                error_popup(root, e)
                raise


        def frozen_revolutions(self):
            try:
                log("Start of frozen_revolutions")

                target = self.newTiles[3][0][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=143, y=227)
                self.create_tooltip(tooltipDict=tooltipDict, x=143, y=243)
                self.create_tooltip(tooltipDict=tooltipDict, x=354, y=243)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of frozen_revolutions")
            except Exception as e:
                error_popup(root, e)
                raise


        def giants_coffin(self):
            try:
                log("Start of giants_coffin")

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=241, y=228)

                target = enemyIds[self.newEnemies[5]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=286, y=228)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of giants_coffin")
            except Exception as e:
                error_popup(root, e)
                raise


        def gleaming_silver(self):
            try:
                log("Start of gleaming_silver")

                targets = [enemyIds[enemy].name for enemy in list(set(sorted(self.newEnemies, key=lambda x: enemyIds[x].difficulty[self.numberOfCharacters])[1:-1]))]

                for i, target in enumerate(targets):
                    tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                    self.create_tooltip(tooltipDict=tooltipDict, x=144 + (i * 20), y=270)

                target = enemyIds[self.newEnemies[5]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=180, y=212)

                log("\tEnd of gleaming_silver")
            except Exception as e:
                error_popup(root, e)
                raise


        def gnashing_beaks(self):
            try:
                log("Start of gnashing_beaks")

                target = enemyIds[self.newEnemies[2]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=314, y=232)

                target = enemyIds[self.newEnemies[3]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=338, y=232)

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=235, y=244)

                log("\tEnd of gnashing_beaks")
            except Exception as e:
                error_popup(root, e)
                raise


        def grave_matters(self):
            try:
                log("Start of grave_matters")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of grave_matters")
            except Exception as e:
                error_popup(root, e)
                raise


        def grim_reunion(self):
            try:
                log("Start of grim_reunion")

                target = enemyIds[self.newEnemies[10]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=219, y=196)
                self.create_tooltip(tooltipDict=tooltipDict, x=269, y=255)

                log("\tEnd of grim_reunion")
            except Exception as e:
                error_popup(root, e)
                raise


        def hanging_rafters(self):
            try:
                log("Start of hanging_rafters")

                imageWithText = ImageDraw.Draw(self.encounterImage)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of hanging_rafters")
            except Exception as e:
                error_popup(root, e)
                raise


        def in_deep_water(self):
            try:
                log("Start of in_deep_water")

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=239, y=198)

                target = enemyIds[self.newEnemies[5]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=323, y=198)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of in_deep_water")
            except Exception as e:
                error_popup(root, e)
                raise


        def inhospitable_ground(self):
            try:
                log("Start of inhospitable_ground")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of inhospitable_ground")
            except Exception as e:
                error_popup(root, e)
                raise


        def lakeview_refuge(self):
            try:
                log("Start of lakeview_refuge")

                target = enemyIds[self.newEnemies[-(self.numberOfCharacters + 1)]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=215, y=228)
                self.create_tooltip(tooltipDict=tooltipDict, x=291, y=264)

                for i, enemy in enumerate(self.newEnemies[-self.numberOfCharacters:]):
                    target = enemyIds[enemy].name
                    tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                    self.create_tooltip(tooltipDict=tooltipDict, x=181 + (20 * i), y=288)

                log("\tEnd of lakeview_refuge")
            except Exception as e:
                error_popup(root, e)
                raise


        def monstrous_maw(self):
            try:
                log("Start of monstrous_maw")

                target = self.newTiles[1][1][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=65, y=147)
                self.create_tooltip(tooltipDict=tooltipDict, x=210, y=196)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of monstrous_maw")
            except Exception as e:
                error_popup(root, e)
                raise


        def no_safe_haven(self):
            try:
                log("Start of no_safe_haven")

                target = self.newTiles[2][0][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=63, y=147)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of no_safe_haven")
            except Exception as e:
                error_popup(root, e)
                raise


        def painted_passage(self):
            try:
                log("Start of painted_passage")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of painted_passage")
            except Exception as e:
                error_popup(root, e)
                raise


        def parish_church(self):
            try:
                log("Start of parish_church")

                target = enemyIds[self.newEnemies[10]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=180, y=198)

                log("\tEnd of parish_church")
            except Exception as e:
                error_popup(root, e)
                raise


        def parish_gates(self):
            try:
                log("Start of parish_gates")

                target = enemyIds[self.newEnemies[3]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=301, y=220)
                self.create_tooltip(tooltipDict=tooltipDict, x=188, y=255)
                self.create_tooltip(tooltipDict=tooltipDict, x=144, y=280)

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=321, y=220)
                self.create_tooltip(tooltipDict=tooltipDict, x=208, y=255)
                self.create_tooltip(tooltipDict=tooltipDict, x=164, y=280)

                log("\tEnd of parish_gates")
            except Exception as e:
                error_popup(root, e)
                raise


        def pitch_black(self):
            try:
                log("Start of pitch_black")

                tile1Enemies = self.newTiles[1][0] + self.newTiles[1][1]
                tile2Enemies = self.newTiles[2][0] + self.newTiles[2][1]
                target = sorted([enemy for enemy in tile1Enemies if tile1Enemies.count(enemy) == 1], key=lambda x: enemiesDict[x].difficulty[self.numberOfCharacters], reverse=True)[0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=65, y=147)
                target = sorted([enemy for enemy in tile2Enemies if tile2Enemies.count(enemy) == 1], key=lambda x: enemiesDict[x].difficulty[self.numberOfCharacters], reverse=True)[0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=222, y=147)

                log("\tEnd of pitch_black")
            except Exception as e:
                error_popup(root, e)
                raise


        def puppet_master(self):
            try:
                log("Start of puppet_master")

                target = self.newTiles[1][0][1]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=64, y=148)
                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=145, y=196)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of puppet_master")
            except Exception as e:
                error_popup(root, e)
                raise


        def rain_of_filth(self):
            try:
                log("Start of rain_of_filth")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of rain_of_filth")
            except Exception as e:
                error_popup(root, e)
                raise


        def shattered_keep(self):
            try:
                log("Start of shattered_keep")
                
                targets = set([self.newTiles[1][0][1], self.newTiles[1][1][0], self.newTiles[1][1][1]])
                for i, target in enumerate(targets):
                    tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                    self.create_tooltip(tooltipDict=tooltipDict, x=145 + (20 * i), y=213)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 255), newTreasureLines[0], "black", font)
                imageWithText.text((21, 266), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of shattered_keep")
            except Exception as e:
                error_popup(root, e)
                raise


        def skeletal_spokes(self):
            try:
                log("Start of skeletal_spokes")

                target = self.newTiles[2][0][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=145, y=196)
                self.create_tooltip(tooltipDict=tooltipDict, x=165, y=210)
                self.create_tooltip(tooltipDict=tooltipDict, x=165, y=239)

                log("\tEnd of skeletal_spokes")
            except Exception as e:
                error_popup(root, e)
                raise


        def skeleton_overlord(self):
            try:
                log("Start of skeleton_overlord")

                target = enemyIds[self.newEnemies[1]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=230, y=196)
                self.create_tooltip(tooltipDict=tooltipDict, x=208, y=257)

                target = enemyIds[self.newEnemies[2]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=309, y=196)
                self.create_tooltip(tooltipDict=tooltipDict, x=245, y=257)

                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=65, y=147)
                self.create_tooltip(tooltipDict=tooltipDict, x=313, y=232)
                self.create_tooltip(tooltipDict=tooltipDict, x=332, y=257)

                log("\tEnd of skeleton_overlord")
            except Exception as e:
                error_popup(root, e)
                raise


        def tempting_maw(self):
            try:
                log("Start of tempting_maw")

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=224, y=145)
                self.create_tooltip(tooltipDict=tooltipDict, x=220, y=197)
                self.create_tooltip(tooltipDict=tooltipDict, x=346, y=256)

                log("\tEnd of tempting_maw")
            except Exception as e:
                error_popup(root, e)
                raise


        def the_abandoned_chest(self):
            try:
                log("Start of the_abandoned_chest")

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=322, y=195)

                target = enemyIds[self.newEnemies[5]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=144, y=208)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of the_abandoned_chest")
            except Exception as e:
                error_popup(root, e)
                raise


        def the_beast_from_the_depths(self):
            try:
                log("Start of the_beast_from_the_depths")

                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=65, y=147)
                self.create_tooltip(tooltipDict=tooltipDict, x=158, y=222)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of the_beast_from_the_depths")
            except Exception as e:
                error_popup(root, e)
                raise


        def the_bell_tower(self):
            try:
                log("Start of the_bell_tower")

                target = enemyIds[self.newEnemies[2]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=321, y=195)

                target = enemyIds[self.newEnemies[3]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=341, y=195)

                log("\tEnd of the_bell_tower")
            except Exception as e:
                error_popup(root, e)
                raise


        def the_first_bastion(self):
            try:
                log("Start of the_first_bastion")

                targets = sorted([enemyIds[enemy].name for enemy in self.newEnemies[-3:]], key=lambda x: (-enemiesDict[x].toughness, enemiesDict[x].difficulty[self.numberOfCharacters]))
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[targets[0]]["image text" if self.forPrinting else "photo image text"], "imageName": targets[0]}
                self.create_tooltip(tooltipDict=tooltipDict, x=362, y=212)
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[targets[1]]["image text" if self.forPrinting else "photo image text"], "imageName": targets[1]}
                self.create_tooltip(tooltipDict=tooltipDict, x=188, y=237)
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[targets[2]]["image text" if self.forPrinting else "photo image text"], "imageName": targets[2]}
                self.create_tooltip(tooltipDict=tooltipDict, x=247, y=249)
                self.create_tooltip(tooltipDict=tooltipDict, x=216, y=197)

                log("\tEnd of the_first_bastion")
            except Exception as e:
                error_popup(root, e)
                raise


        def the_fountainhead(self):
            try:
                log("Start of the_fountainhead")

                gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
                if gang == "Alonne":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangAlonne if self.forPrinting else self.gangAlonnePhoto, "imageName": "gang"}
                elif gang == "Hollow":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangHollow if self.forPrinting else self.gangHollowPhoto, "imageName": "gang"}
                elif gang == "Silver Knight":
                    tooltipDict = {"image" if self.forPrinting else "image" if self.forPrinting else "photo image": self.gangSilverKnight if self.forPrinting else self.gangSilverKnightPhoto, "imageName": "gang"}
                elif gang == "Skeleton":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangSkeleton if self.forPrinting else self.gangSkeletonPhoto, "imageName": "gang"}

                self.create_tooltip(tooltipDict=tooltipDict, x=142, y=200)

                log("\tEnd of the_fountainhead")
            except Exception as e:
                error_popup(root, e)
                raise


        def the_grand_hall(self):
            try:
                log("Start of the_grand_hall")

                target = enemyIds[self.newEnemies[7]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=180, y=213)

                log("\tEnd of the_grand_hall")
            except Exception as e:
                error_popup(root, e)
                raise


        def the_iron_golem(self):
            try:
                log("Start of the_iron_golem")

                target = self.newTiles[1][1][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=65, y=147)
                self.create_tooltip(tooltipDict=tooltipDict, x=188, y=196)
                self.create_tooltip(tooltipDict=tooltipDict, x=174, y=219)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 266), newTreasureLines[0], "black", font)
                imageWithText.text((21, 277), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of the_iron_golem")
            except Exception as e:
                error_popup(root, e)
                raise


        def the_last_bastion(self):
            try:
                log("Start of the_last_bastion")

                target = sorted([enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1]], key=lambda x: enemiesDict[x].difficulty[self.numberOfCharacters])[0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=215, y=227)
                self.create_tooltip(tooltipDict=tooltipDict, x=316, y=250)
                self.create_tooltip(tooltipDict=tooltipDict, x=337, y=263)

                log("\tEnd of the_last_bastion")
            except Exception as e:
                error_popup(root, e)
                raise


        def the_locked_grave(self):
            try:
                log("Start of the_locked_grave")

                target = enemyIds[self.newEnemies[7]].name
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=217, y=197)
                self.create_tooltip(tooltipDict=tooltipDict, x=306, y=220)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of the_locked_grave")
            except Exception as e:
                error_popup(root, e)
                raise


        def the_shine_of_gold(self):
            try:
                log("Start of the_shine_of_gold")

                target = self.newTiles[1][1][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=65, y=147)
                self.create_tooltip(tooltipDict=tooltipDict, x=207, y=219)
                self.create_tooltip(tooltipDict=tooltipDict, x=280, y=254)
                self.create_tooltip(tooltipDict=tooltipDict, x=250, y=268)

                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=268, y=195)

                log("\tEnd of the_shine_of_gold")
            except Exception as e:
                error_popup(root, e)
                raise


        def the_skeleton_ball(self):
            try:
                log("Start of the_skeleton_ball")

                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=64, y=148)
                target = self.newTiles[3][1][0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=222, y=148)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of the_skeleton_ball")
            except Exception as e:
                error_popup(root, e)
                raise


        def trecherous_tower(self):
            try:
                log("Start of trecherous_tower")

                spawn1 = enemyIds[self.newEnemies[2]].name
                spawn2 = enemyIds[self.newEnemies[3]].name
                spawn3 = enemyIds[self.newEnemies[4]].name

                self.encounterImage.paste(im=allEnemies[spawn1]["imageNew"], box=(285, 218), mask=allEnemies[spawn1]["imageNew"])
                self.encounterImage.paste(im=allEnemies[spawn2]["imageNew"], box=(285, 248), mask=allEnemies[spawn2]["imageNew"])
                self.encounterImage.paste(im=allEnemies[spawn3]["imageNew"], box=(285, 280), mask=allEnemies[spawn3]["imageNew"])

                log("\tEnd of trecherous_tower")
            except Exception as e:
                error_popup(root, e)
                raise


        def trophy_room(self):
            try:
                log("Start of trophy_room")

                targets = set([self.newTiles[2][0][0], self.newTiles[2][1][0]])
                for i, target in enumerate(targets):
                    tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                    self.create_tooltip(tooltipDict=tooltipDict, x=61 + (20 * i), y=147)
                    self.create_tooltip(tooltipDict=tooltipDict, x=210 + (20 * i), y=197)
                    self.create_tooltip(tooltipDict=tooltipDict, x=145 + (20 * i), y=244)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of trophy_room")
            except Exception as e:
                error_popup(root, e)
                raise


        def twilight_falls(self):
            try:
                log("Start of twilight_falls")

                gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
                if gang == "Alonne":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangAlonne if self.forPrinting else self.gangAlonnePhoto, "imageName": "gang"}
                elif gang == "Hollow":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangHollow if self.forPrinting else self.gangHollowPhoto, "imageName": "gang"}
                elif gang == "Silver Knight":
                    tooltipDict = {"image" if self.forPrinting else "image" if self.forPrinting else "photo image": self.gangSilverKnight if self.forPrinting else self.gangSilverKnightPhoto, "imageName": "gang"}
                elif gang == "Skeleton":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangSkeleton if self.forPrinting else self.gangSkeletonPhoto, "imageName": "gang"}

                self.create_tooltip(tooltipDict=tooltipDict, x=142, y=214)

                log("\tEnd of twilight_falls")
            except Exception as e:
                error_popup(root, e)
                raise


        def undead_sanctum(self):
            try:
                log("Start of undead_sanctum")

                gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
                if gang == "Alonne":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangAlonne if self.forPrinting else self.gangAlonnePhoto, "imageName": "gang"}
                elif gang == "Hollow":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangHollow if self.forPrinting else self.gangHollowPhoto, "imageName": "gang"}
                elif gang == "Silver Knight":
                    tooltipDict = {"image" if self.forPrinting else "image" if self.forPrinting else "photo image": self.gangSilverKnight if self.forPrinting else self.gangSilverKnightPhoto, "imageName": "gang"}
                elif gang == "Skeleton":
                    tooltipDict = {"image" if self.forPrinting else "photo image": self.gangSkeleton if self.forPrinting else self.gangSkeletonPhoto, "imageName": "gang"}

                self.create_tooltip(tooltipDict=tooltipDict, x=142, y=214)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of undead_sanctum")
            except Exception as e:
                error_popup(root, e)
                raise

        def unseen_scurrying(self):
            try:
                log("Start of unseen_scurrying")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of unseen_scurrying")
            except Exception as e:
                error_popup(root, e)
                raise


        def urns_of_the_fallen(self):
            try:
                log("Start of urns_of_the_fallen")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of urns_of_the_fallen")
            except Exception as e:
                error_popup(root, e)
                raise


        def velkas_chosen(self):
            try:
                log("Start of velkas_chosen")

                target = sorted([enemy for enemy in self.newTiles[2][0] + self.newTiles[2][1]], key=lambda x: enemiesDict[x].difficulty[self.numberOfCharacters], reverse=True)[0]
                tooltipDict = {"image" if self.forPrinting else "photo image": allEnemies[target]["image text" if self.forPrinting else "photo image text"], "imageName": target}
                self.create_tooltip(tooltipDict=tooltipDict, x=65, y=147)
                self.create_tooltip(tooltipDict=tooltipDict, x=298, y=195)
                self.create_tooltip(tooltipDict=tooltipDict, x=205, y=219)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableExpansions), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of velkas_chosen")
            except Exception as e:
                error_popup(root, e)
                raise


    coreSets = {"Dark Souls The Board Game", "Painted World of Ariamis", "Tomb of Giants", "The Sunless City"}

    root = tk.Tk()
    root.withdraw()
    root.attributes('-alpha', 0.0)
        
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
            p = PopupWindow(root, "A new version of DSBG-Shuffle is available!\nCheck it out on Github!\n\nIf you don't want to see this notification anymore,\ndisable checking for updates in the settings.", firstButton="Ok", secondButton=True)
            root.wait_window(p)

    s = ttk.Style()

    app = Application(root)
    app.pack(fill="both", expand=True)

    center(root)
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.attributes('-alpha', 1.0)
    root.mainloop()
    log("Closing application")
    root.destroy()

except Exception as e:
    error = str(sys.exc_info())
    if "application has been destroyed" not in error:
        log(error, exception=True)
        raise
