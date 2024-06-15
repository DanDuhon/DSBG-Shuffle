try:
    from collections import Counter
    from json import load
    from PIL import ImageTk, ImageDraw
    from random import choice
    from tkinter import ttk

    from dsbg_shuffle_enemies import enemiesDict, enemyIds
    from dsbg_shuffle_treasure import pick_treasure, treasureSwapEncounters
    from dsbg_shuffle_utility import PopupWindow, clear_other_tab_images, do_nothing, error_popup, log, baseFolder, font, pathSep


    class EncountersFrame(ttk.Frame):
        def __init__(self, app, root):
            super(EncountersFrame, self).__init__()
            self.app = app
            self.root = root
            
            self.encountersToPrint = []

            self.expansionsForRandomEncounters = ((self.app.v1Expansions if "v1" in self.app.settings["encounterTypes"] else set()) | (self.app.v2Expansions if "v2" in self.app.settings["encounterTypes"] else set()) | (self.app.level4Expansions if "Level 4 encounters" in self.app.settings["availableExpansions"] else set())) & self.app.allExpansions
            self.set_encounter_list()

            # If specific enemies (rather than just expansions) are toggled on or off, do extra work
            # to make sure all encounters are still valid.
            if self.app.settings["customEnemyList"]:
                i = 0
                self.app.progress.destroy()
                self.app.progress = PopupWindow(root, labelText="Applying custom enemy list...", progressBar=True, progressMax=len(self.encounterList), loadingImage=True)
                self.encountersToRemove = set()
                for encounter in self.encounterList:
                    i += 1
                    self.app.progress.progressVar.set(i)
                    self.root.update_idletasks()
                    self.load_encounter(encounter=encounter, customEnemyListCheck=True)
                    if all([not set(alt).issubset(self.app.enabledEnemies) for alt in self.app.selected["alternatives"]]):
                        self.encountersToRemove.add(encounter)

                self.encounterList = list(set(self.encounterList) - self.encountersToRemove)

            self.scrollbarTreeviewEncounters = ttk.Scrollbar(self)
            self.scrollbarTreeviewEncounters.pack(side="right", fill="y")
            self.create_encounters_treeview()

            # What encounters have what special rules
            self.encounterTooltips = {
                ("A Trusty Ally", "Tomb of Giants"): [
                    {"image": self.app.onslaught, "photo image": ImageTk.PhotoImage(self.app.onslaught), "imageName": "onslaught"}
                    ],
                ("Abandoned and Forgotten", "Painted World of Ariamis"): [
                    {"image": self.app.eerie, "photo image": ImageTk.PhotoImage(self.app.eerie), "imageName": "eerie"}
                    ],
                ("Aged Sentinel", "The Sunless City"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("Altar of Bones", "Tomb of Giants"): [
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"}
                    ],
                ("Archive Entrance", "The Sunless City"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("Broken Passageway (TSC)", "The Sunless City"): [
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"},
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"}
                    ],
                ("Castle Break In", "The Sunless City"): [
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"},
                    {},
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"}
                    ],
                ("Central Plaza", "Painted World of Ariamis"): [
                    {"image": self.app.barrage, "photo image": ImageTk.PhotoImage(self.app.barrage), "imageName": "barrage"}
                    ],
                ("Cold Snap", "Painted World of Ariamis"): [
                    {"image": self.app.snowstorm, "photo image": ImageTk.PhotoImage(self.app.snowstorm), "imageName": "snowstorm"},
                    {"image": self.app.bitterCold, "photo image": ImageTk.PhotoImage(self.app.bitterCold), "imageName": "bitterCold"},
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("Corrupted Hovel", "Painted World of Ariamis"): [
                    {"image": self.app.poisonMist, "photo image": ImageTk.PhotoImage(self.app.poisonMist), "imageName": "poisonMist"},
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("Corvian Host", "Painted World of Ariamis"): [
                    {"image": self.app.poisonMist, "photo image": ImageTk.PhotoImage(self.app.poisonMist), "imageName": "poisonMist"}
                    ],
                ("Dark Resurrection", "Tomb of Giants"): [
                    {"image": self.app.darkness, "photo image": ImageTk.PhotoImage(self.app.darkness), "imageName": "darkness"}
                    ],
                ("Deathly Freeze", "Painted World of Ariamis"): [
                    {"image": self.app.snowstorm, "photo image": ImageTk.PhotoImage(self.app.snowstorm), "imageName": "snowstorm"},
                    {"image": self.app.bitterCold, "photo image": ImageTk.PhotoImage(self.app.bitterCold), "imageName": "bitterCold"}
                    ],
                ("Deathly Tolls", "The Sunless City"): [
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"},
                    {"image": self.app.mimic, "photo image": ImageTk.PhotoImage(self.app.mimic), "imageName": "mimic"},
                    {"image": self.app.onslaught, "photo image": ImageTk.PhotoImage(self.app.onslaught), "imageName": "onslaught"}
                    ],
                ("Depths of the Cathedral", "The Sunless City"): [
                    {"image": self.app.mimic, "photo image": ImageTk.PhotoImage(self.app.mimic), "imageName": "mimic"}
                    ],
                ("Distant Tower", "Painted World of Ariamis"): [
                    {"image": self.app.barrage, "photo image": ImageTk.PhotoImage(self.app.barrage), "imageName": "barrage"},
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("Eye of the Storm", "Painted World of Ariamis"): [
                    {"image": self.app.hidden, "photo image": ImageTk.PhotoImage(self.app.hidden), "imageName": "hidden"}
                    ],
                ("Far From the Sun", "Tomb of Giants"): [
                    {"image": self.app.darkness, "photo image": ImageTk.PhotoImage(self.app.darkness), "imageName": "darkness"}
                    ],
                ("Flooded Fortress", "The Sunless City"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("Frozen Revolutions", "Painted World of Ariamis"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("Frozen Sentries", "Painted World of Ariamis"): [
                    {"image": self.app.snowstorm, "photo image": ImageTk.PhotoImage(self.app.snowstorm), "imageName": "snowstorm"}
                    ],
                ("Giant's Coffin", "Tomb of Giants"): [
                    {"image": self.app.onslaught, "photo image": ImageTk.PhotoImage(self.app.onslaught), "imageName": "onslaught"},
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"},
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"}
                    ],
                ("Gleaming Silver", "The Sunless City"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"},
                    {"image": self.app.mimic, "photo image": ImageTk.PhotoImage(self.app.mimic), "imageName": "mimic"}
                    ],
                ("Gnashing Beaks", "Painted World of Ariamis"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("Grim Reunion", "The Sunless City"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("Hanging Rafters", "The Sunless City"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"},
                    {"image": self.app.onslaught, "photo image": ImageTk.PhotoImage(self.app.onslaught), "imageName": "onslaught"}
                    ],
                ("Illusionary Doorway", "The Sunless City"): [
                    {"image": self.app.illusion, "photo image": ImageTk.PhotoImage(self.app.illusion), "imageName": "illusion"}
                    ],
                ("In Deep Water", "Tomb of Giants"): [
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"}
                    ],
                ("Inhospitable Ground", "Painted World of Ariamis"): [
                    {"image": self.app.snowstorm, "photo image": ImageTk.PhotoImage(self.app.snowstorm), "imageName": "snowstorm"}
                    ],
                ("Kingdom's Messengers", "The Sunless City"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("Lakeview Refuge", "Tomb of Giants"): [
                    {"image": self.app.onslaught, "photo image": ImageTk.PhotoImage(self.app.onslaught), "imageName": "onslaught"},
                    {"image": self.app.darkness, "photo image": ImageTk.PhotoImage(self.app.darkness), "imageName": "darkness"},
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("Last Rites", "Tomb of Giants"): [
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"}
                    ],
                ("Last Shred of Light", "Tomb of Giants"): [
                    {"image": self.app.darkness, "photo image": ImageTk.PhotoImage(self.app.darkness), "imageName": "darkness"}
                    ],
                ("No Safe Haven", "Painted World of Ariamis"): [
                    {"image": self.app.poisonMist, "photo image": ImageTk.PhotoImage(self.app.poisonMist), "imageName": "poisonMist"}
                    ],
                ("Painted Passage", "Painted World of Ariamis"): [
                    {"image": self.app.snowstorm, "photo image": ImageTk.PhotoImage(self.app.snowstorm), "imageName": "snowstorm"}
                    ],
                ("Parish Church", "The Sunless City"): [
                    {"image": self.app.mimic, "photo image": ImageTk.PhotoImage(self.app.mimic), "imageName": "mimic"},
                    {"image": self.app.illusion, "photo image": ImageTk.PhotoImage(self.app.illusion), "imageName": "illusion"},
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("Pitch Black", "Tomb of Giants"): [
                    {"image": self.app.darkness, "photo image": ImageTk.PhotoImage(self.app.darkness), "imageName": "darkness"}
                    ],
                ("Promised Respite", "Painted World of Ariamis"): [
                    {"image": self.app.snowstorm, "photo image": ImageTk.PhotoImage(self.app.snowstorm), "imageName": "snowstorm"}
                    ],
                ("Skeleton Overlord", "Tomb of Giants"): [
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"}
                    ],
                ("Snowblind", "Painted World of Ariamis"): [
                    {"image": self.app.snowstorm, "photo image": ImageTk.PhotoImage(self.app.snowstorm), "imageName": "snowstorm"},
                    {"image": self.app.bitterCold, "photo image": ImageTk.PhotoImage(self.app.bitterCold), "imageName": "bitterCold"},
                    {"image": self.app.hidden, "photo image": ImageTk.PhotoImage(self.app.hidden), "imageName": "hidden"}
                    ],
                ("Tempting Maw", "The Sunless City"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("The Beast From the Depths", "Tomb of Giants"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("The First Bastion", "Painted World of Ariamis"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("The Grand Hall", "The Sunless City"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"},
                    {"image": self.app.mimic, "photo image": ImageTk.PhotoImage(self.app.mimic), "imageName": "mimic"}
                    ],
                ("The Last Bastion", "Painted World of Ariamis"): [
                    {"image": self.app.snowstorm, "photo image": ImageTk.PhotoImage(self.app.snowstorm), "imageName": "snowstorm"},
                    {"image": self.app.bitterCold, "photo image": ImageTk.PhotoImage(self.app.bitterCold), "imageName": "bitterCold"},
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("The Locked Grave", "Tomb of Giants"): [
                    {"image": self.app.trial, "photo image": ImageTk.PhotoImage(self.app.trial), "imageName": "trial"}
                    ],
                ("The Mass Grave", "Tomb of Giants"): [
                    {"image": self.app.onslaught, "photo image": ImageTk.PhotoImage(self.app.onslaught), "imageName": "onslaught"},
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"},
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"},
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"}
                    ],
                ("The Shine of Gold", "The Sunless City"): [
                    {"image": self.app.timer, "photo image": ImageTk.PhotoImage(self.app.timer), "imageName": "timer"}
                    ],
                ("Trecherous Tower", "Painted World of Ariamis"): [
                    {"image": self.app.snowstorm, "photo image": ImageTk.PhotoImage(self.app.snowstorm), "imageName": "snowstorm"},
                    {"image": self.app.bitterCold, "photo image": ImageTk.PhotoImage(self.app.bitterCold), "imageName": "bitterCold"},
                    {"image": self.app.onslaught, "photo image": ImageTk.PhotoImage(self.app.eerie), "imageName": "eerie"}
                    ],
                ("Twilight Falls", "The Sunless City"): [
                    {"image": self.app.illusion, "photo image": ImageTk.PhotoImage(self.app.illusion), "imageName": "illusion"}
                    ],
                ("Undead Sanctum", "The Sunless City"): [
                    {"image": self.app.onslaught, "photo image": ImageTk.PhotoImage(self.app.onslaught), "imageName": "onslaught"}
                    ],
                ("Unseen Scurrying", "Painted World of Ariamis"): [
                    {"image": self.app.hidden, "photo image": ImageTk.PhotoImage(self.app.hidden), "imageName": "hidden"}
                    ]
            }

            self.newEnemies = []
            self.newTiles = dict()
            self.rewardTreasure = None


        def set_encounter_list(self):
            """
            Sets of the list of available encounters in the encounter tab based on what
            the user selected in the settings.
            """
            try:
                log("Start of set_encounter_list")

                # Set the list of encounters based on available expansions.
                self.encounterList = [encounter for encounter in self.app.encounters if (
                    all([
                        any([frozenset(expCombo).issubset(self.app.availableExpansions) for expCombo in self.app.encounters[encounter]["expansionCombos"]["1"]]),
                        any([frozenset(expCombo).issubset(self.app.availableExpansions) for expCombo in self.app.encounters[encounter]["expansionCombos"]["2"]]),
                        True if "3" not in self.app.encounters[encounter]["expansionCombos"] else any([frozenset(expCombo).issubset(self.app.availableExpansions) for expCombo in self.app.encounters[encounter]["expansionCombos"]["3"]]),
                        self.app.encounters[encounter]["expansion"] in ((self.app.v1Expansions if "v1" in self.app.settings["encounterTypes"] else set()) | (self.app.v2Expansions if "v2" in self.app.settings["encounterTypes"] else set()) | (self.app.level4Expansions if "level4" in self.app.settings["encounterTypes"] else set()))
                            ]))]

                log("End of set_encounter_list")
            except Exception as e:
                error_popup(self.root, e)
                raise

        def create_encounters_treeview(self):
            """
            Create the encounters treeview, where a user can select an encounter
            and shuffle the enemies in it.
            """
            try:
                log("Start of create_encounters_treeview")

                self.treeviewEncounters = ttk.Treeview(
                    self,
                    selectmode="browse",
                    columns=("Name"),
                    yscrollcommand=self.scrollbarTreeviewEncounters.set,
                    height=28 if self.root.winfo_screenheight() > 1000 else 19
                )

                self.treeviewEncounters.pack(expand=True, fill="both")
                self.scrollbarTreeviewEncounters.config(command=self.treeviewEncounters.yview)

                self.treeviewEncounters.column("#0", anchor="w")
                self.treeviewEncounters.heading("#0", text="  Name", anchor="w")

                # Sort encounters by:
                # 1. encounters that have more than just level 4 encounters first
                # 2. New core sets first
                # 3. V2 non-core sets
                # 4. Original core set
                # 5. Executioner Chariot at the top of the mega bosses list because it has non-level 4 encounters
                # 6. By level
                # 7. Alphabetically
                self.encountersSorted = [encounter for encounter in sorted(self.encounterList, key=lambda x: (
                    1 if self.app.encounters[x]["level"] == 4 else 0,
                    0 if self.app.encounters[x]["expansion"] in self.app.coreSets and self.app.encounters[x]["expansion"] in self.app.v2Expansions else 1,
                    0 if self.app.encounters[x]["expansion"] in self.app.v2Expansions else 1,
                    1 if self.app.encounters[x]["expansion"] == "Executioner Chariot" else 0,
                    self.app.encounters[x]["expansion"],
                    self.app.encounters[x]["level"],
                    self.app.encounters[x]["name"]))]
                tvData = []
                tvParents = dict()
                x = 0
                for e in self.encountersSorted:
                    if self.app.encounters[e]["expansion"] not in [t[2] for t in tvData]:
                        tvData.append(("", x, self.app.encounters[e]["expansion"], False))
                        tvParents[self.app.encounters[e]["expansion"]] = {"exp": tvData[-1][1]}
                        x += 1

                    if self.app.encounters[e]["expansion"] == "Executioner Chariot" and self.app.encounters[e]["level"] < 4 and "v1"not in self.app.settings["encounterTypes"]:
                        continue

                    if self.app.encounters[e]["level"] == 4 and "level4" not in self.app.settings["encounterTypes"]:
                        continue
                    
                    if self.app.encounters[e]["level"] < 4 and ["level4"] == self.app.settings["encounterTypes"]:
                        continue

                    if self.app.encounters[e]["level"] not in tvParents[self.app.encounters[e]["expansion"]]:
                        tvData.append((tvParents[self.app.encounters[e]["expansion"]]["exp"], x, "Level " + str(self.app.encounters[e]["level"]), False))
                        tvParents[self.app.encounters[e]["expansion"]][self.app.encounters[e]["level"]] = tvData[-1][1]
                        x += 1

                    tvData.append((tvParents[self.app.encounters[e]["expansion"]][self.app.encounters[e]["level"]], x, e, True))
                    x += 1

                for item in tvData:
                    self.treeviewEncounters.insert(parent=item[0], index="end", iid=item[1], text=item[2], tags=item[3])

                    if item[0] == "":
                        self.treeviewEncounters.item(item[1], open=True)

                self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)

                log("End of create_encounters_treeview")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def random_encounter(self, event=None, level=None, encounterList=None):
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
                log("Start of random_encounter, level={}".format(str(level)))

                if not encounterList:
                    encounterList = self.encounterList

                self.load_encounter(encounter=choice([encounter for encounter in encounterList if (
                    self.app.encounters[encounter]["level"] == level
                    and (self.app.encounters[encounter]["expansion"] in self.expansionsForRandomEncounters
                        or self.app.encounters[encounter]["level"] == 4))]))

                log("\tEnd of random_encounter")
            except Exception as e:
                error_popup(self.root, e)
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
                log("Start of load_encounter, event={}, encounter={}, customEnemyListCheck={}".format(str(event), str(encounter), str(customEnemyListCheck)))

                if not customEnemyListCheck:
                    self.treeviewEncounters.unbind("<<TreeviewSelect>>")

                # If this encounter was clicked on, get that information.
                if event:
                    tree = event.widget
                    if not tree.item(tree.selection())["tags"][0]:
                        log("\tNo encounter selected")
                        self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)
                        self.app.display.bind("<Button 1>", self.shuffle_enemies)
                        log("\tEnd of load_encounter")
                        return
                    encounterName = tree.item(tree.selection())["text"]
                else:
                    encounterName = encounter

                    # If the encounter clicked on is already displayed, no need to load it again,
                    # just shuffle the enemies.
                    if self.app.encounters[encounterName] == self.app.selected:
                        self.shuffle_enemies()
                        self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)
                        self.app.display.bind("<Button 1>", self.shuffle_enemies)
                        log("\tEnd of load_encounter")
                        return

                self.app.selected = self.app.encounters[encounterName]

                # Get the possible alternative enemies from the encounter's file.
                log("\tOpening " + baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + encounterName + str(self.app.numberOfCharacters) + ".json")
                with open(baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + encounterName + str(self.app.numberOfCharacters) + ".json") as alternativesFile:
                    alts = load(alternativesFile)

                self.app.selected["alternatives"] = []
                self.app.selected["enemySlots"] = alts["enemySlots"]
                self.newEnemies = []

                # Use only alternative enemies for expansions and enemies the user has activated in the settings.
                for expansionCombo in alts["alternatives"]:
                    if set(expansionCombo.split(",")).issubset(self.app.availableExpansions):
                        self.app.selected["alternatives"] += [alt for alt in alts["alternatives"][expansionCombo] if set(alt).issubset(self.app.enabledEnemies) and sum([1 for a in alt if enemyIds[a].expansions == set(["Phantoms"]) or enemyIds[a].name in {"Hungry Mimic", "Voracious Mimic"}]) <= self.app.settings["maxInvaders"]]

                self.newTiles = dict()

                if not customEnemyListCheck:
                    self.shuffle_enemies()
                    self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)
                    self.app.display.bind("<Button 1>", self.shuffle_enemies)

                log("\tEnd of load_encounter")
            except Exception as e:
                error_popup(self.root, e)
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

                self.app.display.bind("<Button 1>", do_nothing)
                if not self.app.selected:
                    log("\tNo encounter loaded - nothing to shuffle")
                    self.app.display.bind("<Button 1>", self.shuffle_enemies)
                    log("\tEnd of shuffle_enemies")
                    return

                self.rewardTreasure = None

                # Make sure a new set of enemies is chosen each time, otherwise it
                # feels like the program isn't doing anything.
                oldEnemies = [e for e in self.newEnemies]
                self.newEnemies = choice(self.app.selected["alternatives"])
                # Check to see if there are multiple alternatives.
                if len(set([tuple(a) for a in self.app.selected["alternatives"]])) > 1:
                    while self.newEnemies == oldEnemies:
                        self.newEnemies = choice(self.app.selected["alternatives"])

                self.edit_encounter_card(self.app.selected["name"], self.app.selected["expansion"], self.app.selected["level"], self.app.selected["enemySlots"])

                log("\tEnd of shuffle_enemies")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def edit_encounter_card(self, name, expansion, level, enemySlots, campaignGen=False, right=False):
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

            Optional Parameters:
                campaignGen: Boolean
                    Whether this call if from the v2 campaign generator.

                right: Boolean
                    Display on the right side of the display pane if True.
            """
            try:
                log("Start of edit_encounter_card, name={}, expansion={}, level={}, enemySlots={}, right={}".format(str(name), str(expansion), str(level), str(enemySlots), str(right)))

                displayPhotoImage = self.app.create_image(name + ".jpg", "encounter", level, expansion)

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
                            x = 116 + (43 * e) - (1 if "Phantoms" in enemyIds[self.newEnemies[s]].expansions else 0)
                            y = 78 + (47 * slotNum) - ((1 * (2 - slotNum)) if "Phantoms" in enemyIds[self.newEnemies[s]].expansions else 0)
                            imageType = "imageOldLevel4"
                        elif expansion in {"Dark Souls The Board Game", "Iron Keep", "Darkroot", "Explorers", "Executioner Chariot"}:
                            x = 67 + (40 * e)
                            y = 66 + (46 * slotNum)
                            imageType = "imageOld"
                        else:
                            x = 300 + (29 * e)
                            y = 323 + (29 * (slotNum - (0 if slotNum < 4 else 5 if slotNum < 7 else 8))) + (((1 if slotNum < 4 else 2 if slotNum < 7 else 3) - 1) * 122)
                            imageType = "imageNew"
                            
                        image = self.app.allEnemies[enemyIds[self.newEnemies[s]].name][imageType]

                        log("Pasting " + enemyIds[self.newEnemies[s]].name + " image onto encounter at " + str((x, y)) + ".")
                        self.app.displayImage.paste(im=image, box=(x, y), mask=image)
                        s += 1

                self.apply_keyword_tooltips(name, expansion, right=right)

                # These are new encounters that have text referencing specific enemies.
                if name == "Abandoned and Forgotten":
                    self.abandoned_and_forgotten()
                elif name == "Aged Sentinel":
                    self.aged_sentinel(right=right)
                elif name == "Castle Break In":
                    self.castle_break_in()
                elif (name == "Central Plaza" or name == "Central Plaza (TSC)") and expansion == "The Sunless City":
                    self.central_plaza(right=right)
                elif name == "Cloak and Feathers":
                    self.cloak_and_feathers(right=right)
                elif name == "Cold Snap":
                    self.cold_snap(right=right)
                elif name == "Corvian Host":
                    self.corvian_host(right=right)
                elif name == "Corrupted Hovel":
                    self.corrupted_hovel(right=right)
                elif name == "Dark Alleyway":
                    self.dark_alleyway(right=right)
                elif name == "Dark Resurrection":
                    self.dark_resurrection()
                elif name == "Deathly Freeze":
                    self.deathly_freeze(level, right=right)
                elif name == "Deathly Magic":
                    self.deathly_magic(level, right=right)
                elif name == "Deathly Tolls":
                    self.deathly_tolls(right=right)
                elif name == "Depths of the Cathedral":
                    self.depths_of_the_cathedral(right=right)
                elif name == "Distant Tower":
                    self.distant_tower(right=right)
                elif name == "Eye of the Storm":
                    self.eye_of_the_storm(right=right)
                elif name == "Flooded Fortress":
                    self.flooded_fortress(right=right)
                elif name == "Frozen Revolutions":
                    self.frozen_revolutions(right=right)
                elif name == "Giant's Coffin":
                    self.giants_coffin(right=right)
                elif name == "Gleaming Silver":
                    self.gleaming_silver(level, right=right)
                elif name == "Gnashing Beaks":
                    self.gnashing_beaks(right=right)
                elif name == "Grave Matters":
                    self.grave_matters()
                elif name == "Grim Reunion":
                    self.grim_reunion(right=right)
                elif name == "Hanging Rafters":
                    self.hanging_rafters()
                elif name == "In Deep Water":
                    self.in_deep_water(right=right)
                elif name == "Inhospitable Ground":
                    self.inhospitable_ground()
                elif name == "Lakeview Refuge":
                    self.lakeview_refuge(right=right)
                elif name == "Monstrous Maw":
                    self.monstrous_maw(right=right)
                elif name == "No Safe Haven":
                    self.no_safe_haven(right=right)
                elif name == "Painted Passage":
                    self.painted_passage()
                elif name == "Parish Church":
                    self.parish_church(right=right)
                elif name == "Parish Gates":
                    self.parish_gates(right=right)
                elif name == "Pitch Black":
                    self.pitch_black(level, right=right)
                elif name == "Puppet Master":
                    self.puppet_master(right=right)
                elif name == "Rain of Filth":
                    self.rain_of_filth()
                elif name == "Shattered Keep":
                    self.shattered_keep(right=right)
                elif name == "Skeletal Spokes":
                    self.skeletal_spokes(right=right)
                elif name == "Skeleton Overlord":
                    self.skeleton_overlord(right=right)
                elif name == "Tempting Maw":
                    self.tempting_maw(right=right)
                elif name == "The Abandoned Chest":
                    self.the_abandoned_chest(right=right)
                elif name == "The Beast From the Depths":
                    self.the_beast_from_the_depths(right=right)
                elif name == "The Bell Tower":
                    self.the_bell_tower(right=right)
                elif name == "The First Bastion":
                    self.the_first_bastion(level, right=right)
                elif name == "The Fountainhead":
                    self.the_fountainhead(right=right)
                elif name == "The Grand Hall":
                    self.the_grand_hall(right=right)
                elif name == "The Iron Golem":
                    self.the_iron_golem(right=right)
                elif name == "The Last Bastion":
                    self.the_last_bastion(level, right=right)
                elif name == "The Locked Grave":
                    self.the_locked_grave(right=right)
                elif name == "The Shine of Gold":
                    self.the_shine_of_gold(right=right)
                elif name == "The Skeleton Ball":
                    self.the_skeleton_ball(right=right)
                elif name == "Trecherous Tower":
                    self.trecherous_tower()
                elif name == "Trophy Room":
                    self.trophy_room(right=right)
                elif name == "Twilight Falls":
                    self.twilight_falls(right=right)
                elif name == "Undead Sanctum":
                    self.undead_sanctum(right=right)
                elif name == "Unseen Scurrying":
                    self.unseen_scurrying()
                elif name == "Urns of the Fallen":
                    self.urns_of_the_fallen()
                elif name == "Velka's Chosen":
                    self.velkas_chosen(level, right=right)

                displayPhotoImage = ImageTk.PhotoImage(self.app.displayImage)

                if right:
                    self.app.displayImages["encounters"][self.app.display2]["name"] = name
                    self.app.displayImages["encounters"][self.app.display2]["image"] = displayPhotoImage
                    self.app.displayImages["encounters"][self.app.display2]["activeTab"] = "encounters"
                    self.app.display2.image = displayPhotoImage
                    self.app.display2.config(image=displayPhotoImage)
                else:
                    self.app.displayImages["encounters"][self.app.display]["name"] = name
                    self.app.displayImages["encounters"][self.app.display]["image"] = displayPhotoImage
                    self.app.displayImages["encounters"][self.app.display]["activeTab"] = "encounters"
                    self.app.display.image = displayPhotoImage
                    self.app.display.config(image=displayPhotoImage)

                if not self.app.forPrinting and not campaignGen:
                    self.app.displayImages["encounters"][self.app.display]["name"] = name
                    self.app.displayImages["encounters"][self.app.display]["image"] = displayPhotoImage
                    self.app.displayImages["encounters"][self.app.display]["activeTab"] = "encounters"
                    self.app.display.config(image=displayPhotoImage)
                    self.app.display2.config(image="")
                    self.app.display3.config(image="")
                self.app.display.bind("<Button 1>", self.shuffle_enemies)

                log("\tEnd of edit_encounter_card")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def apply_keyword_tooltips(self, name, set, right=False):
            """
            If the encounter card has keywords, create an image of the word imposed over
            the original word and create a tooltip that shows up when mousing over the keyword image.
            """
            try:
                log("Start of apply_keyword_tooltips, name={}, set={}".format(str(name), str(set)))

                if not right:
                    for tooltip in self.app.tooltips:
                        tooltip.destroy()

                if not self.app.selected and self.app.notebook.tab(self.app.notebook.select(), "text") != "Campaign":
                    log("\tEnd of apply_keyword_tooltips (removed tooltips only)")
                    return

                for i, tooltip in enumerate(self.encounterTooltips.get((name, set), [])):
                    if not tooltip:
                        continue
                    self.app.create_tooltip(tooltipDict=tooltip, x=142, y=int(199 + (15.5 * i)), right=right)

                log("\tEnd of apply_keyword_tooltips")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def new_treasure_name(self, newTreasure):
            try:
                log("Start of new_treasure_name, newTreasure={}".format(str(newTreasure)))

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

                log("\tEnd of new_treasure_name, returning {}".format(str(treasureLines)))

                return treasureLines
            except Exception as e:
                error_popup(self.root, e)
                raise


        def abandoned_and_forgotten(self):
            try:
                log("Start of abandoned_and_forgotten")

                spawn1 = enemyIds[self.newEnemies[0]].name
                spawn2 = enemyIds[self.newEnemies[1]].name
                spawn3 = enemyIds[self.newEnemies[2]].name

                self.app.displayImage.paste(im=self.app.allEnemies[spawn1]["imageNew"], box=(285, 218), mask=self.app.allEnemies[spawn1]["imageNew"])
                self.app.displayImage.paste(im=self.app.allEnemies[spawn2]["imageNew"], box=(285, 248), mask=self.app.allEnemies[spawn2]["imageNew"])
                self.app.displayImage.paste(im=self.app.allEnemies[spawn3]["imageNew"], box=(285, 280), mask=self.app.allEnemies[spawn3]["imageNew"])

                log("\tEnd of abandoned_and_forgotten")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def aged_sentinel(self, right=False):
            try:
                log("Start of aged_sentinel")

                target = self.newTiles[1][1][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=143, y=231, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=203, y=255, right=right)

                log("\tEnd of aged_sentinel")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def castle_break_in(self):
            try:
                log("Start of castle_break_in")

                imageWithText = ImageDraw.Draw(self.app.displayImage)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 255), newTreasureLines[0], "black", font)
                imageWithText.text((21, 266), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of castle_break_in")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def central_plaza(self, right=False):
            try:
                log("Start of central_plaza")

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=143, y=262, right=right)

                log("\tEnd of central_plaza")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def cloak_and_feathers(self, right=False):
            try:
                log("Start of cloak_and_feathers")

                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)

                log("\tEnd of cloak_and_feathers")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def cold_snap(self, right=False):
            try:
                log("Start of cold_snap")

                target = self.newTiles[2][0][1]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=216, y=227, right=right)

                log("\tEnd of cold_snap")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def corrupted_hovel(self, right=False):
            try:
                log("Start of corrupted_hovel")

                target = [enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1] if (self.newTiles[1][0] + self.newTiles[1][1]).count(enemy) == 2][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=146, y=250, right=right)

                log("\tEnd of corrupted_hovel")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def corvian_host(self, right=False):
            try:
                log("Start of corvian_host")

                target = self.newTiles[1][1][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=161, y=238, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=263, y=238, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=261, y=251, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=189, y=276, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=145, y=288, right=right)

                imageWithText = ImageDraw.Draw(self.app.displayImage)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of corvian_host")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def dark_alleyway(self, right=False):
            try:
                log("Start of dark_alleyway")

                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)

                log("\tEnd of dark_alleyway")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def dark_resurrection(self):
            try:
                log("Start of dark_resurrection")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 235), newTreasureLines[0], "black", font)
                imageWithText.text((21, 246), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of dark_resurrection")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def deathly_freeze(self, level, right=False):
            try:
                log("Start of deathly_freeze")

                deathlyFreezeTile1 = [enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1]]
                deathlyFreezeTile2 = [enemy for enemy in self.newTiles[2][0] + self.newTiles[2][1]]
                overlap = set(deathlyFreezeTile1) & set(deathlyFreezeTile2)
                target = sorted([enemy for enemy in overlap if deathlyFreezeTile1.count(enemy) + deathlyFreezeTile2.count(enemy) == 2], key=lambda x: (-enemiesDict[x].difficultyTiers[level]["toughness"], enemiesDict[x].difficultyTiers[level]["difficulty"][self.app.numberOfCharacters]), reverse=True)[0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=141, y=242, right=right)

                log("\tEnd of deathly_freeze")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def deathly_magic(self, level, right=False):
            try:
                log("Start of deathly_magic")

                target = sorted([enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1] if (self.newTiles[1][0] + self.newTiles[1][1]).count(enemy) == 1], key=lambda x: enemiesDict[x].difficultyTiers[level]["difficulty"][self.app.numberOfCharacters], reverse=True)[0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=274, y=196, right=right)

                log("\tEnd of deathly_magic")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def deathly_tolls(self, right=False):
            try:
                log("Start of deathly_tolls")

                target = enemyIds[self.newEnemies[7]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=180, y=212, right=right)

                gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
                if gang == "Alonne":
                    tooltipDict = {"image" if self.app.forPrinting else "image" if self.app.forPrinting else "photo image": self.app.gangAlonne if self.app.forPrinting else self.app.gangAlonnePhoto, "imageName": "gang"}
                elif gang == "Hollow":
                    tooltipDict = {"image" if self.app.forPrinting else "image" if self.app.forPrinting else "photo image": self.app.gangHollow if self.app.forPrinting else self.app.gangHollowPhoto, "imageName": "gang"}
                elif gang == "Silver Knight":
                    tooltipDict = {"image" if self.app.forPrinting else "image" if self.app.forPrinting else "photo image": self.app.gangSilverKnight if self.app.forPrinting else self.app.gangSilverKnightPhoto, "imageName": "gang"}
                elif gang == "Skeleton":
                    tooltipDict = {"image" if self.app.forPrinting else "image" if self.app.forPrinting else "photo image": self.app.gangSkeleton if self.app.forPrinting else self.app.gangSkeletonPhoto, "imageName": "gang"}

                self.app.create_tooltip(tooltipDict=tooltipDict, x=142, y=245, right=right)

                log("\tEnd of deathly_tolls")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def depths_of_the_cathedral(self, right=False):
            try:
                log("Start of depths_of_the_cathedral")

                gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
                if gang == "Alonne":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangAlonne if self.app.forPrinting else self.app.gangAlonnePhoto, "imageName": "gang"}
                elif gang == "Hollow":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangHollow if self.app.forPrinting else self.app.gangHollowPhoto, "imageName": "gang"}
                elif gang == "Silver Knight":
                    tooltipDict = {"image" if self.app.forPrinting else "image" if self.app.forPrinting else "photo image": self.app.gangSilverKnight if self.app.forPrinting else self.app.gangSilverKnightPhoto, "imageName": "gang"}
                elif gang == "Skeleton":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangSkeleton if self.app.forPrinting else self.app.gangSkeletonPhoto, "imageName": "gang"}

                self.app.create_tooltip(tooltipDict=tooltipDict, x=142, y=214, right=right)

                log("\tEnd of depths_of_the_cathedral")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def distant_tower(self, right=False):
            try:
                log("Start of distant_tower")

                target = self.newTiles[3][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=217, y=213, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 283), newTreasureLines[0], "black", font)
                imageWithText.text((21, 294), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of distant_tower")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def eye_of_the_storm(self, right=False):
            try:
                log("Start of eye_of_the_storm")

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                fourTarget = [enemyIds[enemy].name for enemy in self.newEnemies if self.newEnemies.count(enemy) == 4]
                targets = list(set([enemyIds[enemy].name for enemy in self.newEnemies if self.newEnemies.count(enemy) == 2]))
                text1 = "Increase        "
                if fourTarget:
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[fourTarget[0]]["image text" if self.app.forPrinting else "photo image text"], "imageName": fourTarget[0]}
                    self.app.create_tooltip(tooltipDict=tooltipDict, x=187, y=255, right=right)
                else:
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[targets[0]]["image text" if self.app.forPrinting else "photo image text"], "imageName": targets[0]}
                    self.app.create_tooltip(tooltipDict=tooltipDict, x=187, y=255, right=right)
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[targets[1]]["image text" if self.app.forPrinting else "photo image text"], "imageName": targets[1]}
                    self.app.create_tooltip(tooltipDict=tooltipDict, x=232, y=255, right=right)
                    text1 += " and        "
                text1 += "block and resistance"
                text2 = "values by 1. Once these enemies have been"
                text3 = "killed, spawn the        on      , on tile 3."

                target = enemyIds[self.newEnemies[5]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=228, y=281, right=right)
                self.app.displayImage.paste(im=self.app.enemyNode2, box=(263, 281), mask=self.app.enemyNode2)
                imageWithText.text((140, 255), text1, "black", font)
                imageWithText.text((140, 268), text2, "black", font)
                imageWithText.text((140, 282), text3, "black", font)

                log("\tEnd of eye_of_the_storm")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def flooded_fortress(self, right=False):
            try:
                log("Start of flooded_fortress")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
                if gang == "Alonne":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangAlonne if self.app.forPrinting else self.app.gangAlonnePhoto, "imageName": "gang"}
                elif gang == "Hollow":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangHollow if self.app.forPrinting else self.app.gangHollowPhoto, "imageName": "gang"}
                elif gang == "Silver Knight":
                    tooltipDict = {"image" if self.app.forPrinting else "image" if self.app.forPrinting else "photo image": self.app.gangSilverKnight if self.app.forPrinting else self.app.gangSilverKnightPhoto, "imageName": "gang"}
                elif gang == "Skeleton":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangSkeleton if self.app.forPrinting else self.app.gangSkeletonPhoto, "imageName": "gang"}

                self.app.create_tooltip(tooltipDict=tooltipDict, x=142, y=215, right=right)

                log("\tEnd of flooded_fortress")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def frozen_revolutions(self, right=False):
            try:
                log("Start of frozen_revolutions")

                target = self.newTiles[3][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=143, y=227, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=143, y=243, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=354, y=243, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of frozen_revolutions")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def giants_coffin(self, right=False):
            try:
                log("Start of giants_coffin")

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=241, y=228, right=right)

                target = enemyIds[self.newEnemies[5]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=286, y=228, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of giants_coffin")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def gleaming_silver(self, level, right=False):
            try:
                log("Start of gleaming_silver")

                targets = [enemyIds[enemy].name for enemy in list(set(sorted(self.newEnemies, key=lambda x: enemyIds[x].difficultyTiers[level]["difficulty"][self.app.numberOfCharacters])[1:-1]))]

                for i, target in enumerate(targets):
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                    self.app.create_tooltip(tooltipDict=tooltipDict, x=144 + (i * 20), y=270, right=right)

                target = enemyIds[self.newEnemies[5]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=180, y=212, right=right)

                log("\tEnd of gleaming_silver")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def gnashing_beaks(self, right=False):
            try:
                log("Start of gnashing_beaks")

                target = enemyIds[self.newEnemies[2]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=314, y=232, right=right)

                target = enemyIds[self.newEnemies[3]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=338, y=232, right=right)

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=235, y=244, right=right)

                log("\tEnd of gnashing_beaks")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def grave_matters(self):
            try:
                log("Start of grave_matters")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of grave_matters")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def grim_reunion(self, right=False):
            try:
                log("Start of grim_reunion")

                target = enemyIds[self.newEnemies[10]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=219, y=196, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=269, y=255, right=right)

                log("\tEnd of grim_reunion")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def hanging_rafters(self):
            try:
                log("Start of hanging_rafters")

                imageWithText = ImageDraw.Draw(self.app.displayImage)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of hanging_rafters")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def in_deep_water(self, right=False):
            try:
                log("Start of in_deep_water")

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=239, y=198, right=right)

                target = enemyIds[self.newEnemies[5]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=323, y=198, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of in_deep_water")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def inhospitable_ground(self):
            try:
                log("Start of inhospitable_ground")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of inhospitable_ground")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def lakeview_refuge(self, right=False):
            try:
                log("Start of lakeview_refuge")

                target = enemyIds[self.newEnemies[-(self.app.numberOfCharacters + 1)]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=215, y=228, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=291, y=264, right=right)

                for i, enemy in enumerate(self.newEnemies[-self.app.numberOfCharacters:]):
                    target = enemyIds[enemy].name
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                    self.app.create_tooltip(tooltipDict=tooltipDict, x=181 + (20 * i), y=288, right=right)

                log("\tEnd of lakeview_refuge")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def monstrous_maw(self, right=False):
            try:
                log("Start of monstrous_maw")

                target = self.newTiles[1][1][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=210, y=196, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of monstrous_maw")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def no_safe_haven(self, right=False):
            try:
                log("Start of no_safe_haven")

                target = self.newTiles[2][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=63, y=147, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of no_safe_haven")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def painted_passage(self):
            try:
                log("Start of painted_passage")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of painted_passage")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def parish_church(self, right=False):
            try:
                log("Start of parish_church")

                target = enemyIds[self.newEnemies[10]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=180, y=198, right=right)

                log("\tEnd of parish_church")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def parish_gates(self, right=False):
            try:
                log("Start of parish_gates")

                target = enemyIds[self.newEnemies[3]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=301, y=220, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=188, y=255, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=144, y=280, right=right)

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=321, y=220, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=208, y=255, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=164, y=280, right=right)

                log("\tEnd of parish_gates")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def pitch_black(self, level, right=False):
            try:
                log("Start of pitch_black")

                tile1Enemies = self.newTiles[1][0] + self.newTiles[1][1]
                tile2Enemies = self.newTiles[2][0] + self.newTiles[2][1]
                target = sorted([enemy for enemy in tile1Enemies if tile1Enemies.count(enemy) == 1], key=lambda x: enemiesDict[x].difficultyTiers[level]["difficulty"][self.app.numberOfCharacters], reverse=True)[0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)
                target = sorted([enemy for enemy in tile2Enemies if tile2Enemies.count(enemy) == 1], key=lambda x: enemiesDict[x].difficultyTiers[level]["difficulty"][self.app.numberOfCharacters], reverse=True)[0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=222, y=147, right=right)

                log("\tEnd of pitch_black")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def puppet_master(self, right=False):
            try:
                log("Start of puppet_master")

                target = self.newTiles[1][0][1]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=64, y=148, right=right)
                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=145, y=196, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of puppet_master")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def rain_of_filth(self):
            try:
                log("Start of rain_of_filth")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of rain_of_filth")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def shattered_keep(self, right=False):
            try:
                log("Start of shattered_keep")
                
                targets = set([self.newTiles[1][0][1], self.newTiles[1][1][0], self.newTiles[1][1][1]])
                for i, target in enumerate(targets):
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                    self.app.create_tooltip(tooltipDict=tooltipDict, x=145 + (20 * i), y=213, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 255), newTreasureLines[0], "black", font)
                imageWithText.text((21, 266), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of shattered_keep")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def skeletal_spokes(self, right=False):
            try:
                log("Start of skeletal_spokes")

                target = self.newTiles[2][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=145, y=196, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=165, y=210, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=165, y=239, right=right)

                log("\tEnd of skeletal_spokes")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def skeleton_overlord(self, right=False):
            try:
                log("Start of skeleton_overlord")

                target = enemyIds[self.newEnemies[1]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=230, y=196, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=208, y=257, right=right)

                target = enemyIds[self.newEnemies[2]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=309, y=196, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=245, y=257, right=right)

                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=313, y=232, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=332, y=257, right=right)

                log("\tEnd of skeleton_overlord")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def tempting_maw(self, right=False):
            try:
                log("Start of tempting_maw")

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=224, y=145, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=220, y=197, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=346, y=256, right=right)

                log("\tEnd of tempting_maw")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def the_abandoned_chest(self, right=False):
            try:
                log("Start of the_abandoned_chest")

                target = enemyIds[self.newEnemies[4]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=322, y=195, right=right)

                target = enemyIds[self.newEnemies[5]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=144, y=208, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of the_abandoned_chest")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def the_beast_from_the_depths(self, right=False):
            try:
                log("Start of the_beast_from_the_depths")

                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=158, y=222, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of the_beast_from_the_depths")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def the_bell_tower(self, right=False):
            try:
                log("Start of the_bell_tower")

                target = enemyIds[self.newEnemies[2]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=321, y=195, right=right)

                target = enemyIds[self.newEnemies[3]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=341, y=195, right=right)

                log("\tEnd of the_bell_tower")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def the_first_bastion(self, level, right=False):
            try:
                log("Start of the_first_bastion")

                targets = sorted([enemyIds[enemy].name for enemy in self.newEnemies[-3:]], key=lambda x: (-enemiesDict[x].difficultyTiers[level]["toughness"], enemiesDict[x].difficultyTiers[level]["difficulty"][self.app.numberOfCharacters]))
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[targets[0]]["image text" if self.app.forPrinting else "photo image text"], "imageName": targets[0]}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=362, y=212, right=right)
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[targets[1]]["image text" if self.app.forPrinting else "photo image text"], "imageName": targets[1]}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=188, y=237, right=right)
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[targets[2]]["image text" if self.app.forPrinting else "photo image text"], "imageName": targets[2]}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=247, y=249, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=216, y=197, right=right)

                log("\tEnd of the_first_bastion")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def the_fountainhead(self, right=False):
            try:
                log("Start of the_fountainhead")

                gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
                if gang == "Alonne":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangAlonne if self.app.forPrinting else self.app.gangAlonnePhoto, "imageName": "gang"}
                elif gang == "Hollow":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangHollow if self.app.forPrinting else self.app.gangHollowPhoto, "imageName": "gang"}
                elif gang == "Silver Knight":
                    tooltipDict = {"image" if self.app.forPrinting else "image" if self.app.forPrinting else "photo image": self.app.gangSilverKnight if self.app.forPrinting else self.app.gangSilverKnightPhoto, "imageName": "gang"}
                elif gang == "Skeleton":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangSkeleton if self.app.forPrinting else self.app.gangSkeletonPhoto, "imageName": "gang"}

                self.app.create_tooltip(tooltipDict=tooltipDict, x=142, y=200, right=right)

                log("\tEnd of the_fountainhead")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def the_grand_hall(self, right=False):
            try:
                log("Start of the_grand_hall")

                target = enemyIds[self.newEnemies[7]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=180, y=213, right=right)

                log("\tEnd of the_grand_hall")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def the_iron_golem(self, right=False):
            try:
                log("Start of the_iron_golem")

                target = self.newTiles[1][1][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=188, y=196, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=174, y=219, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 266), newTreasureLines[0], "black", font)
                imageWithText.text((21, 277), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of the_iron_golem")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def the_last_bastion(self, level, right=False):
            try:
                log("Start of the_last_bastion")

                target = sorted([enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1]], key=lambda x: enemiesDict[x].difficultyTiers[level]["difficulty"][self.app.numberOfCharacters])[0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=215, y=227, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=316, y=250, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=337, y=263, right=right)

                log("\tEnd of the_last_bastion")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def the_locked_grave(self, right=False):
            try:
                log("Start of the_locked_grave")

                target = enemyIds[self.newEnemies[7]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=217, y=197, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=306, y=220, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of the_locked_grave")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def the_shine_of_gold(self, right=False):
            try:
                log("Start of the_shine_of_gold")

                target = self.newTiles[1][1][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=207, y=219, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=280, y=254, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=250, y=268, right=right)

                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=268, y=195)

                log("\tEnd of the_shine_of_gold")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def the_skeleton_ball(self, right=False):
            try:
                log("Start of the_skeleton_ball")

                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=64, y=148, right=right)
                target = self.newTiles[3][1][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=222, y=148, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of the_skeleton_ball")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def trecherous_tower(self):
            try:
                log("Start of trecherous_tower")

                spawn1 = enemyIds[self.newEnemies[2]].name
                spawn2 = enemyIds[self.newEnemies[3]].name
                spawn3 = enemyIds[self.newEnemies[4]].name

                self.app.displayImage.paste(im=self.app.allEnemies[spawn1]["imageNew"], box=(285, 218), mask=self.app.allEnemies[spawn1]["imageNew"])
                self.app.displayImage.paste(im=self.app.allEnemies[spawn2]["imageNew"], box=(285, 248), mask=self.app.allEnemies[spawn2]["imageNew"])
                self.app.displayImage.paste(im=self.app.allEnemies[spawn3]["imageNew"], box=(285, 280), mask=self.app.allEnemies[spawn3]["imageNew"])

                log("\tEnd of trecherous_tower")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def trophy_room(self, right=False):
            try:
                log("Start of trophy_room")

                targets = set([self.newTiles[2][0][0], self.newTiles[2][1][0]])
                for i, target in enumerate(targets):
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                    self.app.create_tooltip(tooltipDict=tooltipDict, x=61 + (20 * i), y=147, right=right)
                    self.app.create_tooltip(tooltipDict=tooltipDict, x=210 + (20 * i), y=197, right=right)
                    self.app.create_tooltip(tooltipDict=tooltipDict, x=145 + (20 * i), y=244, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of trophy_room")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def twilight_falls(self, right=False):
            try:
                log("Start of twilight_falls")

                gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
                if gang == "Alonne":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangAlonne if self.app.forPrinting else self.app.gangAlonnePhoto, "imageName": "gang"}
                elif gang == "Hollow":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangHollow if self.app.forPrinting else self.app.gangHollowPhoto, "imageName": "gang"}
                elif gang == "Silver Knight":
                    tooltipDict = {"image" if self.app.forPrinting else "image" if self.app.forPrinting else "photo image": self.app.gangSilverKnight if self.app.forPrinting else self.app.gangSilverKnightPhoto, "imageName": "gang"}
                elif gang == "Skeleton":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangSkeleton if self.app.forPrinting else self.app.gangSkeletonPhoto, "imageName": "gang"}

                self.app.create_tooltip(tooltipDict=tooltipDict, x=142, y=214, right=right)

                log("\tEnd of twilight_falls")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def undead_sanctum(self, right=False):
            try:
                log("Start of undead_sanctum")

                gang = Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
                if gang == "Alonne":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangAlonne if self.app.forPrinting else self.app.gangAlonnePhoto, "imageName": "gang"}
                elif gang == "Hollow":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangHollow if self.app.forPrinting else self.app.gangHollowPhoto, "imageName": "gang"}
                elif gang == "Silver Knight":
                    tooltipDict = {"image" if self.app.forPrinting else "image" if self.app.forPrinting else "photo image": self.app.gangSilverKnight if self.app.forPrinting else self.app.gangSilverKnightPhoto, "imageName": "gang"}
                elif gang == "Skeleton":
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.gangSkeleton if self.app.forPrinting else self.app.gangSkeletonPhoto, "imageName": "gang"}

                self.app.create_tooltip(tooltipDict=tooltipDict, x=142, y=214, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of undead_sanctum")
            except Exception as e:
                error_popup(self.root, e)
                raise

        def unseen_scurrying(self):
            try:
                log("Start of unseen_scurrying")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of unseen_scurrying")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def urns_of_the_fallen(self):
            try:
                log("Start of urns_of_the_fallen")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of urns_of_the_fallen")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def velkas_chosen(self, level, right=False):
            try:
                log("Start of velkas_chosen")

                target = sorted([enemy for enemy in self.newTiles[2][0] + self.newTiles[2][1]], key=lambda x: enemiesDict[x].difficultyTiers[level]["difficulty"][self.app.numberOfCharacters], reverse=True)[0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=298, y=195, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=205, y=219, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of velkas_chosen")
            except Exception as e:
                error_popup(self.root, e)
                raise

except Exception as e:
    log(e, exception=True)
    raise