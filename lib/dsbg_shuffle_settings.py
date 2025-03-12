try:
    import tkinter as tk
    import webbrowser
    from tkinter import ttk
    from json import load, dump

    from dsbg_shuffle_characters import soulCost
    from dsbg_shuffle_utility import VerticalScrolledFrame, center, log, baseFolder, pathSep


    class SettingsWindow(object):
        """
        Window in which the user selects which expansions they own and whether they want to see
        V1, V1, or both styles of encounters when being shown encounters.
        """
        def __init__(self, app, root, coreSets):
            try:
                log("Creating settings window")
                self.root = root
                self.app = app
                top = self.top = tk.Toplevel(root)
                top.attributes("-alpha", 0.0)
                top.wait_visibility()
                top.grab_set_global()
                canvas = tk.Canvas(top)
                canvas.grid(row=0, column=0, sticky="nsew", columnspan=3)

                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep)) as settingsFile:
                    self.settings = load(settingsFile)

                self.availableExpansions = set(self.settings["availableExpansions"])
                self.enabledEnemies = self.settings["enabledEnemies"]
                self.enabledBossOptions = self.settings.get("enabledBossOptions", [])
                self.coreSets = coreSets

                self.notebook = ttk.Notebook(canvas)
                self.notebook.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=4, columnspan=2)

                self.create_characters_tab()
                self.create_expansion_tab()
                self.create_enemies_tab()
                self.create_boss_options_tab()
                self.create_invaders_tab()
                self.create_treasure_swap_tab()
                self.create_encounters_tab()
                self.create_variant_tab()
                self.create_update_tab()
                self.create_buttons(top)

                self.errLabel = ttk.Label(top, text="")
                self.errLabel.grid(column=0, row=4, padx=18, columnspan=8, sticky="w")

                canvas.rowconfigure(0, weight=1)
                canvas.columnconfigure(0, weight=1)

                center(top)
                top.attributes('-alpha', 1.0)
            except Exception as e:
                log(e, exception=True)
                raise


        def create_expansion_tab(self):
            try:
                log("Start of create_expansion_tab")

                self.expansions = {
                    "Painted World of Ariamis": {"button": None, "value": tk.IntVar(), "displayName": "Painted World of Ariamis (V2 Core Set)"},
                    "The Sunless City": {"button": None, "value": tk.IntVar(), "displayName": "The Sunless City (V2 Core Set)"},
                    "Tomb of Giants": {"button": None, "value": tk.IntVar(), "displayName": "Tomb of Giants (V2 Core Set)"},
                    "Dark Souls The Board Game": {"button": None, "value": tk.IntVar(), "displayName": "Dark Souls The Board Game (V1 Core Set)"},
                    "Darkroot": {"button": None, "value": tk.IntVar(), "displayName": "Darkroot (V1)"},
                    "Explorers": {"button": None, "value": tk.IntVar(), "displayName": "Explorers (V1)"},
                    "Iron Keep": {"button": None, "value": tk.IntVar(), "displayName": "Iron Keep (V1)"},
                    "Characters Expansion": {"button": None, "value": tk.IntVar(), "displayName": "Characters Expansion (V1)"},
                    "Phantoms": {"button": None, "value": tk.IntVar(), "displayName": "Phantoms (V1)"},
                    "Asylum Demon": {"button": None, "value": tk.IntVar(), "displayName": "Asylum Demon"},
                    "Black Dragon Kalameet": {"button": None, "value": tk.IntVar(), "displayName": "Black Dragon Kalameet"},
                    "Executioner Chariot": {"button": None, "value": tk.IntVar(), "displayName": "Executioner Chariot"},
                    "Gaping Dragon": {"button": None, "value": tk.IntVar(), "displayName": "Gaping Dragon"},
                    "Guardian Dragon": {"button": None, "value": tk.IntVar(), "displayName": "Guardian Dragon"},
                    "Manus, Father of the Abyss": {"button": None, "value": tk.IntVar(), "displayName": "Manus, Father of the Abyss"},
                    "Old Iron King": {"button": None, "value": tk.IntVar(), "displayName": "Old Iron King"},
                    "Vordt of the Boreal Valley": {"button": None, "value": tk.IntVar(), "displayName": "Vordt of the Boreal Valley"},
                    "The Four Kings": {"button": None, "value": tk.IntVar(), "displayName": "The Four Kings"},
                    "The Last Giant": {"button": None, "value": tk.IntVar(), "displayName": "The Last Giant"}
                }

                for s in list(set([e[0] for e in self.app.customEncounters])):
                    self.expansions[s] = {"button": None, "value": tk.IntVar(), "displayName": s + " (Custom)"}
                    self.expansions[s]["value"].set(1 if s in self.settings["availableExpansions"] else 0)

                self.expansionTab = VerticalScrolledFrame(self.notebook)
                self.notebook.add(self.expansionTab, text="Enabled Expansions")

                for i, expansion in enumerate(self.expansions):
                    self.expansions[expansion]["button"] = ttk.Checkbutton(self.expansionTab.interior, text=self.expansions[expansion]["displayName"], variable=self.expansions[expansion]["value"], command=lambda expansion=expansion: self.toggle_expansion(expansion=expansion))
                    self.expansions[expansion]["button"].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")
                    
                self.expansions["Phantoms"]["value"].set(1 if "Phantoms" in self.settings["availableExpansions"] else 0)
                self.expansions["Characters Expansion"]["value"].set(1 if "Characters Expansion" in self.settings["availableExpansions"] else 0)
                self.expansions["Asylum Demon"]["value"].set(1 if "Asylum Demon" in self.settings["availableExpansions"] else 0)
                self.expansions["Black Dragon Kalameet"]["value"].set(1 if "Black Dragon Kalameet" in self.settings["availableExpansions"] else 0)
                self.expansions["Gaping Dragon"]["value"].set(1 if "Gaping Dragon" in self.settings["availableExpansions"] else 0)
                self.expansions["Guardian Dragon"]["value"].set(1 if "Guardian Dragon" in self.settings["availableExpansions"] else 0)
                self.expansions["Manus, Father of the Abyss"]["value"].set(1 if "Manus, Father of the Abyss" in self.settings["availableExpansions"] else 0)
                self.expansions["Old Iron King"]["value"].set(1 if "Old Iron King" in self.settings["availableExpansions"] else 0)
                self.expansions["Vordt of the Boreal Valley"]["value"].set(1 if "Vordt of the Boreal Valley" in self.settings["availableExpansions"] else 0)
                self.expansions["The Four Kings"]["value"].set(1 if "The Four Kings" in self.settings["availableExpansions"] else 0)
                self.expansions["The Last Giant"]["value"].set(1 if "The Last Giant" in self.settings["availableExpansions"] else 0)

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


        def create_boss_options_tab(self):
            try:
                log("Start of create_boss_options_tab")

                self.bossOptions = {
                    "Kalameet": {"button": None, "value": tk.IntVar(), "displayName": "Black Dragon Kalameet\nConsistent 8 card Fiery Ruin deck,\ngenerated on deck reset."},
                    "Chariot": {"button": None, "value": tk.IntVar(), "displayName": "Executioner Chariot\nConsistent 4 card Death Race deck,\ngenerated on deck reset."},
                    "Guardian Dragon": {"button": None, "value": tk.IntVar(), "displayName": "Guardian Dragon\nConsistent 4 card Fiery Breath deck,\ngenerated on deck reset."},
                    "Old Iron King": {"button": None, "value": tk.IntVar(), "displayName": "Old Iron King\nConsistent 6 card Blasted Nodes deck,\ngenerated on deck reset."}
                }

                self.bossOptionsTab = VerticalScrolledFrame(self.notebook)
                self.bossOptionsTab.grid_propagate(False)
                self.notebook.add(self.bossOptionsTab, text="Boss Options")
                
                for i, option in enumerate(self.bossOptions):
                    self.bossOptions[option]["button"] = ttk.Checkbutton(self.bossOptionsTab.interior, text=self.bossOptions[option]["displayName"], variable=self.bossOptions[option]["value"])
                    self.bossOptions[option]["button"].grid(row=i, column=0, padx=5, pady=1, sticky="nsew")

                for option in self.enabledBossOptions:
                    self.bossOptions[option]["value"].set(1)

                log("End of create_boss_options_tab")
            except Exception as e:
                log(e, exception=True)
                raise


        def create_characters_tab(self):
            try:
                log("Start of create_characters_tab")

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
                
                self.characterTab = ttk.Frame(self.notebook)
                self.characterTab.grid_propagate(False)
                self.notebook.add(self.characterTab, text="Characters")
                self.characterLabel = ttk.Label(self.characterTab, text="The number of characters\nselected affects enemy swapping\nand the characters selected\naffects treasure swapping.", justify=tk.LEFT)
                self.characterLabel.pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=True)
                for i, character in enumerate(self.charactersActive, 1):
                    self.charactersActive[character]["value"].set(1 if character in self.settings["charactersActive"] else 0)
                    self.charactersActive[character]["button"] = ttk.Checkbutton(self.characterTab, text=character, variable=self.charactersActive[character]["value"], command=self.check_max_characters)
                    self.charactersActive[character]["button"].pack(side=tk.TOP, anchor=tk.W, fill=tk.X, expand=True)

                log("End of create_characters_tab")
            except Exception as e:
                log(e, exception=True)
                raise


        def create_invaders_tab(self):
            try:
                log("Start of create_invaders_tab")

                self.invaderTab = ttk.Frame(self.notebook)
                self.invaderTab.grid_propagate(False)
                self.notebook.add(self.invaderTab, text="Invaders")

                self.invadersLabel = ttk.Label(self.invaderTab, text="Number of invaders allowed to take the place of an\nequal number of enemies in an encounter.", justify=tk.LEFT)
                self.invadersLabel.grid(row=0, column=0, padx=5, pady=10, columnspan=6)
                
                self.maxInvadersVals = {
                    1: tk.IntVar(),
                    2: tk.IntVar(),
                    3: tk.IntVar(),
                    4: tk.IntVar()
                }
                
                self.maxInvadersVals[1].set(self.settings["maxInvaders"]["1"]),
                self.maxInvadersVals[2].set(self.settings["maxInvaders"]["2"]),
                self.maxInvadersVals[3].set(self.settings["maxInvaders"]["3"]),
                self.maxInvadersVals[4].set(self.settings["maxInvaders"]["4"])
                
                self.level1Label = ttk.Label(self.invaderTab, text="Level 1")
                self.level1Label.grid(row=1, column=0)
                self.maxInvadersLevel1Val = tk.IntVar()
                self.maxInvadersLevel1Radio0 = ttk.Radiobutton(self.invaderTab, text="0", variable=self.maxInvadersVals[1], value=0)
                self.maxInvadersLevel1Radio0.grid(row=1, column=1)
                self.maxInvadersLevel1Radio1 = ttk.Radiobutton(self.invaderTab, text="1", variable=self.maxInvadersVals[1], value=1)
                self.maxInvadersLevel1Radio1.grid(row=1, column=2)
                self.maxInvadersLevel1Radio2 = ttk.Radiobutton(self.invaderTab, text="2", variable=self.maxInvadersVals[1], value=2)
                self.maxInvadersLevel1Radio2.grid(row=1, column=3)
                self.maxInvadersLevel1Radio3 = ttk.Radiobutton(self.invaderTab, text="3", variable=self.maxInvadersVals[1], value=3)
                self.maxInvadersLevel1Radio3.grid(row=1, column=4)
                self.maxInvadersLevel1Radio4 = ttk.Radiobutton(self.invaderTab, text="4", variable=self.maxInvadersVals[1], value=4)
                self.maxInvadersLevel1Radio4.grid(row=1, column=5)
                self.maxInvadersLevel1Radio5 = ttk.Radiobutton(self.invaderTab, text="5", variable=self.maxInvadersVals[1], value=5)
                self.maxInvadersLevel1Radio5.grid(row=1, column=6)
                
                self.level2Label = ttk.Label(self.invaderTab, text="Level 2")
                self.level2Label.grid(row=2, column=0)
                self.maxInvadersLevel2Val = tk.IntVar()
                self.maxInvadersLevel2Radio0 = ttk.Radiobutton(self.invaderTab, text="0", variable=self.maxInvadersVals[2], value=0)
                self.maxInvadersLevel2Radio0.grid(row=2, column=1)
                self.maxInvadersLevel2Radio1 = ttk.Radiobutton(self.invaderTab, text="1", variable=self.maxInvadersVals[2], value=1)
                self.maxInvadersLevel2Radio1.grid(row=2, column=2)
                self.maxInvadersLevel2Radio2 = ttk.Radiobutton(self.invaderTab, text="2", variable=self.maxInvadersVals[2], value=2)
                self.maxInvadersLevel2Radio2.grid(row=2, column=3)
                self.maxInvadersLevel2Radio3 = ttk.Radiobutton(self.invaderTab, text="3", variable=self.maxInvadersVals[2], value=3)
                self.maxInvadersLevel2Radio3.grid(row=2, column=4)
                self.maxInvadersLevel2Radio4 = ttk.Radiobutton(self.invaderTab, text="4", variable=self.maxInvadersVals[2], value=4)
                self.maxInvadersLevel2Radio4.grid(row=2, column=5)
                self.maxInvadersLevel2Radio5 = ttk.Radiobutton(self.invaderTab, text="5", variable=self.maxInvadersVals[2], value=5)
                self.maxInvadersLevel2Radio5.grid(row=2, column=6)
                
                self.level3Label = ttk.Label(self.invaderTab, text="Level 3")
                self.level3Label.grid(row=3, column=0)
                self.maxInvadersLevel3Val = tk.IntVar()
                self.maxInvadersLevel3Radio0 = ttk.Radiobutton(self.invaderTab, text="0", variable=self.maxInvadersVals[3], value=0)
                self.maxInvadersLevel3Radio0.grid(row=3, column=1)
                self.maxInvadersLevel3Radio1 = ttk.Radiobutton(self.invaderTab, text="1", variable=self.maxInvadersVals[3], value=1)
                self.maxInvadersLevel3Radio1.grid(row=3, column=2)
                self.maxInvadersLevel3Radio2 = ttk.Radiobutton(self.invaderTab, text="2", variable=self.maxInvadersVals[3], value=2)
                self.maxInvadersLevel3Radio2.grid(row=3, column=3)
                self.maxInvadersLevel3Radio3 = ttk.Radiobutton(self.invaderTab, text="3", variable=self.maxInvadersVals[3], value=3)
                self.maxInvadersLevel3Radio3.grid(row=3, column=4)
                self.maxInvadersLevel3Radio4 = ttk.Radiobutton(self.invaderTab, text="4", variable=self.maxInvadersVals[3], value=4)
                self.maxInvadersLevel3Radio4.grid(row=3, column=5)
                self.maxInvadersLevel3Radio5 = ttk.Radiobutton(self.invaderTab, text="5", variable=self.maxInvadersVals[3], value=5)
                self.maxInvadersLevel3Radio5.grid(row=3, column=6)
                
                self.level4Label = ttk.Label(self.invaderTab, text="Level 4")
                self.level4Label.grid(row=4, column=0)
                self.maxInvadersLevel4Val = tk.IntVar()
                self.maxInvadersLevel4Radio0 = ttk.Radiobutton(self.invaderTab, text="0", variable=self.maxInvadersVals[4], value=0)
                self.maxInvadersLevel4Radio0.grid(row=4, column=1)
                self.maxInvadersLevel4Radio1 = ttk.Radiobutton(self.invaderTab, text="1", variable=self.maxInvadersVals[4], value=1)
                self.maxInvadersLevel4Radio1.grid(row=4, column=2)
                self.maxInvadersLevel4Radio2 = ttk.Radiobutton(self.invaderTab, text="2", variable=self.maxInvadersVals[4], value=2)
                self.maxInvadersLevel4Radio2.grid(row=4, column=3)
                self.maxInvadersLevel4Radio3 = ttk.Radiobutton(self.invaderTab, text="3", variable=self.maxInvadersVals[4], value=3)
                self.maxInvadersLevel4Radio3.grid(row=4, column=4)
                self.maxInvadersLevel4Radio4 = ttk.Radiobutton(self.invaderTab, text="4", variable=self.maxInvadersVals[4], value=4)
                self.maxInvadersLevel4Radio4.grid(row=4, column=5)
                self.maxInvadersLevel4Radio5 = ttk.Radiobutton(self.invaderTab, text="5", variable=self.maxInvadersVals[4], value=5)
                self.maxInvadersLevel4Radio5.grid(row=4, column=6)

                log("End of create_invaders_tab")
            except Exception as e:
                log(e, exception=True)
                raise


        def create_treasure_swap_tab(self):
            try:
                log("Start of create_treasure_swap_tab")

                treasureSwapText = {
                    "Similar Soul Cost": "Similar Soul Cost\n    Rewards an item of the same type as the\n    original that also costs about the same\n    souls in leveling stats in order to equip it.",
                    "Tier Based": "Tier Based\n    Splits treasure into equal tiers based on\n    soul cost to equip and rewards an item\n    in the same tier as the original reward.",
                    "Generic Treasure": "Generic Treasure\n    Changes all specific item rewards to a\n    number of draws equal to the encounter\n    level.",
                    "Original": "Original\n    Display the original reward on the card only."
                }

                self.treasureSwapOptions = {
                    "Similar Soul Cost": {"button": None, "value": tk.StringVar(value="Similar Soul Cost")},
                    "Tier Based": {"button": None, "value": tk.StringVar(value="Tier Based")},
                    "Generic Treasure": {"button": None, "value": tk.StringVar(value="Generic Treasure")},
                    "Original": {"button": None, "value": tk.StringVar(value="Original")}
                }

                self.treasureTab = ttk.Frame(self.notebook)
                self.treasureTab.grid_propagate(False)
                self.notebook.add(self.treasureTab, text="Treasure")

                self.treasureSwapOption = tk.StringVar()
                for i, option in enumerate(self.treasureSwapOptions):
                    self.treasureSwapOptions[option]["button"] = ttk.Radiobutton(self.treasureTab, text=treasureSwapText[option], variable=self.treasureSwapOption, value=option)
                    self.treasureSwapOptions[option]["button"].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")
                self.treasureSwapOption.set(self.settings["treasureSwapOption"])

                log("End of create_treasure_swap_tab")
            except Exception as e:
                log(e, exception=True)
                raise


        def create_encounters_tab(self):
            try:
                log("Start of create_encounters_tab")

                self.encounters = {
                    "v1": {"button": None, "value": tk.IntVar()},
                    "v2": {"button": None, "value": tk.IntVar()},
                    "level4": {"button": None, "value": tk.IntVar()}
                }

                self.encountersTab = ttk.Frame(self.notebook)
                self.encountersTab.grid_propagate(False)
                self.notebook.add(self.encountersTab, text="Encounters")

                self.encountersLabel = ttk.Label(self.encountersTab, text="Determines which encounters are shown in the main encounter list.")
                self.encountersLabel.grid(row=0, column=0, padx=5, pady=10)
                self.encounters["v1"]["value"].set(1 if "v1" in self.settings["encounterTypes"] else 0)
                self.encounters["v2"]["value"].set(1 if "v2" in self.settings["encounterTypes"] else 0)
                self.encounters["level4"]["value"].set(1 if "level4" in self.settings["encounterTypes"] else 0)
                self.encounters["v1"]["button"] = ttk.Checkbutton(self.encountersTab, text="V1 Encounters", variable=self.encounters["v1"]["value"])
                self.encounters["v2"]["button"] = ttk.Checkbutton(self.encountersTab, text="V2 Encounters", variable=self.encounters["v2"]["value"])
                self.encounters["level4"]["button"] = ttk.Checkbutton(self.encountersTab, text="Level 4 Encounters", variable=self.encounters["level4"]["value"])
                self.encounters["v1"]["button"].grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
                self.encounters["v2"]["button"].grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
                self.encounters["level4"]["button"].grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

                log("End of create_encounters_tab")
            except Exception as e:
                log(e, exception=True)
                raise


        def create_variant_tab(self):
            try:
                log("Start of create_variant_tab")

                self.variantTab = ttk.Frame(self.notebook)
                self.variantTab.grid_propagate(False)
                self.notebook.add(self.variantTab, text="Variants")

                self.variantEnable = {"button": None, "value": tk.IntVar()}
                self.variantEnable["value"].set(1 if "on" in self.settings["variantEnable"] else 0)
                self.variantEnable["button"] = ttk.Checkbutton(self.variantTab, text="Enable Variants Tab", variable=self.variantEnable["value"])
                self.variantEnable["button"].grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
                self.variantEnableLabel = ttk.Label(self.variantTab, text="If disabled, the Behavior\nVariants tab will do\nnothing if clicked on.\n\nIf you don't use behavior\nvariants, disabling this will\nmake the app load faster.")
                self.variantEnableLabel.grid(row=1, column=0, padx=5, pady=10)

                log("End of create_variant_tab")
            except Exception as e:
                log(e, exception=True)
                raise


        def create_update_tab(self):
            try:
                log("Start of create_update_tab")

                self.updateTab = ttk.Frame(self.notebook)
                self.updateTab.grid_propagate(False)
                self.notebook.add(self.updateTab, text="Updates")

                self.updateCheck = {"button": None, "value": tk.IntVar()}
                self.updateCheck["value"].set(1 if "on" in self.settings["updateCheck"] else 0)
                self.updateCheck["button"] = ttk.Checkbutton(self.updateTab, text="Check for updates", variable=self.updateCheck["value"])
                self.updateCheck["button"].grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
                self.updateLabel = ttk.Label(self.updateTab, text="If enabled, makes an\nAPI call to Github once\na month when the\napp is opened to check\nfor a new version.\n\nThe app won't\ndownload anything or\nupdate itself but will\nlet you know if\nthere's a new version.")
                self.updateLabel.grid(row=1, column=0, padx=5, pady=10)

                log("End of create_update_tab")
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

                self.wikiButtonFrame = ttk.Frame(parent, padding=(0, 0, 0, 10))
                self.wikiButtonFrame.grid(row=5, column=2, padx=15, pady=(10, 0), sticky="e")
                self.wikiButtonFrame.columnconfigure(index=0, weight=1)
                
                # Link to the wiki
                wikiLink = ttk.Button(self.wikiButtonFrame, text="Open the wiki", width=16, command=lambda x="https://github.com/DanDuhon/DSBG-Shuffle/wiki/Settings/": webbrowser.open_new(x))
                wikiLink.grid(column=1, row=1)

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

                if " (Custom)" in self.expansions[expansion]["displayName"] or expansion in {
                    "Characters Expansion",
                    "Level 4 Encounters",
                    "Asylum Demon",
                    "Black Dragon Kalameet",
                    "Gaping Dragon",
                    "Guardian Dragon",
                    "Manus, Father of the Abyss",
                    "Old Iron King",
                    "Vordt of the Boreal Valley",
                    "The Four Kings",
                    "The Last Giant"
                    }:
                    log("End of toggle_expansion (Characters Expansion, Level 4 Encounters, or custom set - nothing to do)")
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

                if all([self.encounters[i]["value"].get() == 0 for i in self.encounters]):
                    self.errLabel.config(text="You need to check at least one box in the \"Encounters Shown\" section!")
                    log("End of quit_with_save")
                    return

                if len([i for i in self.charactersActive if self.charactersActive[i]["value"].get() == 1]) < 1:
                    self.errLabel.config(text="You need to select at least 1 character!")
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

                enabledBossOptions = [s for s in self.bossOptions if self.bossOptions[s]["value"].get() == 1]

                encounterTypes = set([s for s in self.encounters if self.encounters[s]["value"].get() == 1])
                charactersActive = set([s for s in self.charactersActive if self.charactersActive[s]["value"].get() == 1])

                newSettings = {
                    "availableExpansions": list(expansionsActive),
                    "enabledEnemies": list(enabledEnemies),
                    "enabledBossOptions": list(enabledBossOptions),
                    "customEnemyList": customEnemyList,
                    "encounterTypes": list(encounterTypes),
                    "charactersActive": list(charactersActive),
                    "treasureSwapOption": self.treasureSwapOptions[self.treasureSwapOption.get()]["value"].get(),
                    "updateCheck": "on" if self.updateCheck["value"].get() == 1 else "off",
                    "variantEnable": "on" if self.variantEnable["value"].get() == 1 else "off",
                    "maxInvaders": {
                        "1": self.maxInvadersVals[1].get(),
                        "2": self.maxInvadersVals[2].get(),
                        "3": self.maxInvadersVals[3].get(),
                        "4": self.maxInvadersVals[4].get()
                    }
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