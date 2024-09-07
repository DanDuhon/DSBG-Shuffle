try:
    import os
    import tkinter as tk
    from bisect import bisect_left
    from copy import deepcopy
    from fpdf import FPDF
    from json import dump, load
    from math import ceil
    from PIL import ImageDraw, ImageTk
    from random import choice
    from statistics import mean
    from tkinter import filedialog, ttk

    from dsbg_shuffle_enemies import bosses, enemiesDict
    from dsbg_shuffle_behaviors import behaviorDetail, behaviors
    from dsbg_shuffle_utility import PopupWindow, clear_other_tab_images, error_popup, log, set_display_bindings_by_tab, baseFolder, font, font2, font3, pathSep


    modIdLookup = {
        1: "dodge1",
        2: "dodge2",
        3: "damage1",
        4: "damage2",
        5: "damage3",
        6: "damage4",
        7: "armor1",
        8: "armor2",
        9: "resist1",
        10: "resist2",
        11: "health1",
        12: "health2",
        13: "health3",
        14: "health4",
        15: "repeat",
        16: "magic",
        17: "bleed",
        18: "frostbite",
        19: "poison",
        20: "stagger",
        21: "physical",
        22: "armor resist1",
        23: "damage health1",
        24: "damage health2"
        }
    
    dataCardMods = {m for m in modIdLookup if (
        "armor" in modIdLookup[m]
        or "resist" in modIdLookup[m]
        or "health" in modIdLookup[m])}


    def get_health_bonus(health, mods):
        modsSet = set([modIdLookup[m] if type(m) == int else m for m in mods])
        return (
            1 if health == 1 and {"health1", "damage health1"} & modsSet
            else 2 if health == 1 and {"health2", "damage health2"} & modsSet
            else 3 if health == 1 and {"health3", "damage health3"} & modsSet
            else 4 if health == 1 and {"health4", "damage health4"} & modsSet
            else 2 if health == 5 and {"health1", "damage health1"} & modsSet
            else 3 if health == 5 and {"health2", "damage health2"} & modsSet
            else 5 if health == 5 and {"health3", "damage health3"} & modsSet
            else 6 if health == 5 and {"health4", "damage health4"} & modsSet
            else 2 if health == 10 and {"health1", "damage health1"} & modsSet
            else 4 if health == 10 and {"health2", "damage health2"} & modsSet
            else 6 if health == 10 and {"health3", "damage health3"} & modsSet
            else 8 if health == 10 and {"health4", "damage health4"} & modsSet
            else ceil(health * 0.1) if {"health1", "damage health1"} & modsSet
            else ceil(health * 0.2) if {"health2", "damage health2"} & modsSet
            else ceil(health * 0.3) if {"health3", "damage health3"} & modsSet
            else ceil(health * 0.4) if {"health4", "damage health4"} & modsSet
            else 0)


    class VariantsFrame(ttk.Frame):
        def __init__(self, app, root):
            super(VariantsFrame, self).__init__()
            self.app = app
            self.root = root

            self.selectedVariant = None
            self.currentVariants = {}
            self.lockedVariants = {}

            self.app.progress.label.config(text = "Loading variants... ")

            # Load the enemy variants files.
            self.variants = {}
            i = self.app.progress.progressVar.get()
            for enemy in list(enemiesDict.keys()) + list(bosses.keys()):
                i += 3
                self.app.progress.progressVar.set(i)
                root.update_idletasks()
                
                with open(baseFolder + "\\lib\\dsbg_shuffle_difficulty\\dsbg_shuffle_difficulty_" + enemy + ".json", "r") as f:
                    enemyDifficulty = load(f)

                self.variants[enemy] = {1: {}, 2: {}, 3: {}, 4: {}}
                for x in range(1, 5):
                    for diffInc in enemyDifficulty[str(x)]:
                        self.variants[enemy][x][float(diffInc)] = {}
                        for defKey in enemyDifficulty[str(x)][diffInc]:
                            self.variants[enemy][x][float(diffInc)][frozenset([""] if not defKey else [int(k) for k in defKey.split(",")])] = enemyDifficulty[str(x)][diffInc][defKey]

                    self.variants[enemy][x] = {k: self.variants[enemy][x][k] for k in sorted(self.variants[enemy][x])}

            self.variantsTabButtonsFrame = ttk.Frame(self)
            self.variantsTabButtonsFrame.pack()
            self.variantsTabButtonsFrame2 = ttk.Frame(self)
            self.variantsTabButtonsFrame2.pack()
            self.variantsTabMenuFrame = ttk.Frame(self)
            self.variantsTabMenuFrame.pack()
            self.variantsTabMenuFrame2 = ttk.Frame(self)
            self.variantsTabMenuFrame2.pack()
            self.variantsTabMenuFrame3 = ttk.Frame(self)
            self.variantsTabMenuFrame3.pack()
            self.variantsListTreeviewFrame = ttk.Frame(self)
            self.variantsListTreeviewFrame.pack(fill="both", expand=True)
            self.variantsTabButtonsFrame3 = ttk.Frame(self)
            self.variantsTabButtonsFrame3.pack()
            self.variantsTabButtonsFrame4 = ttk.Frame(self)
            self.variantsTabButtonsFrame4.pack()
            self.variantsLockedTreeviewFrame = ttk.Frame(self)
            self.variantsLockedTreeviewFrame.pack(fill="both", expand=True)
            self.scrollbarTreeviewVariantsList = ttk.Scrollbar(self.variantsListTreeviewFrame)
            self.scrollbarTreeviewVariantsList.pack(side="right", fill="y")
            self.scrollbarTreeviewVariantsLocked = ttk.Scrollbar(self.variantsLockedTreeviewFrame)
            self.scrollbarTreeviewVariantsLocked.pack(side="right", fill="y")
            
            vcmd = (self.register(self.callback))

            self.diffLabel = ttk.Label(self.variantsTabButtonsFrame, text="Difficulty Modifier: +")
            self.diffLabel.pack(side=tk.LEFT, anchor=tk.CENTER, pady=5)
            self.entryText = tk.StringVar()
            self.diffEntry = ttk.Entry(self.variantsTabButtonsFrame, textvariable=self.entryText, width=7, validate="all", validatecommand=(vcmd, "%P"))
            self.diffEntry.pack(side=tk.LEFT, anchor=tk.CENTER, pady=5)
            self.diffLabel2 = ttk.Label(self.variantsTabButtonsFrame, text="%")
            self.diffLabel2.pack(side=tk.LEFT, anchor=tk.CENTER, pady=5)
            self.applyModButton = ttk.Button(self.variantsTabButtonsFrame, text="Apply Modifier", width=16, command=self.apply_difficulty_modifier)
            self.applyModButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.lockButton = ttk.Button(self.variantsTabButtonsFrame2, text="Lock Variant", width=16, command=self.lock_variant_card)
            self.lockButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.removeButton = ttk.Button(self.variantsTabButtonsFrame2, text="Remove Variant", width=16, command=self.remove_variant_card)
            self.removeButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

            self.healthMenuList = ["Heath Allowed", "Heath Required", "Heath Banned"]
            self.healthMenuVal = tk.StringVar(value=self.healthMenuList[0])
            self.healthMenu = ttk.Combobox(self.variantsTabMenuFrame, state="readonly", width=19, values=self.healthMenuList, textvariable=self.healthMenuVal)
            self.healthMenu.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.armorMenuList = ["Armor Allowed", "Armor Required", "Armor Banned"]
            self.armorMenuVal = tk.StringVar(value=self.armorMenuList[0])
            self.armorMenu = ttk.Combobox(self.variantsTabMenuFrame, state="readonly", width=19, values=self.armorMenuList, textvariable=self.armorMenuVal)
            self.armorMenu.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.resistMenuList = ["Resist Allowed", "Resist Required", "Resist Banned"]
            self.resistMenuVal = tk.StringVar(value=self.resistMenuList[0])
            self.resistMenu = ttk.Combobox(self.variantsTabMenuFrame, state="readonly", width=19, values=self.resistMenuList, textvariable=self.resistMenuVal)
            self.resistMenu.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.damageMenuList = ["Damage Allowed", "Damage Required", "Damage Banned"]
            self.damageMenuVal = tk.StringVar(value=self.damageMenuList[0])
            self.damageMenu = ttk.Combobox(self.variantsTabMenuFrame2, state="readonly", width=19, values=self.damageMenuList, textvariable=self.damageMenuVal)
            self.damageMenu.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.dodgeMenuList = ["Dodge Allowed", "Dodge Required", "Dodge Banned"]
            self.dodgeMenuVal = tk.StringVar(value=self.dodgeMenuList[0])
            self.dodgeMenu = ttk.Combobox(self.variantsTabMenuFrame2, state="readonly", width=19, values=self.dodgeMenuList, textvariable=self.dodgeMenuVal)
            self.dodgeMenu.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.repeatMenuList = ["Repeat Allowed", "Repeat Required", "Repeat Banned"]
            self.repeatMenuVal = tk.StringVar(value=self.repeatMenuList[0])
            self.repeatMenu = ttk.Combobox(self.variantsTabMenuFrame3, state="readonly", width=19, values=self.repeatMenuList, textvariable=self.repeatMenuVal)
            self.repeatMenu.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.conditionsMenuList = ["Conditions Allowed", "Conditions Required", "Conditions Banned"]
            self.conditionsMenuVal = tk.StringVar(value=self.conditionsMenuList[0])
            self.conditionsMenu = ttk.Combobox(self.variantsTabMenuFrame3, state="readonly", width=19, values=self.conditionsMenuList, textvariable=self.conditionsMenuVal)
            self.conditionsMenu.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

            self.variantMenus = {
                "health": {"button": self.healthMenu, "value": self.healthMenuVal, "mods": {m for m in modIdLookup if "health" in modIdLookup[m]}},
                "armor": {"button": self.armorMenu, "value": self.armorMenuVal, "mods": {m for m in modIdLookup if "armor" in modIdLookup[m]}},
                "resist": {"button": self.resistMenu, "value": self.resistMenuVal, "mods": {m for m in modIdLookup if "resist" in modIdLookup[m]}},
                "damage": {"button": self.damageMenu, "value": self.damageMenuVal, "mods": {m for m in modIdLookup if "damage" in modIdLookup[m]}},
                "dodge": {"button": self.dodgeMenu, "value": self.dodgeMenuVal, "mods": {m for m in modIdLookup if "dodge" in modIdLookup[m]}},
                "repeat": {"button": self.repeatMenu, "value": self.repeatMenuVal, "mods": {m for m in modIdLookup if "repeat" in modIdLookup[m]}},
                "conditions": {"button": self.conditionsMenu, "value": self.conditionsMenuVal, "mods": {m for m in modIdLookup if "bleed" in modIdLookup[m] or "frostbite" in modIdLookup[m] or "poison" in modIdLookup[m] or "stagger" in modIdLookup[m]}}
            }
            
            self.removeLockedButton = ttk.Button(self.variantsTabButtonsFrame3, text="Remove Variant(s)", width=16, command=self.delete_locked_variant)
            self.removeLockedButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.saveButton = ttk.Button(self.variantsTabButtonsFrame3, text="Save Variants", width=16, command=self.save_variants)
            self.saveButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.loadButton = ttk.Button(self.variantsTabButtonsFrame3, text="Load Variants", width=16, command=self.load_variants)
            self.loadButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.imagesPdfButton = ttk.Button(self.variantsTabButtonsFrame4, text="Images to PDF", width=16, command=self.print_variant_cards)
            self.imagesPdfButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

            self.create_variants_treeview()


        def reset_treeview(self):
            self.treeviewVariantsList.pack_forget()
            self.treeviewVariantsList.destroy()
            self.selectedVariant = None
            self.currentVariants = {}
            self.create_variants_treeview()
                

        def create_variants_treeview(self):
            """
            Create the behavior variants treeview, where a user can select an
            enemy or behavior and see variants based on a selected difficulty modifier.
            """
            try:
                log("Start of create_variants_treeview")

                self.treeviewVariantsList = ttk.Treeview(
                    self.variantsListTreeviewFrame,
                    selectmode="browse",
                    columns=("Name", "Current Modifier"),
                    yscrollcommand=self.scrollbarTreeviewVariantsList.set,
                    height=11 if self.root.winfo_screenheight() > 1000 else 5
                )

                self.treeviewVariantsList.pack(expand=True, fill="both")
                self.scrollbarTreeviewVariantsList.config(command=self.treeviewVariantsList.yview)

                self.treeviewVariantsList.column('#0', width=50)

                self.treeviewVariantsList.heading("Name", text="Name", anchor=tk.W)
                self.treeviewVariantsList.heading("Current Modifier", text="Current Modifier", anchor=tk.W)
                self.treeviewVariantsList.column("Name", anchor=tk.W, width=300)
                self.treeviewVariantsList.column("Current Modifier", anchor=tk.W, width=90)
                
                self.treeviewVariantsList.insert(parent="", index="end", iid="All", values=("All", 0), tags=False, open=True)
                self.treeviewVariantsList.insert(parent="All", index="end", iid="Enemies", values=("    Enemies", 0), tags=False)
                if {"Phantoms", "Explorers"} & self.app.availableExpansions:
                    self.treeviewVariantsList.insert(parent="All", index="end", iid="Invaders & Explorers Mimics", values=("    Invaders & Explorers Mimics", 0), tags=False)
                self.treeviewVariantsList.insert(parent="All", index="end", iid="Mini Bosses", values=("    Mini Bosses", 0), tags=False)
                self.treeviewVariantsList.insert(parent="All", index="end", iid="Main Bosses", values=("    Main Bosses", 0), tags=False)
                self.treeviewVariantsList.insert(parent="All", index="end", iid="Mega Bosses", values=("    Mega Bosses", 0), tags=False)

                for enemy in sorted([enemy for enemy in enemiesDict if enemiesDict[enemy].expansions & self.app.availableExpansions]):
                    self.treeviewVariantsList.insert(parent="Invaders & Explorers Mimics" if "Phantoms" in enemiesDict[enemy].expansions or enemiesDict[enemy].name in {"Hungry Mimic", "Voracious Mimic"} else "Enemies", index="end", iid=enemy, values=("        " + enemy, 0), tags=True)
                    
                for enemy in sorted([enemy for enemy in bosses if bosses[enemy]["expansions"] & self.app.availableExpansions]):
                    self.treeviewVariantsList.insert(parent=bosses[enemy]["level"] + "es", index="end", iid=enemy, values=("        " + enemy, 0), tags=True)

                for enemy in behaviors:
                    if "(" in enemy:
                        continue
                    if enemy in bosses and not bosses[enemy]["expansions"] & self.app.availableExpansions:
                        continue
                    if enemy in enemiesDict and not enemiesDict[enemy].expansions & self.app.availableExpansions:
                        continue
                    for behavior in behaviors[enemy]:
                        self.treeviewVariantsList.insert(parent=enemy, index="end", iid=enemy + " - " + behavior, values=("            " + behavior, 0), tags=True)

                self.treeviewVariantsList.selection_set("All")
                self.treeviewVariantsList.focus_set()
                self.treeviewVariantsList.focus("All")
                    
                self.treeviewVariantsList.bind("<<TreeviewSelect>>", self.load_variant_card)

                if not hasattr(self, "treeviewVariantsLocked"):
                    self.treeviewVariantsLocked = ttk.Treeview(
                        self.variantsLockedTreeviewFrame,
                        selectmode="browse",
                        columns=("Name", "Current Modifier"),
                        yscrollcommand=self.scrollbarTreeviewVariantsLocked.set,
                        height=11 if self.root.winfo_screenheight() > 1000 else 5
                    )

                    self.treeviewVariantsLocked.pack(expand=True, fill="both")
                    self.scrollbarTreeviewVariantsLocked.config(command=self.treeviewVariantsLocked.yview)

                    self.treeviewVariantsLocked.column('#0', width=50)

                    self.treeviewVariantsLocked.heading("Name", text="Name", anchor=tk.W)
                    self.treeviewVariantsLocked.heading("Current Modifier", text="Current Modifier", anchor=tk.W)
                    self.treeviewVariantsLocked.column("Name", anchor=tk.W, width=300)
                    self.treeviewVariantsLocked.column("Current Modifier", anchor=tk.W)
                    
                    self.treeviewVariantsLocked.insert(parent="", index="end", iid="All", values=("All", ""), tags=False, open=True)
                    self.treeviewVariantsLocked.insert(parent="All", index="end", iid="Enemies", values=("    Enemies", ""), tags=False)
                    if {"Phantoms", "Explorers"} & self.app.availableExpansions:
                        self.treeviewVariantsLocked.insert(parent="All", index="end", iid="Invaders & Explorers Mimics", values=("    Invaders & Explorers Mimics", ""), tags=False)
                    self.treeviewVariantsLocked.insert(parent="All", index="end", iid="Mini Bosses", values=("    Mini Bosses", ""), tags=False)
                    self.treeviewVariantsLocked.insert(parent="All", index="end", iid="Main Bosses", values=("    Main Bosses", ""), tags=False)
                    self.treeviewVariantsLocked.insert(parent="All", index="end", iid="Mega Bosses", values=("    Mega Bosses", ""), tags=False)
                    
                self.treeviewVariantsLocked.bind("<<TreeviewSelect>>", self.load_variant_card_locked)

                log("End of create_variants_treeview")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def load_variant_card(self, event=None, variant=None, fromLocked=False, bottomLeftDisplay=False, bottomRightDisplay=False, selfCall=None, forPrinting=False, armorerDennis=False, oldIronKing=False, pursuer=False, deckDataCard=False, healthMod=None, fromDeck=False):
            """
            Load a variant card that was selected (or passed in).
            """
            try:
                log("Start of load_variant_card, variant={}, selfCall={}, forPrinting={}, armorerDennis={}, oldIronKing={}, pursuer={}, deckDataCard={}, healthMod={}, fromDeck={}".format(str(variant), str(selfCall), str(forPrinting), str(armorerDennis), str(oldIronKing), str(pursuer), str(deckDataCard), str(healthMod), str(fromDeck)))

                self.treeviewVariantsList.unbind("<<TreeviewSelect>>")
                self.treeviewVariantsLocked.unbind("<<TreeviewSelect>>")

                if fromDeck:
                    variants = "behaviorDeck"
                elif fromLocked:
                    variants = "variantsLocked"
                else:
                    variants = "variants"

                # If this behavior was clicked on, get that information.
                if event:
                    tree = event.widget
                    
                    if not tree.selection():
                        log("\tNo variant selected")
                        log("\tEnd of load_variant_card")
                        self.treeviewVariantsList.bind("<<TreeviewSelect>>", self.load_variant_card)
                        self.treeviewVariantsLocked.bind("<<TreeviewSelect>>", self.load_variant_card_locked)
                        return
                    
                    if self.treeviewVariantsLocked.selection():
                        self.treeviewVariantsLocked.selection_remove(self.treeviewVariantsLocked.selection()[0])
                    
                    if not tree.item(tree.selection()[0])["tags"][0]:
                        log("\tNo variant selected")
                        log("\tEnd of load_variant_card")
                        self.treeviewVariantsList.bind("<<TreeviewSelect>>", self.load_variant_card)
                        self.treeviewVariantsLocked.bind("<<TreeviewSelect>>", self.load_variant_card_locked)
                        return

                    self.selectedVariant = tree.selection()[0]
                    
                    if tree.parent(self.selectedVariant) in {
                        "Enemies",
                        "Invaders & Explorers Mimics",
                        "Mini Bosses",
                        "Main Bosses",
                        "Mega Bosses"
                        }:
                        self.selectedVariant += " - data"
                        
                        self.app.displayTopLeft.config(image="")
                        self.app.displayTopLeft.image=None
                        self.app.displayImages["variantsLocked"][self.app.displayTopLeft]["image"] = None
                        self.app.displayImages["variantsLocked"][self.app.displayTopLeft]["name"] = None
                        self.app.displayImages["variantsLocked"][self.app.displayTopLeft]["activeTab"] = None
                else:
                    self.selectedVariant = variant

                if self.selectedVariant[-1] == "_":
                    self.selectedVariant = self.selectedVariant.replace("_", "")

                clear_other_tab_images(
                    self.app,
                    variants,
                    variants,
                    name=self.selectedVariant[:self.selectedVariant.index(" - ")] if " - " in self.selectedVariant else self.selectedVariant[:self.selectedVariant.index("_")] if "_" in self.selectedVariant else self.selectedVariant)
                    
                if "Smough" not in self.selectedVariant and "Gaping Dragon" not in self.selectedVariant and "Vordt" not in self.selectedVariant and self.app.displayImages["variants"][self.app.displayBottomRight]["image"]:
                    self.app.displayBottomRight.config(image="")
                    self.app.displayBottomRight.image=None
                    self.app.displayImages["variantsLocked"][self.app.displayBottomRight]["image"] = None
                    self.app.displayImages["variantsLocked"][self.app.displayBottomRight]["name"] = None
                    self.app.displayImages["variantsLocked"][self.app.displayBottomRight]["activeTab"] = None
                    
                if not selfCall:
                    originalSelection = deepcopy(self.selectedVariant)

                # Remove keyword tooltips from the previous image shown, if there are any.
                for tooltip in self.app.tooltips:
                    tooltip.destroy()

                if ("Ornstein" in self.selectedVariant or "Smough" in self.selectedVariant) and (self.selectedVariant.count("&") == 2 or "data" in self.selectedVariant):
                    if "data" not in self.selectedVariant:
                        # Create and display the variant image.
                        self.variantPhotoImage = self.app.create_image(self.selectedVariant + ".jpg", "enemyCard")

                        self.edit_variant_card_os(fromDeck=fromDeck)
                    else:
                        for enemy in ["Ornstein", "Smough"]:
                            # Create and display the variant image.
                            self.variantPhotoImage = self.app.create_image(enemy + " - data.jpg", "enemyCard")

                            self.edit_variant_card_os(enemy=enemy, healthMod=healthMod if healthMod else {"Ornstein": 0, "Smough": 0}, fromDeck=fromDeck)
                else:
                    self.selectedVariant += " - data" if "-" not in self.selectedVariant else ""
                    
                    # Create and display the variant image.
                    self.variantPhotoImage = self.app.create_image((self.selectedVariant[:self.selectedVariant.index("_")] + self.selectedVariant.replace(variant, "") if "_" in self.selectedVariant else self.selectedVariant) + ".jpg", "enemyCard")

                    self.edit_variant_card(variant=self.selectedVariant, bottomLeftDisplay=bottomLeftDisplay, bottomRightDisplay=bottomRightDisplay, lockedTree=fromLocked, armorerDennis=armorerDennis, oldIronKing=oldIronKing, pursuer=pursuer, healthMod=healthMod, fromDeck=fromDeck)

                if "data" not in self.selectedVariant and self.app.displayImages[variants][self.app.displayTopRight]["name"] != self.selectedVariant and "The Four Kings" not in self.selectedVariant and not forPrinting:
                    self.load_variant_card(variant=self.selectedVariant[:self.selectedVariant.index(" - ")] + " - data", fromLocked=fromLocked, selfCall=originalSelection, armorerDennis=armorerDennis, oldIronKing=oldIronKing, pursuer=pursuer, deckDataCard=deckDataCard, healthMod=healthMod, fromDeck=fromDeck)

                if not selfCall:
                    self.selectedVariant = originalSelection

                set_display_bindings_by_tab(self.app, ("Ornstein" in self.selectedVariant or "Smough" in self.selectedVariant) and (self.selectedVariant.count("&") == 2 or "data" in self.selectedVariant))

                self.treeviewVariantsList.bind("<<TreeviewSelect>>", self.load_variant_card)
                self.treeviewVariantsLocked.bind("<<TreeviewSelect>>", self.load_variant_card_locked)

                log("End of load_variant_card")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def load_variant_card_locked(self, event=None, variant=None, selfCall=None, bottomLeftDisplay=False, bottomRightDisplay=False, forPrinting=False, armorerDennis=False, oldIronKing=False, pursuer=False, deckDataCard=False, healthMod=None, fromDeck=False):
            try:
                log("Start of load_variant_card_locked, variant={}, selfCall={}, forPrinting={}, armorerDennis={}, oldIronKing={}, pursuer={}, deckDataCard={}, healthMod={}, fromDeck={}".format(str(variant), str(selfCall), str(forPrinting), str(armorerDennis), str(oldIronKing), str(pursuer), str(deckDataCard), str(healthMod), str(fromDeck)))
                    
                self.treeviewVariantsList.unbind("<<TreeviewSelect>>")
                self.treeviewVariantsLocked.unbind("<<TreeviewSelect>>")

                # If this behavior was clicked on, get that information.
                if event:
                    tree = event.widget

                    if not tree.selection():
                        log("\tNo variant selected")
                        log("\tEnd of load_variant_card_locked")
                        self.treeviewVariantsList.bind("<<TreeviewSelect>>", self.load_variant_card)
                        self.treeviewVariantsLocked.bind("<<TreeviewSelect>>", self.load_variant_card_locked)
                        return
                    
                    if self.treeviewVariantsList.selection():
                        self.treeviewVariantsList.selection_remove(self.treeviewVariantsList.selection()[0])

                    if not tree.item(tree.selection()[0])["tags"][0]:
                        log("\tNo variant selected")
                        log("\tEnd of load_variant_card")
                        self.treeviewVariantsList.bind("<<TreeviewSelect>>", self.load_variant_card)
                        self.treeviewVariantsLocked.bind("<<TreeviewSelect>>", self.load_variant_card_locked)
                        return

                    name = tree.selection()[0][:tree.selection()[0].index("_")]

                    # Account for Ornstein & Smough behaviors.
                    if type(self.lockedVariants[tree.selection()[0]]["mods"][0]) == list:
                        mods = [
                            [modIdLookup[m] for m in list(self.lockedVariants[tree.selection()[0]]["mods"][0]) if m],
                            [modIdLookup[m] for m in list(self.lockedVariants[tree.selection()[0]]["mods"][1]) if m]
                            ]
                    else:
                        mods = [modIdLookup[m] for m in list(self.lockedVariants[tree.selection()[0]]["mods"]) if m]

                    self.selectedVariant = (
                        name
                        + (" - data" if tree.parent(tree.selection()[0]) in {
                            "Enemies",
                            "Invaders & Explorers Mimics",
                            "Mini Bosses",
                            "Main Bosses",
                            "Mega Bosses"
                            } else ""))
                elif variant in self.lockedVariants:
                    name = variant[:variant.index("_")]

                    # Account for Ornstein & Smough behaviors.
                    if type(self.lockedVariants[variant]["mods"][0]) == list:
                        mods = [
                            [modIdLookup[m] for m in list(self.lockedVariants[variant]["mods"][0]) if m],
                            [modIdLookup[m] for m in list(self.lockedVariants[variant]["mods"][1]) if m]
                            ]
                    else:
                        mods = [modIdLookup[m] for m in list(self.lockedVariants[variant]["mods"]) if m]

                    self.selectedVariant = (
                        name
                        + (" - data" if self.treeviewVariantsLocked.parent(variant) in {
                            "Enemies",
                            "Invaders & Explorers Mimics",
                            "Mini Bosses",
                            "Main Bosses",
                            "Mega Bosses"
                            } else ""))
                elif (
                    (variant[:variant.index(" - ")] if " - " in variant else variant) in set([v[:v.index("_")] for v in self.lockedVariants])
                    or (("Ornstein" in variant or "Smough" in variant) and "Ornstein & Smough" in set([v[:v.index("_")] for v in self.lockedVariants]))
                    ):
                    if "Ornstein" in variant and "&" not in variant:
                        var = variant.replace("Ornstein", "Ornstein & Smough")
                        selection = [v for v in self.lockedVariants if (var[:var.index("_")] if "_" in var else var[:var.index(" - ")] + "_") in v][0]
                    elif "Smough" in variant and "&" not in variant:
                        var = variant.replace("Smough", "Ornstein & Smough")
                        selection = [v for v in self.lockedVariants if (var[:var.index("_")] if "_" in var else var[:var.index(" - ")] + "_") in v][0]
                    else:
                        selection = [v for v in self.lockedVariants if (variant[:variant.index("_")] if "_" in variant else variant[:variant.index(" - ")]) + "_" in v][0]

                    # Account for Ornstein & Smough behaviors.
                    if type(self.lockedVariants[selection]["mods"][0]) == list:
                        mods = [
                            [modIdLookup[m] for m in list(self.lockedVariants[selection]["mods"][0]) if m],
                            [modIdLookup[m] for m in list(self.lockedVariants[selection]["mods"][1]) if m]
                            ]
                    else:
                        mods = [modIdLookup[m] for m in list(self.lockedVariants[selection]["mods"]) if m]

                    if "_" in variant:
                        name = variant[:variant.index("_")]
                    elif "-" in variant:
                        name = variant[:variant.index(" - ")]
                    else:
                        name = variant

                    self.selectedVariant = (
                        name
                        + (" - data" if self.treeviewVariantsLocked.parent(selection) in {
                            "Enemies",
                            "Invaders & Explorers Mimics",
                            "Mini Bosses",
                            "Main Bosses",
                            "Mega Bosses"
                            } else ""))
                elif variant not in self.lockedVariants:
                    self.load_variant_card(variant=variant, fromLocked=True, armorerDennis=armorerDennis, oldIronKing=oldIronKing, pursuer=pursuer, deckDataCard=deckDataCard, healthMod=healthMod, fromDeck=fromDeck, selfCall=selfCall, bottomLeftDisplay=bottomLeftDisplay, bottomRightDisplay=bottomRightDisplay)
                    log("End of load_variant_card_locked")
                    return
                else:
                    name = variant[:variant.index("_")]

                    # Account for Ornstein & Smough behaviors.
                    if "Ornstein" in variant or "Smough" in variant:
                        mods = [
                            [modIdLookup[m] for m in list(self.lockedVariants[variant][0]) if m],
                            [modIdLookup[m] for m in list(self.lockedVariants[variant][1]) if m]
                            ]
                    else:
                        mods = [modIdLookup[m] for m in list(self.lockedVariants[variant]) if m]

                    self.selectedVariant = (
                        name
                        + (" - data" if self.treeviewVariantsLocked.parent(variant) in {
                            "Enemies",
                            "Invaders & Explorers Mimics",
                            "Mini Bosses",
                            "Main Bosses",
                            "Mega Bosses"
                            } else ""))

                if fromDeck:
                    variants = "behaviorDeck"
                else:
                    variants = "variantsLocked"

                clear_other_tab_images(
                    self.app,
                    variants,
                    variants,
                    name=self.selectedVariant[:self.selectedVariant.index(" - ")] if " - " in self.selectedVariant else self.selectedVariant[:self.selectedVariant.index("_")] if "_" in self.selectedVariant else self.selectedVariant)
                    
                if not selfCall and "data" in self.selectedVariant and self.app.displayTopLeft.image == self.app.displayImages["variants"][self.app.displayTopLeft]["image"]:
                    self.app.displayTopLeft.config(image="")
                    self.app.displayTopLeft.image=None
                    self.app.displayImages["variants"][self.app.displayTopLeft]["image"] = None
                    self.app.displayImages["variants"][self.app.displayTopLeft]["name"] = None
                    self.app.displayImages["variants"][self.app.displayTopLeft]["activeTab"] = None
                    
                if "Ornstein & Smough" not in self.selectedVariant and "Gaping Dragon" not in self.selectedVariant and self.app.displayBottomRight.image == self.app.displayImages["variants"][self.app.displayBottomRight]["image"]:
                    self.app.displayBottomRight.config(image="")
                    self.app.displayBottomRight.image=None
                    self.app.displayImages["variants"][self.app.displayBottomRight]["image"] = None
                    self.app.displayImages["variants"][self.app.displayBottomRight]["name"] = None
                    self.app.displayImages["variants"][self.app.displayBottomRight]["activeTab"] = None
                    
                if not selfCall:
                    originalSelection = deepcopy(self.selectedVariant)

                # Remove keyword tooltips from the previous image shown, if there are any.
                for tooltip in self.app.tooltips:
                    tooltip.destroy()

                if ("Ornstein" in self.selectedVariant or "Smough" in self.selectedVariant) and (self.selectedVariant.count("&") == 2 or "data" in self.selectedVariant):
                    if "data" not in self.selectedVariant:
                        # Create and display the variant image.
                        self.variantPhotoImage = self.app.create_image(self.selectedVariant + ".jpg", "enemyCard")

                        self.edit_variant_card_os(variant=mods, lockedTree=True, fromDeck=fromDeck)
                    else:
                        for enemy in ["Ornstein", "Smough"]:
                            # Create and display the variant image.
                            self.variantPhotoImage = self.app.create_image(enemy + " - data.jpg", "enemyCard")

                            self.edit_variant_card_os(variant=mods, lockedTree=True, enemy=enemy, healthMod=healthMod if healthMod else {"Ornstein": 0, "Smough": 0}, fromDeck=fromDeck)
                else:
                    # Create and display the variant image.
                    self.variantPhotoImage = self.app.create_image(self.selectedVariant + ".jpg", "enemyCard")

                    self.edit_variant_card(variant=mods, lockedTree=True, armorerDennis=armorerDennis, oldIronKing=oldIronKing, pursuer=pursuer, healthMod=healthMod, fromDeck=fromDeck, bottomLeftDisplay=bottomLeftDisplay, bottomRightDisplay=bottomRightDisplay)

                if "data" not in self.selectedVariant and self.app.displayImages["variantsLocked"][self.app.displayTopRight]["name"] != self.selectedVariant and "The Four Kings" not in self.selectedVariant and not forPrinting:
                    modString = ",".join([str(x) for x in sorted([n for n in modIdLookup if modIdLookup[n] in set(mods[0] if mods and type(mods[0]) == list else mods) & set([modIdLookup[m] for m in dataCardMods])])])
                    self.load_variant_card_locked(variant=self.selectedVariant[:self.selectedVariant.index(" - ")] + "_" + modString, selfCall=True, armorerDennis=armorerDennis, oldIronKing=oldIronKing, pursuer=pursuer, deckDataCard=deckDataCard, healthMod=healthMod, fromDeck=fromDeck)

                if not selfCall:
                    self.selectedVariant = originalSelection

                set_display_bindings_by_tab(self.app, ("Ornstein" in self.selectedVariant or "Smough" in self.selectedVariant) and (self.selectedVariant.count("&") == 2 or "data" in self.selectedVariant))
                    
                self.treeviewVariantsList.bind("<<TreeviewSelect>>", self.load_variant_card)
                self.treeviewVariantsLocked.bind("<<TreeviewSelect>>", self.load_variant_card_locked)

                log("End of load_variant_card_locked")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def apply_difficulty_modifier(self, event=None):
            """
            Find the appropriate variants for the entered difficulty.
            """
            try:
                log("Start of apply_difficulty_modifier")

                if self.app.notebook.tab(self.app.notebook.select(), "text") != "Behavior Variants":
                    log("End of apply_difficulty_modifier (wrong tab)")
                    return

                tree = self.treeviewVariantsList
                if not tree.selection():
                    log("End of apply_difficulty_modifier (nothing selected)")
                    return
                
                if not self.entryText.get():
                    log("End of apply_difficulty_modifier (no mod entered)")
                    return

                clear_other_tab_images(
                    self.app,
                    "variants",
                    "variants",
                    name=None if not self.selectedVariant else self.selectedVariant[:self.selectedVariant.index(" - ")] if " - " in self.selectedVariant else self.selectedVariant[:self.selectedVariant.index("_")] if "_" in self.selectedVariant else self.selectedVariant)

                set_display_bindings_by_tab(self.app, self.selectedVariant and ("Ornstein" in self.selectedVariant or "Smough" in self.selectedVariant) and (self.selectedVariant.count("&") == 2 or "data" in self.selectedVariant))

                if event:
                    if tree.selection()[0] in {"All", "Enemies", "Invaders & Explorers Mimics", "Mini Bosses", "Main Bosses", "Mega Bosses"}:
                        log("End of apply_difficulty_modifier (event click with category selected)")
                        
                    if event.widget == self.app.displayTopRight and not tree.get_children(tree.selection()[0]) and tree.parent(tree.selection()[0]) != "Enemies":
                        self.selectedVariant = tree.parent(tree.selection()[0]) + " - data"

                    variantName = None
                    if " - data" in self.selectedVariant:
                        variantName = self.selectedVariant[:self.selectedVariant.index(" - data")]
                    tree.selection_set(variantName if variantName else self.selectedVariant)
                    tree.focus_set()
                    tree.focus(variantName if variantName else self.selectedVariant)

                diffKey = 1.0 + (float(self.entryText.get()) / 100)
                diffKey = ceil((diffKey * 10)) / 10
                start = tree.focus()
                
                progress = None

                # Selected enemy name - generate variants for all enemy behaviors.
                if tree.item(start)["tags"] and start in self.variants:
                    self.pick_enemy_variants_enemy(start, diffKey, progress=progress)
                    self.app.behaviorDeckTab.set_decks(enemy=start, skipClear=True)
                # Generate different variant for selected behavior.
                elif " - " in start:
                    startReal = start[:start.index(" - ")]
                    diffKeyIndex = bisect_left(list(self.variants[startReal][self.app.numberOfCharacters].keys()), diffKey)
                    diffKeyIndex -= 1 if diffKeyIndex > len(list(self.variants[startReal][self.app.numberOfCharacters].keys())) - 1 else 0
                    diffKeyReal = list(self.variants[startReal][self.app.numberOfCharacters].keys())[diffKeyIndex]

                    if "defKey" not in self.currentVariants.get(startReal, {}):
                        defKey = choice(list(self.variants[startReal][self.app.numberOfCharacters][diffKeyReal].keys()))
                        self.currentVariants[startReal] = {"defKey": list(defKey)}
                    else:
                        defKey = self.currentVariants[startReal]["defKey"]

                    modsRequired = [
                        self.variantMenus[s]["mods"] for s in self.variantMenus if (
                            "Required" in self.variantMenus[s]["value"].get())]
                    
                    modsBanned = [
                        self.variantMenus[s]["mods"] for s in self.variantMenus if (
                            "Banned" in self.variantMenus[s]["value"].get())]
                    
                    if modsRequired or modsBanned:
                        # This effectively rebuilds self.variants but limited to variants that
                        # have the required variants.  Also had to ensure no empty lists or keys.
                        variants = {
                            k: self.get_variant_difficulty_dict(startReal, k, modsRequired, modsBanned)
                                for k in self.variants[startReal][self.app.numberOfCharacters] if (
                                    self.get_variant_difficulty_dict(startReal, k, modsRequired, modsBanned))
                            }
                    else:
                        variants = self.variants[startReal][self.app.numberOfCharacters]
                    
                    self.pick_enemy_variants_behavior(startReal, start[start.index(" - ")+3:], diffKeyReal, defKey, variants)
                    self.app.behaviorDeckTab.set_decks(enemy=self.treeviewVariantsList.parent(start), skipClear=True)
                elif start in {"Enemies", "Invaders & Explorers Mimics", "Mini Bosses", "Main Bosses", "Mega Bosses"}:
                    if start == "Enemies":
                        progress = PopupWindow(self.root, labelText="Generating variants...", progressBar=True, progressMax=len(tree.get_children("Enemies")), loadingImage=True)
                    else:
                        progressMax = 0
                        for child in tree.get_children(start):
                            progressMax += len(tree.get_children(child))

                        progress = PopupWindow(self.root, labelText="Generating variants...", progressBar=True, progressMax=progressMax, loadingImage=True)

                    i = 0

                    for child in tree.get_children(start):
                        if start == "Enemies":
                            i += 1
                        else:
                            i += len(tree.get_children(child))
                        progress.progressVar.set(i)
                        self.root.update_idletasks()
                        self.pick_enemy_variants_enemy(child, diffKey, progress=progress)
                        self.app.behaviorDeckTab.set_decks(enemy=child, skipClear=True)
                        clear_other_tab_images(
                            self.app,
                            "variants",
                            "variants",
                            onlyDisplay=self.app.displayTopLeft,
                            name=child[:child.index(" - ")] if " - " in child else child[:child.index("_")] if "_" in child else child)
                elif start == "All":
                    progressMax = 0
                    for child in tree.get_children("All"):
                        for subChild in tree.get_children(child):
                            progressMax += len(tree.get_children(subChild))

                    progress = PopupWindow(self.root, labelText="Generating variants...", progressBar=True, progressMax=progressMax + len(set(self.currentVariants.keys()) & set(tree.get_children("Enemies"))), loadingImage=True)

                    i = 0

                    for child in tree.get_children(start):
                        for subChild in tree.get_children(child):
                            i += len(tree.get_children(subChild))
                            progress.progressVar.set(i)
                            self.root.update_idletasks()
                            self.pick_enemy_variants_enemy(subChild, diffKey, progress=progress)
                            self.app.behaviorDeckTab.set_decks(enemy=subChild, skipClear=True)
                            
                    clear_other_tab_images(
                        self.app,
                        "variants",
                        "variants",
                        onlyDisplay=self.app.displayTopLeft)

                if progress:
                    progress.label.config(text = "Calculating difficulty averages...")
                    progress.progressBar.grid_forget()
                    self.root.update_idletasks()
                # Recalculate the average difficulty mod for this row and its parents and children.
                for child in tree.get_children(start):
                    for subChild in tree.get_children(child):
                        for subSubChild in tree.get_children(subChild):
                            self.recalc_variant_average(tree, subSubChild)
                        self.recalc_variant_average(tree, subChild)
                    self.recalc_variant_average(tree, child)

                if tree.parent(start):
                    self.recalc_variant_average(tree, start)
                    if tree.parent(tree.parent(start)):
                        self.recalc_variant_average(tree, tree.parent(start))
                        if tree.parent(tree.parent(tree.parent(start))):
                            self.recalc_variant_average(tree, tree.parent(tree.parent(start)))

                if self.selectedVariant:
                    self.load_variant_card(variant=self.selectedVariant)

                if progress:
                    progress.destroy()

                log("End of apply_difficulty_modifier")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def recalc_variant_average(self, tree, start):
            """
            Calculate and display the rolled up average for a treeview parent row.
            """
            try:
                log("Start of recalc_variant_average, tree={}, start={}".format(str(tree), str(start)))

                parent = tree.parent(start)
                diffAvg = []
                for child in tree.get_children(tree.parent(start)):
                    if tree.item(child)["values"][1]:
                        diffAvg.append(int(tree.item(child)["values"][1]))
                    else:
                        diffAvg.append(0)

                if not diffAvg:
                    return
                    
                tree.item(parent, values=(tree.item(parent)["values"][0], int(round(mean(diffAvg)))))

                log("End of recalc_variant_average")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def get_variant_difficulty_dict(self, start, k, modsRequired, modsBanned):
            return {
                d: self.get_variant_behavior_dict(start, k, d, modsRequired, modsBanned)
                for d in self.variants[start][self.app.numberOfCharacters][k] if (
                    self.get_variant_behavior_dict(start, k, d, modsRequired, modsBanned))
                }


        def get_variant_behavior_dict(self, start, k, d, modsRequired, modsBanned):
            r = {
                e: self.get_variant_list_key(start, k, d, e, modsRequired, modsBanned)
                for e in self.variants[start][self.app.numberOfCharacters][k][d] if (
                    self.get_variant_list_key(start, k, d, e, modsRequired, modsBanned))
                }
            return r if set(r.keys()) == set(self.variants[start][self.app.numberOfCharacters][k][d].keys()) else {}


        def get_variant_list_key(self, start, k, d, e, modsRequired, modsBanned):
            return [f for f in self.variants[start][self.app.numberOfCharacters][k][d][e] if (
                (all(set(f) & r for r in modsRequired) or not modsRequired)
                and (all(not set(f) & r for r in modsBanned) or not modsBanned))]


        def pick_enemy_variants_enemy(self, start, diffKey, progress):
            """
            Find the appropriate variants for the entered difficulty.
            """
            try:
                log("Start of pick_enemy_variants_enemy, start={}, diffKey={}".format(str(start), str(diffKey)))

                modsRequired = [
                    self.variantMenus[s]["mods"] for s in self.variantMenus if (
                        "Required" in self.variantMenus[s]["value"].get())]
                
                modsBanned = [
                    self.variantMenus[s]["mods"] for s in self.variantMenus if (
                        "Banned" in self.variantMenus[s]["value"].get())]
                
                if modsRequired or modsBanned:
                    # This effectively rebuilds self.variants but limited to variants that
                    # have the required variants.  Also had to ensure no empty lists or keys.
                    if not progress:
                        progress2 = PopupWindow(self.root, labelText="Generating variant...", loadingImage=True)

                    variants = {
                        k: self.get_variant_difficulty_dict(start, k, modsRequired, modsBanned)
                            for k in self.variants[start][self.app.numberOfCharacters] if (
                                self.get_variant_difficulty_dict(start, k, modsRequired, modsBanned))
                        }
                    
                    if not progress:
                        progress2.destroy()
                else:
                    variants = self.variants[start][self.app.numberOfCharacters]

                if not variants:
                    log("End of pick_enemy_variants_enemy")
                    return

                diffKeyIndex = bisect_left(list(variants.keys()), diffKey)
                diffKeyIndex -= 1 if diffKeyIndex > len(list(variants.keys())) - 1 else 0
                diffKeyReal = list(variants.keys())[diffKeyIndex]
                defKey = choice(list(variants[diffKeyReal].keys()))
                self.currentVariants[start] = {"defKey": list(defKey)}

                for behavior in variants[diffKeyReal][defKey]:
                    self.pick_enemy_variants_behavior(start, behavior, diffKeyReal, defKey, variants)
                
                log("End of pick_enemy_variants_enemy")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def pick_enemy_variants_behavior(self, start, behavior, diffKey, defKey, variants):
            """
            Find the appropriate variants for the entered difficulty.
            """
            try:
                log("Start of pick_enemy_variants_behavior (start={}, behavior={}, diffKey={}, defKey={})".format(start, behavior, str(diffKey), str(defKey)))

                if behavior in {"Back Dash", "Forward Dash"}:
                    log("End of pick_enemy_variants_behavior (nothing done)")
                    return
                
                if start == "Ornstein & Smough":
                    behavior = [k for k in behaviors[start] if behavior in k][0]

                curVariant = self.currentVariants[start].get(behavior, 1)

                if start == "Ornstein & Smough" and "&" in behavior:
                    behaviorO = behavior[:behavior.index(" & ")]
                    behaviorS = behavior[behavior.index(" & ")+3:]

                    if frozenset(defKey) not in variants[diffKey]:
                        p = PopupWindow(self.root, "The difficulty modifier you chose is incompatible with the\ndifficulty modifiers on other behaviors.\n\nPlease try a different difficulty modifier or change the difficulty\nmodifier at the {} level.".format(start, start), firstButton="Ok")
                        self.root.wait_window(p)
                        return

                    self.currentVariants[start][behavior] = {
                        behaviorO: choice(list(variants[diffKey][frozenset(defKey)][behaviorO])),
                        behaviorS: choice(list(variants[diffKey][frozenset(defKey)][behaviorS]))
                    }
                else:
                    if frozenset(defKey) not in variants[diffKey]:
                        p = PopupWindow(self.root, "The difficulty modifier you chose is incompatible with the\ndifficulty modifiers on other behaviors.\n\nPlease try a different difficulty modifier or change the difficulty\nmodifier at the {} level.".format(start, start), firstButton="Ok")
                        self.root.wait_window(p)
                        return

                    while (
                        len(self.currentVariants[start].get(behavior, [])) == 0
                        or (
                            behavior in self.currentVariants[start]
                            and len(variants[diffKey][frozenset(defKey)][behavior]) > 1
                            and curVariant == self.currentVariants[start][behavior]
                            )
                        ):
                        self.currentVariants[start][behavior] = choice(variants[diffKey][frozenset(defKey)][behavior])
                    
                self.treeviewVariantsList.item(start + (" - " + behavior if behavior else ""), values=(self.treeviewVariantsList.item(start + (" - " + behavior if behavior else ""))["values"][0], int(round((diffKey - 1.0) * 100, -1))))
                
                log("End of pick_enemy_variants_behavior")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def edit_variant_card(self, variant=None, lockedTree=False, event=None, bottomLeftDisplay=False, bottomRightDisplay=False, armorerDennis=False, oldIronKing=False, pursuer=False, deckDataCard=False, healthMod=0, fromDeck=False):
            try:
                log("Start of edit_variant_card, variant={}".format(str(variant)))

                enemy = self.selectedVariant[:self.selectedVariant.index(" - ")] if " - " in self.selectedVariant else None
                enemy = enemy[:enemy.index("_")] if "_" in enemy else enemy
                behavior = self.selectedVariant[self.selectedVariant.index(" - ")+3:] if " - " in self.selectedVariant else None

                if behavior == "data":
                    self.edit_variant_card_data(enemy, variant=variant, healthMod=healthMod)
                
                if behavior != "data" or "behavior" in behaviorDetail[enemy]:
                    self.edit_variant_card_behavior(variant=variant, armorerDennis=armorerDennis, oldIronKing=oldIronKing, pursuer=pursuer)

                displayPhotoImage = ImageTk.PhotoImage(self.app.displayImage)

                if fromDeck:
                    key = "behaviorDeck"
                elif lockedTree:
                    key = "variantsLocked"
                else:
                    key = "variants"

                if bottomRightDisplay:
                    self.app.displayBottomRight.image = displayPhotoImage
                    self.app.displayBottomRight.config(image=displayPhotoImage)
                    self.app.displayImages[key][self.app.displayBottomRight]["image"] = displayPhotoImage
                    self.app.displayImages[key][self.app.displayBottomRight]["name"] = self.selectedVariant
                    self.app.displayImages[key][self.app.displayBottomRight]["activeTab"] = key if not fromDeck else "behaviorDeck"
                elif bottomLeftDisplay:
                    self.app.displayBottomLeft.image = displayPhotoImage
                    self.app.displayBottomLeft.config(image=displayPhotoImage)
                    self.app.displayImages[key][self.app.displayBottomLeft]["image"] = displayPhotoImage
                    self.app.displayImages[key][self.app.displayBottomLeft]["name"] = self.selectedVariant
                    self.app.displayImages[key][self.app.displayBottomLeft]["activeTab"] = key if not fromDeck else "behaviorDeck"
                elif deckDataCard:
                    self.app.displayTopRight.image = displayPhotoImage
                    self.app.displayTopRight.config(image=displayPhotoImage)
                    self.app.displayImages[key][self.app.displayTopRight]["image"] = displayPhotoImage
                    self.app.displayImages[key][self.app.displayTopRight]["name"] = self.selectedVariant
                    self.app.displayImages[key][self.app.displayTopRight]["activeTab"] = key if not fromDeck else "behaviorDeck"
                else:
                    if behavior == "data":
                        self.app.displayTopRight.image = displayPhotoImage
                        self.app.displayTopRight.config(image=displayPhotoImage)
                        self.app.displayImages[key][self.app.displayTopRight]["image"] = displayPhotoImage
                        self.app.displayImages[key][self.app.displayTopRight]["name"] = self.selectedVariant
                        self.app.displayImages[key][self.app.displayTopRight]["activeTab"] = key if not fromDeck else "behaviorDeck"
                    else:
                        self.app.displayTopLeft.image = displayPhotoImage
                        self.app.displayTopLeft.config(image=displayPhotoImage)
                        self.app.displayImages[key][self.app.displayTopLeft]["image"] = displayPhotoImage
                        self.app.displayImages[key][self.app.displayTopLeft]["name"] = self.selectedVariant
                        self.app.displayImages[key][self.app.displayTopLeft]["activeTab"] = key if not fromDeck else "behaviorDeck"

                log("End of edit_variant_card")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def lock_variant_card(self, event=None):
            try:
                log("Start of lock_variant_card")
                
                progress = None

                tree = self.treeviewVariantsList
                treeLocked = self.treeviewVariantsLocked
                iidForAvg = tree.focus()

                if not tree.selection():
                    log("End of lock_variant_card (nothing done)")
                    return
                
                v = tree.item(tree.selection()[0])["values"]

                if not v[1]:
                    log("End of lock_variant_card (nothing done)")
                    return
                
                if tree.focus() == "Enemies":
                    progress = PopupWindow(self.root, labelText="Locking variants...", progressBar=True, progressMax=len(tree.get_children("Enemies")), loadingImage=True)

                    for i, child in enumerate(tree.get_children(tree.focus())):
                        progress.progressVar.set(i)
                        self.root.update_idletasks()
                        if child not in self.currentVariants:
                            continue
                        v = tree.item(child)["values"]
                        modList = sorted([v for v in self.currentVariants[child][[k for k in list(self.currentVariants[child].keys()) if k != "defKey"][0]]])
                        iidChild = child + "_" + ",".join([str(m) for m in sorted(modList)])

                        if iidChild in self.lockedVariants:
                            continue
                        
                        self.lockedVariants[iidChild] = {
                            "mods": modList,
                            "defKey": set(modList) & dataCardMods
                            }
                        contents = [treeLocked.item(child)["values"][0] for child in treeLocked.get_children("Enemies")]
                        treeLocked.insert(parent="Enemies", index=bisect_left(contents, v[0]), iid=iidChild, values=(v[0], v[1]), tags=True)

                        self.app.behaviorDeckTab.set_decks(enemy=child, skipClear=True)
                elif tree.focus() in {"Invaders & Explorers Mimics", "Mini Bosses", "Main Bosses", "Mega Bosses"}:
                    progressMax = 0
                    for child in tree.get_children(tree.focus()):
                        progressMax += len([c for c in tree.get_children(child) if c != "defKey"])

                    progress = PopupWindow(self.root, labelText="Locking variants...", progressBar=True, progressMax=progressMax, loadingImage=True)
                    
                    i = 0
                    for e in tree.get_children(tree.focus()):
                        if e not in self.currentVariants:
                            continue
                        v = tree.item(e)["values"]
                        modList = sorted(list(self.currentVariants[e]["defKey"]))
                        iid = e + "_" + ",".join([str(m) for m in sorted(modList)])
                        iidForAvg = iid

                        if iid in self.lockedVariants:
                            log("End of lock_variant_card (nothing done)")
                            continue
                        
                        self.lockedVariants[iid] = {
                            "mods": modList,
                            "defKey": set(modList) & dataCardMods
                            }
                        contents = [treeLocked.item(child)["values"][0] for child in treeLocked.get_children(tree.parent(e))]
                        treeLocked.insert(parent=tree.parent(e), index=bisect_left(contents, v[0]), iid=iid, values=(v[0], v[1]), tags=True)
                        
                        for child in tree.get_children(e):
                            i += 1
                            progress.progressVar.set(i)
                            self.root.update_idletasks()

                            if " - " in child:
                                enemy = child[:child.index(" - ")]
                                behavior = child[child.index(" - ")+3:]

                            if behavior in {"Back Dash", "Forward Dash"}:
                                continue
                                
                            v = tree.item(child)["values"]
                        
                            if enemy == "Ornstein & Smough" and "&" in behavior:
                                modList1 = sorted([v for v in self.currentVariants[enemy][behavior][behavior[:behavior.index(" & ")]]])
                                modList2 = sorted([v for v in self.currentVariants[enemy][behavior][behavior[behavior.index(" & ")+3:]]])
                                iidChild = child + "_" + ",".join([str(m) for m in sorted(modList1)]) + "_" + ",".join([str(m) for m in sorted(modList2)])
                            else:
                                modList = sorted([v for v in self.currentVariants[enemy][behavior]])
                                iidChild = child + "_" + ",".join([str(m) for m in sorted(modList)])

                            if iidChild in self.lockedVariants:
                                continue
                            
                            if enemy == "Ornstein & Smough" and "&" in behavior:
                                self.lockedVariants[iidChild] = {
                                    "mods": [modList1, modList2],
                                    "defKey": set(modList) & dataCardMods
                                    }
                            else:
                                self.lockedVariants[iidChild] = {
                                    "mods": modList,
                                    "defKey": set(modList) & dataCardMods
                                    }

                            contents = [treeLocked.item(child)["values"][0] for child in treeLocked.get_children(iid)]
                            treeLocked.insert(parent=iid, index=bisect_left(contents, v[0]), iid=iidChild, values=(v[0], v[1]), tags=True)

                        self.app.behaviorDeckTab.set_decks(enemy=e, skipClear=True)
                elif tree.focus() == "All":
                    progressMax = 0
                    for child in tree.get_children("All"):
                        for subChild in tree.get_children(child):
                            progressMax += len(tree.get_children(subChild))

                    progress = PopupWindow(self.root, labelText="Locking variants...", progressBar=True, progressMax=len(list(self.currentVariants.keys())), loadingImage=True)

                    i = 0
                    iidForAvg = "All"
                    for cat in tree.get_children("All"):
                        for e in tree.get_children(cat):
                            v = tree.item(e)["values"]
                            if cat == "Enemies":
                                modList = sorted([v for v in self.currentVariants[e][[k for k in list(self.currentVariants[e].keys()) if k != "defKey"][0]]])
                                i += 1
                                progress.progressVar.set(i)
                                self.root.update_idletasks()
                            elif e in self.currentVariants:
                                modList = sorted(list(self.currentVariants[e]["defKey"]))
                            else:
                                continue
                            iid = e + "_" + ",".join([str(m) for m in sorted(modList)])

                            if iid in self.lockedVariants:
                                log("End of lock_variant_card (nothing done)")
                                continue
                            
                            self.lockedVariants[iid] = {
                                "mods": modList,
                                "defKey": set(modList) & dataCardMods
                                }
                            contents = [treeLocked.item(child)["values"][0] for child in treeLocked.get_children(cat)]
                            treeLocked.insert(parent=cat, index=bisect_left(contents, v[0]), iid=iid, values=(v[0], v[1]), tags=True)
                            
                            for child in tree.get_children(e):
                                i += 1
                                progress.progressVar.set(i)
                                self.root.update_idletasks()

                                if " - " in child:
                                    enemy = child[:child.index(" - ")]
                                    behavior = child[child.index(" - ")+3:]

                                if behavior in {"Back Dash", "Forward Dash"}:
                                    continue
                                    
                                v = tree.item(child)["values"]
                        
                                if enemy == "Ornstein & Smough" and "&" in behavior:
                                    modList1 = sorted([v for v in self.currentVariants[enemy][behavior][behavior[:behavior.index(" & ")]]])
                                    modList2 = sorted([v for v in self.currentVariants[enemy][behavior][behavior[behavior.index(" & ")+3:]]])
                                    iidChild = child + "_" + ",".join([str(m) for m in sorted(modList1)]) + "_" + ",".join([str(m) for m in sorted(modList2)])
                                else:
                                    modList = sorted([v for v in self.currentVariants[enemy][behavior]])
                                    iidChild = child + "_" + ",".join([str(m) for m in sorted(modList)])

                                if iidChild in self.lockedVariants:
                                    continue
                                
                                if enemy == "Ornstein & Smough" and "&" in behavior:
                                    self.lockedVariants[iidChild] = {
                                        "mods": [modList1, modList2],
                                        "defKey": set(modList) & dataCardMods
                                        }
                                else:
                                    self.lockedVariants[iidChild] = {
                                        "mods": modList,
                                        "defKey": set(modList) & dataCardMods
                                        }

                                contents = [treeLocked.item(child)["values"][0] for child in treeLocked.get_children(iid)]
                                treeLocked.insert(parent=iid, index=bisect_left(contents, v[0]), iid=iidChild, values=(v[0], v[1]), tags=True)
                                
                            if e in self.app.behaviorDeckTab.decks:
                                self.app.behaviorDeckTab.set_decks(enemy=e, skipClear=True)
                elif tree.get_children(tree.focus()) or " - " in tree.focus():
                    if " - " in tree.focus():
                        focus = tree.parent(tree.focus())
                        v = tree.item(focus)["values"]
                    else:
                        focus = tree.focus()

                    modList = sorted(list(self.currentVariants[focus]["defKey"]))
                    iid = focus + "_" + ",".join([str(m) for m in sorted(modList)])
                    iidForAvg = iid

                    if iid not in self.lockedVariants:
                        self.lockedVariants[iid] = {
                            "mods": modList,
                            "defKey": set(modList) & dataCardMods
                            }
                        contents = [treeLocked.item(child)["values"][0] for child in treeLocked.get_children(tree.parent(tree.focus()))] if treeLocked.exists(tree.parent(tree.focus())) else []
                        treeLocked.insert(parent=tree.parent(focus), index=bisect_left(contents, v[0]), iid=iid, values=(v[0], v[1]), tags=True)
                    
                    for child in tree.get_children(focus):
                        if " - " in child:
                            enemy = child[:child.index(" - ")]
                            behavior = child[child.index(" - ")+3:]

                        if behavior in {"Back Dash", "Forward Dash"}:
                            continue
                            
                        v = tree.item(child)["values"]
                        
                        if enemy == "Ornstein & Smough" and "&" in behavior:
                            modList1 = sorted([v for v in self.currentVariants[enemy][behavior][behavior[:behavior.index(" & ")]]])
                            modList2 = sorted([v for v in self.currentVariants[enemy][behavior][behavior[behavior.index(" & ")+3:]]])
                            iidChild = child + "_" + ",".join([str(m) for m in sorted(modList1)]) + "_" + ",".join([str(m) for m in sorted(modList2)])
                        elif behavior not in self.currentVariants[enemy]:
                            continue
                        else:
                            modList = sorted([v for v in self.currentVariants[enemy][behavior]])
                            iidChild = child + "_" + ",".join([str(m) for m in sorted(modList)])

                        if iidChild in self.lockedVariants:
                            continue
                            
                        if enemy == "Ornstein & Smough" and "&" in behavior:
                            self.lockedVariants[iidChild] = {
                                "mods": [modList1, modList2],
                                "defKey": set(modList) & dataCardMods
                                }
                        else:
                            self.lockedVariants[iidChild] = {
                                "mods": modList,
                                "defKey": set(modList) & dataCardMods
                                }
                            
                        contents = treeLocked.get_children(iid)
                        treeLocked.insert(parent=iid, index=bisect_left(contents, iidChild), iid=iidChild, values=(v[0], v[1]), tags=True)
                        
                    if "Vordt" in focus:
                        self.app.behaviorDeckTab.set_decks(enemy="Vordt of the Boreal Valley (move)", skipClear=True)
                        self.app.behaviorDeckTab.set_decks(enemy="Vordt of the Boreal Valley (attack)", skipClear=True)
                    else:
                        self.app.behaviorDeckTab.set_decks(enemy=focus, skipClear=True)
                else:
                    modList = sorted([v for v in self.currentVariants[tree.focus()][[k for k in list(self.currentVariants[tree.focus()].keys()) if k != "defKey"][0]]])
                    iid = tree.focus() + "_" + ",".join([str(m) for m in sorted(modList)])
                    iidForAvg = iid

                    if iid in self.lockedVariants:
                        log("End of lock_variant_card (nothing done)")
                        return
                    
                    self.lockedVariants[iid] = {
                        "mods": modList,
                        "defKey": set(modList) & dataCardMods
                        }
                    contents = [treeLocked.item(child)["values"][0] for child in treeLocked.get_children(tree.parent(tree.focus()))]
                    treeLocked.insert(parent=tree.parent(tree.focus()), index=bisect_left(contents, v[0]), iid=iid, values=(v[0], v[1]), tags=True)
                    
                    self.app.behaviorDeckTab.set_decks(enemy=tree.focus(), skipClear=True)

                if progress:
                    progress.label.config(text = "Calculating difficulty averages...")
                    progress.progressBar.grid_forget()
                    self.root.update_idletasks()
                # Recalculate the average difficulty mod for this row and its parents and children.
                for child in treeLocked.get_children(iidForAvg):
                    for subChild in treeLocked.get_children(child):
                        for subSubChild in treeLocked.get_children(subChild):
                            self.recalc_variant_average(treeLocked, subSubChild)
                        self.recalc_variant_average(treeLocked, subChild)
                    self.recalc_variant_average(treeLocked, child)

                if treeLocked.parent(iidForAvg):
                    self.recalc_variant_average(treeLocked, iidForAvg)
                    if treeLocked.parent(treeLocked.parent(iidForAvg)):
                        self.recalc_variant_average(treeLocked, treeLocked.parent(iidForAvg))
                        if treeLocked.parent(treeLocked.parent(treeLocked.parent(iidForAvg))):
                            self.recalc_variant_average(treeLocked, treeLocked.parent(treeLocked.parent(iidForAvg)))
                            
                if progress:
                    progress.destroy()

                log("End of lock_variant_card")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def remove_variant_card(self, variant=None):
            try:
                log("Start of remove_variant_card, variant={}".format(str(variant)))
                
                tree = self.treeviewVariantsList

                for display in [self.app.displayTopLeft, self.app.displayBottomLeft, self.app.displayTopRight, self.app.displayBottomRight]:
                    display.config(image="")
                    display.image=None
                    self.app.displayImages["variants"][display]["image"] = None
                    self.app.displayImages["variants"][display]["name"] = None
                    self.app.displayImages["variants"][display]["activeTab"] = None
                
                if variant:
                    target = variant
                # If the button is clicked with no selection, do nothing.
                elif not tree.selection():
                    log("End of remove_variant_card (nothing done)")
                    return
                else:
                    target = tree.selection()[0]
                
                # Remove the deleted variants from the treeview.
                if target == "All":
                    self.currentVariants = {}
                    tree.item(target, values=(tree.item(target)["values"][0], 0))
                    for child in tree.get_children(target):
                        tree.item(child, values=(tree.item(child)["values"][0], 0))
                        for subChild in tree.get_children(child):
                            tree.item(subChild, values=(tree.item(subChild)["values"][0], 0))
                            for subSubChild in tree.get_children(subChild):
                                tree.item(subSubChild, values=(tree.item(subSubChild)["values"][0], 0))

                            if subChild == "Vordt of the Boreal Valley":
                                self.app.behaviorDeckTab.set_decks(enemy="Vordt of the Boreal Valley (move)", skipClear=True)
                                self.app.behaviorDeckTab.set_decks(enemy="Vordt of the Boreal Valley (attack)", skipClear=True)
                            elif subChild in self.app.behaviorDeckTab.decks:
                                self.app.behaviorDeckTab.set_decks(enemy=subChild, skipClear=True)
                else:
                    for child in tree.get_children(target):
                        parent = tree.parent(child)

                        if " - " in child:
                            childReal = child[child.index(" - ")+3:]
                        else:
                            childReal = child

                        for subChild in tree.get_children(child):
                            if " - " in subChild:
                                subChildReal = subChild[subChild.index(" - ")+3:]
                            else:
                                subChildReal = subChild

                            if childReal in self.currentVariants and subChildReal in self.currentVariants[childReal]:
                                del self.currentVariants[childReal][subChildReal]
                                tree.item(subChild, values=(tree.item(subChild)["values"][0], 0))

                        if childReal in self.currentVariants:
                            del self.currentVariants[childReal]
                            tree.item(child, values=(tree.item(child)["values"][0], 0))

                        if parent in self.currentVariants and childReal in self.currentVariants[parent]:
                            del self.currentVariants[parent][childReal]
                            tree.item(child, values=(tree.item(child)["values"][0], 0))

                    if " - " in target:
                        parent = target[:target.index(" - ")]
                        child = target[target.index(" - ")+3:]
                        if child in self.currentVariants[parent]:
                            del self.currentVariants[parent][child]
                            tree.item(target, values=(tree.item(target)["values"][0], 0))
                    else:
                        if target in self.currentVariants:
                            del self.currentVariants[target]
                            tree.item(target, values=(tree.item(target)["values"][0], 0))

                    if target in self.app.behaviorDeckTab.decks:
                        self.app.behaviorDeckTab.set_decks(enemy=target, skipClear=True)
                    elif tree.parent(target) in self.app.behaviorDeckTab.decks:
                        self.app.behaviorDeckTab.set_decks(enemy=tree.parent(target), skipClear=True)

                progress = PopupWindow(self.root, labelText="Calculating difficulty averages...", loadingImage=True)
                # Recalculate the average difficulty mod for this row and its parents and children.
                for child in tree.get_children(target):
                    for subChild in tree.get_children(child):
                        for subSubChild in tree.get_children(subChild):
                            self.recalc_variant_average(tree, subSubChild)
                        self.recalc_variant_average(tree, subChild)
                    self.recalc_variant_average(tree, child)

                if tree.parent(target):
                    self.recalc_variant_average(tree, target)
                    if tree.parent(tree.parent(target)):
                        self.recalc_variant_average(tree, tree.parent(target))
                        if tree.parent(tree.parent(tree.parent(target))):
                            self.recalc_variant_average(tree, tree.parent(tree.parent(target)))

                # Remove the image displaying a deleted item.
                clear_other_tab_images(
                    self.app,
                    "variants",
                    "variants")

                progress.destroy()

                log("End of remove_variant_card")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def delete_locked_variant(self, variant=None):
            """
            Delete a variant from the locked list.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of delete_locked_variant, variant={}".format(str(variant)))
                
                tree = self.treeviewVariantsLocked
                
                if variant:
                    target = variant
                # If the button is clicked with no selection, do nothing.
                elif not tree.selection():
                    log("End of delete_locked_variant (nothing done)")
                    return
                else:
                    target = tree.selection()[0]
                
                parent = tree.parent(target)
                
                # Remove the deleted variants from the treeview.
                for child in tree.get_children(target):
                    for subChild in tree.get_children(child):
                        for subSubChild in tree.get_children(subChild):
                            if subSubChild in self.lockedVariants:
                                del self.lockedVariants[subSubChild]
                                
                            if subSubChild not in {"All", "Enemies", "Invaders & Explorers Mimics", "Mini Bosses", "Main Bosses", "Mega Bosses"}:
                                tree.delete(subSubChild)

                        if subChild in self.lockedVariants:
                            del self.lockedVariants[subChild]
                            
                        if subChild not in {"All", "Enemies", "Invaders & Explorers Mimics", "Mini Bosses", "Main Bosses", "Mega Bosses"}:
                            tree.delete(subChild)

                        if "_" in subChild and subChild[:subChild.index("_")] in self.app.behaviorDeckTab.decks:
                            self.app.behaviorDeckTab.set_decks(enemy=subChild[:subChild.index("_")], skipClear=True)

                    if child in self.lockedVariants:
                        del self.lockedVariants[child]
                        
                    if child not in {"All", "Enemies", "Invaders & Explorers Mimics", "Mini Bosses", "Main Bosses", "Mega Bosses"}:
                        tree.delete(child)

                    if "_" in child and child[:child.index("_")] in self.app.behaviorDeckTab.decks:
                        self.app.behaviorDeckTab.set_decks(enemy=child[:child.index("_")], skipClear=True)

                if target in self.lockedVariants:
                    del self.lockedVariants[target]
                    
                if target not in {"All", "Enemies", "Invaders & Explorers Mimics", "Mini Bosses", "Main Bosses", "Mega Bosses"}:
                    tree.delete(target)

                if "_" in target and target[:target.index("_")] in self.app.behaviorDeckTab.decks:
                    self.app.behaviorDeckTab.set_decks(enemy=target[:target.index("_")], skipClear=True)

                progress = PopupWindow(self.root, labelText="Calculating difficulty averages...", loadingImage=True)
                # Recalculate the average difficulty mod for this row and its parents and children.
                for child in tree.get_children("All"):
                    if not tree.get_children(child):
                        tree.item(child, values=(tree.item(child)["values"][0], ""))
                        continue
                    self.recalc_variant_average(tree, child)
                    for subChild in tree.get_children(child):
                        self.recalc_variant_average(tree, subChild)
                        for subSubChild in tree.get_children(subChild):
                            self.recalc_variant_average(tree, subSubChild)

                if not any([tree.item(child)["values"][1] for child in tree.get_children("All")]):
                    tree.item("All", values=("All", ""))
                elif parent:
                    self.recalc_variant_average(tree, parent)
                    if tree.parent(tree.parent(parent)):
                        self.recalc_variant_average(tree, tree.parent(parent))

                # Remove the image displaying a deleted item.
                clear_other_tab_images(
                    self.app,
                    "variants",
                    "variants")

                progress.destroy()

                log("End of delete_locked_variant")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def edit_variant_card_data(self, enemy, variant=None, event=None, healthMod=0):
            try:
                log("Start of edit_variant_card_data, variant={}".format(str(variant)))

                imageWithText = ImageDraw.Draw(self.app.displayImage)

                healthAddition = 0
                health = behaviorDetail[enemy]["health"]
                armor = behaviorDetail[enemy]["armor"]
                resist = behaviorDetail[enemy]["resist"]
                heatup = []
                if "heatup1" in behaviorDetail[enemy]:
                    heatup.append(behaviorDetail[enemy]["heatup1"])
                    heatup.append(behaviorDetail[enemy]["heatup2"])
                elif "heatup" in behaviorDetail[enemy]:
                    heatup.append(behaviorDetail[enemy]["heatup"])

                if type(variant) != list and enemy in self.currentVariants:
                    mods = [modIdLookup[m] for m in list(self.currentVariants[enemy]["defKey"]) if m]
                    healthAddition = get_health_bonus(health, mods)
                    health += healthAddition
                    heatup = [h + healthAddition for h in heatup]
                    for mod in mods:
                        armor += int(mod[-1]) if "armor" in mod else 0
                        resist += int(mod[-1]) if "resist" in mod else 0
                elif type(variant) == list:
                    healthAddition = get_health_bonus(health, variant)
                    health += healthAddition
                    heatup = [h + healthAddition for h in heatup]
                    for mod in variant:
                        armor += int(mod[-1]) if "armor" in mod else 0
                        resist += int(mod[-1]) if "resist" in mod else 0

                if enemy == "Maldron the Assassin":
                    imageWithText.text((132 + (4 if health < 10 else 0), 340), str(health), "black", font)
                elif enemy == "Paladin Leeroy":
                    imageWithText.text((184, 340), str(2 + healthAddition), "black", font)

                if healthMod and health + healthMod >= 0:
                    health += healthMod

                imageWithText.text((251 + (
                    7 if health == 1 else
                    4 if health == 0 else
                    1 if 49 < health < 60 else
                    5 if 1 < health < 10 else
                    3 if health < 20 else 0), 35), str(health), "white", font2)
                imageWithText.text((130, 245 - (10 if "behavior" in behaviorDetail[enemy] else 0)), str(armor), "white", font3)
                imageWithText.text((154, 245 - (10 if "behavior" in behaviorDetail[enemy] else 0)), str(resist), "black", font3)

                if heatup:
                    if enemy == "Vordt of the Boreal Valley":
                        imageWithText.text((189, 245), str(heatup[0]), "black", font2)
                        imageWithText.text((242, 245), str(heatup[1]), "black", font2)
                    else:
                        imageWithText.text((243 + (4 if heatup[0] < 10 else 0), 245), str(heatup[0]), "black", font2)

                log("End of edit_variant_card_data")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def edit_variant_card_behavior(self, variant=None, event=None, armorerDennis=False, oldIronKing=False, pursuer=False):
            try:
                log("Start of edit_variant_card_behavior, variant={}".format(str(variant)))

                enemy = self.selectedVariant[:self.selectedVariant.index(" - ")] if " - " in self.selectedVariant else None
                enemy = enemy[:enemy.index("_")] if "_" in enemy else enemy
                if "behavior" in behaviorDetail[enemy]:
                    behavior = "behavior"
                else:
                    behavior = self.selectedVariant[self.selectedVariant.index(" - ")+3:] if " - " in self.selectedVariant else None

                if "_" in behavior:
                    behavior = behavior[:behavior.index("_")]

                dodge = behaviorDetail[enemy][behavior]["dodge"] + (1 if armorerDennis else 0) + (1 if oldIronKing and "Fire Beam" in behavior else 0)
                repeat = behaviorDetail[enemy][behavior].get("repeat", 1)
                actions = {}
                for position in ["left", "middle", "right"]:
                    if position in behaviorDetail[enemy][behavior]:
                        if "effect" in behaviorDetail[enemy][behavior][position]:
                            actions[position] = {"effect": []}
                            actions[position]["effect"] = [e for e in behaviorDetail[enemy][behavior][position]["effect"]]
                        else:
                            actions[position] = behaviorDetail[enemy][behavior][position].copy()
                            if (
                                pursuer
                                or (
                                    "Fire Beam" in behavior
                                    and "damage" in actions[position]
                                    and oldIronKing
                                    )
                                ):
                                actions[position]["damage"] += 1

                if variant:
                    dodge, repeat, actions = self.apply_mods_to_actions(enemy, behavior, dodge, repeat, actions, variant)
                elif enemy in self.currentVariants and ("" if behavior == "behavior" else behavior) in self.currentVariants[enemy]:
                    dodge, repeat, actions = self.apply_mods_to_actions(enemy, behavior, dodge, repeat, actions)

                self.add_components_to_variant_card_behavior(enemy, behavior, dodge, repeat, actions)

                log("End of edit_variant_card_behavior")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def add_components_to_variant_card_behavior(self, enemy, behavior, dodge, repeat, actions, event=None):
            try:
                log("Start of add_components_to_variant_card_behavior, enemy={}, behavior={}, dodge={}, repeat={}, actions={}".format(str(enemy), str(behavior), str(dodge), str(repeat), str(actions)))

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                imageWithText.text((267, 233), str(dodge), "black", font2)

                if repeat > 1 and behavior != "behavior":
                    image = self.app.repeat[repeat]
                    self.app.displayImage.paste(im=image, box=(126, 225), mask=image)
                                    
                for position in ["left", "middle", "right"]:
                    if position not in actions or not actions[position]:
                        continue
                    if "type" in actions[position] and (actions[position]["type"] == "physical" or actions[position]["type"] == "magic") and "Cage Grasp Inferno" not in behavior:
                        x = 12 if position == "left" else 107 if position == "middle" else 202
                        image = self.app.attack[actions[position]["type"]][actions[position]["damage"]]
                        log("Pasting " + actions[position]["type"] + " attack image onto variant at " + str((x, 280)) + ".")
                        self.app.displayImage.paste(im=image, box=(x, 280), mask=image)
                    elif "Cage Grasp Inferno" in behavior:
                        if "type" in actions[position]:
                            image = self.app.attack[actions[position]["type"]][actions[position]["damage"]]
                            log("Pasting " + actions[position]["type"] + " attack image onto variant at " + str((-13, 343)) + ".")
                            self.app.displayImage.paste(im=image, box=(-13, 343), mask=image)
                        elif "effect" in actions[position]:
                            for i, effect in enumerate(actions[position]["effect"]):
                                if effect == "bleed":
                                    image = self.app.bleed
                                elif effect == "frostbite":
                                    image = self.app.frostbite
                                elif effect == "poison":
                                    image = self.app.poison
                                elif effect == "stagger":
                                    image = self.app.stagger
                                else:
                                    continue

                                self.app.displayImage.paste(im=image, box=(80 + (i * 50), 363), mask=image)
                    elif "type" in actions[position] and actions[position]["type"] == "push":
                        x = 15 if position == "left" else 110 if position == "middle" else 206
                        image = self.app.attack[actions[position]["type"]][actions[position]["damage"]]
                        log("Pasting " + actions[position]["type"] + " attack image onto variant at " + str((x, 283)) + ".")
                        self.app.displayImage.paste(im=image, box=(x, 283), mask=image)
                    elif "repeat" in actions[position]:
                        x = 127 if position == "middle" else 238
                        image = self.app.repeat[actions[position]["repeat"]]
                        log("Pasting repeat image onto variant at " + str((x, 300)) + ".")
                        self.app.displayImage.paste(im=image, box=(x, 300), mask=image)
                    elif "effect" in actions[position]:
                        for i, effect in enumerate(actions[position]["effect"]):
                            xOffset = 0
                            if effect == "bleed":
                                image = self.app.bleed
                            elif effect == "frostbite":
                                image = self.app.frostbite
                                xOffset = -9
                            elif effect == "poison":
                                image = self.app.poison
                            elif effect == "stagger":
                                image = self.app.stagger
                                xOffset = -5
                            elif effect == "corrosion":
                                image = self.app.corrosion
                                xOffset = -4
                            elif effect == "calamity":
                                image = self.app.calamity
                                xOffset = -6
                            else:
                                continue

                            x = (130 if position == "middle" else 240) + xOffset
                            self.app.displayImage.paste(im=image, box=(x, 280 + (i * 50)), mask=image)
                
                if enemy in {"Phalanx", "Phalanx Hollow", "Silver Knight Spearman"}:
                    x = 115 if "repeat" in actions["right"] else 209
                    image = self.app.sksMove if enemy == "Silver Knight Spearman" else self.app.phalanxMove
                    log("Pasting move image onto variant at " + str((x, 285)) + ".")
                    self.app.displayImage.paste(im=image, box=(x, 285), mask=image)

                log("End of add_components_to_variant_card_behavior")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def apply_mods_to_actions(self, enemy, behavior, dodge, repeat, actions, variant=None, event=None):
            try:
                log("Start of apply_mods_to_actions, enemy={}, behavior={}, dodge={}, repeat={}, actions={}, variant={}".format(str(enemy), str(behavior), str(dodge), str(repeat), str(actions), str(variant)))

                behavior = "" if behavior == "behavior" else behavior

                if type(variant) == list:
                    mods = variant
                elif enemy in self.currentVariants and behavior in self.currentVariants[enemy]:
                    mods = sorted([modIdLookup[m] for m in list(self.currentVariants[enemy][behavior])], key=lambda x: 1 if x == "repeat" else 0)
                else:
                    log("End of apply_mods_to_actions (nothing to do)")
                    return dodge, repeat, actions

                for mod in mods:
                    dodge += int(mod[-1]) if "dodge" in mod else 0
                    repeat += 1 if "repeat" in mod else 0
                    newConditionAdded = False

                    # For behaviors that do not already cause a condition.
                    if (
                        mod in {"bleed", "frostbite", "poison", "stagger"}
                        and "effect" not in actions.get("middle", {})
                        and "effect" not in actions.get("right", {})
                        ):
                        for position in ["middle", "right"]:
                            if position in actions and not actions[position]:
                                actions[position]["effect"] = [mod]
                                newConditionAdded = True
                                break

                    if newConditionAdded:
                        continue

                    repeatAdded = False if behavior == "" else True
                    if any(["repeat" in actions[position] for position in actions]):
                        repeatAdded = True

                    for position in ["left", "middle", "right"]:
                        if position in actions:
                            if "damage" in actions[position]:
                                actions[position]["damage"] += int(mod[-1]) if "damage" in mod else 0
                                actions[position]["type"] = mod if mod in {"physical", "magic"} and actions[position]["type"] != "push" else actions[position]["type"]
                            elif "repeat" in actions[position] and "repeat" in mod:
                                actions[position]["repeat"] += 1
                            # For behaviors that already cause a condition.
                            elif "effect" in actions[position] and mod in {"bleed", "frostbite", "poison", "stagger"} and mod not in actions[position]["effect"]:
                                actions[position]["effect"].append(mod)
                            elif actions[position]:
                                continue
                            elif not actions[position] and "repeat" in mod and not repeatAdded:
                                # These enemies have their move shifted if they get a repeat.
                                if enemy in {"Phalanx", "Phalanx Hollow", "Silver Knight Spearman"} and position == "middle":
                                    continue
                                actions[position] = {"repeat": repeat}
                                repeatAdded = True

                log("End of apply_mods_to_actions")

                return dodge, repeat, actions
            except Exception as e:
                error_popup(self.root, e)
                raise


        def edit_variant_card_os(self, enemy=None, variant=None, lockedTree=False, event=None, healthMod={"Ornstein": 0, "Smough": 0}, fromDeck=False):
            try:
                log("Start of edit_variant_card_os, enemy={}, variant={}".format(str(enemy), str(variant)))

                if "data" in self.selectedVariant:
                    self.edit_variant_card_data_os(variant=variant, enemy=enemy, healthMod=healthMod)
                else:
                    self.edit_variant_card_behavior_os(variant=variant)

                photoImage = ImageTk.PhotoImage(self.app.displayImage)

                key = "variants" + ("Locked" if lockedTree else "")
                
                if "data" in self.selectedVariant:
                    if enemy == "Ornstein":
                        self.app.displayTopRight.image = photoImage
                        self.app.displayTopRight.config(image=photoImage)
                        self.app.displayImages[key][self.app.displayTopRight]["image"] = photoImage
                        self.app.displayImages[key][self.app.displayTopRight]["name"] = self.selectedVariant
                        self.app.displayImages[key][self.app.displayTopRight]["activeTab"] = key if not fromDeck else "behaviorDeck"
                    else:
                        if enemy != "The Four Kings":
                            self.app.displayKing1.grid_forget()
                            self.app.displayKing2.grid_forget()
                            self.app.displayKing3.grid_forget()
                            self.app.displayKing4.grid_forget()

                        self.app.displayBottomRight.image = photoImage
                        self.app.displayBottomRight.config(image=photoImage)
                        self.app.displayImages[key][self.app.displayBottomRight]["image"] = photoImage
                        self.app.displayImages[key][self.app.displayBottomRight]["name"] = self.selectedVariant
                        self.app.displayImages[key][self.app.displayBottomRight]["activeTab"] = key if not fromDeck else "behaviorDeck"
                else:
                    self.app.displayTopLeft.image = photoImage
                    self.app.displayTopLeft.config(image=photoImage)
                    self.app.displayImages[key][self.app.displayTopLeft]["image"] = photoImage
                    self.app.displayImages[key][self.app.displayTopLeft]["name"] = self.selectedVariant
                    self.app.displayImages[key][self.app.displayTopLeft]["activeTab"] = key if not fromDeck else "behaviorDeck"

                log("End of edit_variant_card_os")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def edit_variant_card_data_os(self, enemy, healthMod={"Ornstein": 0, "Smough": 0}, variant=None, event=None):
            try:
                log("Start of edit_variant_card_data_os, variant={}".format(str(variant)))

                imageWithText = ImageDraw.Draw(self.app.displayImage)

                healthAddition = 0
                health = behaviorDetail["Ornstein & Smough"][enemy]["health"]
                armor = behaviorDetail["Ornstein & Smough"][enemy]["armor"]
                resist = behaviorDetail["Ornstein & Smough"][enemy]["resist"]

                if type(variant) != list and "Ornstein & Smough" in self.currentVariants:
                    mods = [modIdLookup[m] for m in list(self.currentVariants["Ornstein & Smough"]["defKey"]) if m]
                    healthAddition = get_health_bonus(health, mods)
                    health += healthAddition
                    for mod in mods:
                        armor += int(mod[-1]) if "armor" in mod else 0
                        resist += int(mod[-1]) if "resist" in mod else 0
                elif type(variant) == list:
                    healthAddition = get_health_bonus(health, variant)
                    health += healthAddition
                    for mod in variant:
                        armor += int(mod[-1]) if "armor" in mod else 0
                        resist += int(mod[-1]) if "resist" in mod else 0

                if health + healthMod[enemy] >= 0:
                    health += healthMod[enemy]

                imageWithText.text((246, 245), "0", "black", font2)
                imageWithText.text((252 + (2 if health == 0 else 4 if health < 10 else 0), 35), str(health), "white", font2)
                imageWithText.text((130, 245), str(armor), "white", font3)
                imageWithText.text((154, 245), str(resist), "black", font3)
                imageWithText.text((248, 340), str(10 + healthAddition + (5 if enemy == "Smough" else 0)), "black", font)

                log("End of edit_variant_card_data_os")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def edit_variant_card_behavior_os(self, variant=None, event=None):
            try:
                log("Start of edit_variant_card_behavior_os, variant={}".format(str(variant)))

                enemy = self.selectedVariant[:self.selectedVariant.index(" - ")] if " - " in self.selectedVariant else None
                behavior = self.selectedVariant[self.selectedVariant.index(" - ")+3:] if " - " in self.selectedVariant else None
                behaviorSplit = behavior.split(" & ")

                for i, b in enumerate(behaviorSplit):
                    dodge = behaviorDetail[enemy][behavior][b]["dodge"]
                    repeat = behaviorDetail[enemy][behavior][b].get("repeat", 1)
                    actions = {}
                    for position in ["left", "right"]:
                        if position in behaviorDetail[enemy][behavior][b]:
                            actions[position] = behaviorDetail[enemy][behavior][b][position].copy()

                    if variant:
                        dodge, repeat, actions = self.apply_mods_to_actions_os(enemy, behavior, b, dodge, repeat, actions, variant[i])
                    elif enemy in self.currentVariants and behavior in self.currentVariants[enemy]:
                        dodge, repeat, actions = self.apply_mods_to_actions_os(enemy, behavior, b, dodge, repeat, actions)

                    self.add_components_to_variant_card_behavior_os(dodge, repeat, actions, i)

                log("End of edit_variant_card_behavior_os")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def add_components_to_variant_card_behavior_os(self, dodge, repeat, actions, id, event=None):
            try:
                log("Start of add_components_to_variant_card_behavior, dodge={}, repeat={}, actions={}, id={}".format(str(dodge), str(repeat), str(actions), str(id)))

                imageWithText = ImageDraw.Draw(self.app.displayImage)
                if id == 0:
                    imageWithText.text((267, 15), str(dodge), "black", font2)
                else:
                    imageWithText.text((267, 377), str(dodge), "black", font2)

                if repeat > 1 and id == 0:
                    image = self.app.repeat[repeat]
                    self.app.displayImage.paste(im=image, box=(17, 145), mask=image)
                elif repeat > 1:
                    image = self.app.repeat[repeat]
                    self.app.displayImage.paste(im=image, box=(240, 310), mask=image)
                                    
                for position in ["left", "right"]:
                    if position not in actions or not actions[position]:
                        continue
                    if "type" in actions[position] and (actions[position]["type"] == "physical" or actions[position]["type"] == "magic"):
                        if id == 0:
                            x = 107 if position == "left" else 202
                            y = 63
                        else:
                            x = 12 if position == "left" else 107
                            y = 242
                        image = self.app.attack[actions[position]["type"]][actions[position]["damage"]]
                        log("Pasting " + actions[position]["type"] + " attack image onto variant at " + str((x, y)) + ".")
                        self.app.displayImage.paste(im=image, box=(x, y), mask=image)
                    elif "type" in actions[position] and actions[position]["type"] == "push":
                        x = 15 if position == "left" else 110
                        image = self.app.attack[actions[position]["type"]][actions[position]["damage"]]
                        log("Pasting " + actions[position]["type"] + " attack image onto variant at " + str((x, 244)) + ".")
                        self.app.displayImage.paste(im=image, box=(x, 244), mask=image)

                log("End of add_components_to_variant_card_behavior")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def apply_mods_to_actions_os(self, enemy, behavior, b, dodge, repeat, actions, variant=None, event=None):
            try:
                log("Start of apply_mods_to_actions_os, enemy={}, behavior={}, b={}, dodge={}, repeat={}, actions={}, variant={}".format(str(enemy), str(behavior), str(b), str(dodge), str(repeat), str(actions), str(variant)))

                if variant:
                    mods = variant
                else:
                    mods = [modIdLookup[m] for m in list(self.currentVariants[enemy][behavior][b])]

                for mod in mods:
                    dodge += int(mod[-1]) if "dodge" in mod else 0
                    repeat += 1 if "repeat" in mod else 0
                    newConditionAdded = False

                    # For behaviors that do not already cause a condition.
                    if (
                        mod in {"bleed", "frostbite", "poison", "stagger"}
                        and "effect" not in actions.get("right", {})
                        ):
                        if "right" in actions and not actions["right"]:
                            actions[position]["effect"] = [mod]
                            newConditionAdded = True

                    if newConditionAdded:
                        continue

                    for position in ["left", "right"]:
                        if position in actions:
                            if "damage" in actions[position]:
                                actions[position]["damage"] += int(mod[-1]) if "damage" in mod else 0
                            if "type" in actions[position]:
                                actions[position]["type"] = mod if mod in {"physical", "magic"} else actions[position]["type"]
                            # For behaviors that already cause a condition.
                            elif "effect" in actions[position] and mod in {"bleed", "frostbite", "poison", "stagger"} and mod not in actions[position]["effect"]:
                                actions[position]["effect"].append(mod)

                log("End of apply_mods_to_actions_os")

                return dodge, repeat, actions
            except Exception as e:
                error_popup(self.root, e)
                raise


        def save_variants(self):
            """
            Save locked variants to a JSON file that can be loaded later.
            """
            try:
                log("Start of save_variants")

                # Prompt user to save the file.
                fileName = filedialog.asksaveasfile(mode="w", initialdir=baseFolder + "\\lib\\dsbg_shuffle_saved_variants".replace("\\", pathSep), defaultextension=".json")

                # If they canceled it, do nothing.
                if not fileName:
                    log("End of save_variants (nothing done)")
                    return
                
                tree = self.treeviewVariantsLocked
                
                variantData = {
                    "lockedVariants": self.lockedVariants,
                    "Enemies": [],
                    "Invaders & Explorers Mimics": [],
                    "Mini Bosses": [],
                    "Main Bosses": [],
                    "Mega Bosses": []
                    }
                
                for cat in variantData:
                    if cat == "lockedVariants":
                        continue
                    for child in tree.get_children(cat):
                        variantData[cat].append((tree.parent(child), child, tree.item(child)))
                        for subChild in tree.get_children(child):
                            variantData[cat].append((tree.parent(subChild), subChild, tree.item(subChild)))

                with open(fileName.name, "w") as variantFile:
                    dump(variantData, variantFile)

                log("End of save_variants (saved to " + str(variantFile) + ")")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def load_variants(self):
            """
            Load variants from a JSON file, clearing the current locked variants treeview and replacing
            it with the data from the JSON file.
            """
            try:
                log("Start of load_variants")

                # Prompt the user to find the campaign file.
                variantFile = filedialog.askopenfilename(initialdir=baseFolder + "\\lib\\dsbg_shuffle_saved_variants".replace("\\", pathSep), filetypes = [(".json", ".json")])

                # If the user did not select a file, do nothing.
                if not variantFile:
                    log("End of load_variants (file dialog canceled)")
                    return
                
                # If the user did not select a JSON file, notify them that that was an invalid file.
                if os.path.splitext(variantFile)[1] != ".json":
                    self.set_bindings_buttons_menus(False)
                    PopupWindow(self.master, labelText="Invalid DSBG-Shuffle variants file.", firstButton="Ok")
                    self.set_bindings_buttons_menus(True)
                    log("End of load_variants (invalid file)")
                    return
                
                progress = PopupWindow(self.root, labelText="Loading variants, please wait...", loadingImage=True)
                
                log("Loading file " + variantFile)

                with open(variantFile, "r") as f:
                    variantData = load(f)

                tree = self.treeviewVariantsLocked
                treeList = self.treeviewVariantsList

                itemCheck = ["lockedVariants", "Enemies", "Invaders & Explorers Mimics", "Mini Bosses", "Main Bosses", "Mega Bosses"]

                for cat in itemCheck:
                    if treeList.exists(cat):
                        for enemy in treeList.get_children(cat):
                            itemCheck.append(enemy)
                            for behavior in treeList.get_children(enemy):
                                itemCheck.append(behavior)

                itemCheck = set(itemCheck)

                # Check to see if there are any invalid names in the JSON file.
                # This is about as sure as I can be that you can't load random JSON into the app.
                if any([v not in itemCheck for v in variantData]):
                    self.set_bindings_buttons_menus(False)
                    PopupWindow(self.master, labelText="Invalid DSBG-Shuffle variant file.", firstButton="Ok")
                    self.set_bindings_buttons_menus(True)
                    log("End of load_variants (invalid file)")
                    return
                
                # Remove existing locked variants.
                self.delete_locked_variant("All")

                # Create the locked variant treeview rows.
                self.lockedVariants = variantData["lockedVariants"]
                for item in variantData:
                    if treeList.exists(item):
                        for subItem in variantData[item]:
                            tree.insert(parent=subItem[0], iid=subItem[1], values=subItem[2]["values"], index="end", tags=True)

                # Recalculate the average difficulty mod for this row and its parents and children.
                for child in tree.get_children("All"):
                    for subChild in tree.get_children(child):
                        for subSubChild in tree.get_children(subChild):
                            self.recalc_variant_average(tree, subSubChild)
                        self.recalc_variant_average(tree, subChild)
                    self.recalc_variant_average(tree, child)

                progress.destroy()

                log("End of load_variants (loaded from " + str(variantFile) + ")")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def print_variant_cards(self):
            """
            Export variant cards to a PDF.
            """
            try:
                log("Start of print_variant_cards")

                # Add cards to a list associated with their type/size.
                l = list(self.lockedVariants.keys())
                variantsToPrint = []
                for i in range(0, len(l), 9):
                    if any(["Ornstein & Smough_" in b for b in l[i:i+9]]):
                        m = [a for a in l[i:i+8]]
                        osVal = [b for b in l[i:i+9] if "Ornstein & Smough_" in b][0]
                        osIdx = m.index(osVal)
                        m.insert(osIdx+1, None)
                        variantsToPrint.append(m)
                    else:
                        variantsToPrint.append(l[i:i+9])

                progress = PopupWindow(self.root, labelText="Creating PDF...", progressBar=True, progressMax=len(l), loadingImage=True)
                p = 0

                width = 63
                height = 88
                standardCards = 8
                columnBreaks = {2, 5}

                buffer = 5
                pdf = FPDF(unit="mm")
                pdf.set_margins(buffer, buffer, buffer)

                # Loop through the card list and add them to pages.
                for page in variantsToPrint:
                    pdf.add_page()
                    x = buffer
                    y = buffer
                    pdf.set_x(x)
                    pdf.set_y(y)

                    for i, variant in enumerate(page):
                        if not variant:
                            continue
                        # Create the variant card.
                        if "Ornstein & Smough" in variant:
                            self.load_variant_card_locked(variant=variant, forPrinting=True, healthMod={"Ornstein": 0, "Smough": 0})
                        else:
                            self.load_variant_card_locked(variant=variant, forPrinting=True)

                        # Stage the image.
                        if self.app.displayImages["variants"][self.app.displayTopLeft]["image"]:
                            self.add_card_to_pdf(variant, width, pdf, self.app.displayImages["variants"][self.app.displayTopLeft]["image"], x, y)
                        if self.app.displayImages["variants"][self.app.displayTopRight]["image"] and "Ornstein & Smough_" in variant:
                            self.add_card_to_pdf(variant, width, pdf, self.app.displayImages["variants"][self.app.displayTopRight]["image"], x, y, ornstein=True)
                        elif self.app.displayImages["variants"][self.app.displayTopRight]["image"]:
                            self.add_card_to_pdf(variant, width, pdf, self.app.displayImages["variants"][self.app.displayTopRight]["image"], x, y)

                        if i < standardCards:
                            if i in columnBreaks:
                                x += width + buffer
                                y = buffer
                            else:
                                y += height + buffer
                        elif i == standardCards:
                            x += width + buffer
                            y = buffer
                        else:
                            y += width + buffer

                        if self.app.displayImages["variants"][self.app.displayBottomRight]["image"] and "Ornstein & Smough_" in variant:
                            self.add_card_to_pdf(variant, width, pdf, self.app.displayImages["variants"][self.app.displayBottomRight]["image"], x, y, smough=True)

                            i += 1

                            if i < standardCards:
                                if i in columnBreaks:
                                    x += width + buffer
                                    y = buffer
                                else:
                                    y += height + buffer
                            elif i == standardCards:
                                x += width + buffer
                                y = buffer
                            else:
                                y += width + buffer

                        p += 1
                        progress.progressVar.set(p)
                        self.root.update_idletasks()

                progress.destroy()

                # Prompt user to save the file.
                pdfOutput = filedialog.asksaveasfile(mode="w", initialdir=baseFolder + "\\lib\\dsbg_shuffle_exports".replace("\\", pathSep), defaultextension=".pdf")

                # If they canceled it, do nothing.
                if not pdfOutput:
                    log("End of print_variant_cards (nothing done)")
                    return
                
                progress = PopupWindow(self.root, labelText="Saving PDF, please wait...", loadingImage=True)

                pdf.output(pdfOutput.name)

                progress.destroy()

                log("End of print_variant_cards")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def add_card_to_pdf(self, variant, width, pdf, imageToAdd, x, y, ornstein=False, smough=False):
            """
            Adds a card to the PDF.
            """
            try:
                log("Start of add_card_to_pdf")
                
                imageStage = ImageTk.getimage(imageToAdd)

                if ornstein:
                    variant = variant.replace(" & Smough", "")
                elif smough:
                    variant = variant.replace("Ornstein & ", "")

                imageStage.save(baseFolder + "\\lib\\dsbg_shuffle_image_staging\\".replace("\\", pathSep) + variant + ".png")

                log("\tAdding " + variant + " to PDF at (" + str(x) + ", " + str(y) + ") with width of " + str(width))
                pdf.image(baseFolder + "\\lib\\dsbg_shuffle_image_staging\\".replace("\\", pathSep) + variant + ".png", x=x, y=y, type="PNG", w=width)

                log("End of add_card_to_pdf")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def callback(self, P):
            """
            Validates whether the input for enemy difficulty is an integer.
            """
            try:
                log("Start of callback")

                if (str.isdigit(P) or str(P) == "") and len(P) <= 7:
                    log("End of callback")
                    return True
                else:
                    log("End of callback")
                    return False
            except Exception as e:
                error_popup(self.root, e)
                raise

except Exception as e:
    log(e, exception=True)
    raise
