try:
    import errno
    import tkinter as tk
    from copy import deepcopy
    from datetime import datetime
    from json import dump, load
    from os import listdir, path
    from PIL import ImageTk, ImageDraw, UnidentifiedImageError
    from tkinter import filedialog, ttk

    from dsbg_shuffle_enemies import enemyNames
    from dsbg_shuffle_utility import PopupWindow, VerticalScrolledFrame, clear_other_tab_images, error_popup, log, baseFolder, font, fontEncounterName, fontFlavor, pathSep


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
            self.infoFrame6 = ttk.Frame(self.interior)
            self.infoFrame6.pack(side=tk.TOP, anchor=tk.W)
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
            
            self.encounterSetLabel = ttk.Label(self.infoFrame1, text="Set Name")
            self.encounterSetLabel.grid(column=0, row=0, padx=5, pady=5)
            self.encounterSetEntry = tk.Text(self.infoFrame1, width=17, height=1)
            self.encounterSetEntry.grid(column=1, row=0, padx=5, pady=5)
            self.encounterSaveLabelVal = tk.StringVar()
            self.encounterSaveLabel = ttk.Label(self.infoFrame1, textvariable=self.encounterSaveLabelVal)
            self.encounterSaveLabel.grid(column=2, row=0, padx=5, pady=5)
            
            self.encounterNameLabel = ttk.Label(self.infoFrame2, text="Encounter\nName\t")
            self.encounterNameLabel.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)
            self.encounterNameEntry = tk.Text(self.infoFrame2, width=17, height=2)
            self.encounterNameEntry.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.levelLabel = ttk.Label(self.infoFrame2, text="Encounter\nLevel")
            self.levelLabel.pack(side=tk.LEFT, anchor=tk.W, padx=(40, 5), pady=5)
            self.levelMenuList = ["1", "2", "3", "4"]
            self.levelMenuVal = tk.StringVar()
            self.levelMenuVal.set(self.levelMenuList[0])
            self.levelMenu = ttk.Combobox(self.infoFrame2, width=5, state="readonly", values=self.levelMenuList, textvariable=self.levelMenuVal)
            self.levelMenu.bind("<<ComboboxSelected>>", self.update_row_list)
            self.levelMenu.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.numberOfTilesLabel = ttk.Label(self.infoFrame2, text="Number\nof Tiles")
            self.numberOfTilesLabel.pack(side=tk.LEFT, anchor=tk.W, padx=(40, 5), pady=5)
            self.numberOfTilesMenuList = ["1", "2", "3"]
            self.numberOfTilesMenuVal = tk.StringVar()
            self.numberOfTilesMenuVal.set(self.numberOfTilesMenuList[0])
            self.previousNumberOfTilesMenuVal = ""
            self.numberOfTilesMenu = ttk.Combobox(self.infoFrame2, width=5, state="readonly", values=self.numberOfTilesMenuList, textvariable=self.numberOfTilesMenuVal)
            self.numberOfTilesMenu.bind("<<ComboboxSelected>>", self.update_lists)
            self.numberOfTilesMenu.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.flavorLabel = ttk.Label(self.infoFrame3, text="Flavor\nText\t")
            self.flavorLabel.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)
            self.flavorEntry = tk.Text(self.infoFrame3, width=70, height=2)
            self.flavorEntry.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.objectiveLabel = ttk.Label(self.infoFrame4, text="Objective\t")
            self.objectiveLabel.pack(side=tk.LEFT, anchor=tk.NW, padx=5, pady=5)
            self.objectiveEntry = tk.Text(self.infoFrame4, width=70, height=2)
            self.objectiveEntry.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            
            self.rewardSoulsPerPlayerVal = tk.IntVar()
            self.rewardSoulsPerPlayer = ttk.Checkbutton(self.infoFrame5, text="Souls Reward\nPer Player", variable=self.rewardSoulsPerPlayerVal)
            self.rewardSoulsPerPlayer.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)
            self.rewardSoulsPerPlayer.state(["!alternate"])
            
            self.shortcutVal = tk.IntVar()
            self.shortcut = ttk.Checkbutton(self.infoFrame5, text="Shortcut\nReward", variable=self.shortcutVal)
            self.shortcut.grid(column=2, row=0, padx=5, pady=5, sticky=tk.W)
            self.shortcut.state(["!alternate"])
            
            self.rewardSoulsLabel = ttk.Label(self.infoFrame5, text="Souls\nReward\t")
            self.rewardSoulsLabel.grid(column=0, row=1, padx=5, pady=5)
            self.rewardSoulsEntry = tk.Text(self.infoFrame5, width=17, height=2)
            self.rewardSoulsEntry.grid(column=1, row=1, padx=5, pady=5, sticky=tk.W)
            
            self.rewardSearchLabel = ttk.Label(self.infoFrame5, text="Search\nReward\t")
            self.rewardSearchLabel.grid(column=0, row=2, padx=5, pady=5)
            self.rewardSearchEntry = tk.Text(self.infoFrame5, width=17, height=2)
            self.rewardSearchEntry.grid(column=1, row=2, padx=5, pady=5, sticky=tk.W)
            
            self.rewardDrawLabel = ttk.Label(self.infoFrame5, text="Draw\nReward\t")
            self.rewardDrawLabel.grid(column=0, row=3, padx=5, pady=5)
            self.rewardDrawEntry = tk.Text(self.infoFrame5, width=17, height=2)
            self.rewardDrawEntry.grid(column=1, row=3, padx=5, pady=5, sticky=tk.W)
            
            self.rewardTrialLabel = ttk.Label(self.infoFrame5, text="Trial\nReward\t")
            self.rewardTrialLabel.grid(column=0, row=4, padx=5, pady=5)
            self.rewardTrialEntry = tk.Text(self.infoFrame5, width=17, height=2)
            self.rewardTrialEntry.grid(column=1, row=4, padx=5, pady=5, sticky=tk.W)
            
            self.keywordsLabel = ttk.Label(self.infoFrame5, text="Keywords")
            self.keywordsLabel.grid(column=2, row=1, padx=(24, 5), pady=5, sticky=tk.W)
            self.keywordsEntry = tk.Text(self.infoFrame5, width=39, height=2)
            self.keywordsEntry.grid(column=3, row=1, pady=5, columnspan=2, sticky=tk.W)
            
            self.specialRulesLabel = ttk.Label(self.infoFrame5, text="Special\nRules")
            self.specialRulesLabel.grid(column=2, row=2, padx=(24, 5), pady=5, sticky=tk.W)
            self.specialRulesEntry = tk.Text(self.infoFrame5, width=39, height=8)
            self.specialRulesEntry.grid(column=3, row=2, pady=5, rowspan=3, columnspan=2, sticky=tk.W)
            
            self.tileLayoutLabel = ttk.Label(self.infoFrame6, text="Tile\nLayout\t")
            self.tileLayoutLabel.pack(side=tk.LEFT, anchor=tk.W, padx=5, pady=5)
            self.tileLayoutMenuList = []
            self.tileLayoutMenuVal = tk.StringVar()
            self.tileLayoutMenu = ttk.Combobox(self.infoFrame6, width=30, state="readonly", values=self.tileLayoutMenuList, textvariable=self.tileLayoutMenuVal)
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
            self.xPositionLabel = ttk.Label(self.iconsFrame, text="\nx:\n0-400")
            self.xPositionLabel.grid(column=1, row=4, padx=5, pady=5, sticky=tk.W)
            self.xPositionVal = tk.StringVar()
            self.xPositionEntry = ttk.Entry(self.iconsFrame, textvariable=self.xPositionVal, width=4, validate="all", validatecommand=(vcmdX, "%P"))
            self.xPositionEntry.grid(column=2, row=4, padx=5, pady=5, sticky=tk.W)
            self.yPositionLabel = ttk.Label(self.iconsFrame, text="\ny:\n0-685")
            self.yPositionLabel.grid(column=3, row=4, padx=5, pady=5, sticky=tk.E)
            self.yPositionVal = tk.StringVar()
            self.yPositionEntry = ttk.Entry(self.iconsFrame, textvariable=self.yPositionVal, width=4, validate="all", validatecommand=(vcmdY, "%P"))
            self.yPositionEntry.grid(column=4, row=4, padx=5, pady=5, sticky=tk.E)
            self.iconView = tk.Label(self.iconsFrame, width=26, height=2)
            self.iconView.grid(column=5, row=4, pady=5, sticky=tk.NSEW)

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
                self.rowSelectionMenuVal.set("")
                self.tileSelectionMenuList = []
                self.tileSelectionMenuVal.set("")
                self.iconMenuList = []
                self.iconMenuVal.set("")
                self.iconSaveErrorsVal.set("")
                self.iconSizeMenuVal.set("")
                self.iconImageErrorsVal.set("")
                self.xPositionVal.set("")
                self.yPositionVal.set("")
                
                self.encounterSetEntry.delete("1.0", tk.END)
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

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                
                # Encounter Name
                imageWithText.text((80, 25 + (10 if self.encounterNameEntry.get("1.0", "end").strip().count("\n") < 1 else 0)), self.encounterNameEntry.get("1.0", "end"), "white", fontEncounterName)
                
                # Flavor Text
                imageWithText.text((20, 88 + (7 if self.flavorEntry.get("1.0", "end").strip().count("\n") < 1 else 0)), self.flavorEntry.get("1.0", "end"), "black", fontFlavor)
                
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
                for icon in [icon for icon in self.icons if "" not in self.icons[icon]["position"]]:
                    image = self.icons[icon]["image"]
                    box = (int(self.icons[icon]["position"][0]), int(self.icons[icon]["position"][1]))
                    self.app.displayImage.paste(im=image, box=box, mask=image)

                self.customEncounter["set"] = self.encounterSetEntry.get("1.0", "end")
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
                self.customEncounter["icons"] = {k: v for k, v in self.icons.items() if "" not in self.icons[k]["position"]}
                self.customEncounter["tileSelections"] = {
                    1: {
                        "startingTile": {"value": self.tileSelections[1]["startingTile"]["value"].get()},
                        "startingNodes": {"value": self.tileSelections[1]["startingNodes"]["value"].get()},
                        "traps": {"value": self.tileSelections[1]["traps"]["value"].get()},
                        1: {"terrain": {"value": self.tileSelections[1][1]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": self.tileSelections[1][1]["enemies"][1]["value"].get()},
                                2: {"value": self.tileSelections[1][1]["enemies"][2]["value"].get()},
                                3: {"value": self.tileSelections[1][1]["enemies"][3]["value"].get()}
                            }},
                        2: {"terrain": {"value": self.tileSelections[1][2]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": self.tileSelections[1][2]["enemies"][1]["value"].get()},
                                2: {"value": self.tileSelections[1][2]["enemies"][2]["value"].get()},
                                3: {"value": self.tileSelections[1][2]["enemies"][3]["value"].get()}
                            }},
                        3: {"terrain": {"value": self.tileSelections[1][3]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": self.tileSelections[1][3]["enemies"][1]["value"].get()},
                                2: {"value": self.tileSelections[1][3]["enemies"][2]["value"].get()},
                                3: {"value": self.tileSelections[1][3]["enemies"][3]["value"].get()}
                            }},
                        4: {"terrain": {"value": self.tileSelections[1][4]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": self.tileSelections[1][4]["enemies"][1]["value"].get()},
                                2: {"value": self.tileSelections[1][4]["enemies"][2]["value"].get()},
                                3: {"value": self.tileSelections[1][4]["enemies"][3]["value"].get()}
                            }}
                        },
                    2: {
                        "startingTile": {"value": self.tileSelections[2]["startingTile"]["value"].get()},
                        "startingNodes": {"value": self.tileSelections[2]["startingNodes"]["value"].get()},
                        "traps": {"value": self.tileSelections[2]["traps"]["value"].get()},
                        1: {"terrain": {"value": self.tileSelections[2][1]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": self.tileSelections[2][1]["enemies"][1]["value"].get()},
                                2: {"value": self.tileSelections[2][1]["enemies"][2]["value"].get()},
                                3: {"value": self.tileSelections[2][1]["enemies"][3]["value"].get()}
                            }},
                        2: {"terrain": {"value": self.tileSelections[2][2]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": self.tileSelections[2][2]["enemies"][1]["value"].get()},
                                2: {"value": self.tileSelections[2][2]["enemies"][2]["value"].get()},
                                3: {"value": self.tileSelections[2][2]["enemies"][3]["value"].get()}
                            }},
                        3: {"terrain": {"value": self.tileSelections[2][3]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": self.tileSelections[2][3]["enemies"][1]["value"].get()},
                                2: {"value": self.tileSelections[2][3]["enemies"][2]["value"].get()},
                                3: {"value": self.tileSelections[2][3]["enemies"][3]["value"].get()}
                            }},
                        4: {"terrain": {"value": self.tileSelections[2][4]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": self.tileSelections[2][4]["enemies"][1]["value"].get()},
                                2: {"value": self.tileSelections[2][4]["enemies"][2]["value"].get()},
                                3: {"value": self.tileSelections[2][4]["enemies"][3]["value"].get()}
                            }}
                        },
                    3: {
                        "startingTile": {"value": self.tileSelections[3]["startingTile"]["value"].get()},
                        "startingNodes": {"value": self.tileSelections[3]["startingNodes"]["value"].get()},
                        "traps": {"value": self.tileSelections[3]["traps"]["value"].get()},
                        1: {"terrain": {"value": self.tileSelections[3][1]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": self.tileSelections[3][1]["enemies"][1]["value"].get()},
                                2: {"value": self.tileSelections[3][1]["enemies"][2]["value"].get()},
                                3: {"value": self.tileSelections[3][1]["enemies"][3]["value"].get()}
                            }},
                        2: {"terrain": {"value": self.tileSelections[3][2]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": self.tileSelections[3][2]["enemies"][1]["value"].get()},
                                2: {"value": self.tileSelections[3][2]["enemies"][2]["value"].get()},
                                3: {"value": self.tileSelections[3][2]["enemies"][3]["value"].get()}
                            }},
                        3: {"terrain": {"value": self.tileSelections[3][3]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": self.tileSelections[3][3]["enemies"][1]["value"].get()},
                                2: {"value": self.tileSelections[3][3]["enemies"][2]["value"].get()},
                                3: {"value": self.tileSelections[3][3]["enemies"][3]["value"].get()}
                            }},
                        4: {"terrain": {"value": self.tileSelections[3][4]["terrain"]["value"].get()},
                            "enemies": {
                                1: {"value": self.tileSelections[3][4]["enemies"][1]["value"].get()},
                                2: {"value": self.tileSelections[3][4]["enemies"][2]["value"].get()},
                                3: {"value": self.tileSelections[3][4]["enemies"][3]["value"].get()}
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
                for icon in self.icons:
                    if "" in self.icons[icon]["position"]:
                        continue
                    saveIcons[icon] = {k: v for k, v in self.icons[icon].items() if k not in {"image", "photoImage"}}

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

                # Check to see if there are any invalid keys in the JSON file.
                # This is about as sure as I can be that you can't load random JSON into the app.
                if set(self.customEncounter.keys()) != {
                        "set", "numberOfTiles", "level", "encounterName", "flavor", "objective", "keywords",
                        "specialRules", "rewardSouls", "rewardSoulsPerPlayer", "rewardSearch", "rewardDraw",
                        "rewardTrial", "rewardShortcut", "layout", "icons", "tileSelections"}:
                    self.app.set_bindings_buttons_menus(False)
                    PopupWindow(self.root, labelText="Invalid DSBG-Shuffle encounter file.", firstButton="Ok")
                    self.app.set_bindings_buttons_menus(True)
                    self.campaign = []
                    log("End of load_custom_encounter (invalid file)")
                    return
                
                self.customEncounter["image"] = self.app.create_image(" ".join(self.customEncounter["encounterName"].strip().replace("\n", " ").split()) + ".jpg", "encounter", 1, customEncounter=True)
                for icon in self.customEncounter["icons"]:
                    if not path.isfile(self.customEncounter["icons"][icon]["file"]):
                        PopupWindow(self.root, labelText="Missing custom icon image for " + icon + ".", firstButton="Ok")
                        return
                    i, p = self.app.create_image(self.customEncounter["icons"][icon]["file"], self.customEncounter["icons"][icon]["size"], 99, pathProvided=True, extensionProvided=True)
                    self.customEncounter["icons"][icon]["image"] = i
                    self.customEncounter["icons"][icon]["photoImage"] = p

                self.icons = self.customEncounter["icons"]
                self.iconMenuList = [icon for icon in self.icons.keys()]
                self.iconMenu.config(values=self.iconMenuList)
                self.iconMenu.set("")

                # Need to fill in all the GUI elements.
                self.encounterSetEntry.insert(tk.END, self.customEncounter["set"])
                self.numberOfTilesMenuVal.set(self.customEncounter["numberOfTiles"])
                self.levelMenuVal.set(self.customEncounter["level"])
                self.encounterNameEntry.insert(tk.END, self.customEncounter["encounterName"])
                self.flavorEntry.insert(tk.END, self.customEncounter["flavor"])
                self.objectiveEntry.insert(tk.END, self.customEncounter["objective"])
                self.keywordsEntry.insert(tk.END, self.customEncounter["keywords"])
                self.specialRulesEntry.insert(tk.END, self.customEncounter["specialRules"])
                self.rewardSoulsEntry.insert(tk.END, self.customEncounter["rewardSouls"])
                self.rewardSoulsPerPlayerVal.set(self.customEncounter["rewardSoulsPerPlayer"])
                self.rewardSearchEntry.insert(tk.END, self.customEncounter["rewardSearch"])
                self.rewardDrawEntry.insert(tk.END, self.customEncounter["rewardDraw"])
                self.rewardTrialEntry.insert(tk.END, self.customEncounter["rewardTrial"])
                self.shortcutVal.set(self.customEncounter["rewardShortcut"])
                self.tileLayoutMenuVal.set(self.customEncounter["layout"])
                self.tileSelections[1]["startingTile"]["value"].set(self.customEncounter["tileSelections"]["1"]["startingTile"]["value"])
                self.tileSelections[1]["startingNodes"]["value"].set(self.customEncounter["tileSelections"]["1"]["startingNodes"]["value"])
                self.tileSelections[1]["traps"]["value"].set(self.customEncounter["tileSelections"]["1"]["traps"]["value"])
                self.tileSelections[1][1]["terrain"]["value"].set(self.customEncounter["tileSelections"]["1"]["1"]["terrain"]["value"])
                self.tileSelections[1][1]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["1"]["1"]["enemies"]["1"]["value"])
                self.tileSelections[1][1]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["1"]["1"]["enemies"]["2"]["value"])
                self.tileSelections[1][1]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["1"]["1"]["enemies"]["3"]["value"])
                self.tileSelections[1][2]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["1"]["2"]["enemies"]["1"]["value"])
                self.tileSelections[1][2]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["1"]["2"]["enemies"]["2"]["value"])
                self.tileSelections[1][2]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["1"]["2"]["enemies"]["3"]["value"])
                self.tileSelections[1][3]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["1"]["3"]["enemies"]["1"]["value"])
                self.tileSelections[1][3]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["1"]["3"]["enemies"]["2"]["value"])
                self.tileSelections[1][3]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["1"]["3"]["enemies"]["3"]["value"])
                self.tileSelections[1][4]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["1"]["4"]["enemies"]["1"]["value"])
                self.tileSelections[1][4]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["1"]["4"]["enemies"]["2"]["value"])
                self.tileSelections[1][4]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["1"]["4"]["enemies"]["3"]["value"])
                self.tileSelections[2]["startingTile"]["value"].set(self.customEncounter["tileSelections"]["2"]["startingTile"]["value"])
                self.tileSelections[2]["startingNodes"]["value"].set(self.customEncounter["tileSelections"]["2"]["startingNodes"]["value"])
                self.tileSelections[2]["traps"]["value"].set(self.customEncounter["tileSelections"]["2"]["traps"]["value"])
                self.tileSelections[2][1]["terrain"]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["terrain"]["value"])
                self.tileSelections[2][1]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["enemies"]["1"]["value"])
                self.tileSelections[2][1]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["enemies"]["2"]["value"])
                self.tileSelections[2][1]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["2"]["1"]["enemies"]["3"]["value"])
                self.tileSelections[2][2]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["enemies"]["1"]["value"])
                self.tileSelections[2][2]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["enemies"]["2"]["value"])
                self.tileSelections[2][2]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["2"]["2"]["enemies"]["3"]["value"])
                self.tileSelections[2][3]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["2"]["3"]["enemies"]["1"]["value"])
                self.tileSelections[2][3]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["2"]["3"]["enemies"]["2"]["value"])
                self.tileSelections[2][3]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["2"]["3"]["enemies"]["3"]["value"])
                self.tileSelections[2][4]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["2"]["4"]["enemies"]["1"]["value"])
                self.tileSelections[2][4]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["2"]["4"]["enemies"]["2"]["value"])
                self.tileSelections[2][4]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["2"]["4"]["enemies"]["3"]["value"])
                self.tileSelections[3]["startingTile"]["value"].set(self.customEncounter["tileSelections"]["3"]["startingTile"]["value"])
                self.tileSelections[3]["startingNodes"]["value"].set(self.customEncounter["tileSelections"]["3"]["startingNodes"]["value"])
                self.tileSelections[3]["traps"]["value"].set(self.customEncounter["tileSelections"]["3"]["traps"]["value"])
                self.tileSelections[3][1]["terrain"]["value"].set(self.customEncounter["tileSelections"]["3"]["1"]["terrain"]["value"])
                self.tileSelections[3][1]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["3"]["1"]["enemies"]["1"]["value"])
                self.tileSelections[3][1]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["3"]["1"]["enemies"]["2"]["value"])
                self.tileSelections[3][1]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["3"]["1"]["enemies"]["3"]["value"])
                self.tileSelections[3][2]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["3"]["2"]["enemies"]["1"]["value"])
                self.tileSelections[3][2]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["3"]["2"]["enemies"]["2"]["value"])
                self.tileSelections[3][2]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["3"]["2"]["enemies"]["3"]["value"])
                self.tileSelections[3][3]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["3"]["3"]["enemies"]["1"]["value"])
                self.tileSelections[3][3]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["3"]["3"]["enemies"]["2"]["value"])
                self.tileSelections[3][3]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["3"]["3"]["enemies"]["3"]["value"])
                self.tileSelections[3][4]["enemies"][1]["value"].set(self.customEncounter["tileSelections"]["3"]["4"]["enemies"]["1"]["value"])
                self.tileSelections[3][4]["enemies"][2]["value"].set(self.customEncounter["tileSelections"]["3"]["4"]["enemies"]["2"]["value"])
                self.tileSelections[3][4]["enemies"][3]["value"].set(self.customEncounter["tileSelections"]["3"]["4"]["enemies"]["3"]["value"])

                for tile in range(1, 4):
                    self.toggle_starting_nodes_menu(tile=tile)
                    
                self.update_lists()

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


        def change_icon(self, event=None):
            try:
                log("Start of change_icon")

                icon = self.iconMenu.get()

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

                self.icons[icon]["image"], self.icons[icon]["photoImage"] = self.app.create_image(self.currentIcon["file"], self.currentIcon["size"], 99, pathProvided=True, extensionProvided=True)
                
                self.customEncounter["icons"] = {k: v for k, v in self.icons.items() if "" not in self.icons[k]["position"]}

                self.apply_changes()

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
                self.currentIcon["file"] = file
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