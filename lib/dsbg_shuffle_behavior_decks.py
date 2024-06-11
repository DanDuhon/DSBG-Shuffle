try:
    import tkinter as tk
    from random import choice, sample, shuffle
    from tkinter import ttk

    from dsbg_shuffle_enemies import bosses, enemiesDict
    from dsbg_shuffle_behaviors import behaviorDetail, behaviors
    from dsbg_shuffle_utility import PopupWindow, error_popup, log
    from dsbg_shuffle_variants import dataCardMods


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
                    "lastCardDrawn": None
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
                self.treeviewDecks.insert(parent="", index="end", iid="Mega Bosses", values=("Mega Bosses", "", ""), tags=False)

                for enemy in sorted([enemy for enemy in enemiesDict if enemiesDict[enemy].expansions & self.app.availableExpansions and ("Phantoms" in enemiesDict[enemy].expansions or enemiesDict[enemy].name in {"Hungry Mimic", "Voracious Mimic"})]):
                    self.treeviewDecks.insert(parent="Invaders & Explorers Mimics", index="end", iid=enemy, values=("    " + enemy, enemiesDict[enemy].cards, "no"), tags=True)
                    
                for enemy in sorted([enemy for enemy in bosses if (
                    enemy != "Vordt of the Boreal Valley"
                    and (
                        bosses[enemy]["level"] == "Mega Boss"
                        or enemy == "Asylum Demon"
                        or bosses[enemy]["expansions"] & self.app.availableExpansions))]):
                    self.treeviewDecks.insert(parent=bosses[enemy]["level"] + "es", index="end", iid=enemy, values=("    " + enemy, bosses[enemy]["cards"]), tags=True)

                if "Vordt of the Boreal Valley" in self.app.availableExpansions:
                    self.treeviewDecks.insert(parent="Mega Bosses", index="end", iid="Vordt of the Boreal Valley (move)", values=("    Vordt of the Boreal Valley (move)", 3), tags=True)
                    self.treeviewDecks.insert(parent="Mega Bosses", index="end", iid="Vordt of the Boreal Valley (attack)", values=("    Vordt of the Boreal Valley (attack)", 4), tags=True)

                
                self.treeviewDecks.bind("<<TreeviewSelect>>", self.display_deck_cards)

                log("End of create_deck_treeview")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def load_deck(self, enemy):
            try:
                log("Start of load_deck")

                lookupName = enemy if "(" not in enemy else enemy[:enemy.index(" (")]

                behaviorsWithDupes = behaviors
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
                    deck = sample(nonHeatupCards, 3)
                elif "(attack)" in enemy: # Vordt
                    deck = sample(nonHeatupCards, 4)
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
                    self.app.display.config(image="")
                    self.app.display2.config(image="")

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
                    self.decks[enemy]["heatupCards"]["ornstein"] = ["Charged Bolt", "Charged Swiping Combo", "Electric Clash", "High Voltage", "Lightning Stab"]
                    self.decks[enemy]["heatupCards"]["smough"] = ["Charged Charge", "Electric Bonzai Drop", "Electric Hammer Smash", "Jumping Volt Slam", "Lightning Sweep"]
                    shuffle(self.decks[enemy]["heatupCards"]["ornstein"])
                    shuffle(self.decks[enemy]["heatupCards"]["smough"])
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
                
                if self.decks[selection]["curIndex"] == len(self.decks[selection]["deck"]):
                    self.decks[selection]["curIndex"] = 0

                variantSelection = (selection[:selection.index(" (")] if "Vordt" in selection else selection)
                cardToDraw = variantSelection + " - " + self.decks[selection]["deck"][self.decks[selection]["curIndex"]]
                
                if variantSelection in set([v[:v.index("_")] for v in self.app.variantsTab.lockedVariants]) and cardToDraw in set([v[:v.index("_")] for v in self.app.variantsTab.lockedVariants]):
                    variant = cardToDraw + choice([v[v.index("_"):] for v in self.app.variantsTab.lockedVariants if (
                        cardToDraw in v
                        and (self.decks[selection]["defKey"] == "" or set([int(x) for x in v[v.index("_")+1:].split(",")]).issuperset(set([int(x) for x in self.decks[selection]["defKey"].split(",")])))
                        and (self.decks[selection]["defKey"] != "" or not set([int(x) for x in v[v.index("_")+1:].split(",")]) & dataCardMods))])
                else:
                    variant = cardToDraw
                    
                if selection == "Armorer Dennis" and self.decks[selection]["heatup"]:
                    self.app.variantsTab.load_variant_card_locked(variant=variant, armorerDennis=True)
                elif selection == "Old Iron King" and self.decks[selection]["heatup"]:
                    self.app.variantsTab.load_variant_card_locked(variant=variant, oldIronKing=True)
                else:
                    self.app.variantsTab.load_variant_card_locked(variant=variant)
                
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

                tree = event.widget
                selection = tree.selection()[0]

                if selection in self.decks:
                    # Remove keyword tooltips from the previous image shown, if there are any.
                    for tooltip in self.app.tooltips:
                        tooltip.destroy()

                    # Remove the displayed item.
                    self.app.display.config(image="")
                    self.app.display2.config(image="")

                    self.app.variantsTab.load_variant_card_locked(variant=selection + " - data", deckDataCard=True)
                    if self.decks[selection]["lastCardDrawn"]:
                        self.app.variantsTab.load_variant_card_locked(variant=self.decks[selection]["lastCardDrawn"])

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
                self.app.display.config(image="")
                self.app.display2.config(image="")

                if selection not in self.decks or not self.decks[selection]["lastCardDrawn"]:
                    log("End of draw_behavior_card (nothing done)")
                    return
                
                if selection in set([i[:i.index("_")] for i in self.app.variantsTab.lockedVariants]):
                    pass
                else:
                    if selection == "Armorer Dennis" and self.decks[selection]["heatup"]:
                        self.app.variantsTab.load_variant_card_locked(variant=self.decks[selection]["lastCardDrawn"], armorerDennis=True)
                    if selection == "Old Iron King" and self.decks[selection]["heatup"]:
                        self.app.variantsTab.load_variant_card_locked(variant=self.decks[selection]["lastCardDrawn"], oldIronKing=True)
                    else:
                        self.app.variantsTab.load_variant_card_locked(variant=self.decks[selection]["lastCardDrawn"])

                log("End of draw_behavior_card")
            except Exception as e:
                error_popup(self.root, e)
                raise
                

        def heatup(self):
            try:
                log("Start of heatup")

                selection = self.treeviewDecks.selection()[0]

                if (
                    not selection
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
                self.app.display.config(image="")
                self.app.display2.config(image="")

                if selection == "Oliver the Collector":
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
                    p = PopupWindow(self.master, labelText="Who is heating up?", ornsteinButton=True, smoughButton=True)
                    self.root.wait_window(p)
                    self.decks[selection]["deck"] = self.decks[selection]["heatupCards"][p.answer]
                    self.decks[selection]["heatup"] = True
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
                    self.decks[selection]["deck"] += sample(self.decks[selection]["heatupCards"], 3)
                    self.decks[selection]["deck"] += ["Falling Slam"]
                else:
                    self.decks[selection]["deck"] += self.decks[selection]["heatupCards"]
                    self.decks[selection]["heatup"] = True
                
                shuffle(self.decks[selection]["deck"])
                self.decks[selection]["curIndex"] = 0
                self.decks[selection]["lastCardDrawn"] = None

                self.treeviewDecks.item(selection, values=(self.treeviewDecks.item(selection)["values"][0], len(self.decks[selection]["deck"]) - self.decks[selection]["curIndex"]))

                log("End of heatup")
            except Exception as e:
                error_popup(self.root, e)
                raise
    
except Exception as e:
    log(e, exception=True)
    raise
