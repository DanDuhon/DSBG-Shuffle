# Change from pickle to JSON
# Add the ability to put bosses in the campaign, and maybe notes as child items?

try:
    import sys
    import logging
    import inspect
    import os
    import pickle
    from os import path
    from json import load, dump
    from random import choice
    from itertools import combinations
    from PIL import Image, ImageTk, ImageFont, ImageDraw
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog

    from enemies import enemyIds, enemiesDict


    def enable_binding(bindKey, method):
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
        font = ImageFont.truetype(baseFolder + "\\Goudy Oldstyle.otf", 11)
        fontSmall = ImageFont.truetype(baseFolder + "\\Goudy Oldstyle.otf", 10)
        fontItalics = ImageFont.truetype(baseFolder + "\\Goudy Old Style Bold Italic.otf", 11)
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
        def __init__(self, widget, text="widget info"):
            self.waittime = 500     #miliseconds
            self.wraplength = 225   #pixels
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
            self.hidetip()

        def schedule(self):
            self.unschedule()
            self.id = self.widget.after(self.waittime, self.showtip)

        def unschedule(self):
            id = self.id
            self.id = None
            if id:
                self.widget.after_cancel(id)

        def showtip(self, event=None):
            x = y = 0
            x, y, cx, cy = self.widget.bbox("insert")
            x += self.widget.winfo_rootx() + 25
            y += self.widget.winfo_rooty() + 20
            # creates a toplevel window
            self.tw = tk.Toplevel(self.widget)
            # Leaves only the label and removes the app window
            self.tw.wm_overrideredirect(True)
            self.tw.wm_geometry("+%d+%d" % (x, y))
            label = ttk.Label(self.tw, text=self.text, font=(font, 12), justify="left", relief="solid", borderwidth=1, wraplength = self.wraplength)
            label.pack(ipadx=1)

        def hidetip(self):
            tw = self.tw
            self.tw= None
            if tw:
                tw.destroy()


    class HelpWindow(object):
        def __init__(self, master):
            try:
                adapter.debug("Creating help window")
                top = self.top = tk.Toplevel(master)
                top.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
                top.wait_visibility()
                top.grab_set_global()

                self.helpTextFrame = ttk.Frame(top, padding=(0, 0, 0, 10))
                self.helpTextFrame.pack()

                helpText = "You can either select an encounter from the list\n"
                helpText += "or click the \"Random Level x\" buttons.\n\n"
                helpText += "Once an encounter card has been loaded, you can use the \"s\"\n"
                helpText += "key to reshuffle the enemies on the encounter.\n"
                helpText += "Clicking on the encounter card will also do this.\n\n"
                helpText += "In the settings menu, you can enable the different core sets/expansions\n"
                helpText += "that add enemies to the game. These are the only sets listed on purpose\n"
                helpText += "as they are the ones that add non-boss enemies.\n\n"
                helpText += "If you try to shuffle the enemies and nothing happens,\n"
                helpText += "there's probably only one combination available!\n"
                helpText += "Many encounters with a single enemy have no alternatives,\n"
                helpText += "even with all enemy expansions activated.\n\n"
                helpText += "Mousing over keywords (in bold and italics) will display the\n"
                helpText += "rules for that keyword.\n\n"
                helpText += "In the Campaign tab, you can build your own campaign by adding\n"
                helpText += "encounters to it. You can also save and load campaigns.\n"
                helpText += "You may only have one of each encounter name, but there are\n"
                helpText += "no restrictions beyond that. Encounters added to a campaign\n"
                helpText += "are frozen so you cannot shuffle the enemies."
                self.helpTextLabel = ttk.Label(self.helpTextFrame, text=helpText)
                self.helpTextLabel.pack(padx=5)

                self.helpButtonsFrame = ttk.Frame(top, padding=(0, 0, 0, 10))
                self.helpButtonsFrame.pack()
                self.helpButtonsFrame.columnconfigure(index=0, weight=1)

                self.okButton = ttk.Button(self.helpButtonsFrame, text="OK", width=14, command=self.top.destroy)
                self.okButton.pack()
            except Exception as e:
                adapter.exception(e)
                raise


    class SettingsWindow(object):
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
                
                # These are the only sets that matter - the ones that add enemies.
                # All encounters are always going to be available.
                self.sets = {
                    "Dark Souls The Board Game": {"frame": None, "button": None, "value": tk.IntVar()},
                    "The Painted World of Ariamis": {"frame": None, "button": None, "value": tk.IntVar()},
                    "The Tomb of Giants": {"frame": None, "button": None, "value": tk.IntVar()},
                    "Darkroot": {"frame": None, "button": None, "value": tk.IntVar()},
                    "Explorers": {"frame": None, "button": None, "value": tk.IntVar()},
                    "Iron Keep": {"frame": None, "button": None, "value": tk.IntVar()},
                    "Phantoms": {"frame": None, "button": None, "value": tk.IntVar()},
                    "Executioner Chariot": {"frame": None, "button": None, "value": tk.IntVar()}
                }
                
                self.checkFrame = ttk.LabelFrame(top, text="Enabled Enemies From Sets", padding=(20, 10))
                self.checkFrame.pack(padx=(20, 10), pady=(20, 10), side=tk.LEFT, anchor=tk.N)
                for i, a in enumerate(self.sets):
                    self.sets[a]["frame"] = ttk.Frame(self.checkFrame)
                    self.sets[a]["frame"].pack(anchor=tk.W)
                    self.sets[a]["value"].set(1 if a in self.settings["availableSets"] else 0)
                    self.sets[a]["button"] = ttk.Checkbutton(self.sets[a]["frame"], text=a + (" (Core Set)" if a in coreSets else ""), variable=self.sets[a]["value"])
                    self.sets[a]["button"].pack(padx=5, pady=10)
                
                self.randomEncounters = {
                    "old": {"frame": None, "button": None, "value": tk.IntVar()},
                    "new": {"frame": None, "button": None, "value": tk.IntVar()}
                }

                self.randomEncounterFrame = ttk.LabelFrame(top, text="Random Encounters Shown", padding=(20, 10))
                self.randomEncounterFrame.pack(padx=(20, 10), pady=(20, 10), side=tk.LEFT, anchor=tk.N)
                self.randomEncounters["old"]["value"].set(1 if "old" in self.settings["randomEncounterTypes"] else 0)
                self.randomEncounters["old"]["frame"] = ttk.Frame(self.randomEncounterFrame)
                self.randomEncounters["old"]["frame"].pack(anchor=tk.W)
                self.randomEncounters["old"]["button"] = ttk.Checkbutton(self.randomEncounters["old"]["frame"], text="\"Old\" Style Encounters", variable=self.randomEncounters["old"]["value"])
                self.randomEncounters["old"]["button"].pack(padx=5, pady=10)
                self.randomEncounters["new"]["value"].set(1 if "new" in self.settings["randomEncounterTypes"] else 0)
                self.randomEncounters["new"]["frame"] = ttk.Frame(self.randomEncounterFrame)
                self.randomEncounters["new"]["frame"].pack(anchor=tk.W)
                self.randomEncounters["new"]["button"] = ttk.Checkbutton(self.randomEncounters["new"]["frame"], text="\"New\" Style Encounters", variable=self.randomEncounters["new"]["value"])
                self.randomEncounters["new"]["button"].pack(padx=5, pady=10)
                self.randomEncounters["new"]["button"].pack(padx=5, pady=10)
                
                self.errLabel = tk.Label(self.top, text="")
                self.errLabel.pack(padx=5)

                self.settingsButtonsFrame = ttk.Frame(top, padding=(0, 0, 0, 10))
                self.settingsButtonsFrame.pack(padx=15, pady=(10, 0))
                
                self.saveButton = ttk.Button(self.settingsButtonsFrame, text="Save", width=14, command=lambda: self.quit_with_save())
                self.cancelButton = ttk.Button(self.settingsButtonsFrame, text="Cancel", width=14, command=self.quit_no_save)
                self.saveButton.pack(padx=5)
                self.cancelButton.pack(padx=5)
            except Exception as e:
                adapter.exception(e)
                raise
            
            
        def quit_with_save(self, event=None):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of quit_with_save", caller=calframe[1][3])

                if all([self.sets[s]["value"].get() == 0 for s in coreSets]):
                    self.errLabel.config(text="You need to select at least one Core Set!")
                    adapter.debug("End of quit_with_save", caller=calframe[1][3])
                    return

                newAvailableSets = set([s for s in self.sets if self.sets[s]["value"].get() == 1])
                randomEncounterTypes = set([s for s in self.randomEncounters if self.randomEncounters[s]["value"].get() == 1])

                newSettings = {
                    "availableSets": list(newAvailableSets),
                    "randomEncounterTypes": list(randomEncounterTypes)
                }

                if newSettings != self.settings:
                    global settingsChanged
                    settingsChanged = True

                    with open(baseFolder + "\\settings.json", "w") as settingsFile:
                        dump(newSettings, settingsFile)

                self.top.destroy()
                adapter.debug("End of quit_with_save", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise
            
            
        def quit_no_save(self, event=None):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of quit_no_save", caller=calframe[1][3])

                self.top.destroy()
                adapter.debug("End of quit_no_save", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


    class Application(ttk.Frame):
        def __init__(self, parent):
            try:
                adapter.debug("Initiating application")
                
                ttk.Frame.__init__(self)
                self.grid_rowconfigure(index=1, weight=1)
                self.grid_rowconfigure(index=2, weight=0)
                self.encounterScrollbar = ttk.Scrollbar(root)
                self.encounterScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    
                with open(baseFolder + "\\settings.json") as settingsFile:
                    self.settings = load(settingsFile)

                self.allSets = set([encounters[encounter]["expansion"] for encounter in encounters])
                self.availableSets = set(self.settings["availableSets"])
                self.availableCoreSets = coreSets & self.availableSets
                oldSets = {"Dark Souls The Board Game", "Darkroot", "Executioner Chariot", "Explorers", "Iron Keep"} if "old" in self.settings["randomEncounterTypes"] else set()
                newSets = (self.allSets - {"Dark Souls The Board Game", "Darkroot", "Executioner Chariot", "Explorers", "Iron Keep"}) if "new" in self.settings["randomEncounterTypes"] else set()
                self.setsForRandomEncounters = (oldSets | newSets) & self.allSets
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

                self.keywordText = {
                    "snowstorm": "At the start of each character's turn, that character suffers Frostbite unless they have the torch token on their dashboard or are on the same node as the torch token or a character with the torch token on their dashboard.",
                    "bitterCold": "If a character has a Frostbite token at the end of their turn, they suffer 1 damage.",
                    "barrage": "At the end of each character's turn, that character must make a defense roll using only their dodge dice.\n\nIf no dodge symbols are rolled, the character suffers 2 damage and Stagger.",
                    "hidden": "After declaring an attack, players must discard a die of their choice before rolling.\n\nIf the attacks only has a single die already, ignore this rule.",
                    "poisonMist": "During setup, place trap tokens on the tile indicated in brackets using the normal trap placement rules.\n\nThen, reveal the tokens, replacing each token with a value with a poison cloud token.",
                    "eerieTooltip": "During setup, take five blank trap tokens and five trap tokens with values on them, and place a random token face down on each of the highlighted nodes.\n\nIf a character moves onto a node with a token, flip the token.\n\nIf the token is blank, place it to one side.\n\nIf the token has a damage value, instead of resolving it normally, spawn an enemy corresponding to the value shown, then discard the token.",
                    "trial": "Trials offer an extra objective providing additional rewards if completed.\n\nThis is shown in parentheses, either in writing, or as a number of turns in which the characters must complete the encounter's main objective.\n\nCompleting trial objectives is not mandatory to complete an encounter.",
                    "onslaught": "Each tile begins the encounter as active (all enemies on active tiles act on their turn).",
                    "darkness": "During this encounter, characters can only attack enemies on the same or an adjacent node.",
                    "timer": "If the timer marker reaches the value shown in brackets, resolve the effect listed.",
                    "respawn": "Place additional models using the enemies and enemy nodes shown on the encounter card.\n\nWhen respawning, if there are insufficient enemy models (because some enemy models are already in play), place as many enemies as possible, then place an enemy token for each missing enemy on the node it would spawn on.\n\nAs soon as the corresponding model becomes available, replace the token with the model."
                }

                self.campaign = []

                self.deathlyFreezeTarget = None

                for enemy in allEnemies:
                    allEnemies[enemy]["image old"] = self.create_image(enemy + ".png", "enemyOld")
                    allEnemies[enemy]["image new"] = self.create_image(enemy + ".png", "enemyNew")

                self.playerCountImage = self.create_image("player_count.png", "playerCount")
                self.enemyNode1 = self.create_image("enemy_node_1.png", "enemyNode")
                self.enemyNode2 = self.create_image("enemy_node_2.png", "enemyNode")
                self.stagger = self.create_image("stagger.png", "condition")
                self.poison = self.create_image("poison.png", "condition")
                self.bleed = self.create_image("bleed.png", "condition")
                self.nodeAttack = self.create_image("node_attack.png", "condition")
                self.attackRange1 = self.create_image("range_1_attack.png", "condition")
                self.repeatAction = self.create_image("repeat_action.png", "condition")
                self.push = self.create_image("push.png", "condition")
                self.eerie = self.create_image("eerie.png", "eerie")

                self.poisonMist = ImageTk.PhotoImage(self.create_image("poison_mist.png", "poisonMist"))
                self.darkness = ImageTk.PhotoImage(self.create_image("darkness.png", "darkness"))
                self.trial = ImageTk.PhotoImage(self.create_image("trial.png", "trial"))
                self.timer = ImageTk.PhotoImage(self.create_image("timer.png", "timer"))
                self.onslaught = ImageTk.PhotoImage(self.create_image("onslaught.png", "onslaught"))
                self.snowstorm = ImageTk.PhotoImage(self.create_image("snowstorm.png", "snowstorm"))
                self.hidden = ImageTk.PhotoImage(self.create_image("hidden.png", "hidden"))
                self.bitterCold = ImageTk.PhotoImage(self.create_image("bitter_cold.png", "bitterCold"))
                self.eerieTooltip = ImageTk.PhotoImage(self.create_image("eerie_tooltip.png", "eerieTooltip"))
                self.barrage = ImageTk.PhotoImage(self.create_image("barrage.png", "barrage"))
                
                self.selected = None
                self.newEnemies = []
                self.newTiles = dict()
            except Exception as e:
                adapter.exception(e)
                raise
                

        def onFrameConfigure(self, canvas):
            """Reset the scroll region to encompass the inner frame"""
            canvas.configure(scrollregion=canvas.bbox("all"))
            

        def _bound_to_mousewheel(self, event):
            self.encounterCanvas.bind_all("<MouseWheel>", self._on_mousewheel)


        def _unbound_to_mousewheel(self, event):
            self.encounterCanvas.unbind_all("<MouseWheel>")


        def _on_mousewheel(self, event):
            self.encounterCanvas.yview_scroll(int(-1*(event.delta/120)), "units")


        def add_encounter_to_campaign(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of add_encounter_to_campaign", caller=calframe[1][3])

                if not self.selected:
                    adapter.debug("End of add_encounter_to_campaign (nothing done)")
                    return
                
                encounter = {
                    "name": self.selected["name"],
                    "level": self.selected["level"],
                    "enemies": self.newEnemies
                }

                if encounter["name"] not in set([e["name"] for e in self.campaign]):
                    self.campaign.append(encounter)

                self.treeviewCampaign.pack_forget()
                self.treeviewCampaign.destroy()
                self.create_campaign_treeview()

                for item in self.campaign:
                    self.treeviewCampaign.insert(parent="", values=(item["name"], item["level"]), index="end")

                adapter.debug("End of add_encounter_to_campaign")
            except Exception as e:
                adapter.exception(e)
                raise


        def delete_encounter_from_campaign(self, event=None):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of delete_encounter_from_campaign", caller=calframe[1][3])
                
                if not self.treeviewCampaign.selection():
                    adapter.debug("End of delete_encounter_from_campaign (nothing done)")
                    return

                self.campaign = [e for e in self.campaign if e["name"] not in set([self.treeviewCampaign.item(e)["values"][0] for e in self.treeviewCampaign.selection()])]

                self.treeviewCampaign.pack_forget()
                self.treeviewCampaign.destroy()
                self.create_campaign_treeview()

                for item in self.campaign:
                    self.treeviewCampaign.insert(parent="", values=(item["name"], item["level"]), index="end")

                self.encounter.config(image="")

                adapter.debug("End of delete_encounter_from_campaign")
            except Exception as e:
                adapter.exception(e)
                raise


        def save_campaign(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of save_campaign", caller=calframe[1][3])

                campaignName = filedialog.asksaveasfile(mode="w", initialdir=baseFolder + "\\saved campaigns", defaultextension=".dsbgc")

                if not campaignName:
                    adapter.debug("End of save_campaign (nothing done)")
                    return

                with open(campaignName.name, "wb") as campaignFile:
                    pickle.dump(self.campaign, campaignFile)

                adapter.debug("End of save_campaign (saved to " + str(campaignFile) + ")")
            except Exception as e:
                adapter.exception(e)
                raise


        def load_campaign(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of load_campaign", caller=calframe[1][3])

                campaignFile = filedialog.askopenfilename(initialdir=baseFolder + "\\saved campaigns", filetypes = [("Dark Souls Board Game Campaign files", ".dsbgc")])
                if not campaignFile:
                    adapter.debug("End of load_campaign (file dialog canceled)")
                    return
                
                if os.path.splitext(campaignFile)[1] != ".dsbgc":
                    adapter.debug("End of load_campaign (invalid file)")
                    return

                with open(campaignFile, "rb") as p:
                    self.campaign = pickle.load(p)

                self.treeviewCampaign.pack_forget()
                self.treeviewCampaign.destroy()
                self.create_campaign_treeview()

                for item in self.campaign:
                    self.treeviewCampaign.insert(parent="", values=(item["name"], item["level"]), index="end")

                adapter.debug("End of load_campaign (loaded from " + str(campaignFile) + ")")
            except Exception as e:
                adapter.exception(e)
                raise


        def move_up(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of move_up", caller=calframe[1][3])

                leaves = self.treeviewCampaign.selection()
                for i in leaves:
                    self.treeviewCampaign.move(i, self.treeviewCampaign.parent(i), self.treeviewCampaign.index(i)-1)

                adapter.debug("End of move_up")
            except Exception as e:
                adapter.exception(e)
                raise


        def move_down(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of move_down", caller=calframe[1][3])

                leaves = self.treeviewCampaign.selection()
                for i in reversed(leaves):
                    self.treeviewCampaign.move(i, self.treeviewCampaign.parent(i), self.treeviewCampaign.index(i)+1)

                adapter.debug("End of move_down")
            except Exception as e:
                adapter.exception(e)
                raise


        def load_campaign_encounter(self, event=None):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of load_campaign_encounter", caller=calframe[1][3])

                self.selected = None
                self.encounter.unbind("<Button 1>")

                tree = event.widget
                if len(tree.selection()) != 1:
                    adapter.debug("End of load_campaign_encounter (not updating image)")
                    return
                
                campaignEncounter = [e for e in self.campaign if e["name"] == tree.item(tree.selection())["values"][0]]
                if campaignEncounter:
                    self.encounterImage = campaignEncounter[0]["image"]
                    self.encounterPhotoImage = ImageTk.PhotoImage(self.encounterImage)
                    self.encounter.image = self.encounterPhotoImage
                    self.encounter.config(image=self.encounterPhotoImage)

                self.apply_tooltips()

                adapter.debug("End of load_campaign_encounter")
            except Exception as e:
                adapter.exception(e)
                raise


        def set_encounter_list(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of set_encounter_list", caller=calframe[1][3])

                self.encounterList = [encounter for encounter in encounters if (
                    (
                        (self.availableSets & {"Explorers", "Phantoms"}
                            or encounter not in encountersWithInvadersOrMimics)
                        and any([frozenset(expCombo).issubset(self.availableSets) for expCombo in encounters[encounter]["setCombos"]])
                        and any([frozenset(expCombo).issubset(self.availableSets) for expCombo in encounters[encounter]["setCombos"]])
                        and any([frozenset(expCombo).issubset(self.availableSets) for expCombo in encounters[encounter]["setCombos"]])
                    )
                    and (encounter != "Abandoned and Forgotten" or "The Painted World of Ariamis" in self.availableSets)
                    and (encounter != "Trecherous Tower" or "The Painted World of Ariamis" in self.availableSets)
                    )]

                adapter.debug("End of set_encounter_list")
            except Exception as e:
                adapter.exception(e)
                raise


        def create_tabs(self, event=None):
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

                adapter.debug("End of create_tabs")
            except Exception as e:
                adapter.exception(e)
                raise


        def create_encounters_treeview(self):
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

                encountersSorted = [encounter for encounter in sorted(self.encounterList, key=lambda x: (
                    1 if encounters[x]["level"] == 4 else 0,
                    0 if encounters[x]["expansion"] in coreSets else 1,
                    0 if encounters[x]["expansion"] != "Executioner Chariot" else 1,
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
                self.encounterFrame.bind("<Configure>", lambda event, canvas=self.encounterCanvas: self.onFrameConfigure(canvas))

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
                    self.encounter.config(image="")
                    self.treeviewEncounters.pack_forget()
                    self.treeviewEncounters.destroy()
                    self.availableSets = set(self.settings["availableSets"])
                    self.availableCoreSets = coreSets & self.availableSets
                    oldSets = {"Dark Souls The Board Game", "Darkroot", "Executioner Chariot", "Explorers", "Iron Keep"} if "old" in self.settings["randomEncounterTypes"] else set()
                    newSets = (self.allSets - {"Dark Souls The Board Game", "Darkroot", "Executioner Chariot", "Explorers", "Iron Keep"}) if "new" in self.settings["randomEncounterTypes"] else set()
                    self.setsForRandomEncounters = (oldSets | newSets) & self.allSets
                    self.set_encounter_list()
                    self.create_encounters_treeview()
                
                self.set_bindings_buttons_menus(True)

                adapter.debug("End of settings_window", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def help_window(self):
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


        def create_image(self, imageFileName, imageType):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of create_image", caller=calframe[1][3])

                imagePath = baseFolder + "\\images\\" + imageFileName
                adapter.debug("\tOpening " + imagePath, caller=calframe[1][3])

                if imageType == "encounter":
                    if self.selected["level"] < 4 and self.selected["expansion"] in {"Dark Souls The Board Game", "Iron Keep", "Darkroot", "Explorers", "Executioner Chariot"}:
                        width = 200
                        height = 300
                    elif self.selected["level"] == 4:
                        width = 305
                        height = 424
                    else:
                        width = 400
                        height = 685

                    self.encounterImage = Image.open(imagePath).resize((width, height), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.encounterImage)
                elif imageType == "enemyOld":
                    image = Image.open(imagePath).resize((36, 36), Image.Resampling.LANCZOS)
                elif imageType == "enemyNew":
                    image = Image.open(imagePath).resize((25, 25), Image.Resampling.LANCZOS)
                elif imageType == "resurrection":
                    image = Image.open(imagePath).resize((9, 17), Image.Resampling.LANCZOS)
                elif imageType == "playerCount":
                    image = Image.open(imagePath).resize((12, 12), Image.Resampling.LANCZOS)
                elif imageType == "enemyNode":
                    image = Image.open(imagePath).resize((12, 12), Image.Resampling.LANCZOS)
                elif imageType == "condition":
                    image = Image.open(imagePath).resize((13, 13), Image.Resampling.LANCZOS)
                elif imageType == "eerie":
                    image = Image.open(imagePath).resize((94, 100), Image.Resampling.LANCZOS)
                elif imageType == "poisonMist":
                    image = Image.open(imagePath).resize((60, 15), Image.Resampling.LANCZOS)
                elif imageType == "darkness":
                    image = Image.open(imagePath).resize((45, 11), Image.Resampling.LANCZOS)
                elif imageType == "trial":
                    image = Image.open(imagePath).resize((28, 11), Image.Resampling.LANCZOS)
                elif imageType == "timer":
                    image = Image.open(imagePath).resize((30, 11), Image.Resampling.LANCZOS)
                elif imageType == "onslaught":
                    image = Image.open(imagePath).resize((48, 14), Image.Resampling.LANCZOS)
                elif imageType == "snowstorm":
                    image = Image.open(imagePath).resize((54, 11), Image.Resampling.LANCZOS)
                elif imageType == "hidden":
                    image = Image.open(imagePath).resize((37, 12), Image.Resampling.LANCZOS)
                elif imageType == "bitterCold":
                    image = Image.open(imagePath).resize((50, 11), Image.Resampling.LANCZOS)
                elif imageType == "eerieTooltip":
                    image = Image.open(imagePath).resize((29, 11), Image.Resampling.LANCZOS)
                elif imageType == "barrage":
                    image = Image.open(imagePath).resize((40, 14), Image.Resampling.LANCZOS)

                adapter.debug("\tEnd of create_image", caller=calframe[1][3])
                
                return image
            except Exception as e:
                adapter.exception(e)
                raise


        def random_encounter(self, event=None, level=None):
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
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of load_encounter", caller=calframe[1][3])
                
                self.treeviewEncounters.unbind("<<TreeviewSelect>>")

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

                if encounters[encounterName] == self.selected:
                    self.shuffle_enemies()
                    self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)
                    adapter.debug("\tEnd of load_encounter", caller=calframe[1][3])
                    return
                
                self.selected = encounters[encounterName]
                self.selected["difficultyMod"] = {}
                self.selected["restrictRanged"] = {}

                adapter.debug("\tOpening " + baseFolder + "\\encounters\\" + encounterName + ".json", caller=calframe[1][3])
                with open(baseFolder + "\\encounters\\" + encounterName + ".json") as alternativesFile:
                    alts = load(alternativesFile)

                self.selected["alternatives"] = []
                self.selected["enemySlots"] = alts["enemySlots"]

                for expansionCombo in alts["alternatives"]:
                    if set(expansionCombo.split(",")).issubset(self.availableSets):
                        self.selected["alternatives"] += alts["alternatives"][expansionCombo]

                self.lakeviewRefugeBigEnemiesAvailable = sum([1 for enemy in enemiesDict if (
                    enemiesDict[enemy].health >= 5
                    and enemiesDict[enemy].expansion in self.availableSets)])

                self.newTiles = dict()

                self.shuffle_enemies()
                self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)
                self.encounter.bind("<Button 1>", self.shuffle_enemies)

                adapter.debug("\tEnd of load_encounter", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise

        def shuffle_enemies(self, event=None):
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

                self.encounterPhotoImage = self.create_image(self.selected["name"] + ".jpg", "encounter")

                oldEnemies = [e for e in self.newEnemies]
                self.newEnemies = choice(self.selected["alternatives"])
                if len(self.selected["alternatives"]) > 1:
                    while self.newEnemies == oldEnemies:
                        self.newEnemies = choice(self.selected["alternatives"])

                self.newTiles = {
                    1: [[], [], [], []],
                    2: [[], []],
                    3: [[], []]
                }
                
                adapter.debug("New enemies: " + str(self.newEnemies), caller=calframe[1][3])
                        
                s = 0
                for slotNum, slot in enumerate(self.selected["enemySlots"]):
                    for e in range(slot):
                        self.newTiles[1 if slotNum < 4 else 2 if slotNum < 6 else 3][slotNum - (0 if slotNum < 4 else 4 if slotNum < 6 else 6)].append(enemyIds[self.newEnemies[s]].name)
                        if self.selected["level"] == 4:
                            x = (115 if e == 0 else 157 if e == 1 else 200)
                            y = 79 + (47 * slotNum)
                            imageType = "image old"
                        elif self.selected["expansion"] in {"Dark Souls The Board Game", "Iron Keep", "Darkroot", "Explorers", "Executioner Chariot"}:
                            x = (59 if e == 0 else 105 if e == 1 else 150)
                            y = 57 + (50 * slotNum)
                            imageType = "image old"
                        else:
                            x = (299 if e == 0 else 327 if e == 1 else 355)
                            y = 318 + (28 * (slotNum - (0 if slotNum < 4 else 4 if slotNum < 6 else 6))) + (((1 if slotNum < 4 else 2 if slotNum < 6 else 3) - 1) * 119)
                            imageType = "image new"

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

                # These are new encounters that have text referencing specific enemies.
                if self.selected["name"] == "Abandoned and Forgotten":
                    self.abandoned_and_forgotten()
                elif self.selected["name"] == "Cloak and Feathers":
                    self.cloak_and_feathers()
                elif self.selected["name"] == "Cold Snap":
                    self.cold_snap()
                elif self.selected["name"] == "Corvian Host":
                    self.corvian_host()
                elif self.selected["name"] == "Corrupted Hovel":
                    self.corrupted_hovel()
                elif self.selected["name"] == "Deathly Freeze":
                    self.deathly_freeze()
                elif self.selected["name"] == "Deathly Magic":
                    self.deathly_magic()
                elif self.selected["name"] == "Distant Tower":
                    self.distant_tower()
                elif self.selected["name"] == "Eye of the Storm":
                    self.eye_of_the_storm()
                elif self.selected["name"] == "Frozen Revolutions":
                    self.frozen_revolutions()
                elif self.selected["name"] == "Giant's Coffin":
                    self.giants_coffin()
                elif self.selected["name"] == "Gnashing Beaks":
                    self.gnashing_beaks()
                elif self.selected["name"] == "In Deep Water":
                    self.in_deep_water()
                elif self.selected["name"] == "Lakeview Refuge":
                    self.lakeview_refuge()
                elif self.selected["name"] == "Last Rites":
                    self.last_rites()
                elif self.selected["name"] == "Monstrous Maw":
                    self.monstrous_maw()
                elif self.selected["name"] == "No Safe Haven":
                    self.no_safe_haven()
                elif self.selected["name"] == "Pitch Black":
                    self.pitch_black()
                elif self.selected["name"] == "Puppet Master":
                    self.puppet_master()
                elif self.selected["name"] == "Skeletal Spokes":
                    self.skeletal_spokes()
                elif self.selected["name"] == "Skeleton Overlord":
                    self.skeleton_overlord()
                elif self.selected["name"] == "The Abandoned Chest":
                    self.the_abandoned_chest()
                elif self.selected["name"] == "The Beast From the Depths":
                    self.the_beast_from_the_depths()
                elif self.selected["name"] == "The First Bastion":
                    self.the_first_bastion()
                elif self.selected["name"] == "The Last Bastion":
                    self.the_last_bastion()
                elif self.selected["name"] == "The Locked Grave":
                    self.the_locked_grave()
                elif self.selected["name"] == "The Skeleton Ball":
                    self.the_skeleton_ball()
                elif self.selected["name"] == "Trecherous Tower":
                    self.trecherous_tower()
                elif self.selected["name"] == "Velka's Chosen":
                    self.velkas_chosen()
                
                self.encounterPhotoImage = ImageTk.PhotoImage(self.encounterImage)
                self.encounter.image = self.encounterPhotoImage
                self.encounter.config(image=self.encounterPhotoImage)
                self.encounter.bind("<Button 1>", self.shuffle_enemies)

                self.apply_tooltips()

                adapter.debug("\tEnd of shuffle_enemies", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def apply_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of apply_tooltips", caller=calframe[1][3])

                if hasattr(self, "keyword0") and self.keyword0.winfo_exists():
                    self.keyword0.destroy()
                if hasattr(self, "keyword1") and self.keyword1.winfo_exists():
                    self.keyword1.destroy()
                if hasattr(self, "keyword2") and self.keyword2.winfo_exists():
                    self.keyword2.destroy()
                if hasattr(self, "keyword3") and self.keyword3.winfo_exists():
                    self.keyword3.destroy()

                if self.selected:
                    encounter = self.selected["name"]
                elif self.treeviewCampaign.focus():
                    encounter = self.treeviewCampaign.item(self.treeviewCampaign.focus())["values"][0]
                else:
                    adapter.debug("\tEnd of apply_tooltips (removed tooltips only)", caller=calframe[1][3])
                    return

                if encounter == "A Trusty Ally":
                    self.a_trusty_ally_tooltips()
                elif encounter == "Abandoned and Forgotten":
                    self.abandoned_and_forgotten_tooltips()
                elif encounter == "Altar of Bones":
                    self.altar_of_bones_tooltips()
                elif encounter == "Central Plaza":
                    self.central_plaza_tooltips()
                elif encounter == "Cold Snap":
                    self.cold_snap_tooltips()
                elif encounter == "Corrupted Hovel":
                    self.corrupted_hovel_tooltips()
                elif encounter == "Corvian Host":
                    self.corvian_host_tooltips()
                elif encounter == "Dark Resurrection":
                    self.dark_resurrection_tooltips()
                elif encounter == "Deathly Freeze":
                    self.deathly_freeze_tooltips()
                elif encounter == "Distant Tower":
                    self.distant_tower_tooltips()
                elif encounter == "Eye of the Storm":
                    self.eye_of_the_storm_tooltips()
                elif encounter == "Far From the Sun":
                    self.far_from_the_sun_tooltips()
                elif encounter == "Frozen Sentries":
                    self.frozen_sentries_tooltips()
                elif encounter == "Frozen Revolutions":
                    self.frozen_revolutions_tooltips()
                elif encounter == "Gnashing Beaks":
                    self.gnashing_beaks_tooltips()
                elif encounter == "Giant's Coffin":
                    self.giants_coffin_tooltips()
                elif encounter == "In Deep Water":
                    self.in_deep_water_tooltips()
                elif encounter == "Inhospitable Ground":
                    self.inhospitable_ground_tooltips()
                elif encounter == "Lakeview Refuge":
                    self.lakeview_refuge_tooltips()
                elif encounter == "Last Rites":
                    self.last_rites_tooltips()
                elif encounter == "Last Shred of Light":
                    self.last_shred_of_light_tooltips()
                elif encounter == "No Safe Haven":
                    self.no_safe_haven_tooltips()
                elif encounter == "Painted Passage":
                    self.painted_passage_tooltips()
                elif encounter == "Pitch Black":
                    self.pitch_black_tooltips()
                elif encounter == "Promised Respite":
                    self.promised_respite_tooltips()
                elif encounter == "Skeleton Overlord":
                    self.skeleton_overlord_tooltips()
                elif encounter == "Snowblind":
                    self.snowblind_tooltips()
                elif encounter == "The Beast From the Depths":
                    self.the_beast_from_the_depths_tooltips()
                elif encounter == "The First Bastion":
                    self.the_first_bastion_tooltips()
                elif encounter == "The Last Bastion":
                    self.the_last_bastion_tooltips()
                elif encounter == "The Locked Grave":
                    self.the_locked_grave_tooltips()
                elif encounter == "The Mass Grave":
                    self.the_mass_grave_tooltips()
                elif encounter == "Trecherous Tower":
                    self.trecherous_tower_tooltips()
                elif encounter == "Unseen Scurrying":
                    self.unseen_scurrying_tooltips()

                adapter.debug("\tEnd of apply_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def a_trusty_ally_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of giants_coffin_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.onslaught, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=148, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["onslaught"])

                adapter.debug("\tEnd of giants_coffin_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def abandoned_and_forgotten(self):
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

                self.encounterImage.paste(im=self.eerie, box=(140, 205), mask=self.eerie)
                self.encounterImage.paste(im=allEnemies[spawns[0]]["image new"], box=(175, 209), mask=allEnemies[spawns[0]]["image new"])
                self.encounterImage.paste(im=allEnemies[spawns[1]]["image new"], box=(175, 242), mask=allEnemies[spawns[1]]["image new"])
                self.encounterImage.paste(im=allEnemies[spawns[2]]["image new"], box=(175, 275), mask=allEnemies[spawns[2]]["image new"])

                adapter.debug("\tEnd of abandoned_and_forgotten", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def abandoned_and_forgotten_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of abandoned_and_forgotten_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.eerieTooltip, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["eerieTooltip"])

                adapter.debug("\tEnd of abandoned_and_forgotten_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def altar_of_bones_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of altar_of_bones_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.timer, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=149, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["timer"])

                adapter.debug("\tEnd of altar_of_bones_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def central_plaza_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of central_plaza_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.barrage, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146, y=198)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["barrage"])

                adapter.debug("\tEnd of central_plaza_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def cloak_and_feathers(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of cloak_and_feathers", caller=calframe[1][3])

                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((30, 150), "Kill the " + self.newTiles[1][0][0] + (" (and resulting Hollows)" if self.newTiles[1][0][0] == "Phalanx" else ""), "black", font)

                adapter.debug("\tEnd of cloak_and_feathers", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def cold_snap(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of cold_snap", caller=calframe[1][3])

                coldSnapTarget = self.newTiles[2][0][1]

                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((145, 230), "Trial  (Kill the " + coldSnapTarget + (" and resulting Hollows)" if coldSnapTarget == "Phalanx" else ")"), "black", fontItalics)
                if enemiesDict[coldSnapTarget].health == 1 and (enemiesDict[coldSnapTarget].armor < 2 or enemiesDict[coldSnapTarget].resist < 2):
                    text = "Increase the " + coldSnapTarget
                    text += "'s\n"
                    if enemiesDict[coldSnapTarget].armor < 2 and enemiesDict[coldSnapTarget].resist < 2:
                        text += "block and resistance values to 2."
                    elif enemiesDict[coldSnapTarget].armor < 2:
                        text += "block value to 2."
                    elif enemiesDict[coldSnapTarget].resist < 2:
                        text += "resistance value to 2."
                    imageWithText.text((145, 245), text, "black", font)

                adapter.debug("\tEnd of cold_snap", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def cold_snap_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of cold_snap_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.snowstorm, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=147, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["snowstorm"])

                self.keyword1 = tk.Label(self.encounterFrame, image=self.bitterCold, borderwidth=0, highlightthickness=0)
                self.keyword1.place(x=146, y=215)
                tooltip1 =  CreateToolTip(self.keyword1, self.keywordText["bitterCold"])

                self.keyword2 = tk.Label(self.encounterFrame, image=self.trial, borderwidth=0, highlightthickness=0)
                self.keyword2.place(x=146, y=233)
                tooltip2 =  CreateToolTip(self.keyword2, self.keywordText["trial"])

                adapter.debug("\tEnd of cold_snap_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def corrupted_hovel_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of corrupted_hovel_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.poisonMist, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=145, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["poisonMist"])

                self.keyword1 = tk.Label(self.encounterFrame, image=self.trial, borderwidth=0, highlightthickness=0)
                self.keyword1.place(x=146, y=214.5)
                tooltip1 =  CreateToolTip(self.keyword1, self.keywordText["trial"])

                adapter.debug("\tEnd of corrupted_hovel_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def corvian_host(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of corvian_host", caller=calframe[1][3])
                
                corvianHostTile1 = [enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1] if enemiesDict[enemy].health >= 5]
                corvianHostTile2 = [enemy for enemy in self.newTiles[2][0] + self.newTiles[2][1] if enemiesDict[enemy].health >= 5]
                overlap = set(corvianHostTile1) & set(corvianHostTile2)
                corvianHostTarget = choice([enemy for enemy in overlap if corvianHostTile1.count(enemy) + corvianHostTile2.count(enemy) == 2])

                imageWithText = ImageDraw.Draw(self.encounterImage)
                text = "When a tile is made active, reset the timer.\n"
                text += "Characters can only leave a tile if there are no\n" + corvianHostTarget + "s on it. When all\n" + corvianHostTarget
                text += "s have been killed on tiles one\nand two, spawn a" + ("n " if corvianHostTarget[0].lower() in {"a", "e", "i", "o", "u"} else " ")
                text += corvianHostTarget + " on both\nenemy spawn nodes on tile three.\n"
                if enemiesDict[corvianHostTarget].armor + enemiesDict[corvianHostTarget].resist <= 3:
                    text += "Increase " + corvianHostTarget + "s' "
                    text += ("block, resistance, and\ndamage values by 1" if corvianHostTarget in {"Skeleton Soldier", "Falchion Skeleton"} else "block and resistance\nvalues by 1 and their attacks gain     .")
                    self.encounterImage.paste(im=self.bleed, box=(280, 294), mask=self.bleed)
                else:
                    text += corvianHostTarget + "\nattacks gain     ."
                    self.encounterImage.paste(im=self.bleed, box=(194, 294), mask=self.bleed)
                imageWithText.text((145, 207), text, "black", fontSmall)

                adapter.debug("\tEnd of corvian_host", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def corvian_host_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of corvian_host_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.poisonMist, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=142, y=194.5)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["poisonMist"])

                adapter.debug("\tEnd of corvian_host_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def corrupted_hovel(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of corrupted_hovel", caller=calframe[1][3])

                self.encounterImage.paste(im=self.poison, box=(166, 247), mask=self.poison)
                self.encounterImage.paste(im=self.nodeAttack, box=(200, 247), mask=self.nodeAttack)
                imageWithText = ImageDraw.Draw(self.encounterImage)
                target = [enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1] if (self.newTiles[1][0] + self.newTiles[1][1]).count(enemy) == 2][0]
                imageWithText.text((145, 235), target + " attacks\ngain      and     .", "black", font)

                adapter.debug("\tEnd of corrupted_hovel", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def dark_resurrection_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of dark_resurrection_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.darkness, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=147, y=197.5)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["darkness"])

                adapter.debug("\tEnd of dark_resurrection_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def deathly_freeze(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of deathly_freeze", caller=calframe[1][3])
                    
                deathlyFreezeTile1 = [enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1]]
                deathlyFreezeTile2 = [enemy for enemy in self.newTiles[2][0] + self.newTiles[2][1]]
                overlap = set(deathlyFreezeTile1) & set(deathlyFreezeTile2)
                deathlyFreezeTarget = sorted([enemy for enemy in overlap if deathlyFreezeTile1.count(enemy) + deathlyFreezeTile2.count(enemy) > 1], key=lambda x: enemiesDict[x].difficulty, reverse=True)[0]

                self.encounterImage.paste(im=self.nodeAttack, box=(166, 248), mask=self.nodeAttack)
                self.encounterImage.paste(im=self.attackRange1, box=(202, 248), mask=self.attackRange1)
                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((145, 235), deathlyFreezeTarget + " attacks\ngain      and      .", "black", font)

                adapter.debug("\tEnd of deathly_freeze", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def deathly_freeze_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of deathly_freeze_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.snowstorm, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=145, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["snowstorm"])

                self.keyword1 = tk.Label(self.encounterFrame, image=self.bitterCold, borderwidth=0, highlightthickness=0)
                self.keyword1.place(x=144.5, y=214.5)
                tooltip1 =  CreateToolTip(self.keyword1, self.keywordText["bitterCold"])

                adapter.debug("\tEnd of deathly_freeze_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def deathly_magic(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of deathly_magic", caller=calframe[1][3])

                deathlyMagicTarget = choice([enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1] if (self.newTiles[1][0] + self.newTiles[1][1]).count(enemy) == 1])
                
                self.encounterImage.paste(im=self.playerCountImage, box=(244, 210), mask=self.playerCountImage)

                imageWithText = ImageDraw.Draw(self.encounterImage)

                text = "The " + deathlyMagicTarget + "'s\nstarting health is 5 +      ."
                
                imageWithText.text((145, 198), text, "black", font)
                imageWithText.text((30, 150), "Kill the " + deathlyMagicTarget + (" (and resulting Hollows)" if deathlyMagicTarget == "Phalanx" else ""), "black", font)

                adapter.debug("\tEnd of deathly_magic", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def distant_tower(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of distant_tower", caller=calframe[1][3])

                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((145, 214), "Trial  (Kill the " + self.newTiles[3][0][0] + (" and resulting Hollows)" if self.newTiles[3][0][0] == "Phalanx" else ")"), "black", fontItalics)

                adapter.debug("\tEnd of distant_tower", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def distant_tower_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of distant_tower_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.barrage, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146, y=198)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["barrage"])

                self.keyword1 = tk.Label(self.encounterFrame, image=self.trial, borderwidth=0, highlightthickness=0)
                self.keyword1.place(x=146, y=217)
                tooltip1 =  CreateToolTip(self.keyword1, self.keywordText["trial"])

                adapter.debug("\tEnd of distant_tower_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def eye_of_the_storm(self):
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

                self.encounterImage.paste(im=self.enemyNode2, box=(160, 295), mask=self.enemyNode2)
                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((30, 150), "Kill the " + spawn + (" (and resulting Hollows)" if spawn == "Phalanx" else ""), "black", font)
                fourTarget = [enemyIds[enemy].name for enemy in self.newEnemies if self.newEnemies.count(enemy) == 4]
                targets = list(set([enemyIds[enemy].name for enemy in self.newEnemies if self.newEnemies.count(enemy) == 2]))
                text = "Increase " + (fourTarget[0] if fourTarget else targets[0]) + "s'" + (" and " + targets[1] + "s'" if not fourTarget else "")
                text += "\nblock and resistance values by 1. Once these\nenemies have been killed, spawn the\n" + spawn + "\non     , on tile three."
                imageWithText.text((145, 240), text, "black", font)

                adapter.debug("\tEnd of eye_of_the_storm", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def eye_of_the_storm_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of eye_of_the_storm_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.hidden, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146.5, y=198)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["hidden"])

                adapter.debug("\tEnd of eye_of_the_storm_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def far_from_the_sun_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of far_from_the_sun_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.darkness, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=147, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["darkness"])

                adapter.debug("\tEnd of far_from_the_sun_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def frozen_revolutions(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of frozen_revolutions", caller=calframe[1][3])

                self.encounterImage.paste(im=self.repeatAction, box=(181, 237), mask=self.repeatAction)
                self.encounterImage.paste(im=self.stagger, box=(338, 280), mask=self.stagger)
                imageWithText = ImageDraw.Draw(self.encounterImage)
                text = self.newTiles[3][0][0] + " behaviors\ngain +1     .\n"
                text += self.newTiles[3][0][0] + "s ignore barrels during\nmovement. If a" + ("n " if self.newTiles[3][0][0][0].lower() in {"a", "e", "i", "o", "u"} else " ") + self.newTiles[3][0][0]
                text += " is pushed\nonto a node containing a barrel, it suffers     ,\nthen discard the barrel."
                imageWithText.text((145, 225), text, "black", font)

                adapter.debug("\tEnd of frozen_revolutions", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def frozen_revolutions_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of frozen_revolutions_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.trial, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=145, y=196.5)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["trial"])

                adapter.debug("\tEnd of frozen_revolutions_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def frozen_sentries_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of frozen_sentries_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.snowstorm, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=148, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["snowstorm"])

                adapter.debug("\tEnd of frozen_sentries_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def giants_coffin(self):
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

                self.encounterImage.paste(im=self.enemyNode1, box=(159, 258), mask=self.enemyNode1)
                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((145, 198), "Onslaught\nTrial  (7)\nTimer (2)", "black", fontItalics)
                imageWithText.text((191, 230), "Spawn a" + ("n " if spawn1[0].lower() in {"a", "e", "i", "o", "u"} else " ") + spawn1 + " and a" + ("n " if spawn2[0].lower() in {"a", "e", "i", "o", "u"} else " "), "black", font)
                text = spawn2 + " on tile two,\non     .\nIf there are enemies on their tile, characters must\nspend 1 stamina if they move during their turn."
                imageWithText.text((145, 245), text, "black", font)

                adapter.debug("\tEnd of giants_coffin", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def giants_coffin_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of giants_coffin_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.onslaught, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146.5, y=201)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["onslaught"])

                self.keyword1 = tk.Label(self.encounterFrame, image=self.trial, borderwidth=0, highlightthickness=0)
                self.keyword1.place(x=145, y=217)
                tooltip1 =  CreateToolTip(self.keyword1, self.keywordText["trial"])

                self.keyword2 = tk.Label(self.encounterFrame, image=self.timer, borderwidth=0, highlightthickness=0)
                self.keyword2.place(x=146, y=231)
                tooltip2 =  CreateToolTip(self.keyword2, self.keywordText["timer"])

                adapter.debug("\tEnd of giants_coffin_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def gnashing_beaks(self):
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

                imageWithText = ImageDraw.Draw(self.encounterImage)
                self.encounterImage.paste(im=self.enemyNode1, box=(160, 242), mask=self.enemyNode1)
                self.encounterImage.paste(im=self.enemyNode2, box=(160, 270), mask=self.enemyNode2)
                text = "When the chest is opened, spawn two\n" + spawn1 + "s\non      on tile one,\nand a"
                text += ("n " if spawn2[0].lower() in {"a", "e", "i", "o", "u"} else " ") + spawn2
                text += "\non      on tile one."
                imageWithText.text((145, 215), text, "black", font)

                adapter.debug("\tEnd of gnashing_beaks", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def gnashing_beaks_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of gnashing_beaks_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.trial, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146, y=196)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["trial"])

                adapter.debug("\tEnd of gnashing_beaks_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def in_deep_water(self):
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

                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((194, 195), "Spawn a" + ("n " if spawn[0].lower() in {"a", "e", "i", "o", "u"} else " ") + spawn, "black", font)
                imageWithText.text((146, 206), "on each enemy node.", "black", font)

                adapter.debug("\tEnd of in_deep_water", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def in_deep_water_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of in_deep_water_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.timer, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=148, y=196)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["timer"])

                adapter.debug("\tEnd of in_deep_water_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def inhospitable_ground_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of inhospitable_ground_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.snowstorm, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=148, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["snowstorm"])

                adapter.debug("\tEnd of inhospitable_ground_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def lakeview_refuge(self):
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

                self.encounterImage.paste(im=self.playerCountImage, box=(198, 270), mask=self.playerCountImage)
                self.encounterImage.paste(im=self.enemyNode1, box=(160, 270), mask=self.enemyNode1)
                self.encounterImage.paste(im=self.enemyNode2, box=(215, 285), mask=self.enemyNode2)
                
                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((145, 198), "Onslaught, Darkness\nTrial  (Kill the " + spawn1 + (" and resulting Hollows)" if spawn1 == "Phalanx" else ")"), "black", fontItalics)
                text = "The first time a character is placed on the same\nnode as the torch token, spawn a" + ("n " if spawn1[0].lower() in {"a", "e", "i", "o", "u"} else " ")
                text += "\n" + spawn1 + " on the torch's tile\non     , and      " + spawn2 + "s\non tile two, on     ."
                imageWithText.text((145, 230), text, "black", font)

                adapter.debug("\tEnd of lakeview_refuge", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def lakeview_refuge_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of lakeview_refuge_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.onslaught, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146.5, y=201)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["onslaught"])

                self.keyword1 = tk.Label(self.encounterFrame, image=self.darkness, borderwidth=0, highlightthickness=0)
                self.keyword1.place(x=199, y=201)
                tooltip1 =  CreateToolTip(self.keyword1, self.keywordText["darkness"])

                self.keyword2 = tk.Label(self.encounterFrame, image=self.trial, borderwidth=0, highlightthickness=0)
                self.keyword2.place(x=146, y=216)
                tooltip2 =  CreateToolTip(self.keyword2, self.keywordText["trial"])

                adapter.debug("\tEnd of lakeview_refuge_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def last_rites(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of last_rites", caller=calframe[1][3])

                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((145, 270), "All enemy attacks gain +1 damage.", "black", font)

                adapter.debug("\tEnd of last_rites", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def last_rites_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of last_rites", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.timer, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=149, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["timer"])

                adapter.debug("\tEnd of last_rites", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def last_shred_of_light_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of last_shred_of_light_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.darkness, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=147, y=197.5)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["darkness"])

                adapter.debug("\tEnd of last_shred_of_light_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def monstrous_maw(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of monstrous_maw", caller=calframe[1][3])

                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((30, 150), "Kill the " + self.newTiles[1][1][0] + (" (and resulting Hollows)" if self.newTiles[1][1][0] == "Phalanx" else ""), "black", font)
                text = "Increase the " + self.newTiles[1][1][0] + "'s\nstarting health to 10, "
                text += "and increase its block,\nresistance, and dodge difficulty values by 1."
                imageWithText.text((145, 197), text, "black", font)

                adapter.debug("\tEnd of monstrous_maw", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def no_safe_haven(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of no_safe_haven", caller=calframe[1][3])

                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((30, 150), "Kill the " + self.newTiles[2][0][0] + (" (and resulting Hollows)" if self.newTiles[2][0][0] == "Phalanx" else "") + " starting on tile two", "black", font)

                adapter.debug("\tEnd of no_safe_haven", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def no_safe_haven_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of no_safe_haven_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.poisonMist, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=144, y=195)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["poisonMist"])

                adapter.debug("\tEnd of no_safe_haven_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def painted_passage_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of painted_passage_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.snowstorm, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=148, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["snowstorm"])

                adapter.debug("\tEnd of painted_passage_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def pitch_black(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of pitch_black", caller=calframe[1][3])

                tile1Enemies = self.newTiles[1][0] + self.newTiles[1][1]
                tile2Enemies = self.newTiles[2][0] + self.newTiles[2][1]
                target1 = self.newTiles[1][0][0] if tile1Enemies.count(self.newTiles[1][0][0]) == 1 else self.newTiles[1][0][1] if tile1Enemies.count(self.newTiles[1][0][1]) == 1 else self.newTiles[1][1][0]
                target2 = self.newTiles[2][0][0] if tile2Enemies.count(self.newTiles[2][0][0]) == 1 else self.newTiles[2][0][1] if tile2Enemies.count(self.newTiles[2][0][1]) == 1 else self.newTiles[2][1][0]

                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((30, 145), "Kill the " + target1 + (" (and resulting Hollows)" if target1 == "Phalanx" else "") + " starting on tile one\nand the " + target2 + (" (and resulting Hollows)" if target2 == "Phalanx" else "") + " starting on tile two", "black", font)
                imageWithText.text((145, 250), "All objective enemies have 5 health.", "black", font)

                adapter.debug("\tEnd of pitch_black", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def pitch_black_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of pitch_black_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.darkness, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=147, y=197.5)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["darkness"])

                adapter.debug("\tEnd of pitch_black_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def promised_respite_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of promised_respite_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.snowstorm, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=148, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["snowstorm"])

                adapter.debug("\tEnd of promised_respite_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def puppet_master(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of puppet_master", caller=calframe[1][3])

                imageWithText = ImageDraw.Draw(self.encounterImage)

                text = "The " + self.newTiles[1][0][0] + " cannot suffer\ndamage."
                if enemies[self.newTiles[1][0][1]]["health"] < 5:
                    text += "\nThe " + self.newTiles[1][0][1] + " has 5 health."

                imageWithText.text((145, 198), text, "black", font)
                imageWithText.text((30, 150), "Kill the " + self.newTiles[1][0][1] + (" (and resulting Hollows)" if self.newTiles[1][0][1] == "Phalanx" else ""), "black", font)

                adapter.debug("\tEnd of puppet_master", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def skeletal_spokes(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of skeletal_spokes", caller=calframe[1][3])

                self.encounterImage.paste(im=self.stagger, box=(338, 225), mask=self.stagger)
                imageWithText = ImageDraw.Draw(self.encounterImage)
                text = self.newTiles[2][0][0] + "s ignore barrels during\nmovement. If a" + ("n " if self.newTiles[2][0][0][0].lower() in {"a", "e", "i", "o", "u"} else " ") + self.newTiles[2][0][0]
                text += " is pushed\nonto a node containing a barrel, it suffers     ,\nthen discard the barrel. If a" + ("n " if self.newTiles[2][0][0][0].lower() in {"a", "e", "i", "o", "u"} else " ")
                text += self.newTiles[2][0][0] + "\nis killed, respawn it on the closest enemy node,\nthen draw a treasure card and add it to the\ninventory."
                imageWithText.text((145, 198), text, "black", font)

                adapter.debug("\tEnd of skeletal_spokes", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def skeleton_overlord(self):
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

                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((30, 150), "Kill the " + self.newTiles[1][0][0] + (" (and resulting Hollows)" if self.newTiles[1][0][0] == "Phalanx" else ""), "black", font)
                imageWithText.text((145, 194), "Timer (2)", "black", fontItalics)
                imageWithText.text((192, 197), "Spawn a" + ("n " if spawn[0].lower() in {"a", "e", "i", "o", "u"} else " ") + spawn, "black", font)
                text = "on each enemy node, then reset the timer track."
                text += "\nDouble the " + self.newTiles[1][0][0] + "'s starting\nhealth, and increase its armour and resistance\nvalues by 1."
                text += "\nEach time a" + ("n " if spawn[0].lower() in {"a", "e", "i", "o", "u"} else " ") + spawn
                text += " is killed, the\n" + self.newTiles[1][0][0] + " suffers 1 damage."
                imageWithText.text((145, 210), text, "black", font)

                adapter.debug("\tEnd of skeleton_overlord", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def skeleton_overlord_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of skeleton_overlord_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.timer, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["timer"])

                adapter.debug("\tEnd of skeleton_overlord_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def snowblind_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of snowblind_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.snowstorm, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146.5, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["snowstorm"])

                self.keyword1 = tk.Label(self.encounterFrame, image=self.bitterCold, borderwidth=0, highlightthickness=0)
                self.keyword1.place(x=146, y=215)
                tooltip1 =  CreateToolTip(self.keyword1, self.keywordText["bitterCold"])

                self.keyword2 = tk.Label(self.encounterFrame, image=self.hidden, borderwidth=0, highlightthickness=0)
                self.keyword2.place(x=146, y=233)
                tooltip2 =  CreateToolTip(self.keyword2, self.keywordText["hidden"])

                adapter.debug("\tEnd of snowblind_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_abandoned_chest(self):
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

                imageWithText = ImageDraw.Draw(self.encounterImage)
                text = "When the chest is opened,\nspawn a" + ("n " if spawn1[0].lower() in {"a", "e", "i", "o", "u"} else " ")
                text += spawn1 + "\nand a" + ("n " if spawn1[0].lower() in {"a", "e", "i", "o", "u"} else " ")
                text += spawn2 + "\non the enemy node closest to the chest."
                imageWithText.text((145, 198), text, "black", font)

                adapter.debug("\tEnd of the_abandoned_chest", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_beast_from_the_depths(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_beast_from_the_depths", caller=calframe[1][3])

                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((30, 150), "Kill the " + self.newTiles[1][0][0] + (" (and resulting Hollows)" if self.newTiles[1][0][0] == "Phalanx" else ""), "black", font)
                imageWithText.text((145, 210), "If an enemy attack causes 0 damage,\nthe target adds on stamina token to their\nendurance bar.", "black", font)

                adapter.debug("\tEnd of the_beast_from_the_depths", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_beast_from_the_depths_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_beast_from_the_depths_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.trial, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146, y=196)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["trial"])

                adapter.debug("\tEnd of the_beast_from_the_depths_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_first_bastion(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_first_bastion", caller=calframe[1][3])

                self.encounterImage.paste(im=self.enemyNode1, box=(188, 227), mask=self.enemyNode1)
                self.encounterImage.paste(im=self.enemyNode1, box=(193, 256), mask=self.enemyNode1)
                self.encounterImage.paste(im=self.enemyNode2, box=(201, 242), mask=self.enemyNode2)

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

                imageWithText = ImageDraw.Draw(self.encounterImage)
                imageWithText.text((145, 198), "Trial  (Kill the " + spawn3 + (" and resulting Hollows)" if spawn3 == "Phalanx" else ")"), "black", fontItalics)

                text = "Lever activations:"
                text += "\nFirst: On     spawn a" + ("n " if spawn1[0].lower() in {"a", "e", "i", "o", "u"} else " ") + spawn1
                text += "\nSecond: On     spawn a" + ("n " if spawn2[0].lower() in {"a", "e", "i", "o", "u"} else " ") + spawn2
                text += "\nThird: On     spawn a" + ("n " if spawn3[0].lower() in {"a", "e", "i", "o", "u"} else " ") + spawn3
                imageWithText.text((145, 215), text, "black", font)

                adapter.debug("\tEnd of the_first_bastion", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_first_bastion_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_first_bastion_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.trial, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146, y=201)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["trial"])

                adapter.debug("\tEnd of the_first_bastion_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_last_bastion(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_last_bastion", caller=calframe[1][3])

                self.encounterImage.paste(im=self.push, box=(204, 285), mask=self.push)
                imageWithText = ImageDraw.Draw(self.encounterImage)
                target = sorted([enemy for enemy in self.newTiles[1][0] + self.newTiles[1][1]], key=lambda x: enemiesDict[x].difficulty)[0]
                imageWithText.text((145, 230), "Trial  (Kill the " + target + (" and resulting Hollows" if target == "Phalanx" else "") + " first.)", "black", fontItalics)
                text = "Increase the " + target + "'s starting\nhealth " + ("to 10" if enemiesDict[target].health < 10 else "by 5")
                text += ", and its dodge difficulty value by 1.\nThe " + target + "'s\n attacks gain     and +1 damage"
                imageWithText.text((145, 245), text, "black", font)

                adapter.debug("\tEnd of the_last_bastion", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_last_bastion_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_last_bastion_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.snowstorm, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146.5, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["snowstorm"])

                self.keyword1 = tk.Label(self.encounterFrame, image=self.bitterCold, borderwidth=0, highlightthickness=0)
                self.keyword1.place(x=146, y=215)
                tooltip1 =  CreateToolTip(self.keyword1, self.keywordText["bitterCold"])

                self.keyword2 = tk.Label(self.encounterFrame, image=self.trial, borderwidth=0, highlightthickness=0)
                self.keyword2.place(x=146, y=233)
                tooltip2 =  CreateToolTip(self.keyword2, self.keywordText["trial"])

                adapter.debug("\tEnd of the_last_bastion_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_locked_grave(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_locked_grave", caller=calframe[1][3])

                imageWithText = ImageDraw.Draw(self.encounterImage)
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
                
                spawn = choice(enemyList)
                imageWithText.text((145, 198), "Trial  (Kill the " + spawn + (" and resulting Hollows)" if spawn == "Phalanx" else ")"), "black", fontItalics)
                text = "If the lever is activated,\nspawn a" + ("n " if spawn[0].lower() in {"a", "e", "i", "o", "u"} else " ")
                text += spawn + " on tile three,\non the closest enemy spawn node\nto the character."
                imageWithText.text((145, 215), text, "black", font)

                adapter.debug("\tEnd of the_locked_grave", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_locked_grave_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_locked_grave_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.trial, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146, y=201)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["trial"])

                adapter.debug("\tEnd of the_locked_grave_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_mass_grave_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_mass_grave_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.onslaught, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=147, y=197.5)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["onslaught"])

                self.keyword1 = tk.Label(self.encounterFrame, image=self.timer, borderwidth=0, highlightthickness=0)
                self.keyword1.place(x=147, y=215)
                tooltip1 =  CreateToolTip(self.keyword1, self.keywordText["timer"])

                self.keyword2 = tk.Label(self.encounterFrame, image=self.timer, borderwidth=0, highlightthickness=0)
                self.keyword2.place(x=147, y=227)
                tooltip2 =  CreateToolTip(self.keyword2, self.keywordText["timer"])

                self.keyword3 = tk.Label(self.encounterFrame, image=self.timer, borderwidth=0, highlightthickness=0)
                self.keyword3.place(x=147, y=239)
                tooltip3 =  CreateToolTip(self.keyword3, self.keywordText["timer"])

                adapter.debug("\tEnd of the_mass_grave_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def the_skeleton_ball(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of the_skeleton_ball", caller=calframe[1][3])

                imageWithText = ImageDraw.Draw(self.encounterImage)
                text = "Kill the " + self.newTiles[1][0][0] + (" (and resulting Hollows)" if self.newTiles[1][0][0] == "Phalanx" else "") + " starting on tile one\nand the " + self.newTiles[3][1][0] + (" (and resulting Hollows)" if self.newTiles[3][1][0] == "Phalanx" else "") + " starting on tile three"
                imageWithText.text((30, 145), text, "black", font)

                adapter.debug("\tEnd of the_skeleton_ball", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def trecherous_tower(self):
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

                self.encounterImage.paste(im=self.eerie, box=(220, 205), mask=self.eerie)
                self.encounterImage.paste(im=allEnemies[spawns[0]]["image new"], box=(255, 209), mask=allEnemies[spawns[0]]["image new"])
                self.encounterImage.paste(im=allEnemies[spawns[1]]["image new"], box=(255, 242), mask=allEnemies[spawns[1]]["image new"])
                self.encounterImage.paste(im=allEnemies[spawns[2]]["image new"], box=(255, 275), mask=allEnemies[spawns[2]]["image new"])

                adapter.debug("\tEnd of trecherous_tower", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def trecherous_tower_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of trecherous_tower_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.snowstorm, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=148, y=197)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["snowstorm"])

                self.keyword1 = tk.Label(self.encounterFrame, image=self.bitterCold, borderwidth=0, highlightthickness=0)
                self.keyword1.place(x=148, y=214)
                tooltip1 =  CreateToolTip(self.keyword1, self.keywordText["bitterCold"])

                self.keyword2 = tk.Label(self.encounterFrame, image=self.eerieTooltip, borderwidth=0, highlightthickness=0)
                self.keyword2.place(x=146, y=232)
                tooltip2 =  CreateToolTip(self.keyword2, self.keywordText["eerieTooltip"])

                adapter.debug("\tEnd of trecherous_tower_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def unseen_scurrying_tooltips(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of unseen_scurrying_tooltips", caller=calframe[1][3])

                self.keyword0 = tk.Label(self.encounterFrame, image=self.hidden, borderwidth=0, highlightthickness=0)
                self.keyword0.place(x=146.5, y=198)
                tooltip0 =  CreateToolTip(self.keyword0, self.keywordText["hidden"])

                adapter.debug("\tEnd of unseen_scurrying_tooltips", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


        def velkas_chosen(self):
            try:
                curframe = inspect.currentframe()
                calframe = inspect.getouterframes(curframe, 2)
                adapter.debug("Start of velkas_chosen", caller=calframe[1][3])

                self.encounterImage.paste(im=self.playerCountImage, box=(228, 212), mask=self.playerCountImage)
                self.encounterImage.paste(im=self.poison, box=(169, 255), mask=self.poison)
                imageWithText = ImageDraw.Draw(self.encounterImage)
                target = sorted([enemy for enemy in self.newTiles[2][0] + self.newTiles[2][1]], key=lambda x: enemiesDict[x].difficulty, reverse=True)[0]
                imageWithText.text((30, 150), "Kill the " + target + (" (and resulting Hollows)" if target == "Phalanx" else ""), "black", font)
                text = "Increase the " + target + "'s\nstarting health by     +2, and its block,\nresistance, and dodge difficulty values by 1.\n" + target + " attacks\n gain     ."
                imageWithText.text((145, 200), text, "black", font)

                adapter.debug("\tEnd of velkas_chosen", caller=calframe[1][3])
            except Exception as e:
                adapter.exception(e)
                raise


    coreSets = {"Dark Souls The Board Game", "The Painted World of Ariamis", "The Tomb of Giants"}
    encountersWithInvadersOrMimics = {
        "Blazing Furnace",
        "Brume Tower",
        "Courtyard of Lothric",
        "Fortress Gates",
        "Sewers of Lordran"
    }
    
    root = tk.Tk()
    root.title("Dark Souls The Board Game Enemy Shuffler")
    root.tk.call("source", "Azure-ttk-theme-main\\azure.tcl")
    root.tk.call("set_theme", "dark")
    root.iconphoto(True, tk.PhotoImage(file=os.path.join(baseFolder + "\\images", "Crystal Lizard.png")))

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
