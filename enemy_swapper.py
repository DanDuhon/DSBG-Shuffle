try:
    import sys
    import logging
    import inspect
    import os
    from os import path
    from json import load, dump
    from random import choice
    from itertools import combinations
    from PIL import Image, ImageTk, ImageFont, ImageDraw
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog

    from enemies import enemyIds, enemiesDict
    from treasure import generate_treasure_soul_cost, populate_treasure_tiers, pick_treasure
    from character import soulCost


    def enable_binding(bindKey, method):
        """
        Sets a keyboard shortcut.

        Required Parameters:
            bindKey: String
                The key combination to be bound to a method.

            method: method/function
                The method or function to run when the key combination is pressed.
        """
        try:
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            adapter.debug("Start of enable_binding: bindKey=" + bindKey + ", method=" + str(method), caller=calframe[1][3])
            adapter.debug("End of enable_binding")
            return root.bind_all("<" + bindKey + ">", method)
        except Exception as e:
            adapter.exception(e)
            raise


    def do_nothing(event=None):
        pass


    class CustomAdapter(logging.LoggerAdapter):
        """
        Used for logging.
        """
        def process(self, msg, kwargs):
            my_context = kwargs.pop("caller", self.extra["caller"])
            return "[%s] %s" % (my_context, msg), kwargs


    logger = logging.getLogger(__name__)
    formatter = logging.Formatter("%(asctime)s|%(levelname)s|%(message)s", "%d/%m/%Y %H:%M:%S")
    fh = logging.FileHandler(path.dirname(path.realpath(__file__)) + "\\log.txt", "w")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    adapter = CustomAdapter(logger, {"caller": ""})
    logger.setLevel(logging.DEBUG)

    try:
        baseFolder = path.dirname(__file__)
        font = ImageFont.truetype(baseFolder + "\\Adobe Caslon Pro Semibold.ttf", 12)
        enemyImages = {}
        settingsChanged = False

        with open(baseFolder + "\\enemies.json") as enemiesFile:
            enemies = load(enemiesFile)

        with open(baseFolder + "\\invaders_standard.json") as invadersStandardFile:
            invadersStandard = load(invadersStandardFile)

        with open(baseFolder + "\\invaders_advanced.json") as invadersAdvancedFile:
            invadersAdvanced = load(invadersAdvancedFile)

        allEnemies = enemies | invadersStandard | invadersAdvanced

        with open(baseFolder + "\\encounters.json") as encountersFile:
            encounters = load(encountersFile)
    except Exception as e:
        adapter.exception(e)
        raise


    class CreateToolTip(object):
        """
        A tooltip that displays while the user is hovered over a particular Label.
        """
        def __init__(self, widget, text="widget info"):
            self.waittime = 500     # miliseconds
            self.wraplength = 225   # pixels
            self.widget = widget
            self.text = text
            self.widget.bind("<Enter>", self.enter)
            self.widget.bind("<Leave>", self.leave)
            self.widget.bind("<ButtonPress>", self.leave)
            self.id = None
            self.tw = None

        def enter(self, event=None):
            self.schedule()

        def leave(self, event=None):
            self.unschedule()
            self.hide_tip()

        def schedule(self):
            self.unschedule()
            self.id = self.widget.after(self.waittime, self.show_tip)

        def unschedule(self):
            id = self.id
            self.id = None
            if id:
                self.widget.after_cancel(id)

        def show_tip(self, event=None):
            x = y = 0
            x, y, cx, cy = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 20
            # Creates a toplevel window
            self.tw = tk.Toplevel(self.widget)
            # Leaves only the label and removes the app window
            self.tw.wm_overrideredirect(True)
            self.tw.wm_geometry("+%d+%d" % (x, y))
            label = ttk.Label(self.tw, text=self.text, font=(font, 12), justify="left", relief="solid", borderwidth=1, wraplength = self.wraplength)
            label.pack(ipadx=1)

        def hide_tip(self):
            tw = self.tw
            self.tw= None
            if tw:
                tw.destroy()


    class HelpWindow(object):
        """
        Window that just displays text about how to use the app.
        """
        def __init__(self, master):
            try:
                adapter.debug("Creating help window")
                top = self.top = tk.Toplevel(master)
                top.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
                top.wait_visibility()
                top.grab_set_global()

                self.helpTextFrame = ttk.Frame(top, padding=(0, 0, 0, 10))
                self.helpTextFrame.grid(row=0, column=0, padx=15, pady=(10, 0), sticky="w")

                helpText = "Encounters Tab\n"
                helpText += "You can either select an encounter from the list or click the \"Random\n"
                helpText += "Level x\" buttons. Once an encounter card has been loaded, you can click\n"
                helpText += "on the card or use the \"s\" key to reshuffle the encounter's enemies and\n"
                helpText += "treasure reward, if any.\n\n"
                helpText += "If you try to shuffle the enemies and nothing happens, there's probably\n"
                helpText += "only one combination available! Many encounters with a single enemy have\n"
                helpText += "no alternatives, even with all sets activated.\n\n"
                helpText += "Mousing over keywords (in bold and italics) and icons in the Objectives\n"
                helpText += "and Special Rules sections will display the name or rules for that keyword.\n\n"
                helpText += "Campaign Tab\n"
                helpText += "You can build your own campaign by adding encounters to it. You can also\n"
                helpText += "save and load campaigns. You may only have one of each encounter name,\n"
                helpText += "but there are no restrictions beyond that. Encounters added to a campaign\n"
                helpText += "are frozen so you cannot shuffle the enemies.\n\n"
                helpText += "Settings\n"
                helpText += "In the settings menu, you can enable the different core sets/expansions\n"
                helpText += "that add enemies or basic treasure to the game. These are the only sets\n"
                helpText += "listed on purpose as they are the ones that add non-boss enemies.\n\n"
                helpText += "Treasure Swap Options are as follows:\n"
                helpText += "Similar Soul Cost: Rewards an item of the same type as the original that\n"
                helpText += "    also costs about the same souls in leveling stats in order to equip it\n"
                helpText += "Tier Based: Splits treasure into tiers and rewards an item in the same\n"
                helpText += "    tier as the original reward.\n"
                helpText += "Generic Treasure: Changes all specific item rewards to a number of draws\n"
                helpText += "    equal to the encounter level.\n"
                helpText += "Original: Display the original reward on the card only."
                self.helpTextLabel = ttk.Label(self.helpTextFrame, text=helpText)
                self.helpTextLabel.grid()

                self.helpButtonsFrame = ttk.Frame(top, padding=(0, 0, 0, 10))
                self.helpButtonsFrame.grid(row=1, column=0, padx=15, pady=(10, 0), sticky="w")
                self.helpButtonsFrame.columnconfigure(index=0, weight=1)

                self.okButton = ttk.Button(self.helpButtonsFrame, text="OK", width=14, command=self.top.destroy)
                self.okButton.grid(column=0, row=0, padx=5)
            except Exception as e:
                adapter.exception(e)
                raise


    class SettingsWindow(object):
        """
        Window in which the user selects which sets they own and whether they want to see
        old, new, or both styles of encounters when being shown random encounters.
        """
        def __init__(self, master):
            try:
                adapter.debug("Creating settings window")
                top = self.top = tk.Toplevel(master)
                top.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
                top.wait_visibility()
                top.grab_set_global()
                
                with open(baseFolder + "\\settings.json") as settingsFile:
                    self.settings = load(settingsFile)

                self.availableSets = set(self.settings["availableSets"])
                
                # These are the only sets that matter - the ones that add enemies or regular treasure.
                # All encounters are always going to be available.
                self.sets = {
                    "Dark Souls The Board Game": {"button": None, "value": tk.IntVar()},
                    "Painted World of Ariamis": {"button": None, "value": tk.IntVar()},
                    "Tomb of Giants": {"button": None, "value": tk.IntVar()},
                    "Darkroot": {"button": None, "value": tk.IntVar()},
                    "Explorers": {"button": None, "value": tk.IntVar()},
                    "Iron Keep": {"button": None, "value": tk.IntVar()},
                    "Phantoms": {"button": None, "value": tk.IntVar()},
                    "The Executioner's Chariot": {"button": None, "value": tk.IntVar()},
                    "Character Expansion": {"button": None, "value": tk.IntVar()}
                }
                
                self.setsFrame = ttk.LabelFrame(top, text="Enabled Enemies From Sets", padding=(20, 10))
                self.setsFrame.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=2, columnspan=2)
                for i, a in enumerate(self.sets):
                    self.sets[a]["value"].set(1 if a in self.settings["availableSets"] else 0)
                    self.sets[a]["button"] = ttk.Checkbutton(self.setsFrame, text=a + (" (Core Set)" if a in coreSets else ""), variable=self.sets[a]["value"])
                    if i > 11:
                        self.sets[a]["button"].grid(row=i-12, column=1, padx=5, pady=10, sticky="nsew")
                    else:
                        self.sets[a]["button"].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")

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
                
                self.characterFrame = ttk.LabelFrame(top, text="Characters Being Played (up to 4)", padding=(20, 10))
                self.characterFrame.grid(row=0, column=3, padx=(20, 10), pady=(20, 10), sticky="nsew", rowspan=2, columnspan=2)
                for i, a in enumerate(self.charactersActive):
                    self.charactersActive[a]["value"].set(1 if a in self.settings["charactersActive"] else 0)
                    self.charactersActive[a]["button"] = ttk.Checkbutton(self.characterFrame, text=a, variable=self.charactersActive[a]["value"], command=self.check_max_characters)
                    self.charactersActive[a]["button"].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")
                    
                self.treasureSwapOptions = {
                    "Similar Soul Cost": {"button": None, "value": tk.StringVar(value="Similar Soul Cost")},
                    "Tier Based": {"button": None, "value": tk.StringVar(value="Tier Based")},
                    "Generic Treasure": {"button": None, "value": tk.StringVar(value="Generic Treasure")},
                    "Original": {"button": None, "value": tk.StringVar(value="Original")}
                }

                self.treasureSwapOption = tk.StringVar(value=self.settings["treasureSwapOption"])
                self.treasureSwapFrame = ttk.LabelFrame(top, text="Treasure Swap Options", padding=(20, 10))
                self.treasureSwapFrame.grid(row=0, column=5, padx=(20, 10), pady=(20, 10), sticky="nsew")
                for i, a in enumerate(self.treasureSwapOptions):
                    self.treasureSwapOptions[a]["button"] = ttk.Radiobutton(self.treasureSwapFrame, text=a, variable=self.treasureSwapOption, value=a)
                    self.treasureSwapOptions[a]["button"].grid(row=i, column=0, padx=5, pady=10, sticky="nsew")
                
                self.randomEncounters = {
                    "old": {"button": None, "value": tk.IntVar()},
                    "new": {"button": None, "value": tk.IntVar()}
                }

                self.randomEncounterFrame = ttk.LabelFrame(top, text="Random Encounters Shown", padding=(20, 10))
                self.randomEncounterFrame.grid(row=1, column=5, padx=(20, 10), pady=(20, 10), sticky="nsew")
                self.randomEncounters["old"]["value"].set(1 if "old" in self.settings["randomEncounterTypes"] else 0)
                self.randomEncounters["new"]["value"].set(1 if "new" in self.settings["randomEncounterTypes"] else 0)
                self.randomEncounters["old"]["button"] = ttk.Checkbutton(self.randomEncounterFrame, text="\"Old\" Style Encounters", variable=self.randomEncounters["old"]["value"])
                self.randomEncounters["new"]["button"] = ttk.Checkbutton(self.randomEncounterFrame, text="\"New\" Style Encounters", variable=self.randomEncounters["new"]["value"])
                self.randomEncounters["old"]["button"].grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
                self.randomEncounters["new"]["button"].grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
                
                self.errLabel = tk.Label(self.top, text="")
                self.errLabel.grid(column=0, row=3, padx=18, columnspan=8)

                self.saveCancelButtonsFrame = ttk.Frame(top, padding=(0, 0, 0, 10))
                self.saveCancelButtonsFrame.grid(row=4, column=0, padx=15, pady=(10, 0), sticky="w", columnspan=2)
                self.saveCancelButtonsFrame.columnconfigure(index=0, weight=1)
                
                self.saveButton = ttk.Button(self.saveCancelButtonsFrame, text="Save", width=14, command=lambda: self.quit_with_save())
                self.cancelButton = ttk.Button(self.saveCancelButtonsFrame, text="Cancel", width=14, command=self.quit_no_save)
                self.saveButton.grid(column=0, row=0, padx=5)
                self.cancelButton.grid(column=1, row=0, padx=5)

                self.themeButtonFrame = ttk.Frame(top, padding=(0, 0, 0, 10))
                self.themeButtonFrame.grid(row=4, column=5, padx=15, pady=(10, 0), sticky="e", columnspan=2)
                self.themeButtonFrame.columnconfigure(index=0, weight=1)

                self.lightTheme = {"button": None, "value": tk.IntVar()}
                self.lightTheme["value"].set(0 if self.settings["theme"] == "dark" else 1)
                self.lightTheme["button"] = ttk.Button(self.themeButtonFrame, text="Switch to light theme" if self.lightTheme["value"].get() == 0 else "Switch to dark theme", command=self.switch_theme)
                self.lightTheme["button"].grid(column=3, row=0, columnspan=2)
            except Exception as e:
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
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of check_max_characters", caller=calframe[1][3])

                numChars = len([c for c in self.charactersActive if self.charactersActive[c]["value"].get() == 1])
                if numChars == 4:
                    for c in [c for c in self.charactersActive if self.charactersActive[c]["value"].get() == 0]:
                        self.charactersActive[c]["button"].config(state=tk.DISABLED)
                        if self.lightTheme["value"].get() == 0:
                            self.charactersActive[c]["button"].config(foreground="gray")
                else:
                    for c in self.charactersActive:
                        self.charactersActive[c]["button"].config(state=tk.NORMAL)
                        if self.lightTheme["value"].get() == 1:
                            self.charactersActive[c]["button"].config(fg="white")

                adapter.debug("End of check_max_characters", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def switch_theme(self, event=None):
            """
            Changes the theme from dark to light or vice versa.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of switch_theme", caller=calframe[1][3])

                self.lightTheme["value"].set(0 if self.lightTheme["value"].get() == 1 else 1)
                self.settings["theme"] = "light" if self.lightTheme["value"].get() == 1 else "dark"
                root.tk.call("set_theme", "light" if self.lightTheme["value"].get() == 1 else "dark")
                self.lightTheme["button"]["text"] = "Switch to light theme" if self.lightTheme["value"].get() == 0 else "Switch to dark (souls) theme"
                self.errLabel.config(text="To keep this theme when you open the program again, you need to click Save!")

                adapter.debug("End of switch_theme", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise
            
            
        def quit_with_save(self, event=None):
            """
            Saves the settings and exits the settings window.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of quit_with_save", caller=calframe[1][3])

                self.errLabel.config(text="")

                if all([self.sets[s]["value"].get() == 0 for s in coreSets]):
                    self.errLabel.config(text="You need to select at least one Core Set!")
                    adapter.debug("End of quit_with_save", caller=calframe[1][3])
                    return

                if all([self.randomEncounters[i]["value"].get() == 0 for i in self.randomEncounters]):
                    self.errLabel.config(text="You need to check at least one box in the \"Random Encounters Shown\" section!")
                    adapter.debug("End of quit_with_save", caller=calframe[1][3])
                    return

                if len([i for i in self.charactersActive if self.charactersActive[i]["value"].get() == 1]) < 1 and self.treasureSwapOption.get() in set(["Similar Soul Cost", "Tier Based"]):
                    self.errLabel.config(text="You need to select at least 1 character if using the Similar Soul Cost or Tier Based treasure swap options!")
                    adapter.debug("End of quit_with_save", caller=calframe[1][3])
                    return
                
                characterSets = set()
                for c in soulCost:
                    characterSets.update(soulCost[c]["sets"])

                setsActive = set([s for s in self.sets if self.sets[s]["value"].get() == 1])
                if characterSets - setsActive:
                    self.errLabel.config(text="You have selected one or more characters from sets you have disabled!")
                    adapter.debug("End of quit_with_save", caller=calframe[1][3])
                    return

                randomEncounterTypes = set([s for s in self.randomEncounters if self.randomEncounters[s]["value"].get() == 1])
                charactersActive = set([s for s in self.charactersActive if self.charactersActive[s]["value"].get() == 1])

                newSettings = {
                    "theme": "light" if self.lightTheme["value"].get() == 1 else "dark",
                    "availableSets": list(setsActive),
                    "randomEncounterTypes": list(randomEncounterTypes),
                    "charactersActive": list(charactersActive),
                    "treasureSwapOption": self.treasureSwapOption.get()
                }

                # This will trigger the encounters treeview to be recreated to account for the changes.
                if newSettings != self.settings:
                    global settingsChanged
                    settingsChanged = True

                    with open(baseFolder + "\\settings.json", "w") as settingsFile:
                        dump(newSettings, settingsFile)

                    # Recalculate the average soul cost of treasure.
                    if self.treasureSwapOption.get() == "Similar Soul Cost":
                        generate_treasure_soul_cost(setsActive, charactersActive)
                    elif self.treasureSwapOption.get() == "Tier Based":
                        generate_treasure_soul_cost(setsActive, charactersActive)
                        populate_treasure_tiers(setsActive, charactersActive)

                self.top.destroy()
                adapter.debug("End of quit_with_save", caller=calframe[1][3])
            except Exception as e:
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
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of quit_no_save", caller=calframe[1][3])

                self.top.destroy()

                adapter.debug("End of quit_no_save", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise
        

    class PopupWindow(object):
        """
        A popup window that either displays a message for the user or asks
        for input in the form of an entry field or a choice of two options.

        Required parameters:
            master: tkinter.Tk object
                The tkinter Tk object (root).
                
            labelText: String
                The message to be displayed in the popup window.

            button1Text: String
                The text displayed on the first button.
        """
        def __init__(self, master, labelText, buttonText):
            try:
                top = self.top = tk.Toplevel(master)
                top.wait_visibility()
                top.grab_set_global()
                self.l = ttk.Label(top, text=labelText, font=("calibri", 16))
                self.l.pack()
                self.l.focus_force()

                self.b = ttk.Button(top, text=buttonText, command=lambda: self.top.destroy())
                self.b.pack()
            except Exception as e:
                adapter.exception(e)
                raise


    class Application(ttk.Frame):
        def __init__(self, parent):
            try:
                adapter.debug("Initiating application")
                    
                with open(baseFolder + "\\settings.json") as settingsFile:
                    self.settings = load(settingsFile)

                if self.settings["theme"] == "light":
                    root.tk.call("set_theme", "light")
                
                ttk.Frame.__init__(self)
                self.grid_rowconfigure(index=1, weight=1)
                self.grid_rowconfigure(index=2, weight=0)
                self.encounterScrollbar = ttk.Scrollbar(root)
                self.encounterScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                self.bossMenu = [
                    "Boss List",
                    "--Mini Bosses--",
                    "Asylum Demon",
                    "Black Knight",
                    "Boreal Outrider Knight",
                    "Heavy Knight",
                    "Old Dragonslayer",
                    "Titanite Demon",
                    "Winged Knight",
                    "--Main Bosses--",
                    "Artorias",
                    "Crossbreed Priscilla",
                    "Dancer of the Boreal Valley",
                    "Gravelord Nito",
                    "Great Grey Wolf Sif",
                    "Ornstein and Smough",
                    "Sir Alonne",
                    "Smelter Demon",
                    "The Pursuer",
                    "--Mega Bosses--",
                    "Black Dragon Kalameet",
                    "The Executioner's Chariot",
                    "Gaping Dragon",
                    "Guardian Dragon",
                    "Manus, Father of the Abyss",
                    "Old Iron King",
                    "Stray Demon",
                    "The Four Kings",
                    "The Last Giant",
                    "Vordt of the Boreal Valley"
                    ]

                self.bosses = {
                    "Asylum Demon": {"name": "Asylum Demon", "level": "Mini Boss", "expansion": "Asylum Demon"},
                    "Black Knight": {"name": "Black Knight", "level": "Mini Boss", "expansion": "Tomb of Giants"},
                    "Boreal Outrider Knight": {"name": "Boreal Outrider Knight", "level": "Mini Boss", "expansion": "Dark Souls The Board Game"},
                    "Heavy Knight": {"name": "Heavy Knight", "level": "Mini Boss", "expansion": "Painted World of Ariamis"},
                    "Old Dragonslayer": {"name": "Old Dragonslayer", "level": "Mini Boss", "expansion": "Explorers"},
                    "Titanite Demon": {"name": "Titanite Demon", "level": "Mini Boss", "expansion": "Dark Souls The Board Game"},
                    "Winged Knight": {"name": "Winged Knight", "level": "Mini Boss", "expansion": "Dark Souls The Board Game"},
                    "Artorias": {"name": "Artorias", "level": "Main Boss", "expansion": "Darkroot"},
                    "Crossbreed Priscilla": {"name": "Crossbreed Priscilla", "level": "Main Boss", "expansion": "Painted World of Ariamis"},
                    "Dancer of the Boreal Valley": {"name": "Dancer of the Boreal Valley", "level": "Main Boss", "expansion": "Dark Souls The Board Game"},
                    "Gravelord Nito": {"name": "Gravelord Nito", "level": "Main Boss", "expansion": "Tomb of Giants"},
                    "Great Grey Wolf Sif": {"name": "Great Grey Wolf Sif", "level": "Main Boss", "expansion": "Darkroot"},
                    "Ornstein and Smough": {"name": "Ornstein and Smough", "level": "Main Boss", "expansion": "Dark Souls The Board Game"},
                    "Sir Alonne": {"name": "Sir Alonne", "level": "Main Boss", "expansion": "Iron Keep"},
                    "Smelter Demon": {"name": "Smelter Demon", "level": "Main Boss", "expansion": "Iron Keep"},
                    "The Pursuer": {"name": "The Pursuer", "level": "Main Boss", "expansion": "Explorers"},
                    "Black Dragon Kalameet": {"name": "Black Dragon Kalameet", "level": "Mega Boss", "expansion": "Black Dragon Kalameet"},
                    "The Executioner's Chariot": {"name": "The Executioner's Chariot", "level": "Mega Boss", "expansion": "The Executioner's Chariot"},
                    "Gaping Dragon": {"name": "Gaping Dragon", "level": "Mega Boss", "expansion": "Gaping Dragon"},
                    "Guardian Dragon": {"name": "Guardian Dragon", "level": "Mega Boss", "expansion": "Guardian Dragon"},
                    "Manus, Father of the Abyss": {"name": "Manus, Father of the Abyss", "level": "Mega Boss", "expansion": "Manus, Father of the Abyss"},
                    "Old Iron King": {"name": "Old Iron King", "level": "Mega Boss", "expansion": "Old Iron King"},
                    "Stray Demon": {"name": "Stray Demon", "level": "Mega Boss", "expansion": "Asylum Demon"},
                    "The Four Kings": {"name": "The Four Kings", "level": "Mega Boss", "expansion": "The Four Kings"},
                    "The Last Giant": {"name": "The Last Giant", "level": "Mega Boss", "expansion": "The Last Giant"},
                    "Vordt of the Boreal Valley": {"name": "Vordt of the Boreal Valley", "level": "Mega Boss", "expansion": "Vordt of the Boreal Valley"}
                }
                
                self.selectedBoss = tk.StringVar()

                self.allSets = set([encounters[encounter]["expansion"] for encounter in encounters])
                self.availableSets = set(self.settings["availableSets"])
                self.charactersActive = set(self.settings["charactersActive"])
                self.availableCoreSets = coreSets & self.availableSets
                oldSets = {"Dark Souls The Board Game", "Darkroot", "The Executioner's Chariot", "Explorers", "Iron Keep"} if "old" in self.settings["randomEncounterTypes"] else set()
                newSets = (self.allSets - {"Dark Souls The Board Game", "Darkroot", "The Executioner's Chariot", "Explorers", "Iron Keep"}) if "new" in self.settings["randomEncounterTypes"] else set()
                self.setsForRandomEncounters = (oldSets | newSets) & self.allSets
                
                if self.settings["treasureSwapOption"] == "Similar Soul Cost":
                    generate_treasure_soul_cost(self.availableSets, self.charactersActive)
                elif self.settings["treasureSwapOption"] == "Tier Based":
                    generate_treasure_soul_cost(self.availableSets, self.charactersActive)
                    populate_treasure_tiers(self.availableSets, self.charactersActive)
                self.set_encounter_list()
                self.create_buttons()
                self.create_tabs()
                self.scrollbarTreeviewEncounters = ttk.Scrollbar(self.encounterTab)
                self.scrollbarTreeviewEncounters.pack(side="right", fill="y")
                self.create_encounters_treeview()
                self.scrollbarTreeviewCampaign = ttk.Scrollbar(self.campaignTabTreeviewFrame)
                self.scrollbarTreeviewCampaign.pack(side="right", fill="y")
                self.create_campaign_treeview()
                self.create_encounter_frame()
                self.create_menu()
                self.set_bindings_buttons_menus(True)

                self.treasureSwapEncounters = {
                    "Corvian Host": "Bloodshield",
                    "Dark Resurrection": "Fireball",
                    "Distant Tower": "Velka's Rapier",
                    "Frozen Revolutions": "Red Tearstone Ring",
                    "Giant's Coffin": "Black Knight Greataxe",
                    "Grave Matters": "Firebombs",
                    "In Deep Water": "Thorolund Talisman",
                    "Inhospitable Ground": "Pike",
                    "Monstrous Maw": "Exile Greatsword",
                    "No Safe Haven": "Throwing Knives",
                    "Painted Passage": "Painting Guardian Armour",
                    "Puppet Master": "Skull Lantern",
                    "Rain of Filth": "Poison Mist",
                    "The Abandoned Chest": "Chloranthy Ring",
                    "The Beast From the Depths": "Mask of the Child",
                    "The Locked Grave": "Dragon Scale",
                    "The Skeleton Ball": "Divine Blessing",
                    "Unseen Scurrying": "Kukris",
                    "Urns of the Fallen": "Bonewheel Shield",
                    "Velka's Chosen": "Demon Titanite"
                }

                self.tooltipText = {
                    "bitterCold": "If a character has a Frostbite token at the end of their turn, they suffer 1 damage.",
                    "barrage": "At the end of each character's turn, that character must make a defense roll using only their dodge dice.\n\nIf no dodge symbols are rolled, the character suffers 2 damage and Stagger.",
                    "darkness": "During this encounter, characters can only attack enemies on the same or an adjacent node.",
                    "eerie": "During setup, take five blank trap tokens and five trap tokens with values on them, and place a random token face down on each of the highlighted nodes.\n\nIf a character moves onto a node with a token, flip the token.\n\nIf the token is blank, place it to one side.\n\nIf the token has a damage value, instead of resolving it normally, spawn an enemy corresponding to the value shown, then discard the token.",
                    "hidden": "After declaring an attack, players must discard a die of their choice before rolling.\n\nIf the attacks only has a single die already, ignore this rule.",
                    "onslaught": "Each tile begins the encounter as active (all enemies on active tiles act on their turn).",
                    "poisonMist": "During setup, place trap tokens on the tile indicated in brackets using the normal trap placement rules.\n\nThen, reveal the tokens, replacing each token with a value with a poison cloud token.",
                    "snowstorm": "At the start of each character's turn, that character suffers Frostbite unless they have the torch token on their dashboard or are on the same node as the torch token or a character with the torch token on their dashboard.",
                    "timer": "If the timer marker reaches the value shown in brackets, resolve the effect listed.",
                    "trial": "Trials offer an extra objective providing additional rewards if completed.\n\nThis is shown in parentheses, either in writing, or as a number of turns in which the characters must complete the encounter's main objective.\n\nCompleting trial objectives is not mandatory to complete an encounter.",
                    "Alonne Bow Knight": "Alonne Bow Knight",
                    "Alonne Knight Captain": "Alonne Knight Captain",
                    "Alonne Sword Knight": "Alonne Sword Knight",
                    "Black Hollow Mage": "Black Hollow Mage",
                    "Bonewheel Skeleton": "Bonewheel Skeleton",
                    "Crossbow Hollow": "Crossbow Hollow",
                    "Crow Demon": "Crow Demon",
                    "Demonic Foliage": "Demonic Foliage",
                    "Engorged Zombie": "Engorged Zombie",
                    "Falchion Skeleton": "Falchion Skeleton",
                    "Firebomb Hollow": "Firebomb Hollow",
                    "Giant Skeleton Archer": "Giant Skeleton Archer",
                    "Giant Skeleton Soldier": "Giant Skeleton Soldier",
                    "Hollow Soldier": "Hollow Soldier",
                    "Ironclad Soldier": "Ironclad Soldier",
                    "Large Hollow Soldier": "Large Hollow Soldier",
                    "Mushroom Child": "Mushroom Child",
                    "Mushroom Parent": "Mushroom Parent",
                    "Necromancer": "Necromancer",
                    "Phalanx": "Phalanx",
                    "Phalanx Hollow": "Phalanx Hollow",
                    "Plow Scarecrow": "Plow Scarecrow",
                    "Sentinel": "Sentinel",
                    "Shears Scarecrow": "Shears Scarecrow",
                    "Silver Knight Greatbowman": "Silver Knight Greatbowman",
                    "Silver Knight Spearman": "Silver Knight Spearman",
                    "Silver Knight Swordsman": "Silver Knight Swordsman",
                    "Skeleton Archer": "Skeleton Archer",
                    "Skeleton Beast": "Skeleton Beast",
                    "Skeleton Soldier": "Skeleton Soldier",
                    "Snow Rat": "Snow Rat",
                    "Stone Guardian": "Stone Guardian",
                    "Stone Knight": "Stone Knight"
                }

                self.campaign = []

                self.deathlyFreezeTarget = None

                # Create images
                # Enemies
                for enemy in allEnemies:
                    allEnemies[enemy]["imageOld"] = self.create_image(enemy + ".png", "enemyOld")
                    allEnemies[enemy]["imageOldLevel4"] = self.create_image(enemy + ".png", "enemyOldLevel4")
                    allEnemies[enemy]["imageNew"] = self.create_image(enemy + ".png", "enemyNew")
                    if enemy in enemies:
                        allEnemies[enemy]["image text"] = ImageTk.PhotoImage(self.create_image(enemy + ".png", "enemyText"))

                # Icons
                self.enemyNode2 = self.create_image("enemy_node_2.png", "enemyNode")
                self.bleed = self.create_image("bleed.png", "condition")

                # Keywords
                self.poisonMist = ImageTk.PhotoImage(self.create_image("poison_mist.png", "poisonMist"))
                self.darkness = ImageTk.PhotoImage(self.create_image("darkness.png", "darkness"))
                self.trial = ImageTk.PhotoImage(self.create_image("trial.png", "trial"))
                self.timer = ImageTk.PhotoImage(self.create_image("timer.png", "timer"))
                self.onslaught = ImageTk.PhotoImage(self.create_image("onslaught.png", "onslaught"))
                self.snowstorm = ImageTk.PhotoImage(self.create_image("snowstorm.png", "snowstorm"))
                self.hidden = ImageTk.PhotoImage(self.create_image("hidden.png", "hidden"))
                self.bitterCold = ImageTk.PhotoImage(self.create_image("bitter_cold.png", "bitterCold"))
                self.eerie = ImageTk.PhotoImage(self.create_image("eerie.png", "eerie"))
                self.barrage = ImageTk.PhotoImage(self.create_image("barrage.png", "barrage"))

                self.tooltips = []

                self.encounterTooltips = {
                    "A Trusty Ally": [
                        {"image": self.onslaught, "imageName": "onslaught"}
                        ],
                    "Abandoned and Forgotten": [
                        {"image": self.eerie, "imageName": "eerie"}
                        ],
                    "Altar of Bones": [
                        {"image": self.timer, "imageName": "timer"}
                        ],
                    "Central Plaza": [
                        {"image": self.barrage, "imageName": "barrage"}
                        ],
                    "Cold Snap": [
                        {"image": self.snowstorm, "imageName": "snowstorm"},
                        {"image": self.bitterCold, "imageName": "bitterCold"},
                        {"image": self.trial, "imageName": "trial"}
                        ],
                    "Corrupted Hovel": [
                        {"image": self.poisonMist, "imageName": "poisonMist"},
                        {"image": self.trial, "imageName": "trial"}
                        ],
                    "Corvian Host": [
                        {"image": self.poisonMist, "imageName": "poisonMist"}
                        ],
                    "Dark Resurrection": [
                        {"image": self.darkness, "imageName": "darkness"}
                        ],
                    "Deathly Freeze": [
                        {"image": self.snowstorm, "imageName": "snowstorm"},
                        {"image": self.bitterCold, "imageName": "bitterCold"}
                        ],
                    "Distant Tower": [
                        {"image": self.barrage, "imageName": "barrage"},
                        {"image": self.trial, "imageName": "trial"}
                        ],
                    "Eye of the Storm": [
                        {"image": self.hidden, "imageName": "hidden"}
                        ],
                    "Far From the Sun": [
                        {"image": self.darkness, "imageName": "darkness"}
                        ],
                    "Frozen Revolutions": [
                        {"image": self.trial, "imageName": "trial"}
                        ],
                    "Frozen Sentries": [
                        {"image": self.snowstorm, "imageName": "snowstorm"}
                        ],
                    "Giant's Coffin": [
                        {"image": self.onslaught, "imageName": "onslaught"},
                        {"image": self.trial, "imageName": "trial"},
                        {"image": self.timer, "imageName": "timer"}
                        ],
                    "Gnashing Beaks": [
                        {"image": self.trial, "imageName": "trial"}
                        ],
                    "In Deep Water": [
                        {"image": self.timer, "imageName": "timer"}
                        ],
                    "Inhospitable Ground": [
                        {"image": self.snowstorm, "imageName": "snowstorm"}
                        ],
                    "Lakeview Refuge": [
                        {"image": self.onslaught, "imageName": "onslaught"},
                        {"image": self.darkness, "imageName": "darkness"},
                        {"image": self.trial, "imageName": "trial"}
                        ],
                    "Last Rites": [
                        {"image": self.timer, "imageName": "timer"}
                        ],
                    "Last Shred of Light": [
                        {"image": self.darkness, "imageName": "darkness"}
                        ],
                    "No Safe Haven": [
                        {"image": self.poisonMist, "imageName": "poisonMist"}
                        ],
                    "Painted Passage": [
                        {"image": self.snowstorm, "imageName": "snowstorm"}
                        ],
                    "Pitch Black": [
                        {"image": self.darkness, "imageName": "darkness"}
                        ],
                    "Promised Respite": [
                        {"image": self.snowstorm, "imageName": "snowstorm"}
                        ],
                    "Skeleton Overlord": [
                        {"image": self.timer, "imageName": "timer"}
                        ],
                    "Snowblind": [
                        {"image": self.snowstorm, "imageName": "snowstorm"},
                        {"image": self.bitterCold, "imageName": "bitterCold"},
                        {"image": self.hidden, "imageName": "hidden"}
                        ],
                    "The Beast From the Depths": [
                        {"image": self.trial, "imageName": "trial"}
                        ],
                    "The First Bastion": [
                        {"image": self.trial, "imageName": "trial"}
                        ],
                    "The Last Bastion": [
                        {"image": self.snowstorm, "imageName": "snowstorm"},
                        {"image": self.bitterCold, "imageName": "bitterCold"},
                        {"image": self.trial, "imageName": "trial"}
                        ],
                    "The Locked Grave": [
                        {"image": self.trial, "imageName": "trial"}
                        ],
                    "The Mass Grave": [
                        {"image": self.onslaught, "imageName": "onslaught"},
                        {"image": self.timer, "imageName": "timer"},
                        {"image": self.timer, "imageName": "timer"},
                        {"image": self.timer, "imageName": "timer"}
                        ],
                    "Trecherous Tower": [
                        {"image": self.snowstorm, "imageName": "snowstorm"},
                        {"image": self.bitterCold, "imageName": "bitterCold"},
                        {"image": self.eerie, "imageName": "eerie"}
                        ],
                    "Unseen Scurrying": [
                        {"image": self.hidden, "imageName": "hidden"}
                        ]
                }
                
                self.selected = None
                self.newEnemies = []
                self.newTiles = dict()
                self.rewardTreasure = None
            except Exception as e:
                adapter.exception(e)
                raise


        def least_frequent_items(self, listToCheck):
            """
            Return the least frequent element in a list.
            Used for cycling things like Trial targets.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of least_frequent_items: listToCheck=" + str(listToCheck), caller=calframe[1][3])

                n = len(listToCheck)

                # Create a dictionary and store the frequency counts as values.
                freq = dict()
                for i in range(n):
                    if listToCheck[i] in freq.keys():
                        freq[listToCheck[i]] += 1
                    else:
                        freq[listToCheck[i]] = 1

                if n > 3:
                    cutoff = -2
                else:
                    cutoff = -1

                res = choice([item[0] for item in sorted(freq.items(), key=lambda x: x[1])][:cutoff])

                adapter.debug("End of least_frequent_items, returning " + str(res))
                    
                return res
            except Exception as e:
                adapter.exception(e)
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
            

        def popup(self, labelText, buttonText):
            """
            Create a popup window for informing or requesting information from the user.

            Required Parameters:
                labelText: String
                    The text displayed in the popup window.

                buttonText: String
                    The text to display in the first button. If None, no button is displayed.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of popup: labelText=" + labelText + ", buttonText=" + str(buttonText), caller=calframe[1][3])
                
                self.set_bindings_buttons_menus(False)
                p = PopupWindow(self.master, labelText, buttonText=buttonText)
                self.master.wait_window(p.top)
                self.set_bindings_buttons_menus(True)

                adapter.debug("End of popup")
            except Exception as e:
                adapter.exception(e)
                raise


        def add_encounter_to_campaign(self):
            """
            Adds an encounter card to the campaign, visible in the campaign treeview.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of add_encounter_to_campaign", caller=calframe[1][3])

                if not self.selected:
                    adapter.debug("End of add_encounter_to_campaign (nothing done)")
                    return
                
                # Build the dictionary that will be saved to JSON if this campaign is saved.
                encounter = {
                    "name": self.selected["name"],
                    "expansion": self.selected["expansion"],
                    "level": self.selected["level"],
                    "enemies": self.newEnemies,
                    "trialTarget": self.trialTarget,
                    "rewardTreasure": self.rewardTreasure
                }

                # Only allow one encounter of the same name per campaign.
                if encounter["name"] not in set([e["name"] for e in self.campaign]):
                    self.campaign.append(encounter)
                    self.treeviewCampaign.insert(parent="", values=(encounter["name"], encounter["level"]), index="end")

                adapter.debug("End of add_encounter_to_campaign")
            except Exception as e:
                adapter.exception(e)
                raise


        def add_boss_to_campaign(self):
            """
            Adds a boss to the campaign, visible in the campaign treeview.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of add_boss_to_campaign", caller=calframe[1][3])

                # If a menu item that isn't a boss (e.g. --Mini Boss--) is selected in the combobox, don't do anything.
                if self.selectedBoss.get() not in self.bosses:
                    adapter.debug("End of add_boss_to_campaign (nothing done)")
                    return
                
                # Only allow a boss to appear once in a campaign.
                if self.selectedBoss.get() not in set([e["name"] for e in self.campaign]):
                    self.campaign.append(self.bosses[self.selectedBoss.get()])
                    self.treeviewCampaign.insert(parent="", values=(self.campaign[-1]["name"], self.campaign[-1]["level"]), index="end")

                adapter.debug("End of add_boss_to_campaign")
            except Exception as e:
                adapter.exception(e)
                raise


        def delete_encounter_from_campaign(self, event=None):
            """
            Delete an encounter or boss from the campaign.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of delete_encounter_from_campaign", caller=calframe[1][3])
                
                # If the button is clicked with no selection, do nothing.
                if not self.treeviewCampaign.selection():
                    adapter.debug("End of delete_encounter_from_campaign (nothing done)")
                    return

                # Remove the deleted encounters from the campaign list.
                self.campaign = [e for e in self.campaign if e["name"] not in set([self.treeviewCampaign.item(e)["values"][0] for e in self.treeviewCampaign.selection()])]
                
                # Remove the deleted encounters from the treeview.
                for item in self.treeviewCampaign.selection():
                    self.treeviewCampaign.delete(item)

                # Remove the image displaying a deleted encounter.
                self.encounter.config(image="")

                adapter.debug("End of delete_encounter_from_campaign")
            except Exception as e:
                adapter.exception(e)
                raise


        def save_campaign(self):
            """
            Save the campaign to a JSON file that can be loaded later.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of save_campaign", caller=calframe[1][3])

                # Prompt user to save the file.
                campaignName = filedialog.asksaveasfile(mode="w", initialdir=baseFolder + "\\saved campaigns", defaultextension=".json")

                # If they canceled it, do nothing.
                if not campaignName:
                    adapter.debug("End of save_campaign (nothing done)")
                    return

                with open(campaignName.name, "w") as campaignFile:
                    dump(self.campaign, campaignFile)

                adapter.debug("End of save_campaign (saved to " + str(campaignFile) + ")")
            except Exception as e:
                adapter.exception(e)
                raise


        def load_campaign(self):
            """
            Load a campaign from a JSON file, clearing the current campaign treeview and replacing
            it with the data from the JSON file.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of load_campaign", caller=calframe[1][3])

                # Prompt the user to find the campaign file.
                campaignFile = filedialog.askopenfilename(initialdir=baseFolder + "\\saved campaigns", filetypes = [(".json", ".json")])

                # If the user did not select a file, do nothing.
                if not campaignFile:
                    adapter.debug("End of load_campaign (file dialog canceled)")
                    return
                
                # If the user did not select a JSON file, notify them that that was an invalid file.
                if os.path.splitext(campaignFile)[1] != ".json":
                    self.popup("Invalid DSBG-Shuffle campaign file.", "Ok")
                    adapter.debug("End of load_campaign (invalid file)")
                    return
                
                adapter.debug("Loading file " + campaignFile)

                with open(campaignFile, "r") as f:
                    self.campaign = load(f)

                # Check to see if there are any invalid names or levels in the JSON file.
                # This is about as sure as I can be that you can't load random JSON into the app.
                if any([(item["name"] not in encounters and item["name"] not in self.bosses) or item["level"] not in set([1, 2, 3, 4, "Mini Boss", "Main Boss", "Mega Boss"]) for item in self.campaign]):
                    self.popup("Invalid DSBG-Shuffle campaign file.", "Ok")
                    self.campaign = []
                    adapter.debug("End of load_campaign (invalid file)")
                    return
                
                # Remove existing campaign elements.
                for item in self.treeviewCampaign.get_children():
                    self.treeviewCampaign.delete(item)

                # Create the campaign from the campaign list.
                for item in self.campaign:
                    self.treeviewCampaign.insert(parent="", values=(item["name"], item["level"]), index="end")

                adapter.debug("End of load_campaign (loaded from " + str(campaignFile) + ")")
            except Exception as e:
                adapter.exception(e)
                raise


        def move_up(self):
            """
            Move an item up in the campaign treeview, with corresponding movement in the campaign list.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of move_up", caller=calframe[1][3])
                
                leaves = self.treeviewCampaign.selection()
                for i in leaves:
                    self.treeviewCampaign.move(i, self.treeviewCampaign.parent(i), self.treeviewCampaign.index(i) - 1)
                    self.campaign.insert(self.treeviewCampaign.index(i) + 1, self.campaign.pop(self.treeviewCampaign.index(i)))
                
                adapter.debug("End of move_up")
            except Exception as e:
                adapter.exception(e)
                raise


        def move_down(self):
            """
            Move an item down in the campaign treeview, with corresponding movement in the campaign list.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of move_down", caller=calframe[1][3])

                leaves = self.treeviewCampaign.selection()
                for i in reversed(leaves):
                    self.treeviewCampaign.move(i, self.treeviewCampaign.parent(i), self.treeviewCampaign.index(i) + 1)
                    self.campaign.insert(self.treeviewCampaign.index(i) - 1, self.campaign.pop(self.treeviewCampaign.index(i)))

                adapter.debug("End of move_down")
            except Exception as e:
                adapter.exception(e)
                raise


        def load_campaign_encounter(self, event=None):
            """
            When an encounter in the campaign is clicked on, display the encounter
            and enemies that were originally saved.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of load_campaign_encounter", caller=calframe[1][3])

                self.selected = None
                self.rewardTreasure = None
                self.encounter.unbind("<Button 1>")

                tree = event.widget

                # Don't update the image shown if you've selected more than one encounter.
                if len(tree.selection()) != 1:
                    adapter.debug("End of load_campaign_encounter (not updating image)")
                    return
                
                # Get the encounter selected.
                campaignEncounter = [e for e in self.campaign if e["name"] == tree.item(tree.selection())["values"][0]]

                self.rewardTreasure = campaignEncounter[0]["rewardTreasure"]

                # If the selected encounter is a boss.
                if campaignEncounter[0]["name"] in self.bosses:
                    # Remove keyword tooltips from the previous encounter shown, if there are any.
                    for tooltip in self.tooltips:
                        tooltip.destroy()

                    # Create and display the boss image.
                    self.create_image(campaignEncounter[0]["name"] + ".jpg", "encounter", 4)
                    self.encounterPhotoImage = ImageTk.PhotoImage(self.encounterImage)
                    self.encounter.image = self.encounterPhotoImage
                    self.encounter.config(image=self.encounterPhotoImage)
                elif campaignEncounter:
                    adapter.debug("\tOpening " + baseFolder + "\\encounters\\" + campaignEncounter[0]["name"] + ".json", caller=calframe[1][3])
                    # Get the enemy slots for this encounter.
                    with open(baseFolder + "\\encounters\\" + campaignEncounter[0]["name"] + ".json") as alternativesFile:
                        alts = load(alternativesFile)

                    # Create the encounter card with saved enemies and tooltips.
                    self.newEnemies = campaignEncounter[0]["enemies"]
                    self.trialTarget = campaignEncounter[0]["trialTarget"]
                    self.edit_encounter_card(campaignEncounter[0]["name"], campaignEncounter[0]["expansion"], campaignEncounter[0]["level"], alts["enemySlots"])

                adapter.debug("End of load_campaign_encounter")
            except Exception as e:
                adapter.exception(e)
                raise


        def set_encounter_list(self):
            """
            Sets of the list of available encounters in the encounter tab based on what
            the user selected in the settings.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of set_encounter_list", caller=calframe[1][3])

                # Set the list of encounters based on available sets.
                self.encounterList = [encounter for encounter in encounters if (
                    (
                        (self.availableSets & {"Explorers", "Phantoms"}
                            or encounter not in encountersWithInvadersOrMimics)
                        and any([frozenset(expCombo).issubset(self.availableSets) for expCombo in encounters[encounter]["setCombos"]])
                    )
                    # Because these two have their enemies set on the fly, I can't guarantee there are valid enemies
                    # without the Painted World core set.
                    and (encounter != "Abandoned and Forgotten" or "Painted World of Ariamis" in self.availableSets)
                    and (encounter != "Trecherous Tower" or "Painted World of Ariamis" in self.availableSets)
                    )]

                adapter.debug("End of set_encounter_list")
            except Exception as e:
                adapter.exception(e)
                raise


        def create_tabs(self, event=None):
            """
            Create the encounter and campaign tabs in the main window.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_tabs", caller=calframe[1][3])

                with open(baseFolder + "\\settings.json") as settingsFile:
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
                
                self.addButton = ttk.Button(self.campaignTabButtonsFrame, text="Add Encounter", width=16, command=self.add_encounter_to_campaign)
                self.addButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.deleteButton = ttk.Button(self.campaignTabButtonsFrame, text="Remove Encounter", width=16, command=self.delete_encounter_from_campaign)
                self.deleteButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.loadButton = ttk.Button(self.campaignTabButtonsFrame, text="Load Campaign", width=16, command=self.load_campaign)
                self.loadButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.saveButton = ttk.Button(self.campaignTabButtonsFrame, text="Save Campaign", width=16, command=self.save_campaign)
                self.saveButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                
                self.moveUpButton = ttk.Button(self.campaignTabButtonsFrame2, text="Move Up", width=16, command=self.move_up)
                self.moveUpButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.moveDownButton = ttk.Button(self.campaignTabButtonsFrame2, text="Move Down", width=16, command=self.move_down)
                self.moveDownButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.addBossButton = ttk.Button(self.campaignTabButtonsFrame2, text="Add Boss", width=16, command=self.add_boss_to_campaign)
                self.addBossButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
                self.bossMenu = ttk.Combobox(self.campaignTabButtonsFrame2, state="readonly", values=self.bossMenu, textvariable=self.selectedBoss)
                self.bossMenu.current(0)
                self.bossMenu.config(width=17)
                self.bossMenu.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

                adapter.debug("End of create_tabs")
            except Exception as e:
                adapter.exception(e)
                raise


        def create_encounters_treeview(self):
            """
            Create the encounters treeview, where a user can select an encounter
            and shuffle the enemies in it.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_encounters_treeview", caller=calframe[1][3])
                
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
                # 2. Core sets first
                # 3. The Executioner's Chariot at the top of the mega bosses list because it has non-level 4 encounters
                # 4. By level
                # 5. Alphabetically
                encountersSorted = [encounter for encounter in sorted(self.encounterList, key=lambda x: (
                    1 if encounters[x]["level"] == 4 else 0,
                    0 if encounters[x]["expansion"] in coreSets else 1,
                    0 if encounters[x]["expansion"] != "The Executioner's Chariot" else 1,
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
                
                global settingsChanged
                settingsChanged = False

                adapter.debug("End of create_encounters_treeview")
            except Exception as e:
                adapter.exception(e)
                raise


        def create_campaign_treeview(self):
            """
            Create the campaign treeview where users can see saved encounters they've selected.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_campaign_treeview", caller=calframe[1][3])
                
                self.treeviewCampaign = ttk.Treeview(
                    self.campaignTabTreeviewFrame,
                    selectmode="extended",
                    columns=("Name", "Level"),
                    yscrollcommand=self.scrollbarTreeviewCampaign.set,
                    height=29 if root.winfo_screenheight() > 1000 else 20,
                    show=["headings"]
                )
                
                self.treeviewCampaign.pack(expand=True, fill="both")
                self.scrollbarTreeviewCampaign.config(command=self.treeviewCampaign.yview)

                self.treeviewCampaign.column("#1", anchor="w")
                self.treeviewCampaign.heading("#1", text="Name", anchor="w")
                self.treeviewCampaign.column("#2", anchor="w")
                self.treeviewCampaign.heading("#2", text="Level", anchor="w")
                
                self.treeviewCampaign.bind("<<TreeviewSelect>>", self.load_campaign_encounter)
                self.treeviewCampaign.bind("<Control-a>", lambda *args: self.treeviewCampaign.selection_add(self.treeviewCampaign.get_children()))

                adapter.debug("End of create_campaign_treeview")
            except Exception as e:
                adapter.exception(e)
                raise


        def create_encounter_frame(self):
            """
            Create the frame in which encounters will be displayed.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_encounter_frame", caller=calframe[1][3])

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

                adapter.debug("End of create_encounter_frame")
            except Exception as e:
                adapter.exception(e)
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
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of set_bindings_buttons_menus: enable=" + str(enable), caller=calframe[1][3])

                if enable:
                    enable_binding("Key-1", lambda x: self.keybind_call("1"))
                    enable_binding("Key-2", lambda x: self.keybind_call("2"))
                    enable_binding("Key-3", lambda x: self.keybind_call("3"))
                    enable_binding("Key-4", lambda x: self.keybind_call("4"))
                    enable_binding("s", self.shuffle_enemies)
                    enable_binding("Control-q", lambda x: self.keybind_call("q"))
                else:
                    enable_binding("Key-1", do_nothing)
                    enable_binding("Key-2", do_nothing)
                    enable_binding("Key-3", do_nothing)
                    enable_binding("Key-4", do_nothing)
                    enable_binding("s", do_nothing)

                if enable:
                    self.fileMenu.entryconfig("Random Level 1 Encounter", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Random Level 2 Encounter", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Random Level 3 Encounter", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Random Level 4 Encounter", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Shuffle Enemies", state=tk.NORMAL)
                else:
                    self.fileMenu.entryconfig("Random Level 1 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Random Level 2 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Random Level 3 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Random Level 4 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Shuffle Enemies", state=tk.DISABLED)

                adapter.debug("End of set_bindings_buttons_menus")
            except Exception as e:
                adapter.exception(e)
                raise
                   

        def create_buttons(self):
            """
            Create the buttons on the main screen.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_buttons", caller=calframe[1][3])

                self.buttonsFrame = ttk.Frame(self)
                self.buttonsFrame.grid(row=0, column=0, pady=(10, 0), sticky="nw")
                self.buttonsFrame.columnconfigure(index=0, weight=1)

                self.buttons = set()
                self.l1 = ttk.Button(self.buttonsFrame, text="Random Level 1", width=14, command=lambda x=1: self.random_encounter(level=x))
                self.l2 = ttk.Button(self.buttonsFrame, text="Random Level 2", width=14, command=lambda x=2: self.random_encounter(level=x))
                self.l3 = ttk.Button(self.buttonsFrame, text="Random Level 3", width=14, command=lambda x=3: self.random_encounter(level=x))
                self.l4 = ttk.Button(self.buttonsFrame, text="Random Level 4", width=14, command=lambda x=4: self.random_encounter(level=x))
                self.buttons.add(self.l1)
                self.buttons.add(self.l2)
                self.buttons.add(self.l3)
                self.buttons.add(self.l4)
                self.l1.grid(column=0, row=0, padx=5)
                self.l2.grid(column=1, row=0, padx=5)
                self.l3.grid(column=2, row=0, padx=5)
                self.l4.grid(column=3, row=0, padx=5)

                adapter.debug("End of create_buttons", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def create_menu(self):
            """
            Create the menu.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_menu", caller=calframe[1][3])
                
                menuBar = tk.Menu()
                self.fileMenu = tk.Menu(menuBar, tearoff=0)
                self.fileMenu.add_command(label="Random Level 1 Encounter", command=lambda x=1: self.random_encounter(level=x), accelerator="1")
                self.fileMenu.add_command(label="Random Level 2 Encounter", command=lambda x=2: self.random_encounter(level=x), accelerator="2")
                self.fileMenu.add_command(label="Random Level 3 Encounter", command=lambda x=3: self.random_encounter(level=x), accelerator="3")
                self.fileMenu.add_command(label="Random Level 4 Encounter", command=lambda x=4: self.random_encounter(level=x), accelerator="4")
                self.fileMenu.add_command(label="Shuffle Enemies", command=self.shuffle_enemies, accelerator="s")
                self.fileMenu.add_separator()
                self.fileMenu.add_command(label="Quit", command=root.quit, accelerator="Ctrl+Q")
                menuBar.add_cascade(label="File", menu=self.fileMenu)

                self.optionsMenu = tk.Menu(menuBar, tearoff=0)
                self.optionsMenu.add_command(label="Enabled Sets", command=self.settings_window)
                menuBar.add_cascade(label="Settings", menu=self.optionsMenu)

                self.helpMenu = tk.Menu(menuBar, tearoff=0)
                self.helpMenu.add_command(label="How to use ", command=self.help_window)
                menuBar.add_cascade(label="Help", menu=self.helpMenu)

                root.config(menu=menuBar)

                adapter.debug("End of create_menu", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def keybind_call(self, call, event=None):
            """
            Keyboard shortcut for creating a new set of word bingo cards.

            Required Parameters:
                call: String
                    The keybind activated.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of keybind_call: call=" + call, caller=calframe[1][3])

                if call == "1":
                    self.random_encounter(level=1)
                elif call == "2":
                    self.random_encounter(level=2)
                elif call == "3":
                    self.random_encounter(level=3)
                elif call == "4":
                    self.random_encounter(level=4)
                elif call == "s":
                    self.shuffle_enemies()
                elif call == "q":
                    root.quit()

                adapter.debug("End of keybind_call", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def settings_window(self):
            """
            Show the settings window, where a user can change what sets are active and
            whether random encounters show old, new, or both kinds of encounters.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of settings_window", caller=calframe[1][3])

                self.set_bindings_buttons_menus(False)

                s = SettingsWindow(root)
                        
                self.wait_window(s.top)
                
                if settingsChanged and self.treeviewEncounters.winfo_exists():
                    with open(baseFolder + "\\settings.json") as settingsFile:
                        self.settings = load(settingsFile)
                    self.selected = None
                    self.rewardTreasure = None
                    self.encounter.config(image="")
                    self.treeviewEncounters.pack_forget()
                    self.treeviewEncounters.destroy()
                    self.availableSets = set(self.settings["availableSets"])
                    self.availableCoreSets = coreSets & self.availableSets
                    oldSets = {"Dark Souls The Board Game", "Darkroot", "The Executioner's Chariot", "Explorers", "Iron Keep"} if "old" in self.settings["randomEncounterTypes"] else set()
                    newSets = (self.allSets - {"Dark Souls The Board Game", "Darkroot", "The Executioner's Chariot", "Explorers", "Iron Keep"}) if "new" in self.settings["randomEncounterTypes"] else set()
                    self.setsForRandomEncounters = (oldSets | newSets) & self.allSets
                    self.set_encounter_list()
                    self.create_encounters_treeview()
                
                self.set_bindings_buttons_menus(True)

                adapter.debug("End of settings_window", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def help_window(self):
            """
            Display the help window, which shows basic usage information.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of settings_window", caller=calframe[1][3])

                self.set_bindings_buttons_menus(False)
                h = HelpWindow(root)
                self.wait_window(h.top)
                self.set_bindings_buttons_menus(True)

                adapter.debug("End of settings_window", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
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
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_image", caller=calframe[1][3])

                imagePath = baseFolder + "\\images\\" + (imageFileName[:-4] + " rule bg.jpg" if imageType == "enemyText" else imageFileName)
                adapter.debug("\tOpening " + imagePath, caller=calframe[1][3])

                if imageType == "encounter":
                    if imageFileName == "Ornstein and Smough.jpg":
                        width = 305
                        height = 850
                    elif level < 4 and expansion in {"Dark Souls The Board Game", "Iron Keep", "Darkroot", "Explorers", "The Executioner's Chariot"}:
                        width = 200
                        height = 300
                    elif level == 4:
                        width = 305
                        height = 424
                    else:
                        width = 400
                        height = 685

                    self.encounterImage = Image.open(imagePath).resize((width, height), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.encounterImage)
                elif imageType == "enemyOld":
                    image = Image.open(imagePath).resize((27, 27), Image.Resampling.LANCZOS)
                elif imageType == "enemyOldLevel4":
                    image = Image.open(imagePath).resize((32, 32), Image.Resampling.LANCZOS)
                elif imageType == "enemyNew":
                    image = Image.open(imagePath).resize((22, 22), Image.Resampling.LANCZOS)
                elif imageType == "enemyText":
                    image = Image.open(imagePath).resize((14, 14), Image.Resampling.LANCZOS)
                elif imageType == "resurrection":
                    image = Image.open(imagePath).resize((9, 17), Image.Resampling.LANCZOS)
                elif imageType == "playerCount":
                    image = Image.open(imagePath).resize((12, 12), Image.Resampling.LANCZOS)
                elif imageType == "enemyNode":
                    image = Image.open(imagePath).resize((12, 12), Image.Resampling.LANCZOS)
                elif imageType == "condition":
                    image = Image.open(imagePath).resize((13, 13), Image.Resampling.LANCZOS)
                elif imageType == "poisonMist":
                    image = Image.open(imagePath).resize((61, 13), Image.Resampling.LANCZOS)
                elif imageType == "darkness":
                    image = Image.open(imagePath).resize((48, 13), Image.Resampling.LANCZOS)
                elif imageType == "trial":
                    image = Image.open(imagePath).resize((26, 13), Image.Resampling.LANCZOS)
                elif imageType == "timer":
                    image = Image.open(imagePath).resize((31, 13), Image.Resampling.LANCZOS)
                elif imageType == "onslaught":
                    image = Image.open(imagePath).resize((54, 13), Image.Resampling.LANCZOS)
                elif imageType == "snowstorm":
                    image = Image.open(imagePath).resize((56, 13), Image.Resampling.LANCZOS)
                elif imageType == "hidden":
                    image = Image.open(imagePath).resize((38, 13), Image.Resampling.LANCZOS)
                elif imageType == "bitterCold":
                    image = Image.open(imagePath).resize((56, 13), Image.Resampling.LANCZOS)
                elif imageType == "eerie":
                    image = Image.open(imagePath).resize((27, 13), Image.Resampling.LANCZOS)
                elif imageType == "barrage":
                    image = Image.open(imagePath).resize((41, 13), Image.Resampling.LANCZOS)

                adapter.debug("\tEnd of create_image", caller=calframe[1][3])
                
                return image
            except Exception as e:
                adapter.exception(e)
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
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of random_encounter", caller=calframe[1][3])

                self.load_encounter(encounter=choice([encounter for encounter in self.encounterList if (
                    encounters[encounter]["level"] == level
                    and (encounters[encounter]["expansion"] in self.setsForRandomEncounters
                        or encounters[encounter]["level"] == 4))]))

                adapter.debug("\tEnd of random_encounter", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def load_encounter(self, event=None, encounter=None):
            """
            Loads an encounter from file data for display.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
                    Default: None

                encounter: String
                    The expansion of the encounter.
                    Default: None
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of load_encounter", caller=calframe[1][3])
                
                self.treeviewEncounters.unbind("<<TreeviewSelect>>")

                # If this encounter was clicked on, get that information.
                if event:
                    tree = event.widget
                    if not tree.item(tree.selection())["tags"][0]:
                        adapter.debug("\tNo encounter selected", caller=calframe[1][3])
                        self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)
                        adapter.debug("\tEnd of load_encounter", caller=calframe[1][3])
                        return
                    encounterName = tree.item(tree.selection())["text"]
                else:
                    encounterName = encounter

                # If the encounter clicked on is already displayed, no need to load it again,
                # just shuffle the enemies.
                if encounters[encounterName] == self.selected:
                    self.shuffle_enemies()
                    self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)
                    adapter.debug("\tEnd of load_encounter", caller=calframe[1][3])
                    return
                
                self.selected = encounters[encounterName]
                self.selected["difficultyMod"] = {}
                self.selected["restrictRanged"] = {}

                # Get the possible alternative enemies from the encounter's file.
                adapter.debug("\tOpening " + baseFolder + "\\encounters\\" + encounterName + ".json", caller=calframe[1][3])
                with open(baseFolder + "\\encounters\\" + encounterName + ".json") as alternativesFile:
                    alts = load(alternativesFile)

                # If this encounter has a Trial Enemies file, load it.
                if os.path.isfile(baseFolder + "\\encounters\\" + encounterName + " Trial Enemies.json"):
                    adapter.debug("\tOpening " + baseFolder + "\\encounters\\" + encounterName + " Trial Enemies.json", caller=calframe[1][3])
                    with open(baseFolder + "\\encounters\\" + encounterName + " Trial Enemies.json") as trialFile:
                        self.trialEnemies = load(trialFile)
                else:
                    self.trialEnemies = []

                self.selected["alternatives"] = []
                self.selected["enemySlots"] = alts["enemySlots"]

                # Use only alternative enemies for sets the user has activated in the settings.
                for expansionCombo in alts["alternatives"]:
                    if set(expansionCombo.split(",")).issubset(self.availableSets):
                        self.selected["alternatives"] += alts["alternatives"][expansionCombo]

                self.newTiles = dict()

                self.shuffle_enemies()
                self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)
                self.encounter.bind("<Button 1>", self.shuffle_enemies)

                adapter.debug("\tEnd of load_encounter", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
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
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of shuffle_enemies", caller=calframe[1][3])

                self.encounter.bind("<Button 1>", do_nothing)
                if not self.selected:
                    adapter.debug("\tNo encounter loaded - nothing to shuffle", caller=calframe[1][3])
                    self.encounter.bind("<Button 1>", self.shuffle_enemies)
                    adapter.debug("\tEnd of shuffle_enemies", caller=calframe[1][3])
                    return
                
                self.rewardTreasure = None
                
                if self.selected["name"] in set(["Corvian Host", "Distant Tower"]):
                    self.trialTarget = self.least_frequent_items(self.trialEnemies)
                else:
                    self.trialTarget = None

                # Make sure a new set of enemies is chosen each time, otherwise it
                # feels like the program isn't doing anything.
                # Also, make sure we're rotating through Trial enemies faster than
                # pure random - encounters such as Corvian Host do not often show
                # Crow Demons as the Trial enemy if you have all sets enabled!
                oldEnemies = [e for e in self.newEnemies]
                self.newEnemies = choice(self.selected["alternatives"])
                if len(self.selected["alternatives"]) > 1:
                    while (self.newEnemies == oldEnemies
                           or (self.selected["name"] == "Corvian Host"
                               and sorted([enemy for enemy in self.newEnemies if enemyIds[enemy].health >= 5], key=lambda x: enemyIds[x].difficulty, reverse=True)[0] != self.trialTarget)
                           or (self.selected["name"] == "Distant Tower"
                               and sorted(self.newEnemies, key=lambda x: enemyIds[x].difficulty, reverse=True)[0] != self.trialTarget)):
                        self.newEnemies = choice(self.selected["alternatives"])

                if self.trialTarget:
                    self.trialEnemies.append(self.trialTarget)

                self.edit_encounter_card(self.selected["name"], self.selected["expansion"], self.selected["level"], self.selected["enemySlots"])

                adapter.debug("\tEnd of shuffle_enemies", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
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
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of edit_encounter_card", caller=calframe[1][3])

                self.encounterPhotoImage = self.create_image(name + ".jpg", "encounter", level, expansion)

                self.newTiles = {
                    1: [[], [], [], []],
                    2: [[], []],
                    3: [[], []]
                    }
                
                adapter.debug("New enemies: " + str(self.newEnemies), caller=calframe[1][3])
                        
                # Determine where enemies should be placed determined by whether this is an old or new style encounter,
                # the level of the encounter, and where on the original encounter card enemies were found.
                s = 0
                for slotNum, slot in enumerate(enemySlots):
                    for e in range(slot):
                        self.newTiles[1 if slotNum < 4 else 2 if slotNum < 6 else 3][slotNum - (0 if slotNum < 4 else 4 if slotNum < 6 else 6)].append(enemyIds[self.newEnemies[s]].name)
                        if level == 4:
                            x = 116 + (43 * e)
                            y = 78 + (47 * slotNum)
                            imageType = "imageOldLevel4"
                        elif expansion in {"Dark Souls The Board Game", "Iron Keep", "Darkroot", "Explorers", "The Executioner's Chariot"}:
                            x = 67 + (40 * e)
                            y = 66 + (46 * slotNum)
                            imageType = "imageOld"
                        else:
                            x = 300 + (29 * e)
                            y = 323 + (29 * (slotNum - (0 if slotNum < 4 else 4 if slotNum < 6 else 6))) + (((1 if slotNum < 4 else 2 if slotNum < 6 else 3) - 1) * 122)
                            imageType = "imageNew"

                        if enemyIds[self.newEnemies[s]].name == "Standard Invader/Hungry Mimic":
                            invaders = (["Hungry Mimic"] if "Explorers" in self.availableSets else []) + ([invader for invader in invadersStandard if invader != "Hungry Mimic" and "Phantoms" in self.availableSets])
                            image = allEnemies[choice(invaders)][imageType]
                        elif enemyIds[self.newEnemies[s]].name == "Advanced Invader/Voracious Mimic":
                            invaders = (["Voracious Mimic"] if "Explorers" in self.availableSets else []) + ([invader for invader in invadersAdvanced if invader != "Voracious Mimic" and "Phantoms" in self.availableSets])
                            image = allEnemies[choice(invaders)][imageType]
                        else:
                            image = allEnemies[enemyIds[self.newEnemies[s]].name][imageType]

                        adapter.debug("Pasting " + enemyIds[self.newEnemies[s]].name + " image onto encounter at " + str((x, y)) + ".", caller=calframe[1][3])
                        self.encounterImage.paste(im=image, box=(x, y), mask=image)
                        s += 1

                self.apply_keyword_tooltips(name)

                # # These are new encounters that have text referencing specific enemies.
                if name == "Abandoned and Forgotten":
                    self.abandoned_and_forgotten()
                elif name == "Cloak and Feathers":
                    self.cloak_and_feathers()
                elif name == "Cold Snap":
                    self.cold_snap()
                elif name == "Corvian Host":
                    self.corvian_host()
                elif name == "Corrupted Hovel":
                    self.corrupted_hovel()
                elif name == "Dark Resurrection":
                    self.dark_resurrection()
                elif name == "Deathly Freeze":
                    self.deathly_freeze()
                elif name == "Deathly Magic":
                    self.deathly_magic()
                elif name == "Distant Tower":
                    self.distant_tower()
                elif name == "Eye of the Storm":
                    self.eye_of_the_storm()
                elif name == "Frozen Revolutions":
                    self.frozen_revolutions()
                elif name == "Giant's Coffin":
                    self.giants_coffin()
                elif name == "Gnashing Beaks":
                    self.gnashing_beaks()
                elif name == "Grave Matters":
                    self.grave_matters()
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
                elif name == "Pitch Black":
                    self.pitch_black()
                elif name == "Puppet Master":
                    self.puppet_master()
                elif name == "Rain of Filth":
                    self.rain_of_filth()
                elif name == "Skeletal Spokes":
                    self.skeletal_spokes()
                elif name == "Skeleton Overlord":
                    self.skeleton_overlord()
                elif name == "The Abandoned Chest":
                    self.the_abandoned_chest()
                elif name == "The Beast From the Depths":
                    self.the_beast_from_the_depths()
                elif name == "The First Bastion":
                    self.the_first_bastion()
                elif name == "The Last Bastion":
                    self.the_last_bastion()
                elif name == "The Locked Grave":
                    self.the_locked_grave()
                elif name == "The Skeleton Ball":
                    self.the_skeleton_ball()
                elif name == "Trecherous Tower":
                    self.trecherous_tower()
                elif name == "Unseen Scurrying":
                    self.unseen_scurrying()
                elif name == "Urns of the Fallen":
                    self.urns_of_the_fallen()
                elif name == "Velka's Chosen":
                    self.velkas_chosen()
                
                self.encounterPhotoImage = ImageTk.PhotoImage(self.encounterImage)
                self.encounter.image = self.encounterPhotoImage
                self.encounter.config(image=self.encounterPhotoImage)
                self.encounter.bind("<Button 1>", self.shuffle_enemies)

                adapter.debug("\tEnd of edit_encounter_card", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def create_tooltip(self, image, text, x, y):
            """
            Create a label and tooltip that will be placed and later removed.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_tooltip", caller=calframe[1][3])

                label = tk.Label(self.encounterFrame, image=image, borderwidth=0, highlightthickness=0)
                self.tooltips.append(label)
                label.place(x=x, y=y)
                CreateToolTip(label, text)

                adapter.debug("\tEnd of create_tooltip", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def apply_keyword_tooltips(self, name):
            """
            If the encounter card has keywords, create an image of the word imposed over
            the original word and create a tooltip that shows up when mousing over the keyword image.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of apply_keyword_tooltips", caller=calframe[1][3])

                for tooltip in self.tooltips:
                    tooltip.destroy()

                if not self.selected and not self.treeviewCampaign.focus():
                    adapter.debug("\tEnd of apply_keyword_tooltips (removed tooltips only)", caller=calframe[1][3])
                    return

                for i, tooltip in enumerate(self.encounterTooltips.get(name, [])):
                    self.create_tooltip(image=tooltip["image"], text=self.tooltipText[tooltip["imageName"]], x=142, y=199 + (15.5 * i))

                adapter.debug("\tEnd of apply_keyword_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def abandoned_and_forgotten(self):
            """
            Choose enemies for Eerie keyword.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of abandoned_and_forgotten", caller=calframe[1][3])

                totalDifficulty = sum([enemiesDict["Phalanx Hollow"].difficulty, enemiesDict["Engorged Zombie"].difficulty, enemiesDict["Crow Demon"].difficulty])
                minDifficulty = totalDifficulty * 0.9
                maxDifficulty = totalDifficulty * 1.1
                allCombos = set(combinations([enemy for enemy in allEnemies if (
                    enemy not in invadersStandard
                    and enemy not in invadersAdvanced
                    and enemiesDict[enemy].expansion in self.availableSets)], 3))
                combos = [combo for combo in allCombos if minDifficulty <= sum([enemiesDict[enemy].difficulty for enemy in combo]) <= maxDifficulty]
                spawns = choice(combos)
                spawns = sorted(spawns, key=lambda x: enemiesDict[x].difficulty)

                self.encounterImage.paste(im=allEnemies[spawns[0]]["imageNew"], box=(285, 218), mask=allEnemies[spawns[0]]["imageNew"])
                self.encounterImage.paste(im=allEnemies[spawns[1]]["imageNew"], box=(285, 248), mask=allEnemies[spawns[1]]["imageNew"])
                self.encounterImage.paste(im=allEnemies[spawns[2]]["imageNew"], box=(285, 280), mask=allEnemies[spawns[2]]["imageNew"])

                adapter.debug("\tEnd of abandoned_and_forgotten", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def cloak_and_feathers(self):
            """
            Put enemy icon in the objective.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of cloak_and_feathers", caller=calframe[1][3])

                target = self.newTiles[1][0][0]
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=65, y=147)

                adapter.debug("\tEnd of cloak_and_feathers", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def cold_snap(self):
            """
            Modify trial text, add armor/resist to make the replacement enemy as tough as an Engorged Zombie.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of cold_snap", caller=calframe[1][3])

                coldSnapTarget = self.newTiles[2][0][1]

                image = allEnemies[coldSnapTarget]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[coldSnapTarget], x=216, y=227)

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if enemiesDict[coldSnapTarget].health == 1 and (enemiesDict[coldSnapTarget].armor < 2 or enemiesDict[coldSnapTarget].resist < 2):
                    self.create_tooltip(image=image, text=self.tooltipText[coldSnapTarget], x=207, y=251)

                    text = "Increase the \n"
                    if enemiesDict[coldSnapTarget].armor < 2 and enemiesDict[coldSnapTarget].resist < 2:
                        text += "block and resistance values to 2."
                    elif enemiesDict[coldSnapTarget].armor < 2:
                        text += "block value to 2."
                    elif enemiesDict[coldSnapTarget].resist < 2:
                        text += "resistance value to 2."
                    imageWithText.text((140, 250), text, "black", font)

                adapter.debug("\tEnd of cold_snap", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def corrupted_hovel(self):
            """
            Change Engorged Zombie to another enemy.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of corrupted_hovel", caller=calframe[1][3])

                target = [enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1] if (self.newTiles[1][0] + self.newTiles[1][1]).count(enemy) == 2][0]
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=146, y=250)

                adapter.debug("\tEnd of corrupted_hovel", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def corvian_host(self):
            """
            Change Crow Demons to another enemy.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of corvian_host", caller=calframe[1][3])

                target = enemyIds[self.trialTarget].name
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=159, y=238)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=255, y=238)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=242, y=251)

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if enemyIds[self.trialTarget].armor + enemyIds[self.trialTarget].resist <= 3:
                    self.create_tooltip(image=image, text=self.tooltipText[target], x=185, y=274)
                    text1 = "Increase       block and resistance"
                    text2 = "values by 1 and their attacks gain     ."
                    self.encounterImage.paste(im=self.bleed, box=(301, 284), mask=self.bleed)
                    imageWithText.text((140, 273), text1, "black", font, spacing=0)
                    imageWithText.text((140, 285), text2, "black", font, spacing=0)
                else:
                    self.create_tooltip(image=image, text=self.tooltipText[target], x=145, y=288)
                    text = "       attacks gain     ."
                    self.encounterImage.paste(im=self.bleed, box=(223, 287), mask=self.bleed)
                    imageWithText.text((140, 288), text, "black", font, spacing=0)
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                if newTreasure.count(" ") > 2:
                    breakIdx = newTreasure.rfind(" ", 0, newTreasure.rfind(" ") - 1)
                    newTreasure1 = newTreasure[:breakIdx]
                    newTreasure2 = newTreasure[breakIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                elif newTreasure.count(" ") > 0 and len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of corvian_host", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def dark_resurrection(self):
            """
            Swap treasure reward.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of dark_resurrection", caller=calframe[1][3])
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of dark_resurrection", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def deathly_freeze(self):
            """
            Change Engorged Zombie to another enemy.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of deathly_freeze", caller=calframe[1][3])
                    
                deathlyFreezeTile1 = [enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1]]
                deathlyFreezeTile2 = [enemy for enemy in self.newTiles[2][0] + self.newTiles[2][1]]
                overlap = set(deathlyFreezeTile1) & set(deathlyFreezeTile2)
                target = sorted([enemy for enemy in overlap if deathlyFreezeTile1.count(enemy) + deathlyFreezeTile2.count(enemy) > 1], key=lambda x: enemiesDict[x].difficulty, reverse=True)[0]

                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=141, y=242)

                adapter.debug("\tEnd of deathly_freeze", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def deathly_magic(self):
            """
            Change Necromancer to another enemy and specify starting health.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of deathly_magic", caller=calframe[1][3])
                target = sorted([enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1] if (self.newTiles[1][0] + self.newTiles[1][1]).count(enemy) == 1], key=lambda x: enemiesDict[x].difficulty, reverse=True)[0]
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=65, y=147)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=273, y=197)

                adapter.debug("\tEnd of deathly_magic", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def distant_tower(self):
            """
            Change trial objective Crow Demon to another enemy.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of distant_tower", caller=calframe[1][3])

                target = self.newTiles[3][0][0]
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=215, y=213)
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 283), newTreasure1, "black", font)
                    imageWithText.text((21, 294), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 283), newTreasure, "black", font)

                adapter.debug("\tEnd of distant_tower", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def eye_of_the_storm(self):
            """
            Change Phalanx objective to another enemy.
            Change Phalanx Hollows to another enemy.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of eye_of_the_storm", caller=calframe[1][3])
                
                totalDifficulty = sum([enemiesDict["Phalanx Hollow"].difficulty * 4, enemiesDict["Engorged Zombie"].difficulty, enemiesDict["Phalanx"].difficulty])

                diffMod = 0.1
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemies[enemy]["name"] for enemy in enemies if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and not enemies[enemy]["ranged"] and minDifficulty <= sum([
                            (enemiesDict[enemy].difficulty),
                            enemiesDict[self.newTiles[1][0][0]].difficulty,
                            enemiesDict[self.newTiles[1][1][0]].difficulty,
                            enemiesDict[self.newTiles[2][0][0]].difficulty,
                            enemiesDict[self.newTiles[2][1][0]].difficulty
                        ]) <= maxDifficulty
                        and enemiesDict[enemy].health >= 5)]
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                spawn = choice(enemyList)

                imageWithText = ImageDraw.Draw(self.encounterImage)
                fourTarget = [enemyIds[enemy].name for enemy in self.newEnemies if self.newEnemies.count(enemy) == 4]
                targets = list(set([enemyIds[enemy].name for enemy in self.newEnemies if self.newEnemies.count(enemy) == 2]))
                text1 = "Increase       "
                if fourTarget:
                    image1 = allEnemies[fourTarget[0]]["image text"]
                    self.create_tooltip(image=image1, text=self.tooltipText[fourTarget[0]], x=186, y=247)
                else:
                    image1 = allEnemies[targets[0]]["image text"]
                    image2 = allEnemies[targets[1]]["image text"]
                    self.create_tooltip(image=image1, text=self.tooltipText[targets[0]], x=186, y=247)
                    self.create_tooltip(image=image2, text=self.tooltipText[targets[1]], x=228, y=247)
                    text1 += " and       "
                text1 += "block and resistance"
                text2 = "values by 1. Once these enemies have been"
                text3 = "killed, spawn the       on      , on tile three."
                image3 = allEnemies[spawn]["image text"]
                self.create_tooltip(image=image3, text=self.tooltipText[spawn], x=226, y=274)
                self.create_tooltip(image=image3, text=self.tooltipText[spawn], x=65, y=147)
                self.encounterImage.paste(im=self.enemyNode2, box=(260, 272), mask=self.enemyNode2)
                imageWithText.text((140, 246), text1, "black", font)
                imageWithText.text((140, 259), text2, "black", font)
                imageWithText.text((140, 273), text3, "black", font)

                adapter.debug("\tEnd of eye_of_the_storm", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def frozen_revolutions(self):
            """
            Change Bonewheel Skeletons to another enemy and specify repeat behavior.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of frozen_revolutions", caller=calframe[1][3])

                target = self.newTiles[3][0][0]
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=143, y=225)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=143, y=238)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=348, y=238)
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 258), newTreasure1, "black", font)
                    imageWithText.text((21, 269), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 258), newTreasure, "black", font)

                adapter.debug("\tEnd of frozen_revolutions", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def giants_coffin(self):
            """
            Change Giant Skeleton Soldier and Giant Skeleton Archer to different enemies.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of giants_coffin", caller=calframe[1][3])
                
                totalDifficulty = sum([enemiesDict["Giant Skeleton Archer"].difficulty * 2, enemiesDict["Giant Skeleton Soldier"].difficulty * 3])
                diffMod = 0.1
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemies[enemy]["name"] for enemy in enemies if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and not enemies[enemy]["ranged"] and minDifficulty <= sum([
                            (enemiesDict[enemy].difficulty),
                            enemiesDict[self.newTiles[1][0][0]].difficulty,
                            enemiesDict[self.newTiles[1][1][0]].difficulty,
                            enemiesDict[self.newTiles[2][0][0]].difficulty,
                            enemiesDict[self.newTiles[2][1][0]].difficulty
                        ]) <= maxDifficulty)]
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                spawn1 = choice(enemyList)
                image = allEnemies[spawn1]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[spawn1], x=241, y=228)
                    
                totalDifficulty += enemiesDict["Giant Skeleton Archer"].difficulty
                diffMod = 0.1
                restrictRanged = True
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemies[enemy]["name"] for enemy in enemies if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and enemies[enemy]["ranged"] or not restrictRanged) and minDifficulty <= sum([
                            (enemiesDict[enemy].difficulty),
                            enemiesDict[self.newTiles[1][0][0]].difficulty,
                            enemiesDict[self.newTiles[1][1][0]].difficulty,
                            enemiesDict[self.newTiles[2][0][0]].difficulty,
                            enemiesDict[self.newTiles[2][1][0]].difficulty,
                            enemiesDict[spawn1].difficulty
                        ]) <= maxDifficulty]
                    if not enemyList:
                        diffMod += 0.05
                        if restrictRanged and diffMod > 0.2:
                            restrictRanged = False
                            diffMod = 0.1
                        continue
                    break
                spawn2 = choice(enemyList)
                image = allEnemies[spawn2]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[spawn2], x=280, y=228)
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 258), newTreasure1, "black", font)
                    imageWithText.text((21, 269), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 258), newTreasure, "black", font)

                adapter.debug("\tEnd of giants_coffin", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def gnashing_beaks(self):
            """
            Change Phalanx Hollows and Crow Demon to new enemies.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of gnashing_beaks", caller=calframe[1][3])
                
                totalDifficulty = sum([enemiesDict["Snow Rat"].difficulty * 2, enemiesDict["Crow Demon"].difficulty])
                diffMod = 0.1
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemies[enemy]["name"] for enemy in enemies if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and enemies[enemy]["count"] > 1 and minDifficulty <= sum([
                            (enemiesDict[enemy].difficulty * 2),
                            enemiesDict[self.newTiles[1][0][0]].difficulty,
                            enemiesDict[self.newTiles[1][1][0]].difficulty,
                            enemiesDict[self.newTiles[2][0][0]].difficulty
                        ]) <= maxDifficulty)]
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                spawn1 = choice(enemyList)
                image = allEnemies[spawn1]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[spawn1], x=333, y=232)
                    
                totalDifficulty += enemiesDict["Crow Demon"].difficulty
                diffMod = 0.1
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemies[enemy]["name"] for enemy in enemies if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and minDifficulty <= sum([
                            enemiesDict[enemy].difficulty,
                            enemiesDict[self.newTiles[1][0][0]].difficulty,
                            enemiesDict[self.newTiles[1][1][0]].difficulty,
                            enemiesDict[self.newTiles[2][0][0]].difficulty
                        ]) <= maxDifficulty)]
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                spawn2 = choice(enemyList)
                image = allEnemies[spawn2]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[spawn2], x=235, y=243)

                adapter.debug("\tEnd of gnashing_beaks", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def grave_matters(self):
            """
            Swap treasure reward.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of grave_matters", caller=calframe[1][3])
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of grave_matters", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def in_deep_water(self):
            """
            Change Skeleton Archer to new enemy.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of in_deep_water", caller=calframe[1][3])
                
                totalDifficulty = sum([enemiesDict["Giant Skeleton Soldier"].difficulty * 2, enemiesDict["Giant Skeleton Archer"].difficulty * 2])

                diffMod = 0.1
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemies[enemy]["name"] for enemy in enemies if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and enemies[enemy]["count"] > 1 and minDifficulty <= sum([
                            (enemiesDict[enemy].difficulty * 2),
                            enemiesDict[self.newTiles[1][0][0]].difficulty,
                            enemiesDict[self.newTiles[1][1][0]].difficulty
                        ]) <= maxDifficulty)]
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                spawn = choice(enemyList)
                image = allEnemies[spawn]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[spawn], x=247, y=198)
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of in_deep_water", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def inhospitable_ground(self):
            """
            Swap treasure reward.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of inhospitable_ground", caller=calframe[1][3])
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of inhospitable_ground", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def lakeview_refuge(self):
            """
            Update trial Skeleton Beast to new enemy and references to Skeleton Beast and Skeleton Soldiers to new enemies.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of lakeview_refuge", caller=calframe[1][3])

                allTileEnemies = (
                    self.newTiles[1][0]
                    + self.newTiles[1][1]
                    + self.newTiles[2][0]
                    + self.newTiles[2][1]
                    + self.newTiles[3][0]
                    + self.newTiles[3][1]
                )
                
                totalDifficulty = sum([
                    enemiesDict["Skeleton Soldier"].difficulty * 2,
                    enemiesDict["Giant Skeleton Archer"].difficulty,
                    enemiesDict["Skeleton Archer"].difficulty * 2,
                    enemiesDict["Giant Skeleton Soldier"].difficulty,
                    enemiesDict["Necromancer"].difficulty * 2,
                    enemiesDict["Skeleton Beast"].difficulty])
                diffMod = 0.1

                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemies[enemy]["name"] for enemy in enemies if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and minDifficulty <= sum([
                            (enemiesDict[enemy].difficulty),
                            sum([enemiesDict[e].difficulty for e in allTileEnemies])
                        ]) <= maxDifficulty
                        and enemy not in allTileEnemies
                        and (enemy != "Phalanx" or allTileEnemies.count("Phalanx Hollow") < 3)
                        and enemiesDict[enemy].health >= 5)]
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                spawn1 = choice(enemyList)
                allTileEnemies.append(spawn1)
                image1 = allEnemies[spawn1]["image text"]
                self.create_tooltip(image=image1, text=self.tooltipText[spawn1], x=225, y=228)
                self.create_tooltip(image=image1, text=self.tooltipText[spawn1], x=291, y=259)

                totalDifficulty += enemiesDict["Skeleton Soldier"].difficulty
                diffMod = 0.1
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemies[enemy]["name"] for enemy in enemies if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and enemies[enemy]["count"] > 1
                        and minDifficulty <= sum([
                            (enemiesDict[enemy].difficulty),
                            sum([enemiesDict[e].difficulty for e in allTileEnemies])
                            ]) <= maxDifficulty)
                        and enemy != spawn1
                        and (enemy != "Phalanx" or allTileEnemies.count("Phalanx Hollow") < 3)]
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                spawn2 = choice(enemyList)
                image2 = allEnemies[spawn2]["image text"]
                self.create_tooltip(image=image2, text=self.tooltipText[spawn2], x=245, y=273)

                adapter.debug("\tEnd of lakeview_refuge", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def monstrous_maw(self):
            """
            Change Snow Rat references to new enemy.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of monstrous_maw", caller=calframe[1][3])
                
                target = self.newTiles[1][1][0]
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=208, y=197)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=65, y=147)
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of monstrous_maw", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def no_safe_haven(self):
            """
            Change Engorged Zombie objective to new enemy.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of no_safe_haven", caller=calframe[1][3])

                target = self.newTiles[2][0][0]
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=63, y=147)
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of no_safe_haven", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def painted_passage(self):
            """
            Swap treasure reward.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of painted_passage", caller=calframe[1][3])
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of painted_passage", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def pitch_black(self):
            """
            Change Necromancer objective to new (and possibly different from each other) enemies.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of pitch_black", caller=calframe[1][3])

                tile1Enemies = self.newTiles[1][0] + self.newTiles[1][1]
                tile2Enemies = self.newTiles[2][0] + self.newTiles[2][1]
                target1 = sorted([enemy for enemy in tile1Enemies if tile1Enemies.count(enemy) == 1], key=lambda x: enemiesDict[x].difficulty, reverse=True)[0]
                target2 = sorted([enemy for enemy in tile2Enemies if tile2Enemies.count(enemy) == 1], key=lambda x: enemiesDict[x].difficulty, reverse=True)[0]
                image1 = allEnemies[target1]["image text"]
                image2 = allEnemies[target2]["image text"]
                self.create_tooltip(image=image1, text=self.tooltipText[target1], x=65, y=147)
                self.create_tooltip(image=image2, text=self.tooltipText[target2], x=219, y=147)

                adapter.debug("\tEnd of pitch_black", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def puppet_master(self):
            """
            Change Necromancer and Giant Skeleton Soldier to different enemies, specify Necromancer replacement starting health.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of puppet_master", caller=calframe[1][3])

                target1 = self.newTiles[1][0][1]
                target2 = self.newTiles[1][0][0]
                image1 = allEnemies[target1]["image text"]
                image2 = allEnemies[target2]["image text"]
                self.create_tooltip(image=image1, text=self.tooltipText[target1], x=65, y=147)
                self.create_tooltip(image=image2, text=self.tooltipText[target2], x=145, y=198)
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of puppet_master", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def rain_of_filth(self):
            """
            Swap treasure reward.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of rain_of_filth", caller=calframe[1][3])
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of rain_of_filth", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def skeletal_spokes(self):
            """
            Update Bonewheel Skeletons to different enemy.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of skeletal_spokes", caller=calframe[1][3])
                
                target = self.newTiles[2][0][0]
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=145, y=197)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=162, y=212)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=162, y=252)

                adapter.debug("\tEnd of skeletal_spokes", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def skeleton_overlord(self):
            """
            Update Giant Skeleton Soldier and Skeleton Soldier to different enemies.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of skeleton_overlord", caller=calframe[1][3])

                totalDifficulty = sum([enemiesDict["Giant Skeleton Soldier"].difficulty, (enemiesDict["Skeleton Soldier"].difficulty * enemies["Skeleton Soldier"]["count"])])

                diffMod = 0.1
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemy for enemy in enemiesDict if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and enemiesDict[enemy].health == 1
                        and minDifficulty <= (enemiesDict[enemy].difficulty * enemies[enemy]["count"]) + enemiesDict[self.newTiles[1][0][0]].difficulty <= maxDifficulty
                        and (enemy != "Phalanx Hollow" or self.newTiles[1][0][0] != "Phalanx"))]
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                spawn = choice(enemyList)
                image = allEnemies[spawn]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[spawn], x=241, y=198)
                self.create_tooltip(image=image, text=self.tooltipText[spawn], x=204, y=251)

                target = self.newTiles[1][0][0]
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=65, y=147)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=311, y=226)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=285, y=251)

                adapter.debug("\tEnd of skeleton_overlord", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_abandoned_chest(self):
            """
            Update Giant Skeleton Soldier and Giant Skeleton Archers to new enemies.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_abandoned_chest", caller=calframe[1][3])

                totalDifficulty = sum([enemiesDict["Necromancer"].difficulty, enemiesDict["Skeleton Archer"].difficulty, enemiesDict["Skeleton Soldier"].difficulty * enemies["Skeleton Soldier"]["count"], enemiesDict["Giant Skeleton Soldier"].difficulty])
                diffMod = 0.1
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemy for enemy in enemiesDict if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and minDifficulty <= sum([
                            enemiesDict[enemy].difficulty,
                            enemiesDict[self.newTiles[1][0][0]].difficulty,
                            enemiesDict[self.newTiles[1][0][1]].difficulty,
                            enemiesDict[self.newTiles[2][0][0]].difficulty,
                            enemiesDict[self.newTiles[2][1][0]].difficulty]) <= maxDifficulty
                        and (enemy != "Phalanx Hollow" or "Phalanx" not in self.newTiles[1][0] + self.newTiles[1][1] + self.newTiles[2][0] + self.newTiles[2][1]))]
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                spawn1 = choice(enemyList)
                image = allEnemies[spawn1]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[spawn1], x=321, y=197)

                totalDifficulty += enemiesDict["Giant Skeleton Archer"].difficulty
                diffMod = 0.1
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemy for enemy in enemiesDict if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and minDifficulty <= sum([
                            enemiesDict[enemy].difficulty,
                            enemiesDict[self.newTiles[1][0][0]].difficulty,
                            enemiesDict[self.newTiles[1][0][1]].difficulty,
                            enemiesDict[self.newTiles[2][0][0]].difficulty,
                            enemiesDict[self.newTiles[2][1][0]].difficulty,
                            enemiesDict[spawn1].difficulty]) <= maxDifficulty
                        and (enemy != "Phalanx Hollow" or "Phalanx" not in self.newTiles[1][0] + self.newTiles[1][1] + self.newTiles[2][0] + self.newTiles[2][1]))]
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                spawn2 = choice(enemyList)
                image = allEnemies[spawn2]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[spawn2], x=144, y=212)
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of the_abandoned_chest", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_beast_from_the_depths(self):
            """
            Update Skeleton Beast to different enemy.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_beast_from_the_depths", caller=calframe[1][3])

                target = self.newTiles[1][0][0]
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=65, y=147)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=154, y=220)
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 258), newTreasure1, "black", font)
                    imageWithText.text((21, 269), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 258), newTreasure, "black", font)

                adapter.debug("\tEnd of the_beast_from_the_depths", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_first_bastion(self):
            """
            Update Snow Rat, Phalanx Hollow, and Engorged Zombie to different enemies.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_first_bastion", caller=calframe[1][3])

                totalDifficulty = sum([enemiesDict["Snow Rat"].difficulty * 2])
                diffMod = 0.1
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemy for enemy in enemiesDict if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and minDifficulty <= sum([
                            enemiesDict[enemy].difficulty,
                            enemiesDict[self.newTiles[1][1][0]].difficulty]) <= maxDifficulty)]
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                spawn1 = choice(enemyList)
                image = allEnemies[spawn1]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[spawn1], x=363, y=220)

                totalDifficulty += enemiesDict["Phalanx Hollow"].difficulty
                diffMod = 0.1
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemy for enemy in enemiesDict if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and minDifficulty <= sum([
                            enemiesDict[enemy].difficulty,
                            enemiesDict[self.newTiles[1][1][0]].difficulty,
                            enemiesDict[spawn1].difficulty]) <= maxDifficulty)]
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                spawn2 = choice(enemyList)
                image = allEnemies[spawn2]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[spawn2], x=185, y=245)

                totalDifficulty += enemiesDict["Engorged Zombie"].difficulty
                diffMod = 0.1
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemy for enemy in enemiesDict if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and minDifficulty <= sum([
                            enemiesDict[enemy].difficulty,
                            enemiesDict[self.newTiles[1][1][0]].difficulty,
                            enemiesDict[spawn1].difficulty,
                            enemiesDict[spawn2].difficulty]) <= maxDifficulty
                            and enemy not in {spawn1, spawn2, self.newTiles[1][1][0]})]
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                spawn3 = choice(enemyList)
                image = allEnemies[spawn3]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[spawn3], x=236, y=257)
                self.create_tooltip(image=image, text=self.tooltipText[spawn3], x=214, y=197)

                adapter.debug("\tEnd of the_first_bastion", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_last_bastion(self):
            """
            Update Phalanx to different enemy and specify health, dodge, and damage.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_last_bastion", caller=calframe[1][3])
                
                target = sorted([enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1]], key=lambda x: enemiesDict[x].difficulty)[0]
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=215, y=227)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=315, y=250)

                adapter.debug("\tEnd of the_last_bastion", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_locked_grave(self):
            """
            Update Skeleton Beast to different enemy.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_locked_grave", caller=calframe[1][3])

                totalDifficulty = sum([
                    enemiesDict["Necromancer"].difficulty,
                    enemiesDict["Skeleton Archer"].difficulty * 2,
                    enemiesDict["Skeleton Soldier"].difficulty * enemies["Skeleton Soldier"]["count"],
                    enemiesDict["Giant Skeleton Soldier"].difficulty,
                    enemiesDict["Giant Skeleton Archer"].difficulty * 2,
                    enemiesDict["Skeleton Beast"].difficulty])

                newEnemies = self.newTiles[1][0][0] + self.newTiles[1][1][0] + self.newTiles[2][0][0] + self.newTiles[2][1][0] + self.newTiles[3][0][0] + self.newTiles[3][1][0] + self.newTiles[3][1][1]

                diffMod = 0.1
                while True:
                    minDifficulty = totalDifficulty * (1 - diffMod)
                    maxDifficulty = totalDifficulty * (1 + diffMod)
                    enemyList = [enemy for enemy in enemies if (
                        enemiesDict[enemy].expansion in self.availableSets
                        and enemiesDict[enemy].difficulty > 0
                        and minDifficulty <= sum([
                                enemiesDict[enemy].difficulty,
                                enemiesDict[self.newTiles[1][0][0]].difficulty,
                                enemiesDict[self.newTiles[1][1][0]].difficulty,
                                enemiesDict[self.newTiles[2][0][0]].difficulty,
                                enemiesDict[self.newTiles[2][1][0]].difficulty,
                                enemiesDict[self.newTiles[3][0][0]].difficulty,
                                enemiesDict[self.newTiles[3][1][0]].difficulty,
                                enemiesDict[self.newTiles[3][1][1]].difficulty]) <= maxDifficulty
                            and enemy not in newEnemies
                            and (enemy != "Phalanx" or newEnemies.count("Phalanx Hollow") < 3)
                            )]
                    if not enemyList:
                        diffMod += 0.05
                        continue
                    break
                
                target = choice(enemyList)
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=225, y=197)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=302, y=220)
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    if newTreasure.count(" ") > 1:
                        lastSpaceIdx = newTreasure.rfind(" ", 0, newTreasure.rfind(" "))
                    else:
                        lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((56, 258), newTreasure1, "black", font)
                    imageWithText.text((21, 270), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 270), newTreasure, "black", font)

                adapter.debug("\tEnd of the_locked_grave", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_skeleton_ball(self):
            """
            Update Necromancers to different enemy.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_skeleton_ball", caller=calframe[1][3])

                target1 = self.newTiles[1][0][0]
                target2 = self.newTiles[3][1][0]
                image1 = allEnemies[target1]["image text"]
                image2 = allEnemies[target2]["image text"]
                self.create_tooltip(image=image1, text=self.tooltipText[target1], x=64, y=147)
                self.create_tooltip(image=image2, text=self.tooltipText[target2], x=220, y=147)
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of the_skeleton_ball", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def trecherous_tower(self):
            """
            Choose enemies for Eerie keyword.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of trecherous_tower", caller=calframe[1][3])

                totalDifficulty = sum([enemiesDict["Phalanx Hollow"].difficulty, enemiesDict["Engorged Zombie"].difficulty, enemiesDict["Crow Demon"].difficulty])
                minDifficulty = totalDifficulty * 0.9
                maxDifficulty = totalDifficulty * 1.1
                allCombos = set(combinations([enemy for enemy in allEnemies if (
                    enemy not in invadersStandard
                    and enemy not in invadersAdvanced
                    and enemiesDict[enemy].expansion in self.availableSets)], 3))
                combos = [combo for combo in allCombos if minDifficulty <= sum([enemiesDict[enemy].difficulty for enemy in combo]) <= maxDifficulty]
                spawns = choice(combos)
                spawns = sorted(spawns, key=lambda x: enemiesDict[x].difficulty)

                self.encounterImage.paste(im=allEnemies[spawns[0]]["imageNew"], box=(285, 218), mask=allEnemies[spawns[0]]["imageNew"])
                self.encounterImage.paste(im=allEnemies[spawns[1]]["imageNew"], box=(285, 248), mask=allEnemies[spawns[1]]["imageNew"])
                self.encounterImage.paste(im=allEnemies[spawns[2]]["imageNew"], box=(285, 280), mask=allEnemies[spawns[2]]["imageNew"])

                adapter.debug("\tEnd of trecherous_tower", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def unseen_scurrying(self):
            """
            Swap treasure reward.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of unseen_scurrying", caller=calframe[1][3])
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of unseen_scurrying", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def urns_of_the_fallen(self):
            """
            Swap treasure reward.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of urns_of_the_fallen", caller=calframe[1][3])
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of urns_of_the_fallen", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def velkas_chosen(self):
            """
            Update Crow Demon to different enemy.
            """
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of velkas_chosen", caller=calframe[1][3])
                
                target = sorted([enemy for enemy in self.newTiles[2][0] + self.newTiles[2][1]], key=lambda x: enemiesDict[x].difficulty, reverse=True)[0]
                image = allEnemies[target]["image text"]
                self.create_tooltip(image=image, text=self.tooltipText[target], x=65, y=147)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=297, y=195)
                self.create_tooltip(image=image, text=self.tooltipText[target], x=210, y=219)
                
                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure(self.settings["treasureSwapOption"], self.treasureSwapEncounters[self.selected["name"]], self.rewardTreasure, self.selected["level"], set(self.availableSets), set(self.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.encounterImage)
                if len(newTreasure) >= 15:
                    lastSpaceIdx = newTreasure.rfind(" ")
                    newTreasure1 = newTreasure[:lastSpaceIdx]
                    newTreasure2 = newTreasure[lastSpaceIdx+1:]
                    imageWithText.text((21, 232), newTreasure1, "black", font)
                    imageWithText.text((21, 243), newTreasure2, "black", font)
                else:
                    imageWithText.text((21, 232), newTreasure, "black", font)

                adapter.debug("\tEnd of velkas_chosen", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


    coreSets = {"Dark Souls The Board Game", "Painted World of Ariamis", "Tomb of Giants"}
    encountersWithInvadersOrMimics = {
        "Blazing Furnace",
        "Brume Tower",
        "Courtyard of Lothric",
        "Fortress Gates",
        "Sewers of Lordran"
    }
    
    root = tk.Tk()
    root.title("Dark Souls The Board Game Encounter Shuffler")
    root.tk.call("source", "Azure-ttk-theme-main\\azure.tcl")
    root.tk.call("set_theme", "dark")
    root.iconphoto(True, tk.PhotoImage(file=os.path.join(baseFolder, "icon.png")))

    app = Application(root)
    app.pack(fill="both", expand=True)

    root.update()
    root.maxsize(root.winfo_screenwidth(), root.winfo_screenheight())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()
    adapter.debug("Closing application")
    root.destroy()

except Exception as e:
    error = str(sys.exc_info())
    if "application has been destroyed" not in error:
        raise
