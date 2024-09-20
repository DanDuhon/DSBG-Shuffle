try:
    import errno
    import tkinter as tk
    from copy import deepcopy
    from datetime import datetime
    from json import dump, load
    from os import path
    from PIL import ImageTk, ImageDraw, UnidentifiedImageError
    from tkinter import filedialog, ttk

    from dsbg_shuffle_enemies import enemiesDict
    from dsbg_shuffle_utility import PopupWindow, VerticalScrolledFrame, clear_other_tab_images, error_popup, log, baseFolder, font, fontEncounterName, fontFlavor, pathSep


    class EncounterBuilderFrame(ttk.Frame):
        def __init__(self, app, root):
            super(EncounterBuilderFrame, self).__init__()
            self.app = app
            self.root = root

            self.customEncounter = {}

            self.customEncountersButtonFrame = ttk.Frame(self)
            self.customEncountersButtonFrame.pack(side=tk.TOP, anchor=tk.W)

            self.newEncounterButton = ttk.Button(self.customEncountersButtonFrame, text="New Encounter", width=16, command=self.new_custom_encounter)
            self.newEncounterButton.grid(column=0, row=0, padx=5, pady=5)
            self.loadButton = ttk.Button(self.customEncountersButtonFrame, text="Load Encounter", width=16, command=self.load_custom_encounter)
            self.loadButton.grid(column=2, row=0, padx=(175, 5), pady=5)
            self.saveButton = ttk.Button(self.customEncountersButtonFrame, text="Save Encounter", width=16, command=self.save_custom_encounter)
            self.saveButton.grid(column=3, row=0, padx=5, pady=5)
            
            self.encounterBuilderScroll = EncounterBuilderScrollFrame(root=root, app=app, topFrame=self)
            self.encounterBuilderScroll.pack(side=tk.TOP, anchor=tk.W, expand=True, fill="both")

            self.new_custom_encounter()


        def new_custom_encounter(self, event=None):
            try:
                log("Start of new_custom_encounter")

                self.app.selected = None

                e = self.encounterBuilderScroll

                e.iconMenuVal.set("")
                e.iconSaveErrorsVal.set("")
                e.iconSizeMenuVal.set("")
                e.iconImageErrorsVal.set("")
                e.xPositionVal.set("")
                e.yPositionVal.set("")
                
                e.encounterSetEntry.delete("1.0", tk.END)
                e.encounterNameEntry.delete("1.0", tk.END)
                e.flavorEntry.delete("1.0", tk.END)
                e.objectiveEntry.delete("1.0", tk.END)
                e.rewardSoulsEntry.delete("1.0", tk.END)
                e.rewardSearchEntry.delete("1.0", tk.END)
                e.rewardDrawEntry.delete("1.0", tk.END)
                e.rewardRefreshEntry.delete("1.0", tk.END)
                e.rewardTrialEntry.delete("1.0", tk.END)
                e.keywordsEntry.delete("1.0", tk.END)
                e.specialRulesEntry.delete("1.0", tk.END)
                e.iconNameEntry.delete("1.0", tk.END)

                e.rewardSoulsPerPlayer.state(["!selected"])
                e.shortcut.state(["!selected"])
                e.levelMenu.set(e.levelMenuList[0])
                e.numberOfTilesMenu.set(e.numberOfTilesMenuList[0])
                e.tileLayoutMenu.set("")

                e.update_lists()
                
                clear_other_tab_images(self.app, "encounters", "encounters")
                if getattr(self.app, "displayTopLeft", None):
                    self.app.displayImages["encounters"][self.app.displayTopLeft]["image"] = "custom"
                    self.app.displayImages["encounters"][self.app.displayTopLeft]["activeTab"] = "custom"
                    self.app.displayTopLeft.config(image="")
                    self.app.displayTopLeft.image=None
                
                log("End of new_custom_encounter")
            except Exception as e:
                error_popup(self.root, e)
                raise

            
        def apply_changes(self, event=None):
            try:
                if not hasattr(self, "encounterBuilderScroll") or not hasattr(self.app, "encounterTab"):
                    return
                
                log("Start of apply_changes")

                e = self.encounterBuilderScroll

                clear_other_tab_images(self.app, "encounters", "encounters")

                self.app.encounterTab.apply_keyword_tooltips(None, None)
                
                if e.numberOfTilesMenuVal.get() == "1" and e.tileLayoutMenu.get() == "1 Tile 4x4" and e.tileSelections[1]["traps"]["value"].get() == 1:
                    displayPhotoImage = self.app.create_image("custom_encounter_1_tile_4x4_traps.jpg", "customEncounter", 1, extensionProvided=True)
                elif e.numberOfTilesMenuVal.get() == "1" and e.tileLayoutMenu.get() == "1 Tile 4x4":
                    displayPhotoImage = self.app.create_image("custom_encounter_1_tile_4x4_no_traps.jpg", "customEncounter", 1, extensionProvided=True)
                elif e.numberOfTilesMenuVal.get() == "1" and e.tileSelections[1]["traps"]["value"].get() == 1:
                    displayPhotoImage = self.app.create_image("custom_encounter_1_tile_traps.jpg", "customEncounter", 1, extensionProvided=True)
                elif e.numberOfTilesMenuVal.get() == "1":
                    displayPhotoImage = self.app.create_image("custom_encounter_1_tile_no_traps.jpg", "customEncounter", 1, extensionProvided=True)
                elif e.numberOfTilesMenuVal.get() == "2":
                    displayPhotoImage = self.app.create_image("custom_encounter_2_tile.jpg", "customEncounter", 1, extensionProvided=True)
                elif e.numberOfTilesMenuVal.get() == "3":
                    displayPhotoImage = self.app.create_image("custom_encounter_3_tile.jpg", "customEncounter", 1, extensionProvided=True)
                else:
                    return

                imageWithText = ImageDraw.Draw(self.app.displayImage)

                # Empty Set Icon
                if e.emptySetIconVal.get() == 1:
                    self.app.displayImage.paste(im=self.app.emptySetIcon, box=(11, 15), mask=self.app.emptySetIcon)
                
                # Encounter Name
                imageWithText.text((80, 25 + (10 if e.encounterNameEntry.get("1.0", "end").strip().count("\n") < 1 else 0)), e.encounterNameEntry.get("1.0", "end"), "white", fontEncounterName)
                
                # Flavor Text
                imageWithText.text((20, 88 + (7 if e.flavorEntry.get("1.0", "end").strip().count("\n") < 1 else 0)), e.flavorEntry.get("1.0", "end"), "black", fontFlavor)
                
                # Objective Text
                imageWithText.text((20, 146), e.objectiveEntry.get("1.0", "end"), "black", font)
                
                # Keywords
                imageWithText.text((141, 195), e.keywordsEntry.get("1.0", "end"), "black", fontFlavor)
                rulesNewlines = 0 if not e.keywordsEntry.get("1.0", "end").strip() else e.keywordsEntry.get("1.0", "end").strip().count("\n")
                
                # Special Rules
                imageWithText.text((141, 195), ("\n" + ("\n" * rulesNewlines) if e.keywordsEntry.get("1.0", "end").strip() else "") + e.specialRulesEntry.get("1.0", "end"), "black", font)

                # Encounter Level
                if e.levelMenuVal.get():
                    self.app.displayImage.paste(im=self.app.levelIcons[int(e.levelMenuVal.get())], box=(328, 15), mask=self.app.levelIcons[int(e.levelMenuVal.get())])

                lineCount = 0

                # Reward Souls
                if e.rewardSoulsEntry.get("1.0", "end").strip():
                    if e.rewardSoulsPerPlayerVal.get() == 1:
                        self.app.displayImage.paste(im=self.app.rewardsSoulsPlayersIcon, box=(20, 195), mask=self.app.rewardsSoulsPlayersIcon)
                    else:
                        self.app.displayImage.paste(im=self.app.rewardsSoulsIcon, box=(20, 195), mask=self.app.rewardsSoulsIcon)
                    imageWithText.text((20, 195), "\n" + ("      " if e.rewardSoulsPerPlayerVal.get() == 1 else "") + e.rewardSoulsEntry.get("1.0", "end"), "black", font)
                    lineCount += 2 + e.rewardSoulsEntry.get("1.0", "end").strip().count("\n")

                # Reward Search
                if e.rewardSearchEntry.get("1.0", "end").strip():
                    y = 195 + round(12.5 * lineCount)
                    self.app.displayImage.paste(im=self.app.rewardsSearchIcon, box=(20, y), mask=self.app.rewardsSearchIcon)
                    imageWithText.text((20, y), "\n" + e.rewardSearchEntry.get("1.0", "end"), "black", font)
                    lineCount += 2 + e.rewardSearchEntry.get("1.0", "end").strip().count("\n")

                # Reward Draw
                if e.rewardDrawEntry.get("1.0", "end").strip():
                    y = 195 + round(12.5 * lineCount)
                    self.app.displayImage.paste(im=self.app.rewardsDrawIcon, box=(20, y), mask=self.app.rewardsDrawIcon)
                    imageWithText.text((20, y), "\n" + e.rewardDrawEntry.get("1.0", "end"), "black", font)
                    lineCount += 2 + e.rewardDrawEntry.get("1.0", "end").strip().count("\n")

                # Reward Refresh
                if e.rewardRefreshEntry.get("1.0", "end").strip():
                    y = 195 + round(12.5 * lineCount)
                    self.app.displayImage.paste(im=self.app.rewardsRefreshIcon, box=(20, y), mask=self.app.rewardsRefreshIcon)
                    imageWithText.text((20, y), "\n" + e.rewardRefreshEntry.get("1.0", "end"), "black", font)
                    lineCount += 2 + e.rewardRefreshEntry.get("1.0", "end").strip().count("\n")

                # Reward Trial
                if e.rewardTrialEntry.get("1.0", "end").strip():
                    y = 195 + round(12.5 * lineCount)
                    self.app.displayImage.paste(im=self.app.rewardsTrialIcon, box=(20, y), mask=self.app.rewardsTrialIcon)
                    imageWithText.text((20, y), "\n" + e.rewardTrialEntry.get("1.0", "end"), "black", font)
                    lineCount += 2 + e.rewardTrialEntry.get("1.0", "end").strip().count("\n")

                # Reward Shortcut
                if e.shortcutVal.get() == 1:
                    y = 195 + round(12.5 * lineCount)
                    self.app.displayImage.paste(im=self.app.rewardsShortcutIcon, box=(20, y), mask=self.app.rewardsShortcutIcon)

                # Tile Layout
                tileLayout = self.app.tileLayouts.get(e.tileLayoutMenuVal.get(), None)
                if tileLayout:
                    self.app.displayImage.paste(im=tileLayout["layout"], box=(20, 330), mask=tileLayout["layout"])

                    # Starting nodes
                    for tile in range(1, 4):
                        if e.tileSelections[tile]["startingTile"]["value"].get() == 1 and e.tileSelections[tile]["startingNodes"]["value"].get():
                            startingNodesLocation = e.tileSelections[tile]["startingNodes"]["value"].get()
                            if tile not in tileLayout["box"]:
                                continue
                            box = tileLayout["box"][tile][startingNodesLocation]
                            if startingNodesLocation in {"North", "South"}:
                                self.app.displayImage.paste(im=tileLayout["startingNodesHorizontal"], box=box, mask=tileLayout["startingNodesHorizontal"])
                            else:
                                self.app.displayImage.paste(im=tileLayout["startingNodesVertical"], box=box, mask=tileLayout["startingNodesVertical"])
                                
                # Tile numbers and traps
                if e.numberOfTilesMenuVal.get() != "1":
                    for tile in range(1, 4):
                        if tile > int(e.numberOfTilesMenuVal.get()):
                            continue

                        box = (334, 377 + (122 * (tile - 1)))

                        if e.tileSelections[tile]["startingTile"]["value"].get() == 1 and e.tileSelections[tile]["traps"]["value"].get() == 1:
                            image = self.app.tileNumbers[tile]["starting"]["traps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)
                        elif e.tileSelections[tile]["startingTile"]["value"].get() == 1 and e.tileSelections[tile]["traps"]["value"].get() != 1:
                            image = self.app.tileNumbers[tile]["starting"]["noTraps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)
                        elif e.tileSelections[tile]["startingTile"]["value"].get() != 1 and e.tileSelections[tile]["traps"]["value"].get() == 1:
                            image = self.app.tileNumbers[tile]["notStarting"]["traps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)
                        elif e.tileSelections[tile]["startingTile"]["value"].get() != 1 and e.tileSelections[tile]["traps"]["value"].get() != 1:
                            image = self.app.tileNumbers[tile]["notStarting"]["noTraps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)

                # Terrain
                for tile in range(1, int(e.numberOfTilesMenuVal.get()) + 1):
                    for row in range(1, 5 if e.tileLayoutMenu.get() == "1 Tile 4x4" else 3):
                        box = (301, 380 + (29 * (row - 1)) + (122 * (tile - 1)) + (29 if e.levelMenuVal.get() == "4" else 0))
                        if e.tileSelections[tile][row]["terrain"]["value"].get() in self.app.terrain:
                            image = self.app.terrain[e.tileSelections[tile][row]["terrain"]["value"].get()]
                            self.app.displayImage.paste(im=image, box=box, mask=image)

                # Enemies
                for tile in range(1, int(e.numberOfTilesMenuVal.get()) + 1):
                    for row in range(1, 5 if e.tileLayoutMenu.get() == "1 Tile 4x4" else 3):
                        for en in range(1, 4):
                            box = (300 + (29 * (en - 1)), 323 + (29 * (row - 1)) + (122 * (tile - 1)))
                            if e.tileSelections[tile][row]["enemies"][en]["value"].get() in self.app.allEnemies:
                                enemy = e.tileSelections[tile][row]["enemies"][en]["value"].get()
                                image = self.app.allEnemies[enemy]["imageNew"]
                                self.app.displayImage.paste(im=image, box=box, mask=image)

                # Custom Icons
                for icon in [icon for icon in e.icons if "" not in e.icons[icon]["position"]]:
                    image = e.icons[icon]["image"]
                    box = (int(e.icons[icon]["position"][0]), int(e.icons[icon]["position"][1]))
                    self.app.displayImage.paste(im=image, box=box, mask=image)

                self.customEncounter["set"] = e.encounterSetEntry.get("1.0", "end")
                self.customEncounter["emptySetIcon"] = e.emptySetIconVal.get()
                self.customEncounter["image"] = self.app.displayImage.copy()
                self.customEncounter["numberOfTiles"] = e.numberOfTilesMenuVal.get()
                self.customEncounter["level"] = e.levelMenuVal.get()
                self.customEncounter["encounterName"] = e.encounterNameEntry.get("1.0", "end")
                self.customEncounter["flavor"] = e.flavorEntry.get("1.0", "end")
                self.customEncounter["objective"] = e.objectiveEntry.get("1.0", "end")
                self.customEncounter["keywords"] = e.keywordsEntry.get("1.0", "end")
                self.customEncounter["specialRules"] = e.specialRulesEntry.get("1.0", "end")
                self.customEncounter["rewardSouls"] = e.rewardSoulsEntry.get("1.0", "end")
                self.customEncounter["rewardSoulsPerPlayer"] = e.rewardSoulsPerPlayerVal.get()
                self.customEncounter["rewardSearch"] = e.rewardSearchEntry.get("1.0", "end")
                self.customEncounter["rewardDraw"] = e.rewardDrawEntry.get("1.0", "end")
                self.customEncounter["rewardRefresh"] = e.rewardRefreshEntry.get("1.0", "end")
                self.customEncounter["rewardTrial"] = e.rewardTrialEntry.get("1.0", "end")
                self.customEncounter["rewardShortcut"] = e.shortcutVal.get()
                self.customEncounter["layout"] = e.tileLayoutMenuVal.get()
                self.customEncounter["icons"] = {k: v for k, v in e.icons.items() if "" not in e.icons[k]["position"]}
                self.customEncounter["tileSelections"] = {
                    1: {
                        "startingTile": {"value": e.tileSelections[1]["startingTile"]["value"].get()},
                        "startingNodes": {"value": e.tileSelections[1]["startingNodes"]["value"].get()},
                        "traps": {"value": e.tileSelections[1]["traps"]["value"].get()},
                        1: {"terrain": {"value": e.tileSelections[1][1]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": e.tileSelections[1][1]["enemies"][1]["value"].get()},
                                2: {"value": e.tileSelections[1][1]["enemies"][2]["value"].get()},
                                3: {"value": e.tileSelections[1][1]["enemies"][3]["value"].get()}
                            }},
                        2: {"terrain": {"value": e.tileSelections[1][2]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": e.tileSelections[1][2]["enemies"][1]["value"].get()},
                                2: {"value": e.tileSelections[1][2]["enemies"][2]["value"].get()},
                                3: {"value": e.tileSelections[1][2]["enemies"][3]["value"].get()}
                            }},
                        3: {"terrain": {"value": e.tileSelections[1][3]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": e.tileSelections[1][3]["enemies"][1]["value"].get()},
                                2: {"value": e.tileSelections[1][3]["enemies"][2]["value"].get()},
                                3: {"value": e.tileSelections[1][3]["enemies"][3]["value"].get()}
                            }},
                        4: {"terrain": {"value": e.tileSelections[1][4]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": e.tileSelections[1][4]["enemies"][1]["value"].get()},
                                2: {"value": e.tileSelections[1][4]["enemies"][2]["value"].get()},
                                3: {"value": e.tileSelections[1][4]["enemies"][3]["value"].get()}
                            }}
                        },
                    2: {
                        "startingTile": {"value": e.tileSelections[2]["startingTile"]["value"].get()},
                        "startingNodes": {"value": e.tileSelections[2]["startingNodes"]["value"].get()},
                        "traps": {"value": e.tileSelections[2]["traps"]["value"].get()},
                        1: {"terrain": {"value": e.tileSelections[2][1]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": e.tileSelections[2][1]["enemies"][1]["value"].get()},
                                2: {"value": e.tileSelections[2][1]["enemies"][2]["value"].get()},
                                3: {"value": e.tileSelections[2][1]["enemies"][3]["value"].get()}
                            }},
                        2: {"terrain": {"value": e.tileSelections[2][2]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": e.tileSelections[2][2]["enemies"][1]["value"].get()},
                                2: {"value": e.tileSelections[2][2]["enemies"][2]["value"].get()},
                                3: {"value": e.tileSelections[2][2]["enemies"][3]["value"].get()}
                            }}
                        },
                    3: {
                        "startingTile": {"value": e.tileSelections[3]["startingTile"]["value"].get()},
                        "startingNodes": {"value": e.tileSelections[3]["startingNodes"]["value"].get()},
                        "traps": {"value": e.tileSelections[3]["traps"]["value"].get()},
                        1: {"terrain": {"value": e.tileSelections[3][1]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": e.tileSelections[3][1]["enemies"][1]["value"].get()},
                                2: {"value": e.tileSelections[3][1]["enemies"][2]["value"].get()},
                                3: {"value": e.tileSelections[3][1]["enemies"][3]["value"].get()}
                            }},
                        2: {"terrain": {"value": e.tileSelections[3][2]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": e.tileSelections[3][2]["enemies"][1]["value"].get()},
                                2: {"value": e.tileSelections[3][2]["enemies"][2]["value"].get()},
                                3: {"value": e.tileSelections[3][2]["enemies"][3]["value"].get()}
                            }}
                        }
                    }

                displayPhotoImage = ImageTk.PhotoImage(self.app.displayImage)
                self.app.displayTopLeft.config(image=displayPhotoImage)
                self.app.displayTopLeft.image=displayPhotoImage
                
                log("End of apply_changes")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def save_custom_encounter(self, event=None):
            try:
                log("Start of save_custom_encounter")

                e = self.encounterBuilderScroll

                file = (
                    baseFolder
                    + "\\lib\\dsbg_shuffle_custom_encounters\\".replace("\\", pathSep)
                    + " ".join(self.customEncounter["set"].strip().replace("\n", " ").split())
                    + "_"
                    + " ".join(self.customEncounter["encounterName"].strip().replace("\n", " ").split())
                    + "_"
                    + str(self.customEncounter["level"])
                    + ".json")

                saveIcons = {}
                for icon in e.icons:
                    if "" in e.icons[icon]["position"]:
                        continue
                    saveIcons[icon] = {k: v for k, v in e.icons[icon].items() if k not in {"image", "photoImage"}}

                saveEncounter = {k: v for k, v in self.customEncounter.items() if k not in {"image", "icons"}}
                saveEncounter["icons"] = saveIcons

                with open(file, "w") as encounterFile:
                    dump(saveEncounter, encounterFile)

                self.customEncounter["image"].save(path.splitext(file)[0] + ".jpg")
                
                self.app.add_custom_encounters()
                self.app.allExpansions = set([self.app.encounters[encounter]["expansion"] for encounter in self.app.encounters]) | set(["Phantoms"])
                self.app.level4Expansions = set([self.app.encounters[encounter]["expansion"] for encounter in self.app.encounters if self.app.encounters[encounter]["level"] == 4])
                self.app.availableExpansions = set(self.app.settings["availableExpansions"])
                self.app.v2Expansions = (self.app.allExpansions - self.app.v1Expansions - self.app.level4Expansions)
                self.app.encounterTab.set_encounter_list()
                self.app.encounterTab.treeviewEncounters.pack_forget()
                self.app.encounterTab.treeviewEncounters.destroy()
                self.app.encounterTab.create_encounters_treeview()

                self.encounterSaveLabelVal.set((" " * 64) + "Saved " + datetime.now().strftime("%H:%M:%S"))

                log("End of save_custom_encounter (saved to " + str(encounterFile) + ")")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def load_custom_encounter(self, event=None):
            try:
                log("Start of load_custom_encounter")

                e = self.encounterBuilderScroll

                # Prompt the user to find the encounter file.
                file = filedialog.askopenfilename(initialdir=baseFolder + "\\lib\\dsbg_shuffle_custom_encounters".replace("\\", pathSep), filetypes = [(".json", ".json")])

                # If the user did not select a file, do nothing.
                if not file:
                    log("End of load_custom_encounter (file dialog canceled)")
                    return

                # If the user did not select a JSON file, notify them that that was an invalid file.
                if path.splitext(file)[1] != ".json":
                    self.app.set_bindings_buttons_menus(False)
                    PopupWindow(self.root, labelText="Invalid DSBG-Shuffle encounter file.", firstButton="Ok")
                    self.app.set_bindings_buttons_menus(True)
                    log("End of load_custom_encounter (invalid file)")
                    return

                self.new_custom_encounter()

                log("Loading file " + file)

                with open(file, "r") as f:
                    self.customEncounter = load(f)
                    
                # I forgot Refresh rewards - add that if this is an older custom encounter file.
                if set(self.customEncounter.keys()) == {
                        "set", "numberOfTiles", "level", "encounterName", "flavor", "objective", "keywords",
                        "specialRules", "rewardSouls", "rewardSoulsPerPlayer", "rewardSearch", "rewardDraw",
                        "rewardTrial", "rewardShortcut", "layout", "icons", "tileSelections"}:
                    self.customEncounter["rewardRefresh"] = ""

                # Add empty set icon key for older encounter files.
                if set(self.customEncounter.keys()) == {
                        "set", "numberOfTiles", "level", "encounterName", "flavor", "objective", "keywords",
                        "specialRules", "rewardSouls", "rewardSoulsPerPlayer", "rewardSearch", "rewardDraw",
                        "rewardRefresh", "rewardTrial", "rewardShortcut", "layout", "icons", "tileSelections"}:
                    self.customEncounter["emptySetIcon"] = 0

                # Check to see if there are any invalid keys in the JSON file.
                # This is about as sure as I can be that you can't load random JSON into the app.
                if set(self.customEncounter.keys()) != {
                        "set", "numberOfTiles", "level", "encounterName", "flavor", "objective", "keywords",
                        "specialRules", "rewardSouls", "rewardSoulsPerPlayer", "rewardSearch", "rewardDraw",
                        "rewardRefresh", "rewardTrial", "rewardShortcut", "layout", "icons", "tileSelections",
                        "emptySetIcon"}:
                    self.app.set_bindings_buttons_menus(False)
                    PopupWindow(self.root, labelText="Invalid DSBG-Shuffle encounter file.", firstButton="Ok")
                    self.app.set_bindings_buttons_menus(True)
                    self.campaign = []
                    log("End of load_custom_encounter (invalid file)")
                    return
                
                for icon in self.customEncounter["icons"]:
                    if not path.isfile(baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + self.customEncounter["icons"][icon]["file"]):
                        PopupWindow(self.root, labelText="Missing custom icon image for " + icon + ".", firstButton="Ok")
                        return
                    i, p = self.app.create_image(baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + self.customEncounter["icons"][icon]["file"], self.customEncounter["icons"][icon]["size"], 99, pathProvided=True, extensionProvided=True, emptySetIcon=self.customEncounter["emptySetIcon"])
                    self.customEncounter["icons"][icon]["image"] = i
                    self.customEncounter["icons"][icon]["photoImage"] = p

                e.icons = self.customEncounter["icons"]
                e.iconMenuList = [icon for icon in e.icons.keys()]
                e.iconMenu.config(values=e.iconMenuList)
                e.iconMenu.set("")
                
                e.encounterSaveLabelVal.set("")

                # Need to fill in all the GUI elements.
                e.encounterSetEntry.insert(tk.END, self.customEncounter["set"])
                e.emptySetIconVal.set(self.customEncounter["emptySetIcon"])
                e.numberOfTilesMenuVal.set(self.customEncounter["numberOfTiles"])
                e.levelMenuVal.set(self.customEncounter["level"])
                e.encounterNameEntry.insert(tk.END, self.customEncounter["encounterName"])
                e.flavorEntry.insert(tk.END, self.customEncounter["flavor"])
                e.objectiveEntry.insert(tk.END, self.customEncounter["objective"])
                e.keywordsEntry.insert(tk.END, self.customEncounter["keywords"])
                e.specialRulesEntry.insert(tk.END, self.customEncounter["specialRules"])
                e.rewardSoulsEntry.insert(tk.END, self.customEncounter["rewardSouls"])
                e.rewardSoulsPerPlayerVal.set(self.customEncounter["rewardSoulsPerPlayer"])
                e.rewardSearchEntry.insert(tk.END, self.customEncounter["rewardSearch"])
                e.rewardDrawEntry.insert(tk.END, self.customEncounter["rewardDraw"])
                e.rewardRefreshEntry.insert(tk.END, self.customEncounter["rewardRefresh"])
                e.rewardTrialEntry.insert(tk.END, self.customEncounter["rewardTrial"])
                e.shortcutVal.set(self.customEncounter["rewardShortcut"])
                    
                e.update_lists()

                e.tileLayoutMenuVal.set(self.customEncounter["layout"])
                e.tileSelections[1]["startingTile"]["value"].set(self.customEncounter["tileSelections"]["1"]["startingTile"]["value"])
                e.tileSelections[1]["startingNodes"]["value"].set(self.customEncounter["tileSelections"]["1"]["startingNodes"]["value"])
                e.tileSelections[1]["traps"]["value"].set(self.customEncounter["tileSelections"]["1"]["traps"]["value"])
                e.tileSelections[1][1]["terrain"]["value"].set(self.customEncounter["tileSelections"]["1"]["1"]["terrain"]["value"])
                e.tileSelections[1][1]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["1"]["1"]["enemies"]["1"]["value"])
                e.tileSelections[1][1]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["1"]["1"]["enemies"]["2"]["value"])
                e.tileSelections[1][1]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["1"]["1"]["enemies"]["3"]["value"])
                e.tileSelections[1][2]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["1"]["2"]["enemies"]["1"]["value"])
                e.tileSelections[1][2]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["1"]["2"]["enemies"]["2"]["value"])
                e.tileSelections[1][2]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["1"]["2"]["enemies"]["3"]["value"])
                if e.numberOfTilesMenuVal.get() == "1" and e.tileLayoutMenuVal.get() == "1 Tile 4x4":
                    e.tileSelections[1][3]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["2"]["3"]["enemies"]["1"]["value"])
                    e.tileSelections[1][3]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["2"]["3"]["enemies"]["2"]["value"])
                    e.tileSelections[1][3]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["2"]["3"]["enemies"]["3"]["value"])
                    e.tileSelections[1][3]["terrain"]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["terrain"]["value"])
                    e.tileSelections[1][4]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["2"]["4"]["enemies"]["1"]["value"])
                    e.tileSelections[1][4]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["2"]["4"]["enemies"]["2"]["value"])
                    e.tileSelections[1][4]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["2"]["4"]["enemies"]["3"]["value"])
                    e.tileSelections[1][4]["terrain"]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["terrain"]["value"])
                e.tileSelections[2]["startingTile"]["value"].set(self.customEncounter["tileSelections"]["2"]["startingTile"]["value"])
                e.tileSelections[2]["startingNodes"]["value"].set(self.customEncounter["tileSelections"]["2"]["startingNodes"]["value"])
                e.tileSelections[2]["traps"]["value"].set(self.customEncounter["tileSelections"]["2"]["traps"]["value"])
                e.tileSelections[2][1]["terrain"]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["terrain"]["value"])
                e.tileSelections[2][1]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["enemies"]["1"]["value"])
                e.tileSelections[2][1]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["enemies"]["2"]["value"])
                e.tileSelections[2][1]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["enemies"]["3"]["value"])
                e.tileSelections[2][2]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["enemies"]["1"]["value"])
                e.tileSelections[2][2]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["enemies"]["2"]["value"])
                e.tileSelections[2][2]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["enemies"]["3"]["value"])
                e.tileSelections[3]["startingTile"]["value"].set(self.customEncounter["tileSelections"]["3"]["startingTile"]["value"])
                e.tileSelections[3]["startingNodes"]["value"].set(self.customEncounter["tileSelections"]["3"]["startingNodes"]["value"])
                e.tileSelections[3]["traps"]["value"].set(self.customEncounter["tileSelections"]["3"]["traps"]["value"])
                e.tileSelections[3][1]["terrain"]["value"].set(self.customEncounter["tileSelections"]["3"]["1"]["terrain"]["value"])
                e.tileSelections[3][1]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["3"]["1"]["enemies"]["1"]["value"])
                e.tileSelections[3][1]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["3"]["1"]["enemies"]["2"]["value"])
                e.tileSelections[3][1]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["3"]["1"]["enemies"]["3"]["value"])
                e.tileSelections[3][2]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["3"]["2"]["enemies"]["1"]["value"])
                e.tileSelections[3][2]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["3"]["2"]["enemies"]["2"]["value"])
                e.tileSelections[3][2]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["3"]["2"]["enemies"]["3"]["value"])

                for tile in range(1, 4):
                    e.toggle_starting_nodes_menu(tile=tile)

                self.apply_changes()
                
                log("End of load_custom_encounter")
            except UnidentifiedImageError:
                # Handling for this occurred in create_image.
                return
            except EnvironmentError as err:
                if err.errno == errno.ENOENT: # ENOENT -> "no entity" -> "file not found"
                    # Handling for this occurred in create_image.
                    return
                else:
                    raise
            except Exception as e:
                error_popup(self.root, e)
                raise


    class EncounterBuilderScrollFrame(VerticalScrolledFrame):
        def __init__(self, app, root, topFrame):
            super(EncounterBuilderScrollFrame, self).__init__(parent=topFrame)
            self.app = app
            self.root = root
            self.topFrame = topFrame
            
            self._afterId = None

            self.rowSelectionMenuList = []
            self.tileSelectionMenuList = []
            self.iconMenuList = []

            self.eNamesDict = {enemiesDict[e].name: str(enemiesDict[e].expansions).replace("Dark Souls The Board Game", "Core") for e in enemiesDict}

            self.eNames = (
                [""] +   ["----------- Core -------------"]
                + sorted([enemiesDict[e].name for e in enemiesDict if "Dark Souls The Board Game" in enemiesDict[e].expansions])
                + [""] + ["---------- Darkroot ----------"]
                + sorted([enemiesDict[e].name for e in enemiesDict if "Darkroot" in enemiesDict[e].expansions])
                + [""] + ["--------- Explorers ----------"]
                + sorted([enemiesDict[e].name for e in enemiesDict if "Explorers" in enemiesDict[e].expansions])
                + [""] + ["--------- Iron Keep ----------"]
                + sorted([enemiesDict[e].name for e in enemiesDict if "Iron Keep" in enemiesDict[e].expansions])
                + [""] + ["---- Executioner Chariot -----"]
                + sorted([enemiesDict[e].name for e in enemiesDict if "Executioner Chariot" in enemiesDict[e].expansions])
                + [""] + ["-- Painted World of Ariamis --"]
                + sorted([enemiesDict[e].name for e in enemiesDict if "Painted World of Ariamis" in enemiesDict[e].expansions])
                + [""] + ["------ The Sunless City ------"]
                + sorted([enemiesDict[e].name for e in enemiesDict if "The Sunless City" in enemiesDict[e].expansions])
                + [""] + ["------- Tomb of Giants -------"]
                + sorted([enemiesDict[e].name for e in enemiesDict if "Tomb of Giants" in enemiesDict[e].expansions])
                + [""] + ["--------- Phantoms -----------"]
                + sorted([enemiesDict[e].name for e in enemiesDict if "Phantoms" in enemiesDict[e].expansions])
                )
                
            self.terrainNames = [
                "",
                "Barrel",
                "Envoy Banner",
                "Exit",
                "Fang Boar",
                "Gravestone",
                "Lever",
                "Shrine",
                "Torch",
                "Treasure Chest"
            ]

            self.startingNodesMenuList = ["North", "East", "South", "West"]
            
            self.infoFrame1 = ttk.Frame(self.interior)
            self.infoFrame1.pack(side=tk.TOP, anchor=tk.W)
            self.infoFrame2 = ttk.Frame(self.interior)
            self.infoFrame2.pack(side=tk.TOP, anchor=tk.W)
            self.infoFrame3 = ttk.Frame(self.interior)
            self.infoFrame3.pack(side=tk.TOP, anchor=tk.W)
            self.infoFrame4 = ttk.Frame(self.interior)
            self.infoFrame4.pack(side=tk.TOP, anchor=tk.W)
            self.separator1 = ttk.Separator(self.interior)
            self.separator1.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.infoFrame5 = ttk.Frame(self.interior)
            self.infoFrame5.pack(side=tk.TOP, anchor=tk.W)
            self.separator2 = ttk.Separator(self.interior)
            self.separator2.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.infoFrame6 = ttk.Frame(self.interior)
            self.infoFrame6.pack(side=tk.TOP, anchor=tk.W)
            self.separator3 = ttk.Separator(self.interior)
            self.separator3.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.layoutFrame1 = ttk.Frame(self.interior)
            self.layoutFrame1.pack(side=tk.TOP, anchor=tk.W)
            self.tileFrame1 = ttk.Frame(self.interior)
            self.tileFrame1.pack(side=tk.TOP, anchor=tk.W)
            self.separator4 = ttk.Separator(self.interior)
            self.separator4.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.tileFrame2 = ttk.Frame(self.interior)
            self.tileFrame2.pack(side=tk.TOP, anchor=tk.W)
            self.separator5 = ttk.Separator(self.interior)
            self.separator5.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.tileFrame3 = ttk.Frame(self.interior)
            self.tileFrame3.pack(side=tk.TOP, anchor=tk.W)
            self.separator6 = ttk.Separator(self.interior)
            self.separator6.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.iconsFrame = ttk.Frame(self.interior)
            self.iconsFrame.pack(side=tk.TOP, anchor=tk.W)
            self.iconsFrame2 = ttk.Frame(self.interior)
            self.iconsFrame2.pack(side=tk.TOP, anchor=tk.W)

            self.encounterTitle = ttk.Label(self.infoFrame1, text=(" " * 35) + "Encounter Data", font=("Arial", 16))
            self.encounterTitle.grid(column=0, row=0, padx=5, pady=5, columnspan=6, sticky=tk.W)
            
            self.encounterSetLabel = ttk.Label(self.infoFrame1, text="Set Name")
            self.encounterSetLabel.grid(column=0, row=1, padx=5, pady=5)
            self.encounterSetEntry = tk.Text(self.infoFrame1, width=17, height=1)
            self.encounterSetEntry.grid(column=1, row=1, padx=5, pady=5)
            self.encounterSaveLabelVal = tk.StringVar()
            self.encounterSaveLabel = ttk.Label(self.infoFrame1, textvariable=self.encounterSaveLabelVal)
            self.encounterSaveLabel.grid(column=2, row=1, padx=5, pady=5)
            
            self.emptySetIconVal = tk.IntVar()
            self.emptySetIcon = ttk.Checkbutton(self.infoFrame1, text="Empty Set Icon", variable=self.emptySetIconVal, command=self.topFrame.apply_changes)
            self.emptySetIcon.grid(column=3, row=1, padx=24, pady=5)
            self.emptySetIcon.state(["!alternate"])
            
            self.encounterNameLabel = ttk.Label(self.infoFrame2, text="Encounter\nName\t")
            self.encounterNameLabel.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)
            self.encounterNameEntry = tk.Text(self.infoFrame2, width=17, height=2)
            self.encounterNameEntry.bind("<KeyRelease>", self.handle_wait)
            self.encounterNameEntry.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.levelLabel = ttk.Label(self.infoFrame2, text="Encounter\nLevel")
            self.levelLabel.pack(side=tk.LEFT, anchor=tk.W, padx=(40, 5), pady=5)
            self.levelMenuList = ["1", "2", "3", "4"]
            self.levelMenuVal = tk.StringVar()
            self.levelMenuVal.set(self.levelMenuList[0])
            self.levelMenu = ttk.Combobox(self.infoFrame2, width=5, state="readonly", values=self.levelMenuList, textvariable=self.levelMenuVal)
            self.levelMenu.bind("<<ComboboxSelected>>", self.update_lists)
            self.levelMenu.unbind_class("TCombobox", "<MouseWheel>")
            self.levelMenu.unbind_class("TCombobox", "<ButtonPress-4>")
            self.levelMenu.unbind_class("TCombobox", "<ButtonPress-5>")
            self.previousLevelMenuVal = ""
            self.levelMenu.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.flavorLabel = ttk.Label(self.infoFrame3, text="Flavor\nText\t")
            self.flavorLabel.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)
            self.flavorEntry = tk.Text(self.infoFrame3, width=70, height=2)
            self.flavorEntry.bind("<KeyRelease>", self.handle_wait)
            self.flavorEntry.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.objectiveLabel = ttk.Label(self.infoFrame4, text="Objective\t")
            self.objectiveLabel.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)
            self.objectiveEntry = tk.Text(self.infoFrame4, width=70, height=2)
            self.objectiveEntry.bind("<KeyRelease>", self.handle_wait)
            self.objectiveEntry.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)

            self.rewardsTitle = ttk.Label(self.infoFrame5, text=(" " * 30) + "Rewards/Special Rules", font=("Arial", 16))
            self.rewardsTitle.grid(column=0, row=0, padx=5, pady=5, columnspan=6, sticky=tk.W)
            
            self.rewardSoulsPerPlayerVal = tk.IntVar()
            self.rewardSoulsPerPlayer = ttk.Checkbutton(self.infoFrame5, text="Souls Reward\nPer Player", variable=self.rewardSoulsPerPlayerVal, command=self.topFrame.apply_changes)
            self.rewardSoulsPerPlayer.grid(column=1, row=1, padx=5, pady=5, sticky=tk.W)
            self.rewardSoulsPerPlayer.state(["!alternate"])
            
            self.shortcutVal = tk.IntVar()
            self.shortcut = ttk.Checkbutton(self.infoFrame5, text="Shortcut\nReward", variable=self.shortcutVal, command=self.topFrame.apply_changes)
            self.shortcut.grid(column=2, row=1, padx=5, pady=5, sticky=tk.W)
            self.shortcut.state(["!alternate"])
            
            self.rewardSoulsLabel = ttk.Label(self.infoFrame5, text="Souls\nReward\t")
            self.rewardSoulsLabel.grid(column=0, row=2, padx=5, pady=5)
            self.rewardSoulsEntry = tk.Text(self.infoFrame5, width=17, height=2)
            self.rewardSoulsEntry.bind("<KeyRelease>", self.handle_wait)
            self.rewardSoulsEntry.grid(column=1, row=2, padx=5, pady=5, sticky=tk.W)
            
            self.rewardSearchLabel = ttk.Label(self.infoFrame5, text="Search\nReward\t")
            self.rewardSearchLabel.grid(column=0, row=3, padx=5, pady=5)
            self.rewardSearchEntry = tk.Text(self.infoFrame5, width=17, height=2)
            self.rewardSearchEntry.bind("<KeyRelease>", self.handle_wait)
            self.rewardSearchEntry.grid(column=1, row=3, padx=5, pady=5, sticky=tk.W)
            
            self.rewardDrawLabel = ttk.Label(self.infoFrame5, text="Draw\nReward\t")
            self.rewardDrawLabel.grid(column=0, row=4, padx=5, pady=5)
            self.rewardDrawEntry = tk.Text(self.infoFrame5, width=17, height=2)
            self.rewardDrawEntry.bind("<KeyRelease>", self.handle_wait)
            self.rewardDrawEntry.grid(column=1, row=4, padx=5, pady=5, sticky=tk.W)
            
            self.rewardRefreshLabel = ttk.Label(self.infoFrame5, text="Refresh\nReward\t")
            self.rewardRefreshLabel.grid(column=0, row=5, padx=5, pady=5)
            self.rewardRefreshEntry = tk.Text(self.infoFrame5, width=17, height=2)
            self.rewardRefreshEntry.bind("<KeyRelease>", self.handle_wait)
            self.rewardRefreshEntry.grid(column=1, row=5, padx=5, pady=5, sticky=tk.W)
            
            self.rewardTrialLabel = ttk.Label(self.infoFrame5, text="Trial\nReward\t")
            self.rewardTrialLabel.grid(column=0, row=6, padx=5, pady=5)
            self.rewardTrialEntry = tk.Text(self.infoFrame5, width=17, height=2)
            self.rewardTrialEntry.bind("<KeyRelease>", self.handle_wait)
            self.rewardTrialEntry.grid(column=1, row=6, padx=5, pady=5, sticky=tk.W)
            
            self.keywordsLabel = ttk.Label(self.infoFrame5, text="Keywords")
            self.keywordsLabel.grid(column=2, row=2, padx=(24, 5), pady=5, sticky=tk.NW)
            self.keywordsEntry = tk.Text(self.infoFrame5, width=39, height=3)
            self.keywordsEntry.bind("<KeyRelease>", self.handle_wait)
            self.keywordsEntry.grid(column=3, row=2, pady=5, columnspan=2, sticky=tk.W)
            
            self.specialRulesLabel = ttk.Label(self.infoFrame5, text="Special\nRules")
            self.specialRulesLabel.grid(column=2, row=3, padx=(24, 5), pady=5, sticky=tk.NW)
            self.specialRulesEntry = tk.Text(self.infoFrame5, width=39, height=12)
            self.specialRulesEntry.bind("<KeyRelease>", self.handle_wait)
            self.specialRulesEntry.grid(column=3, row=3, pady=5, rowspan=4, columnspan=2, sticky=tk.W)
            
            self.numberOfTilesLabel = ttk.Label(self.infoFrame6, text="Number\nof Tiles")
            self.numberOfTilesLabel.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            self.numberOfTilesMenuList = ["1", "2", "3"]
            self.numberOfTilesMenuVal = tk.StringVar()
            self.numberOfTilesMenuVal.set(self.numberOfTilesMenuList[0])
            self.previousNumberOfTilesMenuVal = ""
            self.numberOfTilesMenu = ttk.Combobox(self.infoFrame6, width=5, state="readonly", values=self.numberOfTilesMenuList, textvariable=self.numberOfTilesMenuVal)
            self.numberOfTilesMenu.bind("<<ComboboxSelected>>", self.update_lists)
            self.numberOfTilesMenu.unbind_class("TCombobox", "<MouseWheel>")
            self.numberOfTilesMenu.unbind_class("TCombobox", "<ButtonPress-4>")
            self.numberOfTilesMenu.unbind_class("TCombobox", "<ButtonPress-5>")
            self.numberOfTilesMenu.pack(side=tk.LEFT, anchor=tk.W, padx=(11, 5), pady=5)
            
            self.tileLayoutLabel = ttk.Label(self.infoFrame6, text="\t          Tile\n\t          Layout")
            self.tileLayoutLabel.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            self.tileLayoutMenuList = []
            self.tileLayoutMenuVal = tk.StringVar()
            self.tileLayoutMenu = ttk.Combobox(self.infoFrame6, width=30, state="readonly", values=self.tileLayoutMenuList, textvariable=self.tileLayoutMenuVal)
            self.previousTileLayoutMenuVal = ""
            self.tileLayoutMenu.bind("<KeyRelease>", self.search_layout_combobox)
            self.tileLayoutMenu.bind("<<ComboboxSelected>>", self.update_lists)
            self.tileLayoutMenu.unbind_class("TCombobox", "<MouseWheel>")
            self.tileLayoutMenu.unbind_class("TCombobox", "<ButtonPress-4>")
            self.tileLayoutMenu.unbind_class("TCombobox", "<ButtonPress-5>")
            self.tileLayoutMenu.pack(side=tk.LEFT, anchor=tk.W, padx=18, pady=5)

            self.tileSelections = {}
            
            for tile in range(1, 4):
                if tile == 1:
                    frame = self.tileFrame1
                elif tile == 2:
                    frame = self.tileFrame2
                elif tile == 3:
                    frame = self.tileFrame3

                self.tileSelections[tile] = {
                    "label": ttk.Label(frame, text=(" " * 46) + "Tile " + str(tile), font=("Arial", 16)),
                    "traps": {"value": tk.IntVar()},
                    "startingTile": {"value": tk.IntVar()},
                    "startingNodesLabel": ttk.Label(frame, text="\tStarting\n\tNodes\t"),
                    "startingNodes": {"value": tk.StringVar()},
                    "terrainLabel": ttk.Label(frame, text="Terrain")
                }

                self.tileSelections[tile]["traps"]["widget"] = ttk.Checkbutton(frame, text="Traps", variable=self.tileSelections[tile]["traps"]["value"], command=self.topFrame.apply_changes)
                self.tileSelections[tile]["startingTile"]["widget"] = ttk.Checkbutton(frame, text="Starting\nTile", variable=self.tileSelections[tile]["startingTile"]["value"], command=lambda x=tile: self.toggle_starting_nodes_menu(tile=x))
                self.tileSelections[tile]["startingNodes"]["widget"] = ttk.Combobox(frame, state="readonly", values=self.startingNodesMenuList, textvariable=self.tileSelections[tile]["startingNodes"]["value"])
                self.tileSelections[tile]["startingNodes"]["widget"].bind("<<ComboboxSelected>>", self.topFrame.apply_changes)
                self.tileSelections[tile]["startingNodes"]["widget"].unbind_class("TCombobox", "<MouseWheel>")
                self.tileSelections[tile]["startingNodes"]["widget"].unbind_class("TCombobox", "<ButtonPress-4>")
                self.tileSelections[tile]["startingNodes"]["widget"].unbind_class("TCombobox", "<ButtonPress-5>")
                
                self.tileSelections[tile]["traps"]["widget"].state(["!alternate"])
                self.tileSelections[tile]["startingTile"]["widget"].state(["!alternate"])
                self.tileSelections[tile]["startingNodes"]["widget"].config(width=8)
                
                for row in range(1, 5):
                    if tile > 1 and row > 2:
                        continue

                    self.tileSelections[tile][row] = {
                        "enemyLabel": ttk.Label(frame, text="Enemies Row " + str(row) + "\t"),
                        "enemies": {
                            1: {"value": tk.StringVar()},
                            2: {"value": tk.StringVar()},
                            3: {"value": tk.StringVar()}
                        },
                        "terrain": {"value": tk.StringVar()}
                    }

                    for x in range(1, 4):
                        self.tileSelections[tile][row]["enemies"][x]["widget"] = ttk.Combobox(frame, height=int(28 * (self.root.winfo_screenheight() / 1080)), width=25, values=self.eNames, textvariable=self.tileSelections[tile][row]["enemies"][x]["value"])
                        self.tileSelections[tile][row]["enemies"][x]["widget"].set("")
                        self.tileSelections[tile][row]["enemies"][x]["widget"].bind("<KeyRelease>", self.search_enemy_combobox)
                        self.tileSelections[tile][row]["enemies"][x]["widget"].bind("<<ComboboxSelected>>", self.topFrame.apply_changes)
                        self.tileSelections[tile][row]["enemies"][x]["widget"].unbind_class("TCombobox", "<MouseWheel>")
                        self.tileSelections[tile][row]["enemies"][x]["widget"].unbind_class("TCombobox", "<ButtonPress-4>")
                        self.tileSelections[tile][row]["enemies"][x]["widget"].unbind_class("TCombobox", "<ButtonPress-5>")

                    self.tileSelections[tile][row]["terrain"]["widget"] = ttk.Combobox(frame, height=int(28 * (self.root.winfo_screenheight() / 1080)) if len(self.terrainNames) > int(28 * (self.root.winfo_screenheight() / 1080)) else len(self.terrainNames), width=15, values=self.terrainNames, textvariable=self.tileSelections[tile][row]["terrain"]["value"])
                    self.tileSelections[tile][row]["terrain"]["widget"].set("")
                    self.tileSelections[tile][row]["terrain"]["widget"].bind("<KeyRelease>", self.search_terrain_combobox)
                    self.tileSelections[tile][row]["terrain"]["widget"].bind("<<ComboboxSelected>>", self.topFrame.apply_changes)
                    self.tileSelections[tile][row]["terrain"]["widget"].unbind_class("TCombobox", "<MouseWheel>")
                    self.tileSelections[tile][row]["terrain"]["widget"].unbind_class("TCombobox", "<ButtonPress-4>")
                    self.tileSelections[tile][row]["terrain"]["widget"].unbind_class("TCombobox", "<ButtonPress-5>")
                    
            self.tileSelections[1]["label"].grid(column=0, row=0, padx=5, pady=5, sticky=tk.W, columnspan=4)
            self.tileSelections[1]["traps"]["widget"].grid(column=1, row=1, pady=5)
            self.tileSelections[1]["startingTile"]["widget"].grid(column=2, row=1, pady=5, sticky=tk.W)
            self.tileSelections[1][1]["enemyLabel"].grid(column=0, row=2, padx=5, pady=5, columnspan=2)
            self.tileSelections[1][1]["enemies"][1]["widget"].grid(column=0, row=3, padx=5, pady=5, columnspan=2)
            self.tileSelections[1][1]["enemies"][2]["widget"].grid(column=0, row=4, padx=5, pady=5, columnspan=2)
            self.tileSelections[1][1]["enemies"][3]["widget"].grid(column=0, row=5, padx=5, pady=5, columnspan=2)
            self.tileSelections[1][2]["enemyLabel"].grid(column=2, row=2, padx=5, pady=5, columnspan=2)
            self.tileSelections[1][2]["enemies"][1]["widget"].grid(column=2, row=3, padx=5, pady=5, columnspan=2)
            self.tileSelections[1][2]["enemies"][2]["widget"].grid(column=2, row=4, padx=5, pady=5, columnspan=2)
            self.tileSelections[1][2]["enemies"][3]["widget"].grid(column=2, row=5, padx=5, pady=5, columnspan=2)
            self.tileSelections[1]["terrainLabel"].grid(column=4, row=2, padx=5, pady=5, sticky=tk.W, columnspan=2)
            self.tileSelections[1][1]["terrain"]["widget"].grid(column=4, row=3, padx=5, pady=5, columnspan=2, sticky=tk.W)
            self.tileSelections[1][2]["terrain"]["widget"].grid(column=4, row=4, padx=5, pady=5, columnspan=2, sticky=tk.W)

            self.tileSelections[2]["label"].grid(column=0, row=0, padx=5, pady=5, sticky=tk.W, columnspan=4)
            self.tileSelections[3]["label"].grid(column=0, row=0, padx=5, pady=5, sticky=tk.W, columnspan=4)

            self.icons = {}
            self.currentIcon = {
                "label": None,
                "file": None,
                "image": None,
                "photoImage": None,
                "size": None,
                "position": None
            }
            
            self.iconTitle = ttk.Label(self.iconsFrame, text=(" " * 40) + "Custom Icons", font=("Arial", 16))
            self.iconTitle.grid(column=0, row=0, padx=5, pady=5, columnspan=6, sticky=tk.W)
            self.iconWarningLabel = ttk.Label(self.iconsFrame, text="Please check the wiki for details on how to use custom icons!")
            self.iconWarningLabel.grid(column=0, row=1, padx=5, pady=5, columnspan=6, sticky=tk.W)
            self.iconLabel = ttk.Label(self.iconsFrame, text="Custom Icons\t")
            self.iconLabel.grid(column=0, row=2, padx=5, pady=5)
            self.iconMenuList = []
            self.iconMenuVal = tk.StringVar()
            self.iconMenu = ttk.Combobox(self.iconsFrame, width=24, state="readonly", values=self.iconMenuList, textvariable=self.iconMenuVal)
            self.iconMenu.bind("<<ComboboxSelected>>", self.change_icon)
            self.iconMenu.unbind_class("TCombobox", "<MouseWheel>")
            self.iconMenu.unbind_class("TCombobox", "<ButtonPress-4>")
            self.iconMenu.unbind_class("TCombobox", "<ButtonPress-5>")
            self.iconMenu.grid(column=1, row=2, padx=5, pady=5, columnspan=4, sticky=tk.W)
            self.deleteIconButton = ttk.Button(self.iconsFrame, text="Delete Icon", width=16, command=self.delete_custom_icon)
            self.deleteIconButton.grid(column=5, row=2, padx=(5, 0), pady=5)
            
            self.iconNameLabel = ttk.Label(self.iconsFrame, text="Icon Name\t")
            self.iconNameLabel.grid(column=0, row=3, padx=5, pady=5)
            self.iconNameEntry = tk.Text(self.iconsFrame, width=25, height=1)
            self.iconNameEntry.grid(column=1, row=3, padx=5, pady=5, columnspan=4)
            self.saveIconButton = ttk.Button(self.iconsFrame, text="Save Icon", width=16, command=self.save_custom_icon)
            self.saveIconButton.grid(column=5, row=3, padx=(5, 0), pady=5)
            self.iconSaveErrorsVal = tk.StringVar()
            self.iconSaveErrors = tk.Label(self.iconsFrame, width=26, height=2, textvariable=self.iconSaveErrorsVal)
            self.iconSaveErrors.grid(column=6, row=3, pady=5, sticky=tk.W)
            
            self.iconSizeLabel = ttk.Label(self.iconsFrame, text="Icon Size\t")
            self.iconSizeLabel.grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)
            self.iconSizeMenuList = ["Text", "Enemy/Terrain", "Set Icon"]
            self.iconSizeMenuVal = tk.StringVar()
            self.iconSizeMenu = ttk.Combobox(self.iconsFrame, width=24, state="readonly", values=self.iconSizeMenuList, textvariable=self.iconSizeMenuVal)
            self.iconSizeMenu.unbind_class("TCombobox", "<MouseWheel>")
            self.iconSizeMenu.unbind_class("TCombobox", "<ButtonPress-4>")
            self.iconSizeMenu.unbind_class("TCombobox", "<ButtonPress-5>")
            self.iconSizeMenu.grid(column=1, row=4, padx=5, pady=5, columnspan=4, sticky=tk.W)
            self.chooseIconButton = ttk.Button(self.iconsFrame, text="Choose Image", width=16, command=self.choose_icon_image)
            self.chooseIconButton.grid(column=5, row=4, padx=(5, 0), pady=5)
            self.iconImageErrorsVal = tk.StringVar()
            self.iconImageErrors = tk.Label(self.iconsFrame, width=26, height=2, textvariable=self.iconImageErrorsVal)
            self.iconImageErrors.grid(column=6, row=4, pady=5, rowspan=2, sticky=tk.NW)
            
            vcmdX = (self.register(self.callback_x))
            vcmdY = (self.register(self.callback_y))
            self.positionLabel = ttk.Label(self.iconsFrame, text="Position\t")
            self.positionLabel.grid(column=0, row=5, padx=5, pady=5, sticky=tk.W)
            self.xPositionLabel = ttk.Label(self.iconsFrame, text="\nx:\n0-400")
            self.xPositionLabel.grid(column=1, row=5, padx=5, pady=5, sticky=tk.W)
            self.xPositionVal = tk.StringVar()
            self.xPositionEntry = ttk.Entry(self.iconsFrame, textvariable=self.xPositionVal, width=4, validate="all", validatecommand=(vcmdX, "%P"))
            self.xPositionEntry.grid(column=2, row=5, padx=5, pady=5, sticky=tk.W)
            self.yPositionLabel = ttk.Label(self.iconsFrame, text="\ny:\n0-685")
            self.yPositionLabel.grid(column=3, row=5, padx=5, pady=5, sticky=tk.E)
            self.yPositionVal = tk.StringVar()
            self.yPositionEntry = ttk.Entry(self.iconsFrame, textvariable=self.yPositionVal, width=4, validate="all", validatecommand=(vcmdY, "%P"))
            self.yPositionEntry.grid(column=4, row=5, padx=5, pady=5, sticky=tk.E)
            self.iconView = tk.Label(self.iconsFrame, width=30, height=2)
            self.iconView.grid(column=5, row=5, pady=5, sticky=tk.NSEW)


        def handle_wait(self, event):
            # cancel the old job
            if self._afterId is not None:
                self.after_cancel(self._afterId)

            # create a new job
            self.after(1, self.topFrame.apply_changes())


        def search_layout_combobox(self, event):
            try:
                log("Start of search_layout_combobox")

                w = event.widget
                val = w.get()
                if val == "":
                    w["values"] = self.tileLayoutMenuList
                else:
                    w["values"] = [e for e in self.tileLayoutMenuList if val.lower() in e.lower()]
                
                log("End of search_layout_combobox")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def search_enemy_combobox(self, event):
            try:
                log("Start of search_enemy_combobox, variant")

                w = event.widget
                val = w.get()
                if val == "" or "--" in val:
                    w["values"] = self.eNames
                else:
                    w["values"] = sorted(list(set([e for e in self.eNames if val.lower() in e.lower() or (e in self.eNamesDict and val.lower() in self.eNamesDict[e].lower())])))
                
                log("End of search_enemy_combobox")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def search_terrain_combobox(self, event):
            try:
                log("Start of search_terrain_combobox")

                w = event.widget
                val = w.get()
                if val == "":
                    w["values"] = self.terrainNames
                else:
                    w["values"] = [e for e in self.terrainNames if val.lower() in e.lower()]
                
                log("End of search_terrain_combobox")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def update_lists(self, event=None):
            try:
                log("Start of update_lists")

                tiles = self.numberOfTilesMenu.get()
                level = self.levelMenu.get()
                layout = self.tileLayoutMenu.get()
                if self.previousNumberOfTilesMenuVal != tiles:
                    self.update_tile_layout_list(tiles)
                    self.update_tile_sections(tiles)
                elif self.previousLevelMenuVal != level or (level == "4" and layout != self.previousTileLayoutMenuVal):
                    self.update_tile_sections(tiles)
                self.previousNumberOfTilesMenuVal = tiles
                self.previousLevelMenuVal = level
                self.previousTileLayoutMenuVal = layout

                self.topFrame.apply_changes()
                
                log("End of update_lists")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def update_tile_layout_list(self, tiles):
            try:
                log("Start of update_tile_layout_list, tiles={}".format(str(tiles)))

                self.tileLayoutMenuList = [k for k in self.app.tileLayouts.keys() if tiles + " Tile" in k]
                self.tileLayoutMenu.config(values=self.tileLayoutMenuList)
                self.tileLayoutMenu.set(self.tileLayoutMenuList[0])
                
                log("End of update_tile_layout_list")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def update_tile_sections(self, tiles):
            try:
                log("Start of update_tile_sections, tiles={}".format(str(tiles)))

                layout = self.tileLayoutMenu.get()

                if layout == "1 Tile 4x4" and not self.tileSelections[1][3]["enemyLabel"].winfo_viewable():
                    self.tileSelections[1][3]["enemyLabel"].grid(column=0, row=6, padx=5, pady=5)
                    self.tileSelections[1][3]["enemies"][1]["widget"].grid(column=0, row=7, padx=5, pady=5)
                    self.tileSelections[1][3]["enemies"][2]["widget"].grid(column=0, row=8, padx=5, pady=5)
                    self.tileSelections[1][3]["enemies"][3]["widget"].grid(column=0, row=9, padx=5, pady=5)
                    self.tileSelections[1][4]["enemyLabel"].grid(column=1, row=6, padx=5, pady=5, columnspan=2)
                    self.tileSelections[1][4]["enemies"][1]["widget"].grid(column=1, row=7, padx=5, pady=5, columnspan=2)
                    self.tileSelections[1][4]["enemies"][2]["widget"].grid(column=1, row=8, padx=5, pady=5, columnspan=2)
                    self.tileSelections[1][4]["enemies"][3]["widget"].grid(column=1, row=9, padx=5, pady=5, columnspan=2)
                    self.tileSelections[1][3]["terrain"]["widget"].grid(column=3, row=5, padx=5, pady=5)
                    self.tileSelections[1][4]["terrain"]["widget"].grid(column=3, row=6, padx=5, pady=5)
                else:
                    self.tileSelections[1][3]["enemyLabel"].grid_forget()
                    self.tileSelections[1][3]["enemies"][1]["widget"].grid_forget()
                    self.tileSelections[1][3]["enemies"][2]["widget"].grid_forget()
                    self.tileSelections[1][3]["enemies"][3]["widget"].grid_forget()
                    self.tileSelections[1][4]["enemyLabel"].grid_forget()
                    self.tileSelections[1][4]["enemies"][1]["widget"].grid_forget()
                    self.tileSelections[1][4]["enemies"][2]["widget"].grid_forget()
                    self.tileSelections[1][4]["enemies"][3]["widget"].grid_forget()
                    self.tileSelections[1][3]["terrain"]["widget"].grid_forget()
                    self.tileSelections[1][4]["terrain"]["widget"].grid_forget()
                    
                if int(tiles) > 1 and not self.tileSelections[2]["traps"]["widget"].winfo_viewable():
                    self.tileSelections[2]["traps"]["widget"].grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
                    self.tileSelections[2]["startingTile"]["widget"].grid(column=1, row=1, padx=(40, 5), pady=5)
                    self.tileSelections[2]["startingNodesLabel"].grid(column=2, row=1, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections[2]["startingNodes"]["widget"].grid(column=3, row=1, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections[2][1]["enemyLabel"].grid(column=0, row=2, padx=5, pady=5)
                    self.tileSelections[2][1]["enemies"][1]["widget"].grid(column=0, row=3, padx=5, pady=5)
                    self.tileSelections[2][1]["enemies"][2]["widget"].grid(column=0, row=4, padx=5, pady=5)
                    self.tileSelections[2][1]["enemies"][3]["widget"].grid(column=0, row=5, padx=5, pady=5)
                    self.tileSelections[2][2]["enemyLabel"].grid(column=1, row=2, padx=5, pady=5, columnspan=2)
                    self.tileSelections[2][2]["enemies"][1]["widget"].grid(column=1, row=3, padx=5, pady=5, columnspan=2)
                    self.tileSelections[2][2]["enemies"][2]["widget"].grid(column=1, row=4, padx=5, pady=5, columnspan=2)
                    self.tileSelections[2][2]["enemies"][3]["widget"].grid(column=1, row=5, padx=5, pady=5, columnspan=2)
                    self.tileSelections[2]["terrainLabel"].grid(column=3, row=2, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections[2][1]["terrain"]["widget"].grid(column=3, row=3, padx=5, pady=5)
                    self.tileSelections[2][2]["terrain"]["widget"].grid(column=3, row=4, padx=5, pady=5)
                else:
                    self.tileSelections[2]["traps"]["widget"].grid_forget()
                    self.tileSelections[2]["startingTile"]["widget"].grid_forget()
                    self.tileSelections[2]["startingNodesLabel"].grid_forget()
                    self.tileSelections[2]["startingNodes"]["widget"].grid_forget()
                    self.tileSelections[2][1]["enemyLabel"].grid_forget()
                    self.tileSelections[2][1]["enemies"][1]["widget"].grid_forget()
                    self.tileSelections[2][1]["enemies"][2]["widget"].grid_forget()
                    self.tileSelections[2][1]["enemies"][3]["widget"].grid_forget()
                    self.tileSelections[2][2]["enemyLabel"].grid_forget()
                    self.tileSelections[2][2]["enemies"][1]["widget"].grid_forget()
                    self.tileSelections[2][2]["enemies"][2]["widget"].grid_forget()
                    self.tileSelections[2][2]["enemies"][3]["widget"].grid_forget()
                    self.tileSelections[2]["terrainLabel"].grid_forget()
                    self.tileSelections[2][1]["terrain"]["widget"].grid_forget()
                    self.tileSelections[2][2]["terrain"]["widget"].grid_forget()

                if int(tiles) > 2 and not self.tileSelections[3]["traps"]["widget"].winfo_viewable():
                    self.tileSelections[3]["traps"]["widget"].grid(column=0, row=1, padx=5, pady=5, sticky=tk.E)
                    self.tileSelections[3]["startingTile"]["widget"].grid(column=1, row=1, padx=(40, 5), pady=5)
                    self.tileSelections[3]["startingNodesLabel"].grid(column=2, row=1, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections[3]["startingNodes"]["widget"].grid(column=3, row=1, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections[3][1]["enemyLabel"].grid(column=0, row=2, padx=5, pady=5)
                    self.tileSelections[3][1]["enemies"][1]["widget"].grid(column=0, row=3, padx=5, pady=5)
                    self.tileSelections[3][1]["enemies"][2]["widget"].grid(column=0, row=4, padx=5, pady=5)
                    self.tileSelections[3][1]["enemies"][3]["widget"].grid(column=0, row=5, padx=5, pady=5)
                    self.tileSelections[3][2]["enemyLabel"].grid(column=1, row=2, padx=5, pady=5, columnspan=2)
                    self.tileSelections[3][2]["enemies"][1]["widget"].grid(column=1, row=3, padx=5, pady=5, columnspan=2)
                    self.tileSelections[3][2]["enemies"][2]["widget"].grid(column=1, row=4, padx=5, pady=5, columnspan=2)
                    self.tileSelections[3][2]["enemies"][3]["widget"].grid(column=1, row=5, padx=5, pady=5, columnspan=2)
                    self.tileSelections[3]["terrainLabel"].grid(column=3, row=2, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections[3][1]["terrain"]["widget"].grid(column=3, row=3, padx=5, pady=5)
                    self.tileSelections[3][2]["terrain"]["widget"].grid(column=3, row=4, padx=5, pady=5)
                else:
                    self.tileSelections[3]["traps"]["widget"].grid_forget()
                    self.tileSelections[3]["startingTile"]["widget"].grid_forget()
                    self.tileSelections[3]["startingNodesLabel"].grid_forget()
                    self.tileSelections[3]["startingNodes"]["widget"].grid_forget()
                    self.tileSelections[3][1]["enemyLabel"].grid_forget()
                    self.tileSelections[3][1]["enemies"][1]["widget"].grid_forget()
                    self.tileSelections[3][1]["enemies"][2]["widget"].grid_forget()
                    self.tileSelections[3][1]["enemies"][3]["widget"].grid_forget()
                    self.tileSelections[3][2]["enemyLabel"].grid_forget()
                    self.tileSelections[3][2]["enemies"][1]["widget"].grid_forget()
                    self.tileSelections[3][2]["enemies"][2]["widget"].grid_forget()
                    self.tileSelections[3][2]["enemies"][3]["widget"].grid_forget()
                    self.tileSelections[3]["terrainLabel"].grid_forget()
                    self.tileSelections[3][1]["terrain"]["widget"].grid_forget()
                    self.tileSelections[3][2]["terrain"]["widget"].grid_forget()
                
                log("End of update_tile_sections")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def toggle_starting_nodes_menu(self, tile, event=None):
            try:
                log("Start of toggle_starting_nodes_menu, tile={}".format(str(tile)))

                if self.tileSelections[tile]["startingTile"]["value"].get() == 1:
                    self.tileSelections[tile]["startingNodesLabel"].grid(column=3, row=1, pady=5, sticky=tk.W)
                    self.tileSelections[tile]["startingNodes"]["widget"].grid(column=4, row=1, pady=5, sticky=tk.W)
                else:
                    self.tileSelections[tile]["startingNodes"]["widget"].grid_forget()
                    self.tileSelections[tile]["startingNodesLabel"].grid_forget()

                self.topFrame.apply_changes()
                
                log("End of toggle_starting_nodes_menu")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def change_icon(self, event=None):
            try:
                log("Start of change_icon")

                icon = self.iconMenu.get()

                if not icon:
                    log("End of change_icon")
                    return

                if self.icons[icon]["size"] == "iconEnemy":
                    size = "Enemy/Terrain"
                elif self.icons[icon]["size"] == "iconText":
                    size = "Text"
                elif self.icons[icon]["size"] == "iconSet":
                    size = "Set Icon"

                self.currentIcon = {
                    "label": icon,
                    "file": self.icons[icon]["file"],
                    "size": self.icons[icon]["size"],
                    "position": self.icons[icon]["position"],
                    "image": self.icons[icon]["image"],
                    "photoImage": self.icons[icon]["photoImage"]
                }
                self.iconNameEntry.delete("1.0", tk.END)
                self.iconNameEntry.insert("end-1c", icon)
                self.iconSizeMenuVal.set(size)
                self.iconSizeMenu.set(size)
                self.xPositionVal.set(str(self.currentIcon["position"][0] if self.currentIcon["position"] else ""))
                self.yPositionVal.set(str(self.currentIcon["position"][1] if self.currentIcon["position"] else ""))
                self.choose_icon_image(file=baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + self.currentIcon["file"])
                
                log("End of change_icon")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def delete_custom_icon(self, event=None):
            try:
                log("Start of delete_custom_icon")

                self.iconImageErrorsVal.set("")
                self.iconSaveErrorsVal.set("")
                self.iconSaveErrors.config(image="")
                self.iconSaveErrors.image = None
                if self.currentIcon["label"] in self.icons:
                    del self.icons[self.currentIcon["label"]]
                    self.iconMenuList.remove(self.currentIcon["label"])
                    self.iconMenuVal.set("")
                self.currentIcon = {
                    "label": None,
                    "file": None,
                    "image": None,
                    "photoImage": None,
                    "size": None,
                    "position": None
                }
                self.iconMenu.config(values=self.iconMenuList)
                self.iconMenu.set("")
                
                log("End of delete_custom_icon")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def save_custom_icon(self, event=None):
            try:
                log("Start of save_custom_icon")

                errors = []
                noImage = False
                icon = self.iconNameEntry.get("1.0", "end").strip()

                if not icon:
                    errors.append("name")
                if not self.currentIcon["size"]:
                    errors.append("size")
                if not self.currentIcon["image"]:
                    noImage = True

                if errors:
                    errorText = "Required:" + (" image" if noImage else "") + "\n" + ", ".join(errors)
                    self.iconSaveErrorsVal.set(errorText)
                    return

                self.iconSaveErrorsVal.set("")

                self.currentIcon["label"] = icon
                
                if icon and icon not in self.icons:
                    self.iconMenuList.append(icon)
                    self.iconMenu.config(values=self.iconMenuList)
                    self.iconMenu.set(self.iconMenuList[-1])
                    
                self.icons[icon] = {
                    "label": icon,
                    "size": deepcopy(self.currentIcon["size"]),
                    "position": (self.xPositionEntry.get(), self.yPositionEntry.get()),
                    "file": deepcopy(self.currentIcon["file"])
                    }

                self.icons[icon]["image"], self.icons[icon]["photoImage"] = self.app.create_image(baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + self.currentIcon["file"], self.currentIcon["size"], 99, pathProvided=True, extensionProvided=True)
                
                self.topFrame.customEncounter["icons"] = {k: v for k, v in self.icons.items() if "" not in self.icons[k]["position"]}

                self.topFrame.apply_changes()

                self.iconSaveErrorsVal.set("Saved " + datetime.now().strftime("%H:%M:%S"))

                log("End of save_custom_icon")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def choose_icon_image(self, event=None, file=None):
            """
            Create a label and tooltip that will be placed and later removed.
            """
            try:
                log("Start of choose_icon_image, file={}".format(str(file)))

                errors = []

                if self.iconSizeMenu.get() not in {"Enemy/Terrain", "Text", "Set Icon"}:
                    errors.append("size")

                if errors:
                    self.iconView.config(image="")
                    self.iconView.image=None
                    errorText = "Required:\n" + ", ".join(errors)
                    self.iconImageErrorsVal.set(errorText)
                    return

                self.iconImageErrorsVal.set("")

                if self.iconSizeMenu.get() == "Enemy/Terrain":
                    size = "iconEnemy"
                elif self.iconSizeMenu.get() == "Text":
                    size = "iconText"
                elif self.iconSizeMenu.get() == "Set Icon":
                    size = "iconSet"
                
                if not file:
                    file = filedialog.askopenfilename(initialdir=baseFolder)

                    # If they canceled, do nothing.
                    if not file:
                        return
                    
                    fileName = path.splitext(path.basename(file))
                    newFile = baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + fileName[0] + "_" + size + ".png"
                    if not path.isfile(newFile):
                        i, p = self.app.create_image(file, size, 99, pathProvided=True, extensionProvided=True)
                        i.save(newFile)
                    else:
                        i, p = self.app.create_image(newFile, size, 99, pathProvided=True, extensionProvided=True)
                    file = newFile
                else:
                    i, p = self.app.create_image(file, size, 99, pathProvided=True, extensionProvided=True)

                self.currentIcon["size"] = size
                self.currentIcon["file"] = path.splitext(path.basename(file))[0] + ".png"
                self.currentIcon["image"] = i
                self.currentIcon["photoImage"] = p

                self.iconView.config(image=p)
                self.iconView.image=p

                log("\tEnd of choose_icon_image")
            except UnidentifiedImageError:
                # Handling for this occurred in create_image.
                return
            except EnvironmentError as err:
                if err.errno == errno.ENOENT: # ENOENT -> "no entity" -> "file not found"
                    # Handling for this occurred in create_image.
                    return
                else:
                    raise
            except Exception as e:
                error_popup(self.root, e)
                raise


        def callback_x(self, P):
            """
            Validates whether the input for x coordinate is an integer in range.
            """
            try:
                log("Start of callback_x")

                if (str.isdigit(P) and int(P) <= 400) or str(P) == "":
                    log("End of callback_x")
                    return True
                else:
                    log("End of callback_x")
                    return False
            except Exception as e:
                error_popup(self.root, e)
                raise


        def callback_y(self, P):
            """
            Validates whether the input for y coordinate is an integer in range.
            """
            try:
                log("Start of callback_y")

                if (str.isdigit(P) and int(P) <= 685) or str(P) == "":
                    log("End of callback_y")
                    return True
                else:
                    log("End of callback_y")
                    return False
            except Exception as e:
                error_popup(self.root, e)
                raise

except Exception as e:
    log(e, exception=True)
    raise