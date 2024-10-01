try:
    import errno
    import tkinter as tk
    from bisect import bisect_left
    from copy import deepcopy
    from datetime import datetime
    from json import dump, load
    from os import path
    from PIL import ImageTk, ImageDraw, UnidentifiedImageError
    from tkinter import filedialog, ttk

    from dsbg_shuffle_enemies import enemiesDict
    from dsbg_shuffle_utility import PopupWindow, VerticalScrolledFrame, clear_other_tab_images, error_popup, log, baseFolder, font, fontSize11, fontSize10, fontEncounterName, fontFlavor, pathSep


    class EncounterBuilderFrame(ttk.Frame):
        def __init__(self, app, root):
            super(EncounterBuilderFrame, self).__init__()
            self.app = app
            self.root = root

            self.customEncounter = {}
            self.bind("<1>", lambda event: event.widget.focus_set())

            self.customEncountersButtonFrame = ttk.Frame(self)
            self.customEncountersButtonFrame.bind("<1>", lambda event: event.widget.focus_set())
            self.customEncountersButtonFrame.pack(side=tk.TOP, anchor=tk.W)
            self.separator = ttk.Separator(self)
            self.separator.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")

            self.newEncounterButton = ttk.Button(self.customEncountersButtonFrame, text="New Encounter", width=16, command=self.new_custom_encounter)
            self.newEncounterButton.grid(column=0, row=0, padx=5, pady=5)
            self.loadButton = ttk.Button(self.customEncountersButtonFrame, text="Load Encounter", width=16, command=self.load_custom_encounter)
            self.loadButton.grid(column=1, row=0, padx=5, pady=5)
            self.saveButton = ttk.Button(self.customEncountersButtonFrame, text="Save Encounter", width=16, command=self.save_custom_encounter)
            self.saveButton.grid(column=2, row=0, padx=5, pady=5)
            
            self.encounterSaveLabelVal = tk.StringVar()
            self.encounterSaveLabel = ttk.Label(self.customEncountersButtonFrame, textvariable=self.encounterSaveLabelVal)
            self.encounterSaveLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.encounterSaveLabel.grid(column=3, row=0, padx=5, pady=5)
            
            self.encounterBuilderScroll = EncounterBuilderScrollFrame(root=root, app=app, topFrame=self)
            self.encounterBuilderScroll.pack(side=tk.TOP, anchor=tk.W, expand=True, fill="both")
            
            self.new_custom_encounter()


        def new_custom_encounter(self, event=None):
            try:
                log("Start of new_custom_encounter")

                self.app.selected = None

                e = self.encounterBuilderScroll

                # e.iconMenuVal.set("")
                # e.iconImageErrorsVal.set("")
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
                e.specialRulesTextSizeVal.set(12)
                e.iconNameEntry.delete("1.0", tk.END)

                e.rewardSoulsPerPlayer.state(["!selected"])
                e.shortcut.state(["!selected"])
                e.levelRadioVal.set(1)
                e.numberOfTilesRadioVal.set(1)

                for tile in range(1, 4):
                    e.tileSelections[str(tile)]["traps"]["value"].set(0)
                    e.tileSelections[str(tile)]["startingNodes"]["value"].set(0)
                    for row in range(1, 5):
                        if tile > 1 and row > 2:
                            continue

                        for x in range(1, 4):
                            e.tileSelections[str(tile)][str(row)]["enemies"][str(x)]["widget"].set("")

                        e.tileSelections[str(tile)][str(row)]["terrain"]["widget"].set("")
                
                clear_other_tab_images(self.app, "encounters", "encounters")
                if getattr(self.app, "displayTopLeft", None):
                    self.app.displayImages["encounters"][self.app.displayTopLeft]["image"] = "custom"
                    self.app.displayImages["encounters"][self.app.displayTopLeft]["activeTab"] = "custom"
                    self.app.displayTopLeft.config(image="")
                    self.app.displayTopLeft.image=None

                e.update_lists()
                
                log("End of new_custom_encounter")
            except Exception as e:
                error_popup(self.root, e)
                raise

            
        def apply_changes(self, event=None):
            try:
                if not hasattr(self, "encounterBuilderScroll") or not hasattr(self.app, "encounterTab") or self.app.notebook.tab(self.app.notebook.select(), "text") != "Encounter Builder":
                    return
                
                log("Start of apply_changes")

                e = self.encounterBuilderScroll

                clear_other_tab_images(self.app, "encounters", "encounters")

                self.app.encounterTab.apply_keyword_tooltips(None, None)
                
                if e.numberOfTilesRadioVal.get() == 1 and e.tileLayoutMenu.get() == "1 Tile 4x4" and e.tileSelections["1"]["traps"]["value"].get() == 1:
                    displayPhotoImage = self.app.create_image("custom_encounter_1_tile_4x4_traps.jpg", "customEncounter", 1, extensionProvided=True)
                elif e.numberOfTilesRadioVal.get() == 1 and e.tileLayoutMenu.get() == "1 Tile 4x4":
                    displayPhotoImage = self.app.create_image("custom_encounter_1_tile_4x4_no_traps.jpg", "customEncounter", 1, extensionProvided=True)
                elif e.numberOfTilesRadioVal.get() == 1:
                    displayPhotoImage = self.app.create_image("custom_encounter_1_tile.jpg", "customEncounter", 1, extensionProvided=True)
                elif e.numberOfTilesRadioVal.get() == 2:
                    displayPhotoImage = self.app.create_image("custom_encounter_2_tile.jpg", "customEncounter", 1, extensionProvided=True)
                elif e.numberOfTilesRadioVal.get() == 3:
                    displayPhotoImage = self.app.create_image("custom_encounter_3_tile.jpg", "customEncounter", 1, extensionProvided=True)
                else:
                    return

                imageWithText = ImageDraw.Draw(self.app.displayImage)

                # Empty Set Icon
                if e.emptySetIconVal.get() == 1:
                    self.app.displayImage.paste(im=self.app.emptySetIcon, box=(11, 15), mask=self.app.emptySetIcon)
                
                # Encounter Name
                if e.encounterNameEntry.get("1.0", "end").strip():
                    lines = len(e.encounterNameEntry.get("1.0", "end").strip().split("\n"))
                    for i, substring in enumerate(e.encounterNameEntry.get("1.0", "end").strip().split("\n")):
                        _, _, w, h = imageWithText.textbbox((0, 0), "QJ" + substring, font=fontEncounterName, align="center")
                        imageWithText.text(((432-w)/2, (((108 if lines == 1 else 84)-h)/2) + (i * 26)), substring, font=fontEncounterName, fill="white")
                
                # Flavor Text
                if e.flavorEntry.get("1.0", "end").strip():
                    lines = len(e.flavorEntry.get("1.0", "end").strip().split("\n"))
                    for i, substring in enumerate(e.flavorEntry.get("1.0", "end").strip().split("\n")):
                        _, _, w, h = imageWithText.textbbox((0, 0), "Qq" + substring, font=fontFlavor, align="center")
                        imageWithText.text(((416-w)/2, (((202 if lines == 1 else 190)-h)/2) + (i * 13)), substring, font=fontFlavor, fill="black")
                
                # Objective Text
                imageWithText.text((20, 146), e.objectiveEntry.get("1.0", "end").strip(), "black", font)
                
                # Keywords
                keywords = e.keywordsEntry.get("1.0", "end").strip()
                if keywords:
                    imageWithText.text((141, 195), keywords, "black", fontFlavor)
                    rulesNewlines = 1 + keywords.count("\n")
                else:
                    rulesNewlines = 0
                
                # Special Rules
                specialRules = e.specialRulesEntry.get("1.0", "end").strip()
                if specialRules:
                    if e.specialRulesTextSizeVal.get() == 12:
                        f = font
                        lineMod = 13
                        substringMod = 5
                    elif e.specialRulesTextSizeVal.get() == 11:
                        f = fontSize11
                        lineMod = 12.5
                        substringMod = 4.5
                    elif e.specialRulesTextSizeVal.get() == 10:
                        f = fontSize10
                        lineMod = 12
                        substringMod = 4

                    lineCount = 0
                    for i, substring in enumerate(specialRules.split("\n\n")):
                        imageWithText.text((141, 200 + int(((lineCount if i > 0 else 0) + rulesNewlines) * lineMod) + int(i * substringMod)), substring, "black", f)
                        lineCount += substring.count("\n") + 1

                # Encounter Level
                if e.levelRadioVal.get():
                    self.app.displayImage.paste(im=self.app.levelIcons[int(e.levelRadioVal.get())], box=(328, 15), mask=self.app.levelIcons[int(e.levelRadioVal.get())])

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
                        if e.tileSelections[str(tile)]["startingNodes"]["value"].get():
                            startingNodesLocation = e.tileSelections[str(tile)]["startingNodes"]["value"].get()
                            if tile not in tileLayout["box"]:
                                continue
                            box = tileLayout["box"][tile][startingNodesLocation]
                            if startingNodesLocation in {1, 2}:
                                self.app.displayImage.paste(im=tileLayout["startingNodesHorizontal"], box=box, mask=tileLayout["startingNodesHorizontal"])
                            else:
                                self.app.displayImage.paste(im=tileLayout["startingNodesVertical"], box=box, mask=tileLayout["startingNodesVertical"])
                                
                # Tile numbers and traps
                if e.tileLayoutMenuVal.get() != "1 Tile 4x4":
                    for tile in range(1, 4):
                        if tile > int(e.numberOfTilesRadioVal.get()):
                            continue

                        box = (334, 377 + (122 * (tile - 1)))

                        if e.tileSelections[str(tile)]["startingNodes"]["value"].get() and e.tileSelections[str(tile)]["traps"]["value"].get() == 1:
                            image = self.app.tileNumbers[tile]["starting"]["traps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)
                        elif e.tileSelections[str(tile)]["startingNodes"]["value"].get() and e.tileSelections[str(tile)]["traps"]["value"].get() != 1:
                            image = self.app.tileNumbers[tile]["starting"]["noTraps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)
                        elif not e.tileSelections[str(tile)]["startingNodes"]["value"].get() and e.tileSelections[str(tile)]["traps"]["value"].get() == 1:
                            image = self.app.tileNumbers[tile]["notStarting"]["traps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)
                        elif not e.tileSelections[str(tile)]["startingNodes"]["value"].get() and e.tileSelections[str(tile)]["traps"]["value"].get() != 1:
                            image = self.app.tileNumbers[tile]["notStarting"]["noTraps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)

                # Terrain
                for tile in range(1, int(e.numberOfTilesRadioVal.get()) + 1):
                    for row in range(1, 5 if e.tileLayoutMenu.get() == "1 Tile 4x4" else 3):
                        box = (301, 380 + (29 * (row - 1)) + (122 * (tile - 1)) + (29 if e.levelRadioVal.get() == "4" else 0))
                        if e.tileSelections[str(tile)][str(row)]["terrain"]["value"].get() in self.app.terrain:
                            image = self.app.terrain[e.tileSelections[str(tile)][str(row)]["terrain"]["value"].get()]
                            self.app.displayImage.paste(im=image, box=box, mask=image)

                # Enemies
                for tile in range(1, int(e.numberOfTilesRadioVal.get()) + 1):
                    for row in range(1, 5 if e.tileLayoutMenu.get() == "1 Tile 4x4" else 3):
                        for en in range(1, 4):
                            box = (300 + (29 * (en - 1)), 323 + (29 * (row - 1)) + (122 * (tile - 1)))
                            if e.tileSelections[str(tile)][str(row)]["enemies"][str(en)]["value"].get() in self.app.allEnemies:
                                enemy = e.tileSelections[str(tile)][str(row)]["enemies"][str(en)]["value"].get()
                                image = self.app.allEnemies[enemy]["imageNew"]
                                self.app.displayImage.paste(im=image, box=box, mask=image)

                # # Custom Icons
                # for icon in [icon for icon in e.icons if "" not in e.icons[icon]["position"]]:
                #     image = e.icons[icon]["image"]
                #     box = (int(e.icons[icon]["position"][0]), int(e.icons[icon]["position"][1]))
                #     self.app.displayImage.paste(im=image, box=box, mask=image)

                # self.customEncounter["set"] = e.encounterSetEntry.get("1.0", "end").strip()
                # self.customEncounter["emptySetIcon"] = e.emptySetIconVal.get()
                # self.customEncounter["image"] = self.app.displayImage.copy()
                # self.customEncounter["numberOfTiles"] = e.numberOfTilesRadioVal.get()
                # self.customEncounter["level"] = e.levelRadioVal.get()
                # self.customEncounter["encounterName"] = e.encounterNameEntry.get("1.0", "end").strip()
                # self.customEncounter["flavor"] = e.flavorEntry.get("1.0", "end").strip()
                # self.customEncounter["objective"] = e.objectiveEntry.get("1.0", "end").strip()
                # self.customEncounter["keywords"] = e.keywordsEntry.get("1.0", "end").strip()
                # self.customEncounter["specialRules"] = e.specialRulesEntry.get("1.0", "end").strip()
                # self.customEncounter["specialRulesTextSize"] = e.specialRulesTextSizeVal.get()
                # self.customEncounter["rewardSouls"] = e.rewardSoulsEntry.get("1.0", "end").strip()
                # self.customEncounter["rewardSoulsPerPlayer"] = e.rewardSoulsPerPlayerVal.get()
                # self.customEncounter["rewardSearch"] = e.rewardSearchEntry.get("1.0", "end").strip()
                # self.customEncounter["rewardDraw"] = e.rewardDrawEntry.get("1.0", "end").strip()
                # self.customEncounter["rewardRefresh"] = e.rewardRefreshEntry.get("1.0", "end").strip()
                # self.customEncounter["rewardTrial"] = e.rewardTrialEntry.get("1.0", "end").strip()
                # self.customEncounter["rewardShortcut"] = e.shortcutVal.get()
                # self.customEncounter["layout"] = e.tileLayoutMenuVal.get()
                # self.customEncounter["icons"] = {k: v for k, v in e.icons.items() if "" not in e.icons[k]["position"]}
                # self.customEncounter["tileSelections"] = {
                #     "1": {
                #         "startingNodes": {"value": e.tileSelections["1"]["startingNodes"]["value"].get()},
                #         "traps": {"value": e.tileSelections["1"]["traps"]["value"].get()},
                #         "1": {"terrain": {"value": e.tileSelections["1"]["1"]["terrain"]["value"].get()},
                #             "enemies": {
                #                 "1": {"value": e.tileSelections["1"]["1"]["enemies"]["1"]["value"].get()},
                #                 "2": {"value": e.tileSelections["1"]["1"]["enemies"]["2"]["value"].get()},
                #                 "3": {"value": e.tileSelections["1"]["1"]["enemies"]["3"]["value"].get()}
                #             }},
                #         "2": {"terrain": {"value": e.tileSelections["1"]["2"]["terrain"]["value"].get()},
                #             "enemies": {
                #                 "1": {"value": e.tileSelections["1"]["2"]["enemies"]["1"]["value"].get()},
                #                 "2": {"value": e.tileSelections["1"]["2"]["enemies"]["2"]["value"].get()},
                #                 "3": {"value": e.tileSelections["1"]["2"]["enemies"]["3"]["value"].get()}
                #             }},
                #         "3": {"terrain": {"value": e.tileSelections["1"]["3"]["terrain"]["value"].get()},
                #             "enemies": {
                #                 "1": {"value": e.tileSelections["1"]["3"]["enemies"]["1"]["value"].get()},
                #                 "2": {"value": e.tileSelections["1"]["3"]["enemies"]["2"]["value"].get()},
                #                 "3": {"value": e.tileSelections["1"]["3"]["enemies"]["3"]["value"].get()}
                #             }},
                #         "4": {"terrain": {"value": e.tileSelections["1"]["4"]["terrain"]["value"].get()},
                #             "enemies": {
                #                 "1": {"value": e.tileSelections["1"]["4"]["enemies"]["1"]["value"].get()},
                #                 "2": {"value": e.tileSelections["1"]["4"]["enemies"]["2"]["value"].get()},
                #                 "3": {"value": e.tileSelections["1"]["4"]["enemies"]["3"]["value"].get()}
                #             }}
                #         },
                #     "2": {
                #         "startingNodes": {"value": e.tileSelections["2"]["startingNodes"]["value"].get()},
                #         "traps": {"value": e.tileSelections["2"]["traps"]["value"].get()},
                #         "1": {"terrain": {"value": e.tileSelections["2"]["1"]["terrain"]["value"].get()},
                #             "enemies": {
                #                 "1": {"value": e.tileSelections["2"]["1"]["enemies"]["1"]["value"].get()},
                #                 "2": {"value": e.tileSelections["2"]["1"]["enemies"]["2"]["value"].get()},
                #                 "3": {"value": e.tileSelections["2"]["1"]["enemies"]["3"]["value"].get()}
                #             }},
                #         "2": {"terrain": {"value": e.tileSelections["2"]["2"]["terrain"]["value"].get()},
                #             "enemies": {
                #                 "1": {"value": e.tileSelections["2"]["2"]["enemies"]["1"]["value"].get()},
                #                 "2": {"value": e.tileSelections["2"]["2"]["enemies"]["2"]["value"].get()},
                #                 "3": {"value": e.tileSelections["2"]["2"]["enemies"]["3"]["value"].get()}
                #             }}
                #         },
                #     "3": {
                #         "startingNodes": {"value": e.tileSelections["3"]["startingNodes"]["value"].get()},
                #         "traps": {"value": e.tileSelections["3"]["traps"]["value"].get()},
                #         "1": {"terrain": {"value": e.tileSelections["3"]["1"]["terrain"]["value"].get()},
                #             "enemies": {
                #                 "1": {"value": e.tileSelections["3"]["1"]["enemies"]["1"]["value"].get()},
                #                 "2": {"value": e.tileSelections["3"]["1"]["enemies"]["2"]["value"].get()},
                #                 "3": {"value": e.tileSelections["3"]["1"]["enemies"]["3"]["value"].get()}
                #             }},
                #         "2": {"terrain": {"value": e.tileSelections["3"]["2"]["terrain"]["value"].get()},
                #             "enemies": {
                #                 "1": {"value": e.tileSelections["3"]["2"]["enemies"]["1"]["value"].get()},
                #                 "2": {"value": e.tileSelections["3"]["2"]["enemies"]["2"]["value"].get()},
                #                 "3": {"value": e.tileSelections["3"]["2"]["enemies"]["3"]["value"].get()}
                #             }}
                #         }
                #     }

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

                if not self.customEncounter["set"].strip() or not self.customEncounter["encounterName"].strip():
                    self.encounterSaveLabelVal.set("Set and Name required.")
                    log("End of save_custom_encounter (not saved)")
                    return

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

                self.encounterSaveLabelVal.set("Saved " + datetime.now().strftime("%H:%M:%S"))

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
                
                # Legacy conversion
                if set(self.customEncounter.keys()) == {
                        "set", "objective", "keywords", "rewardSouls", "rewardDraw", "layout", "encounterName",
                        "rewardSoulsPerPlayer", "rewardTrial", "tileSelections", "icons", "rewardSearch",
                        "flavor", "rewardShortcut", "level", "rewardRefresh", "specialRules", "numberOfTiles"}:
                    self.customEncounter["rewardRefresh"] = ""
                    self.customEncounter["emptySetIcon"] = 0
                    self.customEncounter["specialRulesTextSize"] = 12
                    self.customEncounter["encounterScale1"] = 0
                    self.customEncounter["encounterScale2"] = 0
                    self.customEncounter["flavorScale1"] = 0
                    self.customEncounter["flavorScale2"] = 0
                    self.customEncounter["encounterName"] = "\n".join([substring.strip() for substring in self.customEncounter["encounterName"].split("\n")])
                    self.customEncounter["flavor"] = "\n".join([substring.strip() for substring in self.customEncounter["flavor"].split("\n")])
                    for tile in self.customEncounter["tileSelections"]:
                        if "startingTile" in self.customEncounter["tileSelections"][tile]:
                            del self.customEncounter["tileSelections"][tile]["startingTile"]
                        if self.customEncounter["tileSelections"][tile]["startingNodes"]["value"] == "North":
                            self.customEncounter["tileSelections"][tile]["startingNodes"]["value"] = 1
                        elif self.customEncounter["tileSelections"][tile]["startingNodes"]["value"] == "South":
                            self.customEncounter["tileSelections"][tile]["startingNodes"]["value"] = 2
                        elif self.customEncounter["tileSelections"][tile]["startingNodes"]["value"] == "West":
                            self.customEncounter["tileSelections"][tile]["startingNodes"]["value"] = 3
                        elif self.customEncounter["tileSelections"][tile]["startingNodes"]["value"] == "East":
                            self.customEncounter["tileSelections"][tile]["startingNodes"]["value"] = 4
                        else:
                            self.customEncounter["tileSelections"][tile]["startingNodes"]["value"] = 0

                # Check to see if there are any invalid keys in the JSON file.
                # This is about as sure as I can be that you can't load random JSON into the app.
                if set(self.customEncounter.keys()) != {
                        "set", "numberOfTiles", "level", "encounterName", "flavor", "objective", "keywords",
                        "specialRules", "rewardSouls", "rewardSoulsPerPlayer", "rewardSearch", "rewardDraw",
                        "rewardRefresh", "rewardTrial", "rewardShortcut", "layout", "icons", "tileSelections",
                        "emptySetIcon", "specialRulesTextSize"}:
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
                
                self.encounterSaveLabelVal.set("")

                # Need to fill in all the GUI elements.
                e.encounterSetEntry.insert(tk.END, self.customEncounter["set"])
                e.emptySetIconVal.set(self.customEncounter["emptySetIcon"])
                e.numberOfTilesRadioVal.set(self.customEncounter["numberOfTiles"])
                e.levelRadioVal.set(self.customEncounter["level"])
                e.encounterNameEntry.insert(tk.END, self.customEncounter["encounterName"])
                e.encounterScale1Val.set(self.customEncounter["encounterScale1"])
                e.encounterScale2Val.set(self.customEncounter["encounterScale2"])
                e.flavorEntry.insert(tk.END, self.customEncounter["flavor"])
                e.flavorScale1Val.set(self.customEncounter["flavorScale1"])
                e.flavorScale2Val.set(self.customEncounter["flavorScale2"])
                e.objectiveEntry.insert(tk.END, self.customEncounter["objective"])
                e.keywordsEntry.insert(tk.END, self.customEncounter["keywords"])
                e.specialRulesEntry.insert(tk.END, self.customEncounter["specialRules"])
                e.specialRulesTextSizeVal.set(self.customEncounter["specialRulesTextSize"])
                e.rewardSoulsEntry.insert(tk.END, self.customEncounter["rewardSouls"])
                e.rewardSoulsPerPlayerVal.set(self.customEncounter["rewardSoulsPerPlayer"])
                e.rewardSearchEntry.insert(tk.END, self.customEncounter["rewardSearch"])
                e.rewardDrawEntry.insert(tk.END, self.customEncounter["rewardDraw"])
                e.rewardRefreshEntry.insert(tk.END, self.customEncounter["rewardRefresh"])
                e.rewardTrialEntry.insert(tk.END, self.customEncounter["rewardTrial"])
                e.shortcutVal.set(self.customEncounter["rewardShortcut"])
                    
                e.update_lists(apply=False)

                e.tileLayoutMenuVal.set(self.customEncounter["layout"])
                e.tileSelections["1"]["startingNodes"]["value"].set(self.customEncounter["tileSelections"]["1"]["startingNodes"]["value"])
                e.tileSelections["1"]["traps"]["value"].set(self.customEncounter["tileSelections"]["1"]["traps"]["value"])
                e.tileSelections["1"]["1"]["enemies"]["1"]["value"].set(self.customEncounter["tileSelections"]["1"]["1"]["enemies"]["1"]["value"])
                e.tileSelections["1"]["1"]["enemies"]["2"]["value"].set(self.customEncounter["tileSelections"]["1"]["1"]["enemies"]["2"]["value"])
                e.tileSelections["1"]["1"]["enemies"]["3"]["value"].set(self.customEncounter["tileSelections"]["1"]["1"]["enemies"]["3"]["value"])
                e.tileSelections["1"]["1"]["terrain"]["value"].set(self.customEncounter["tileSelections"]["1"]["1"]["terrain"]["value"])
                e.tileSelections["1"]["2"]["enemies"]["1"]["value"].set(self.customEncounter["tileSelections"]["1"]["2"]["enemies"]["1"]["value"])
                e.tileSelections["1"]["2"]["enemies"]["2"]["value"].set(self.customEncounter["tileSelections"]["1"]["2"]["enemies"]["2"]["value"])
                e.tileSelections["1"]["2"]["enemies"]["3"]["value"].set(self.customEncounter["tileSelections"]["1"]["2"]["enemies"]["3"]["value"])
                e.tileSelections["1"]["2"]["terrain"]["value"].set(self.customEncounter["tileSelections"]["1"]["2"]["terrain"]["value"])
                if e.numberOfTilesRadioVal.get() == "1" and e.tileLayoutMenuVal.get() == "1 Tile 4x4":
                    e.tileSelections["1"]["3"]["enemies"]["1"]["value"].set(self.customEncounter["tileSelections"]["1"]["3"]["enemies"]["1"]["value"])
                    e.tileSelections["1"]["3"]["enemies"]["2"]["value"].set(self.customEncounter["tileSelections"]["1"]["3"]["enemies"]["2"]["value"])
                    e.tileSelections["1"]["3"]["enemies"]["3"]["value"].set(self.customEncounter["tileSelections"]["1"]["3"]["enemies"]["3"]["value"])
                    e.tileSelections["1"]["3"]["terrain"]["value"].set(self.customEncounter["tileSelections"]["1"]["3"]["terrain"]["value"])
                    e.tileSelections["1"]["4"]["enemies"]["1"]["value"].set(self.customEncounter["tileSelections"]["1"]["4"]["enemies"]["1"]["value"])
                    e.tileSelections["1"]["4"]["enemies"]["2"]["value"].set(self.customEncounter["tileSelections"]["1"]["4"]["enemies"]["2"]["value"])
                    e.tileSelections["1"]["4"]["enemies"]["3"]["value"].set(self.customEncounter["tileSelections"]["1"]["4"]["enemies"]["3"]["value"])
                    e.tileSelections["1"]["4"]["terrain"]["value"].set(self.customEncounter["tileSelections"]["1"]["4"]["terrain"]["value"])
                e.tileSelections["2"]["startingNodes"]["value"].set(self.customEncounter["tileSelections"]["2"]["startingNodes"]["value"])
                e.tileSelections["2"]["traps"]["value"].set(self.customEncounter["tileSelections"]["2"]["traps"]["value"])
                e.tileSelections["2"]["1"]["enemies"]["1"]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["enemies"]["1"]["value"])
                e.tileSelections["2"]["1"]["enemies"]["2"]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["enemies"]["2"]["value"])
                e.tileSelections["2"]["1"]["enemies"]["3"]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["enemies"]["3"]["value"])
                e.tileSelections["2"]["1"]["terrain"]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["terrain"]["value"])
                e.tileSelections["2"]["2"]["enemies"]["1"]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["enemies"]["1"]["value"])
                e.tileSelections["2"]["2"]["enemies"]["2"]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["enemies"]["2"]["value"])
                e.tileSelections["2"]["2"]["enemies"]["3"]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["enemies"]["3"]["value"])
                e.tileSelections["2"]["2"]["terrain"]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["terrain"]["value"])
                e.tileSelections["3"]["startingNodes"]["value"].set(self.customEncounter["tileSelections"]["3"]["startingNodes"]["value"])
                e.tileSelections["3"]["traps"]["value"].set(self.customEncounter["tileSelections"]["3"]["traps"]["value"])
                e.tileSelections["3"]["1"]["enemies"]["1"]["value"].set(self.customEncounter["tileSelections"]["3"]["1"]["enemies"]["1"]["value"])
                e.tileSelections["3"]["1"]["enemies"]["2"]["value"].set(self.customEncounter["tileSelections"]["3"]["1"]["enemies"]["2"]["value"])
                e.tileSelections["3"]["1"]["enemies"]["3"]["value"].set(self.customEncounter["tileSelections"]["3"]["1"]["enemies"]["3"]["value"])
                e.tileSelections["3"]["1"]["terrain"]["value"].set(self.customEncounter["tileSelections"]["3"]["1"]["terrain"]["value"])
                e.tileSelections["3"]["2"]["enemies"]["1"]["value"].set(self.customEncounter["tileSelections"]["3"]["2"]["enemies"]["1"]["value"])
                e.tileSelections["3"]["2"]["enemies"]["2"]["value"].set(self.customEncounter["tileSelections"]["3"]["2"]["enemies"]["2"]["value"])
                e.tileSelections["3"]["2"]["enemies"]["3"]["value"].set(self.customEncounter["tileSelections"]["3"]["2"]["enemies"]["3"]["value"])
                e.tileSelections["3"]["2"]["terrain"]["value"].set(self.customEncounter["tileSelections"]["3"]["2"]["terrain"]["value"])

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
            self.bind("<1>", lambda event: event.widget.focus_set())

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

            self.startingNodesMenuList = ["", "North", "East", "South", "West"]
            
            self.infoFrame1 = ttk.Frame(self.interior)
            self.infoFrame1.pack(side=tk.TOP, anchor=tk.W)
            self.infoFrame2 = ttk.Frame(self.interior)
            self.infoFrame2.pack(side=tk.TOP, anchor=tk.W)
            self.separator1 = ttk.Separator(self.interior)
            self.separator1.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.infoFrame3 = ttk.Frame(self.interior)
            self.infoFrame3.pack(side=tk.TOP, anchor=tk.W)
            self.separator2 = ttk.Separator(self.interior)
            self.separator2.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.infoFrame4 = ttk.Frame(self.interior)
            self.infoFrame4.pack(side=tk.TOP, anchor=tk.W)
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
            self.iconsFrame1 = ttk.Frame(self.interior)
            self.iconsFrame1.pack(side=tk.TOP, anchor=tk.W)
            self.iconsFrame2 = ttk.Frame(self.interior)
            self.iconsFrame2.pack(side=tk.TOP, anchor=tk.W)
            
            self.infoFrame1.bind("<1>", lambda event: event.widget.focus_set())
            self.infoFrame2.bind("<1>", lambda event: event.widget.focus_set())
            self.infoFrame3.bind("<1>", lambda event: event.widget.focus_set())
            self.infoFrame4.bind("<1>", lambda event: event.widget.focus_set())
            self.layoutFrame1.bind("<1>", lambda event: event.widget.focus_set())
            self.tileFrame1.bind("<1>", lambda event: event.widget.focus_set())
            self.tileFrame2.bind("<1>", lambda event: event.widget.focus_set())
            self.tileFrame3.bind("<1>", lambda event: event.widget.focus_set())
            self.iconsFrame1.bind("<1>", lambda event: event.widget.focus_set())
            self.iconsFrame2.bind("<1>", lambda event: event.widget.focus_set())

            self.encounterTitle = ttk.Label(self.infoFrame1, text=(" " * 35) + "Encounter Data", font=("Arial", 16))
            self.encounterTitle.bind("<1>", lambda event: event.widget.focus_set())
            self.encounterTitle.grid(column=0, row=0, padx=5, pady=5, columnspan=4, sticky=tk.W)
            
            self.encounterSetLabel = ttk.Label(self.infoFrame1, text="Set Name")
            self.encounterSetLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.encounterSetLabel.grid(column=0, row=1, padx=(5, 4), pady=5, sticky=tk.W)
            self.encounterSetEntry = tk.Text(self.infoFrame1, width=24, height=1, bg="#181818")
            self.encounterSetEntry.grid(column=1, row=1, padx=5, pady=5, columnspan=2, sticky=tk.W)
            
            self.emptySetIconVal = tk.IntVar()
            self.emptySetIcon = ttk.Checkbutton(self.infoFrame1, text="Empty Set Icon", variable=self.emptySetIconVal, command=self.topFrame.apply_changes)
            self.emptySetIcon.grid(column=3, row=1, padx=(45, 5), pady=5, sticky=tk.W)
            self.emptySetIcon.state(["!alternate"])
            
            self.encounterNameLabel = ttk.Label(self.infoFrame1, text="Encounter\nName\t")
            self.encounterNameLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.encounterNameLabel.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)
            self.encounterNameEntry = tk.Text(self.infoFrame1, width=24, height=2, bg="#181818")
            self.encounterNameEntry.bind("<KeyRelease>", self.handle_wait)
            self.encounterNameEntry.grid(column=1, row=2, padx=5, pady=5, columnspan=2, sticky=tk.W)

            self.levelRadioVal = tk.IntVar()
            self.previouslevelRadioVal = 0
            self.levelLabel = ttk.Label(self.infoFrame1, text="Encounter\nLevel")
            self.levelLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.levelLabel.grid(column=3, row=2, padx=(47, 5), pady=5, sticky=tk.W)
            self.levelRadio1 = ttk.Radiobutton(self.infoFrame1, text="1", variable=self.levelRadioVal, value=1, command=self.update_lists)
            self.levelRadio1.grid(column=3, row=2, padx=(120, 5), pady=5, sticky=tk.W)
            self.levelRadio2 = ttk.Radiobutton(self.infoFrame1, text="2", variable=self.levelRadioVal, value=2, command=self.update_lists)
            self.levelRadio2.grid(column=3, row=2, padx=(172, 5), pady=5, sticky=tk.W)
            self.levelRadio3 = ttk.Radiobutton(self.infoFrame1, text="3", variable=self.levelRadioVal, value=3, command=self.update_lists)
            self.levelRadio3.grid(column=3, row=2, padx=(225, 5), pady=5, sticky=tk.W)
            self.levelRadio4 = ttk.Radiobutton(self.infoFrame1, text="4", variable=self.levelRadioVal, value=4, command=self.update_lists)
            self.levelRadio4.grid(column=3, row=2, padx=(278, 5), pady=5, sticky=tk.W)
            
            self.flavorLabel = ttk.Label(self.infoFrame2, text="Flavor\nText\t")
            self.flavorLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.flavorLabel.grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)
            self.flavorEntry = tk.Text(self.infoFrame2, width=70, height=2, bg="#181818")
            self.flavorEntry.bind("<KeyRelease>", self.handle_wait)
            self.flavorEntry.grid(column=1, row=3, padx=5, pady=5, columnspan=6, sticky=tk.W)
            
            self.objectiveLabel = ttk.Label(self.infoFrame2, text="Objective\t")
            self.objectiveLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.objectiveLabel.grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)
            self.objectiveEntry = tk.Text(self.infoFrame2, width=70, height=2, bg="#181818")
            self.objectiveEntry.bind("<KeyRelease>", self.handle_wait)
            self.objectiveEntry.grid(column=1, row=4, padx=5, pady=5, columnspan=6, sticky=tk.W)

            self.rewardsTitle = ttk.Label(self.infoFrame3, text=(" " * 30) + "Rewards/Special Rules", font=("Arial", 16))
            self.rewardsTitle.bind("<1>", lambda event: event.widget.focus_set())
            self.rewardsTitle.grid(column=0, row=0, padx=5, pady=5, columnspan=6, sticky=tk.W)
            
            self.rewardSoulsPerPlayerVal = tk.IntVar()
            self.rewardSoulsPerPlayer = ttk.Checkbutton(self.infoFrame3, text="Souls Reward\nPer Player", variable=self.rewardSoulsPerPlayerVal, command=self.topFrame.apply_changes)
            self.rewardSoulsPerPlayer.grid(column=1, row=1, padx=(1, 5), pady=5, sticky=tk.W)
            self.rewardSoulsPerPlayer.state(["!alternate"])
            
            self.shortcutVal = tk.IntVar()
            self.shortcut = ttk.Checkbutton(self.infoFrame3, text="Shortcut\nReward", variable=self.shortcutVal, command=self.topFrame.apply_changes)
            self.shortcut.grid(column=2, row=1, padx=22, pady=5, sticky=tk.W, columnspan=2)
            self.shortcut.state(["!alternate"])
            
            self.rewardSoulsLabel = ttk.Label(self.infoFrame3, text="Souls\nReward\t")
            self.rewardSoulsLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.rewardSoulsLabel.grid(column=0, row=2, padx=5, pady=5, sticky=tk.NW)
            self.rewardSoulsEntry = tk.Text(self.infoFrame3, width=17, height=2, bg="#181818")
            self.rewardSoulsEntry.bind("<KeyRelease>", self.handle_wait)
            self.rewardSoulsEntry.grid(column=1, row=2, padx=5, pady=5, sticky=tk.NW)
            
            self.rewardSearchLabel = ttk.Label(self.infoFrame3, text="Search\nReward\t")
            self.rewardSearchLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.rewardSearchLabel.grid(column=0, row=3, padx=5, pady=5, rowspan=2, sticky=tk.NW)
            self.rewardSearchEntry = tk.Text(self.infoFrame3, width=17, height=2, bg="#181818")
            self.rewardSearchEntry.bind("<KeyRelease>", self.handle_wait)
            self.rewardSearchEntry.grid(column=1, row=3, padx=5, pady=5, rowspan=2, sticky=tk.NW)
            
            self.rewardDrawLabel = ttk.Label(self.infoFrame3, text="Draw\nReward\t")
            self.rewardDrawLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.rewardDrawLabel.grid(column=0, row=5, padx=5, pady=5, sticky=tk.NW)
            self.rewardDrawEntry = tk.Text(self.infoFrame3, width=17, height=2, bg="#181818")
            self.rewardDrawEntry.bind("<KeyRelease>", self.handle_wait)
            self.rewardDrawEntry.grid(column=1, row=5, padx=5, pady=5, sticky=tk.NW)
            
            self.rewardRefreshLabel = ttk.Label(self.infoFrame3, text="Refresh\nReward\t")
            self.rewardRefreshLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.rewardRefreshLabel.grid(column=0, row=6, padx=5, pady=5, sticky=tk.NW)
            self.rewardRefreshEntry = tk.Text(self.infoFrame3, width=17, height=2, bg="#181818")
            self.rewardRefreshEntry.bind("<KeyRelease>", self.handle_wait)
            self.rewardRefreshEntry.grid(column=1, row=6, padx=5, pady=5, sticky=tk.NW)
            
            self.rewardTrialLabel = ttk.Label(self.infoFrame3, text="Trial\nReward\t")
            self.rewardTrialLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.rewardTrialLabel.grid(column=0, row=7, padx=5, pady=5, sticky=tk.NW)
            self.rewardTrialEntry = tk.Text(self.infoFrame3, width=17, height=2, bg="#181818")
            self.rewardTrialEntry.bind("<KeyRelease>", self.handle_wait)
            self.rewardTrialEntry.grid(column=1, row=7, padx=5, pady=5, sticky=tk.NW)
            
            self.keywordsLabel = ttk.Label(self.infoFrame3, text="Keywords")
            self.keywordsLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.keywordsLabel.grid(column=2, row=2, padx=(24, 5), pady=5, sticky=tk.NW)
            self.keywordsEntry = tk.Text(self.infoFrame3, width=39, height=3, bg="#181818")
            self.keywordsEntry.bind("<KeyRelease>", self.handle_wait)
            self.keywordsEntry.grid(column=3, row=2, pady=5, rowspan=2, sticky=tk.NW)
            
            self.specialRulesLabel = ttk.Label(self.infoFrame3, text="Special\nRules")
            self.specialRulesLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.specialRulesLabel.grid(column=2, row=4, padx=(24, 5), pady=5, sticky=tk.NW)
            self.specialRulesEntry = tk.Text(self.infoFrame3, width=39, height=9, bg="#181818")
            self.specialRulesEntry.bind("<KeyRelease>", self.handle_wait)
            self.specialRulesEntry.grid(column=3, row=4, pady=5, rowspan=3, sticky=tk.NW)
            
            self.specialRulesTextSizeLabel = ttk.Label(self.infoFrame3, text="Special Rules\nText Size")
            self.specialRulesTextSizeLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.specialRulesTextSizeLabel.grid(column=2, row=7, padx=(24, 5), pady=5, sticky=tk.NW)
            self.specialRulesTextSizeVal = tk.IntVar()
            self.specialRulesTextSizeRadio1 = ttk.Radiobutton(self.infoFrame3, text="10", variable=self.specialRulesTextSizeVal, value=10, command=self.topFrame.apply_changes)
            self.specialRulesTextSizeRadio1.grid(column=2, row=7, padx=(120, 5), pady=5, columnspan=2, sticky=tk.W)
            self.specialRulesTextSizeRadio2 = ttk.Radiobutton(self.infoFrame3, text="11", variable=self.specialRulesTextSizeVal, value=11, command=self.topFrame.apply_changes)
            self.specialRulesTextSizeRadio2.grid(column=2, row=7, padx=(172, 5), pady=5, columnspan=2, sticky=tk.W)
            self.specialRulesTextSizeRadio3 = ttk.Radiobutton(self.infoFrame3, text="12", variable=self.specialRulesTextSizeVal, value=12, command=self.topFrame.apply_changes)
            self.specialRulesTextSizeRadio3.grid(column=2, row=7, padx=(225, 5), pady=5, columnspan=2, sticky=tk.W)
            
            self.tileLayoutLabel = ttk.Label(self.infoFrame4, text="Tile\nLayout")
            self.tileLayoutLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.tileLayoutLabel.grid(column=1, row=0, padx=(21, 5), pady=5, sticky=tk.W)
            self.tileLayoutMenuList = []
            self.tileLayoutMenuVal = tk.StringVar()
            self.tileLayoutMenu = ttk.Combobox(self.infoFrame4, height=11, width=37, state="readonly", values=self.tileLayoutMenuList, textvariable=self.tileLayoutMenuVal)
            self.previousTileLayoutMenuVal = ""
            self.tileLayoutMenu.bind("<KeyRelease>", self.search_layout_combobox)
            self.tileLayoutMenu.bind("<<ComboboxSelected>>", self.update_lists)
            self.tileLayoutMenu.unbind_class("TCombobox", "<MouseWheel>")
            self.tileLayoutMenu.unbind_class("TCombobox", "<ButtonPress-4>")
            self.tileLayoutMenu.unbind_class("TCombobox", "<ButtonPress-5>")
            self.tileLayoutMenu.grid(column=2, row=0, padx=(18, 5), pady=5, sticky=tk.W)

            self.numberOfTilesRadioVal = tk.IntVar()
            self.previousnumberOfTilesRadioVal = 0
            self.numberOfTilesLabel = ttk.Label(self.infoFrame4, text="Number\nof Tiles")
            self.numberOfTilesLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.numberOfTilesLabel.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
            self.numberOfTilesRadio1 = ttk.Radiobutton(self.infoFrame4, text="1", variable=self.numberOfTilesRadioVal, value=1, command=self.update_lists)
            self.numberOfTilesRadio1.grid(column=0, row=0, padx=(71, 5), pady=5, sticky=tk.W)
            self.numberOfTilesRadio2 = ttk.Radiobutton(self.infoFrame4, text="2", variable=self.numberOfTilesRadioVal, value=2, command=self.update_lists)
            self.numberOfTilesRadio2.grid(column=0, row=0, padx=(115, 5), pady=5, sticky=tk.W)
            self.numberOfTilesRadio3 = ttk.Radiobutton(self.infoFrame4, text="3", variable=self.numberOfTilesRadioVal, value=3, command=self.update_lists)
            self.numberOfTilesRadio3.grid(column=0, row=0, padx=(161, 5), pady=5, sticky=tk.W)

            self.tileSelections = {}
            
            for tile in range(1, 4):
                if tile == 1:
                    frame = self.tileFrame1
                elif tile == 2:
                    frame = self.tileFrame2
                elif tile == 3:
                    frame = self.tileFrame3

                self.tileSelections[str(tile)] = {
                    "label": ttk.Label(frame, text=(" " * 46) + "Tile " + str(tile), font=("Arial", 16)),
                    "traps": {"value": tk.IntVar()},
                    "enemiesLabel": ttk.Label(frame, text="Enemies"),
                    "startingNodesLabel": ttk.Label(frame, text="Starting Nodes"),
                    "startingNodes": {"value": tk.IntVar()},
                    "terrainLabel": ttk.Label(frame, text="Terrain")
                }

                self.tileSelections[str(tile)]["label"].bind("<1>", lambda event: event.widget.focus_set())
                self.tileSelections[str(tile)]["startingNodesLabel"].bind("<1>", lambda event: event.widget.focus_set())
                self.tileSelections[str(tile)]["terrainLabel"].bind("<1>", lambda event: event.widget.focus_set())
                self.tileSelections[str(tile)]["enemiesLabel"].bind("<1>", lambda event: event.widget.focus_set())

                self.tileSelections[str(tile)]["traps"]["widget"] = ttk.Checkbutton(frame, text="Traps", variable=self.tileSelections[str(tile)]["traps"]["value"], command=self.topFrame.apply_changes)

                self.tileSelections[str(tile)]["startingNodes"]["widgets"] = {
                    "None": ttk.Radiobutton(frame, text="None", variable=self.tileSelections[str(tile)]["startingNodes"]["value"], value=0, command=self.topFrame.apply_changes),
                    "Up": ttk.Radiobutton(frame, text="Up", variable=self.tileSelections[str(tile)]["startingNodes"]["value"], value=1, command=self.topFrame.apply_changes),
                    "Down": ttk.Radiobutton(frame, text="Down", variable=self.tileSelections[str(tile)]["startingNodes"]["value"], value=2, command=self.topFrame.apply_changes),
                    "Left": ttk.Radiobutton(frame, text="Left", variable=self.tileSelections[str(tile)]["startingNodes"]["value"], value=3, command=self.topFrame.apply_changes),
                    "Right": ttk.Radiobutton(frame, text="Right", variable=self.tileSelections[str(tile)]["startingNodes"]["value"], value=4, command=self.topFrame.apply_changes)
                }
                
                self.tileSelections[str(tile)]["traps"]["widget"].state(["!alternate"])
                
                for row in range(1, 5):
                    if tile > 1 and row > 2:
                        continue

                    self.tileSelections[str(tile)][str(row)] = {
                        "enemies": {
                            "1": {"value": tk.StringVar()},
                            "2": {"value": tk.StringVar()},
                            "3": {"value": tk.StringVar()}
                        },
                        "terrain": {"value": tk.StringVar()}
                    }

                    for x in range(1, 4):
                        self.tileSelections[str(tile)][str(row)]["enemies"][str(x)]["widget"] = ttk.Combobox(frame, height=int(28 * (self.root.winfo_screenheight() / 1080)), width=23, values=self.eNames, textvariable=self.tileSelections[str(tile)][str(row)]["enemies"][str(x)]["value"])
                        self.tileSelections[str(tile)][str(row)]["enemies"][str(x)]["widget"].set("")
                        self.tileSelections[str(tile)][str(row)]["enemies"][str(x)]["widget"].bind("<KeyRelease>", self.search_enemy_combobox)
                        self.tileSelections[str(tile)][str(row)]["enemies"][str(x)]["widget"].bind("<<ComboboxSelected>>", self.topFrame.apply_changes)
                        self.tileSelections[str(tile)][str(row)]["enemies"][str(x)]["widget"].unbind_class("TCombobox", "<MouseWheel>")
                        self.tileSelections[str(tile)][str(row)]["enemies"][str(x)]["widget"].unbind_class("TCombobox", "<ButtonPress-4>")
                        self.tileSelections[str(tile)][str(row)]["enemies"][str(x)]["widget"].unbind_class("TCombobox", "<ButtonPress-5>")

                    self.tileSelections[str(tile)][str(row)]["terrain"]["widget"] = ttk.Combobox(frame, height=int(28 * (self.root.winfo_screenheight() / 1080)) if len(self.terrainNames) > int(28 * (self.root.winfo_screenheight() / 1080)) else len(self.terrainNames), width=23, values=self.terrainNames, textvariable=self.tileSelections[str(tile)][str(row)]["terrain"]["value"])
                    self.tileSelections[str(tile)][str(row)]["terrain"]["widget"].set("")
                    self.tileSelections[str(tile)][str(row)]["terrain"]["widget"].bind("<KeyRelease>", self.search_terrain_combobox)
                    self.tileSelections[str(tile)][str(row)]["terrain"]["widget"].bind("<<ComboboxSelected>>", self.topFrame.apply_changes)
                    self.tileSelections[str(tile)][str(row)]["terrain"]["widget"].unbind_class("TCombobox", "<MouseWheel>")
                    self.tileSelections[str(tile)][str(row)]["terrain"]["widget"].unbind_class("TCombobox", "<ButtonPress-4>")
                    self.tileSelections[str(tile)][str(row)]["terrain"]["widget"].unbind_class("TCombobox", "<ButtonPress-5>")
                    
            self.tileSelections["1"]["label"].grid(column=0, row=0, padx=5, pady=5, sticky=tk.W, columnspan=4)
            self.tileSelections["1"]["enemiesLabel"].grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
            self.tileSelections["1"]["1"]["enemies"]["1"]["widget"].grid(column=0, row=2, padx=(5, 11), pady=5, sticky=tk.W)
            self.tileSelections["1"]["1"]["enemies"]["2"]["widget"].grid(column=1, row=2, padx=(5, 11), pady=5, sticky=tk.W)
            self.tileSelections["1"]["1"]["enemies"]["3"]["widget"].grid(column=2, row=2, padx=(5, 11), pady=5, sticky=tk.W)
            self.tileSelections["1"]["2"]["enemies"]["1"]["widget"].grid(column=0, row=3, padx=(5, 11), pady=5, sticky=tk.W)
            self.tileSelections["1"]["2"]["enemies"]["2"]["widget"].grid(column=1, row=3, padx=(5, 11), pady=5, sticky=tk.W)
            self.tileSelections["1"]["2"]["enemies"]["3"]["widget"].grid(column=2, row=3, padx=(5, 11), pady=5, sticky=tk.W)
            self.tileSelections["1"]["terrainLabel"].grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)
            self.tileSelections["1"]["1"]["terrain"]["widget"].grid(column=0, row=5, padx=5, pady=5, sticky=tk.W)
            self.tileSelections["1"]["2"]["terrain"]["widget"].grid(column=0, row=6, padx=5, pady=5, sticky=tk.W)
            self.tileSelections["1"]["traps"]["widget"].grid(column=1, row=5, padx=5, pady=5)
            self.tileSelections["1"]["startingNodesLabel"].grid(column=2, row=4, padx=5, pady=4, sticky=tk.W)
            self.tileSelections["1"]["startingNodes"]["widgets"]["None"].grid(column=2, row=4, padx=(100, 6), sticky=tk.E)
            self.tileSelections["1"]["startingNodes"]["widgets"]["Up"].grid(column=2, row=5, padx=5, sticky=tk.W)
            self.tileSelections["1"]["startingNodes"]["widgets"]["Down"].grid(column=2, row=5, padx=(100, 5), sticky=tk.E)
            self.tileSelections["1"]["startingNodes"]["widgets"]["Left"].grid(column=2, row=6, padx=5, sticky=tk.W)
            self.tileSelections["1"]["startingNodes"]["widgets"]["Right"].grid(column=2, row=6, padx=(100, 8), sticky=tk.E)

            self.tileSelections["2"]["label"].grid(column=0, row=0, padx=5, pady=5, sticky=tk.W, columnspan=4)
            self.tileSelections["3"]["label"].grid(column=0, row=0, padx=5, pady=5, sticky=tk.W, columnspan=4)

            self.icons = {}
            self.currentIcon = {
                "label": None,
                "file": "",
                "image": None,
                "photoImage": None,
                "size": None,
                "position": None
            }

            self.iconsFrame1.columnconfigure(4, minsize=180)
            self.iconsFrame1.rowconfigure(7, minsize=70)

            with open(baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\customIconsDict.json".replace("\\", pathSep), "r") as f:
                d = load(f)

            self.customIconsDict = {k: v for k, v in d.items() if k == "lookup" or path.isfile(baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + k)}
            
            self.iconTitle = ttk.Label(self.iconsFrame1, text=(" " * 40) + "Custom Icons", font=("Arial", 16))
            self.iconTitle.bind("<1>", lambda event: event.widget.focus_set())
            self.iconTitle.grid(column=0, row=0, padx=5, pady=5, columnspan=6, sticky=tk.W)
            
            self.iconNameLabel = ttk.Label(self.iconsFrame1, text="Icon Name\t")
            self.iconNameLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.iconNameLabel.grid(column=0, row=1, padx=5, pady=(5, 25), sticky=tk.W)
            self.iconNameEntry = tk.Text(self.iconsFrame1, width=20, height=1, bg="#181818")
            self.iconNameEntry.grid(column=1, row=1, padx=(25, 5), pady=(5, 25), columnspan=2, sticky=tk.W)
            
            self.iconSizeLabel = ttk.Label(self.iconsFrame1, text="Icon Size\t")
            self.iconSizeLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.iconSizeLabel.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)
            self.iconSizeVal = tk.IntVar()
            self.iconSizeRadio1 = ttk.Radiobutton(self.iconsFrame1, text="Text", variable=self.iconSizeVal, value=0, command=lambda: self.choose_icon_image(file=baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + self.currentIcon["file"][:self.currentIcon["file"].rfind("_")+1] + "iconText.png"))
            self.iconSizeRadio1.grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)
            self.iconSizeRadio2 = ttk.Radiobutton(self.iconsFrame1, text="Enemy/Terrain", variable=self.iconSizeVal, value=1, command=lambda: self.choose_icon_image(file=baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + self.currentIcon["file"][:self.currentIcon["file"].rfind("_")+1] + "iconEnemy.png"))
            self.iconSizeRadio2.grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)
            self.iconSizeRadio3 = ttk.Radiobutton(self.iconsFrame1, text="Set Icon", variable=self.iconSizeVal, value=2, command=lambda: self.choose_icon_image(file=baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + self.currentIcon["file"][:self.currentIcon["file"].rfind("_")+1] + "iconSet.png"))
            self.iconSizeRadio3.grid(column=0, row=5, padx=5, pady=5, sticky=tk.W)
            
            vcmdX = (self.register(self.callback_x))
            vcmdY = (self.register(self.callback_y))
            self.positionLabel = ttk.Label(self.iconsFrame1, text="Position\t")
            self.positionLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.positionLabel.grid(column=1, row=2, padx=(25, 5), pady=5, sticky=tk.NW, columnspan=2)
            self.xPositionLabel = ttk.Label(self.iconsFrame1, text="x:\n0-400\n")
            self.xPositionLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.xPositionLabel.grid(column=1, row=3, padx=(25, 5), sticky=tk.NW, rowspan=2)
            self.xPositionVal = tk.StringVar()
            self.xPositionEntry = ttk.Entry(self.iconsFrame1, textvariable=self.xPositionVal, width=4, validate="all", validatecommand=(vcmdX, "%P"))
            self.xPositionEntry.bind("<KeyRelease>", self.handle_wait_icon)
            self.xPositionEntry.grid(column=1, row=3, padx=(64, 5), pady=5, sticky=tk.NW, rowspan=2)
            self.yPositionLabel = ttk.Label(self.iconsFrame1, text="y:\n0-685\n")
            self.yPositionLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.yPositionLabel.grid(column=1, row=4, padx=(25, 0), sticky=tk.NW, rowspan=2)
            self.yPositionVal = tk.StringVar()
            self.yPositionEntry = ttk.Entry(self.iconsFrame1, textvariable=self.yPositionVal, width=4, validate="all", validatecommand=(vcmdY, "%P"))
            self.yPositionEntry.bind("<KeyRelease>", self.handle_wait_icon)
            self.yPositionEntry.grid(column=1, row=4, padx=(64, 5), pady=5, sticky=tk.NW, rowspan=2)
            self.chooseIconButton = ttk.Button(self.iconsFrame1, text="Choose Image", width=16, command=lambda x=True: self.choose_icon_image(buttonSource=x))
            self.chooseIconButton.grid(column=1, row=7, padx=(5, 0), pady=5, columnspan=2)
            self.saveIconButton = ttk.Button(self.iconsFrame1, text="Save Icon", width=16, command=self.save_custom_icon)
            self.saveIconButton.grid(column=1, row=8, padx=(5, 0), pady=5, columnspan=2)
            self.iconImageErrorsVal = tk.StringVar()
            self.iconSaveErrors = tk.Label(self.iconsFrame1, width=26, textvariable=self.iconImageErrorsVal)
            self.iconSaveErrors.bind("<1>", lambda event: event.widget.focus_set())
            self.iconSaveErrors.grid(column=3, row=8, pady=5, sticky=tk.W)
            
            self.iconView = tk.Label(self.iconsFrame1)
            self.iconView.bind("<1>", lambda event: event.widget.focus_set())
            self.iconView.grid(column=0, row=6, padx=5, pady=5, sticky=tk.NSEW, rowspan=3)

            self.customIconsFrame = ttk.Frame(self.iconsFrame1)
            self.scrollbarTreeviewCustomIcons = ttk.Scrollbar(self.customIconsFrame)
            self.scrollbarTreeviewCustomIcons.pack(side="right", fill="y")
            self.treeviewCustomIcons = ttk.Treeview(
                self.iconsFrame1,
                selectmode="browse",
                columns=("Name", "Type", "Enabled", "Image"),
                yscrollcommand=self.scrollbarTreeviewCustomIcons.set,
                height=9
            )

            self.treeviewCustomIcons.grid(column=3, row=1, padx=(15, 0), pady=5, rowspan=9, sticky=tk.NW)
            self.scrollbarTreeviewCustomIcons.config(command=self.treeviewCustomIcons.yview)

            self.treeviewCustomIcons.column('#0', width=0)

            self.treeviewCustomIcons.heading("Name", text="Name", anchor=tk.W)
            self.treeviewCustomIcons.heading("Type", text="Type", anchor=tk.W)
            self.treeviewCustomIcons.heading("Enabled", text="Enabled", anchor=tk.W)
            self.treeviewCustomIcons.heading("Image", text="Image", anchor=tk.W)
            self.treeviewCustomIcons.column("Name", anchor=tk.W, width=72)
            self.treeviewCustomIcons.column("Type", anchor=tk.W, width=50)
            self.treeviewCustomIcons.column("Enabled", anchor=tk.W, width=50)
            self.treeviewCustomIcons.column("Image", anchor=tk.W, width=50)

            self.saveIconButton = ttk.Button(self.iconsFrame1, text="Delete Icon", width=16, command=self.delete_custom_icon)
            self.saveIconButton.grid(column=3, row=8, padx=(5, 0), pady=5, sticky=tk.E)


        def handle_wait(self, event):
            # cancel the old job
            if self._afterId is not None:
                self.after_cancel(self._afterId)

            # create a new job
            self.after(1, self.topFrame.apply_changes())


        def handle_wait_icon(self, event):
            # cancel the old job
            if self._afterId is not None:
                self.after_cancel(self._afterId)

            # create a new job
            self.after(1, self.save_custom_icon())


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


        def update_lists(self, event=None, apply=True):
            try:
                log("Start of update_lists")

                tiles = self.numberOfTilesRadioVal.get()
                level = '1'#self.levelMenu.get()
                layout = self.tileLayoutMenu.get()
                if self.previousnumberOfTilesRadioVal != tiles:
                    self.update_tile_layout_list(tiles)
                    self.update_tile_sections(tiles)
                elif tiles == 1 and layout != self.previousTileLayoutMenuVal:
                    self.update_tile_sections(tiles)
                self.previousnumberOfTilesRadioVal = tiles
                self.previouslevelRadioVal = level
                self.previousTileLayoutMenuVal = layout

                self.tileLayoutMenu.selection_clear()

                if apply:
                    self.topFrame.apply_changes()
                
                log("End of update_lists")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def update_tile_layout_list(self, tiles):
            try:
                log("Start of update_tile_layout_list, tiles={}".format(str(tiles)))

                self.tileLayoutMenuList = [k for k in self.app.tileLayouts.keys() if str(tiles) + " Tile" in k]
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

                if layout == "1 Tile 4x4" and not self.tileSelections["1"]["3"]["enemies"]["1"]["widget"].winfo_viewable():
                    self.tileSelections["1"]["terrainLabel"].grid_forget()
                    self.tileSelections["1"]["1"]["terrain"]["widget"].grid_forget()
                    self.tileSelections["1"]["2"]["terrain"]["widget"].grid_forget()
                    self.tileSelections["1"]["traps"]["widget"].grid_forget()
                    self.tileSelections["1"]["startingNodesLabel"].grid_forget()
                    self.tileSelections["1"]["startingNodes"]["widgets"]["None"].grid_forget()
                    self.tileSelections["1"]["startingNodes"]["widgets"]["Up"].grid_forget()
                    self.tileSelections["1"]["startingNodes"]["widgets"]["Down"].grid_forget()
                    self.tileSelections["1"]["startingNodes"]["widgets"]["Left"].grid_forget()
                    self.tileSelections["1"]["startingNodes"]["widgets"]["Right"].grid_forget()

                    self.tileSelections["1"]["1"]["enemies"]["1"]["widget"].grid(column=0, row=4, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["1"]["1"]["enemies"]["2"]["widget"].grid(column=1, row=4, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["1"]["1"]["enemies"]["3"]["widget"].grid(column=2, row=4, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["1"]["2"]["enemies"]["1"]["widget"].grid(column=0, row=5, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["1"]["2"]["enemies"]["2"]["widget"].grid(column=1, row=5, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["1"]["2"]["enemies"]["3"]["widget"].grid(column=2, row=5, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["1"]["3"]["enemies"]["1"]["widget"].grid(column=0, row=6, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["1"]["3"]["enemies"]["2"]["widget"].grid(column=1, row=6, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["1"]["3"]["enemies"]["3"]["widget"].grid(column=2, row=6, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["1"]["4"]["enemies"]["1"]["widget"].grid(column=0, row=7, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["1"]["4"]["enemies"]["2"]["widget"].grid(column=1, row=7, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["1"]["4"]["enemies"]["3"]["widget"].grid(column=2, row=7, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["1"]["terrainLabel"].grid(column=0, row=8, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["1"]["1"]["terrain"]["widget"].grid(column=0, row=9, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["1"]["2"]["terrain"]["widget"].grid(column=0, row=10, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["1"]["3"]["terrain"]["widget"].grid(column=0, row=11, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["1"]["4"]["terrain"]["widget"].grid(column=0, row=12, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["1"]["traps"]["widget"].grid(column=1, row=9, padx=5, pady=5)
                    self.tileSelections["1"]["startingNodesLabel"].grid(column=2, row=8, padx=5, pady=4, sticky=tk.W)
                    self.tileSelections["1"]["startingNodes"]["widgets"]["None"].grid(column=2, row=8, padx=(100, 6), sticky=tk.E)
                    self.tileSelections["1"]["startingNodes"]["widgets"]["Up"].grid(column=2, row=9, padx=5, sticky=tk.W)
                    self.tileSelections["1"]["startingNodes"]["widgets"]["Down"].grid(column=2, row=9, padx=(100, 5), sticky=tk.E)
                    self.tileSelections["1"]["startingNodes"]["widgets"]["Left"].grid(column=2, row=10, padx=5, sticky=tk.W)
                    self.tileSelections["1"]["startingNodes"]["widgets"]["Right"].grid(column=2, row=10, padx=(100, 8), sticky=tk.E)
                else:
                    self.tileSelections["1"]["3"]["enemies"]["1"]["widget"].grid_forget()
                    self.tileSelections["1"]["3"]["enemies"]["2"]["widget"].grid_forget()
                    self.tileSelections["1"]["3"]["enemies"]["3"]["widget"].grid_forget()
                    self.tileSelections["1"]["4"]["enemies"]["1"]["widget"].grid_forget()
                    self.tileSelections["1"]["4"]["enemies"]["2"]["widget"].grid_forget()
                    self.tileSelections["1"]["4"]["enemies"]["3"]["widget"].grid_forget()
                    self.tileSelections["1"]["3"]["terrain"]["widget"].grid_forget()
                    self.tileSelections["1"]["4"]["terrain"]["widget"].grid_forget()
                    
                if int(tiles) > 1 and not self.tileSelections["2"]["terrainLabel"].winfo_viewable():
                    self.tileSelections["2"]["enemiesLabel"].grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["2"]["1"]["enemies"]["1"]["widget"].grid(column=0, row=2, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["2"]["1"]["enemies"]["2"]["widget"].grid(column=1, row=2, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["2"]["1"]["enemies"]["3"]["widget"].grid(column=2, row=2, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["2"]["2"]["enemies"]["1"]["widget"].grid(column=0, row=3, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["2"]["2"]["enemies"]["2"]["widget"].grid(column=1, row=3, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["2"]["2"]["enemies"]["3"]["widget"].grid(column=2, row=3, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["2"]["terrainLabel"].grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["2"]["1"]["terrain"]["widget"].grid(column=0, row=5, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["2"]["2"]["terrain"]["widget"].grid(column=0, row=6, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["2"]["traps"]["widget"].grid(column=1, row=5, padx=5, pady=5)
                    self.tileSelections["2"]["startingNodesLabel"].grid(column=2, row=4, padx=5, pady=4, sticky=tk.W)
                    self.tileSelections["2"]["startingNodes"]["widgets"]["None"].grid(column=2, row=4, padx=(100, 6), sticky=tk.E)
                    self.tileSelections["2"]["startingNodes"]["widgets"]["Up"].grid(column=2, row=5, padx=5, sticky=tk.W)
                    self.tileSelections["2"]["startingNodes"]["widgets"]["Down"].grid(column=2, row=5, padx=(100, 5), sticky=tk.E)
                    self.tileSelections["2"]["startingNodes"]["widgets"]["Left"].grid(column=2, row=6, padx=5, sticky=tk.W)
                    self.tileSelections["2"]["startingNodes"]["widgets"]["Right"].grid(column=2, row=6, padx=(100, 8), sticky=tk.E)
                else:
                    self.tileSelections["2"]["1"]["enemies"]["1"]["widget"].grid_forget()
                    self.tileSelections["2"]["1"]["enemies"]["2"]["widget"].grid_forget()
                    self.tileSelections["2"]["1"]["enemies"]["3"]["widget"].grid_forget()
                    self.tileSelections["2"]["2"]["enemies"]["1"]["widget"].grid_forget()
                    self.tileSelections["2"]["2"]["enemies"]["2"]["widget"].grid_forget()
                    self.tileSelections["2"]["2"]["enemies"]["3"]["widget"].grid_forget()
                    self.tileSelections["2"]["terrainLabel"].grid_forget()
                    self.tileSelections["2"]["1"]["terrain"]["widget"].grid_forget()
                    self.tileSelections["2"]["2"]["terrain"]["widget"].grid_forget()
                    self.tileSelections["2"]["traps"]["widget"].grid_forget()
                    self.tileSelections["2"]["startingNodesLabel"].grid_forget()
                    self.tileSelections["2"]["startingNodes"]["widgets"]["None"].grid_forget()
                    self.tileSelections["2"]["startingNodes"]["widgets"]["Up"].grid_forget()
                    self.tileSelections["2"]["startingNodes"]["widgets"]["Down"].grid_forget()
                    self.tileSelections["2"]["startingNodes"]["widgets"]["Left"].grid_forget()
                    self.tileSelections["2"]["startingNodes"]["widgets"]["Right"].grid_forget()
                    
                if int(tiles) > 2 and not self.tileSelections["2"]["terrainLabel"].winfo_viewable():
                    self.tileSelections["3"]["enemiesLabel"].grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["3"]["1"]["enemies"]["1"]["widget"].grid(column=0, row=2, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["3"]["1"]["enemies"]["2"]["widget"].grid(column=1, row=2, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["3"]["1"]["enemies"]["3"]["widget"].grid(column=2, row=2, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["3"]["2"]["enemies"]["1"]["widget"].grid(column=0, row=3, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["3"]["2"]["enemies"]["2"]["widget"].grid(column=1, row=3, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["3"]["2"]["enemies"]["3"]["widget"].grid(column=2, row=3, padx=(5, 11), pady=5, sticky=tk.W)
                    self.tileSelections["3"]["terrainLabel"].grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["3"]["1"]["terrain"]["widget"].grid(column=0, row=5, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["3"]["2"]["terrain"]["widget"].grid(column=0, row=6, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["3"]["traps"]["widget"].grid(column=1, row=5, padx=5, pady=5)
                    self.tileSelections["3"]["startingNodesLabel"].grid(column=2, row=4, padx=5, pady=4, sticky=tk.W)
                    self.tileSelections["3"]["startingNodes"]["widgets"]["None"].grid(column=2, row=4, padx=(100, 6), sticky=tk.E)
                    self.tileSelections["3"]["startingNodes"]["widgets"]["Up"].grid(column=2, row=5, padx=5, sticky=tk.W)
                    self.tileSelections["3"]["startingNodes"]["widgets"]["Down"].grid(column=2, row=5, padx=(100, 5), sticky=tk.E)
                    self.tileSelections["3"]["startingNodes"]["widgets"]["Left"].grid(column=2, row=6, padx=5, sticky=tk.W)
                    self.tileSelections["3"]["startingNodes"]["widgets"]["Right"].grid(column=2, row=6, padx=(100, 8), sticky=tk.E)
                else:
                    self.tileSelections["3"]["1"]["enemies"]["1"]["widget"].grid_forget()
                    self.tileSelections["3"]["1"]["enemies"]["2"]["widget"].grid_forget()
                    self.tileSelections["3"]["1"]["enemies"]["3"]["widget"].grid_forget()
                    self.tileSelections["3"]["2"]["enemies"]["1"]["widget"].grid_forget()
                    self.tileSelections["3"]["2"]["enemies"]["2"]["widget"].grid_forget()
                    self.tileSelections["3"]["2"]["enemies"]["3"]["widget"].grid_forget()
                    self.tileSelections["3"]["terrainLabel"].grid_forget()
                    self.tileSelections["3"]["1"]["terrain"]["widget"].grid_forget()
                    self.tileSelections["3"]["2"]["terrain"]["widget"].grid_forget()
                    self.tileSelections["3"]["traps"]["widget"].grid_forget()
                    self.tileSelections["3"]["startingNodesLabel"].grid_forget()
                    self.tileSelections["3"]["startingNodes"]["widgets"]["None"].grid_forget()
                    self.tileSelections["3"]["startingNodes"]["widgets"]["Up"].grid_forget()
                    self.tileSelections["3"]["startingNodes"]["widgets"]["Down"].grid_forget()
                    self.tileSelections["3"]["startingNodes"]["widgets"]["Left"].grid_forget()
                    self.tileSelections["3"]["startingNodes"]["widgets"]["Right"].grid_forget()
                
                log("End of update_tile_sections")
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
                self.iconSaveErrors.config(image="")
                self.iconSaveErrors.image = None
                if self.currentIcon["label"] in self.icons:
                    del self.icons[self.currentIcon["label"]]
                    self.iconMenuList.remove(self.currentIcon["label"])
                    self.iconMenuVal.set("")
                self.currentIcon = {
                    "label": None,
                    "file": "",
                    "image": None,
                    "photoImage": None,
                    "size": None,
                    "position": None
                }
                self.iconMenu.config(values=self.iconMenuList)
                self.iconMenu.set("")

                self.topFrame.apply_changes()
                
                log("End of delete_custom_icon")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def save_custom_icon(self, event=None):
            try:
                log("Start of save_custom_icon")

                errors = []
                icon = self.iconNameEntry.get("1.0", "end").strip()

                if not icon:
                    errors.append("name")
                if not self.currentIcon["image"]:
                    errors.append("image")

                if errors:
                    errorText = "Required: " + ", ".join(errors)
                    self.iconImageErrorsVal.set(errorText)
                    return

                self.iconImageErrorsVal.set("")

                self.currentIcon["label"] = icon

                self.customIconsDict["lookup"][icon] = deepcopy(self.currentIcon["file"])
                
                if icon and icon not in self.icons:
                    contents = [(self.treeviewCustomIcons.item(child)["values"][1], self.treeviewCustomIcons.item(child)["values"][0]) for child in self.treeviewCustomIcons.get_children("")]
                    c = (self.currentIcon["size"].replace("icon", ""), self.currentIcon["label"])
                    self.treeviewCustomIcons.insert(parent="", index=bisect_left(contents, (c[0], c[1])), values=(c[1], c[0]), tags=True)
                    
                self.icons[icon] = {
                    "label": icon,
                    "position": (self.xPositionEntry.get(), self.yPositionEntry.get())
                    }

                self.icons[icon]["image"], self.icons[icon]["photoImage"] = self.app.create_image(baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + self.currentIcon["file"], self.currentIcon["size"], 99, pathProvided=True, extensionProvided=True)
                
                self.topFrame.customEncounter["icons"] = {k: v for k, v in self.icons.items() if "" not in self.icons[k]["position"]}

                self.topFrame.apply_changes()

                self.iconImageErrorsVal.set("Saved " + datetime.now().strftime("%H:%M:%S"))

                log("End of save_custom_icon")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def choose_icon_image(self, event=None, file=None, buttonSource=False):
            try:
                log("Start of choose_icon_image, file={}".format(str(file)))

                if file and not self.currentIcon["file"]:
                    return
                
                if self.iconSizeVal.get() == 0:
                    size = "iconText"
                elif self.iconSizeVal.get() == 1:
                    size = "iconEnemy"
                elif self.iconSizeVal.get() == 2:
                    size = "iconSet"
                
                if not file and buttonSource:
                    file = filedialog.askopenfilename(initialdir=baseFolder)

                    # If they canceled, do nothing.
                    if not file:
                        return
                    
                    fileName = path.splitext(path.basename(file))

                    sizes = {"iconEnemy", "iconText", "iconSet"}

                    for imSize in list(sizes - set([size])) + [size]:
                        newFile = baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + fileName[0] + "_" + imSize + ".png"
                        if not path.isfile(newFile):
                            i, p = self.app.create_image(file, imSize, 99, pathProvided=True, extensionProvided=True)
                            i.save(newFile)
                        else:
                            i, p = self.app.create_image(newFile, imSize, 99, pathProvided=True, extensionProvided=True)
                        file = newFile

                    self.customIconsDict[path.basename(file)] = {
                        "originalFileName": fileName[0] + fileName[1],
                        "size": size
                    }
                else:
                    i, p = self.app.create_image(file, size, 99, pathProvided=True, extensionProvided=True)

                self.currentIcon["file"] = path.basename(file)
                self.currentIcon["size"] = size
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