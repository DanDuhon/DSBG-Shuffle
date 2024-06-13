try:
    import datetime
    import os
    import requests
    import sys
    import tkinter as tk
    import webbrowser
    from json import load
    from PIL import Image, ImageTk
    from tkinter import ttk

    from dsbg_shuffle_behavior_decks import BehaviorDeckFrame
    from dsbg_shuffle_campaign import CampaignFrame
    from dsbg_shuffle_encounters import EncountersFrame
    from dsbg_shuffle_enemies import enemyIds, enemiesDict, bosses
    from dsbg_shuffle_events import EventsFrame
    from dsbg_shuffle_settings import SettingsWindow
    from dsbg_shuffle_tooltip_reference import tooltipText
    from dsbg_shuffle_treasure import generate_treasure_soul_cost, populate_treasure_tiers, treasures
    from dsbg_shuffle_utility import CreateToolTip, PopupWindow, enable_binding, center, do_nothing, log, error_popup, baseFolder, pathSep
    from dsbg_shuffle_variants import VariantsFrame


    class Application(ttk.Frame):
        def __init__(self, parent):
            try:
                log("Initiating application")

                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep)) as settingsFile:
                    self.settings = load(settingsFile)

                with open(baseFolder + "\\lib\\dsbg_shuffle_encounters.json".replace("\\", pathSep)) as encountersFile:
                    self.encounters = load(encountersFile)

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
                if "Phantoms" in self.availableExpansions:
                    self.enabledEnemies = self.enabledEnemies.union(set([enemy for enemy in enemyIds if "Phantoms" in enemyIds[enemy].expansions]))
                self.charactersActive = set(self.settings["charactersActive"])
                self.numberOfCharacters = len(self.charactersActive)
                self.availableCoreSets = self.coreSets & self.availableExpansions

                self.allEnemies = {enemy: {} for enemy in enemiesDict}

                root.withdraw()
                i = 0
                self.progress = PopupWindow(root, labelText="Starting up...", progressBar=True, progressMax=(len(self.allEnemies)*6) + (len(list(enemiesDict.keys()) + list(bosses.keys()))*3) + len([t for t in treasures if not treasures[t]["character"] or treasures[t]["character"] in self.charactersActive]), loadingImage=True)

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

                # Create images
                self.progress.label.config(text = "Loading images... ")
                # Enemies
                for enemy in self.allEnemies:
                    i += 6
                    self.progress.progressVar.set(i)
                    root.update_idletasks()
                    self.allEnemies[enemy]["imageOld"] = self.create_image(enemy + ".png", "enemyOld")
                    self.allEnemies[enemy]["imageOldLevel4"] = self.create_image(enemy + ".png", "enemyOldLevel4")
                    self.allEnemies[enemy]["imageNew"] = self.create_image(enemy + ".png", "enemyNew")
                    self.allEnemies[enemy]["image text"] = self.create_image(enemy + ".png", "enemyText")
                    self.allEnemies[enemy]["image text" if self.forPrinting else "photo image text"] = ImageTk.PhotoImage(self.create_image(enemy + ".png", "enemyText"))
                
                self.progress.label.config(text="Loading treasure...")
                if self.settings["treasureSwapOption"] in {"Similar Soul Cost", "Tier Based"}:
                    generate_treasure_soul_cost(self.availableExpansions, self.charactersActive, root, self.progress)
                i = len([t for t in treasures if not treasures[t]["character"] or treasures[t]["character"] in self.charactersActive])
                if self.settings["treasureSwapOption"] == "Tier Based":
                    populate_treasure_tiers(self.availableExpansions, self.charactersActive)

                # Icons
                self.enemyNode2 = self.create_image("enemy_node_2.png", "enemyNode")
                self.attack = {
                    "physical": {},
                    "magic": {},
                    "push": {}
                }
                for x in range(2, 14):
                    for y in ["physical", "magic", "push"]:
                        self.attack[y][x] = self.create_image("attack_" + y + "_" + str(x) + ".png", y if y == "push" else "attack")
                self.bleed = self.create_image("bleed.png", "bleed")
                self.frostbite = self.create_image("frostbite.png", "frostbite")
                self.poison = self.create_image("poison.png", "poison")
                self.stagger = self.create_image("stagger.png", "stagger")
                self.corrosion = self.create_image("corrosion.png", "corrosion")
                self.calamity = self.create_image("calamity.png", "calamity")
                self.repeat = {}
                for x in range(2, 6):
                    self.repeat[x] = self.create_image("repeat_" + str(x) + ".png", "repeat")
                self.sksMove = self.create_image("sks_move.png", "move")
                self.phalanxMove = self.create_image("phalanx_move.png", "move")

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

                self.create_tabs()
                self.create_buttons()
                self.create_display_frame()
                self.create_menu()
                self.set_bindings_buttons_menus(True)

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
                self.paned.grid_rowconfigure(index=0, weight=1)
                self.paned.grid(row=1, column=0, pady=(5, 5), padx=(5, 5), sticky="nsew", columnspan=4)

                self.pane = ttk.Frame(self.paned, padding=5)
                self.pane.grid_rowconfigure(index=0, weight=1)
                self.paned.add(self.pane, weight=1)

                self.notebook = ttk.Notebook(self.paned, width=600)
                self.notebook.pack(fill="both", expand=True)

                self.campaignTab = CampaignFrame(root=root, app=self)
                self.notebook.add(self.campaignTab, text="Campaign")
                
                self.eventTab = EventsFrame(root=root, app=self)
                self.notebook.add(self.eventTab, text="Events")

                self.variantsTab = VariantsFrame(root=root, app=self)
                self.notebook.add(self.variantsTab, text="Behavior Variants")

                self.behaviorDeckTab = BehaviorDeckFrame(root=root, app=self)
                self.notebook.add(self.behaviorDeckTab, text="Behavior Decks")

                self.encounterTab = EncountersFrame(root=root, app=self)
                for index in [0, 1]:
                    self.encounterTab.columnconfigure(index=index, weight=1)
                    self.encounterTab.rowconfigure(index=index, weight=1)
                self.notebook.insert(0, self.encounterTab, text="Encounters")

                self.notebook.select(0)

                log("End of create_tabs")
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

                self.display = ttk.Label(self.displayFrame)
                self.display.grid(column=0, row=0, sticky="nsew")
                self.display2 = ttk.Label(self.displayFrame)
                self.display2.grid(column=1, row=0, sticky="nsew")
                self.display3 = ttk.Label(self.displayFrame)
                self.display3.grid(column=1, row=1, sticky="nsew")

                log("End of create_display_frame")
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

                self.buttons = set()
                self.l1 = ttk.Button(self.buttonsFrame, text="Random Level 1", width=16, command=lambda x=1: self.encounterTab.random_encounter(level=x))
                self.l2 = ttk.Button(self.buttonsFrame, text="Random Level 2", width=16, command=lambda x=2: self.encounterTab.random_encounter(level=x))
                self.l3 = ttk.Button(self.buttonsFrame, text="Random Level 3", width=16, command=lambda x=3: self.encounterTab.random_encounter(level=x))
                self.l4 = ttk.Button(self.buttonsFrame, text="Random Level 4", width=16, command=lambda x=4: self.encounterTab.random_encounter(level=x))
                if "level4" not in self.settings["encounterTypes"]:
                    self.l4["state"] = "disabled"
                if ["level4"] == self.settings["encounterTypes"]:
                    self.l1["state"] = "disabled"
                    self.l2["state"] = "disabled"
                    self.l3["state"] = "disabled"
                self.l5 = ttk.Button(self.buttonsFrame, text="Add to Campaign", width=16, command=self.campaignTab.add_card_to_campaign)
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

                # Link to the wiki
                wikiLink = ttk.Button(self.buttonsFrame, text="Open the wiki", width=16, command=self.open_wiki)
                wikiLink.grid(column=1, row=1)
                
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

                s = SettingsWindow(root, self.coreSets)

                self.wait_window(s.top)

                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep)) as settingsFile:
                    self.settings = load(settingsFile)

                if self.settings != oldSettings:
                    self.selected = None
                    self.rewardTreasure = None
                    self.display.config(image="")
                    self.display2.config(image="")
                    self.display3.config(image="")
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
                    if (oldTreasureSwapOption != self.settings["treasureSwapOption"] and self.settings["treasureSwapOption"] in {"Similar Soul Cost", "Tier Based"}) or (oldCustomEnemyList != self.settings["customEnemyList"] and self.settings["customEnemyList"]):
                        i = 0
                        progress = PopupWindow(root, labelText="Reloading treasure...", progressBar=True, progressMax=len([t for t in treasures if not treasures[t]["character"] or treasures[t]["character"] in self.charactersActive]), loadingImage=True)
                        if oldTreasureSwapOption != self.settings["treasureSwapOption"] and self.settings["treasureSwapOption"] in {"Similar Soul Cost", "Tier Based"}:
                            i = generate_treasure_soul_cost(self.availableExpansions, self.charactersActive, root, progress)
                            if self.settings["treasureSwapOption"] == "Tier Based":
                                populate_treasure_tiers(self.availableExpansions, self.charactersActive)
                        progress.destroy()
                    
                    if oldCustomEnemyList != self.settings["customEnemyList"] and self.settings["customEnemyList"]:
                        i = 0
                        progress = PopupWindow(root, labelText="Applying custom enemy list...", progressBar=True, progressMax=len(self.encounterTab.encounterList), loadingImage=True)
                        
                        self.enabledEnemies = set([enemiesDict[enemy.replace(" (V1)", "")].id for enemy in self.settings["enabledEnemies"] if enemy not in self.allExpansions])
                        if "Phantoms" in self.availableExpansions:
                            self.enabledEnemies = self.enabledEnemies.union(set([enemy for enemy in enemyIds if "Phantoms" in enemyIds[enemy].expansions]))

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
                log("Start of create_image, imageFileName={}, imageType={}, level={}, expansion={}".format(str(imageFileName), str(imageType), str(level), str(expansion)))

                if imageType == "encounter":
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

                    fileName = imageFileName[:-4]
                    if expansion == "The Sunless City" and imageFileName[:-4] in set(["Broken Passageway", "Central Plaza"]):
                        fileName += " (TSC)"
                    fileName += ".jpg"

                    imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\".replace("\\", pathSep) + fileName
                    log("\tOpening " + imagePath)
                    self.displayImage = Image.open(imagePath).resize((width, height), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.displayImage)
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
                            image = Image.open(imagePath).resize((34, 34), Image.Resampling.LANCZOS)
                        else:
                            image = Image.open(imagePath).resize((32, 32), Image.Resampling.LANCZOS)
                    elif imageType == "enemyNew":
                        image = Image.open(imagePath).resize((22, 22), Image.Resampling.LANCZOS)
                    elif imageType == "resurrection":
                        image = Image.open(imagePath).resize((9, 17), Image.Resampling.LANCZOS)
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
                        image = Image.open(imagePath).resize((44, 50), Image.Resampling.LANCZOS)
                    elif imageType == "frostbite":
                        image = Image.open(imagePath).resize((55, 56), Image.Resampling.LANCZOS)
                    elif imageType == "poison":
                        image = Image.open(imagePath).resize((37, 50), Image.Resampling.LANCZOS)
                    elif imageType == "stagger":
                        image = Image.open(imagePath).resize((52, 56), Image.Resampling.LANCZOS)
                    elif imageType == "calamity":
                        image = Image.open(imagePath).resize((51, 50), Image.Resampling.LANCZOS)
                    elif imageType == "corrosion":
                        image = Image.open(imagePath).resize((49, 50), Image.Resampling.LANCZOS)
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
