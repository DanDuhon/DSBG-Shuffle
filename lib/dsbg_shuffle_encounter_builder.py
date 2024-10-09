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
    from dsbg_shuffle_utility import PopupWindow, VerticalScrolledFrame, clear_other_tab_images, error_popup, log, set_display_bindings_by_tab, baseFolder, font, fontSize11, fontSize10, fontEncounterName, fontFlavor, pathSep


    class EncounterBuilderFrame(ttk.Frame):
        def __init__(self, app, root):
            super(EncounterBuilderFrame, self).__init__()
            self.app = app
            self.root = root

            self.customEncounter = {"icons": {}}
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

                e.iconImageErrorsVal.set("")
                
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
                
                e.iconView.config(image=self.app.iconBg1PhotoImage)
                e.iconView.image=self.app.iconBg1PhotoImage

                for icon in e.encounterIcons:
                    e.encounterIcons[icon]["view"].grid_forget()
                    e.encounterIcons[icon]["posLabel"].grid_forget()
                    e.encounterIcons[icon]["xLabel"].grid_forget()
                    e.encounterIcons[icon]["xEntry"].grid_forget()
                    e.encounterIcons[icon]["yLabel"].grid_forget()
                    e.encounterIcons[icon]["yEntry"].grid_forget()
                    
                e.encounterIcons = {}

                e.rewardSoulsPerPlayer.state(["!selected"])
                e.shortcut.state(["!selected"])
                e.levelRadioVal.set(1)
                e.numberOfTilesRadioVal.set(1)

                for tile in range(1, 4):
                    e.tileSelections[str(tile)]["traps"]["value"].set(0)
                    e.tileSelections[str(tile)]["startingNodes"]["tileValue"].set(0)
                    e.tileSelections[str(tile)]["startingNodes"]["nodesValue"].set(0)
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
                        if e.tileSelections[str(tile)]["startingNodes"]["tileValue"].get() and e.tileSelections[str(tile)]["startingNodes"]["nodesValue"].get():
                            startingNodesLocation = e.tileSelections[str(tile)]["startingNodes"]["nodesValue"].get()
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

                        if e.tileSelections[str(tile)]["startingNodes"]["tileValue"].get() and e.tileSelections[str(tile)]["traps"]["value"].get() == 1:
                            image = self.app.tileNumbers[tile]["starting"]["traps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)
                        elif e.tileSelections[str(tile)]["startingNodes"]["tileValue"].get() and e.tileSelections[str(tile)]["traps"]["value"].get() != 1:
                            image = self.app.tileNumbers[tile]["starting"]["noTraps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)
                        elif not e.tileSelections[str(tile)]["startingNodes"]["tileValue"].get() and e.tileSelections[str(tile)]["traps"]["value"].get() == 1:
                            image = self.app.tileNumbers[tile]["notStarting"]["traps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)
                        elif not e.tileSelections[str(tile)]["startingNodes"]["tileValue"].get() and e.tileSelections[str(tile)]["traps"]["value"].get() != 1:
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

                # Custom Icons
                for icon in [icon for icon in e.encounterIcons if e.encounterIcons[icon]["position"][0].get() != "" and e.encounterIcons[icon]["position"][1].get() != ""]:
                    lookup = e.encounterIcons[icon]["lookup"] if e.encounterIcons[icon]["lookup"] in e.customIconsDict else e.encounterIcons[icon]["lookup"]
                    image = e.customIconsDict[lookup]["image"] if lookup in e.customIconsDict else self.app.iconsForCustom[e.encounterIcons[icon]["lookup"]]["image"]
                    box = (int(e.encounterIcons[icon]["position"][0].get()), int(e.encounterIcons[icon]["position"][1].get()))
                    self.app.displayImage.paste(im=image, box=box, mask=image)

                self.customEncounter["set"] = e.encounterSetEntry.get("1.0", "end").strip()
                self.customEncounter["emptySetIcon"] = e.emptySetIconVal.get()
                self.customEncounter["image"] = self.app.displayImage.copy()
                self.customEncounter["numberOfTiles"] = e.numberOfTilesRadioVal.get()
                self.customEncounter["level"] = e.levelRadioVal.get()
                self.customEncounter["encounterName"] = e.encounterNameEntry.get("1.0", "end").strip()
                self.customEncounter["flavor"] = e.flavorEntry.get("1.0", "end").strip()
                self.customEncounter["objective"] = e.objectiveEntry.get("1.0", "end").strip()
                self.customEncounter["keywords"] = e.keywordsEntry.get("1.0", "end").strip()
                self.customEncounter["specialRules"] = e.specialRulesEntry.get("1.0", "end").strip()
                self.customEncounter["specialRulesTextSize"] = e.specialRulesTextSizeVal.get()
                self.customEncounter["rewardSouls"] = e.rewardSoulsEntry.get("1.0", "end").strip()
                self.customEncounter["rewardSoulsPerPlayer"] = e.rewardSoulsPerPlayerVal.get()
                self.customEncounter["rewardSearch"] = e.rewardSearchEntry.get("1.0", "end").strip()
                self.customEncounter["rewardDraw"] = e.rewardDrawEntry.get("1.0", "end").strip()
                self.customEncounter["rewardRefresh"] = e.rewardRefreshEntry.get("1.0", "end").strip()
                self.customEncounter["rewardTrial"] = e.rewardTrialEntry.get("1.0", "end").strip()
                self.customEncounter["rewardShortcut"] = e.shortcutVal.get()
                self.customEncounter["layout"] = e.tileLayoutMenuVal.get()
                for id in e.encounterIcons:
                    if e.encounterIcons[id]["position"][0].get() == "" or e.encounterIcons[id]["position"][1].get() == "":
                        continue

                    newId = 0 if id == 0 else max([int(k) for k in self.customEncounter["icons"].keys()]) + 1

                    self.customEncounter["icons"][str(newId)] = {
                        "lookup": e.encounterIcons[id]["lookup"],
                        "position": (e.encounterIcons[id]["position"][0].get(), e.encounterIcons[id]["position"][1].get()),
                        "note": e.encounterIcons[id]["noteVal"].get()
                    }

                self.customEncounter["tileSelections"] = {
                    "1": {
                        "startingNodes": {
                            "tileValue": e.tileSelections["1"]["startingNodes"]["tileValue"].get(),
                            "nodesValue": e.tileSelections["1"]["startingNodes"]["nodesValue"].get()
                            },
                        "traps": {"value": e.tileSelections["1"]["traps"]["value"].get()},
                        "1": {"terrain": {"value": e.tileSelections["1"]["1"]["terrain"]["value"].get()},
                            "enemies": {
                                "1": {"value": e.tileSelections["1"]["1"]["enemies"]["1"]["value"].get()},
                                "2": {"value": e.tileSelections["1"]["1"]["enemies"]["2"]["value"].get()},
                                "3": {"value": e.tileSelections["1"]["1"]["enemies"]["3"]["value"].get()}
                            }},
                        "2": {"terrain": {"value": e.tileSelections["1"]["2"]["terrain"]["value"].get()},
                            "enemies": {
                                "1": {"value": e.tileSelections["1"]["2"]["enemies"]["1"]["value"].get()},
                                "2": {"value": e.tileSelections["1"]["2"]["enemies"]["2"]["value"].get()},
                                "3": {"value": e.tileSelections["1"]["2"]["enemies"]["3"]["value"].get()}
                            }},
                        "3": {"terrain": {"value": e.tileSelections["1"]["3"]["terrain"]["value"].get()},
                            "enemies": {
                                "1": {"value": e.tileSelections["1"]["3"]["enemies"]["1"]["value"].get()},
                                "2": {"value": e.tileSelections["1"]["3"]["enemies"]["2"]["value"].get()},
                                "3": {"value": e.tileSelections["1"]["3"]["enemies"]["3"]["value"].get()}
                            }},
                        "4": {"terrain": {"value": e.tileSelections["1"]["4"]["terrain"]["value"].get()},
                            "enemies": {
                                "1": {"value": e.tileSelections["1"]["4"]["enemies"]["1"]["value"].get()},
                                "2": {"value": e.tileSelections["1"]["4"]["enemies"]["2"]["value"].get()},
                                "3": {"value": e.tileSelections["1"]["4"]["enemies"]["3"]["value"].get()}
                            }}
                        },
                    "2": {
                        "startingNodes": {
                            "tileValue": e.tileSelections["2"]["startingNodes"]["tileValue"].get(),
                            "nodesValue": e.tileSelections["2"]["startingNodes"]["nodesValue"].get()
                            },
                        "traps": {"value": e.tileSelections["2"]["traps"]["value"].get()},
                        "1": {"terrain": {"value": e.tileSelections["2"]["1"]["terrain"]["value"].get()},
                            "enemies": {
                                "1": {"value": e.tileSelections["2"]["1"]["enemies"]["1"]["value"].get()},
                                "2": {"value": e.tileSelections["2"]["1"]["enemies"]["2"]["value"].get()},
                                "3": {"value": e.tileSelections["2"]["1"]["enemies"]["3"]["value"].get()}
                            }},
                        "2": {"terrain": {"value": e.tileSelections["2"]["2"]["terrain"]["value"].get()},
                            "enemies": {
                                "1": {"value": e.tileSelections["2"]["2"]["enemies"]["1"]["value"].get()},
                                "2": {"value": e.tileSelections["2"]["2"]["enemies"]["2"]["value"].get()},
                                "3": {"value": e.tileSelections["2"]["2"]["enemies"]["3"]["value"].get()}
                            }}
                        },
                    "3": {
                        "startingNodes": {
                            "tileValue": e.tileSelections["3"]["startingNodes"]["tileValue"].get(),
                            "nodesValue": e.tileSelections["3"]["startingNodes"]["nodesValue"].get()
                            },
                        "traps": {"value": e.tileSelections["3"]["traps"]["value"].get()},
                        "1": {"terrain": {"value": e.tileSelections["3"]["1"]["terrain"]["value"].get()},
                            "enemies": {
                                "1": {"value": e.tileSelections["3"]["1"]["enemies"]["1"]["value"].get()},
                                "2": {"value": e.tileSelections["3"]["1"]["enemies"]["2"]["value"].get()},
                                "3": {"value": e.tileSelections["3"]["1"]["enemies"]["3"]["value"].get()}
                            }},
                        "2": {"terrain": {"value": e.tileSelections["3"]["2"]["terrain"]["value"].get()},
                            "enemies": {
                                "1": {"value": e.tileSelections["3"]["2"]["enemies"]["1"]["value"].get()},
                                "2": {"value": e.tileSelections["3"]["2"]["enemies"]["2"]["value"].get()},
                                "3": {"value": e.tileSelections["3"]["2"]["enemies"]["3"]["value"].get()}
                            }}
                        }
                    }

                e.iconImageErrorsVal.set("")

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

                saveEncounter = {k: v for k, v in self.customEncounter.items() if k not in {"image", }}

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

                customEncounterKeys = {
                        "set", "numberOfTiles", "level", "encounterName", "flavor", "objective", "keywords",
                        "specialRules", "rewardSouls", "rewardSoulsPerPlayer", "rewardSearch", "rewardDraw",
                        "rewardRefresh", "rewardTrial", "rewardShortcut", "layout", "icons", "tileSelections",
                        "emptySetIcon", "specialRulesTextSize"}

                # Check to see if there are any invalid keys in the JSON file.
                # This is about as sure as I can be that you can't load random JSON into the app.
                if set(self.customEncounter.keys()) != customEncounterKeys:
                    self.app.set_bindings_buttons_menus(False)
                    PopupWindow(self.root, labelText="Invalid DSBG-Shuffle encounter file.", firstButton="Ok")
                    self.app.set_bindings_buttons_menus(True)
                    log("End of load_custom_encounter (invalid file)")
                    return
                
                for icon in self.customEncounter["icons"]:
                    self.customEncounter["icons"][icon]["lookup"] = tuple(self.customEncounter["icons"][icon]["lookup"])
                
                # Check to make sure that this encounter's icons exist in a way we expect.
                keysToDelete = []
                for icon in self.customEncounter["icons"]:
                    lookup = self.customEncounter["icons"][icon]["lookup"]
                    if not path.isfile(baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + lookup[0]):
                        p = PopupWindow(self.root, labelText="Missing custom icon image " + lookup[0]+ ".\nRemove custom icon and continue loading?", yesButton=True, noButton=True)
                        if not p.answer:
                            return
                        keysToDelete.append(lookup)
                        continue

                    iconCount = len([int(k) for k in self.customEncounter["icons"].keys() if k.isdigit()] + [k for k in e.customIconsDict if k != "lookup"])
                    iid = str(iconCount)
                    if lookup not in e.customIconsDict:
                        e.customIconsDict["lookup"][lookup[0]] = lookup
                        e.customIconsDict[lookup] = {
                            "originalFileName": lookup[0],
                            "originalFileFullPath": baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + lookup[0],
                            "file": lookup[0],
                            "size": lookup[1],
                            "label": lookup[0],
                            "iid": iid
                        }

                    i, p = self.app.create_image(e.customIconsDict[lookup]["originalFileFullPath"], lookup[1], 99, pathProvided=True, extensionProvided=True, emptySetIcon=self.customEncounter["emptySetIcon"])
                    e.customIconsDict[lookup]["image"] = i
                    e.customIconsDict[lookup]["photoImage"] = p

                    e.customIconsDict[lookup]["treeviewImage"] = self.app.create_image(baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + lookup[0], "iconTreeview", 99, pathProvided=True, extensionProvided=True, emptySetIcon=self.customEncounter["emptySetIcon"])

                    if e.customIconsDict[lookup]["size"] == "iconText":
                        sizeDisplay = "Text"
                    elif e.customIconsDict[lookup]["size"] == "iconEnemy":
                        sizeDisplay = "Enemy/Terrain"
                    elif e.customIconsDict[lookup]["size"] == "iconSet":
                        sizeDisplay = "Set Icon"

                for key in keysToDelete:
                    del self.customEncounter["icons"][key]
                    
                contents = [(e.treeviewCustomIcons.item(child)["values"][1], e.treeviewCustomIcons.item(child)["values"][0]) for child in e.treeviewCustomIcons.get_children()]
                iid = str(len(contents))
                c = (sizeDisplay, e.customIconsDict[lookup]["label"])
                if icon not in set([c[1] for c in contents]):
                    e.customIconsTreeviewDict[c[1]] = {
                        "iid": iid,
                        "index": bisect_left(contents, (c[0], c[1])),
                        "values": (c[1], c[0]),
                        "image": e.customIconsDict[lookup]["treeviewImage"]
                    }
                    e.treeviewCustomIcons.insert(parent="", iid=iid, index=e.customIconsTreeviewDict[c[1]]["index"], values=("   " + self.customIconsTreeviewDict[c[1]]["values"][0], self.customIconsTreeviewDict[c[1]]["values"][1]), image=e.customIconsTreeviewDict[c[1]]["image"], tags=False, open=True)
                    e.customIconsDict[lookup]["iid"] = iid

                    e.treeviewCustomIcons.focus(iid)
                    e.treeviewCustomIcons.selection_set(iid)
                    e.add_icon_to_encounter()

                saveDict = {}
                for key in e.customIconsDict:
                    if key == "lookup":
                        saveDict["lookup"] = e.customIconsDict["lookup"]
                    else:
                        saveDict["||".join(key)] = {k: v for k, v in e.customIconsDict[key].items() if "mage" not in k}

                with open(baseFolder + "\\lib\\dsbg_shuffle_custom_icons.json".replace("\\", pathSep), "w") as iconsFile:
                    dump(saveDict, iconsFile)
                
                self.encounterSaveLabelVal.set("")

                # Need to fill in all the GUI elements.
                e.encounterSetEntry.insert(tk.END, self.customEncounter["set"])
                e.emptySetIconVal.set(self.customEncounter["emptySetIcon"])
                e.numberOfTilesRadioVal.set(self.customEncounter["numberOfTiles"])
                e.levelRadioVal.set(self.customEncounter["level"])
                e.encounterNameEntry.insert(tk.END, self.customEncounter["encounterName"])
                e.flavorEntry.insert(tk.END, self.customEncounter["flavor"])
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
                e.tileSelections["1"]["startingNodes"]["tileValue"].set(self.customEncounter["tileSelections"]["1"]["startingNodes"]["tileValue"])
                e.tileSelections["1"]["startingNodes"]["nodesValue"].set(self.customEncounter["tileSelections"]["1"]["startingNodes"]["nodesValue"])
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
                e.tileSelections["2"]["startingNodes"]["tileValue"].set(self.customEncounter["tileSelections"]["2"]["startingNodes"]["tileValue"])
                e.tileSelections["2"]["startingNodes"]["nodesValue"].set(self.customEncounter["tileSelections"]["2"]["startingNodes"]["nodesValue"])
                e.tileSelections["2"]["traps"]["value"].set(self.customEncounter["tileSelections"]["2"]["traps"]["value"])
                e.tileSelections["2"]["1"]["enemies"]["1"]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["enemies"]["1"]["value"])
                e.tileSelections["2"]["1"]["enemies"]["2"]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["enemies"]["2"]["value"])
                e.tileSelections["2"]["1"]["enemies"]["3"]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["enemies"]["3"]["value"])
                e.tileSelections["2"]["1"]["terrain"]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["terrain"]["value"])
                e.tileSelections["2"]["2"]["enemies"]["1"]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["enemies"]["1"]["value"])
                e.tileSelections["2"]["2"]["enemies"]["2"]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["enemies"]["2"]["value"])
                e.tileSelections["2"]["2"]["enemies"]["3"]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["enemies"]["3"]["value"])
                e.tileSelections["2"]["2"]["terrain"]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["terrain"]["value"])
                e.tileSelections["3"]["startingNodes"]["tileValue"].set(self.customEncounter["tileSelections"]["3"]["startingNodes"]["tileValue"])
                e.tileSelections["3"]["startingNodes"]["nodesValue"].set(self.customEncounter["tileSelections"]["3"]["startingNodes"]["nodesValue"])
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


        def get_coords(self, event=None):
            try:
                log("Start of get_coords")

                e = self.encounterBuilderScroll

                x, y = event.x - 2, event.y - 2
                if 0 <= x <= 400 and 0 <= y <= 685:
                    for icon in e.encounterIcons:
                        if e.encounterIcons[icon]["lockVal"].get():
                            e.encounterIcons[icon]["position"][0].set(x)
                            e.encounterIcons[icon]["position"][1].set(y)

                self.apply_changes()
                
                log("End of get_coords")
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
            self.iconsFrame1.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.iconsFrame2 = ttk.Frame(self.interior)
            self.iconsFrame2.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.iconsFrame3 = ttk.Frame(self.interior)
            self.iconsFrame3.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.separator7 = ttk.Separator(self.interior)
            self.separator7.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.iconsFrame4 = ttk.Frame(self.interior)
            self.iconsFrame4.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.iconsFrame5 = ttk.Frame(self.interior)
            self.iconsFrame5.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            
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

            self.previousStartingTileVal = {
                "1": 0,
                "2": 0,
                "3": 0
            }
            
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
                    "startingNodes": {"tileValue": tk.IntVar(), "nodesValue": tk.IntVar()},
                    "terrainLabel": ttk.Label(frame, text="Terrain")
                }

                self.tileSelections[str(tile)]["label"].bind("<1>", lambda event: event.widget.focus_set())
                self.tileSelections[str(tile)]["startingNodesLabel"].bind("<1>", lambda event: event.widget.focus_set())
                self.tileSelections[str(tile)]["terrainLabel"].bind("<1>", lambda event: event.widget.focus_set())
                self.tileSelections[str(tile)]["enemiesLabel"].bind("<1>", lambda event: event.widget.focus_set())

                self.tileSelections[str(tile)]["traps"]["widget"] = ttk.Checkbutton(frame, text="Traps", variable=self.tileSelections[str(tile)]["traps"]["value"], command=self.topFrame.apply_changes)
                
                self.tileSelections[str(tile)]["startingNodes"]["widgets"] = {
                    "toggle": ttk.Checkbutton(frame, text="Starting Tile", variable=self.tileSelections[str(tile)]["startingNodes"]["tileValue"], command=self.update_lists),
                    "Up": ttk.Radiobutton(frame, text="Up", variable=self.tileSelections[str(tile)]["startingNodes"]["nodesValue"], value=1, command=self.topFrame.apply_changes),
                    "Down": ttk.Radiobutton(frame, text="Down", variable=self.tileSelections[str(tile)]["startingNodes"]["nodesValue"], value=2, command=self.topFrame.apply_changes),
                    "Left": ttk.Radiobutton(frame, text="Left", variable=self.tileSelections[str(tile)]["startingNodes"]["nodesValue"], value=3, command=self.topFrame.apply_changes),
                    "Right": ttk.Radiobutton(frame, text="Right", variable=self.tileSelections[str(tile)]["startingNodes"]["nodesValue"], value=4, command=self.topFrame.apply_changes)
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
            self.tileSelections["1"]["startingNodes"]["widgets"]["toggle"].grid(column=1, row=5, padx=5, pady=5)
            self.tileSelections["1"]["traps"]["widget"].grid(column=1, row=6, padx=(45, 5), pady=5, sticky=tk.W)

            self.tileSelections["2"]["label"].grid(column=0, row=0, padx=5, pady=5, sticky=tk.W, columnspan=4)
            self.tileSelections["3"]["label"].grid(column=0, row=0, padx=5, pady=5, sticky=tk.W, columnspan=4)

            self.currentIcon = None
            self.currentSize = None
            self.currentFile = None
            
            self.iconsFrame1.columnconfigure(4, minsize=180)
            self.iconsFrame1.rowconfigure(7, minsize=70)
            
            self.iconTitle = ttk.Label(self.iconsFrame1, text=(" " * 40) + "Custom Icons", font=("Arial", 16), justify="center")
            self.iconTitle.bind("<1>", lambda event: event.widget.focus_set())
            self.iconTitle.pack(expand=True, fill="x")
            
            self.vcmdX = (self.register(self.callback_x))
            self.vcmdY = (self.register(self.callback_y))

            self.customIconsTreeviewDict = {}
            self.customIconsTreeviewFrame = ttk.Frame(self.iconsFrame2)
            self.customIconsTreeviewFrame.pack(fill="x")
            self.scrollbarTreeviewCustomIcons = ttk.Scrollbar(self.customIconsTreeviewFrame)
            self.scrollbarTreeviewCustomIcons.pack(side="right", fill="y")
            self.treeviewCustomIcons = ttk.Treeview(
                self.customIconsTreeviewFrame,
                selectmode="browse",
                columns=("Name", "Size"),
                yscrollcommand=self.scrollbarTreeviewCustomIcons.set,
                height=9
            )

            self.treeviewCustomIcons.pack(expand=True, fill="both")
            self.scrollbarTreeviewCustomIcons.config(command=self.treeviewCustomIcons.yview)

            self.treeviewCustomIcons.column('#0', width=0)

            self.treeviewCustomIcons.heading("Name", text="Name", anchor=tk.W)
            self.treeviewCustomIcons.heading("Size", text="Size", anchor=tk.W)
            self.treeviewCustomIcons.column("Name", anchor=tk.W)
            self.treeviewCustomIcons.column("Size", anchor=tk.W)
            
            self.treeviewCustomIcons.bind("<<TreeviewSelect>>", self.change_icon)
            
            # Conditions
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Conditions", values=("Conditions", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Conditions", index="end", iid="bleed", values=("   Bleed", "Text"), image=self.app.iconsForCustom["Bleed"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Conditions", index="end", iid="calamity", values=("   Calamity", "Text"), image=self.app.iconsForCustom["Calamity"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Conditions", index="end", iid="corrosion", values=("   Corrosion", "Text"), image=self.app.iconsForCustom["Corrosion"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Conditions", index="end", iid="frostbite", values=("   Frostbite", "Text"), image=self.app.iconsForCustom["Frostbite"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Conditions", index="end", iid="poison", values=("   Poison", "Text"), image=self.app.iconsForCustom["Poison"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Conditions", index="end", iid="stagger", values=("   Stagger", "Text"), image=self.app.iconsForCustom["Stagger"]["treeviewImage"], tags=False, open=False)
            
            # Enemies
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Core", values=("Enemies - Core", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Core", index="end", iid="Crossbow Hollow", values=("   Crossbow Hollow", "Text"), image=self.app.iconsForCustom["Crossbow Hollow"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Core", index="end", iid="Hollow Soldier", values=("   Hollow Soldier", "Text"), image=self.app.iconsForCustom["Hollow Soldier"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Core", index="end", iid="Large Hollow Soldier", values=("   Large Hollow Soldier", "Text"), image=self.app.iconsForCustom["Large Hollow Soldier"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Core", index="end", iid="Sentinel", values=("   Sentinel", "Text"), image=self.app.iconsForCustom["Sentinel"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Core", index="end", iid="Silver Knight Greatbowman", values=("   Silver Knight Greatbowman", "Text"), image=self.app.iconsForCustom["Silver Knight Greatbowman"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Core", index="end", iid="Silver Knight Swordsman", values=("   Silver Knight Swordsman", "Text"), image=self.app.iconsForCustom["Silver Knight Swordsman"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Darkroot", values=("Enemies - Darkroot", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Darkroot", index="end", iid="Demonic Foliage", values=("   Demonic Foliage", "Text"), image=self.app.iconsForCustom["Demonic Foliage"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Darkroot", index="end", iid="Mushroom Child", values=("   Mushroom Child", "Text"), image=self.app.iconsForCustom["Mushroom Child"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Darkroot", index="end", iid="Mushroom Parent", values=("   Mushroom Parent", "Text"), image=self.app.iconsForCustom["Mushroom Parent"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Darkroot", index="end", iid="Plow Scarecrow", values=("   Plow Scarecrow", "Text"), image=self.app.iconsForCustom["Plow Scarecrow"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Darkroot", index="end", iid="Shears Scarecrow", values=("   Shears Scarecrow", "Text"), image=self.app.iconsForCustom["Shears Scarecrow"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Darkroot", index="end", iid="Stone Guardian", values=("   Stone Guardian", "Text"), image=self.app.iconsForCustom["Stone Guardian"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Darkroot", index="end", iid="Stone Knight", values=("   Stone Knight", "Text"), image=self.app.iconsForCustom["Stone Knight"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Explorers", values=("Enemies - Explorers", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Explorers", index="end", iid="Firebomb Hollow", values=("   Firebomb Hollow", "Text"), image=self.app.iconsForCustom["Firebomb Hollow"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Explorers", index="end", iid="Hungry Mimic", values=("   Hungry Mimic", "Text"), image=self.app.iconsForCustom["Hungry Mimic"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Explorers", index="end", iid="Silver Knight Spearman", values=("   Silver Knight Spearman", "Text"), image=self.app.iconsForCustom["Silver Knight Spearman"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Explorers", index="end", iid="Voracious Mimic", values=("   Voracious Mimic", "Text"), image=self.app.iconsForCustom["Voracious Mimic"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Iron Keep", values=("Enemies - Iron Keep", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Iron Keep", index="end", iid="Alonne Bow Knight", values=("   Alonne Bow Knight", "Text"), image=self.app.iconsForCustom["Alonne Bow Knight"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Iron Keep", index="end", iid="Alonne Knight Captain", values=("   Alonne Knight Captain", "Text"), image=self.app.iconsForCustom["Alonne Knight Captain"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Iron Keep", index="end", iid="Alonne Sword Knight", values=("   Alonne Sword Knight", "Text"), image=self.app.iconsForCustom["Alonne Sword Knight"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Iron Keep", index="end", iid="Ironclad Soldier", values=("   Ironclad Soldier", "Text"), image=self.app.iconsForCustom["Ironclad Soldier"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Executioner Chariot", values=("Enemies - Executioner Chariot", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Executioner Chariot", index="end", iid="Black Hollow Mage", values=("   Black Hollow Mage", "Text"), image=self.app.iconsForCustom["Black Hollow Mage"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Executioner Chariot", index="end", iid="Falchion Skeleton", values=("   Falchion Skeleton", "Text"), image=self.app.iconsForCustom["Falchion Skeleton"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Painted World of Ariamis", values=("Enemies - Painted World of Ariamis", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Painted World of Ariamis", index="end", iid="Bonewheel Skeleton", values=("   Bonewheel Skeleton", "Text"), image=self.app.iconsForCustom["Bonewheel Skeleton"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Painted World of Ariamis", index="end", iid="Crow Demon", values=("   Crow Demon", "Text"), image=self.app.iconsForCustom["Crow Demon"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Painted World of Ariamis", index="end", iid="Engorged Zombie", values=("   Engorged Zombie", "Text"), image=self.app.iconsForCustom["Engorged Zombie"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Painted World of Ariamis", index="end", iid="Phalanx", values=("   Phalanx", "Text"), image=self.app.iconsForCustom["Phalanx"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Painted World of Ariamis", index="end", iid="Phalanx Hollow", values=("   Phalanx Hollow", "Text"), image=self.app.iconsForCustom["Phalanx Hollow"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Painted World of Ariamis", index="end", iid="Snow Rat", values=("   Snow Rat", "Text"), image=self.app.iconsForCustom["Snow Rat"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="", index="end", iid="The Sunless City", values=("Enemies - The Sunless City", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="The Sunless City", index="end", iid="Crossbow Hollow TSC", values=("   Crossbow Hollow", "Text"), image=self.app.iconsForCustom["Crossbow Hollow"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="The Sunless City", index="end", iid="Hollow Soldier TSC", values=("   Hollow Soldier", "Text"), image=self.app.iconsForCustom["Hollow Soldier"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="The Sunless City", index="end", iid="Mimic", values=("   Mimic", "Text"), image=self.app.iconsForCustom["Mimic"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="The Sunless City", index="end", iid="Sentinel TSC", values=("   Sentinel", "Text"), image=self.app.iconsForCustom["Sentinel"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="The Sunless City", index="end", iid="Silver Knight Greatbowman TSC", values=("   Silver Knight Greatbowman", "Text"), image=self.app.iconsForCustom["Silver Knight Greatbowman"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="The Sunless City", index="end", iid="Silver Knight Swordsman TSC", values=("   Silver Knight Swordsman", "Text"), image=self.app.iconsForCustom["Silver Knight Swordsman"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Tomb of Giants", values=("Enemies - Tomb of Giants", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Tomb of Giants", index="end", iid="Giant Skeleton Archer", values=("   Giant Skeleton Archer", "Text"), image=self.app.iconsForCustom["Giant Skeleton Archer"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Tomb of Giants", index="end", iid="Giant Skeleton Soldier", values=("   Giant Skeleton Soldier", "Text"), image=self.app.iconsForCustom["Giant Skeleton Soldier"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Tomb of Giants", index="end", iid="Necromancer", values=("   Necromancer", "Text"), image=self.app.iconsForCustom["Necromancer"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Tomb of Giants", index="end", iid="Skeleton Archer", values=("   Skeleton Archer", "Text"), image=self.app.iconsForCustom["Skeleton Archer"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Tomb of Giants", index="end", iid="Skeleton Beast", values=("   Skeleton Beast", "Text"), image=self.app.iconsForCustom["Skeleton Beast"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Tomb of Giants", index="end", iid="Skeleton Soldier", values=("   Skeleton Soldier", "Text"), image=self.app.iconsForCustom["Skeleton Soldier"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Phantoms", values=("Enemies - Phantoms", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Phantoms", index="end", iid="Armorer Dennis", values=("   Armorer Dennis", "Text"), image=self.app.iconsForCustom["Armorer Dennis"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Phantoms", index="end", iid="Fencer Sharron", values=("   Fencer Sharron", "Text"), image=self.app.iconsForCustom["Fencer Sharron"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Phantoms", index="end", iid="Invader Brylex", values=("   Invader Brylex", "Text"), image=self.app.iconsForCustom["Invader Brylex"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Phantoms", index="end", iid="Kirk, Knight of Thorns", values=("   Kirk, Knight of Thorns", "Text"), image=self.app.iconsForCustom["Kirk, Knight of Thorns"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Phantoms", index="end", iid="Longfinger Kirk", values=("   Longfinger Kirk", "Text"), image=self.app.iconsForCustom["Longfinger Kirk"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Phantoms", index="end", iid="Maldron the Assassin", values=("   Maldron the Assassin", "Text"), image=self.app.iconsForCustom["Maldron the Assassin"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Phantoms", index="end", iid="Maneater Mildred", values=("   Maneater Mildred", "Text"), image=self.app.iconsForCustom["Maneater Mildred"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Phantoms", index="end", iid="Marvelous Chester", values=("   Marvelous Chester", "Text"), image=self.app.iconsForCustom["Marvelous Chester"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Phantoms", index="end", iid="Melinda the Butcher", values=("   Melinda the Butcher", "Text"), image=self.app.iconsForCustom["Melinda the Butcher"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Phantoms", index="end", iid="Oliver the Collector", values=("   Oliver the Collector", "Text"), image=self.app.iconsForCustom["Oliver the Collector"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Phantoms", index="end", iid="Paladin Leeroy", values=("   Paladin Leeroy", "Text"), image=self.app.iconsForCustom["Paladin Leeroy"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Phantoms", index="end", iid="Xanthous King Jeremiah", values=("   Xanthous King Jeremiah", "Text"), image=self.app.iconsForCustom["Xanthous King Jeremiah"]["treeviewImage"], tags=False, open=False)
            
            # Effects
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Effects", values=("Effects", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Effects", index="end", iid="Dodge", values=("   Dodge", "Text"), image=self.app.iconsForCustom["Dodge"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Effects", index="end", iid="Leap", values=("   Leap", "Text"), image=self.app.iconsForCustom["Leap"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Effects", index="end", iid="Magic", values=("   Magic", "Text"), image=self.app.iconsForCustom["Magic"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Effects", index="end", iid="Node Attack", values=("   Node Attack", "Text"), image=self.app.iconsForCustom["Node Attack"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Effects", index="end", iid="Push", values=("   Push", "Text"), image=self.app.iconsForCustom["Push"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Effects", index="end", iid="Range", values=("   Range", "Text"), image=self.app.iconsForCustom["Range"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Effects", index="end", iid="Repeat", values=("   Repeat", "Text"), image=self.app.iconsForCustom["Repeat"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Effects", index="end", iid="Shaft", values=("   Shaft", "Text"), image=self.app.iconsForCustom["Shaft"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Effects", index="end", iid="Shift", values=("   Shift", "Text"), image=self.app.iconsForCustom["Shift"]["treeviewImage"], tags=False, open=False)
            
            # Nodes
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Nodes", values=("Nodes", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Nodes", index="end", iid="Enemy Node 1", values=("   Enemy Node 1", "Text"), image=self.app.iconsForCustom["Enemy Node 1"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Nodes", index="end", iid="Enemy Node 2", values=("   Enemy Node 2", "Text"), image=self.app.iconsForCustom["Enemy Node 2"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Nodes", index="end", iid="Enemy Node 3", values=("   Enemy Node 3", "Text"), image=self.app.iconsForCustom["Enemy Node 3"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Nodes", index="end", iid="Enemy Node 4", values=("   Enemy Node 4", "Text"), image=self.app.iconsForCustom["Enemy Node 4"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Nodes", index="end", iid="Terrain Node 1", values=("   Terrain Node 1", "Text"), image=self.app.iconsForCustom["Terrain Node 1"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Nodes", index="end", iid="Terrain Node 2", values=("   Terrain Node 2", "Text"), image=self.app.iconsForCustom["Terrain Node 2"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Nodes", index="end", iid="Terrain Node 3", values=("   Terrain Node 3", "Text"), image=self.app.iconsForCustom["Terrain Node 3"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Nodes", index="end", iid="Terrain Node 4", values=("   Terrain Node 4", "Text"), image=self.app.iconsForCustom["Terrain Node 4"]["treeviewImage"], tags=False, open=False)
            
            # Terrain
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Terrain", values=("Terrain", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Terrain", index="end", iid="Barrel", values=("   Barrel", "Text"), image=self.app.iconsForCustom["Barrel"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Terrain", index="end", iid="Envoy Banner", values=("   Envoy Banner", "Text"), image=self.app.iconsForCustom["Envoy Banner"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Terrain", index="end", iid="Exit", values=("   Exit", "Text"), image=self.app.iconsForCustom["Exit"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Terrain", index="end", iid="Fang Boar", values=("   Fang Boar", "Text"), image=self.app.iconsForCustom["Fang Boar"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Terrain", index="end", iid="Gravestone", values=("   Gravestone", "Text"), image=self.app.iconsForCustom["Gravestone"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Terrain", index="end", iid="Lever", values=("   Lever", "Text"), image=self.app.iconsForCustom["Lever"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Terrain", index="end", iid="Shrine", values=("   Shrine", "Text"), image=self.app.iconsForCustom["Shrine"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Terrain", index="end", iid="Torch", values=("   Torch", "Text"), image=self.app.iconsForCustom["Torch"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Terrain", index="end", iid="Treasure Chest", values=("   Treasure Chest", "Text"), image=self.app.iconsForCustom["Treasure Chest"]["treeviewImage"], tags=False, open=False)
            
            # Other
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Other", values=("Other", ""), tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Other", index="end", iid="Aggro", values=("   Aggro", "Text"), image=self.app.iconsForCustom["Aggro"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Other", index="end", iid="Character Count", values=("   Character Count", "Text"), image=self.app.iconsForCustom["Character Count"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Other", index="end", iid="Die (Black)", values=("   Die (Black)", "Text"), image=self.app.iconsForCustom["Die (Black)"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Other", index="end", iid="Die (Blue)", values=("   Die (Blue)", "Text"), image=self.app.iconsForCustom["Die (Blue)"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Other", index="end", iid="Die (Orange)", values=("   Die (Orange)", "Text"), image=self.app.iconsForCustom["Die (Orange)"]["treeviewImage"], tags=False, open=False)
            self.treeviewCustomIcons.insert(parent="Other", index="end", iid="Eerie", values=("   Eerie", "Text"), image=self.app.iconsForCustom["Eerie"]["treeviewImage"], tags=False, open=False)
            
            # Custom
            self.treeviewCustomIcons.insert(parent="", index="end", iid="Custom", values=("Custom", ""), tags=False, open=False)

            if not path.isfile(baseFolder + "\\lib\\dsbg_shuffle_custom_icons.json".replace("\\", pathSep)):
                with open(baseFolder + "\\lib\\dsbg_shuffle_custom_icons.json".replace("\\", pathSep), "w") as iconsFile:
                    dump({"lookup": {}}, iconsFile)

            with open(baseFolder + "\\lib\\dsbg_shuffle_custom_icons.json".replace("\\", pathSep), "r") as f:
                d = load(f)

            self.customIconsDict = {(tuple(k.split("||")) if k != "lookup" else k): v for k, v in d.items() if k == "lookup" or path.isfile(baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + d[k]["file"])}
            for k in self.customIconsDict:
                if k == "lookup":
                    continue

                if self.customIconsDict[k]["size"] == "iconText":
                    sizeDisplay = "Text"
                elif self.customIconsDict[k]["size"] == "iconEnemy":
                    sizeDisplay = "Enemy/Terrain"
                elif self.customIconsDict[k]["size"] == "iconSet":
                    sizeDisplay = "Set Icon"

                contents = [(self.treeviewCustomIcons.item(child)["values"][1], self.treeviewCustomIcons.item(child)["values"][0]) for child in self.treeviewCustomIcons.get_children()]
                iid = str(len(contents))
                c = (sizeDisplay, self.customIconsDict[k]["label"])
                if self.customIconsDict[k]["label"] not in set([c[1] for c in contents]):
                    tp = self.app.create_image(baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + self.customIconsDict[k]["file"], "iconTreeview", 99, pathProvided=True, extensionProvided=True)
                    self.customIconsTreeviewDict[c[1]] = {
                        "iid": iid,
                        "index": bisect_left(contents, (c[0], c[1])),
                        "values": (c[1], c[0]),
                        "image": tp
                    }
                    self.treeviewCustomIcons.insert(parent="Custom", iid=iid, index=self.customIconsTreeviewDict[c[1]]["index"], values=("   " + self.customIconsTreeviewDict[c[1]]["values"][0], self.customIconsTreeviewDict[c[1]]["values"][1]), image=self.customIconsTreeviewDict[c[1]]["image"], tags=False, open=True)
            
            self.iconNameLabel = ttk.Label(self.iconsFrame3, text="Icon Name\t")
            self.iconNameLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.iconNameLabel.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
            self.iconNameEntry = tk.Text(self.iconsFrame3, width=20, height=1, bg="#181818")
            self.iconNameEntry.grid(column=0, row=0, padx=(80, 25), pady=5, sticky=tk.W)
            
            self.iconView = tk.Label(self.iconsFrame3)
            self.iconView.config(image=self.app.iconBg1PhotoImage)
            self.iconView.image=self.app.iconBg1PhotoImage
            self.iconView.bind("<1>", lambda event: event.widget.focus_set())
            self.iconView.grid(column=0, row=1, padx=5, pady=5, sticky=tk.NSEW, columnspan=2, rowspan=3)
            
            self.iconSizeLabel = ttk.Label(self.iconsFrame3, text="Icon Size\t")
            self.iconSizeLabel.bind("<1>", lambda event: event.widget.focus_set())
            self.iconSizeLabel.grid(column=2, row=0, padx=5, pady=5, sticky=tk.W)
            self.iconSizeVal = tk.IntVar()
            self.iconSizeRadio1 = ttk.Radiobutton(self.iconsFrame3, text="Text", variable=self.iconSizeVal, value=0, command=lambda: self.choose_icon_image(file=self.customIconsDict.get((self.currentIcon, self.currentSize), {}).get("originalFileFullPath", None)))
            self.iconSizeRadio1.grid(column=2, row=1, padx=5, pady=5, sticky=tk.W)
            self.iconSizeRadio2 = ttk.Radiobutton(self.iconsFrame3, text="Enemy/Terrain", variable=self.iconSizeVal, value=1, command=lambda: self.choose_icon_image(file=self.customIconsDict.get((self.currentIcon, self.currentSize), {}).get("originalFileFullPath", None)))
            self.iconSizeRadio2.grid(column=2, row=2, padx=5, pady=5, sticky=tk.W)
            self.iconSizeRadio3 = ttk.Radiobutton(self.iconsFrame3, text="Set Icon", variable=self.iconSizeVal, value=2, command=lambda: self.choose_icon_image(file=self.customIconsDict.get((self.currentIcon, self.currentSize), {}).get("originalFileFullPath", None)))
            self.iconSizeRadio3.grid(column=2, row=3, padx=5, pady=5, sticky=tk.W)
            
            self.chooseIconButton = ttk.Button(self.iconsFrame3, text="Choose Image", width=16, command=lambda x=True: self.choose_icon_image(buttonSource=x))
            self.chooseIconButton.grid(column=3, row=0, padx=5, pady=5, sticky=tk.E)
            self.saveIconButton = ttk.Button(self.iconsFrame3, text="Save Icon", width=16, command=lambda: self.save_custom_icon(file=self.currentIcon))
            self.saveIconButton.grid(column=3, row=1, padx=5, pady=5, sticky=tk.E)
            self.iconImageErrorsVal = tk.StringVar()
            self.iconSaveErrors = tk.Label(self.iconsFrame3, width=26, textvariable=self.iconImageErrorsVal)
            self.iconSaveErrors.bind("<1>", lambda event: event.widget.focus_set())
            self.iconSaveErrors.grid(column=3, row=2, pady=5)
            self.deleteIconButton = ttk.Button(self.iconsFrame3, text="Delete Icon", width=16, command=self.delete_custom_icon)
            self.deleteIconButton.grid(column=3, row=3, padx=5, pady=5, sticky=tk.E)
            self.addToEncounterButton = ttk.Button(self.iconsFrame3, text="Add to Encounter", width=16, command=self.add_icon_to_encounter)
            self.addToEncounterButton.grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)

            self.encounterIcons = {}


        def handle_wait(self, event):
            # cancel the old job
            if self._afterId is not None:
                self.after_cancel(self._afterId)

            # create a new job
            self.after(1, self.topFrame.apply_changes())


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
                layout = self.tileLayoutMenu.get()
                if self.previousnumberOfTilesRadioVal != tiles:
                    self.update_tile_layout_list(tiles)
                    self.update_tile_sections(tiles)
                elif (
                    self.previousStartingTileVal["1"] != self.tileSelections["1"]["startingNodes"]["tileValue"].get()
                    or self.previousStartingTileVal["2"] != self.tileSelections["2"]["startingNodes"]["tileValue"].get()
                    or self.previousStartingTileVal["3"] != self.tileSelections["3"]["startingNodes"]["tileValue"].get()
                    ):
                    self.update_tile_sections(tiles)
                elif tiles == 1 and layout != self.previousTileLayoutMenuVal:
                    self.update_tile_sections(tiles)
                self.previousnumberOfTilesRadioVal = tiles
                self.previousTileLayoutMenuVal = layout

                for tile in range(1, 4):
                    self.previousStartingTileVal[str(tile)] = self.tileSelections[str(tile)]["startingNodes"]["tileValue"].get()

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

                if layout == "1 Tile 4x4":
                    if not self.tileSelections["1"]["3"]["enemies"]["1"]["widget"].winfo_viewable():
                        self.tileSelections["1"]["terrainLabel"].grid_forget()
                        self.tileSelections["1"]["1"]["terrain"]["widget"].grid_forget()
                        self.tileSelections["1"]["2"]["terrain"]["widget"].grid_forget()
                        self.tileSelections["1"]["traps"]["widget"].grid_forget()
                        self.tileSelections["1"]["startingNodesLabel"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["toggle"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Up"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Down"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Left"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Right"].grid_forget()

                        self.tileSelections["1"]["1"]["enemies"]["1"]["widget"].grid(column=0, row=2, padx=(5, 11), pady=5, sticky=tk.W)
                        self.tileSelections["1"]["1"]["enemies"]["2"]["widget"].grid(column=1, row=2, padx=(5, 11), pady=5, sticky=tk.W)
                        self.tileSelections["1"]["1"]["enemies"]["3"]["widget"].grid(column=2, row=2, padx=(5, 11), pady=5, sticky=tk.W)
                        self.tileSelections["1"]["2"]["enemies"]["1"]["widget"].grid(column=0, row=3, padx=(5, 11), pady=5, sticky=tk.W)
                        self.tileSelections["1"]["2"]["enemies"]["2"]["widget"].grid(column=1, row=3, padx=(5, 11), pady=5, sticky=tk.W)
                        self.tileSelections["1"]["2"]["enemies"]["3"]["widget"].grid(column=2, row=3, padx=(5, 11), pady=5, sticky=tk.W)
                        self.tileSelections["1"]["3"]["enemies"]["1"]["widget"].grid(column=0, row=4, padx=(5, 11), pady=5, sticky=tk.W)
                        self.tileSelections["1"]["3"]["enemies"]["2"]["widget"].grid(column=1, row=4, padx=(5, 11), pady=5, sticky=tk.W)
                        self.tileSelections["1"]["3"]["enemies"]["3"]["widget"].grid(column=2, row=4, padx=(5, 11), pady=5, sticky=tk.W)
                        self.tileSelections["1"]["4"]["enemies"]["1"]["widget"].grid(column=0, row=5, padx=(5, 11), pady=5, sticky=tk.W)
                        self.tileSelections["1"]["4"]["enemies"]["2"]["widget"].grid(column=1, row=5, padx=(5, 11), pady=5, sticky=tk.W)
                        self.tileSelections["1"]["4"]["enemies"]["3"]["widget"].grid(column=2, row=5, padx=(5, 11), pady=5, sticky=tk.W)
                        self.tileSelections["1"]["terrainLabel"].grid(column=0, row=6, padx=5, pady=5, sticky=tk.W)
                        self.tileSelections["1"]["1"]["terrain"]["widget"].grid(column=0, row=7, padx=5, pady=5, sticky=tk.W)
                        self.tileSelections["1"]["2"]["terrain"]["widget"].grid(column=0, row=8, padx=5, pady=5, sticky=tk.W)
                        self.tileSelections["1"]["3"]["terrain"]["widget"].grid(column=0, row=9, padx=5, pady=5, sticky=tk.W)
                        self.tileSelections["1"]["4"]["terrain"]["widget"].grid(column=0, row=10, padx=5, pady=5, sticky=tk.W)
                        self.tileSelections["1"]["startingNodes"]["widgets"]["toggle"].grid(column=1, row=7, padx=5, pady=5)
                        self.tileSelections["1"]["traps"]["widget"].grid(column=1, row=8, padx=(45, 5), pady=5, sticky=tk.W)

                    if self.tileSelections["1"]["startingNodes"]["tileValue"].get() and not self.tileSelections["1"]["startingNodesLabel"].winfo_viewable():
                        self.tileSelections["1"]["startingNodesLabel"].grid(column=2, row=7, padx=5, pady=4, sticky=tk.W)
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Up"].grid(column=2, row=8, padx=5, sticky=tk.W)
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Down"].grid(column=2, row=8, padx=(100, 5), sticky=tk.E)
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Left"].grid(column=2, row=9, padx=5, sticky=tk.W)
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Right"].grid(column=2, row=9, padx=(100, 8), sticky=tk.E)
                    else:
                        self.tileSelections["1"]["startingNodesLabel"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Up"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Down"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Left"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Right"].grid_forget()
                else:
                    self.tileSelections["1"]["3"]["enemies"]["1"]["widget"].grid_forget()
                    self.tileSelections["1"]["3"]["enemies"]["2"]["widget"].grid_forget()
                    self.tileSelections["1"]["3"]["enemies"]["3"]["widget"].grid_forget()
                    self.tileSelections["1"]["4"]["enemies"]["1"]["widget"].grid_forget()
                    self.tileSelections["1"]["4"]["enemies"]["2"]["widget"].grid_forget()
                    self.tileSelections["1"]["4"]["enemies"]["3"]["widget"].grid_forget()
                    self.tileSelections["1"]["terrainLabel"].grid_forget()
                    self.tileSelections["1"]["1"]["terrain"]["widget"].grid_forget()
                    self.tileSelections["1"]["2"]["terrain"]["widget"].grid_forget()
                    self.tileSelections["1"]["3"]["terrain"]["widget"].grid_forget()
                    self.tileSelections["1"]["4"]["terrain"]["widget"].grid_forget()
                    self.tileSelections["1"]["startingNodes"]["widgets"]["toggle"].grid_forget()
                    self.tileSelections["1"]["traps"]["widget"].grid_forget()
                    self.tileSelections["1"]["terrainLabel"].grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["1"]["1"]["terrain"]["widget"].grid(column=0, row=5, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["1"]["2"]["terrain"]["widget"].grid(column=0, row=6, padx=5, pady=5, sticky=tk.W)
                    self.tileSelections["1"]["startingNodes"]["widgets"]["toggle"].grid(column=1, row=5, padx=5, pady=5)
                    self.tileSelections["1"]["traps"]["widget"].grid(column=1, row=6, padx=(45, 5), pady=5, sticky=tk.W)

                    if self.tileSelections["1"]["startingNodes"]["tileValue"].get():
                        self.tileSelections["1"]["startingNodesLabel"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Up"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Down"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Left"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Right"].grid_forget()
                        self.tileSelections["1"]["startingNodesLabel"].grid(column=2, row=4, padx=5, pady=4, sticky=tk.W)
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Up"].grid(column=2, row=5, padx=5, sticky=tk.W)
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Down"].grid(column=2, row=5, padx=(100, 5), sticky=tk.E)
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Left"].grid(column=2, row=6, padx=5, sticky=tk.W)
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Right"].grid(column=2, row=6, padx=(100, 8), sticky=tk.E)
                    else:
                        self.tileSelections["1"]["startingNodesLabel"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Up"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Down"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Left"].grid_forget()
                        self.tileSelections["1"]["startingNodes"]["widgets"]["Right"].grid_forget()
                    
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
                    self.tileSelections["2"]["startingNodes"]["widgets"]["toggle"].grid(column=1, row=5, padx=5, pady=5)
                    self.tileSelections["2"]["traps"]["widget"].grid(column=1, row=6, padx=(45, 5), pady=5, sticky=tk.W)

                    if self.tileSelections["2"]["startingNodes"]["tileValue"].get():
                        self.tileSelections["2"]["startingNodesLabel"].grid(column=2, row=4, padx=5, pady=4, sticky=tk.W)
                        self.tileSelections["2"]["startingNodes"]["widgets"]["Up"].grid(column=2, row=5, padx=5, sticky=tk.W)
                        self.tileSelections["2"]["startingNodes"]["widgets"]["Down"].grid(column=2, row=5, padx=(100, 5), sticky=tk.E)
                        self.tileSelections["2"]["startingNodes"]["widgets"]["Left"].grid(column=2, row=6, padx=5, sticky=tk.W)
                        self.tileSelections["2"]["startingNodes"]["widgets"]["Right"].grid(column=2, row=6, padx=(100, 8), sticky=tk.E)
                    else:
                        self.tileSelections["2"]["startingNodesLabel"].grid_forget()
                        self.tileSelections["2"]["startingNodes"]["widgets"]["Up"].grid_forget()
                        self.tileSelections["2"]["startingNodes"]["widgets"]["Down"].grid_forget()
                        self.tileSelections["2"]["startingNodes"]["widgets"]["Left"].grid_forget()
                        self.tileSelections["2"]["startingNodes"]["widgets"]["Right"].grid_forget()
                elif int(tiles) == 1:
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
                    self.tileSelections["2"]["startingNodes"]["widgets"]["toggle"].grid_forget()
                    self.tileSelections["2"]["startingNodes"]["widgets"]["Up"].grid_forget()
                    self.tileSelections["2"]["startingNodes"]["widgets"]["Down"].grid_forget()
                    self.tileSelections["2"]["startingNodes"]["widgets"]["Left"].grid_forget()
                    self.tileSelections["2"]["startingNodes"]["widgets"]["Right"].grid_forget()
                    
                if int(tiles) > 2 and not self.tileSelections["3"]["terrainLabel"].winfo_viewable():
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
                    self.tileSelections["3"]["startingNodes"]["widgets"]["toggle"].grid(column=1, row=5, padx=5, pady=5)
                    self.tileSelections["3"]["traps"]["widget"].grid(column=1, row=6, padx=(45, 5), pady=5, sticky=tk.W)

                    if self.tileSelections["3"]["startingNodes"]["tileValue"].get():
                        self.tileSelections["3"]["startingNodesLabel"].grid(column=2, row=4, padx=5, pady=4, sticky=tk.W)
                        self.tileSelections["3"]["startingNodes"]["widgets"]["Up"].grid(column=2, row=5, padx=5, sticky=tk.W)
                        self.tileSelections["3"]["startingNodes"]["widgets"]["Down"].grid(column=2, row=5, padx=(100, 5), sticky=tk.E)
                        self.tileSelections["3"]["startingNodes"]["widgets"]["Left"].grid(column=2, row=6, padx=5, sticky=tk.W)
                        self.tileSelections["3"]["startingNodes"]["widgets"]["Right"].grid(column=2, row=6, padx=(100, 8), sticky=tk.E)
                    else:
                        self.tileSelections["3"]["startingNodesLabel"].grid_forget()
                        self.tileSelections["3"]["startingNodes"]["widgets"]["Up"].grid_forget()
                        self.tileSelections["3"]["startingNodes"]["widgets"]["Down"].grid_forget()
                        self.tileSelections["3"]["startingNodes"]["widgets"]["Left"].grid_forget()
                        self.tileSelections["3"]["startingNodes"]["widgets"]["Right"].grid_forget()
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
                    self.tileSelections["3"]["startingNodes"]["widgets"]["toggle"].grid_forget()
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

                tree = event.widget

                if not tree.selection() or tree.get_children(tree.selection()[0]):
                    log("End of change_icon")
                    return
                
                if tree.parent(tree.selection()[0]) != "Custom":
                    self.iconSizeVal.set(0)
                    self.iconSizeRadio1.config(state=tk.DISABLED)
                    self.iconSizeRadio2.config(state=tk.DISABLED)
                    self.iconSizeRadio3.config(state=tk.DISABLED)
                    self.choose_icon_image(image=self.app.iconsForCustom[tree.item(tree.selection()[0])["values"][0].strip()]["photoImageBg1"])
                else:
                    self.iconSizeRadio1.config(state=tk.ACTIVE)
                    self.iconSizeRadio2.config(state=tk.ACTIVE)
                    self.iconSizeRadio3.config(state=tk.ACTIVE)
                    lookup = tuple(self.customIconsDict["lookup"][tree.item(tree.selection()[0])["values"][0].strip()])

                    if not self.customIconsDict[lookup]:
                        log("End of change_icon")
                        return

                    self.currentIcon = self.customIconsDict[lookup]["originalFileName"]
                    self.currentSize = self.customIconsDict[lookup]["size"]
                    self.currentFile = self.customIconsDict[lookup]["file"]
                    self.iconNameEntry.delete("1.0", tk.END)
                    self.iconNameEntry.insert("end-1c", self.customIconsDict[lookup]["label"])

                    if self.customIconsDict[lookup]["size"] == "iconText":
                        self.iconSizeVal.set(0)
                    elif self.customIconsDict[lookup]["size"] == "iconEnemy":
                        self.iconSizeVal.set(1)
                    elif self.customIconsDict[lookup]["size"] == "iconSet":
                        self.iconSizeVal.set(2)

                    self.choose_icon_image(file=baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + self.customIconsDict[lookup]["file"])
                
                log("End of change_icon")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def delete_custom_icon(self, event=None):
            try:
                log("Start of delete_custom_icon")

                tree = self.treeviewCustomIcons

                if not tree.selection() or tree.parent(tree.selection()[0]) != "Custom":
                    log("End delete_custom_icon")
                    return
                
                sel = tree.selection()
                
                del self.customIconsDict[(self.currentIcon, self.currentSize)]
                
                tree.delete(sel)

                self.iconNameEntry.delete("1.0", tk.END)
                self.iconImageErrorsVal.set("")
                self.iconView.config(image=self.app.iconBg1PhotoImage)
                self.iconView.image=self.app.iconBg1PhotoImage

                self.topFrame.apply_changes()
                
                log("End of delete_custom_icon")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def save_custom_icon(self, file, event=None):
            try:
                log("Start of save_custom_icon")

                errors = []
                icon = self.iconNameEntry.get("1.0", "end").strip()
                
                if self.iconSizeVal.get() == 0:
                    size = "iconText"
                    sizeDisplay = "Text"
                elif self.iconSizeVal.get() == 1:
                    size = "iconEnemy"
                    sizeDisplay = "Enemy/Terrain"
                elif self.iconSizeVal.get() == 2:
                    size = "iconSet"
                    sizeDisplay = "Set Icon"

                if not icon:
                    errors.append("name")
                if (file, size) not in self.customIconsDict or not self.customIconsDict[(file, size)]["image"]:
                    errors.append("custom image")

                if errors:
                    errorText = "Required: " + ", ".join(errors)
                    self.iconImageErrorsVal.set(errorText)
                    return

                if not file:
                    log("End of save_custom_icon")
                    return

                self.iconImageErrorsVal.set("")

                oldIconCount = sum([1 for k in self.customIconsDict if "label" in self.customIconsDict[k]])

                self.customIconsDict[(file, size)]["label"] = icon
                
                newIconCount = sum([1 for k in self.customIconsDict if "label" in self.customIconsDict[k]])

                self.customIconsDict["lookup"][icon] = (file, size)

                i, _ = self.app.create_image(self.customIconsDict[(file, size)]["originalFileFullPath"], self.customIconsDict[(file, size)]["size"], 99, pathProvided=True, extensionProvided=True)

                newFile = baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + self.customIconsDict[(file, size)]["file"]
                if not path.isfile(newFile):
                    i.save(newFile)

                self.currentFile = deepcopy(self.customIconsDict[(file, size)]["file"])

                if oldIconCount == newIconCount:
                    self.treeviewCustomIcons.item(self.customIconsDict[(file, size)]["iid"], values=(icon, sizeDisplay))
                else:
                    contents = [(self.treeviewCustomIcons.item(child)["values"][1], self.treeviewCustomIcons.item(child)["values"][0]) for child in self.treeviewCustomIcons.get_children()]
                    iid = str(len(contents))
                    c = (sizeDisplay, self.customIconsDict[(file, size)]["label"])
                    if icon not in set([c[1] for c in contents]):
                        self.customIconsTreeviewDict[c[1]] = {
                            "iid": iid,
                            "index": bisect_left(contents, (c[0], c[1])),
                            "values": (c[1], c[0])
                        }
                        self.customIconsDict[(file, size)]["treeviewImage"] = self.app.create_image(baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + self.customIconsDict[(file, size)]["file"], "iconTreeview", 99, pathProvided=True, extensionProvided=True)
                        self.customIconsTreeviewDict[c[1]]["image"] = self.customIconsDict[(file, size)]["treeviewImage"]
                        self.treeviewCustomIcons.insert(parent="Custom", iid=iid, index=self.customIconsTreeviewDict[c[1]]["index"], values=("   " + self.customIconsTreeviewDict[c[1]]["values"][0], self.customIconsTreeviewDict[c[1]]["values"][1]), image=self.customIconsTreeviewDict[c[1]]["image"], tags=False, open=True)
                        self.customIconsDict[(file, size)]["iid"] = iid
                        self.treeviewCustomIcons.focus(iid)
                        self.treeviewCustomIcons.selection_set(iid)
                    else:
                        self.treeviewCustomIcons.item(self.customIconsTreeviewDict[c[1]]["iid"], values=(c[1], c[0]))

                saveDict = {}
                for key in self.customIconsDict:
                    if key == "lookup":
                        saveDict["lookup"] = self.customIconsDict["lookup"]
                    elif "label" in self.customIconsDict[key]:
                        saveDict["||".join(key)] = {k: v for k, v in self.customIconsDict[key].items() if "mage" not in k}

                with open(baseFolder + "\\lib\\dsbg_shuffle_custom_icons.json".replace("\\", pathSep), "w") as iconsFile:
                    dump(saveDict, iconsFile)
                
                self.topFrame.apply_changes()

                self.iconImageErrorsVal.set("Saved " + datetime.now().strftime("%H:%M:%S"))

                log("End of save_custom_icon")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def choose_icon_image(self, event=None, file=None, buttonSource=False, image=None):
            try:
                log("Start of choose_icon_image, file={}".format(str(file)))

                if image:
                    self.iconViewImg = image
                else:
                    if not buttonSource and not self.currentIcon:
                        log("\tEnd of choose_icon_image")
                        return
                    
                    if self.iconSizeVal.get() == 0:
                        size = "iconText"
                    elif self.iconSizeVal.get() == 1:
                        size = "iconEnemy"
                    elif self.iconSizeVal.get() == 2:
                        size = "iconSet"

                    self.currentSize = deepcopy(size)
                    
                    if buttonSource:
                        file = filedialog.askopenfilename(initialdir=baseFolder)

                        self.currentIcon = path.basename(file)

                        # If they canceled, do nothing.
                        if not file:
                            return
                        
                        if (self.currentIcon, size) in self.customIconsDict:
                            self.app.set_bindings_buttons_menus(False)
                            p = PopupWindow(self.root, labelText="Replace existing icon image?", yesButton=True, noButton=True)
                            self.app.set_bindings_buttons_menus(True)
                            if not p.answer:
                                return
                        
                        fileName = path.splitext(self.currentIcon)
                        self.currentFile = fileName[0] + fileName[1]

                        i, p = self.app.create_image(file, size, 99, pathProvided=True, extensionProvided=True)

                    if (self.currentIcon, size) not in self.customIconsDict:
                        i, p = self.app.create_image(file, size, 99, pathProvided=True, extensionProvided=True)
                        self.customIconsDict[(self.currentIcon, size)] = {
                            "originalFileName": self.currentFile,
                            "originalFileFullPath": file,
                            "file": self.currentIcon[:-4] + "_" + size + ".png",
                            "size": size,
                            "image": i,
                            "photoImage": p
                        }
                    elif "photoImage" not in self.customIconsDict[(self.currentIcon, size)]:
                        i, p = self.app.create_image(file, size, 99, pathProvided=True, extensionProvided=True)
                        self.customIconsDict[(self.currentIcon, size)]["image"] = i
                        self.customIconsDict[(self.currentIcon, size)]["photoImage"] = p
                    else:
                        p = self.customIconsDict[(self.currentIcon, size)]["photoImage"]

                    w, h = self.customIconsDict[(self.currentIcon, size)]["image"].size
                    self.customIconsDict[(self.currentIcon, size)]["offset"] = (w / 2, h / 2)
                    
                    _, self.iconViewImg = self.app.create_image(file, size, 99, pathProvided=True, extensionProvided=True, addToBg1=True)

                self.iconView.config(image=self.iconViewImg)
                self.iconView.image=self.iconViewImg

                self.iconImageErrorsVal.set("")
                
                if not buttonSource and self.treeviewCustomIcons.parent(self.treeviewCustomIcons.selection()[0]) == "Custom":
                    self.iconSizeRadio1.config(state=tk.ACTIVE)
                    self.iconSizeRadio2.config(state=tk.ACTIVE)
                    self.iconSizeRadio3.config(state=tk.ACTIVE)

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


        def add_icon_to_encounter(self, event=None):
            try:
                log("Start of add_icon_to_encounter")

                tree = self.treeviewCustomIcons

                if not tree.selection() or tree.get_children(tree.selection()[0]):
                    log("End of add_icon_to_encounter")
                    return

                if not self.encounterIcons:
                    id = 0
                else:
                    id = max(self.encounterIcons.keys()) + 3

                self.encounterIcons[id] = {}

                if tree.parent(tree.selection()[0]) == "Custom":
                    label = tree.item(tree.selection()[0])["values"][0].strip()
                    lookup = tuple(self.customIconsDict["lookup"][label])
                    file = self.customIconsDict[lookup]["file"]
                    size = self.customIconsDict[lookup]["size"]
                    _, image = self.app.create_image(baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + file, size, 99, pathProvided=True, extensionProvided=True, addToBg2=True)
                else:
                    image = self.app.iconsForCustom[tree.item(tree.selection()[0])["values"][0].strip()]["photoImageBg2"]

                self.encounterIcons[id] = {
                    "lookup": tree.item(tree.selection()[0])["values"][0].strip() if tree.parent(tree.selection()[0]) != "Custom" else lookup,
                    "view": tk.Label(self.iconsFrame4),
                    "viewImage": image,
                    "noteVal": tk.StringVar(),
                    "xLabel": ttk.Label(self.iconsFrame4, text="x (0-400):"),
                    "yLabel": ttk.Label(self.iconsFrame4, text="y (0-685):"),
                    "position": (tk.StringVar(), tk.StringVar()),
                    "lockVal": tk.IntVar(),
                    "remove": ttk.Button(self.iconsFrame4, text="Remove Icon", width=16, command=lambda: self.remove_icon_from_encounter(id))
                }

                self.encounterIcons[id]["note"] = ttk.Entry(self.iconsFrame4, textvariable=self.encounterIcons[id]["noteVal"], width=15)
                self.encounterIcons[id]["xEntry"] = ttk.Entry(self.iconsFrame4, textvariable=self.encounterIcons[id]["position"][0], width=4, validate="all", validatecommand=(self.vcmdX, "%P"))
                self.encounterIcons[id]["yEntry"] = ttk.Entry(self.iconsFrame4, textvariable=self.encounterIcons[id]["position"][1], width=4, validate="all", validatecommand=(self.vcmdY, "%P"))
                self.encounterIcons[id]["lock"] = ttk.Checkbutton(self.iconsFrame4, text="Click Position", variable=self.encounterIcons[id]["lockVal"], style="Switch.TCheckbutton")
                self.encounterIcons[id]["view"].config(image=self.encounterIcons[id]["viewImage"])
                self.encounterIcons[id]["view"].image = self.encounterIcons[id]["viewImage"]

                if id in self.encounterIcons:
                    #self.encounterIcons[id]["noteVal"].set()
                    lookup = self.encounterIcons[id]["lookup"]
                    posList = [self.topFrame.customEncounter["icons"][l]["position"] for l in self.topFrame.customEncounter["icons"] if self.topFrame.customEncounter["icons"][l]["lookup"] == lookup]
                    if posList:
                        pos = posList[0]
                        if lookup in set([self.topFrame.customEncounter["icons"][l]["lookup"] for l in self.topFrame.customEncounter["icons"]]) and pos[0] and pos[1]:
                            self.encounterIcons[id]["position"][0].set(pos[0])
                            self.encounterIcons[id]["position"][1].set(pos[1])

                self.encounterIcons[id]["view"].bind("<1>", lambda event: event.widget.focus_set())
                self.encounterIcons[id]["xLabel"].bind("<1>", lambda event: event.widget.focus_set())
                self.encounterIcons[id]["xEntry"].bind("<KeyRelease>", self.handle_wait)
                self.encounterIcons[id]["yLabel"].bind("<1>", lambda event: event.widget.focus_set())
                self.encounterIcons[id]["yEntry"].bind("<KeyRelease>", self.handle_wait)
                self.encounterIcons[id]["lock"].bind("<1>", lambda event: self.toggle_position_switches(event=event, id=id))
                self.encounterIcons[id]["view"].grid(column=0, row=id, padx=5, pady=(20, 5), sticky=tk.W, rowspan=2)
                self.encounterIcons[id]["note"].grid(column=0, row=id+2, padx=5, pady=5, sticky=tk.W)
                self.encounterIcons[id]["xLabel"].grid(column=1, row=id, padx=5, pady=(20, 6), sticky=tk.W)
                self.encounterIcons[id]["xEntry"].grid(column=2, row=id, padx=5, pady=(20, 5), sticky=tk.W)
                self.encounterIcons[id]["yLabel"].grid(column=1, row=id+1, padx=5, sticky=tk.W)
                self.encounterIcons[id]["yEntry"].grid(column=2, row=id+1, padx=5, pady=(3, 0), sticky=tk.W)
                self.encounterIcons[id]["lock"].grid(column=1, row=id+2, padx=5, pady=5, sticky=tk.W, columnspan=2)
                self.encounterIcons[id]["remove"].grid(column=4, row=id, padx=11, pady=(20, 5), sticky=tk.E, rowspan=3)

                log("End of add_icon_to_encounter")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def remove_icon_from_encounter(self, id, event=None):
            try:
                log("Start of remove_icon_from_encounter")

                self.encounterIcons[id]["view"].grid_forget()
                self.encounterIcons[id]["posLabel"].grid_forget()
                self.encounterIcons[id]["xLabel"].grid_forget()
                self.encounterIcons[id]["xEntry"].grid_forget()
                self.encounterIcons[id]["yLabel"].grid_forget()
                self.encounterIcons[id]["yEntry"].grid_forget()
                self.encounterIcons[id]["lock"].grid_forget()
                self.encounterIcons[id]["remove"].grid_forget()

                del self.encounterIcons[id]

                self.topFrame.apply_changes()

                log("End of remove_icon_from_encounter")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def toggle_position_switches(self, id, event=None):
            try:
                log("Start of toggle_position_switches")

                if not event:
                    log("End of toggle_position_switches")
                    return

                event.widget.focus_set()

                if self.encounterIcons[id]["lockVal"].get() == 0:
                    for i in [i for i in self.encounterIcons if i != id]:
                        if self.encounterIcons[i]["lockVal"].get() == 1:
                            self.encounterIcons[i]["lock"].invoke()

                log("End of toggle_position_switches")
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