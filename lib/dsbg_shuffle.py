try:
    import datetime
    import errno
    import os
    import requests
    import sys
    import tkinter as tk
    import webbrowser
    from json import load
    from PIL import Image, ImageTk, UnidentifiedImageError
    from tkinter import ttk

    from dsbg_shuffle_behavior_decks import BehaviorDeckFrame
    from dsbg_shuffle_campaign import CampaignFrame
    from dsbg_shuffle_encounters import EncountersFrame
    from dsbg_shuffle_encounter_builder import EncounterBuilderFrame
    from dsbg_shuffle_enemies import enemyIds, enemiesDict, bosses
    from dsbg_shuffle_events import EventsFrame
    from dsbg_shuffle_settings import SettingsWindow
    from dsbg_shuffle_tooltip_reference import tooltipText
    from dsbg_shuffle_treasure import generate_treasure_soul_cost, populate_treasure_tiers, treasures
    from dsbg_shuffle_utility import CreateToolTip, PopupWindow, clear_other_tab_images, enable_binding, center, do_nothing, log, error_popup, baseFolder, pathSep
    from dsbg_shuffle_variants import VariantsFrame


    class Application(ttk.Frame):
        def __init__(self, parent):
            try:
                log("Initiating application")

                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep)) as settingsFile:
                    self.settings = load(settingsFile)

                with open(baseFolder + "\\lib\\dsbg_shuffle_encounters.json".replace("\\", pathSep)) as encountersFile:
                    self.encounters = load(encountersFile)

                self.add_custom_encounters()

                self.selected = None
                self.forPrinting = False
                self.tooltips = []
                self.coreSets = {"Dark Souls The Board Game", "Painted World of Ariamis", "Tomb of Giants", "The Sunless City"}
                self.allExpansions = set([self.encounters[encounter]["expansion"] for encounter in self.encounters]) | set(["Phantoms"])
                self.level4Expansions = set([self.encounters[encounter]["expansion"] for encounter in self.encounters if self.encounters[encounter]["level"] == 4])
                self.availableExpansions = set(self.settings["availableExpansions"])
                self.v1Expansions = {"Dark Souls The Board Game", "Darkroot", "Executioner Chariot", "Explorers", "Iron Keep"}
                self.v2Expansions = (self.allExpansions - self.v1Expansions - self.level4Expansions)
                self.enabledEnemies = set([enemiesDict[enemy.replace(" (V1)", "")].id for enemy in self.settings["enabledEnemies"] if enemy not in self.allExpansions])
                self.charactersActive = set(self.settings["charactersActive"])
                self.numberOfCharacters = len(self.charactersActive)
                self.availableCoreSets = self.coreSets & self.availableExpansions

                self.allEnemies = {enemy: {} for enemy in enemiesDict}

                root.withdraw()
                i = 0
                self.progress = PopupWindow(root, labelText="Starting up...", progressBar=True, progressMax=(len(self.allEnemies)*6) + (len(list(enemiesDict.keys()) + list(bosses.keys()))*3) + len([t for t in treasures if not treasures[t]["character"] or treasures[t]["character"] in self.charactersActive]), loadingImage=True)

                # Delete images from staging
                folder = baseFolder + "\\lib\\dsbg_shuffle_image_staging".replace("\\", pathSep)
                for filename in os.listdir(folder):
                    filePath = os.path.join(folder, filename)

                    if os.path.isfile(filePath) and filePath[-4:] == ".png":
                        os.unlink(filePath)

                ttk.Frame.__init__(self)
                self.grid_rowconfigure(index=1, weight=1)
                self.grid_rowconfigure(index=2, weight=0)
                self.displayScrollbar = ttk.Scrollbar(root)
                self.displayScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                self.bind("<1>", lambda event: event.widget.focus_set())

                # Create images
                self.progress.label.config(text = "Loading images... ")
                # Enemies
                for enemy in self.allEnemies:
                    i += 6
                    self.progress.progressVar.set(i)
                    root.update_idletasks()
                    self.allEnemies[enemy]["imageOld"] = self.create_image(enemy + ".png", "enemyOld")
                    self.allEnemies[enemy]["imageOldLevel4"] = self.create_image(enemy + ".png", "enemyOldLevel4")
                    self.allEnemies[enemy]["imageNew"] = self.create_image(enemy + ".png", "enemyNew")
                    self.allEnemies[enemy]["image text"] = self.create_image(enemy + ".png", "enemyText")
                    self.allEnemies[enemy]["image text" if self.forPrinting else "photo image text"] = ImageTk.PhotoImage(self.create_image(enemy + ".png", "enemyText"))

                # Icons
                self.enemyNode2 = self.create_image("enemy_node_2.png", "enemyNode")
                self.attack = {
                    "physical": {},
                    "magic": {},
                    "push": {}
                }
                for x in range(2, 14):
                    for y in ["physical", "magic", "push"]:
                        self.attack[y][x] = self.create_image("attack_" + y + "_" + str(x) + ".png", y if y == "push" else "attack")
                self.bleed = self.create_image("bleed.png", "bleed")
                self.frostbite = self.create_image("frostbite.png", "frostbite")
                self.poison = self.create_image("poison.png", "poison")
                self.stagger = self.create_image("stagger.png", "stagger")
                self.corrosion = self.create_image("corrosion.png", "corrosion")
                self.calamity = self.create_image("calamity.png", "calamity")
                self.repeat = {}
                for x in range(2, 6):
                    self.repeat[x] = self.create_image("repeat_" + str(x) + ".png", "repeat")
                self.sksMove = self.create_image("sks_move.png", "move")
                self.phalanxMove = self.create_image("phalanx_move.png", "move")

                # Keywords
                self.barrage = self.create_image("barrage.png", "barrage")
                self.bitterCold = self.create_image("bitter_cold.png", "bitterCold")
                self.darkness = self.create_image("darkness.png", "darkness")
                self.eerie = self.create_image("eerie.png", "eerie")
                self.gangAlonne = self.create_image("gang_alonne.png", "gangAlonne")
                self.gangHollow = self.create_image("gang_hollow.png", "gangHollow")
                self.gangSilverKnight = self.create_image("gang_silver_knight.png", "gangSilverKnight")
                self.gangSkeleton = self.create_image("gang_skeleton.png", "gangSkeleton")
                self.gangAlonnePhoto = ImageTk.PhotoImage(self.gangAlonne)
                self.gangHollowPhoto = ImageTk.PhotoImage(self.gangHollow)
                self.gangSilverKnightPhoto = ImageTk.PhotoImage(self.gangSilverKnight)
                self.gangSkeletonPhoto = ImageTk.PhotoImage(self.gangSkeleton)
                self.hidden = self.create_image("hidden.png", "hidden")
                self.illusion = self.create_image("illusion.png", "illusion")
                self.mimic = self.create_image("mimic_keyword.png", "mimic")
                self.onslaught = self.create_image("onslaught.png", "onslaught")
                self.poisonMist = self.create_image("poison_mist.png", "poisonMist")
                self.snowstorm = self.create_image("snowstorm.png", "snowstorm")
                self.timer = self.create_image("timer.png", "timer")
                self.trial = self.create_image("trial.png", "trial")

                self.rewardsDrawIcon = self.create_image("custom_encounter_rewards_draw.png", "reward", 99, extensionProvided=True)
                self.rewardsRefreshIcon = self.create_image("custom_encounter_rewards_refresh.png", "reward", 99, extensionProvided=True)
                self.rewardsSearchIcon = self.create_image("custom_encounter_rewards_search.png", "reward", 99, extensionProvided=True)
                self.rewardsShortcutIcon = self.create_image("custom_encounter_rewards_shortcut.png", "reward", 99, extensionProvided=True)
                self.rewardsSoulsIcon = self.create_image("custom_encounter_rewards_souls.png", "reward", 99, extensionProvided=True)
                self.rewardsSoulsPlayersIcon = self.create_image("custom_encounter_rewards_souls_players.png", "reward", 99, extensionProvided=True)
                self.rewardsTrialIcon = self.create_image("custom_encounter_rewards_trial.png", "reward", 99, extensionProvided=True)

                self.emptySetIcon = self.create_image("empty_set_icon.png", "levelIcon", 99, extensionProvided=True)

                self.levelIcons = {
                    1: self.create_image("custom_encounter_level1_icon.png", "levelIcon", 99, extensionProvided=True),
                    2: self.create_image("custom_encounter_level2_icon.png", "levelIcon", 99, extensionProvided=True),
                    3: self.create_image("custom_encounter_level3_icon.png", "levelIcon", 99, extensionProvided=True),
                    4: self.create_image("custom_encounter_level4_icon.png", "levelIcon", 99, extensionProvided=True)
                    }

                startingHorizontal = self.create_image("custom_encounter_starting_nodes_horizontal.png", "nodesHorizontal", 99, extensionProvided=True)
                startingVertical = self.create_image("custom_encounter_starting_nodes_vertical.png", "nodesVertical", 99, extensionProvided=True)

                self.terrain = {
                    "Barrel": self.create_image("barrel.png", "terrain", 99, extensionProvided=True),
                    "Envoy Banner": self.create_image("envoy_banner.png", "terrain", 99, extensionProvided=True),
                    "Exit": self.create_image("exit.png", "terrain", 99, extensionProvided=True),
                    "Fang Boar": self.create_image("fang_boar.png", "terrain", 99, extensionProvided=True),
                    "Gravestone": self.create_image("gravestone.png", "terrain", 99, extensionProvided=True),
                    "Lever": self.create_image("lever.png", "terrain", 99, extensionProvided=True),
                    "Shrine": self.create_image("shrine.png", "terrain", 99, extensionProvided=True),
                    "Torch": self.create_image("torch.png", "terrain", 99, extensionProvided=True),
                    "Treasure Chest": self.create_image("treasure_chest.png", "terrain", 99, extensionProvided=True)
                }

                self.tileNumbers = {}
                for x in range(1, 4):
                    s = str(x)
                    self.tileNumbers[x] = {
                        "starting": {
                            "traps": self.create_image("custom_encounter_starting_" + s + "_traps.png", "tileNum", 99, extensionProvided=True),
                            "noTraps": self.create_image("custom_encounter_starting_" + s + "_no_traps.png", "tileNum", 99, extensionProvided=True)
                        },
                        "notStarting": {
                            "traps": self.create_image("custom_encounter_not_starting_" + s + "_traps.png", "tileNum", 99, extensionProvided=True),
                            "noTraps": self.create_image("custom_encounter_not_starting_" + s + "_no_traps.png", "tileNum", 99, extensionProvided=True)
                        }
                    }

                self.tileLayouts = {
                    "1 Tile": {
                        "layout": self.create_image("custom_encounter_layout_1_tile.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": self.create_image("custom_encounter_1_tile_starting_nodes_horizontal.png", "nodes1TileHorizontal", 99, extensionProvided=True),
                        "startingNodesVertical": self.create_image("custom_encounter_1_tile_starting_nodes_vertical.png", "nodes1TileVertical", 99, extensionProvided=True),
                        "box": {
                            1: {
                                1: (59, 414),
                                2: (59, 555),
                                3: (59, 414),
                                4: (198, 414)
                                }
                            }
                        },
                    "1 Tile 4x4": {
                        "layout": self.create_image("custom_encounter_layout_1_tile_4x4.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": self.create_image("custom_encounter_4x4_starting_nodes_horizontal.png", "nodesLevel4Horizontal", 99, extensionProvided=True),
                        "startingNodesVertical": self.create_image("custom_encounter_4x4_starting_nodes_vertical.png", "nodesLevel4Vertical", 99, extensionProvided=True),
                        "box": {
                            1: {
                                1: (47, 403),
                                2: (47, 570),
                                3: (47, 403),
                                4: (212, 403)
                                }
                            }
                        },
                    "2 Tiles Horizontal": {
                        "layout": self.create_image("custom_encounter_layout_2_tiles_horizontal.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (44, 452),
                                2: (44, 524),
                                3: (44, 452),
                                4: (115, 452)
                                },
                            2: {
                                1: (152, 452),
                                2: (152, 524),
                                3: (152, 452),
                                4: (223, 452)
                                }
                            }
                        },
                    "2 Tiles Vertical": {
                        "layout": self.create_image("custom_encounter_layout_2_tiles_vertical.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (98, 402),
                                2: (98, 474),
                                3: (98, 402),
                                4: (169, 402)
                                },
                            2: {
                                1: (98, 509),
                                2: (98, 581),
                                3: (98, 509),
                                4: (169, 509)
                                }
                            }
                        },
                    "2 Tiles Illusion": {
                        "layout": self.create_image("custom_encounter_layout_2_tiles_illusion.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (98, 382),
                                2: (98, 454),
                                3: (98, 382),
                                4: (169, 382)
                                }
                            }
                        },
                    "2 Tiles Separated": {
                        "layout": self.create_image("custom_encounter_layout_2_tiles_separated.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (98, 382),
                                2: (98, 454),
                                3: (98, 382),
                                4: (169, 382)
                                },
                            2: {
                                1: (98, 522),
                                2: (98, 594),
                                3: (98, 522),
                                4: (169, 522)
                                }
                            }
                        },
                    "3 Tiles Vertical": {
                        "layout": self.create_image("custom_encounter_layout_3_tile_vertical.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (98, 347),
                                2: (98, 419),
                                3: (98, 347),
                                4: (169, 347)
                                },
                            2: {
                                1: (98, 455),
                                2: (98, 527),
                                3: (98, 455),
                                4: (169, 455)
                                },
                            3: {
                                1: (98, 562),
                                2: (98, 654),
                                3: (98, 562),
                                4: (169, 562)
                                }
                            }
                        },
                    "3 Tiles: 1 NE, 2 NW, 3 SW": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_NE_2_NW_3_SW.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (151, 402),
                                2: (151, 474),
                                3: (151, 402),
                                4: (222, 402)
                                },
                            2: {
                                1: (45, 402),
                                2: (45, 474),
                                3: (45, 402),
                                4: (116, 402)
                                },
                            3: {
                                1: (45, 509),
                                2: (45, 581),
                                3: (45, 509),
                                4: (116, 509)
                                }
                            }
                        },
                    "3 Tiles: 1 NW, 2 NE, 3 SW": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_NW_2_NE_3_SW.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (45, 402),
                                2: (45, 474),
                                3: (45, 402),
                                4: (116, 402)
                                },
                            2: {
                                1: (151, 402),
                                2: (151, 474),
                                3: (151, 402),
                                4: (222, 402)
                                },
                            3: {
                                1: (45, 509),
                                2: (45, 581),
                                3: (45, 509),
                                4: (116, 509)
                                }
                            }
                        },
                    "3 Tiles: 1 NW, 2 SW, 3 SE": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_NW_2_SW_3_SE.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (45, 402),
                                2: (45, 474),
                                3: (45, 402),
                                4: (116, 402)
                                },
                            2: {
                                1: (45, 509),
                                2: (45, 581),
                                3: (45, 509),
                                4: (116, 509)
                                },
                            3: {
                                1: (151, 509),
                                2: (151, 581),
                                3: (151, 509),
                                4: (222, 509)
                                }
                            }
                        },
                    "3 Tiles: 1 SE, 2 NE, 3 NW": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_SE_2_NE_3_NW.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (151, 509),
                                2: (151, 581),
                                3: (151, 509),
                                4: (222, 509)
                                },
                            2: {
                                1: (151, 402),
                                2: (151, 474),
                                3: (151, 402),
                                4: (222, 402)
                                },
                            3: {
                                1: (45, 402),
                                2: (45, 474),
                                3: (45, 402),
                                4: (116, 402)
                                }
                            }
                        },
                    "3 Tiles: 1 SW, 2 NW, 3 SE": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_SW_2_NW_3_SE.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (45, 509),
                                2: (45, 581),
                                3: (45, 509),
                                4: (116, 509)
                                },
                            2: {
                                1: (45, 402),
                                2: (45, 474),
                                3: (45, 402),
                                4: (116, 402)
                                },
                            3: {
                                1: (151, 509),
                                2: (151, 581),
                                3: (151, 509),
                                4: (222, 509)
                                }
                            }
                        },
                    "3 Tiles: 1 SW, 2 SE, 3 NE": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_SW_2_SE_3_NE.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (45, 509),
                                2: (45, 581),
                                3: (45, 509),
                                4: (116, 509)
                                },
                            2: {
                                1: (151, 509),
                                2: (151, 581),
                                3: (151, 509),
                                4: (222, 509)
                                },
                            3: {
                                1: (151, 402),
                                2: (151, 474),
                                3: (151, 402),
                                4: (222, 402)
                                }
                            }
                        },
                    "3 Tiles Illusion": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_illusion.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (38, 393),
                                2: (38, 465),
                                3: (38, 393),
                                4: (109, 393)
                                }
                            }
                        },
                    "3 Tiles Separated": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_separated.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (38, 393),
                                2: (38, 465),
                                3: (38, 393),
                                4: (109, 393)
                                }
                            }
                        },
                    "3 Tiles, Tile 1 Separated": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_1_separate.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (39, 393),
                                2: (39, 465),
                                3: (39, 393),
                                4: (110, 393)
                                },
                            2: {
                                1: (39, 514),
                                2: (39, 586),
                                3: (39, 514),
                                4: (110, 514)
                                },
                            3: {
                                1: (145, 514),
                                2: (145, 586),
                                3: (145, 514),
                                4: (216, 514)
                                }
                            }
                        },
                    "3 Tiles, Tile 3 Separated": {
                        "layout": self.create_image("custom_encounter_layout_3_tiles_3_separate.png", "layout", 99, extensionProvided=True),
                        "startingNodesHorizontal": startingHorizontal,
                        "startingNodesVertical": startingVertical,
                        "box": {
                            1: {
                                1: (38, 407),
                                2: (38, 479),
                                3: (38, 407),
                                4: (109, 407)
                                },
                            2: {
                                1: (38, 514),
                                2: (38, 586),
                                3: (38, 514),
                                4: (109, 514)
                                },
                            3: {
                                1: (158, 514),
                                2: (158, 586),
                                3: (158, 514),
                                4: (229, 514)
                                }
                            }
                        }
                }
                
                self.progress.label.config(text="Loading treasure...")
                if self.settings["treasureSwapOption"] in {"Similar Soul Cost", "Tier Based"}:
                    generate_treasure_soul_cost(self.availableExpansions, self.charactersActive, root, self.progress)
                i = len([t for t in treasures if not treasures[t]["character"] or treasures[t]["character"] in self.charactersActive])
                if self.settings["treasureSwapOption"] == "Tier Based":
                    populate_treasure_tiers(self.availableExpansions, self.charactersActive)

                self.create_tabs()
                self.create_buttons()
                self.create_display_frame()
                self.create_menu()
                self.set_bindings_buttons_menus(True)

                root.state("zoomed")

                self.progress.destroy()
                root.deiconify()
            except Exception as e:
                error_popup(root, e)
                raise


        def on_frame_configure(self, canvas):
            """Reset the scroll region to encompass the inner frame"""
            canvas.configure(scrollregion=canvas.bbox("all"))


        def _bound_to_mousewheel(self, event):
            self.displayCanvas.bind_all("<MouseWheel>", self._on_mousewheel)


        def _unbound_to_mousewheel(self, event):
            self.displayCanvas.unbind_all("<MouseWheel>")


        def _on_mousewheel(self, event):
            self.displayCanvas.yview_scroll(int(-1*(event.delta/120)), "units")


        def create_tabs(self, event=None):
            """
            Create the tabs in the main window.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of create_tabs")

                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep)) as settingsFile:
                    self.settings = load(settingsFile)

                self.paned = ttk.PanedWindow(self)
                self.paned.bind("<1>", lambda event: event.widget.focus_set())
                self.paned.grid_rowconfigure(index=0, weight=1)
                self.paned.grid(row=1, column=0, pady=(5, 5), padx=(5, 5), sticky="nsew", columnspan=4)

                self.pane = ttk.Frame(self.paned, padding=5)
                self.pane.bind("<1>", lambda event: event.widget.focus_set())
                self.pane.grid_rowconfigure(index=0, weight=1)
                self.paned.add(self.pane, weight=1)

                self.notebook = ttk.Notebook(self.paned, width=600)
                self.notebook.bind("<1>", lambda event: event.widget.focus_set())
                self.notebook.bind('<<NotebookTabChanged>>', self.tab_change)
                self.notebook.pack(fill="both", expand=True)

                self.campaignTab = CampaignFrame(root=root, app=self)
                self.campaignTab.bind("<1>", lambda event: event.widget.focus_set())
                self.notebook.add(self.campaignTab, text="Campaign")
                
                self.eventTab = EventsFrame(root=root, app=self)
                self.eventTab.bind("<1>", lambda event: event.widget.focus_set())
                self.notebook.add(self.eventTab, text="Events")

                self.variantsTab = VariantsFrame(root=root, app=self)
                self.variantsTab.bind("<1>", lambda event: event.widget.focus_set())
                self.notebook.add(self.variantsTab, text="Behavior Variants")

                self.behaviorDeckTab = BehaviorDeckFrame(root=root, app=self)
                self.behaviorDeckTab.bind("<1>", lambda event: event.widget.focus_set())
                self.notebook.add(self.behaviorDeckTab, text="Behavior Decks")

                self.encounterBuilderTab = EncounterBuilderFrame(root=root, app=self)
                self.encounterBuilderTab.bind("<1>", lambda event: event.widget.focus_set())
                self.notebook.add(self.encounterBuilderTab, text="Encounter Builder")

                self.encounterTab = EncountersFrame(root=root, app=self)
                self.encounterTab.bind("<1>", lambda event: event.widget.focus_set())
                for index in [0, 1]:
                    self.encounterTab.columnconfigure(index=index, weight=1)
                    self.encounterTab.rowconfigure(index=index, weight=1)
                self.notebook.insert(0, self.encounterTab, text="Encounters")

                self.notebook.select(0)

                log("End of create_tabs")
            except Exception as e:
                error_popup(root, e)
                raise


        def tab_change(self, event=None):
            """
            Clear the current image and open the last selected image, if any.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of tab_change")

                if self.notebook.tab(self.notebook.select(), "text") == "Encounters" and self.encounterTab.treeviewEncounters.selection():
                    tree = self.encounterTab.treeviewEncounters
                    self.encounterTab.load_encounter(encounter=tree.item(tree.selection())["text"])
                elif self.notebook.tab(self.notebook.select(), "text") == "Campaign" and self.campaignTab.treeviewCampaign.selection():
                    self.campaignTab.load_campaign_card()
                elif self.notebook.tab(self.notebook.select(), "text") == "Events":
                    self.eventTab.load_event()
                elif self.notebook.tab(self.notebook.select(), "text") == "Behavior Decks" and self.behaviorDeckTab.treeviewDecks.selection():
                    self.behaviorDeckTab.display_deck_cards()
                elif self.notebook.tab(self.notebook.select(), "text") == "Behavior Variants":
                    if self.variantsTab.treeviewVariantsLocked.selection():
                        self.variantsTab.load_variant_card_locked(variant=self.variantsTab.treeviewVariantsLocked.selection()[0])
                    elif self.variantsTab.treeviewVariantsList.selection():
                        self.variantsTab.load_variant_card(variant=self.variantsTab.treeviewVariantsList.selection()[0])
                elif self.notebook.tab(self.notebook.select(), "text") == "Encounter Builder":
                    self.encounterBuilderTab.apply_changes()
                else:
                    log("End of tab_change (cleared image only)")
                    return

                log("End of tab_change")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_display_frame(self):
            """
            Create the frame in which cards will be displayed.
            """
            try:
                log("Start of create_display_frame")

                self.displayCanvas = tk.Canvas(self, width=820, yscrollcommand=self.displayScrollbar.set)
                self.displayFrame = ttk.Frame(self.displayCanvas)
                self.displayFrame.columnconfigure(index=0, weight=1, minsize=410)
                self.displayCanvas.grid(row=0, column=4, padx=10, pady=(10, 0), sticky="nsew", rowspan=2)
                self.displayCanvas.create_window((0,0), window=self.displayFrame, anchor=tk.NW)
                self.displayScrollbar.config(command=self.displayCanvas.yview)
                self.displayFrame.bind("<Enter>", self._bound_to_mousewheel)
                self.displayFrame.bind("<Leave>", self._unbound_to_mousewheel)
                self.displayFrame.bind("<Configure>", lambda event, canvas=self.displayCanvas: self.on_frame_configure(canvas))

                self.displayTopLeft = ttk.Label(self.displayFrame)
                self.displayTopLeft.image = None
                self.displayTopLeft.grid(column=0, row=0, sticky="nsew")
                self.displayTopRight = ttk.Label(self.displayFrame)
                self.displayTopRight.image = None
                self.displayTopRight.grid(column=1, row=0, sticky="nsew", columnspan=2)
                self.displayBottomLeft = ttk.Label(self.displayFrame)
                self.displayBottomLeft.image = None
                self.displayBottomLeft.grid(column=0, row=1, sticky="nsew")
                self.displayBottomRight = ttk.Label(self.displayFrame)
                self.displayBottomRight.image = None
                self.displayBottomRight.grid(column=1, row=1, sticky="nsew", columnspan=2)

                # Frames for health trackers
                self.displayKing1 = ttk.Label(self.displayFrame)
                self.displayKing1.image = None
                self.displayKing2 = ttk.Label(self.displayFrame)
                self.displayKing2.image = None
                self.displayKing3 = ttk.Label(self.displayFrame)
                self.displayKing3.image = None
                self.displayKing4 = ttk.Label(self.displayFrame)
                self.displayKing4.image = None

                self.displayKing1.bind("<Button 1>", lambda event, x=1: app.behaviorDeckTab.lower_health_king(event=event, king=1, amount=x))
                self.displayKing1.bind("<Shift-Button 1>", lambda event, x=5: app.behaviorDeckTab.lower_health_king(event=event, king=1, amount=x))
                self.displayKing1.bind("<Button 3>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=1, amount=x))
                self.displayKing1.bind("<Shift-Button 3>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=1, amount=x))
                self.displayKing1.bind("<Control-1>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=1, amount=x))
                self.displayKing1.bind("<Shift-Control-1>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=1, amount=x))

                self.displayKing2.bind("<Button 1>", lambda event, x=1: app.behaviorDeckTab.lower_health_king(event=event, king=2, amount=x))
                self.displayKing2.bind("<Shift-Button 1>", lambda event, x=5: app.behaviorDeckTab.lower_health_king(event=event, king=2, amount=x))
                self.displayKing2.bind("<Button 3>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=2, amount=x))
                self.displayKing2.bind("<Shift-Button 3>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=2, amount=x))
                self.displayKing2.bind("<Control-1>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=2, amount=x))
                self.displayKing2.bind("<Shift-Control-1>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=2, amount=x))

                self.displayKing3.bind("<Button 1>", lambda event, x=1: app.behaviorDeckTab.lower_health_king(event=event, king=3, amount=x))
                self.displayKing3.bind("<Shift-Button 1>", lambda event, x=5: app.behaviorDeckTab.lower_health_king(event=event, king=3, amount=x))
                self.displayKing3.bind("<Button 3>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=3, amount=x))
                self.displayKing3.bind("<Shift-Button 3>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=3, amount=x))
                self.displayKing3.bind("<Control-1>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=3, amount=x))
                self.displayKing3.bind("<Shift-Control-1>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=3, amount=x))

                self.displayKing4.bind("<Button 1>", lambda event, x=1: app.behaviorDeckTab.lower_health_king(event=event, king=4, amount=x))
                self.displayKing4.bind("<Shift-Button 1>", lambda event, x=5: app.behaviorDeckTab.lower_health_king(event=event, king=4, amount=x))
                self.displayKing4.bind("<Button 3>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=4, amount=x))
                self.displayKing4.bind("<Shift-Button 3>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=4, amount=x))
                self.displayKing4.bind("<Control-1>", lambda event, x=1: app.behaviorDeckTab.raise_health_king(event=event, king=4, amount=x))
                self.displayKing4.bind("<Shift-Control-1>", lambda event, x=5: app.behaviorDeckTab.raise_health_king(event=event, king=4, amount=x))

                for enemy in [e for e in self.enabledEnemies if "Phantoms" not in enemyIds[e].expansions and enemyIds[e].name not in {"Hungry Mimic", "Voracious Mimic"}]:
                    self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"] = []
                    for _ in range(8):
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"].append(ttk.Label(self.displayFrame))
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].image = None
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].bind("<Button 1>", lambda event, x=1: app.behaviorDeckTab.lower_health_regular(event=event, amount=x))
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].bind("<Shift-Button 1>", lambda event, x=5: app.behaviorDeckTab.lower_health_regular(event=event, amount=x))
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].bind("<Button 3>", lambda event, x=1: app.behaviorDeckTab.raise_health_regular(event=event, amount=x))
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].bind("<Shift-Button 3>", lambda event, x=5: app.behaviorDeckTab.raise_health_regular(event=event, amount=x))
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].bind("<Control-1>", lambda event, x=1: app.behaviorDeckTab.raise_health_regular(event=event, amount=x))
                        self.behaviorDeckTab.decks[enemyIds[enemy].name]["healthTrackers"][-1].bind("<Shift-Control-1>", lambda event, x=5: app.behaviorDeckTab.raise_health_regular(event=event, amount=x))

                self.displayImages = {
                    "encounters": {
                        self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                    },
                    "events": {
                        self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                    },
                    "variants": {
                        self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                    },
                    "variantsLocked": {
                        self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                    },
                    "behaviorDeck": {
                        self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                        self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                    }
                }

                log("End of create_display_frame")
            except Exception as e:
                error_popup(root, e)
                raise


        def add_custom_encounters(self):
            """
            Adds custom encounters to the list of all encounters.
            """
            try:
                log("Start of add_custom_encounters")
                    
                self.customEncounters = [e.split("_") for e in set([os.path.splitext(f)[0] for f in os.listdir(baseFolder + "\\lib\\dsbg_shuffle_custom_encounters".replace("\\", pathSep)) if f.count("_") == 2 and ".jpg" in f])]
                
                for enc in [enc for enc in self.customEncounters if "Custom - " + enc[1] not in self.encounters]:
                    self.encounters["Custom - " + enc[1]] = {
                        "name": enc[1],
                        "expansion": enc[0],
                        "level": int(enc[2]),
                        "expansionCombos": {
                            "1": [[enc[0]]],
                            "2": [[enc[0]]],
                            "3": [[enc[0]]],
                            "4": [[enc[0]]]
                            },
                        "alts": {
                            "enemySlots": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            "alternatives": {enc[0]: []},
                            "original": []
                            }
                        }

                log("End of add_custom_encounters")
            except Exception as e:
                error_popup(root, e)
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
                log("Start of set_bindings_buttons_menus: enable=" + str(enable))

                if enable:
                    enable_binding("Control-Key-1", lambda x: self.keybind_call("1"), root)
                    enable_binding("Control-Key-2", lambda x: self.keybind_call("2"), root)
                    enable_binding("Control-Key-3", lambda x: self.keybind_call("3"), root)
                    enable_binding("Control-Key-4", lambda x: self.keybind_call("4"), root)
                    enable_binding("Control-s", self.encounterTab.shuffle_enemies, root)
                    enable_binding("Control-c", self.campaignTab.add_card_to_campaign, root)
                    enable_binding("Control-q", lambda x: self.keybind_call("q"), root)
                    self.fileMenu.entryconfig("Random Level 1 Encounter", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Random Level 2 Encounter", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Random Level 3 Encounter", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Random Level 4 Encounter", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Shuffle Enemies", state=tk.NORMAL)
                    self.fileMenu.entryconfig("Add to Campaign", state=tk.NORMAL)
                else:
                    enable_binding("Key-1", do_nothing, root)
                    enable_binding("Key-2", do_nothing, root)
                    enable_binding("Key-3", do_nothing, root)
                    enable_binding("Key-4", do_nothing, root)
                    enable_binding("s", do_nothing, root)
                    enable_binding("c", do_nothing, root)
                    self.fileMenu.entryconfig("Random Level 1 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Random Level 2 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Random Level 3 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Random Level 4 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Shuffle Enemies", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Add to Campaign", state=tk.DISABLED)

                if "level4" not in self.settings["encounterTypes"]:
                    self.fileMenu.entryconfig("Random Level 4 Encounter", state=tk.DISABLED)

                if ["level4"] == self.settings["encounterTypes"]:
                    self.fileMenu.entryconfig("Random Level 1 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Random Level 2 Encounter", state=tk.DISABLED)
                    self.fileMenu.entryconfig("Random Level 3 Encounter", state=tk.DISABLED)

                log("End of set_bindings_buttons_menus")
            except Exception as e:
                error_popup(root, e)
                raise


        def open_wiki(self):
            """
            Opens the wiki to the appropriate page.
            """
            try:
                log("Start of open_wiki")

                tab = self.notebook.tab(self.notebook.select(), "text")
                log("Opening https://github.com/DanDuhon/DSBG-Shuffle/wiki/" + tab)
                webbrowser.open_new("https://github.com/DanDuhon/DSBG-Shuffle/wiki/" + tab)
                
                log("End of open_wiki")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_buttons(self):
            """
            Create the buttons on the main screen.
            """
            try:
                log("Start of create_buttons")

                self.buttonsFrame = ttk.Frame(self)
                self.buttonsFrame.grid(row=0, column=0, pady=(10, 0), sticky="nw")
                self.buttonsFrame.columnconfigure(index=0, weight=1)
                self.campaignButton = ttk.Button(self.buttonsFrame, text="Add to Campaign", width=16, command=self.campaignTab.add_card_to_campaign)
                self.campaignButton.grid(column=0, row=1, padx=5, pady=5)

                # Link to the wiki
                wikiLink = ttk.Button(self.buttonsFrame, text="Open the wiki", width=16, command=self.open_wiki)
                wikiLink.grid(column=3, row=1)
                
                log("End of create_buttons")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_menu(self):
            """
            Create the menu.
            """
            try:
                log("Start of create_menu")

                menuBar = tk.Menu()
                self.fileMenu = tk.Menu(menuBar, tearoff=0)
                self.fileMenu.add_command(label="Random Level 1 Encounter", command=lambda x=1: self.encounterTab.random_encounter(level=x), accelerator="Ctrl+1")
                self.fileMenu.add_command(label="Random Level 2 Encounter", command=lambda x=2: self.encounterTab.random_encounter(level=x), accelerator="Ctrl+2")
                self.fileMenu.add_command(label="Random Level 3 Encounter", command=lambda x=3: self.encounterTab.random_encounter(level=x), accelerator="Ctrl+3")
                self.fileMenu.add_command(label="Random Level 4 Encounter", command=lambda x=4: self.encounterTab.random_encounter(level=x), accelerator="Ctrl+4")
                self.fileMenu.add_command(label="Shuffle Enemies", command=self.encounterTab.shuffle_enemies, accelerator="Ctrl+S")
                self.fileMenu.add_command(label="Add to Campaign", command=self.campaignTab.add_card_to_campaign, accelerator="Ctrl+C")
                self.fileMenu.add_separator()
                self.fileMenu.add_command(label="Quit", command=root.quit, accelerator="Ctrl+Q")
                menuBar.add_cascade(label="File", menu=self.fileMenu)

                self.optionsMenu = tk.Menu(menuBar, tearoff=0)
                self.optionsMenu.add_command(label="View/Change Settings", command=self.settings_window)
                menuBar.add_cascade(label="Settings", menu=self.optionsMenu)

                root.config(menu=menuBar)

                log("End of create_menu")
            except Exception as e:
                error_popup(root, e)
                raise


        def keybind_call(self, call, event=None):
            """
            Keyboard shortcuts.

            Required Parameters:
                call: String
                    The keybind activated.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of keybind_call: call=" + call)

                if call == "1" and self.settings["encounterTypes"] != ["level4"]:
                    self.encounterTab.random_encounter(level=1)
                elif call == "2" and self.settings["encounterTypes"] != ["level4"]:
                    self.encounterTab.random_encounter(level=2)
                elif call == "3" and self.settings["encounterTypes"] != ["level4"]:
                    self.encounterTab.random_encounter(level=3)
                elif call == "4" and "level4" in self.settings["encounterTypes"]:
                    self.encounterTab.random_encounter(level=4)
                elif call == "s":
                    self.encounterTab.shuffle_enemies()
                elif call == "c":
                    self.campaignTab.add_card_to_campaign()
                elif call == "q":
                    root.quit()

                log("End of keybind_call")
            except Exception as e:
                error_popup(root, e)
                raise


        def settings_window(self):
            """
            Show the settings window, where a user can change what expansions are active and
            whether random self.encounters show old, new, or both kinds of self.encounters.
            """
            try:
                log("Start of settings_window")

                self.set_bindings_buttons_menus(False)

                oldSettings = {k:v for k, v in self.settings.items()}
                oldTreasureSwapOption = self.settings["treasureSwapOption"]
                oldCustomEnemyList = self.settings["customEnemyList"]

                s = SettingsWindow(app, root, self.coreSets)

                self.wait_window(s.top)

                with open(baseFolder + "\\lib\\dsbg_shuffle_settings.json".replace("\\", pathSep)) as settingsFile:
                    self.settings = load(settingsFile)

                if self.settings != oldSettings:
                    self.selected = None
                    self.rewardTreasure = None
                    self.displayTopLeft.config(image="")
                    self.displayTopLeft.image=None
                    self.displayTopRight.config(image="")
                    self.displayTopRight.image=None
                    self.displayBottomLeft.config(image="")
                    self.displayBottomLeft.image=None
                    self.displayBottomRight.config(image="")
                    self.displayBottomRight.image=None

                    self.displayImages = {
                        "encounters": {
                            self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                        },
                        "events": {
                            self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                        },
                        "variants": {
                            self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                        },
                        "variantsLocked": {
                            self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                        },
                        "behaviorDeck": {
                            self.displayTopLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayTopRight: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomLeft: {"name": None, "image": None, "activeTab": None},
                            self.displayBottomRight: {"name": None, "image": None, "activeTab": None}
                        }
                    }

                    self.encounterTab.treeviewEncounters.pack_forget()
                    self.encounterTab.treeviewEncounters.destroy()
                    self.availableExpansions = set(self.settings["availableExpansions"])
                    self.availableCoreSets = self.coreSets & self.availableExpansions
                    self.expansionsForRandomEncounters = self.allExpansions & ((self.v1Expansions if "v1" in self.settings["encounterTypes"] else set()) | (self.v2Expansions if "v2" in self.settings["encounterTypes"] else set()))
                    self.charactersActive = set(self.settings["charactersActive"])
                    self.numberOfCharacters = len(self.charactersActive)
                    self.encounterTab.set_encounter_list()
                    self.encounterTab.create_encounters_treeview()
                    self.variantsTab.reset_treeview()
                    self.behaviorDeckTab.reset_treeview()

                    self.bossMenuItems = [
                        "Select Boss",
                        "--Mini Bosses--"
                        ]
                    for boss in [boss for boss in bosses if bosses[boss]["level"] == "Mini Boss" and bosses[boss]["expansions"] & self.availableExpansions]:
                        self.bossMenuItems.append(bosses[boss]["name"])

                    self.bossMenuItems.append("--Main Bosses--")
                    for boss in [boss for boss in bosses if bosses[boss]["level"] == "Main Boss" and bosses[boss]["expansions"] & self.availableExpansions]:
                        self.bossMenuItems.append(bosses[boss]["name"])

                    self.bossMenuItems.append("--Mega Bosses--")
                    for boss in [boss for boss in bosses if bosses[boss]["level"] == "Mega Boss" and bosses[boss]["expansions"] & self.availableExpansions]:
                        self.bossMenuItems.append(bosses[boss]["name"])

                    self.campaignTab.bossMenu["values"] = self.bossMenuItems

                    self.campaignTab.selectedBoss.set("Select Boss")

                    # Recalculate the average soul cost of treasure.
                    if (oldTreasureSwapOption != self.settings["treasureSwapOption"] and self.settings["treasureSwapOption"] in {"Similar Soul Cost", "Tier Based"}) or (oldCustomEnemyList != self.settings["customEnemyList"] and self.settings["customEnemyList"]):
                        i = 0
                        progress = PopupWindow(root, labelText="Reloading treasure...", progressBar=True, progressMax=len([t for t in treasures if not treasures[t]["character"] or treasures[t]["character"] in self.charactersActive]), loadingImage=True)
                        if oldTreasureSwapOption != self.settings["treasureSwapOption"] and self.settings["treasureSwapOption"] in {"Similar Soul Cost", "Tier Based"}:
                            i = generate_treasure_soul_cost(self.availableExpansions, self.charactersActive, root, progress)
                            if self.settings["treasureSwapOption"] == "Tier Based":
                                populate_treasure_tiers(self.availableExpansions, self.charactersActive)
                        progress.destroy()
                    
                    if oldCustomEnemyList != self.settings["customEnemyList"] and self.settings["customEnemyList"]:
                        i = 0
                        progress = PopupWindow(root, labelText="Applying custom enemy list...", progressBar=True, progressMax=len(self.encounterTab.encounterList), loadingImage=True)
                        
                        self.enabledEnemies = set([enemiesDict[enemy.replace(" (V1)", "")].id for enemy in self.settings["enabledEnemies"] if enemy not in self.allExpansions])

                        self.encountersToRemove = set()
                        for encounter in self.encounterTab.encounterList:
                            i += 1
                            progress.progressVar.set(i)
                            root.update_idletasks()
                            self.encounterTab.load_encounter(encounter=encounter, customEnemyListCheck=True)
                            if all([not set(alt).issubset(self.enabledEnemies) for alt in self.selected["alternatives"]]):
                                self.encountersToRemove.add(encounter)

                        self.encounterTab.encounterList = list(set(self.encounterTab.encounterList) - self.encountersToRemove)
                        
                        self.encounterTab.treeviewEncounters.pack_forget()
                        self.encounterTab.treeviewEncounters.destroy()
                        self.encounterTab.create_encounters_treeview()

                        progress.destroy()

                self.set_bindings_buttons_menus(True)
                
                if "level4" not in self.settings["encounterTypes"]:
                    self.encounterTab.l4["state"] = "disabled"
                else:
                    self.encounterTab.l4["state"] = "enabled"
                
                if ["level4"] == self.settings["encounterTypes"]:
                    self.encounterTab.l1["state"] = "disabled"
                    self.encounterTab.l2["state"] = "disabled"
                    self.encounterTab.l3["state"] = "disabled"
                else:
                    self.encounterTab.l1["state"] = "enabled"
                    self.encounterTab.l2["state"] = "enabled"
                    self.encounterTab.l3["state"] = "enabled"

                log("End of settings_window")
            except Exception as e:
                error_popup(root, e)
                raise


        def create_image(self, imageFileName, imageType, level=None, expansion=None, pathProvided=False, extensionProvided=False, customEncounter=False, emptySetIcon=False):
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
                log("Start of create_image, imageFileName={}, imageType={}, level={}, expansion={}".format(str(imageFileName), str(imageType), str(level), str(expansion)))

                if imageType in {"encounter", "customEncounter"}:
                    if imageFileName == "Ornstein & Smough.jpg" or imageFileName == "Ornstein & Smough - data.jpg":
                        width = 305
                        height = 850
                    elif level < 4 and expansion in {"Dark Souls The Board Game", "Iron Keep", "Darkroot", "Explorers", "Executioner Chariot"}:
                        width = 200
                        height = 300
                    elif level == 4:
                        width = 305
                        height = 424
                    else:
                        width = 400
                        height = 685

                    fileName = imageFileName[:-4] if not extensionProvided else imageFileName
                    if expansion == "The Sunless City" and imageFileName[:-4] in set(["Broken Passageway", "Central Plaza"]):
                        fileName += " (TSC)"
                    fileName += ".jpg" if not extensionProvided else ""

                    if pathProvided:
                        imagePath = fileName
                    elif customEncounter:
                        key = "Custom - " + fileName[:-4]
                        imagePath = baseFolder + "\\lib\\dsbg_shuffle_custom_encounters\\".replace("\\", pathSep) + self.encounters[key]["expansion"] + "_" + fileName[:-4] + "_" + str(self.encounters[key]["level"]) + ".jpg"
                    elif "custom_encounter_" in fileName:
                        imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\custom_encounters\\".replace("\\", pathSep) + fileName
                    else:
                        imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\encounters\\".replace("\\", pathSep) + fileName
                    log("\tOpening " + imagePath)
                    self.displayImage = Image.open(imagePath).resize((width, height), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.displayImage)
                elif imageType == "event":
                    width = 305
                    height = 424
                        
                    fileName = imageFileName[:-4] if not extensionProvided else imageFileName
                    fileName += ".jpg" if not extensionProvided else ""

                    if pathProvided:
                        imagePath = fileName
                    else:
                        imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\events\\".replace("\\", pathSep) + fileName
                    log("\tOpening " + imagePath)
                    self.displayImage = Image.open(imagePath).resize((width, height), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.displayImage)
                elif imageType == "enemyCard":
                    width = 305
                    height = 424
                        
                    fileName = imageFileName[:-4] if not extensionProvided else imageFileName
                    fileName += ".jpg" if not extensionProvided else ""

                    if pathProvided:
                        imagePath = fileName
                    else:
                        imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\enemies\\".replace("\\", pathSep) + fileName
                    log("\tOpening " + imagePath)
                    self.displayImage = Image.open(imagePath).resize((width, height), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.displayImage)
                elif imageType == "enemyText":
                    imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\enemies\\".replace("\\", pathSep) + imageFileName[:-4] + " rule bg.jpg"
                    log("\tOpening " + imagePath)
                    image = Image.open(imagePath).resize((14, 14), Image.Resampling.LANCZOS)
                elif imageType == "healthTracker":
                    imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\enemies\\".replace("\\", pathSep) + imageFileName
                    log("\tOpening " + imagePath)
                    self.displayImage = Image.open(imagePath).resize((102, 55), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.displayImage)
                elif imageType == "fourKingsHealth":
                    imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\enemies\\".replace("\\", pathSep) + imageFileName
                    log("\tOpening " + imagePath)
                    self.displayImage = Image.open(imagePath).resize((155, 55), Image.Resampling.LANCZOS)
                    image = ImageTk.PhotoImage(self.displayImage)
                else:
                    if pathProvided:
                        imagePath = imageFileName
                    else:
                        subfolder = None

                        if imageType in {
                            "enemyOld",
                            "enemyOldLevel4",
                            "enemyNew",
                            "move"
                        }:
                            subfolder = "enemies\\"
                        elif imageType in {
                            "enemyNode",
                            "attack",
                            "repeat",
                            "push",
                            "bleed",
                            "frostbite",
                            "poison",
                            "stagger",
                            "calamity",
                            "corrosion",
                            "terrain"
                        }:
                            subfolder = "icons\\"
                        elif imageType in {
                            "barrage",
                            "bitterCold",
                            "darkness",
                            "eerie",
                            "gangAlonne",
                            "gangHollow",
                            "gangSilverKnight",
                            "gangSkeleton",
                            "hidden",
                            "illusion",
                            "mimic",
                            "onslaught",
                            "poisonMist",
                            "snowstorm",
                            "timer",
                            "trial"
                        }:
                            subfolder = "encounters\\"
                        elif imageType in {
                            "emptySetIcon",
                            "tileLayout",
                            "tileLayout1Tile",
                            "nodesStartingHorizontal1Tile",
                            "nodesStartingVertical1Tile",
                            "tileLayoutLevel4",
                            "nodesStartingHorizontalLevel4",
                            "nodesStartingVerticalLevel4",
                            "levelIcon",
                            "reward",
                            "layout",
                            "nodesLevel4Vertical",
                            "nodesLevel4Horizontal",
                            "nodes1TileVertical",
                            "nodes1TileHorizontal",
                            "nodesHorizontal",
                            "nodesVertical",
                            "tileNum"
                        }:
                            subfolder = "custom_encounters\\"

                        if subfolder:
                            imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\" + subfolder.replace("\\", pathSep) + imageFileName
                        else:
                            imagePath = baseFolder + "\\lib\\dsbg_shuffle_images\\".replace("\\", pathSep) + imageFileName

                    log("\tOpening " + imagePath)

                    if imageType == "enemyOld":
                        image = Image.open(imagePath).resize((27, 27), Image.Resampling.LANCZOS)
                    elif imageType == "enemyOldLevel4":
                        if "Phantoms" in enemiesDict[imageFileName[:-4]].expansions:
                            image = Image.open(imagePath).resize((34, 34), Image.Resampling.LANCZOS)
                        else:
                            image = Image.open(imagePath).resize((32, 32), Image.Resampling.LANCZOS)
                    elif imageType == "enemyNew":
                        image = Image.open(imagePath).resize((22, 22), Image.Resampling.LANCZOS)
                    elif imageType == "enemyNode":
                        image = Image.open(imagePath).resize((12, 12), Image.Resampling.LANCZOS)
                    elif imageType == "attack":
                        image = Image.open(imagePath).resize((85, 91), Image.Resampling.LANCZOS)
                    elif imageType == "move":
                        image = Image.open(imagePath).resize((75, 75), Image.Resampling.LANCZOS)
                    elif imageType == "repeat":
                        image = Image.open(imagePath).resize((48, 48), Image.Resampling.LANCZOS)
                    elif imageType == "push":
                        image = Image.open(imagePath).resize((26, 32), Image.Resampling.LANCZOS)
                    elif imageType == "bleed":
                        image = Image.open(imagePath).resize((44, 50), Image.Resampling.LANCZOS)
                    elif imageType == "frostbite":
                        image = Image.open(imagePath).resize((55, 56), Image.Resampling.LANCZOS)
                    elif imageType == "poison":
                        image = Image.open(imagePath).resize((37, 50), Image.Resampling.LANCZOS)
                    elif imageType == "stagger":
                        image = Image.open(imagePath).resize((52, 56), Image.Resampling.LANCZOS)
                    elif imageType == "calamity":
                        image = Image.open(imagePath).resize((51, 50), Image.Resampling.LANCZOS)
                    elif imageType == "corrosion":
                        image = Image.open(imagePath).resize((49, 50), Image.Resampling.LANCZOS)
                    elif imageType == "barrage":
                        image = Image.open(imagePath).resize((41, 13), Image.Resampling.LANCZOS)
                    elif imageType == "bitterCold":
                        image = Image.open(imagePath).resize((56, 13), Image.Resampling.LANCZOS)
                    elif imageType == "darkness":
                        image = Image.open(imagePath).resize((48, 13), Image.Resampling.LANCZOS)
                    elif imageType == "eerie":
                        image = Image.open(imagePath).resize((27, 13), Image.Resampling.LANCZOS)
                    elif imageType == "gangAlonne":
                        image = Image.open(imagePath).resize((67, 13), Image.Resampling.LANCZOS)
                    elif imageType == "gangHollow":
                        image = Image.open(imagePath).resize((69, 13), Image.Resampling.LANCZOS)
                    elif imageType == "gangSilverKnight":
                        image = Image.open(imagePath).resize((96, 13), Image.Resampling.LANCZOS)
                    elif imageType == "gangSkeleton":
                        image = Image.open(imagePath).resize((73, 13), Image.Resampling.LANCZOS)
                    elif imageType == "hidden":
                        image = Image.open(imagePath).resize((38, 13), Image.Resampling.LANCZOS)
                    elif imageType == "illusion":
                        image = Image.open(imagePath).resize((36, 13), Image.Resampling.LANCZOS)
                    elif imageType == "mimic":
                        image = Image.open(imagePath).resize((33, 13), Image.Resampling.LANCZOS)
                    elif imageType == "onslaught":
                        image = Image.open(imagePath).resize((54, 13), Image.Resampling.LANCZOS)
                    elif imageType == "poisonMist":
                        image = Image.open(imagePath).resize((61, 13), Image.Resampling.LANCZOS)
                    elif imageType == "snowstorm":
                        image = Image.open(imagePath).resize((56, 13), Image.Resampling.LANCZOS)
                    elif imageType == "timer":
                        image = Image.open(imagePath).resize((31, 13), Image.Resampling.LANCZOS)
                    elif imageType == "trial":
                        image = Image.open(imagePath).resize((26, 13), Image.Resampling.LANCZOS)
                    elif imageType == "tileLayout":
                        image = Image.open(imagePath).resize((235, 329), Image.Resampling.LANCZOS)
                    elif imageType == "tileLayout1Tile":
                        image = Image.open(imagePath).resize((235, 329), Image.Resampling.LANCZOS)
                    elif imageType == "nodesStartingHorizontal1Tile":
                        image = Image.open(imagePath).resize((80, 11), Image.Resampling.LANCZOS)
                    elif imageType == "nodesStartingVertical1Tile":
                        image = Image.open(imagePath).resize((10, 83), Image.Resampling.LANCZOS)
                    elif imageType == "tileLayoutLevel4":
                        image = Image.open(imagePath).resize((235, 329), Image.Resampling.LANCZOS)
                    elif imageType == "nodesStartingHorizontalLevel4":
                        image = Image.open(imagePath).resize((80, 11), Image.Resampling.LANCZOS)
                    elif imageType == "nodesStartingVerticalLevel4":
                        image = Image.open(imagePath).resize((10, 83), Image.Resampling.LANCZOS)
                    elif imageType == "levelIcon":
                        image = Image.open(imagePath).resize((63, 63), Image.Resampling.LANCZOS)
                    elif imageType == "reward":
                        image = Image.open(imagePath).resize((112, 111), Image.Resampling.LANCZOS)
                    elif imageType == "layout":
                        image = Image.open(imagePath).resize((235, 329), Image.Resampling.LANCZOS)
                    elif imageType == "nodesLevel4Vertical":
                        image = Image.open(imagePath).resize((16, 182), Image.Resampling.LANCZOS)
                    elif imageType == "nodesLevel4Horizontal":
                        image = Image.open(imagePath).resize((182, 16), Image.Resampling.LANCZOS)
                    elif imageType == "nodes1TileVertical":
                        image = Image.open(imagePath).resize((20, 161), Image.Resampling.LANCZOS)
                    elif imageType == "nodes1TileHorizontal":
                        image = Image.open(imagePath).resize((159, 20), Image.Resampling.LANCZOS)
                    elif imageType == "nodesHorizontal":
                        image = Image.open(imagePath).resize((81, 9), Image.Resampling.LANCZOS)
                    elif imageType == "nodesVertical":
                        image = Image.open(imagePath).resize((9, 82), Image.Resampling.LANCZOS)
                    elif imageType == "tileNum":
                        image = Image.open(imagePath).resize((40, 60), Image.Resampling.LANCZOS)
                    elif imageType == "terrain":
                        image = Image.open(imagePath).resize((21, 24), Image.Resampling.LANCZOS)
                    elif imageType == "iconText":
                        i = Image.open(imagePath)
                        width, height = i.size
                        if width > height:
                            mod = 13 / width
                        else:
                            mod = 13 / height
                        img = Image.new("RGBA", (13, 13), (0, 0, 0, 0))
                        img.paste(im=Image.open(imagePath).resize((int(width * mod), int(height * mod)), Image.Resampling.LANCZOS))
                        log("\tEnd of create_image")
                        return img, ImageTk.PhotoImage(img)
                    elif imageType == "iconEnemy":
                        i = Image.open(imagePath)
                        width, height = i.size
                        if width > height:
                            mod = 22 / width
                        else:
                            mod = 22 / height
                        img = Image.new("RGBA", (22, 22), (0, 0, 0, 0))
                        img.paste(im=Image.open(imagePath).resize((int(width * mod), int(height * mod)), Image.Resampling.LANCZOS))
                        log("\tEnd of create_image")
                        return img, ImageTk.PhotoImage(img)
                    elif imageType == "iconSet":
                        x = 55 if not emptySetIcon else 58
                        y = 56 if not emptySetIcon else 59
                        i = Image.open(imagePath)
                        width, height = i.size
                        if width > height:
                            mod = x / width
                        else:
                            mod = y / height
                        img = Image.new("RGBA", (x, y), (0, 0, 0, 0))
                        img.paste(im=Image.open(imagePath).resize((int(width * mod), int(height * mod)), Image.Resampling.LANCZOS))
                        log("\tEnd of create_image")
                        return img, ImageTk.PhotoImage(img)

                log("\tEnd of create_image")

                return image
            except UnidentifiedImageError:
                p = PopupWindow(root, "Invalid image file chosen.", firstButton="Ok")
                root.wait_window(p)
                raise
            except EnvironmentError as err:
                if err.errno == errno.ENOENT: # ENOENT -> "no entity" -> "file not found"
                    if customEncounter:
                        p = PopupWindow(root, "Custom encounter file not found.\nWas it deleted?", firstButton="Ok")
                        root.wait_window(p)
                raise
            except Exception as e:
                error_popup(root, e)
                raise


        def create_tooltip(self, tooltipDict, x, y, right=False):
            """
            Create a label and tooltip that will be placed and later removed.
            """
            try:
                log("Start of create_tooltip, tooltipDict={}, x={}, y={}".format(str(tooltipDict), str(x), str(y)))

                if self.forPrinting:
                    convertedImage = tooltipDict["image"].convert("RGBA")
                    self.displayImage.paste(im=convertedImage, box=(x, y), mask=convertedImage)
                else:
                    x += 410 if right else 0
                    label = tk.Label(self.displayFrame, image=tooltipDict["photo image"], borderwidth=0, highlightthickness=0)
                    self.tooltips.append(label)
                    label.place(x=x, y=y)
                    CreateToolTip(label, tooltipText[tooltipDict["imageName"]])

                log("\tEnd of create_tooltip")
            except Exception as e:
                error_popup(root, e)
                raise


    root = tk.Tk()
    root.withdraw()
    root.attributes("-alpha", 0.0)
        
    root.title("DSBG-Shuffle")
    root.tk.call("source", baseFolder + "\\Azure-ttk-theme-main\\azure.tcl".replace("\\", pathSep))
    root.tk.call("set_theme", "dark")
    root.iconphoto(True, tk.PhotoImage(file=os.path.join(baseFolder, "bonfire.png")))

    # Check for a new version
    today = datetime.datetime.today()
    with open(baseFolder + "\\lib\\dsbg_shuffle_version.txt".replace("\\", pathSep)) as vFile:
        version = vFile.readlines()
    if int(version[1]) != today.month:
        version[1] = today.month
        with open(os.path.join(baseFolder, "lib\\dsbg_shuffle_version.txt".replace("\\", pathSep)), "w") as v:
            v.write("\n".join([str(line).replace("\n", "") for line in version]))

        response = requests.get("https://api.github.com/repos/DanDuhon/DSBG-Shuffle/releases/latest")
        if version[0].replace("\n", "") != response.json()["name"]:
            p = PopupWindow(root, "A new version of DSBG-Shuffle is available!\nCurrent:\t"
                            + version[0].replace("\n", "")
                            + "\nNew:\t"
                            + response.json()["name"]
                            + "\nCheck it out on Github!\n\nIf you don't want to see this notification anymore,\ndisable checking for updates in the settings.", firstButton="Ok", secondButton=True)
            root.wait_window(p)

    s = ttk.Style()

    app = Application(root)
    app.pack(fill="both", expand=True)

    root.option_add("*TCombobox*Listbox*Background", "#181818")
    root.option_add("*TCombobox*Listbox.selectForeground", "white")

    center(root)
    root.attributes("-alpha", 1.0)
    root.mainloop()
    log("Closing application")
    root.destroy()

except Exception as e:
    error = str(sys.exc_info())
    if "application has been destroyed" not in error:
        log(error, exception=True)
        raise
