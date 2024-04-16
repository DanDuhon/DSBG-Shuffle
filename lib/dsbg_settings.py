try:
    import platform
    import tkinter as tk
    from tkinter import ttk
    from os import path
    from json import load, dump

    from dsbg_characters import soulCost
    from dsbg_utility import VerticalScrolledFrame, CreateToolTip, center, log


    if platform.system() == "Windows":
        pathSep = "\\"
    else:
        pathSep = "/"

    baseFolder = path.dirname(__file__).replace("\\lib".replace("\\", pathSep), "")


    class SettingsWindow(object):
        """
        Window in which the user selects which expansions they own and whether they want to see
        V1, V1, or both styles of encounters when being shown encounters.
        """
        def __init__(self, root, coreSets):
            try:
                log("Creating settings window")
                self.root = root
                top = self.top = tk.Toplevel(root)
                top.attributes('-alpha', 0.0)
                top.wait_visibility()
                top.grab_set_global()

                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep)) as settingsFile:
                    self.settings = load(settingsFile)

                self.availableExpansions = set(self.settings["availableExpansions"])
                self.enabledEnemies = self.settings["enabledEnemies"]
                self.coreSets = coreSets

                self.notebook = ttk.Notebook(top)
                self.notebook.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=4, columnspan=2)

                self.create_expansion_tab()
                self.create_enemies_tab()
                self.create_characters_pane(top)
                self.create_invaders_pane(top)
                self.create_treasure_swap_pane(top)
                self.create_shown_encounters_pane(top)
                self.create_update_check_pane(top)
                self.create_buttons(top)

                self.errLabel = ttk.Label(self.top, text="")
                self.errLabel.grid(column=0, row=4, padx=18, columnspan=8)

                center(top)
                top.attributes('-alpha', 1.0)
            except Exception as e:
                log(e, exception=True)
                raise


        def create_expansion_tab(self):
            try:
                log("Start of create_expansion_tab")

                # These are the only expansions that matter - the ones that add enemies, regular treasure, or characters.
                self.expansions = {
                    "Painted World of Ariamis": {"button": None, "value": tk.IntVar(), "displayName": "Painted World of Ariamis (V2 Core Set)"},
                    "The Sunless City": {"button": None, "value": tk.IntVar(), "displayName": "The Sunless City (V2 Core Set)"},
                    "Tomb of Giants": {"button": None, "value": tk.IntVar(), "displayName": "Tomb of Giants (V2 Core Set)"},
                    "Dark Souls The Board Game": {"button": None, "value": tk.IntVar(), "displayName": "Dark Souls The Board Game (V1 Core Set)"},
                    "Darkroot": {"button": None, "value": tk.IntVar(), "displayName": "Darkroot (V1)"},
                    "Explorers": {"button": None, "value": tk.IntVar(), "displayName": "Explorers (V1)"},
                    "Iron Keep": {"button": None, "value": tk.IntVar(), "displayName": "Iron Keep (V1)"},
                    "Phantoms": {"button": None, "value": tk.IntVar(), "displayName": "Phantoms (V1)"},
                    "Executioner Chariot": {"button": None, "value": tk.IntVar(), "displayName": "Executioner Chariot (V1)"},
                    "Characters Expansion": {"button": None, "value": tk.IntVar(), "displayName": "Characters Expansion (V1)"}
                }

                self.expansionTab = VerticalScrolledFrame(self.notebook)
                self.notebook.add(self.expansionTab, text="Enabled Expansions")

                for i, expansion in enumerate(self.expansions):
                    self.expansions[expansion]["button"] = ttk.Checkbutton(self.expansionTab.interior, text=self.expansions[expansion]["displayName"], variable=self.expansions[expansion]["value"], command=lambda expansion=expansion: self.toggle_expansion(expansion=expansion))
                    self.expansions[expansion]["button"].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")
                    
                self.expansions["Phantoms"]["value"].set(1 if "Phantoms" in self.settings["availableExpansions"] else 0)
                self.expansions["Characters Expansion"]["value"].set(1 if "Characters Expansion" in self.settings["availableExpansions"] else 0)

                log("End of create_expansion_tab")
            except Exception as e:
                log(e, exception=True)
                raise


        def create_enemies_tab(self):
            try:
                log("Start of create_enemies_tab")

                self.enemies = {
                    "Painted World of Ariamis": {"button": None, "value": tk.IntVar(), "parent": None, "children": [], "displayName": "Painted World of Ariamis (V2)"},
                    "Bonewheel Skeleton": {"button": None, "value": tk.IntVar(), "parent": "Painted World of Ariamis", "children": [], "displayName": "Bonewheel Skeleton"},
                    "Crow Demon": {"button": None, "value": tk.IntVar(), "parent": "Painted World of Ariamis", "children": [], "displayName": "Crow Demon"},
                    "Engorged Zombie": {"button": None, "value": tk.IntVar(), "parent": "Painted World of Ariamis", "children": [], "displayName": "Engorged Zombie"},
                    "Phalanx": {"button": None, "value": tk.IntVar(), "parent": "Painted World of Ariamis", "children": [], "displayName": "Phalanx"},
                    "Phalanx Hollow": {"button": None, "value": tk.IntVar(), "parent": "Painted World of Ariamis", "children": [], "displayName": "Phalanx Hollow"},
                    "Snow Rat": {"button": None, "value": tk.IntVar(), "parent": "Painted World of Ariamis", "children": [], "displayName": "Snow Rat"},
                    "The Sunless City": {"button": None, "value": tk.IntVar(), "parent": None, "children": [], "displayName": "The Sunless City (V2)"},
                    "Crossbow Hollow": {"button": None, "value": tk.IntVar(), "parent": "The Sunless City", "children": [], "displayName": "Crossbow Hollow"},
                    "Hollow Soldier": {"button": None, "value": tk.IntVar(), "parent": "The Sunless City", "children": [], "displayName": "Hollow Soldier"},
                    "Mimic": {"button": None, "value": tk.IntVar(), "parent": "The Sunless City", "children": [], "displayName": "Mimic"},
                    "Sentinel": {"button": None, "value": tk.IntVar(), "parent": "The Sunless City", "children": [], "displayName": "Sentinel"},
                    "Silver Knight Greatbowman": {"button": None, "value": tk.IntVar(), "parent": "The Sunless City", "children": [], "displayName": "Silver Knight Greatbowman"},
                    "Silver Knight Swordsman": {"button": None, "value": tk.IntVar(), "parent": "The Sunless City", "children": [], "displayName": "Silver Knight Swordsman"},
                    "Tomb of Giants": {"button": None, "value": tk.IntVar(), "parent": None, "children": [], "displayName": "Tomb of Giants (V2)"},
                    "Giant Skeleton Archer": {"button": None, "value": tk.IntVar(), "parent": "Tomb of Giants", "children": [], "displayName": "Giant Skeleton Archer"},
                    "Giant Skeleton Soldier": {"button": None, "value": tk.IntVar(), "parent": "Tomb of Giants", "children": [], "displayName": "Giant Skeleton Soldier"},
                    "Necromancer": {"button": None, "value": tk.IntVar(), "parent": "Tomb of Giants", "children": [], "displayName": "Necromancer"},
                    "Skeleton Archer": {"button": None, "value": tk.IntVar(), "parent": "Tomb of Giants", "children": [], "displayName": "Skeleton Archer"},
                    "Skeleton Beast": {"button": None, "value": tk.IntVar(), "parent": "Tomb of Giants", "children": [], "displayName": "Skeleton Beast"},
                    "Skeleton Soldier": {"button": None, "value": tk.IntVar(), "parent": "Tomb of Giants", "children": [], "displayName": "Skeleton Soldier"},
                    "Dark Souls The Board Game": {"button": None, "value": tk.IntVar(), "parent": None, "children": [], "displayName": "Dark Souls The Board Game (V1)              "},
                    "Crossbow Hollow (V1)": {"button": None, "value": tk.IntVar(), "parent": "Dark Souls The Board Game", "children": [], "displayName": "Crossbow Hollow (V1)"},
                    "Hollow Soldier (V1)": {"button": None, "value": tk.IntVar(), "parent": "Dark Souls The Board Game", "children": [], "displayName": "Hollow Soldier (V1)"},
                    "Large Hollow Soldier (V1)": {"button": None, "value": tk.IntVar(), "parent": "Dark Souls The Board Game", "children": [], "displayName": "Large Hollow Soldier (V1)"},
                    "Sentinel (V1)": {"button": None, "value": tk.IntVar(), "parent": "Dark Souls The Board Game", "children": [], "displayName": "Sentinel (V1)"},
                    "Silver Knight Greatbowman (V1)": {"button": None, "value": tk.IntVar(), "parent": "Dark Souls The Board Game", "children": [], "displayName": "Silver Knight Greatbowman (V1)"},
                    "Silver Knight Swordsman (V1)": {"button": None, "value": tk.IntVar(), "parent": "Dark Souls The Board Game", "children": [], "displayName": "Silver Knight Swordsman (V1)"},
                    "Darkroot": {"button": None, "value": tk.IntVar(), "parent": None, "children": [], "displayName": "Darkroot (V1)"},
                    "Demonic Foliage (V1)": {"button": None, "value": tk.IntVar(), "parent": "Darkroot", "children": [], "displayName": "Demonic Foliage (V1)"},
                    "Mushroom Child (V1)": {"button": None, "value": tk.IntVar(), "parent": "Darkroot", "children": [], "displayName": "Mushroom Child (V1)"},
                    "Mushroom Parent (V1)": {"button": None, "value": tk.IntVar(), "parent": "Darkroot", "children": [], "displayName": "Mushroom Parent (V1)"},
                    "Plow Scarecrow (V1)": {"button": None, "value": tk.IntVar(), "parent": "Darkroot", "children": [], "displayName": "Plow Scarecrow (V1)"},
                    "Shears Scarecrow (V1)": {"button": None, "value": tk.IntVar(), "parent": "Darkroot", "children": [], "displayName": "Shears Scarecrow (V1)"},
                    "Stone Guardian (V1)": {"button": None, "value": tk.IntVar(), "parent": "Darkroot", "children": [], "displayName": "Stone Guardian (V1)"},
                    "Stone Knight (V1)": {"button": None, "value": tk.IntVar(), "parent": "Darkroot", "children": [], "displayName": "Stone Knight (V1)"},
                    "Executioner Chariot": {"button": None, "value": tk.IntVar(), "parent": None, "children": [], "displayName": "Executioner Chariot (V1)"},
                    "Black Hollow Mage (V1)": {"button": None, "value": tk.IntVar(), "parent": "Executioner Chariot", "children": [], "displayName": "Black Hollow Mage (V1)"},
                    "Falchion Skeleton (V1)": {"button": None, "value": tk.IntVar(), "parent": "Executioner Chariot", "children": [], "displayName": "Falchion Skeleton (V1)"},
                    "Explorers": {"button": None, "value": tk.IntVar(), "parent": None, "children": [], "displayName": "Explorers (V1)"},
                    "Firebomb Hollow (V1)": {"button": None, "value": tk.IntVar(), "parent": "Explorers", "children": [], "displayName": "Firebomb Hollow (V1)"},
                    "Hungry Mimic (V1)": {"button": None, "value": tk.IntVar(), "parent": "Explorers", "children": [], "displayName": "Hungry Mimic (V1)"},
                    "Voracious Mimic (V1)": {"button": None, "value": tk.IntVar(), "parent": "Explorers", "children": [], "displayName": "Voracious Mimic (V1)"},
                    "Silver Knight Spearman (V1)": {"button": None, "value": tk.IntVar(), "parent": "Explorers", "children": [], "displayName": "Silver Knight Spearman (V1)"},
                    "Iron Keep": {"button": None, "value": tk.IntVar(), "parent": None, "children": [], "displayName": "Iron Keep (V1)"},
                    "Alonne Bow Knight (V1)": {"button": None, "value": tk.IntVar(), "parent": "Iron Keep", "children": [], "displayName": "Alonne Bow Knight (V1)"},
                    "Alonne Knight Captain (V1)": {"button": None, "value": tk.IntVar(), "parent": "Iron Keep", "children": [], "displayName": "Alonne Knight Captain (V1)"},
                    "Alonne Sword Knight (V1)": {"button": None, "value": tk.IntVar(), "parent": "Iron Keep", "children": [], "displayName": "Alonne Sword Knight (V1)"},
                    "Ironclad Soldier (V1)": {"button": None, "value": tk.IntVar(), "parent": "Iron Keep", "children": [], "displayName": "Ironclad Soldier (V1)"},
                    "Phantoms": {"button": None, "value": tk.IntVar(), "parent": None, "children": [], "displayName": "Phantoms (V1)"},
                    "Armorer Dennis (V1)": {"button": None, "value": tk.IntVar(), "parent": "Phantoms", "children": [], "displayName": "Armorer Dennis (V1)"},
                    "Fencer Sharron (V1)": {"button": None, "value": tk.IntVar(), "parent": "Phantoms", "children": [], "displayName": "Fencer Sharron (V1)"},
                    "Invader Brylex (V1)": {"button": None, "value": tk.IntVar(), "parent": "Phantoms", "children": [], "displayName": "Invader Brylex (V1)"},
                    "Kirk, Knight of Thorns (V1)": {"button": None, "value": tk.IntVar(), "parent": "Phantoms", "children": [], "displayName": "Kirk, Knight of Thorns (V1)"},
                    "Longfinger Kirk (V1)": {"button": None, "value": tk.IntVar(), "parent": "Phantoms", "children": [], "displayName": "Longfinger Kirk (V1)"},
                    "Maldron the Assassin (V1)": {"button": None, "value": tk.IntVar(), "parent": "Phantoms", "children": [], "displayName": "Maldron the Assassin (V1)"},
                    "Maneater Mildred (V1)": {"button": None, "value": tk.IntVar(), "parent": "Phantoms", "children": [], "displayName": "Maneater Mildred (V1)"},
                    "Marvelous Chester (V1)": {"button": None, "value": tk.IntVar(), "parent": "Phantoms", "children": [], "displayName": "Marvelous Chester (V1)"},
                    "Melinda the Butcher (V1)": {"button": None, "value": tk.IntVar(), "parent": "Phantoms", "children": [], "displayName": "Melinda the Butcher (V1)"},
                    "Oliver the Collector (V1)": {"button": None, "value": tk.IntVar(), "parent": "Phantoms", "children": [], "displayName": "Oliver the Collector (V1)"},
                    "Paladin Leeroy (V1)": {"button": None, "value": tk.IntVar(), "parent": "Phantoms", "children": [], "displayName": "Paladin Leeroy (V1)"},
                    "Xanthous King Jeremiah (V1)": {"button": None, "value": tk.IntVar(), "parent": "Phantoms", "children": [], "displayName": "Xanthous King Jeremiah (V1)"},
                }

                self.enemiesTab = VerticalScrolledFrame(self.notebook)
                self.enemiesTab.grid_propagate(False)
                self.notebook.add(self.enemiesTab, text="Enabled Enemies")
                
                for i, enemy in enumerate(self.enemies):
                    if self.enemies[enemy]["parent"]:
                        self.enemies[self.enemies[enemy]["parent"]]["children"].append(enemy)
                    else:
                        # Indent children for better visual organization.
                        tk.Label(self.enemiesTab.interior, text="\t").grid(column=0, row=i)

                    self.enemies[enemy]["button"] = ttk.Checkbutton(self.enemiesTab.interior, text=self.enemies[enemy]["displayName"], variable=self.enemies[enemy]["value"], command=lambda enemy=enemy: self.toggle_parent_children(enemy=enemy))
                    self.enemies[enemy]["button"].grid(row=i, column=0 if not self.enemies[enemy]["parent"] else 1, columnspan=2 if not self.enemies[enemy]["parent"] else 3, padx=5, pady=1, sticky="nsew")

                for enemy in self.enabledEnemies:
                    self.enemies[enemy]["value"].set(1)
                    self.toggle_parent_children(enemy=enemy)

                log("End of create_enemies_tab")
            except Exception as e:
                log(e, exception=True)
                raise


        def create_characters_pane(self, parent):
            try:
                log("Start of create_characters_pane")

                self.charactersActive = {
                    "Assassin": {"button": None, "value": tk.IntVar()},
                    "Cleric": {"button": None, "value": tk.IntVar()},
                    "Deprived": {"button": None, "value": tk.IntVar()},
                    "Herald": {"button": None, "value": tk.IntVar()},
                    "Knight": {"button": None, "value": tk.IntVar()},
                    "Mercenary": {"button": None, "value": tk.IntVar()},
                    "Pyromancer": {"button": None, "value": tk.IntVar()},
                    "Sorcerer": {"button": None, "value": tk.IntVar()},
                    "Thief": {"button": None, "value": tk.IntVar()},
                    "Warrior": {"button": None, "value": tk.IntVar()}
                }

                self.characterFrame = ttk.LabelFrame(parent, text="Characters Being Played (up to 4)", padding=(20, 10))
                self.characterFrame.grid(row=0, column=3, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=3)
                for i, character in enumerate(self.charactersActive):
                    self.charactersActive[character]["value"].set(1 if character in self.settings["charactersActive"] else 0)
                    self.charactersActive[character]["button"] = ttk.Checkbutton(self.characterFrame, text=character, variable=self.charactersActive[character]["value"], command=self.check_max_characters)
                    self.charactersActive[character]["button"].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")

                log("End of create_characters_pane")
            except Exception as e:
                log(e, exception=True)
                raise


        def create_invaders_pane(self, parent):
            try:
                log("Start of create_invaders_pane")

                self.invadersFrame = ttk.LabelFrame(parent, text="Include Invaders", padding=(20, 10))
                self.invadersFrame.grid(row=0, column=4, padx=(20, 10), pady=(20, 10), sticky="nsew")
                self.invadersLabel = ttk.Label(self.invadersFrame, text="Max invaders allowed", justify="center", font=("-size", 12))
                self.invadersLabel.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
                
                self.maxInvaders = {"scale": None, "value": tk.IntVar(), "tooltipText": "This many invaders can take the place of enemies."}
                self.maxInvaders["scale"] = ttk.LabeledScale(self.invadersFrame, from_=0, to=14, variable=self.maxInvaders["value"])
                self.maxInvaders["value"].set(self.settings["maxInvaders"])
                self.maxInvaders["scale"].grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
                CreateToolTip(self.invadersLabel, self.maxInvaders["tooltipText"])

                log("End of create_invaders_pane")
            except Exception as e:
                log(e, exception=True)
                raise


        def create_treasure_swap_pane(self, parent):
            try:
                log("Start of create_treasure_swap_pane")

                self.treasureSwapOptions = {
                    "Similar Soul Cost": {"button": None, "value": tk.StringVar(value="Similar Soul Cost"), "tooltipText": "Rewards an item of the same type as the original that also costs about the same souls in leveling stats in order to equip it"},
                    "Tier Based": {"button": None, "value": tk.StringVar(value="Tier Based"), "tooltipText": "Splits treasure into equal tiers based on soul cost to equip and rewards an item in the same tier as the original reward."},
                    "Generic Treasure": {"button": None, "value": tk.StringVar(value="Generic Treasure"), "tooltipText": "Changes all specific item rewards to a number of draws equal to the encounter level."},
                    "Original": {"button": None, "value": tk.StringVar(value="Original"), "tooltipText": "Display the original reward on the card only."}
                }

                self.treasureSwapOption = tk.StringVar(value=self.settings["treasureSwapOption"])
                self.treasureSwapFrame = ttk.LabelFrame(parent, text="Treasure Swap Options", padding=(20, 10))
                self.treasureSwapFrame.grid(row=1, column=4, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=2)
                for i, option in enumerate(self.treasureSwapOptions):
                    self.treasureSwapOptions[option]["button"] = ttk.Radiobutton(self.treasureSwapFrame, text=option, variable=self.treasureSwapOption, value=option)
                    self.treasureSwapOptions[option]["button"].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")
                    CreateToolTip(self.treasureSwapOptions[option]["button"], self.treasureSwapOptions[option]["tooltipText"])

                log("End of create_treasure_swap_pane")
            except Exception as e:
                log(e, exception=True)
                raise


        def create_shown_encounters_pane(self, parent):
            try:
                log("Start of create_shown_encounters_pane")

                self.shownEncounters = {
                    "v1": {"button": None, "value": tk.IntVar()},
                    "v2": {"button": None, "value": tk.IntVar()},
                    "level4": {"button": None, "value": tk.IntVar()}
                }

                self.shownEncounterFrame = ttk.LabelFrame(parent, text="Encounters Shown", padding=(20, 10))
                self.shownEncounterFrame.grid(row=0, column=5, padx=(20, 10), pady=(20, 10), sticky="nsew")
                self.shownEncounters["v1"]["value"].set(1 if "v1" in self.settings["encounterTypes"] else 0)
                self.shownEncounters["v2"]["value"].set(1 if "v2" in self.settings["encounterTypes"] else 0)
                self.shownEncounters["level4"]["value"].set(1 if "level4" in self.settings["encounterTypes"] else 0)
                self.shownEncounters["v1"]["button"] = ttk.Checkbutton(self.shownEncounterFrame, text="V1 Encounters", variable=self.shownEncounters["v1"]["value"])
                self.shownEncounters["v2"]["button"] = ttk.Checkbutton(self.shownEncounterFrame, text="V2 Encounters", variable=self.shownEncounters["v2"]["value"])
                self.shownEncounters["level4"]["button"] = ttk.Checkbutton(self.shownEncounterFrame, text="Level 4 Encounters", variable=self.shownEncounters["level4"]["value"])
                self.shownEncounters["v1"]["button"].grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
                self.shownEncounters["v2"]["button"].grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
                self.shownEncounters["level4"]["button"].grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

                log("End of create_shown_encounters_pane")
            except Exception as e:
                log(e, exception=True)
                raise


        def create_update_check_pane(self, parent):
            try:
                log("Start of create_update_check_pane")

                self.updateCheck = {"button": None, "value": tk.IntVar(), "tooltipText": "If enabled, makes an API call to Github once a month when the app is opened to check for a new version.\n\nThe app won't download anything or update itself but will let you know if there's a new version."}
                self.updateCheckFrame = ttk.LabelFrame(parent, text="Check For Updates", padding=(20, 10))
                self.updateCheckFrame.grid(row=1, column=5, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=2)
                self.updateCheck["value"].set(1 if "on" in self.settings["updateCheck"] else 0)
                self.updateCheck["button"] = ttk.Checkbutton(self.updateCheckFrame, text="Check for updates", variable=self.updateCheck["value"])
                self.updateCheck["button"].grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
                CreateToolTip(self.updateCheck["button"], self.updateCheck["tooltipText"])

                log("End of create_update_check_pane")
            except Exception as e:
                log(e, exception=True)
                raise


        def create_buttons(self, parent):
            try:
                log("Start of create_buttons")

                self.saveCancelButtonsFrame = ttk.Frame(parent, padding=(0, 0, 0, 10))
                self.saveCancelButtonsFrame.grid(row=5, column=0, padx=15, pady=(10, 0), sticky="w", columnspan=2)
                self.saveCancelButtonsFrame.columnconfigure(index=0, weight=1)

                self.saveButton = ttk.Button(self.saveCancelButtonsFrame, text="Save", width=14, command=lambda: self.quit_with_save(coreSets=self.coreSets))
                self.cancelButton = ttk.Button(self.saveCancelButtonsFrame, text="Cancel", width=14, command=self.quit_no_save)
                self.saveButton.grid(column=0, row=0, padx=5)
                self.cancelButton.grid(column=1, row=0, padx=5)

                # self.themeButtonFrame = ttk.Frame(parent, padding=(0, 0, 0, 10))
                # self.themeButtonFrame.grid(row=5, column=5, padx=15, pady=(10, 0), sticky="e", columnspan=2)
                # self.themeButtonFrame.columnconfigure(index=0, weight=1)

                # self.lightTheme = {"button": None, "value": tk.IntVar()}
                # self.lightTheme["value"].set(0 if self.settings["theme"] == "dark" else 1)
                # self.lightTheme["button"] = ttk.Button(self.themeButtonFrame, text="Switch to light theme" if self.lightTheme["value"].get() == 0 else "Switch to dark theme", command=self.switch_theme)
                # self.lightTheme["button"].grid(column=3, row=0, columnspan=2)

                log("End of create_buttons")
            except Exception as e:
                log(e, exception=True)
                raise


        def toggle_parent_children(self, enemy, event=None):
            try:
                log("Start of toggle_parent_children")

                if self.enemies[enemy]["parent"]:
                    if (all([self.enemies[child]["value"].get() == 0 for child in self.enemies[self.enemies[enemy]["parent"]]["children"]])
                            or all([self.enemies[child]["value"].get() == 1 for child in self.enemies[self.enemies[enemy]["parent"]]["children"]])):
                        if enemy in self.expansions:
                            self.expansions[enemy]["value"].set(self.enemies[enemy]["value"].get())
                        else:
                            self.expansions[self.enemies[enemy]["parent"]]["value"].set(self.enemies[enemy]["value"].get())
                        self.enemies[self.enemies[enemy]["parent"]]["value"].set(self.enemies[enemy]["value"].get())
                    else:
                        self.enemies[self.enemies[enemy]["parent"]]["value"].set(0)
                        self.enemies[self.enemies[enemy]["parent"]]["button"].state(["alternate"])
                        self.expansions[self.enemies[enemy]["parent"]]["value"].set(1)
                else:
                    self.expansions[enemy]["value"].set(self.enemies[enemy]["value"].get())
                    
                    for child in self.enemies[enemy]["children"]:
                        self.enemies[child]["value"].set(self.enemies[enemy]["value"].get())

                log("End of toggle_parent_children")
            except Exception as e:
                log(e, exception=True)
                raise


        def toggle_expansion(self, expansion, event=None):
            try:
                log("Start of toggle_expansion")

                if expansion in {"Characters Expansion", "Level 4 Encounters"}:
                    log("End of toggle_expansion (Characters Expansion or Level 4 Encounters, nothing to do)")
                    return

                self.enemies[expansion]["value"].set(self.expansions[expansion]["value"].get())
                
                for child in self.enemies[expansion]["children"]:
                    self.enemies[child]["value"].set(self.expansions[expansion]["value"].get())

                log("End of toggle_expansion")
            except Exception as e:
                log(e, exception=True)
                raise


        def check_max_characters(self, event=None):
            """
            Checks to see how many characters have been selected.
            Disable remaining if 4 have been selected.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of check_max_characters")

                numChars = len([c for c in self.charactersActive if self.charactersActive[c]["value"].get() == 1])
                if numChars == 4:
                    for c in [c for c in self.charactersActive if self.charactersActive[c]["value"].get() == 0]:
                        self.charactersActive[c]["button"].config(state=tk.DISABLED)
                else:
                    for c in self.charactersActive:
                        self.charactersActive[c]["button"].config(state=tk.NORMAL)

                log("End of check_max_characters")
            except Exception as e:
                log(e, exception=True)
                raise


        # def switch_theme(self, root, event=None):
        #     """
        #     Changes the theme from dark to light or vice versa.

        #     Optional Parameters:
        #         event: tkinter.Event
        #             The tkinter Event that is the trigger.
        #     """
        #     try:
        #         log("Start of switch_theme")

        #         self.lightTheme["value"].set(0 if self.lightTheme["value"].get() == 1 else 1)
        #         self.settings["theme"] = "light" if self.lightTheme["value"].get() == 1 else "dark"
        #         root.tk.call("set_theme", "light" if self.lightTheme["value"].get() == 1 else "dark")
        #         self.lightTheme["button"]["text"] = "Switch to light theme" if self.lightTheme["value"].get() == 0 else "Switch to dark (souls) theme"
        #         self.errLabel.config(text="To keep this theme when you open the program again, you need to click Save!")

        #         log("End of switch_theme")
        #     except Exception as e:
        #         log(e, exception=True)
        #         raise


        def quit_with_save(self, coreSets, event=None):
            """
            Saves the settings and exits the settings window.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of quit_with_save")

                self.errLabel.config(text="")

                if all([self.expansions[s]["value"].get() == 0 for s in coreSets]):
                    self.errLabel.config(text="You need to select at least one Core Set!")
                    log("End of quit_with_save")
                    return

                if all([self.shownEncounters[i]["value"].get() == 0 for i in self.shownEncounters]):
                    self.errLabel.config(text="You need to check at least one box in the \"Encounters Shown\" section!")
                    log("End of quit_with_save")
                    return

                if len([i for i in self.charactersActive if self.charactersActive[i]["value"].get() == 1]) < 1 and self.treasureSwapOption.get() in set(["Similar Soul Cost", "Tier Based"]):
                    self.errLabel.config(text="You need to select at least 1 character if using the Similar Soul Cost or Tier Based treasure swap options!")
                    log("End of quit_with_save")
                    return

                characterExpansions = []
                for c in soulCost:
                    if self.charactersActive[c]["value"].get() == 1:
                        characterExpansions.append(soulCost[c]["expansions"])

                expansionsActive = set([s for s in self.expansions if self.expansions[s]["value"].get() == 1])
                expansionsNeeded = [e for e in characterExpansions if not any([e & expansionsActive])]
                if expansionsNeeded:
                    self.errLabel.config(text="You have selected one or more characters from sets you have disabled!")
                    log("End of quit_with_save")
                    return

                enabledEnemies = [s for s in self.enemies if self.enemies[s]["value"].get() == 1]
                if any(["alternate" in self.enemies[enemy]["button"].state() for enemy in self.enemies]):
                    customEnemyList = [enemy for enemy in self.enemies if "selected" in self.enemies[enemy]["button"].state() and not self.enemies[enemy]["children"]]
                else:
                    customEnemyList = []

                encounterTypes = set([s for s in self.shownEncounters if self.shownEncounters[s]["value"].get() == 1])
                charactersActive = set([s for s in self.charactersActive if self.charactersActive[s]["value"].get() == 1])

                newSettings = {
                    "availableExpansions": list(expansionsActive),
                    "enabledEnemies": list(enabledEnemies),
                    "customEnemyList": customEnemyList,
                    "encounterTypes": list(encounterTypes),
                    "charactersActive": list(charactersActive),
                    "treasureSwapOption": self.treasureSwapOption.get(),
                    "updateCheck": "on" if self.updateCheck["value"].get() == 1 else "off",
                    "maxInvaders": self.maxInvaders["value"].get()
                }

                if newSettings != self.settings:
                    with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep), "w") as settingsFile:
                        dump(newSettings, settingsFile)

                self.top.destroy()

                log("End of quit_with_save")
            except Exception as e:
                log(e, exception=True)
                raise


        def quit_no_save(self, event=None):
            """
            Exits the settings window without saving changes.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of quit_no_save")

                self.top.destroy()

                log("End of quit_no_save")
            except Exception as e:
                log(e, exception=True)
                raise
            
except Exception as e:
    log(e, exception=True)
    raise