import logging
import inspect
import platform
import tkinter as tk
from tkinter import ttk
from os import path
from json import load, dump

from dsbg_characters import soulCost
from dsbg_treasure import generate_treasure_soul_cost, populate_treasure_tiers
from dsbg_classes import CustomAdapter, VerticalScrolledFrame, CreateToolTip
from dsbg_functions import center


if platform.system() == "Windows":
    pathSep = "\\"
    windowsOs = True
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter("%(asctime)s|%(levelname)s|%(message)s", "%d/%m/%Y %H:%M:%S")
    fh = logging.FileHandler(path.dirname(path.realpath(__file__)) + "\\log.txt".replace("\\", pathSep), "w")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    adapter = CustomAdapter(logger, {"caller": ""})
    logger.setLevel(logging.DEBUG)
else:
    pathSep = "/"
    windowsOs = False

baseFolder = path.dirname(__file__).replace("\\lib".replace("\\", pathSep), "")


class SettingsWindow(object):
    """
    Window in which the user selects which expansions they own and whether they want to see
    V1, V1, or both styles of encounters when being shown random encounters.
    """
    def __init__(self, master, coreSets):
        try:
            if windowsOs:
                adapter.debug("Creating settings window")
            top = self.top = tk.Toplevel(master)
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
            self.create_treasure_swap_pane(top)
            self.create_random_encounters_pane(top)
            self.create_update_check_pane(top)
            self.create_buttons(top)

            self.errLabel = ttk.Label(self.top, text="")
            self.errLabel.grid(column=0, row=4, padx=18, columnspan=8)

            center(top)
            top.attributes('-alpha', 1.0)
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
            raise


    def create_expansion_tab(self):
        try:
            if windowsOs:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_expansion_tab", caller=calframe[1][3])

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

            if windowsOs:
                adapter.debug("End of create_expansion_tab", caller=calframe[1][3])
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
            raise


    def create_enemies_tab(self):
        try:
            if windowsOs:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_enemies_tab", caller=calframe[1][3])

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
                "Darkroot": {"button": None, "value": tk.IntVar(), "parent": None, "children": [], "displayName": "Darkroot"},
                "Demonic Foliage (V1)": {"button": None, "value": tk.IntVar(), "parent": "Darkroot", "children": [], "displayName": "Demonic Foliage (V1)"},
                "Mushroom Child (V1)": {"button": None, "value": tk.IntVar(), "parent": "Darkroot", "children": [], "displayName": "Mushroom Parent (V1)"},
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
                "Silver Knight Spearman (V1)": {"button": None, "value": tk.IntVar(), "parent": "Explorers", "children": [], "displayName": "Silver Knight Spearman (V1)"},
                "Iron Keep": {"button": None, "value": tk.IntVar(), "parent": None, "children": [], "displayName": "Iron Keep (V1)"},
                "Alonne Bow Knight (V1)": {"button": None, "value": tk.IntVar(), "parent": "Iron Keep", "children": [], "displayName": "Alonne Bow Knight (V1)"},
                "Alonne Knight Captain (V1)": {"button": None, "value": tk.IntVar(), "parent": "Iron Keep", "children": [], "displayName": "Alonne Knight Captain (V1)"},
                "Alonne Sword Knight (V1)": {"button": None, "value": tk.IntVar(), "parent": "Iron Keep", "children": [], "displayName": "Alonne Sword Knight (V1)"},
                "Ironclad Soldier (V1)": {"button": None, "value": tk.IntVar(), "parent": "Iron Keep", "children": [], "displayName": "Ironclad Soldier (V1)"}
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

            if windowsOs:
                adapter.debug("End of create_enemies_tab", caller=calframe[1][3])
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
            raise


    def create_characters_pane(self, parent):
        try:
            if windowsOs:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_characters_pane", caller=calframe[1][3])

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
            self.characterFrame.grid(row=0, column=3, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=4, columnspan=2)
            for i, enemy in enumerate(self.charactersActive):
                self.charactersActive[enemy]["value"].set(1 if enemy in self.settings["charactersActive"] else 0)
                self.charactersActive[enemy]["button"] = ttk.Checkbutton(self.characterFrame, text=enemy, variable=self.charactersActive[enemy]["value"], command=self.check_max_characters)
                self.charactersActive[enemy]["button"].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")

            if windowsOs:
                adapter.debug("End of create_characters_pane", caller=calframe[1][3])
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
            raise


    def create_treasure_swap_pane(self, parent):
        try:
            if windowsOs:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_treasure_swap_pane", caller=calframe[1][3])

            self.treasureSwapOptions = {
                "Similar Soul Cost": {"button": None, "value": tk.StringVar(value="Similar Soul Cost"), "tooltipText": "Rewards an item of the same type as the original that also costs about the same souls in leveling stats in order to equip it"},
                "Tier Based": {"button": None, "value": tk.StringVar(value="Tier Based"), "tooltipText": "Splits treasure into equal tiers based on soul cost to equip and rewards an item in the same tier as the original reward."},
                "Generic Treasure": {"button": None, "value": tk.StringVar(value="Generic Treasure"), "tooltipText": "Changes all specific item rewards to a number of draws equal to the encounter level."},
                "Original": {"button": None, "value": tk.StringVar(value="Original"), "tooltipText": "Display the original reward on the card only."}
            }

            self.treasureSwapOption = tk.StringVar(value=self.settings["treasureSwapOption"])
            self.treasureSwapFrame = ttk.LabelFrame(parent, text="Treasure Swap Options", padding=(20, 10))
            self.treasureSwapFrame.grid(row=0, column=5, padx=(20, 10), pady=(20, 10), sticky="nsew")
            for i, option in enumerate(self.treasureSwapOptions):
                self.treasureSwapOptions[option]["button"] = ttk.Radiobutton(self.treasureSwapFrame, text=option, variable=self.treasureSwapOption, value=option)
                self.treasureSwapOptions[option]["button"].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")
                CreateToolTip(self.treasureSwapOptions[option]["button"], self.treasureSwapOptions[option]["tooltipText"])

            if windowsOs:
                adapter.debug("End of create_treasure_swap_pane", caller=calframe[1][3])
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
            raise


    def create_random_encounters_pane(self, parent):
        try:
            if windowsOs:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_random_encounters_pane", caller=calframe[1][3])

            self.randomEncounters = {
                "v1": {"button": None, "value": tk.IntVar()},
                "v2": {"button": None, "value": tk.IntVar()}
            }

            self.randomEncounterFrame = ttk.LabelFrame(parent, text="Random Encounters Shown", padding=(20, 10))
            self.randomEncounterFrame.grid(row=1, column=5, padx=(20, 10), pady=(20, 10), sticky="nsew")
            self.randomEncounters["v1"]["value"].set(1 if "v1" in self.settings["randomEncounterTypes"] else 0)
            self.randomEncounters["v2"]["value"].set(1 if "v2" in self.settings["randomEncounterTypes"] else 0)
            self.randomEncounters["v1"]["button"] = ttk.Checkbutton(self.randomEncounterFrame, text="V1 Encounters", variable=self.randomEncounters["v1"]["value"])
            self.randomEncounters["v2"]["button"] = ttk.Checkbutton(self.randomEncounterFrame, text="V2 Encounters", variable=self.randomEncounters["v2"]["value"])
            self.randomEncounters["v1"]["button"].grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
            self.randomEncounters["v2"]["button"].grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

            if windowsOs:
                adapter.debug("End of create_random_encounters_pane", caller=calframe[1][3])
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
            raise


    def create_update_check_pane(self, parent):
        try:
            if windowsOs:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_update_check_pane", caller=calframe[1][3])

            self.updateCheck = {"button": None, "value": tk.IntVar(), "tooltipText": "If enabled, makes an API call to Github once a month when the app is opened to check for a new version.\n\nThe app won't download anything or update itself but will let you know if there's a new version."}
            self.updateCheckFrame = ttk.LabelFrame(parent, text="Check For Updates", padding=(20, 10))
            self.updateCheckFrame.grid(row=3, column=5, padx=(20, 10), pady=(20, 10), sticky="nsew")
            self.updateCheck["value"].set(1 if "on" in self.settings["updateCheck"] else 0)
            self.updateCheck["button"] = ttk.Checkbutton(self.updateCheckFrame, text="Check for updates", variable=self.updateCheck["value"])
            self.updateCheck["button"].grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
            CreateToolTip(self.updateCheck["button"], self.updateCheck["tooltipText"])

            if windowsOs:
                adapter.debug("End of create_update_check_pane", caller=calframe[1][3])
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
            raise


    def create_buttons(self, parent):
        try:
            if windowsOs:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_buttons", caller=calframe[1][3])

            self.saveCancelButtonsFrame = ttk.Frame(parent, padding=(0, 0, 0, 10))
            self.saveCancelButtonsFrame.grid(row=5, column=0, padx=15, pady=(10, 0), sticky="w", columnspan=2)
            self.saveCancelButtonsFrame.columnconfigure(index=0, weight=1)

            self.saveButton = ttk.Button(self.saveCancelButtonsFrame, text="Save", width=14, command=lambda: self.quit_with_save(coreSets=self.coreSets))
            self.cancelButton = ttk.Button(self.saveCancelButtonsFrame, text="Cancel", width=14, command=self.quit_no_save)
            self.saveButton.grid(column=0, row=0, padx=5)
            self.cancelButton.grid(column=1, row=0, padx=5)

            self.themeButtonFrame = ttk.Frame(parent, padding=(0, 0, 0, 10))
            self.themeButtonFrame.grid(row=5, column=5, padx=15, pady=(10, 0), sticky="e", columnspan=2)
            self.themeButtonFrame.columnconfigure(index=0, weight=1)

            self.lightTheme = {"button": None, "value": tk.IntVar()}
            self.lightTheme["value"].set(0 if self.settings["theme"] == "dark" else 1)
            self.lightTheme["button"] = ttk.Button(self.themeButtonFrame, text="Switch to light theme" if self.lightTheme["value"].get() == 0 else "Switch to dark theme", command=self.switch_theme)
            self.lightTheme["button"].grid(column=3, row=0, columnspan=2)

            if windowsOs:
                adapter.debug("End of create_buttons", caller=calframe[1][3])
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
            raise


    def toggle_parent_children(self, enemy, event=None):
        try:
            if windowsOs:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of toggle_parent_children", caller=calframe[1][3])

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

            if windowsOs:
                adapter.debug("End of toggle_parent_children", caller=calframe[1][3])
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
            raise


    def toggle_expansion(self, expansion, event=None):
        try:
            if windowsOs:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of toggle_expansion", caller=calframe[1][3])

            if expansion in {"Characters Expansion", "Phantoms"}:
                if windowsOs:
                    adapter.debug("End of toggle_expansion (Characters expansion, nothing to do)", caller=calframe[1][3])
                return

            self.enemies[expansion]["value"].set(self.expansions[expansion]["value"].get())
            
            for child in self.enemies[expansion]["children"]:
                self.enemies[child]["value"].set(self.expansions[expansion]["value"].get())

            if windowsOs:
                adapter.debug("End of toggle_expansion", caller=calframe[1][3])
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
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
            if windowsOs:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of check_max_characters", caller=calframe[1][3])

            numChars = len([c for c in self.charactersActive if self.charactersActive[c]["value"].get() == 1])
            if numChars == 4:
                for c in [c for c in self.charactersActive if self.charactersActive[c]["value"].get() == 0]:
                    self.charactersActive[c]["button"].config(state=tk.DISABLED)
            else:
                for c in self.charactersActive:
                    self.charactersActive[c]["button"].config(state=tk.NORMAL)

            if windowsOs:
                adapter.debug("End of check_max_characters", caller=calframe[1][3])
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
            raise


    def switch_theme(self, root, event=None):
        """
        Changes the theme from dark to light or vice versa.

        Optional Parameters:
            event: tkinter.Event
                The tkinter Event that is the trigger.
        """
        try:
            if windowsOs:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of switch_theme", caller=calframe[1][3])

            self.lightTheme["value"].set(0 if self.lightTheme["value"].get() == 1 else 1)
            self.settings["theme"] = "light" if self.lightTheme["value"].get() == 1 else "dark"
            root.tk.call("set_theme", "light" if self.lightTheme["value"].get() == 1 else "dark")
            self.lightTheme["button"]["text"] = "Switch to light theme" if self.lightTheme["value"].get() == 0 else "Switch to dark (souls) theme"
            self.errLabel.config(text="To keep this theme when you open the program again, you need to click Save!")

            if windowsOs:
                adapter.debug("End of switch_theme", caller=calframe[1][3])
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
            raise


    def quit_with_save(self, coreSets, event=None):
        """
        Saves the settings and exits the settings window.

        Optional Parameters:
            event: tkinter.Event
                The tkinter Event that is the trigger.
        """
        try:
            if windowsOs:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of quit_with_save", caller=calframe[1][3])

            self.errLabel.config(text="")

            if all([self.expansions[s]["value"].get() == 0 for s in coreSets]):
                self.errLabel.config(text="You need to select at least one Core Set!")
                if windowsOs:
                    adapter.debug("End of quit_with_save", caller=calframe[1][3])
                return

            if all([self.randomEncounters[i]["value"].get() == 0 for i in self.randomEncounters]):
                self.errLabel.config(text="You need to check at least one box in the \"Random Encounters Shown\" section!")
                if windowsOs:
                    adapter.debug("End of quit_with_save", caller=calframe[1][3])
                return

            if len([i for i in self.charactersActive if self.charactersActive[i]["value"].get() == 1]) < 1 and self.treasureSwapOption.get() in set(["Similar Soul Cost", "Tier Based"]):
                self.errLabel.config(text="You need to select at least 1 character if using the Similar Soul Cost or Tier Based treasure swap options!")
                if windowsOs:
                    adapter.debug("End of quit_with_save", caller=calframe[1][3])
                return

            characterExpansions = []
            for c in soulCost:
                if self.charactersActive[c]["value"].get() == 1:
                    characterExpansions.append(soulCost[c]["expansions"])

            expansionsActive = set([s for s in self.expansions if self.expansions[s]["value"].get() == 1])
            expansionsNeeded = [e for e in characterExpansions if not any([e & expansionsActive])]
            if expansionsNeeded:
                self.errLabel.config(text="You have selected one or more characters from sets you have disabled!")
                if windowsOs:
                    adapter.debug("End of quit_with_save", caller=calframe[1][3])
                return

            enabledEnemies = [s for s in self.enemies if self.enemies[s]["value"].get() == 1]
            customEnemyList = any(["alternate" in self.enemies[enemy]["button"].state() for enemy in self.enemies])

            randomEncounterTypes = set([s for s in self.randomEncounters if self.randomEncounters[s]["value"].get() == 1])
            charactersActive = set([s for s in self.charactersActive if self.charactersActive[s]["value"].get() == 1])

            newSettings = {
                "theme": "light" if self.lightTheme["value"].get() == 1 else "dark",
                "availableExpansions": list(expansionsActive),
                "enabledEnemies": list(enabledEnemies),
                "customEnemyList": customEnemyList,
                "randomEncounterTypes": list(randomEncounterTypes),
                "charactersActive": list(charactersActive),
                "treasureSwapOption": self.treasureSwapOption.get(),
                "updateCheck": "on" if self.updateCheck["value"].get() == 1 else "off"
            }

            if newSettings != self.settings:
                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep), "w") as settingsFile:
                    dump(newSettings, settingsFile)

                # Recalculate the average soul cost of treasure.
                if self.treasureSwapOption.get() == "Similar Soul Cost":
                    generate_treasure_soul_cost(expansionsActive, charactersActive)
                elif self.treasureSwapOption.get() == "Tier Based":
                    generate_treasure_soul_cost(expansionsActive, charactersActive)
                    populate_treasure_tiers(expansionsActive, charactersActive)

            self.top.destroy()
            if windowsOs:
                adapter.debug("End of quit_with_save", caller=calframe[1][3])
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
            raise


    def quit_no_save(self, event=None):
        """
        Exits the settings window without saving changes.

        Optional Parameters:
            event: tkinter.Event
                The tkinter Event that is the trigger.
        """
        try:
            if windowsOs:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of quit_no_save", caller=calframe[1][3])

            self.top.destroy()

            if windowsOs:
                adapter.debug("End of quit_no_save", caller=calframe[1][3])
        except Exception as e:
            if windowsOs:
                adapter.exception(e)
            raise