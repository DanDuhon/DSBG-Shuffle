try:
    import tkinter as tk
    from copy import deepcopy
    from PIL import ImageDraw, ImageTk
    from random import choice, sample, shuffle
    from tkinter import ttk

    from dsbg_shuffle_enemies import bosses, enemiesDict
    from dsbg_shuffle_behaviors import behaviorDetail, behaviors
    from dsbg_shuffle_utility import PopupWindow, clear_other_tab_images, error_popup, log, set_display_bindings_by_tab, font2
    from dsbg_shuffle_variants import get_health_bonus, modIdLookup


    class BehaviorDeckFrame(ttk.Frame):
        def __init__(self, app, root):
            super(BehaviorDeckFrame, self).__init__()
            self.app = app
            self.root = root

            self.deckTabButtonsFrame = ttk.Frame(self)
            self.deckTabButtonsFrame.pack()
            self.deckTabButtonsFrame2 = ttk.Frame(self)
            self.deckTabButtonsFrame2.pack()
            self.deckTreeviewFrame = ttk.Frame(self)
            self.deckTreeviewFrame.pack(fill="both", expand=True)
            self.scrollbarTreeviewDeck = ttk.Scrollbar(self.deckTreeviewFrame)
            self.scrollbarTreeviewDeck.pack(side="right", fill="y")

            self.drawButton = ttk.Button(self.deckTabButtonsFrame, text="Draw Card", width=16, command=self.draw_behavior_card)
            self.drawButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.heatupButton = ttk.Button(self.deckTabButtonsFrame, text="Heat Up", width=16, command=self.heatup)
            self.heatupButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.resetButton = ttk.Button(self.deckTabButtonsFrame, text="Reset Deck", width=16, command=self.set_decks)
            self.resetButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

            self.drawButton = ttk.Button(self.deckTabButtonsFrame2, text="Add Tracker", width=16, command=lambda add=True: self.health_tracker(add))
            self.drawButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.heatupButton = ttk.Button(self.deckTabButtonsFrame2, text="Remove Trackers", width=16, command=self.remove_all_health_trackers)
            self.heatupButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

            self.decks = (
                {k: {} for k in enemiesDict}
                | {k: {} for k in bosses if "Vordt" not in k}
                | {"Vordt of the Boreal Valley (move)": {}}
                | {"Vordt of the Boreal Valley (attack)": {}}
                )
            
            for enemy in self.decks:
                self.decks[enemy] = {
                    "deck": [],
                    "curIndex": 0,
                    "heatup": 0 if enemy in "Old Dragonslayer" else 1 if enemy == "The Four Kings" else False,
                    "lastCardDrawn": None,
                    "defKey": {"",}
                    }
                
                if enemy not in behaviors and enemiesDict[enemy].id in self.app.enabledEnemies:
                    self.decks[enemy]["healthMod"] = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
                
                if enemy == "Ornstein & Smough":
                    self.decks[enemy]["healthMod"] = {"Ornstein": 0, "Smough": 0}
                elif enemy == "The Four Kings":
                    self.decks[enemy]["healthMod"] = {1: 0, 2: 0, 3: 0, 4: 0}
                else:
                    self.decks[enemy]["healthMod"] = 0
                
                if enemy == "Smelter Demon":
                    self.decks[enemy]["heatupCnt"] = 5
                elif enemy == "Ornstein & Smough":
                    self.decks[enemy]["heatupCnt"] = 5
                elif enemy == "Guardian Dragon":
                    self.decks[enemy]["heatupCnt"] = 7
                elif enemy == "The Last Giant":
                    self.decks[enemy]["heatupCnt"] = 6
                elif enemy == "Paladin Leeroy":
                    self.decks[enemy]["healingTalisman"] = False

            self.create_deck_treeview()
            
            for enemy in self.decks:
                if (
                    ((enemy[:enemy.index(" (")] if "Vordt" in enemy else enemy) in bosses
                        and bosses[(enemy[:enemy.index(" (")] if "Vordt" in enemy else enemy)]["expansions"] & self.app.availableExpansions)
                    or (enemy in enemiesDict
                        and enemiesDict[enemy].expansions & self.app.availableExpansions)
                    ):
                    self.set_decks(enemy, skipClear=True)


        def reset_treeview(self):
            self.treeviewDecks.pack_forget()
            self.treeviewDecks.destroy()
            self.create_deck_treeview()
                

        def create_deck_treeview(self):
            """
            Create the behavior deck treeview, where a user can select an
            enemy to create or draw from a behavior deck.
            """
            try:
                log("Start of create_deck_treeview")

                self.treeviewDecks = ttk.Treeview(
                    self.deckTreeviewFrame,
                    selectmode="browse",
                    columns=("Name", "Cards in Deck", "Heat Up"),
                    yscrollcommand=self.scrollbarTreeviewDeck.set,
                    height=11 if self.root.winfo_screenheight() > 1000 else 9
                )

                self.treeviewDecks.pack(expand=True, fill="both")
                self.scrollbarTreeviewDeck.config(command=self.treeviewDecks.yview)

                self.treeviewDecks.column('#0', width=50)

                self.treeviewDecks.heading("Name", text="Name", anchor=tk.W)
                self.treeviewDecks.heading("Cards in Deck", text="Cards in Deck", anchor=tk.W)
                self.treeviewDecks.heading("Heat Up", text="Heat Up", anchor=tk.W)
                self.treeviewDecks.column("Name", anchor=tk.W, width=300)
                self.treeviewDecks.column("Cards in Deck", anchor=tk.W, width=90)
                self.treeviewDecks.column("Heat Up", anchor=tk.W, width=90)
                
                self.treeviewDecks.insert(parent="", index="end", iid="Enemies", values=("Enemies", "", ""), tags=False)
                if {"Phantoms", "Explorers"} & self.app.availableExpansions:
                    self.treeviewDecks.insert(parent="", index="end", iid="Invaders & Explorers Mimics", values=("Invaders & Explorers Mimics", "", ""), tags=False)
                self.treeviewDecks.insert(parent="", index="end", iid="Mini Bosses", values=("Mini Bosses", "", ""), tags=False)
                self.treeviewDecks.insert(parent="", index="end", iid="Main Bosses", values=("Main Bosses", "", ""), tags=False)
                if set([boss for boss in bosses if bosses[boss]["level"] == "Mega Boss"]) & self.app.availableExpansions:
                    self.treeviewDecks.insert(parent="", index="end", iid="Mega Bosses", values=("Mega Bosses", "", ""), tags=False)

                for enemy in sorted([enemy for enemy in enemiesDict if enemiesDict[enemy].expansions & self.app.availableExpansions and "Phantoms" not in enemiesDict[enemy].expansions and enemiesDict[enemy].name not in {"Hungry Mimic", "Voracious Mimic"}]):
                    self.treeviewDecks.insert(parent="Enemies", index="end", iid=enemy, values=("    " + enemy, "", ""), tags=True)

                for enemy in sorted([enemy for enemy in enemiesDict if enemiesDict[enemy].expansions & self.app.availableExpansions and ("Phantoms" in enemiesDict[enemy].expansions or enemiesDict[enemy].name in {"Hungry Mimic", "Voracious Mimic"})]):
                    self.treeviewDecks.insert(parent="Invaders & Explorers Mimics", index="end", iid=enemy, values=("    " + enemy, enemiesDict[enemy].cards, ""), tags=True)
                    
                for enemy in sorted([enemy for enemy in bosses if (
                    bosses[enemy]["expansions"] & self.app.availableExpansions
                    and enemy != "Vordt of the Boreal Valley"
                    )]):
                    self.treeviewDecks.insert(parent=bosses[enemy]["level"] + "es", index="end", iid=enemy, values=("    " + enemy, bosses[enemy]["cards"], ""), tags=True)

                if "Vordt of the Boreal Valley" in self.app.availableExpansions:
                    self.treeviewDecks.insert(parent="Mega Bosses", index="end", iid="Vordt of the Boreal Valley (move)", values=("    Vordt of the Boreal Valley (move)", 4), tags=True)
                    self.treeviewDecks.insert(parent="Mega Bosses", index="end", iid="Vordt of the Boreal Valley (attack)", values=("    Vordt of the Boreal Valley (attack)", 3), tags=True)

                self.treeviewDecks.bind("<<TreeviewSelect>>", self.display_deck_cards)

                log("End of create_deck_treeview")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def load_deck(self, enemy):
            try:
                log("Start of load_deck")

                if enemy not in behaviors:
                    log("End of load_deck (regular enemy)")
                    return

                lookupName = enemy if "(" not in enemy else enemy[:enemy.index(" (")]

                behaviorsWithDupes = deepcopy(behaviors)
                if enemy == "The Pursuer":
                    behaviorsWithDupes["The Pursuer"].append("Stabbing Strike")
                    behaviorsWithDupes["The Pursuer"].append("Wide Blade Swing")
                    behaviorsWithDupes["The Pursuer"].append("Wide Blade Swing")

                nonHeatupCards = [b for b in behaviorsWithDupes[enemy] if (
                    (
                        not behaviorDetail[lookupName][b].get("heatup", False)
                        or (lookupName == "The Four Kings" and behaviorDetail[lookupName][b].get("heatup", False) == 1)
                    )
                    and b not in {
                        "Mark of Calamity",
                        "Hellfire Blast",
                        "Death Race",
                        "Stomach Slam",
                        "Crawling Charge",
                        "Fire Beam (Left)",
                        "Fire Beam (Right)",
                        "Fire Beam (Front)",
                        "Falling Slam",
                        "Limping Strike"
                    })
                    ]

                if enemy in enemiesDict:
                    deck = sample(nonHeatupCards, enemiesDict[enemy].cards)
                elif "(move)" in enemy: # Vordt
                    deck = sample(nonHeatupCards, 4)
                elif "(attack)" in enemy: # Vordt
                    deck = sample(nonHeatupCards, 3)
                elif enemy == "Executioner Chariot":
                    deck = sample(nonHeatupCards, 4) + [choice([b for b in behaviors[enemy] if behaviorDetail[lookupName][b].get("heatup", False)])]
                elif enemy == "Gaping Dragon":
                    deck = sample(nonHeatupCards, 3)
                    deck += ["Stomach Slam", "Stomach Slam", choice([b for b in behaviors[enemy] if behaviorDetail[lookupName][b].get("heatup", False)])]
                elif enemy == "Old Iron King":
                    deck = sample(nonHeatupCards, 3) + ["Fire Beam (Front)", "Fire Beam (Left)", "Fire Beam (Right)"]
                elif enemy == "The Last Giant":
                    normalCards = [b for b in behaviors[enemy] if (
                        not behaviorDetail[lookupName][b].get("heatup", False)
                        and not behaviorDetail[lookupName][b].get("arm", False)
                        and b != "Falling Slam")
                        ]
                    armCards = [b for b in behaviors[enemy] if behaviorDetail[lookupName][b].get("arm", False)]
                    deck = sample(normalCards, 3) + sample(armCards, 3)
                else:
                    deck = sample(nonHeatupCards, bosses[enemy]["cards"])

                shuffle(deck)

                log("End of load_deck")
                return deck
            except Exception as e:
                error_popup(self.root, e)
                raise


        def set_decks(self, enemy=None, skipClear=False):
            """
            Sets the deck cards for this enemy.
            """
            try:
                log("Start of set_decks")

                if not enemy:
                    # Reset the other Vordt deck if one was reset.
                    if "Vordt" in self.treeviewDecks.selection()[0]:
                        self.set_decks(enemy="Vordt of the Boreal Valley " +  ("(move)" if "(attack)" in self.treeviewDecks.selection()[0] else "(attack)"))
                    enemy = self.treeviewDecks.selection()[0]

                if enemy not in self.decks:
                    log("End of set_decks (nothing done)")
                    return

                if not skipClear:
                    # Remove keyword tooltips from the previous image shown, if there are any.
                    for tooltip in self.app.tooltips:
                        tooltip.destroy()

                    # Remove the displayed item.
                    clear_other_tab_images(
                        self.app,
                        "behaviorDeck",
                        "behaviorDeck",
                        name=enemy[:enemy.index(" - ")] if " - " in enemy else enemy[:enemy.index("_")] if "_" in enemy else enemy)
                
                    self.app.display.config(image="")
                    self.app.display.image=None
                    self.app.displayImages["variantsLocked"][self.app.display]["image"] = None
                    self.app.displayImages["variantsLocked"][self.app.display]["name"] = None
                    self.app.displayImages["variantsLocked"][self.app.display]["activeTab"] = None
                    self.decks[enemy]["lastCardDrawn"] = None

                self.decks[enemy]["deck"] = self.load_deck(enemy)
                
                if enemy in behaviors:
                    if enemy == "Oliver the Collector":
                        self.decks[enemy]["heatupCards"] = [b for b in behaviors[enemy] if b not in set(self.decks[enemy]["deck"])]
                    elif enemy in {"Old Dragonslayer", "Artorias"}:
                        self.decks[enemy]["heatupCards"] = [b for b in behaviors[enemy] if behaviorDetail[enemy][b].get("heatup", False)]
                    elif enemy == "Smelter Demon":
                        self.decks[enemy]["heatupCards"] = sample([b for b in behaviors[enemy] if behaviorDetail[enemy][b].get("heatup", False)], 5)
                    elif enemy == "Ornstein & Smough":
                        self.decks[enemy]["heatupCards"] = {}
                        self.decks[enemy]["heatupCards"]["Ornstein"] = ["Charged Bolt", "Charged Swiping Combo", "Electric Clash", "High Voltage", "Lightning Stab"]
                        self.decks[enemy]["heatupCards"]["Smough"] = ["Charged Charge", "Electric Bonzai Drop", "Electric Hammer Smash", "Jumping Volt Slam", "Lightning Sweep"]
                        shuffle(self.decks[enemy]["heatupCards"]["Ornstein"])
                        shuffle(self.decks[enemy]["heatupCards"]["Smough"])
                    elif enemy == "Guardian Dragon":
                        self.decks[enemy]["heatupCards"] = ["Cage Grasp Inferno", "Cage Grasp Inferno"]
                    elif enemy == "The Four Kings":
                        self.decks[enemy]["heatupCards"] = {}
                        self.decks[enemy]["heatupCards"][2] = [b for b in behaviors[enemy] if behaviorDetail[enemy][b].get("heatup", 1) == 2]
                        self.decks[enemy]["heatupCards"][3] = [b for b in behaviors[enemy] if behaviorDetail[enemy][b].get("heatup", 1) == 3]
                        self.decks[enemy]["heatupCards"][4] = [b for b in behaviors[enemy] if behaviorDetail[enemy][b].get("heatup", 1) == 4]
                        shuffle(self.decks[enemy]["heatupCards"][2])
                        shuffle(self.decks[enemy]["heatupCards"][3])
                        shuffle(self.decks[enemy]["heatupCards"][4])
                    elif enemy == "The Last Giant":
                        self.decks[enemy]["heatupCards"] = sample([b for b in behaviors[enemy] if behaviorDetail[enemy][b].get("heatup", False)], 3) + ["Falling Slam"]
                    else:
                        if "Vordt" in enemy:
                            enemyName = enemy[:enemy.index(" (")]
                        else:
                            enemyName = enemy
                        if [b for b in behaviors[enemy] if behaviorDetail[enemyName][b].get("heatup", False)]:
                            self.decks[enemy]["heatupCards"] = [choice([b for b in behaviors[enemy] if behaviorDetail[enemyName][b].get("heatup", False)])]
                        else:
                            self.decks[enemy]["heatupCards"] = [choice([b for b in behaviors[enemy] if b not in set(self.decks[enemy]["deck"])])]

                    if type(self.decks[enemy]["heatupCards"]) == list:
                        shuffle(self.decks[enemy]["heatupCards"])

                self.decks[enemy]["heatup"] = 0 if enemy == "Old Dragonslayer" else 1 if enemy == "The Four Kings" else False
                self.decks[enemy]["healthMod"] = {"Ornstein": 0, "Smough": 0} if enemy == "Ornstein & Smough" else {1: 0, 2: 0, 3: 0, 4: 0} if enemy == "The Four Kings" else {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0} if enemy not in behaviors and enemiesDict[enemy].id in self.app.enabledEnemies else 0
                self.decks[enemy]["curIndex"] = 0
                self.decks[enemy]["lastCardDrawn"] = None
                self.treeviewDecks.item(enemy, values=(
                    self.treeviewDecks.item(enemy)["values"][0],
                    len(self.decks[enemy]["deck"]) if self.decks[enemy]["deck"] else "",
                    ""))

                if (enemy[:enemy.index(" (")] if "Vordt" in enemy else enemy) in set([v[:v.index("_")] for v in self.app.variantsTab.lockedVariants]):
                    self.decks[enemy]["defKey"] = choice([self.app.variantsTab.lockedVariants[v] for v in self.app.variantsTab.lockedVariants if "-" not in v])
                elif (enemy[:enemy.index(" (")] if "Vordt" in enemy else enemy) in self.app.variantsTab.currentVariants:
                    self.decks[enemy]["defKey"] = self.app.variantsTab.currentVariants[enemy]["defKey"]
                else:
                    self.decks[enemy]["defKey"] = {"",}

                self.remove_all_health_trackers(enemy)

                if not skipClear and self.treeviewDecks.selection():
                    self.display_deck_cards()

                log("End of set_decks")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def draw_behavior_card(self):
            try:
                log("Start of draw_behavior_card")

                if (
                    not self.treeviewDecks.selection()
                    or self.treeviewDecks.selection()[0] not in self.decks 
                    or not self.decks[self.treeviewDecks.selection()[0]]["deck"]):
                    log("End of draw_behavior_card (nothing done)")
                    return

                selection = self.treeviewDecks.selection()[0]
                
                if self.decks[selection]["curIndex"] == len(self.decks[selection]["deck"]):
                    if selection == "The Four Kings":
                        self.heatup(selection)
                    self.decks[selection]["curIndex"] = 0

                variantSelection = (selection[:selection.index(" (")] if "Vordt" in selection else selection)
                variantSelectionWithMods = variantSelection + "_" + ",".join([str(m) for m in self.decks[selection]["defKey"]])
                cardToDraw = variantSelection + " - " + self.decks[selection]["deck"][self.decks[selection]["curIndex"]]
                
                if cardToDraw.count("&") == 2:
                    # O&S pre-heatup behavior
                    cardToDrawOptions = [k for k in self.app.variantsTab.lockedVariants if (
                        cardToDraw in k
                        and set(self.decks[selection]["defKey"]).issubset(set(self.app.variantsTab.lockedVariants[k][0]))
                        and set(self.decks[selection]["defKey"]).issubset(set(self.app.variantsTab.lockedVariants[k][1])))]
                else:
                    cardToDrawOptions = [k for k in self.app.variantsTab.lockedVariants if (
                        cardToDraw in k
                        and set(self.decks[selection]["defKey"]).issubset(set(self.app.variantsTab.lockedVariants[k])))]
                
                if variantSelectionWithMods in set(self.app.variantsTab.lockedVariants) and cardToDrawOptions:
                    variant = choice(cardToDrawOptions)
                else:
                    variant = cardToDraw
                    
                if selection == "Armorer Dennis" and self.decks[selection]["heatup"]:
                    self.app.variantsTab.load_variant_card_locked(variant=variant, armorerDennis=True, fromDeck=True, healthMod=self.decks[self.treeviewDecks.selection()[0]]["healthMod"])
                elif selection == "The Pursuer" and self.decks[selection]["heatup"]:
                    self.app.variantsTab.load_variant_card_locked(variant=variant, pursuer=True, fromDeck=True, healthMod=self.decks[self.treeviewDecks.selection()[0]]["healthMod"])
                elif selection == "Old Iron King" and self.decks[selection]["heatup"]:
                    self.app.variantsTab.load_variant_card_locked(variant=variant, oldIronKing=True, fromDeck=True, healthMod=self.decks[self.treeviewDecks.selection()[0]]["healthMod"])
                else:
                    self.app.variantsTab.load_variant_card_locked(variant=variant, fromDeck=True, healthMod=self.decks[self.treeviewDecks.selection()[0]]["healthMod"])

                if selection == "The Four Kings":
                    for x in range(1, 5):
                        self.four_kings_health_track(king=x, healthMod=self.decks["The Four Kings"]["healthMod"][x])
                
                self.decks[selection]["lastCardDrawn"] = variant

                if selection == "Dancer of the Boreal Valley" and behaviorDetail["Dancer of the Boreal Valley"][self.decks[selection]["deck"][self.decks[selection]["curIndex"]]].get("heatup", False):
                    self.decks[selection]["curIndex"] = 0
                    shuffle(self.decks[selection]["deck"])
                else:
                    self.decks[selection]["curIndex"] += 1

                self.treeviewDecks.item(selection, values=(
                    self.treeviewDecks.item(selection)["values"][0],
                    len(self.decks[selection]["deck"]) - self.decks[selection]["curIndex"],
                    self.treeviewDecks.item(selection)["values"][2]))

                log("End of draw_behavior_card")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def display_deck_cards(self, event=None):
            try:
                log("Start of display_deck_cards")

                selection = self.treeviewDecks.selection()[0]

                if selection in self.decks:
                    # Remove keyword tooltips from the previous image shown, if there are any.
                    for tooltip in self.app.tooltips:
                        tooltip.destroy()

                    # Remove the displayed item.
                    clear_other_tab_images(
                        self.app,
                        "behaviorDeck",
                        "behaviorDeck",
                        name=selection[:selection.index(" - ")] if " - " in selection else selection[:selection.index("_")] if "_" in selection else selection)

                    if selection == "Ornstein & Smough":
                        self.app.variantsTab.load_variant_card_locked(variant="Ornstein - data", deckDataCard=True, healthMod=self.decks[self.treeviewDecks.selection()[0]]["healthMod"], fromDeck=True)
                        self.app.variantsTab.load_variant_card_locked(variant="Smough - data", deckDataCard=True, healthMod=self.decks[self.treeviewDecks.selection()[0]]["healthMod"], fromDeck=True)
                    else:
                        selection = selection[:selection.index(" (")] if "Vordt" in selection else selection
                        self.app.variantsTab.load_variant_card_locked(variant=selection + ("_" + ",".join([str(m) for m in self.decks[self.treeviewDecks.selection()[0]]["defKey"]]) if self.decks[self.treeviewDecks.selection()[0]].get("defKey", None) else ""), deckDataCard=True, healthMod=0 if selection == "The Four Kings" or self.treeviewDecks.parent(selection) == "Enemies" else self.decks[self.treeviewDecks.selection()[0]]["healthMod"], fromDeck=True)

                    if self.decks[self.treeviewDecks.selection()[0]]["lastCardDrawn"]:
                        self.app.variantsTab.load_variant_card_locked(variant=self.decks[self.treeviewDecks.selection()[0]]["lastCardDrawn"], healthMod=0 if selection == "The Four Kings" or self.treeviewDecks.parent(selection) == "Enemies" else self.decks[self.treeviewDecks.selection()[0]]["healthMod"], fromDeck=True)

                    if selection == "The Four Kings":
                        for x in range(1, 5):
                            self.four_kings_health_track(king=x, healthMod=self.decks["The Four Kings"]["healthMod"][x])
                    elif self.treeviewDecks.parent(selection) == "Enemies":
                        self.health_tracker()

                    set_display_bindings_by_tab(self.app, selection == "Ornstein & Smough")

                log("End of display_deck_cards")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def four_kings_health_track(self, king, healthMod=0):
            try:
                log("Start of four_kings_health_track")

                self.app.create_image("The Four Kings health track" + str(king) + ".jpg", "fourKingsHealth")

                imageWithText = ImageDraw.Draw(self.app.displayImage)

                health = behaviorDetail["The Four Kings"]["health"]

                mods = [modIdLookup[m] for m in list(self.decks["The Four Kings"]["defKey"]) if m]
                healthAddition = get_health_bonus(health, mods)
                health += healthAddition

                if healthMod and health + healthMod >= 0:
                    health += healthMod

                if king <= self.decks["The Four Kings"]["heatup"]:
                    imageWithText.text((118 + (2 if health == 0 else 4 if health < 10 else 0), 17), str(health), "white", font2)
                else:
                    imageWithText.text((124, 16), "-", "white", font2)

                displayPhotoImage = ImageTk.PhotoImage(self.app.displayImage)

                if king == 1:
                    display = self.app.displayKing1
                elif king == 2:
                    display = self.app.displayKing2
                elif king == 3:
                    display = self.app.displayKing3
                elif king == 4:
                    display = self.app.displayKing4

                display.image = displayPhotoImage
                display.config(image=displayPhotoImage)
                display.grid(row=king, column=1, sticky="nsew")

                log("End of four_kings_health_track")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def health_tracker(self, add=False, labelIndex=-1):
            try:
                log("Start of health_tracker")

                if not self.treeviewDecks.selection() or self.treeviewDecks.parent(self.treeviewDecks.selection()[0]) != "Enemies":
                    log("End of health_tracker (regular enemy not selected)")
                    return

                if self.app.display2.image != self.app.displayImages["behaviorDeck"][self.app.display2]["image"]:
                    log("End of health_tracker (came from other tab - displaying cards first)")
                    self.display_deck_cards()
                
                enemy = self.treeviewDecks.selection()[0]

                if add:
                    display = None
                    spot = 0

                    for s, d in enumerate(self.decks[enemy]["healthTrackers"]):
                        if not d.image:
                            display = d
                            spot = s
                            healthMod = self.decks[enemy]["healthMod"][s]
                            break

                    if not display:
                        log("End of health_tracker (no spots available)")
                        return

                    self.app.create_image("Health track " + enemy + ".jpg", "healthTracker")

                    imageWithText = ImageDraw.Draw(self.app.displayImage)

                    health = behaviorDetail[enemy]["health"]

                    mods = [modIdLookup[m] for m in list(self.decks[enemy]["defKey"]) if m]
                    healthAddition = get_health_bonus(health, mods)
                    health += healthAddition

                    if healthMod and health + healthMod >= 0:
                        health += healthMod

                    imageWithText.text((67 + (
                        2 if health == 0 else
                        4 if health == 1 else
                        3 if health < 10 else 0), 17), str(health), "white", font2)

                    displayPhotoImage = ImageTk.PhotoImage(self.app.displayImage)

                    display.image = displayPhotoImage
                    display.config(image=displayPhotoImage)
                    display.grid(row=1+int(spot/2), column=1+(spot%2), sticky="nsew")
                elif labelIndex > -1:
                    self.app.create_image("Health track " + enemy + ".jpg", "healthTracker")

                    imageWithText = ImageDraw.Draw(self.app.displayImage)

                    health = behaviorDetail[enemy]["health"]
                    healthMod = self.decks[enemy]["healthMod"][labelIndex]

                    mods = [modIdLookup[m] for m in list(self.decks[enemy]["defKey"]) if m]
                    healthAddition = get_health_bonus(health, mods)
                    health += healthAddition

                    if healthMod and health + healthMod >= 0:
                        health += healthMod

                    imageWithText.text((67 + (
                        2 if health == 0 else
                        4 if health == 1 else
                        3 if health < 10 else 0), 17), str(health), "white", font2)

                    displayPhotoImage = ImageTk.PhotoImage(self.app.displayImage)

                    display = self.decks[enemy]["healthTrackers"][labelIndex]
                    display.image = displayPhotoImage
                    display.config(image=displayPhotoImage)
                    display.grid(row=1+int(labelIndex/2), column=1+(labelIndex%2), sticky="nsew")
                else:
                    for s, d in enumerate(self.decks[enemy]["healthTrackers"]):
                        if d.image:
                            d.grid(row=1+int(s/2), column=1+(s%2), sticky="nsew")

                log("End of health_tracker")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def remove_all_health_trackers(self, enemy=None):
            try:
                log("Start of remove_all_health_trackers")

                if not self.treeviewDecks.selection():
                    log("End of remove_all_health_trackers (nothing done)")
                    return

                if not enemy:
                    enemy = self.treeviewDecks.selection()[0]

                if (
                    enemy not in self.decks
                    or "healthTrackers" not in self.decks[enemy]):
                    log("End of remove_all_health_trackers (nothing done)")
                    return

                self.decks[enemy]["healthMod"] = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}

                for d in self.decks[enemy]["healthTrackers"]:
                    d.image = None
                    d.config(image="")

                log("End of remove_all_health_trackers")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def display_last_card_drawn(self, event=None):
            try:
                log("Start of display_last_card_drawn")

                tree = event.widget
                selection = tree.selection()[0]

                # Remove keyword tooltips from the previous image shown, if there are any.
                for tooltip in self.app.tooltips:
                    tooltip.destroy()

                # Remove the displayed item.
                clear_other_tab_images(
                    self.app,
                    "behaviorDeck",
                    "behaviorDeck",
                    name=selection[:selection.index(" - ")] if " - " in selection else selection[:selection.index("_")] if "_" in selection else selection,
                    onlyDisplay=self.app.display)

                if selection not in self.decks or not self.decks[selection]["lastCardDrawn"]:
                    log("End of draw_behavior_card (nothing done)")
                    return
                
                if selection == "Armorer Dennis" and self.decks[selection]["heatup"]:
                    self.app.variantsTab.load_variant_card_locked(variant=self.decks[selection]["lastCardDrawn"], armorerDennis=True, fromDeck=True)
                if selection == "Old Iron King" and self.decks[selection]["heatup"]:
                    self.app.variantsTab.load_variant_card_locked(variant=self.decks[selection]["lastCardDrawn"], oldIronKing=True, fromDeck=True)
                else:
                    self.app.variantsTab.load_variant_card_locked(variant=self.decks[selection]["lastCardDrawn"], fromDeck=True)

                log("End of draw_behavior_card")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def heatup(self, selection=None, osOption=None):
            try:
                log("Start of heatup")

                if not selection:
                    selection = self.treeviewDecks.selection()[0]

                if (
                    not selection
                    or selection not in self.decks
                    or self.treeviewDecks.parent(selection) == "Enemies"
                    or selection == "Executioner Chariot"
                    or (selection == "Old Dragonslayer" and self.decks[selection]["heatup"] > 2)
                    or (selection == "The Four Kings" and self.decks[selection]["heatup"] > 3)
                    or (type(self.decks[selection]["heatup"]) == bool and self.decks[selection]["heatup"])
                    ):
                    log("End of heatup (nothing done)")
                    return
                
                p = PopupWindow(self.master, labelText="Really " + ("heat up" if selection != "The Four Kings" else "perform Royal Summons") + "?\nThis CANNOT be undone\nwithout completely resetting the deck!", yesButton=True, noButton=True)
                self.root.wait_window(p)

                if not p.answer:
                    log("End of heatup (clicked no)")
                    return
                
                # Remove keyword tooltips from the previous image shown, if there are any.
                for tooltip in self.app.tooltips:
                    tooltip.destroy()

                clear_other_tab_images(
                    self.app,
                    "behaviorDeck",
                    "behaviorDeck",
                    name=selection[:selection.index(" - ")] if " - " in selection else selection[:selection.index("_")] if "_" in selection else selection,
                    onlyDisplay=self.app.display)
                
                self.app.display.config(image="")
                self.app.display.image=None
                self.app.displayImages["variantsLocked"][self.app.display]["image"] = None
                self.app.displayImages["variantsLocked"][self.app.display]["name"] = None
                self.app.displayImages["variantsLocked"][self.app.display]["activeTab"] = None
                self.decks[selection]["lastCardDrawn"] = None

                if selection == "Ornstein & Smough":
                    healthOrnstein = behaviorDetail[selection]["Ornstein"]["health"]
                    healthSmough = behaviorDetail[selection]["Smough"]["health"]
                    healthBonusOrnstein = get_health_bonus(healthOrnstein, self.decks[selection]["defKey"])
                    healthBonusSmough = get_health_bonus(healthSmough, self.decks[selection]["defKey"])
                else:
                    health = behaviorDetail[selection[:selection.index(" (")] if "Vordt" in selection else selection]["health"]
                    healthBonus = get_health_bonus(health, self.decks[selection]["defKey"])

                heatup = "Yes"

                if selection == "Maldron the Assassin":
                    self.decks[selection]["healthMod"] += 8 + healthBonus
                    if self.decks[selection]["healthMod"] > 0:
                        self.decks[selection]["healthMod"] = 0
                    self.decks[selection]["heatup"] = True
                elif selection == "Oliver the Collector":
                    self.decks[selection]["deck"] = self.decks[selection]["heatupCards"]
                    self.decks[selection]["heatup"] = True
                elif selection == "Old Dragonslayer":
                    self.decks[selection]["deck"] += [self.decks[selection]["heatupCards"].pop()]
                    self.decks[selection]["heatup"] += 1
                    heatup = self.decks[selection]["heatup"]
                elif selection == "Artorias":
                    shuffle(self.decks[selection]["deck"])
                    self.decks[selection]["deck"] = self.decks[selection]["deck"][:-2]
                    self.decks[selection]["deck"] += self.decks[selection]["heatupCards"]
                    self.decks[selection]["heatup"] = True
                elif selection == "Ornstein & Smough":
                    if not osOption:
                        p = PopupWindow(self.master, labelText="Which one is heating up?", ornsteinButton=True, smoughButton=True)
                        self.root.wait_window(p)
                        osOption = "Ornstein" if p.answer else "Smough"

                    self.decks[selection]["deck"] = self.decks[selection]["heatupCards"][osOption]
                    self.decks[selection]["heatup"] = True

                    if osOption == "Ornstein":
                        self.decks[selection]["healthMod"]["Ornstein"] += 10 + healthBonusOrnstein
                        if self.decks[selection]["healthMod"]["Ornstein"] > 0:
                            self.decks[selection]["healthMod"]["Ornstein"] = 0
                        self.decks[selection]["healthMod"]["Smough"] = -(behaviorDetail[selection]["Smough"]["health"] + healthBonusSmough)
                    else:
                        self.decks[selection]["healthMod"]["Smough"] += 15 + healthBonusSmough
                        if self.decks[selection]["healthMod"]["Smough"] > 0:
                            self.decks[selection]["healthMod"]["Smough"] = 0
                        self.decks[selection]["healthMod"]["Ornstein"] = -(
                            behaviorDetail[selection]["Ornstein"]["health"] + healthBonusOrnstein)
                elif selection == "Smelter Demon":
                    self.decks[selection]["deck"] = self.decks[selection]["heatupCards"]
                    self.decks[selection]["heatup"] = True
                elif selection == "Guardian Dragon":
                    self.decks[selection]["deck"] += self.decks[selection]["heatupCards"]
                    self.decks[selection]["heatup"] = True
                elif selection == "The Four Kings":
                    self.decks[selection]["heatup"] += 1
                    shuffle(self.decks[selection]["deck"])
                    self.decks[selection]["deck"].pop()
                    self.decks[selection]["deck"] += sample(self.decks[selection]["heatupCards"][self.decks[selection]["heatup"]], 2)
                    heatup = self.decks[selection]["heatup"] - 1
                elif selection == "The Last Giant":
                    self.decks[selection]["deck"] = list(set(self.decks[selection]["deck"]) - set([b for b in behaviors[selection] if behaviorDetail[selection][b].get("arm", False)]))
                    self.decks[selection]["deck"] += self.decks[selection]["heatupCards"]
                else:
                    self.decks[selection]["deck"] += self.decks[selection]["heatupCards"]
                    self.decks[selection]["heatup"] = True
                
                shuffle(self.decks[selection]["deck"])
                self.decks[selection]["curIndex"] = 0
                self.decks[selection]["lastCardDrawn"] = None

                self.treeviewDecks.item(selection, values=(
                    self.treeviewDecks.item(selection)["values"][0],
                    len(self.decks[selection]["deck"]) - self.decks[selection]["curIndex"],
                    heatup))

                if selection in {"Maldron the Assassin", "Ornstein & Smough", "The Four Kings"}:
                    self.display_deck_cards()

                log("End of heatup")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def lower_health(self, amount, event=None):
            try:
                log("Start of lower_health")

                if self.app.notebook.tab(self.app.notebook.select(), "text") != "Behavior Decks":
                    log("End of lower_health (wrong tab)")
                    return

                selection = self.treeviewDecks.selection()[0]

                if selection == "The Four Kings" or selection not in behaviors:
                    log("End of lower_health (wrong tab)")
                    return

                selectionGeneric = selection[:selection.index(" (")] if "Vordt" in selection else selection
                modSelection = self.decks[selectionGeneric]["defKey"]
                osClicked = "Ornstein" if event.widget == self.app.display2 else "Smough" if event.widget == self.app.display3 else ""

                health = (
                    behaviorDetail[selectionGeneric].get("health", 0)
                    + behaviorDetail[selectionGeneric].get(osClicked, {}).get("health", 0)
                )

                healthBonus = get_health_bonus(health, modSelection)

                startingHealth = (
                    (self.decks[selection]["healthMod"][osClicked] if selection == "Ornstein & Smough" else self.decks[selection]["healthMod"])
                    + health
                    + healthBonus
                    )

                if startingHealth == 0:
                    log("End of lower_health (nothing done)")
                    return
                elif startingHealth - amount < 0:
                    amount = startingHealth

                if "Vordt" in selection:
                    self.decks["Vordt of the Boreal Valley (move)"]["healthMod"] -= amount
                    self.decks["Vordt of the Boreal Valley (attack)"]["healthMod"] -= amount
                elif selection == "Ornstein & Smough":
                    self.decks[selection]["healthMod"][osClicked] -= amount
                else:
                    self.decks[selection]["healthMod"] -= amount

                currentHealth = (
                    (self.decks[selection]["healthMod"][osClicked] if self.treeviewDecks.selection()[0] == "Ornstein & Smough" else self.decks[selection]["healthMod"])
                    + health
                    + healthBonus
                )

                if currentHealth == 0 and selection == "Paladin Leeroy" and not self.decks[selection]["healingTalisman"]:
                    p = PopupWindow(self.master, labelText="Use Healing Talisman?\nThis will not trigger again if you click yes (until reset).", yesButton=True, noButton=True)
                    self.root.wait_window(p)

                    if p.answer:
                        self.decks[selection]["healingTalisman"] = True
                        self.decks[selection]["healthMod"] += 2 + healthBonus

                self.app.variantsTab.load_variant_card_locked(variant=(selectionGeneric) + " - data", deckDataCard=True, healthMod=self.decks[selection]["healthMod"], fromDeck=True)

                heatupPoint = -1
                heatupPointVordt1 = -1
                heatupPointVordt2 = -1

                if "Vordt" in selection:
                    heatupPointVordt1 = (
                        behaviorDetail["Vordt of the Boreal Valley"]["heatup1"]
                        + healthBonus
                    )
                    heatupPointVordt2 = (
                        behaviorDetail["Vordt of the Boreal Valley"]["heatup2"]
                        + healthBonus
                    )
                elif selection == "Ornstein & Smough":
                    heatupPoint = 0
                else:
                    heatupPoint = (
                        behaviorDetail[selection].get("heatup", 0)
                        + (1000 if "heatup" not in behaviorDetail[selection] else 0)
                        + healthBonus
                    )

                if startingHealth > heatupPoint and currentHealth <= heatupPoint and not self.decks[selection]["heatup"]:
                    self.heatup(selection, osOption=("Ornstein" if osClicked == "Smough" else "Smough") if osClicked else None)
                elif startingHealth > heatupPointVordt1 and currentHealth <= heatupPointVordt1 and not self.decks["Vordt of the Boreal Valley (attack)"]["heatup"]:
                    self.heatup("Vordt of the Boreal Valley (attack)")
                elif startingHealth > heatupPointVordt2 and currentHealth <= heatupPointVordt2 and not self.decks["Vordt of the Boreal Valley (move)"]["heatup"]:
                    self.heatup("Vordt of the Boreal Valley (move)")

                log("End of lower_health")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def raise_health(self, amount, event=None):
            try:
                log("Start of raise_health")

                if self.app.notebook.tab(self.app.notebook.select(), "text") != "Behavior Decks":
                    log("End of raise_health (wrong tab)")
                    return

                selection = self.treeviewDecks.selection()[0]

                if selection not in behaviors:
                    log("End of raise_health (nothing done)")
                    return

                osClicked = "Ornstein" if event.widget == self.app.display2 else "Smough" if event.widget == self.app.display3 else ""

                if (
                    selection == "The Four Kings"
                    or (self.decks[selection]["healthMod"][osClicked] if selection == "Ornstein & Smough" else self.decks[selection]["healthMod"]) == 0
                    ):
                    log("End of raise_health (nothing done)")
                    return
                elif (self.decks[selection]["healthMod"][osClicked] if selection == "Ornstein & Smough" else self.decks[selection]["healthMod"]) + amount > 0:
                    amount = -(self.decks[selection]["healthMod"][osClicked] if selection == "Ornstein & Smough" else self.decks[selection]["healthMod"])

                if "Vordt" in selection:
                    self.decks["Vordt of the Boreal Valley (move)"]["healthMod"] += amount
                    self.decks["Vordt of the Boreal Valley (attack)"]["healthMod"] += amount
                    selection = selection[:selection.index(" (")] if "Vordt" in selection else selection
                elif selection == "Ornstein & Smough":
                    self.decks[selection]["healthMod"][osClicked] += amount
                else:
                    self.decks[selection]["healthMod"] += amount

                self.app.variantsTab.load_variant_card_locked(variant=selection + " - data", deckDataCard=True, healthMod=self.decks[self.treeviewDecks.selection()[0]]["healthMod"], fromDeck=True)

                log("End of raise_health")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def lower_health_king(self, amount, king, event=None):
            try:
                log("Start of lower_health_king")

                if self.app.notebook.tab(self.app.notebook.select(), "text") != "Behavior Decks":
                    log("End of lower_health_king (wrong tab)")
                    return

                selection = self.treeviewDecks.selection()[0]

                if selection != "The Four Kings" or king > self.decks["The Four Kings"]["heatup"]:
                    log("End of lower_health_king (nothing done)")
                    return
                
                modSelection = self.decks["The Four Kings"]["defKey"] if self.decks["The Four Kings"]["defKey"] else "The Four Kings"

                startingHealth = (
                    behaviorDetail[selection]["health"]
                    + get_health_bonus(25, [] if modSelection == selection else modSelection)
                    + self.decks[selection]["healthMod"][king]
                    )

                if startingHealth == 0:
                    log("End of lower_health_king (nothing done)")
                    return
                
                if startingHealth - amount < 0:
                    amount = startingHealth

                self.decks[selection]["healthMod"][king] -= amount

                self.four_kings_health_track(king, healthMod=self.decks[selection]["healthMod"][king])

                log("End of lower_health_king")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def raise_health_king(self, amount, king, event=None):
            try:
                log("Start of raise_health_king")

                if self.app.notebook.tab(self.app.notebook.select(), "text") != "Behavior Decks":
                    log("End of raise_health_king (wrong tab)")
                    return

                selection = self.treeviewDecks.selection()[0]

                if (
                    selection != "The Four Kings"
                    or self.decks[selection]["healthMod"][king] == 0
                    or king > self.decks["The Four Kings"]["heatup"]
                    ):
                    log("End of raise_health_king (nothing done)")
                    return
                elif self.decks[selection]["healthMod"][king] + amount > 0:
                    amount = -(self.decks[selection]["healthMod"][king])

                self.decks[selection]["healthMod"][king] += amount

                self.four_kings_health_track(king, healthMod=self.decks[selection]["healthMod"][king])

                log("End of raise_health_king")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def lower_health_regular(self, amount, event=None):
            try:
                log("Start of lower_health_regular")

                if self.app.notebook.tab(self.app.notebook.select(), "text") != "Behavior Decks":
                    log("End of lower_health_regular (wrong tab)")
                    return

                selection = self.treeviewDecks.selection()[0]

                if self.treeviewDecks.parent(selection) != "Enemies":
                    log("End of lower_health_king (nothing done)")
                    return
                
                eventLabel = event.widget
                labelIndex = self.decks[selection]["healthTrackers"].index(eventLabel)
                
                modSelection = self.decks[selection]["defKey"] if self.decks[selection]["defKey"] else selection

                startingHealth = (
                    behaviorDetail[selection]["health"]
                    + get_health_bonus(behaviorDetail[selection]["health"], [] if modSelection == selection else modSelection)
                    + self.decks[selection]["healthMod"][labelIndex]
                    )

                if startingHealth == 0:
                    log("End of lower_health_king (nothing done)")
                    return
                
                if startingHealth - amount < 0:
                    amount = startingHealth

                self.decks[selection]["healthMod"][labelIndex] -= amount

                self.health_tracker(labelIndex=labelIndex)

                log("End of lower_health_king")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def raise_health_regular(self, amount, event=None):
            try:
                log("Start of raise_health_regular")

                if self.app.notebook.tab(self.app.notebook.select(), "text") != "Behavior Decks":
                    log("End of raise_health_regular (wrong tab)")
                    return

                selection = self.treeviewDecks.selection()[0]

                if self.treeviewDecks.parent(selection) != "Enemies":
                    log("End of lower_health_king (nothing done)")
                    return
                
                eventLabel = event.widget
                labelIndex = self.decks[selection]["healthTrackers"].index(eventLabel)

                if (
                    self.treeviewDecks.parent(selection) != "Enemies"
                    or self.decks[selection]["healthMod"][labelIndex] == 0
                    ):
                    log("End of raise_health_regular (nothing done)")
                    return
                elif self.decks[selection]["healthMod"][labelIndex] + amount > 0:
                    amount = -(self.decks[selection]["healthMod"][labelIndex])

                self.decks[selection]["healthMod"][labelIndex] += amount

                self.health_tracker(labelIndex=labelIndex)

                log("End of raise_health_regular")
            except Exception as e:
                error_popup(self.root, e)
                raise
    
except Exception as e:
    log(e, exception=True)
    raise
