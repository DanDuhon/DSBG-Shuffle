try:
    import tkinter as tk
    from copy import deepcopy
    from random import choice, sample, shuffle
    from tkinter import ttk

    from dsbg_shuffle_enemies import bosses, enemiesDict
    from dsbg_shuffle_behaviors import behaviorDetail, behaviors
    from dsbg_shuffle_utility import PopupWindow, clear_other_tab_images, error_popup, log
    from dsbg_shuffle_variants import dataCardMods, modIdLookup


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
            self.heatupButton = ttk.Button(self.deckTabButtonsFrame, text="Heatup", width=16, command=self.heatup)
            self.heatupButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.resetButton = ttk.Button(self.deckTabButtonsFrame, text="Reset Deck", width=16, command=self.set_decks)
            self.resetButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

            self.decks = (
                {k: [] for k in enemiesDict if k in behaviors}
                | {k: [] for k in bosses if "Vordt" not in k}
                | {"Vordt of the Boreal Valley (move)": []}
                | {"Vordt of the Boreal Valley (attack)": []}
                )
            
            for enemy in self.decks:
                if "Kings" in enemy:
                    pass
                self.decks[enemy] = {
                    "deck": [],
                    "curIndex": 0,
                    "custom": False,
                    "heatup": 0 if enemy in "Old Dragonslayer" else 1 if enemy == "The Four Kings" else False,
                    "lastCardDrawn": None,
                    "healthMod": {"Ornstein": 0, "Smough": 0} if enemy == "Ornstein & Smough" else 0
                    }
                
                if enemy == "Smelter Demon":
                    self.decks[enemy]["heatupCnt"] = 5
                elif enemy == "Ornstein & Smough":
                    self.decks[enemy]["heatupCnt"] = 5
                elif enemy == "Guardian Dragon":
                    self.decks[enemy]["heatupCnt"] = 7
                elif enemy == "The Last Giant":
                    self.decks[enemy]["heatupCnt"] = 6

            self.create_deck_treeview()
            
            for enemy in self.decks:
                if (
                    (enemy in bosses
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
                    columns=("Name", "Cards in Deck", "Heatup"),
                    yscrollcommand=self.scrollbarTreeviewDeck.set,
                    height=11 if self.root.winfo_screenheight() > 1000 else 9
                )

                self.treeviewDecks.pack(expand=True, fill="both")
                self.scrollbarTreeviewDeck.config(command=self.treeviewDecks.yview)

                self.treeviewDecks.column('#0', width=50)

                self.treeviewDecks.heading("Name", text="Name", anchor=tk.W)
                self.treeviewDecks.heading("Cards in Deck", text="Cards in Deck", anchor=tk.W)
                self.treeviewDecks.heading("Heatup", text="Heatup", anchor=tk.W)
                self.treeviewDecks.column("Name", anchor=tk.W, width=300)
                self.treeviewDecks.column("Cards in Deck", anchor=tk.W, width=90)
                self.treeviewDecks.column("Heatup", anchor=tk.W, width=90)
                
                if {"Phantoms", "Explorers"} & self.app.availableExpansions:
                    self.treeviewDecks.insert(parent="", index="end", iid="Invaders & Explorers Mimics", values=("Invaders & Explorers Mimics", "", ""), tags=False)
                self.treeviewDecks.insert(parent="", index="end", iid="Mini Bosses", values=("Mini Bosses", "", ""), tags=False)
                self.treeviewDecks.insert(parent="", index="end", iid="Main Bosses", values=("Main Bosses", "", ""), tags=False)
                if set([boss for boss in bosses if bosses[boss]["level"] == "Mega Boss"]) & self.app.availableExpansions:
                    self.treeviewDecks.insert(parent="", index="end", iid="Mega Bosses", values=("Mega Bosses", "", ""), tags=False)

                for enemy in sorted([enemy for enemy in enemiesDict if enemiesDict[enemy].expansions & self.app.availableExpansions and ("Phantoms" in enemiesDict[enemy].expansions or enemiesDict[enemy].name in {"Hungry Mimic", "Voracious Mimic"})]):
                    self.treeviewDecks.insert(parent="Invaders & Explorers Mimics", index="end", iid=enemy, values=("    " + enemy, enemiesDict[enemy].cards, "no"), tags=True)
                    
                for enemy in sorted([enemy for enemy in bosses if (
                    bosses[enemy]["expansions"] & self.app.availableExpansions
                    and enemy != "Vordt of the Boreal Valley"
                    )]):
                    self.treeviewDecks.insert(parent=bosses[enemy]["level"] + "es", index="end", iid=enemy, values=("    " + enemy, bosses[enemy]["cards"]), tags=True)

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

                if not skipClear:
                    # Remove keyword tooltips from the previous image shown, if there are any.
                    for tooltip in self.app.tooltips:
                        tooltip.destroy()

                    # Remove the displayed item.
                    clear_other_tab_images(self.app, "variants")

                if not enemy:
                    enemy = self.treeviewDecks.selection()[0]

                self.decks[enemy]["deck"] = self.load_deck(enemy)
                
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

                self.decks[enemy]["heatup"] = 0 if enemy in "Old Dragonslayer" else 1 if enemy == "The Four Kings" else False
                self.decks[enemy]["healthMod"] = {"Ornstein": 0, "Smough": 0} if enemy == "Ornstein & Smough" else 0
                self.decks[enemy]["curIndex"] = 0
                self.decks[enemy]["lastCardDrawn"] = None
                self.treeviewDecks.item(enemy, values=(self.treeviewDecks.item(enemy)["values"][0], len(self.decks[enemy]["deck"])))

                if (enemy[:enemy.index(" (")] if "Vordt" in enemy else enemy) in set([v[:v.index("_")] for v in self.app.variantsTab.lockedVariants]):
                    self.decks[enemy]["defKey"] = choice([v[v.index("_")+1:] for v in self.app.variantsTab.lockedVariants if "-" not in v])

                log("End of set_decks")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def draw_behavior_card(self):
            try:
                log("Start of draw_behavior_card")

                selection = self.treeviewDecks.selection()[0]

                if not selection:
                    log("End of draw_behavior_card (nothing done)")
                    return
                
                self.display_deck_cards()
                
                if self.decks[selection]["curIndex"] == len(self.decks[selection]["deck"]):
                    self.decks[selection]["curIndex"] = 0

                variantSelection = (selection[:selection.index(" (")] if "Vordt" in selection else selection)
                cardToDraw = variantSelection + " - " + self.decks[selection]["deck"][self.decks[selection]["curIndex"]]
                
                if variantSelection in set([v[:v.index("_")] for v in self.app.variantsTab.lockedVariants]) and cardToDraw in set([v[:v.index("_")] for v in self.app.variantsTab.lockedVariants]):
                    if not [v[v.index("_"):] for v in self.app.variantsTab.lockedVariants if (
                        cardToDraw in v
                        and (self.decks[selection]["defKey"] == "" or set([int(x) for x in v[v.index("_")+1:].split(",")]).issuperset(set([int(x) for x in self.decks[selection]["defKey"].split(",")])))
                        and (self.decks[selection]["defKey"] != "" or not set([int(x) for x in v[v.index("_")+1:].split(",")]) & dataCardMods))]:
                        pass
                    
                    variant = cardToDraw + choice([v[v.index("_"):] for v in self.app.variantsTab.lockedVariants if (
                        cardToDraw in v
                        and (self.decks[selection]["defKey"] == "" or set([int(x) for x in v[v.index("_")+1:].split(",")]).issuperset(set([int(x) for x in self.decks[selection]["defKey"].split(",")])))
                        and (self.decks[selection]["defKey"] != "" or not set([int(x) for x in v[v.index("_")+1:].split(",")]) & dataCardMods))])
                else:
                    variant = cardToDraw
                    
                if selection == "Armorer Dennis" and self.decks[selection]["heatup"]:
                    self.app.variantsTab.load_variant_card_locked(variant=variant, armorerDennis=True, fromDeck=True)
                elif selection == "The Pursuer" and self.decks[selection]["heatup"]:
                    self.app.variantsTab.load_variant_card_locked(variant=variant, pursuer=True, fromDeck=True)
                elif selection == "Old Iron King" and self.decks[selection]["heatup"]:
                    self.app.variantsTab.load_variant_card_locked(variant=variant, oldIronKing=True, fromDeck=True)
                else:
                    self.app.variantsTab.load_variant_card_locked(variant=variant, fromDeck=True)
                
                self.decks[selection]["lastCardDrawn"] = variant

                if selection == "Dancer of the Boreal Valley" and behaviorDetail["Dancer of the Boreal Valley"][self.decks[selection]["deck"][self.decks[selection]["curIndex"]]].get("heatup", False):
                    self.decks[selection]["curIndex"] = 0
                    shuffle(self.decks[selection]["deck"])
                else:
                    self.decks[selection]["curIndex"] += 1

                self.treeviewDecks.item(selection, values=(
                    self.treeviewDecks.item(selection)["values"][0],
                    len(self.decks[selection]["deck"]) - self.decks[selection]["curIndex"]))

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
                    clear_other_tab_images(self.app, "variants")

                    if self.decks[selection]["lastCardDrawn"]:
                        self.app.variantsTab.load_variant_card_locked(variant=self.decks[selection]["lastCardDrawn"], fromDeck=True)

                    if selection == "Ornstein & Smough":
                        self.app.variantsTab.load_variant_card_locked(variant="Ornstein - data", deckDataCard=True, healthMod=self.decks[self.treeviewDecks.selection()[0]]["healthMod"], fromDeck=True)
                        self.app.variantsTab.load_variant_card_locked(variant="Smough - data", deckDataCard=True, healthMod=self.decks[self.treeviewDecks.selection()[0]]["healthMod"], fromDeck=True)
                    else:
                        selection = selection[:selection.index(" (")] if "Vordt" in selection else selection
                        self.app.variantsTab.load_variant_card_locked(variant=selection + " - data", deckDataCard=True, healthMod=self.decks[self.treeviewDecks.selection()[0]]["healthMod"], fromDeck=True)

                    self.app.display2.bind("<Button 1>", lambda event, x=1: self.lower_health(event=event, amount=x))
                    self.app.display2.bind("<Shift-Button 1>", lambda event, x=5: self.lower_health(event=event, amount=x))
                    self.app.display2.bind("<Button 3>", lambda event, x=1: self.raise_health(event=event, amount=x))
                    self.app.display2.bind("<Shift-Button 3>", lambda event, x=5: self.raise_health(event=event, amount=x))
                    self.app.display2.bind("<Control-1>", lambda event, x=1: self.raise_health(event=event, amount=x))
                    self.app.display2.bind("<Shift-Control-1>", lambda event, x=5: self.raise_health(event=event, amount=x))

                    if selection == "Ornstein & Smough":
                        self.app.display3.bind("<Button 1>", lambda event, x=1: self.lower_health(event=event, amount=x))
                        self.app.display3.bind("<Shift-Button 1>", lambda event, x=5: self.lower_health(event=event, amount=x))
                        self.app.display3.bind("<Button 3>", lambda event, x=1: self.raise_health(event=event, amount=x))
                        self.app.display3.bind("<Shift-Button 3>", lambda event, x=5: self.raise_health(event=event, amount=x))
                        self.app.display3.bind("<Control-1>", lambda event, x=1: self.raise_health(event=event, amount=x))
                        self.app.display3.bind("<Shift-Control-1>", lambda event, x=5: self.raise_health(event=event, amount=x))

                log("End of display_deck_cards")
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
                clear_other_tab_images(self.app, "variants", onlyDisplay=self.app.display)

                if selection not in self.decks or not self.decks[selection]["lastCardDrawn"]:
                    log("End of draw_behavior_card (nothing done)")
                    return
                
                if selection in set([i[:i.index("_")] for i in self.app.variantsTab.lockedVariants]):
                    pass
                else:
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
                    or selection == "Executioner Chariot"
                    or (selection == "Old Dragonslayer" and self.decks[selection]["heatup"] > 2)
                    or (selection == "The Four Kings" and self.decks[selection]["heatup"] > 3)
                    or (type(self.decks[selection]["heatup"]) == bool and self.decks[selection]["heatup"])
                    ):
                    log("End of heatup (nothing done)")
                    return
                
                p = PopupWindow(self.master, labelText="Really heat up?\nThis CANNOT be undone\nwithout completely resetting the deck!", yesButton=True, noButton=True)
                self.root.wait_window(p)

                if not p.answer:
                    log("End of heatup (clicked no)")
                    return
                
                # Remove keyword tooltips from the previous image shown, if there are any.
                for tooltip in self.app.tooltips:
                    tooltip.destroy()

                # Remove the displayed item.
                clear_other_tab_images(self.app, "variants", onlyDisplay=self.app.display)

                if selection == "Maldron the Assassin":
                    self.decks[selection]["healthMod"] += 8 + ([int(modIdLookup[m][-1]) for m in list(self.app.variantsTab.currentVariants[selection]["defKey"]) if "health" in modIdLookup[m]][0] if selection in self.app.variantsTab.currentVariants else 0)
                    if self.decks[selection]["healthMod"] > 0:
                        self.decks[selection]["healthMod"] = 0
                    self.decks[selection]["heatup"] = True
                elif selection == "Oliver the Collector":
                    self.decks[selection]["deck"] = self.decks[selection]["heatupCards"]
                    self.decks[selection]["heatup"] = True
                elif selection == "Old Dragonslayer":
                    self.decks[selection]["deck"] += [self.decks[selection]["heatupCards"].pop()]
                    self.decks[selection]["heatup"] += 1
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

                    healthVariant = + ([int(modIdLookup[m][-1]) for m in list(self.app.variantsTab.currentVariants[selection]["defKey"]) if "health" in modIdLookup[m]][0] if (selection) in self.app.variantsTab.currentVariants else 0)

                    if osOption == "Ornstein":
                        self.decks[selection]["healthMod"]["Ornstein"] += 10 + healthVariant
                        if self.decks[selection]["healthMod"]["Ornstein"] > 0:
                            self.decks[selection]["healthMod"]["Ornstein"] = 0
                        self.decks[selection]["healthMod"]["Smough"] = -(behaviorDetail[selection]["Smough"]["health"] + healthVariant)
                    else:
                        self.decks[selection]["healthMod"]["Smough"] += 15 + healthVariant
                        if self.decks[selection]["healthMod"]["Smough"] > 0:
                            self.decks[selection]["healthMod"]["Smough"] = 0
                        self.decks[selection]["healthMod"]["Ornstein"] = -(
                            behaviorDetail[selection]["Ornstein"]["health"] + healthVariant)
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
                elif selection == "The Last Giant":
                    self.decks[selection]["deck"] = list(set(self.decks[selection]["deck"]) - set([b for b in behaviors[selection] if behaviorDetail[selection][b].get("arm", False)]))
                    self.decks[selection]["deck"] += self.decks[selection]["heatupCards"]
                else:
                    self.decks[selection]["deck"] += self.decks[selection]["heatupCards"]
                    self.decks[selection]["heatup"] = True
                
                shuffle(self.decks[selection]["deck"])
                self.decks[selection]["curIndex"] = 0
                self.decks[selection]["lastCardDrawn"] = None

                self.treeviewDecks.item(selection, values=(self.treeviewDecks.item(selection)["values"][0], len(self.decks[selection]["deck"]) - self.decks[selection]["curIndex"]))

                if selection in {"Maldron the Assassin", "Ornstein & Smough"}:
                    self.display_deck_cards()

                log("End of heatup")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def lower_health(self, amount, event=None):
            try:
                log("Start of lower_health")

                if self.app.notebook.tab(self.app.notebook.select(), "text") != "Behavior Decks":
                    log("End of lower_health (nothing done)")
                    return

                selection = self.treeviewDecks.selection()[0]

                osClicked = "Ornstein" if event.widget == self.app.display2 else "Smough" if event.widget == self.app.display3 else ""

                startingHealth = ((self.decks[selection]["healthMod"][osClicked] if selection == "Ornstein & Smough" else self.decks[selection]["healthMod"])
                    + behaviorDetail[selection[:selection.index(" (")] if "Vordt" in selection else selection].get("health", 0)
                    + behaviorDetail[selection[:selection.index(" (")] if "Vordt" in selection else selection].get(osClicked, {}).get("health", 0)
                    + ([int(modIdLookup[m][-1]) for m in list(self.app.variantsTab.currentVariants[selection[:selection.index(" (")] if "Vordt" in selection else selection]["defKey"]) if "health" in modIdLookup[m]][0] if (selection[:selection.index(" (")] if "Vordt" in selection else selection) in self.app.variantsTab.currentVariants else 0)
                    )

                if selection == "The Four Kings" or startingHealth == 0:
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

                self.app.variantsTab.load_variant_card_locked(variant=(selection[:selection.index(" (")] if "Vordt" in selection else selection) + " - data", deckDataCard=True, healthMod=self.decks[self.treeviewDecks.selection()[0]]["healthMod"], fromDeck=True)

                currentHealth = (
                    (self.decks[selection]["healthMod"][osClicked] if selection == "Ornstein & Smough" else self.decks[selection]["healthMod"])
                    + behaviorDetail[selection[:selection.index(" (")] if "Vordt" in selection else selection].get("health", 0)
                    + behaviorDetail[selection[:selection.index(" (")] if "Vordt" in selection else selection].get(osClicked, {}).get("health", 0)
                    + ([int(modIdLookup[m][-1]) for m in list(self.app.variantsTab.currentVariants[selection[:selection.index(" (")] if "Vordt" in selection else selection]["defKey"]) if "health" in modIdLookup[m]][0] if (selection[:selection.index(" (")] if "Vordt" in selection else selection) in self.app.variantsTab.currentVariants else 0)
                )

                heatupPoint = -1
                heatupPointVordt1 = -1
                heatupPointVordt2 = -1

                if "Vordt" in selection:
                    heatupPointVordt1 = (
                        behaviorDetail["Vordt of the Boreal Valley"]["heatup1"]
                        + ([int(modIdLookup[m][-1]) for m in list(self.app.variantsTab.currentVariants["Vordt of the Boreal Valley"]["defKey"]) if "health" in modIdLookup[m]][0] if "Vordt of the Boreal Valley" in self.app.variantsTab.currentVariants else 0)
                    )
                    heatupPointVordt2 = (
                        behaviorDetail["Vordt of the Boreal Valley"]["heatup2"]
                        + ([int(modIdLookup[m][-1]) for m in list(self.app.variantsTab.currentVariants["Vordt of the Boreal Valley"]["defKey"]) if "health" in modIdLookup[m]][0] if "Vordt of the Boreal Valley" in self.app.variantsTab.currentVariants else 0)
                    )
                elif selection == "Ornstein & Smough":
                    heatupPoint = 0
                else:
                    heatupPoint = (
                        behaviorDetail[selection].get("heatup", 0)
                        + (1000 if "heatup" not in behaviorDetail[selection] else 0)
                        + ([int(modIdLookup[m][-1]) for m in list(self.app.variantsTab.currentVariants[selection]["defKey"]) if "health" in modIdLookup[m]][0] if selection in self.app.variantsTab.currentVariants else 0)
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
                    log("End of raise_health (nothing done)")
                    return

                selection = self.treeviewDecks.selection()[0]

                osClicked = "Ornstein" if event.widget == self.app.display2 else "Smough" if event.widget == self.app.display3 else ""

                if (
                    selection == "The Four Kings"
                    or (self.decks[selection]["healthMod"][osClicked] if selection == "Ornstein & Smough" else self.decks[selection]["healthMod"]) == 0
                    ):
                    log("End of raise_health (nothing done)")
                    return
                elif self.decks[selection]["healthMod"][osClicked] if selection == "Ornstein & Smough" else self.decks[selection]["healthMod"] + amount > 0:
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
    
except Exception as e:
    log(e, exception=True)
    raise
