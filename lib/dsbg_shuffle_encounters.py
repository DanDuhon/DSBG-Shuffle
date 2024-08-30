try:
    import tkinter as tk
    from collections import Counter
    from copy import deepcopy
    from json import dump, load
    from os import path
    from PIL import ImageTk, ImageDraw, UnidentifiedImageError
    from random import choice
    from tkinter import filedialog, ttk

    from dsbg_shuffle_enemies import enemiesDict, enemyIds, enemyNames
    from dsbg_shuffle_treasure import pick_treasure, treasureSwapEncounters
    from dsbg_shuffle_utility import PopupWindow, VerticalScrolledFrame, clear_other_tab_images, error_popup, log, set_display_bindings_by_tab, baseFolder, font, fontEncounterName, fontFlavor, pathSep


    class EncounterBuilderFrame(VerticalScrolledFrame):
        def __init__(self, app, root):
            super(EncounterBuilderFrame, self).__init__(parent=app)
            self.app = app
            self.root = root

            self.customEncountersButtonFrame = ttk.Frame(self.interior)
            self.customEncountersButtonFrame.pack(side=tk.TOP, anchor=tk.W)

            self.newEncounterButton = ttk.Button(self.customEncountersButtonFrame, text="New Encounter", width=16, command=self.new_custom_encounter)
            self.newEncounterButton.grid(column=0, row=0, padx=5, pady=5)
            self.applyButton = ttk.Button(self.customEncountersButtonFrame, text="Apply Changes", width=16, command=self.apply_changes)
            self.applyButton.grid(column=1, row=0, padx=5, pady=5)
            self.loadButton = ttk.Button(self.customEncountersButtonFrame, text="Load Encounter", width=16, command=self.load_custom_encounter)
            self.loadButton.grid(column=2, row=0, padx=5, pady=5)
            self.saveButton = ttk.Button(self.customEncountersButtonFrame, text="Save Encounter", width=16, command=self.save_custom_encounter)
            self.saveButton.grid(column=3, row=0, padx=5, pady=5)
            
            self.infoFrame1 = ttk.Frame(self.interior)
            self.infoFrame1.pack(side=tk.TOP, anchor=tk.W)
            self.infoFrame2 = ttk.Frame(self.interior)
            self.infoFrame2.pack(side=tk.TOP, anchor=tk.W)
            self.infoFrame3 = ttk.Frame(self.interior)
            self.infoFrame3.pack(side=tk.TOP, anchor=tk.W)
            self.infoFrame4 = ttk.Frame(self.interior)
            self.infoFrame4.pack(side=tk.TOP, anchor=tk.W)
            self.infoFrame5 = ttk.Frame(self.interior)
            self.infoFrame5.pack(side=tk.TOP, anchor=tk.W)
            self.separator1 = ttk.Separator(self.interior)
            self.separator1.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.layoutFrame1 = ttk.Frame(self.interior)
            self.layoutFrame1.pack(side=tk.TOP, anchor=tk.W)
            self.layoutFrame2 = ttk.Frame(self.interior)
            self.layoutFrame2.pack(side=tk.TOP, anchor=tk.W)
            self.layoutFrame3 = ttk.Frame(self.interior)
            self.layoutFrame3.pack(side=tk.TOP, anchor=tk.W)
            self.separator2 = ttk.Separator(self.interior)
            self.separator2.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=5, fill="x")
            self.iconsFrame = ttk.Frame(self.interior)
            self.iconsFrame.pack(side=tk.TOP, anchor=tk.W)
            self.iconsFrame2 = ttk.Frame(self.interior)
            self.iconsFrame2.pack(side=tk.TOP, anchor=tk.W)
            
            self.encounterNameLabel = ttk.Label(self.infoFrame1, text="Encounter\nName\t")
            self.encounterNameLabel.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)
            self.encounterNameEntry = tk.Text(self.infoFrame1, width=17, height=2)
            self.encounterNameEntry.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.levelLabel = ttk.Label(self.infoFrame1, text="Encounter\nLevel")
            self.levelLabel.pack(side=tk.LEFT, anchor=tk.W, padx=(40, 5), pady=5)
            self.levelMenuList = ["1", "2", "3", "4"]
            self.levelMenuVal = tk.StringVar()
            self.levelMenuVal.set(self.levelMenuList[0])
            self.levelMenu = ttk.Combobox(self.infoFrame1, width=5, state="readonly", values=self.levelMenuList, textvariable=self.levelMenuVal)
            self.levelMenu.bind("<<ComboboxSelected>>", self.update_row_list)
            self.levelMenu.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.numberOfTilesLabel = ttk.Label(self.infoFrame1, text="Number\nof Tiles")
            self.numberOfTilesLabel.pack(side=tk.LEFT, anchor=tk.W, padx=(40, 5), pady=5)
            self.numberOfTilesMenuList = ["1", "2", "3"]
            self.numberOfTilesMenuVal = tk.StringVar()
            self.numberOfTilesMenuVal.set(self.numberOfTilesMenuList[0])
            self.previousNumberOfTilesMenuVal = ""
            self.numberOfTilesMenu = ttk.Combobox(self.infoFrame1, width=5, state="readonly", values=self.numberOfTilesMenuList, textvariable=self.numberOfTilesMenuVal)
            self.numberOfTilesMenu.bind("<<ComboboxSelected>>", self.update_lists)
            self.numberOfTilesMenu.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.flavorLabel = ttk.Label(self.infoFrame2, text="Flavor\nText\t")
            self.flavorLabel.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)
            self.flavorEntry = tk.Text(self.infoFrame2, width=70, height=2)
            self.flavorEntry.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.objectiveLabel = ttk.Label(self.infoFrame3, text="Objective\t")
            self.objectiveLabel.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)
            self.objectiveEntry = tk.Text(self.infoFrame3, width=70, height=2)
            self.objectiveEntry.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.rewardSoulsPerPlayerVal = tk.IntVar()
            self.rewardSoulsPerPlayer = ttk.Checkbutton(self.infoFrame4, text="Souls Reward\nPer Player", variable=self.rewardSoulsPerPlayerVal)
            self.rewardSoulsPerPlayer.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)
            self.rewardSoulsPerPlayer.state(["!alternate"])
            
            self.shortcutVal = tk.IntVar()
            self.shortcut = ttk.Checkbutton(self.infoFrame4, text="Shortcut\nReward", variable=self.shortcutVal)
            self.shortcut.grid(column=2, row=0, padx=5, pady=5, sticky=tk.W)
            self.shortcut.state(["!alternate"])
            
            self.rewardSoulsLabel = ttk.Label(self.infoFrame4, text="Souls\nReward\t")
            self.rewardSoulsLabel.grid(column=0, row=1, padx=5, pady=5)
            self.rewardSoulsEntry = tk.Text(self.infoFrame4, width=17, height=2)
            self.rewardSoulsEntry.grid(column=1, row=1, padx=5, pady=5, sticky=tk.W)
            
            self.rewardSearchLabel = ttk.Label(self.infoFrame4, text="Search\nReward\t")
            self.rewardSearchLabel.grid(column=0, row=2, padx=5, pady=5)
            self.rewardSearchEntry = tk.Text(self.infoFrame4, width=17, height=2)
            self.rewardSearchEntry.grid(column=1, row=2, padx=5, pady=5, sticky=tk.W)
            
            self.rewardDrawLabel = ttk.Label(self.infoFrame4, text="Draw\nReward\t")
            self.rewardDrawLabel.grid(column=0, row=3, padx=5, pady=5)
            self.rewardDrawEntry = tk.Text(self.infoFrame4, width=17, height=2)
            self.rewardDrawEntry.grid(column=1, row=3, padx=5, pady=5, sticky=tk.W)
            
            self.rewardTrialLabel = ttk.Label(self.infoFrame4, text="Trial\nReward\t")
            self.rewardTrialLabel.grid(column=0, row=4, padx=5, pady=5)
            self.rewardTrialEntry = tk.Text(self.infoFrame4, width=17, height=2)
            self.rewardTrialEntry.grid(column=1, row=4, padx=5, pady=5, sticky=tk.W)
            
            self.keywordsLabel = ttk.Label(self.infoFrame4, text="Keywords")
            self.keywordsLabel.grid(column=2, row=1, padx=(24, 5), pady=5, sticky=tk.W)
            self.keywordsEntry = tk.Text(self.infoFrame4, width=39, height=2)
            self.keywordsEntry.grid(column=3, row=1, pady=5, columnspan=2, sticky=tk.W)
            
            self.specialRulesLabel = ttk.Label(self.infoFrame4, text="Special\nRules")
            self.specialRulesLabel.grid(column=2, row=2, padx=(24, 5), pady=5, sticky=tk.W)
            self.specialRulesEntry = tk.Text(self.infoFrame4, width=39, height=8)
            self.specialRulesEntry.grid(column=3, row=2, pady=5, rowspan=3, columnspan=2, sticky=tk.W)
            
            self.tileLayoutLabel = ttk.Label(self.infoFrame5, text="Tile\nLayout\t")
            self.tileLayoutLabel.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            self.tileLayoutMenuList = []
            self.tileLayoutMenuVal = tk.StringVar()
            self.tileLayoutMenu = ttk.Combobox(self.infoFrame5, width=30, state="readonly", values=self.tileLayoutMenuList, textvariable=self.tileLayoutMenuVal)
            self.tileLayoutMenu.config(state="disabled")
            self.tileLayoutMenu.bind("<KeyRelease>", self.search_layout_combobox)
            self.tileLayoutMenu.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.rowSelectionLabel = ttk.Label(self.layoutFrame1, text="Selected\nRow\t\t")
            self.rowSelectionLabel.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            self.rowSelectionMenuList = []
            self.rowSelectionMenuVal = tk.StringVar()
            self.rowSelectionMenu = ttk.Combobox(self.layoutFrame1, width=5, state="readonly", values=self.rowSelectionMenuList, textvariable=self.rowSelectionMenuVal)
            self.rowSelectionMenu.bind("<<ComboboxSelected>>", self.change_row)
            self.rowSelectionMenu.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.tileSelectionLabel = ttk.Label(self.layoutFrame1, text="\tSelected\n\tTile\t")
            self.tileSelectionLabel.pack(side=tk.LEFT, anchor=tk.E, padx=(140, 5), pady=5)
            self.tileSelectionMenuList = []
            self.tileSelectionMenuVal = tk.StringVar()
            self.tileSelectionMenu = ttk.Combobox(self.layoutFrame1, width=5, state="readonly", values=self.tileSelectionMenuList, textvariable=self.tileSelectionMenuVal)
            self.tileSelectionMenu.bind("<<ComboboxSelected>>", self.change_tile)
            self.tileSelectionMenu.pack(side=tk.LEFT, anchor=tk.W, padx=10, pady=5)

            self.icons = {}
            self.currentIcon = {
                "label": None,
                "file": None,
                "image": None,
                "photoImage": None,
                "size": None,
                "position": None
            }
            
            self.iconWarningLabel = ttk.Label(self.iconsFrame, text="Please check the wiki for details on how to use custom icons!")
            self.iconWarningLabel.grid(column=0, row=0, padx=5, pady=5, columnspan=6, sticky=tk.W)
            self.iconLabel = ttk.Label(self.iconsFrame, text="Custom Icons\t")
            self.iconLabel.grid(column=0, row=1, padx=5, pady=5)
            self.iconMenuList = []
            self.iconMenuVal = tk.StringVar()
            self.iconMenu = ttk.Combobox(self.iconsFrame, width=24, state="readonly", values=self.iconMenuList, textvariable=self.iconMenuVal)
            self.iconMenu.bind("<<ComboboxSelected>>", self.change_icon)
            self.iconMenu.grid(column=1, row=1, padx=5, pady=5, columnspan=4, sticky=tk.W)
            self.deleteIconButton = ttk.Button(self.iconsFrame, text="Delete Icon", width=16, command=self.delete_custom_icon)
            self.deleteIconButton.grid(column=5, row=1, padx=(5, 0), pady=5)
            
            self.iconNameLabel = ttk.Label(self.iconsFrame, text="Icon Name\t")
            self.iconNameLabel.grid(column=0, row=2, padx=5, pady=5)
            self.iconNameEntry = tk.Text(self.iconsFrame, width=26, height=1)
            self.iconNameEntry.grid(column=1, row=2, padx=5, pady=5, columnspan=4)
            self.saveIconButton = ttk.Button(self.iconsFrame, text="Save Icon", width=16, command=self.save_custom_icon)
            self.saveIconButton.grid(column=5, row=2, padx=(5, 0), pady=5)
            self.iconSaveErrorsVal = tk.StringVar()
            self.iconSaveErrors = tk.Label(self.iconsFrame, width=26, height=2, textvariable=self.iconSaveErrorsVal)
            self.iconSaveErrors.grid(column=6, row=2, pady=5, sticky=tk.W)
            
            self.iconSizeLabel = ttk.Label(self.iconsFrame, text="Icon Size\t")
            self.iconSizeLabel.grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)
            self.iconSizeMenuList = ["Text", "Enemy/Terrain", "Set Icon"]
            self.iconSizeMenuVal = tk.StringVar()
            self.iconSizeMenu = ttk.Combobox(self.iconsFrame, width=24, state="readonly", values=self.iconSizeMenuList, textvariable=self.iconSizeMenuVal)
            self.iconSizeMenu.grid(column=1, row=3, padx=5, pady=5, columnspan=4, sticky=tk.W)
            self.chooseIconButton = ttk.Button(self.iconsFrame, text="Choose Image", width=16, command=self.choose_icon_image)
            self.chooseIconButton.grid(column=5, row=3, padx=(5, 0), pady=5)
            self.iconImageErrorsVal = tk.StringVar()
            self.iconImageErrors = tk.Label(self.iconsFrame, width=26, height=2, textvariable=self.iconImageErrorsVal)
            self.iconImageErrors.grid(column=6, row=3, pady=5, rowspan=2, sticky=tk.NW)
            
            vcmdX = (self.register(self.callback_x))
            vcmdY = (self.register(self.callback_y))
            self.positionLabel = ttk.Label(self.iconsFrame, text="Position\t")
            self.positionLabel.grid(column=0, row=4, padx=5, pady=5, sticky=tk.W)
            self.xPositionLabel = ttk.Label(self.iconsFrame, text="x:")
            self.xPositionLabel.grid(column=1, row=4, padx=5, pady=5, sticky=tk.W)
            self.xPositionVal = tk.StringVar()
            self.xPositionEntry = ttk.Entry(self.iconsFrame, textvariable=self.xPositionVal, width=4, validate="all", validatecommand=(vcmdX, "%P"))
            self.xPositionEntry.grid(column=2, row=4, padx=5, pady=5, sticky=tk.W)
            self.yPositionLabel = ttk.Label(self.iconsFrame, text="y:")
            self.yPositionLabel.grid(column=3, row=4, padx=5, pady=5, sticky=tk.E)
            self.yPositionVal = tk.StringVar()
            self.yPositionEntry = ttk.Entry(self.iconsFrame, textvariable=self.yPositionVal, width=4, validate="all", validatecommand=(vcmdY, "%P"))
            self.yPositionEntry.grid(column=4, row=4, padx=5, pady=5, sticky=tk.E)
            self.xPositionLabel = ttk.Label(self.iconsFrame, text="x: 0-400\ty: 0-685")
            self.xPositionLabel.grid(column=5, row=4, padx=5, pady=5, sticky=tk.W)
            self.iconView = tk.Label(self.iconsFrame, width=26, height=2)
            self.iconView.grid(column=6, row=4, pady=5, rowspan=2, sticky=tk.NSEW)

            self.eNames = [""] + enemyNames
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

            self.selectedTile = 1
            self.selectedRow = 1

            self.tileSelections = {}

            self.customEncounter = {}

            self.new_custom_encounter()


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
                if val == "":
                    w["values"] = self.eNames
                else:
                    w["values"] = [e for e in self.eNames if val.lower() in e.lower()]
                
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


        def change_tile(self, event):
            try:
                log("Start of change_tile")

                w = event.widget
                val = w.get()
                if self.selectedTile == int(val):
                    return
                
                self.tileSelections[self.selectedTile]["traps"]["widget"].grid_forget()
                self.tileSelections[self.selectedTile]["startingTile"]["widget"].grid_forget()
                self.tileSelections[self.selectedTile]["startingNodes"]["widget"].grid_forget()
                
                self.selectedTile = int(val)
                
                self.tileSelections[self.selectedTile]["traps"]["widget"].grid(column=3, row=0, padx=5, pady=5, sticky=tk.W)
                self.tileSelections[self.selectedTile]["startingTile"]["widget"].grid(column=3, row=1, padx=5, pady=5, sticky=tk.W)
                self.tileSelections[self.selectedTile]["startingNodes"]["widget"].grid(column=3, row=2, padx=5, pady=5)

                for tile in range(1, 4):
                    if tile != self.selectedTile:
                        for row in range(1, 5):
                            self.tileSelections[tile][row]["enemyLabel"].grid_forget()
                            self.tileSelections[tile][row]["enemies"][1]["widget"].grid_forget()
                            self.tileSelections[tile][row]["enemies"][2]["widget"].grid_forget()
                            self.tileSelections[tile][row]["enemies"][3]["widget"].grid_forget()
                            self.tileSelections[tile][row]["terrainLabel"].grid_forget()
                            self.tileSelections[tile][row]["terrain"]["widget"].grid_forget()

                self.change_row()
                
                log("End of change_tile")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def change_row(self, event=None):
            try:
                log("Start of change_row")

                if self.selectedRow == int(self.rowSelectionMenu.get()) and event:
                    return

                self.selectedRow = int(self.rowSelectionMenu.get())
                
                for row in range(1, 5):
                    if row != self.selectedRow:
                        self.tileSelections[self.selectedTile][row]["enemyLabel"].grid_forget()
                        self.tileSelections[self.selectedTile][row]["enemies"][1]["widget"].grid_forget()
                        self.tileSelections[self.selectedTile][row]["enemies"][2]["widget"].grid_forget()
                        self.tileSelections[self.selectedTile][row]["enemies"][3]["widget"].grid_forget()
                        self.tileSelections[self.selectedTile][row]["terrainLabel"].grid_forget()
                        self.tileSelections[self.selectedTile][row]["terrain"]["widget"].grid_forget()
                        
                self.tileSelections[self.selectedTile][self.selectedRow]["enemyLabel"].grid(column=0, row=0, padx=5, pady=5)
                self.tileSelections[self.selectedTile][self.selectedRow]["enemies"][1]["widget"].grid(column=1, row=0, padx=5, pady=5)
                self.tileSelections[self.selectedTile][self.selectedRow]["enemies"][2]["widget"].grid(column=1, row=1, padx=5, pady=5)
                self.tileSelections[self.selectedTile][self.selectedRow]["enemies"][3]["widget"].grid(column=1, row=2, padx=5, pady=5)
                self.tileSelections[self.selectedTile][self.selectedRow]["terrainLabel"].grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)
                self.tileSelections[self.selectedTile][self.selectedRow]["terrain"]["widget"].grid(column=1, row=3, padx=5, pady=5)
                
                log("End of change_row")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def update_lists(self, event=None):
            try:
                log("Start of update_lists")

                val = self.numberOfTilesMenu.get()
                if self.previousNumberOfTilesMenuVal != val:
                    self.update_tile_layout_list(val)
                    self.update_tile_list(val)
                self.previousNumberOfTilesMenuVal = val
                self.update_row_list()
                
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
                self.tileLayoutMenu.config(state="active")
                
                log("End of update_tile_layout_list")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def update_tile_list(self, tiles):
            try:
                log("Start of update_tile_list, tiles={}".format(str(tiles)))

                self.tileSelectionMenuList = ([] if self.tileSelectionMenu == "" else [str(x) for x in range(1, int(tiles) + 1)])
                self.tileSelectionMenu.config(values=self.tileSelectionMenuList)
                self.tileSelectionMenu.set(self.tileSelectionMenuList[0])
                
                log("End of update_tile_list")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def update_row_list(self, event=None):
            try:
                log("Start of update_row_list")

                self.rowSelectionMenuList = ["1", "2"] + (["3", "4"] if self.levelMenu.get() == "4" else [])
                self.rowSelectionMenu.config(values=self.rowSelectionMenuList)
                self.rowSelectionMenu.set(self.rowSelectionMenuList[0])
                
                log("End of update_row_list")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def toggle_starting_nodes_menu(self, tile, event=None):
            try:
                log("Start of toggle_starting_nodes_menu, tile={}".format(str(tile)))

                if self.tileSelections[tile]["startingTile"]["value"].get() == 1:
                    self.tileSelections[tile]["startingNodes"]["widget"].configure(state="active")
                else:
                    self.tileSelections[tile]["startingNodes"]["widget"].configure(state="disabled")
                
                log("End of toggle_starting_nodes_menu")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def new_custom_encounter(self, event=None):
            try:
                log("Start of new_custom_encounter")

                self.app.selected = None
                for tile in range(1, 4):
                    self.tileSelections[tile] = {
                        "traps": {"value": tk.IntVar()},
                        "startingTile": {"value": tk.IntVar()},
                        "startingNodesLabel": ttk.Label(self.layoutFrame2, text="\tStarting\n\tNodes\t"),
                        "startingNodes": {"value": tk.StringVar()}
                    }
                    self.tileSelections[tile]["traps"]["widget"] = ttk.Checkbutton(self.layoutFrame2, text="Traps", variable=self.tileSelections[tile]["traps"]["value"])
                    self.tileSelections[tile]["startingTile"]["widget"] = ttk.Checkbutton(self.layoutFrame2, text="Starting Tile", variable=self.tileSelections[tile]["startingTile"]["value"], command=lambda x=tile: self.toggle_starting_nodes_menu(tile=x))
                    self.tileSelections[tile]["startingNodes"]["widget"] = ttk.Combobox(self.layoutFrame2, state="readonly", values=self.startingNodesMenuList, textvariable=self.tileSelections[tile]["startingNodes"]["value"])
                    
                    self.tileSelections[tile]["traps"]["widget"].state(["!alternate"])
                    self.tileSelections[tile]["startingTile"]["widget"].state(["!alternate"])
                    self.tileSelections[tile]["startingNodes"]["widget"].config(width=8)
                    self.tileSelections[tile]["startingNodes"]["widget"].config(state="disabled")
                    
                    for row in range(1, 5):
                        self.tileSelections[tile][row] = {
                            "enemyLabel": ttk.Label(self.layoutFrame2, text="Enemies Row " + str(row) + "\t"),
                            "enemies": {
                                1: {"value": tk.StringVar()},
                                2: {"value": tk.StringVar()},
                                3: {"value": tk.StringVar()}
                            },
                            "terrainLabel": ttk.Label(self.layoutFrame2, text="Terrain Row " + str(row)),
                            "terrain": {"value": tk.StringVar()}
                        }

                        for x in range(1, 4):
                            self.tileSelections[tile][row]["enemies"][x]["widget"] = ttk.Combobox(self.layoutFrame2, width=25, values=self.eNames, textvariable=self.tileSelections[tile][row]["enemies"][x]["value"])
                            self.tileSelections[tile][row]["enemies"][x]["widget"].set("")
                            self.tileSelections[tile][row]["enemies"][x]["widget"].bind("<KeyRelease>", self.search_enemy_combobox)

                        self.tileSelections[tile][row]["terrain"]["widget"] = ttk.Combobox(self.layoutFrame2, width=25, values=self.terrainNames, textvariable=self.tileSelections[tile][row]["terrain"]["value"])
                        self.tileSelections[tile][row]["terrain"]["widget"].set("")
                        self.tileSelections[tile][row]["terrain"]["widget"].bind("<KeyRelease>", self.search_terrain_combobox)
                        
                self.tileSelections[1][1]["enemyLabel"].grid(column=0, row=0, padx=5, pady=5)
                self.tileSelections[1][1]["enemies"][1]["widget"].grid(column=1, row=0, padx=5, pady=5)
                self.tileSelections[1][1]["enemies"][2]["widget"].grid(column=1, row=1, padx=5, pady=5)
                self.tileSelections[1][1]["enemies"][3]["widget"].grid(column=1, row=2, padx=5, pady=5)
                self.tileSelections[1][1]["terrainLabel"].grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)
                self.tileSelections[1][1]["terrain"]["widget"].grid(column=1, row=3, padx=5, pady=5)
                self.tileSelections[1]["traps"]["widget"].grid(column=3, row=0, padx=5, pady=5, sticky=tk.W)
                self.tileSelections[1]["startingTile"]["widget"].grid(column=3, row=1, padx=5, pady=5, sticky=tk.W)
                self.tileSelections[1]["startingNodesLabel"].grid(column=2, row=2, padx=5, pady=5)
                self.tileSelections[1]["startingNodes"]["widget"].grid(column=3, row=2, pady=5)

                self.rowSelectionMenuList = []
                self.rowSelectionMenuVal = tk.StringVar()
                self.tileSelectionMenuList = []
                self.tileSelectionMenuVal = tk.StringVar()
                self.iconMenuList = []
                self.iconMenuVal = tk.StringVar()
                self.iconSaveErrorsVal = tk.StringVar()
                self.iconSizeMenuVal = tk.StringVar()
                self.iconImageErrorsVal = tk.StringVar()
                self.xPositionVal = tk.StringVar()
                self.yPositionVal = tk.StringVar()
                
                self.encounterNameEntry.delete("1.0", tk.END)
                self.flavorEntry.delete("1.0", tk.END)
                self.objectiveEntry.delete("1.0", tk.END)
                self.rewardSoulsEntry.delete("1.0", tk.END)
                self.rewardSearchEntry.delete("1.0", tk.END)
                self.rewardDrawEntry.delete("1.0", tk.END)
                self.rewardTrialEntry.delete("1.0", tk.END)
                self.keywordsEntry.delete("1.0", tk.END)
                self.specialRulesEntry.delete("1.0", tk.END)
                self.iconNameEntry.delete("1.0", tk.END)

                self.rewardSoulsPerPlayer.state(["!selected"])
                self.shortcut.state(["!selected"])
                self.previousNumberOfTilesMenuVal = ""
                self.levelMenu.set(self.levelMenuList[0])
                self.numberOfTilesMenu.set(self.numberOfTilesMenuList[0])
                self.tileLayoutMenu.set("")

                self.update_lists()
                
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
                log("Start of apply_changes")

                clear_other_tab_images(self.app, "encounters", "encounters")

                self.app.encounterTab.apply_keyword_tooltips(None, None)
                
                if self.numberOfTilesMenuVal.get() == "1" and self.levelMenuVal.get() == "4" and self.tileSelections[1]["traps"]["value"].get() == 1:
                    displayPhotoImage = self.app.create_image("custom_encounter_1_tile_level_4_traps.jpg", "encounter", 1, extensionProvided=True)
                elif self.numberOfTilesMenuVal.get() == "1" and self.levelMenuVal.get() == "4":
                    displayPhotoImage = self.app.create_image("custom_encounter_1_tile_level_4_no_traps.jpg", "encounter", 1, extensionProvided=True)
                elif self.numberOfTilesMenuVal.get() == "1" and self.tileSelections[1]["traps"]["value"].get() == 1:
                    displayPhotoImage = self.app.create_image("custom_encounter_1_tile_traps.jpg", "encounter", 1, extensionProvided=True)
                elif self.numberOfTilesMenuVal.get() == "1":
                    displayPhotoImage = self.app.create_image("custom_encounter_1_tile_no_traps.jpg", "encounter", 1, extensionProvided=True)
                elif self.numberOfTilesMenuVal.get() == "2":
                    displayPhotoImage = self.app.create_image("custom_encounter_2_tile.jpg", "encounter", 1, extensionProvided=True)
                elif self.numberOfTilesMenuVal.get() == "3":
                    displayPhotoImage = self.app.create_image("custom_encounter_3_tile.jpg", "encounter", 1, extensionProvided=True)
                else:
                    return
                
                self.save_custom_icon()

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                
                # Encounter Name
                imageWithText.text((80, 25 + (10 if self.encounterNameEntry.get("1.0", "end").count("\n") == 1 else 0)), self.encounterNameEntry.get("1.0", "end"), "white", fontEncounterName)
                
                # Flavor Text
                imageWithText.text((20, 88 + (7 if self.flavorEntry.get("1.0", "end").count("\n") == 1 else 0)), self.flavorEntry.get("1.0", "end"), "black", fontFlavor)
                
                # Objective Text
                imageWithText.text((20, 146), self.objectiveEntry.get("1.0", "end"), "black", font)
                
                # Keywords
                imageWithText.text((141, 195), self.keywordsEntry.get("1.0", "end"), "black", fontFlavor)
                rulesNewlines = 0 if not self.keywordsEntry.get("1.0", "end").strip() else self.keywordsEntry.get("1.0", "end").strip().count("\n")
                
                # Special Rules
                imageWithText.text((141, 195), ("\n" + ("\n" * rulesNewlines) if self.keywordsEntry.get("1.0", "end").strip() else "") + self.specialRulesEntry.get("1.0", "end"), "black", font)

                # Encounter Level
                if self.levelMenuVal.get():
                    self.app.displayImage.paste(im=self.app.levelIcons[int(self.levelMenuVal.get())], box=(328, 15), mask=self.app.levelIcons[int(self.levelMenuVal.get())])

                lineCount = 0

                # Reward Souls
                if self.rewardSoulsEntry.get("1.0", "end").strip():
                    if self.rewardSoulsPerPlayerVal.get() == 1:
                        self.app.displayImage.paste(im=self.app.rewardsSoulsPlayersIcon, box=(20, 195), mask=self.app.rewardsSoulsPlayersIcon)
                    else:
                        self.app.displayImage.paste(im=self.app.rewardsSoulsIcon, box=(20, 195), mask=self.app.rewardsSoulsIcon)
                    imageWithText.text((20, 195), "\n" + ("      " if self.rewardSoulsPerPlayerVal.get() == 1 else "") + self.rewardSoulsEntry.get("1.0", "end"), "black", font)
                    lineCount += 2 + self.rewardSoulsEntry.get("1.0", "end").strip().count("\n")
                # Reward Search
                if self.rewardSearchEntry.get("1.0", "end").strip():
                    y = 195 + round(12.5 * lineCount)
                    self.app.displayImage.paste(im=self.app.rewardsSearchIcon, box=(20, y), mask=self.app.rewardsSearchIcon)
                    imageWithText.text((20, y), "\n" + self.rewardSearchEntry.get("1.0", "end"), "black", font)
                    lineCount += 2 + self.rewardSearchEntry.get("1.0", "end").strip().count("\n")

                # Reward Draw
                if self.rewardDrawEntry.get("1.0", "end").strip():
                    y = 195 + round(12.5 * lineCount)
                    self.app.displayImage.paste(im=self.app.rewardsDrawIcon, box=(20, y), mask=self.app.rewardsDrawIcon)
                    imageWithText.text((20, y), "\n" + self.rewardDrawEntry.get("1.0", "end"), "black", font)
                    lineCount += 2 + self.rewardDrawEntry.get("1.0", "end").strip().count("\n")

                # Reward Trial
                if self.rewardTrialEntry.get("1.0", "end").strip():
                    y = 195 + round(12.5 * lineCount)
                    self.app.displayImage.paste(im=self.app.rewardsTrialIcon, box=(20, y), mask=self.app.rewardsTrialIcon)
                    imageWithText.text((20, y), "\n" + self.rewardTrialEntry.get("1.0", "end"), "black", font)
                    lineCount += 2 + self.rewardTrialEntry.get("1.0", "end").strip().count("\n")

                # Reward Shortcut
                if self.shortcutVal.get() == 1:
                    y = 195 + round(12.5 * lineCount)
                    self.app.displayImage.paste(im=self.app.rewardsShortcutIcon, box=(20, y), mask=self.app.rewardsShortcutIcon)

                # Tile Layout
                tileLayout = self.app.tileLayouts.get(self.tileLayoutMenuVal.get(), None)
                if tileLayout:
                    self.app.displayImage.paste(im=tileLayout["layout"], box=(20, 330), mask=tileLayout["layout"])

                    # Starting nodes
                    for tile in range(1, 4):
                        if self.tileSelections[tile]["startingTile"]["value"].get() == 1 and self.tileSelections[tile]["startingNodes"]["value"].get():
                            startingNodesLocation = self.tileSelections[tile]["startingNodes"]["value"].get()
                            if tile not in tileLayout["box"]:
                                continue
                            box = tileLayout["box"][tile][startingNodesLocation]
                            if startingNodesLocation in {"North", "South"}:
                                self.app.displayImage.paste(im=tileLayout["startingNodesHorizontal"], box=box, mask=tileLayout["startingNodesHorizontal"])
                            else:
                                self.app.displayImage.paste(im=tileLayout["startingNodesVertical"], box=box, mask=tileLayout["startingNodesVertical"])
                                
                # Tile numbers and traps
                if self.numberOfTilesMenuVal.get() != "1":
                    for tile in range(1, 4):
                        if tile > int(self.numberOfTilesMenuVal.get()):
                            continue

                        box = (334, 377 + (122 * (tile - 1)))

                        if self.tileSelections[tile]["startingTile"]["value"].get() == 1 and self.tileSelections[tile]["traps"]["value"].get() == 1:
                            image = self.app.tileNumbers[tile]["starting"]["traps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)
                        elif self.tileSelections[tile]["startingTile"]["value"].get() == 1 and self.tileSelections[tile]["traps"]["value"].get() != 1:
                            image = self.app.tileNumbers[tile]["starting"]["noTraps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)
                        elif self.tileSelections[tile]["startingTile"]["value"].get() != 1 and self.tileSelections[tile]["traps"]["value"].get() == 1:
                            image = self.app.tileNumbers[tile]["notStarting"]["traps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)
                        elif self.tileSelections[tile]["startingTile"]["value"].get() != 1 and self.tileSelections[tile]["traps"]["value"].get() != 1:
                            image = self.app.tileNumbers[tile]["notStarting"]["noTraps"]
                            self.app.displayImage.paste(im=image, box=box, mask=image)

                # Terrain
                for tile in range(1, int(self.numberOfTilesMenuVal.get()) + 1):
                    for row in range(1, 5 if self.levelMenu.get() == "4" else 3):
                        box = (301, 380 + (29 * (row - 1)) + (122 * (tile - 1)) + (29 if self.levelMenuVal.get() == "4" else 0))
                        if self.tileSelections[tile][row]["terrain"]["value"].get() in self.app.terrain:
                            image = self.app.terrain[self.tileSelections[tile][row]["terrain"]["value"].get()]
                            self.app.displayImage.paste(im=image, box=box, mask=image)

                # Enemies
                for tile in range(1, int(self.numberOfTilesMenuVal.get()) + 1):
                    for row in range(1, 5 if self.levelMenu.get() == "4" else 3):
                        for e in range(1, 4):
                            box = (300 + (29 * (e - 1)), 323 + (29 * (row - 1)) + (122 * (tile - 1)))
                            if self.tileSelections[tile][row]["enemies"][e]["value"].get() in self.app.allEnemies:
                                enemy = self.tileSelections[tile][row]["enemies"][e]["value"].get()
                                image = self.app.allEnemies[enemy]["imageNew"]
                                self.app.displayImage.paste(im=image, box=box, mask=image)

                # Custom Icons
                for icon in [icon for icon in self.icons if self.icons[icon]["position"]]:
                    image = self.icons[icon]["image"]
                    self.app.displayImage.paste(im=image, box=self.icons[icon]["position"], mask=image)

                self.customEncounter["image"] = self.app.displayImage.copy()
                self.customEncounter["numberOfTiles"] = self.numberOfTilesMenuVal.get()
                self.customEncounter["level"] = self.levelMenuVal.get()
                self.customEncounter["encounterName"] = self.encounterNameEntry.get("1.0", "end")
                self.customEncounter["flavor"] = self.flavorEntry.get("1.0", "end")
                self.customEncounter["objective"] = self.objectiveEntry.get("1.0", "end")
                self.customEncounter["keywords"] = self.keywordsEntry.get("1.0", "end")
                self.customEncounter["specialRules"] = self.specialRulesEntry.get("1.0", "end")
                self.customEncounter["rewardSouls"] = self.rewardSoulsEntry.get("1.0", "end")
                self.customEncounter["rewardSoulsPerPlayer"] = self.rewardSoulsPerPlayerVal.get()
                self.customEncounter["rewardSearch"] = self.rewardSearchEntry.get("1.0", "end")
                self.customEncounter["rewardDraw"] = self.rewardDrawEntry.get("1.0", "end")
                self.customEncounter["rewardTrial"] = self.rewardTrialEntry.get("1.0", "end")
                self.customEncounter["rewardShortcut"] = self.shortcutVal.get()
                self.customEncounter["layout"] = self.tileLayoutMenuVal.get()
                self.customEncounter["icons"] = self.icons
                self.customEncounter["startingNodes"] = {
                    1: {
                        "startingTile": {"value": self.tileSelections[1]["startingTile"]["value"].get()},
                        "startingNodes": {"value": self.tileSelections[1]["startingNodes"]["value"].get()},
                        "traps": {"value": self.tileSelections[1]["traps"]["value"].get()},
                        1: {"terrain": {"value": self.tileSelections[1][1]["terrain"]["value"].get()},
                            "enemies": {"value": self.tileSelections[1][1]["enemies"][1]["value"].get()},
                            "enemies": {"value": self.tileSelections[1][1]["enemies"][2]["value"].get()},
                            "enemies": {"value": self.tileSelections[1][1]["enemies"][3]["value"].get()}},
                        2: {"terrain": {"value": self.tileSelections[1][2]["terrain"]["value"].get()},
                            "enemies": {"value": self.tileSelections[1][2]["enemies"][1]["value"].get()},
                            "enemies": {"value": self.tileSelections[1][2]["enemies"][2]["value"].get()},
                            "enemies": {"value": self.tileSelections[1][2]["enemies"][3]["value"].get()}},
                        3: {"terrain": {"value": self.tileSelections[1][3]["terrain"]["value"].get()},
                            "enemies": {"value": self.tileSelections[1][3]["enemies"][1]["value"].get()},
                            "enemies": {"value": self.tileSelections[1][3]["enemies"][2]["value"].get()},
                            "enemies": {"value": self.tileSelections[1][3]["enemies"][3]["value"].get()}},
                        4: {"terrain": {"value": self.tileSelections[1][4]["terrain"]["value"].get()},
                            "enemies": {"value": self.tileSelections[1][4]["enemies"][1]["value"].get()},
                            "enemies": {"value": self.tileSelections[1][4]["enemies"][2]["value"].get()},
                            "enemies": {"value": self.tileSelections[1][4]["enemies"][3]["value"].get()}}
                        },
                    2: {
                        "startingTile": {"value": self.tileSelections[2]["startingTile"]["value"].get()},
                        "startingNodes": {"value": self.tileSelections[2]["startingNodes"]["value"].get()},
                        "traps": {"value": self.tileSelections[2]["traps"]["value"].get()},
                        1: {"terrain": {"value": self.tileSelections[2][1]["terrain"]["value"].get()},
                            "enemies": {"value": self.tileSelections[2][1]["enemies"][1]["value"].get()},
                            "enemies": {"value": self.tileSelections[2][1]["enemies"][2]["value"].get()},
                            "enemies": {"value": self.tileSelections[2][1]["enemies"][3]["value"].get()}},
                        2: {"terrain": {"value": self.tileSelections[2][2]["terrain"]["value"].get()},
                            "enemies": {"value": self.tileSelections[2][2]["enemies"][1]["value"].get()},
                            "enemies": {"value": self.tileSelections[2][2]["enemies"][2]["value"].get()},
                            "enemies": {"value": self.tileSelections[2][2]["enemies"][3]["value"].get()}},
                        3: {"terrain": {"value": self.tileSelections[2][3]["terrain"]["value"].get()},
                            "enemies": {"value": self.tileSelections[2][3]["enemies"][1]["value"].get()},
                            "enemies": {"value": self.tileSelections[2][3]["enemies"][2]["value"].get()},
                            "enemies": {"value": self.tileSelections[2][3]["enemies"][3]["value"].get()}},
                        4: {"terrain": {"value": self.tileSelections[2][4]["terrain"]["value"].get()},
                            "enemies": {"value": self.tileSelections[2][4]["enemies"][1]["value"].get()},
                            "enemies": {"value": self.tileSelections[2][4]["enemies"][2]["value"].get()},
                            "enemies": {"value": self.tileSelections[2][4]["enemies"][3]["value"].get()}}
                        },
                    3: {
                        "startingTile": {"value": self.tileSelections[3]["startingTile"]["value"].get()},
                        "startingNodes": {"value": self.tileSelections[3]["startingNodes"]["value"].get()},
                        "traps": {"value": self.tileSelections[3]["traps"]["value"].get()},
                        1: {"terrain": {"value": self.tileSelections[3][1]["terrain"]["value"].get()},
                            "enemies": {"value": self.tileSelections[3][1]["enemies"][1]["value"].get()},
                            "enemies": {"value": self.tileSelections[3][1]["enemies"][2]["value"].get()},
                            "enemies": {"value": self.tileSelections[3][1]["enemies"][3]["value"].get()}},
                        2: {"terrain": {"value": self.tileSelections[3][2]["terrain"]["value"].get()},
                            "enemies": {"value": self.tileSelections[3][2]["enemies"][1]["value"].get()},
                            "enemies": {"value": self.tileSelections[3][2]["enemies"][2]["value"].get()},
                            "enemies": {"value": self.tileSelections[3][2]["enemies"][3]["value"].get()}},
                        3: {"terrain": {"value": self.tileSelections[3][3]["terrain"]["value"].get()},
                            "enemies": {"value": self.tileSelections[3][3]["enemies"][1]["value"].get()},
                            "enemies": {"value": self.tileSelections[3][3]["enemies"][2]["value"].get()},
                            "enemies": {"value": self.tileSelections[3][3]["enemies"][3]["value"].get()}},
                        4: {"terrain": {"value": self.tileSelections[3][4]["terrain"]["value"].get()},
                            "enemies": {"value": self.tileSelections[3][4]["enemies"][1]["value"].get()},
                            "enemies": {"value": self.tileSelections[3][4]["enemies"][2]["value"].get()},
                            "enemies": {"value": self.tileSelections[3][4]["enemies"][3]["value"].get()}}
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

                file = baseFolder + "\\lib\\dsbg_shuffle_custom_icon_images\\".replace("\\", pathSep) + self.customEncounter["encounterName"].strip().replace("\n", " ") + ".jpg"

                with open(file, "w") as encounterFile:
                    dump({k: v for k, v in self.customEncounter.items() if k != "image"}, encounterFile)

                self.customEncounter["image"].save(path.splitext(file)[0] + ".jpg")

                log("End of save_custom_encounter (saved to " + str(encounterFile) + ")")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def load_custom_encounter(self, event=None):
            try:
                log("Start of load_custom_encounter")

                pass
                
                log("End of pick_enemy_variants_behavior")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def change_icon(self, event):
            try:
                log("Start of change_icon")

                icon = self.iconMenuVal.get()
                self.currentIcon = {
                    "label": icon,
                    "file": deepcopy(self.icons[icon]["file"]),
                    "size": deepcopy(self.icons[icon]["size"]),
                    "position": deepcopy(self.icons[icon]["position"])
                }
                self.iconNameEntry.delete(1.0, tk.END)
                self.iconNameEntry.insert("end-1c", icon)
                self.iconSizeMenuVal.set("Enemy/Terrain" if self.currentIcon["size"] == "iconEnemy" else "Text")
                self.xPositionVal.set(str(self.currentIcon["position"][0]))
                self.yPositionVal.set(str(self.currentIcon["position"][1]))
                self.choose_icon_image(file=self.currentIcon["file"])
                
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
                self.iconMenu.set(self.iconMenuList[0])
                
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
                    "position": (int(self.xPositionEntry.get()), int(self.yPositionEntry.get())) if self.xPositionEntry.get() and self.yPositionEntry.get() else None,
                    "file": deepcopy(self.currentIcon["file"])
                    }

                self.icons[icon]["image"], self.icons[icon]["photoImage"] = self.app.create_image(self.currentIcon["file"], self.currentIcon["size"], 99, pathProvided=True, extensionProvided=True)
                
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
                self.currentIcon["file"] = file
                self.currentIcon["image"] = i
                self.currentIcon["photoImage"] = p

                self.iconView.config(image=p)
                self.iconView.image=p

                log("\tEnd of choose_icon_image")
            except UnidentifiedImageError:
                # Handling for this occurred in create_image.
                return
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

            self.buttonsFrame = ttk.Frame(self)
            self.buttonsFrame.pack()

            self.l1 = ttk.Button(self.buttonsFrame, text="Random Level 1", width=16, command=lambda x=1: self.random_encounter(level=x))
            self.l2 = ttk.Button(self.buttonsFrame, text="Random Level 2", width=16, command=lambda x=2: self.random_encounter(level=x))
            self.l3 = ttk.Button(self.buttonsFrame, text="Random Level 3", width=16, command=lambda x=3: self.random_encounter(level=x))
            self.l4 = ttk.Button(self.buttonsFrame, text="Random Level 4", width=16, command=lambda x=4: self.random_encounter(level=x))
            if "level4" not in self.app.settings["encounterTypes"]:
                self.l4["state"] = "disabled"
            if ["level4"] == self.app.settings["encounterTypes"]:
                self.l1["state"] = "disabled"
                self.l2["state"] = "disabled"
                self.l3["state"] = "disabled"
            self.l1.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.l2.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.l3.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.l4.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            
            self.buttonsFrame2 = ttk.Frame(self)
            self.buttonsFrame2.pack()
            self.originalButton = ttk.Button(self.buttonsFrame2, text="Show Original", width=16, command=self.show_original)
            self.originalButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

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
                    and encounter != "Mega Boss Setup"
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

                clear_other_tab_images(self.app, "encounters", "encounters")

                if not customEnemyListCheck:
                    self.treeviewEncounters.unbind("<<TreeviewSelect>>")

                # If this encounter was clicked on, get that information.
                if event:
                    tree = event.widget
                    if not tree.item(tree.selection())["tags"][0]:
                        log("\tNo encounter selected")
                        self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)
                        set_display_bindings_by_tab(self.app)
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
                        set_display_bindings_by_tab(self.app)
                        log("\tEnd of load_encounter")
                        return

                self.app.selected = self.app.encounters[encounterName]

                # Get the possible alternative enemies from the encounter's file.
                log("\tOpening " + baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + encounterName + str(self.app.numberOfCharacters) + ".json")
                with open(baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + encounterName + str(self.app.numberOfCharacters) + ".json") as alternativesFile:
                    alts = load(alternativesFile)

                self.app.selected["alternatives"] = []
                self.app.selected["enemySlots"] = alts["enemySlots"]
                self.app.selected["original"] = alts["original"]
                self.newEnemies = []

                # Use only alternative enemies for expansions and enemies the user has activated in the settings.
                for expansionCombo in alts["alternatives"]:
                    if set(expansionCombo.split(",")).issubset(self.app.availableExpansions):
                        self.app.selected["alternatives"] += [alt for alt in alts["alternatives"][expansionCombo] if set(alt).issubset(self.app.enabledEnemies) and sum([1 for a in alt if enemyIds[a].expansions == set(["Phantoms"]) or enemyIds[a].name in {"Hungry Mimic", "Voracious Mimic"}]) <= self.app.settings["maxInvaders"]]

                self.newTiles = dict()

                if not customEnemyListCheck:
                    self.shuffle_enemies()
                    self.treeviewEncounters.bind("<<TreeviewSelect>>", self.load_encounter)
                    set_display_bindings_by_tab(self.app)

                log("\tEnd of load_encounter")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def show_original(self, event=None):
            """
            Display the encounter with its original enemies.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
                    Default: None
            """
            try:
                log("Start of show_original")

                if self.app.notebook.tab(self.app.notebook.select(), "text") not in {"Encounters", "Campaign"}:
                    log("End of show_original (wrong tab)")
                    return

                if not self.app.selected:
                    log("\tNo encounter loaded - nothing to do")
                    log("\tEnd of show_original")
                    return

                self.rewardTreasure = None

                self.newEnemies = self.app.selected["original"]

                self.edit_encounter_card(self.app.selected["name"], self.app.selected["expansion"], self.app.selected["level"], self.app.selected["enemySlots"], original=True)

                log("\tEnd of show_original")
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

                if self.app.notebook.tab(self.app.notebook.select(), "text") not in {"Encounters", "Campaign"}:
                    log("End of shuffle_enemies (wrong tab)")
                    return

                if not self.app.selected:
                    log("\tNo encounter loaded - nothing to shuffle")
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


        def edit_encounter_card(self, name, expansion, level, enemySlots, campaignGen=False, right=False, original=False):
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
                    self.castle_break_in(original=original)
                elif (name == "Central Plaza" or name == "Central Plaza (TSC)") and expansion == "The Sunless City":
                    self.central_plaza(right=right)
                elif name == "Cloak and Feathers":
                    self.cloak_and_feathers(right=right)
                elif name == "Cold Snap":
                    self.cold_snap(right=right)
                elif name == "Corvian Host":
                    self.corvian_host(right=right, original=original)
                elif name == "Corrupted Hovel":
                    self.corrupted_hovel(right=right)
                elif name == "Dark Alleyway":
                    self.dark_alleyway(right=right)
                elif name == "Dark Resurrection":
                    self.dark_resurrection(original=original)
                elif name == "Deathly Freeze":
                    self.deathly_freeze(level, right=right)
                elif name == "Deathly Magic":
                    self.deathly_magic(level, right=right)
                elif name == "Deathly Tolls":
                    self.deathly_tolls(right=right, original=original)
                elif name == "Depths of the Cathedral":
                    self.depths_of_the_cathedral(right=right, original=original)
                elif name == "Distant Tower":
                    self.distant_tower(right=right, original=original)
                elif name == "Eye of the Storm":
                    self.eye_of_the_storm(right=right)
                elif name == "Flooded Fortress":
                    self.flooded_fortress(right=right, original=original)
                elif name == "Frozen Revolutions":
                    self.frozen_revolutions(right=right)
                elif name == "Giant's Coffin":
                    self.giants_coffin(right=right, original=original)
                elif name == "Gleaming Silver":
                    self.gleaming_silver(level, right=right)
                elif name == "Gnashing Beaks":
                    self.gnashing_beaks(right=right)
                elif name == "Grave Matters":
                    self.grave_matters(original=original)
                elif name == "Grim Reunion":
                    self.grim_reunion(right=right)
                elif name == "Hanging Rafters":
                    self.hanging_rafters(original=original)
                elif name == "In Deep Water":
                    self.in_deep_water(right=right, original=original)
                elif name == "Inhospitable Ground":
                    self.inhospitable_ground(original=original)
                elif name == "Lakeview Refuge":
                    self.lakeview_refuge(right=right)
                elif name == "Monstrous Maw":
                    self.monstrous_maw(right=right, original=original)
                elif name == "No Safe Haven":
                    self.no_safe_haven(right=right, original=original)
                elif name == "Painted Passage":
                    self.painted_passage(original=original)
                elif name == "Parish Church":
                    self.parish_church(right=right)
                elif name == "Parish Gates":
                    self.parish_gates(right=right)
                elif name == "Pitch Black":
                    self.pitch_black(level, right=right)
                elif name == "Puppet Master":
                    self.puppet_master(right=right, original=original)
                elif name == "Rain of Filth":
                    self.rain_of_filth(original=original)
                elif name == "Shattered Keep":
                    self.shattered_keep(right=right, original=original)
                elif name == "Skeletal Spokes":
                    self.skeletal_spokes(right=right)
                elif name == "Skeleton Overlord":
                    self.skeleton_overlord(right=right)
                elif name == "Tempting Maw":
                    self.tempting_maw(right=right)
                elif name == "The Abandoned Chest":
                    self.the_abandoned_chest(right=right, original=original)
                elif name == "The Beast From the Depths":
                    self.the_beast_from_the_depths(right=right, original=original)
                elif name == "The Bell Tower":
                    self.the_bell_tower(right=right)
                elif name == "The First Bastion":
                    self.the_first_bastion(level, right=right)
                elif name == "The Fountainhead":
                    self.the_fountainhead(right=right, original=original)
                elif name == "The Grand Hall":
                    self.the_grand_hall(right=right)
                elif name == "The Iron Golem":
                    self.the_iron_golem(right=right, original=original)
                elif name == "The Last Bastion":
                    self.the_last_bastion(level, right=right)
                elif name == "The Locked Grave":
                    self.the_locked_grave(right=right, original=original)
                elif name == "The Shine of Gold":
                    self.the_shine_of_gold(right=right)
                elif name == "The Skeleton Ball":
                    self.the_skeleton_ball(right=right, original=original)
                elif name == "Trecherous Tower":
                    self.trecherous_tower()
                elif name == "Trophy Room":
                    self.trophy_room(right=right, original=original)
                elif name == "Twilight Falls":
                    self.twilight_falls(right=right, original=original)
                elif name == "Undead Sanctum":
                    self.undead_sanctum(right=right, original=original)
                elif name == "Unseen Scurrying":
                    self.unseen_scurrying(original=original)
                elif name == "Urns of the Fallen":
                    self.urns_of_the_fallen(original=original)
                elif name == "Velka's Chosen":
                    self.velkas_chosen(level, right=right, original=original)

                displayPhotoImage = ImageTk.PhotoImage(self.app.displayImage)

                if right:
                    self.app.displayImages["encounters"][self.app.displayTopRight]["name"] = name
                    self.app.displayImages["encounters"][self.app.displayTopRight]["image"] = displayPhotoImage
                    self.app.displayImages["encounters"][self.app.displayTopRight]["activeTab"] = "encounters"
                    self.app.displayTopRight.image = displayPhotoImage
                    self.app.displayTopRight.config(image=displayPhotoImage)
                else:
                    self.app.displayImages["encounters"][self.app.displayTopLeft]["name"] = name
                    self.app.displayImages["encounters"][self.app.displayTopLeft]["image"] = displayPhotoImage
                    self.app.displayImages["encounters"][self.app.displayTopLeft]["activeTab"] = "encounters"
                    self.app.displayTopLeft.image = displayPhotoImage
                    self.app.displayTopLeft.config(image=displayPhotoImage)

                if not self.app.forPrinting and not campaignGen:
                    self.app.displayImages["encounters"][self.app.displayTopLeft]["name"] = name
                    self.app.displayImages["encounters"][self.app.displayTopLeft]["image"] = displayPhotoImage
                    self.app.displayImages["encounters"][self.app.displayTopLeft]["activeTab"] = "encounters"
                    self.app.displayTopLeft.config(image=displayPhotoImage)
                    self.app.displayTopRight.config(image="")
                    self.app.displayBottomRight.config(image="")
                    self.app.displayTopRight.image=None
                    self.app.displayBottomRight.image=None

                set_display_bindings_by_tab(self.app)


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


        def castle_break_in(self, original=False):
            try:
                log("Start of castle_break_in")

                imageWithText = ImageDraw.Draw(self.app.displayImage)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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


        def corvian_host(self, right=False, original=False):
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
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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


        def dark_resurrection(self, original=False):
            try:
                log("Start of dark_resurrection")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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


        def deathly_tolls(self, right=False, original=False):
            try:
                log("Start of deathly_tolls")

                target = enemyIds[self.newEnemies[7]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=180, y=212, right=right)

                gang = "Hollow" if original else Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
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


        def depths_of_the_cathedral(self, right=False, original=False):
            try:
                log("Start of depths_of_the_cathedral")

                gang = "Hollow" if original else Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
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


        def distant_tower(self, right=False, original=False):
            try:
                log("Start of distant_tower")

                target = self.newTiles[3][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=217, y=213, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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


        def flooded_fortress(self, right=False, original=False):
            try:
                log("Start of flooded_fortress")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                gang =  "Hollow" if original else Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
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


        def frozen_revolutions(self, right=False, original=False):
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
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of frozen_revolutions")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def giants_coffin(self, right=False, original=False):
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
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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


        def grave_matters(self, original=False):
            try:
                log("Start of grave_matters")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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


        def hanging_rafters(self, original=False):
            try:
                log("Start of hanging_rafters")

                imageWithText = ImageDraw.Draw(self.app.displayImage)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 258), newTreasureLines[0], "black", font)
                imageWithText.text((21, 269), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of hanging_rafters")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def in_deep_water(self, right=False, original=False):
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
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of in_deep_water")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def inhospitable_ground(self, original=False):
            try:
                log("Start of inhospitable_ground")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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


        def monstrous_maw(self, right=False, original=False):
            try:
                log("Start of monstrous_maw")

                target = self.newTiles[1][1][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=210, y=196, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of monstrous_maw")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def no_safe_haven(self, right=False, original=False):
            try:
                log("Start of no_safe_haven")

                target = self.newTiles[2][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=63, y=147, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of no_safe_haven")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def painted_passage(self, original=False):
            try:
                log("Start of painted_passage")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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
                self.app.create_tooltip(tooltipDict=tooltipDict, x=164, y=232, right=right)
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


        def puppet_master(self, right=False, original=False):
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
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of puppet_master")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def rain_of_filth(self, original=False):
            try:
                log("Start of rain_of_filth")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of rain_of_filth")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def shattered_keep(self, right=False, original=False):
            try:
                log("Start of shattered_keep")
                
                targets = set([self.newTiles[1][0][1], self.newTiles[1][1][0], self.newTiles[1][1][1]])
                for i, target in enumerate(targets):
                    tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                    self.app.create_tooltip(tooltipDict=tooltipDict, x=145 + (20 * i), y=213, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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


        def the_abandoned_chest(self, right=False, original=False):
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
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of the_abandoned_chest")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def the_beast_from_the_depths(self, right=False, original=False):
            try:
                log("Start of the_beast_from_the_depths")

                target = self.newTiles[1][0][0]
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=65, y=147, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=158, y=222, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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


        def the_fountainhead(self, right=False, original=False):
            try:
                log("Start of the_fountainhead")

                gang = "Hollow" if original else Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
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


        def the_iron_golem(self, right=False, original=False):
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
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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


        def the_locked_grave(self, right=False, original=False):
            try:
                log("Start of the_locked_grave")

                target = enemyIds[self.newEnemies[7]].name
                tooltipDict = {"image" if self.app.forPrinting else "photo image": self.app.allEnemies[target]["image text" if self.app.forPrinting else "photo image text"], "imageName": target}
                self.app.create_tooltip(tooltipDict=tooltipDict, x=217, y=197, right=right)
                self.app.create_tooltip(tooltipDict=tooltipDict, x=306, y=220, right=right)

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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


        def the_skeleton_ball(self, right=False, original=False):
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
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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


        def trophy_room(self, right=False, original=False):
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
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of trophy_room")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def twilight_falls(self, right=False, original=False):
            try:
                log("Start of twilight_falls")

                gang = "Hollow" if original else Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
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


        def undead_sanctum(self, right=False, original=False):
            try:
                log("Start of undead_sanctum")

                gang = "Hollow" if original else Counter([enemyIds[enemy].gang for enemy in self.newEnemies if enemyIds[enemy].gang]).most_common(1)[0][0]
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
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of undead_sanctum")
            except Exception as e:
                error_popup(self.root, e)
                raise

        def unseen_scurrying(self, original=False):
            try:
                log("Start of unseen_scurrying")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of unseen_scurrying")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def urns_of_the_fallen(self, original=False):
            try:
                log("Start of urns_of_the_fallen")

                if self.rewardTreasure:
                    newTreasure = self.rewardTreasure
                else:
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
                    self.rewardTreasure = newTreasure

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                newTreasureLines = self.new_treasure_name(newTreasure)
                imageWithText.text((21, 232), newTreasureLines[0], "black", font)
                imageWithText.text((21, 243), newTreasureLines.get(1, ""), "black", font)

                log("\tEnd of urns_of_the_fallen")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def velkas_chosen(self, level, right=False, original=False):
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
                    newTreasure = pick_treasure("Original" if original else self.app.settings["treasureSwapOption"], treasureSwapEncounters[self.app.selected["name"]], self.rewardTreasure, self.app.selected["level"], set(self.app.availableExpansions), set(self.app.charactersActive))
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