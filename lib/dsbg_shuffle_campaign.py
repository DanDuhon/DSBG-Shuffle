try:
    import os
    import tkinter as tk
    from fpdf import FPDF
    from json import dump, load
    from PIL import Image, ImageTk
    from random import choice
    from tkinter import filedialog, ttk

    from dsbg_shuffle_enemies import bosses
    from dsbg_shuffle_events import events
    from dsbg_shuffle_utility import PopupWindow, clear_other_tab_images, error_popup, log, baseFolder, pathSep


    class CampaignFrame(ttk.Frame):
        def __init__(self, app, root):
            super(CampaignFrame, self).__init__()
            self.app = app
            self.root = root
            
            self.campaign = []

            self.v2Campaign = {
                1: [],
                2: [],
                3: [],
                4: []
            }

            self.bossMenuItems = [
                "Select Boss",
                "--Mini Bosses--"
                ]
            for boss in [boss for boss in bosses if bosses[boss]["level"] == "Mini Boss" and bosses[boss]["expansions"] & self.app.availableExpansions]:
                self.bossMenuItems.append(bosses[boss]["name"])

            self.bossMenuItems.append("--Main Bosses--")
            for boss in [boss for boss in bosses if bosses[boss]["level"] == "Main Boss" and bosses[boss]["expansions"] & self.app.availableExpansions]:
                self.bossMenuItems.append(bosses[boss]["name"])

            self.bossMenuItems.append("--Mega Bosses--")
            for boss in [boss for boss in bosses if bosses[boss]["level"] == "Mega Boss" and bosses[boss]["expansions"] & self.app.availableExpansions]:
                self.bossMenuItems.append(bosses[boss]["name"])

            self.selectedBoss = tk.StringVar()

            self.campaignTabButtonsFrame = ttk.Frame(self)
            self.campaignTabButtonsFrame.pack()
            self.campaignTabButtonsFrame2 = ttk.Frame(self)
            self.campaignTabButtonsFrame2.pack()
            self.campaignTabButtonsFrame3 = ttk.Frame(self)
            self.campaignTabButtonsFrame3.pack()
            self.campaignTabButtonsFrame4 = ttk.Frame(self)
            self.campaignTabButtonsFrame4.pack()
            self.campaignTabButtonsFrame5 = ttk.Frame(self)
            self.campaignTabButtonsFrame5.pack()
            self.campaignTabTreeviewFrame = ttk.Frame(self)
            self.campaignTabTreeviewFrame.pack(fill="both", expand=True)

            self.deleteButton = ttk.Button(self.campaignTabButtonsFrame, text="Remove Card", width=16, command=self.delete_card_from_campaign)
            self.deleteButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.moveUpButton = ttk.Button(self.campaignTabButtonsFrame, text="Move Up", width=16, command=self.move_up)
            self.moveUpButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.moveDownButton = ttk.Button(self.campaignTabButtonsFrame, text="Move Down", width=16, command=self.move_down)
            self.moveDownButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            
            self.loadButton = ttk.Button(self.campaignTabButtonsFrame2, text="Load Campaign", width=16, command=self.load_campaign)
            self.loadButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.saveButton = ttk.Button(self.campaignTabButtonsFrame2, text="Save Campaign", width=16, command=self.save_campaign)
            self.saveButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.printEncounters = ttk.Button(self.campaignTabButtonsFrame2, text="Export to PDF", width=16, command=self.print_encounters)
            self.printEncounters.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

            self.randomMiniBossButton = ttk.Button(self.campaignTabButtonsFrame3, text="Add Mini Boss", width=16, command=lambda x="Mini Boss": self.add_random_boss_to_campaign(level=x))
            self.randomMiniBossButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.randomMiniBossButton = ttk.Button(self.campaignTabButtonsFrame3, text="Add Main Boss", width=16, command=lambda x="Main Boss": self.add_random_boss_to_campaign(level=x))
            self.randomMiniBossButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.randomMiniBossButton = ttk.Button(self.campaignTabButtonsFrame3, text="Add Mega Boss", width=16, command=lambda x="Mega Boss": self.add_random_boss_to_campaign(level=x))
            self.randomMiniBossButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

            self.bossMenu = ttk.Combobox(self.campaignTabButtonsFrame4, state="readonly", values=self.bossMenuItems, textvariable=self.selectedBoss)
            self.bossMenu.current(0)
            self.bossMenu.config(width=17)
            self.bossMenu.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.addBossButton = ttk.Button(self.campaignTabButtonsFrame4, text="Add Boss", width=16, command=self.add_boss_to_campaign)
            self.addBossButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

            self.v1CampaignButton = ttk.Button(self.campaignTabButtonsFrame5, text="V1 Campaign", width=16, command=self.v1_campaign)
            self.v1CampaignButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.v2CampaignButton = ttk.Button(self.campaignTabButtonsFrame5, text="V2 Campaign", width=16, command=self.v2_campaign)
            self.v2CampaignButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.gravestoneButton = ttk.Button(self.campaignTabButtonsFrame5, text="V2 Gravestone", width=16, command=self.v2_campaign_gravestone)
            self.gravestoneButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
        
            self.scrollbarTreeviewCampaign = ttk.Scrollbar(self.campaignTabTreeviewFrame)
            self.scrollbarTreeviewCampaign.pack(side="right", fill="y")
            self.create_campaign_treeview()


        def create_campaign_treeview(self):
            """
            Create the campaign treeview where users can see saved encounters they've selected.
            """
            try:
                log("Start of create_campaign_treeview")

                self.treeviewCampaign = ttk.Treeview(
                    self.campaignTabTreeviewFrame,
                    selectmode="extended",
                    columns=("Name", "Type", "Level"),
                    yscrollcommand=self.scrollbarTreeviewCampaign.set,
                    height=23 if self.root.winfo_screenheight() > 1000 else 14,
                    show=["headings"]
                )

                self.treeviewCampaign.pack(expand=True, fill="both")
                self.scrollbarTreeviewCampaign.config(command=self.treeviewCampaign.yview)

                self.treeviewCampaign.column("Name", anchor="w")
                self.treeviewCampaign.heading("Name", text="Name", anchor="w")
                self.treeviewCampaign.column("Type", anchor="w")
                self.treeviewCampaign.heading("Type", text="Type", anchor="w")
                self.treeviewCampaign.column("Level", anchor="w")
                self.treeviewCampaign.heading("Level", text="Level", anchor="w")

                self.treeviewCampaign.bind("<<TreeviewSelect>>", self.load_campaign_card)
                self.treeviewCampaign.bind("<Control-a>", lambda *args: self.treeviewCampaign.selection_add(self.treeviewCampaign.get_children()))

                log("End of create_campaign_treeview")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def add_card_to_campaign(self, event=None):
            """
            Adds an encounter card to the campaign, visible in the campaign treeview.
            """
            try:
                log("Start of add_card_to_campaign")

                if self.app.notebook.tab(self.app.notebook.select(), "text") == "Events":
                    if not self.app.eventTab.treeviewEventDeck.selection() and not self.app.eventTab.treeviewEventList.selection():
                        log("End of add_card_to_campaign (nothing done)")
                        return
                    
                    eventToAdd = self.app.eventTab.treeviewEventDeck.selection() if self.app.eventTab.treeviewEventDeck.selection() else self.app.eventTab.treeviewEventList.selection()
                    
                    # The underscore is used to denote multiple instances. Only the expansion parents don't have these.
                    # Also do nothing if you have multiple cards selected.
                    if len(eventToAdd) > 1 or "_" not in eventToAdd[0]:
                        log("End of add_card_to_campaign (nothing done)")
                        return
                    
                    eventToAdd = eventToAdd[0]

                    # Multiples need a different iid in the treeview, so append a number.
                    if eventToAdd + "_0" not in self.treeviewCampaign.get_children():
                        self.treeviewCampaign.insert(parent="", iid=eventToAdd + "_0", values=(eventToAdd[:eventToAdd.index("_")], "Event", ""), index="end")
                        iidSuffix = "_0"
                    else:
                        i = max([int(item[item.rindex("_") + 1:]) for item in self.treeviewCampaign.get_children() if item[:item.rindex("_")] == eventToAdd])
                        self.treeviewCampaign.insert(parent="", iid=eventToAdd + "_" + str(i+1), values=(eventToAdd[:eventToAdd.index("_")], "Event", ""), index="end")
                        iidSuffix = "_" + str(i+1)

                    # Build the dictionary that will be saved to JSON if this campaign is saved.
                    card = {
                        "type": "event",
                        "name": eventToAdd[:eventToAdd.index("_")],
                        "level": " ",
                        "iid": eventToAdd + iidSuffix
                    }

                    self.campaign.append(card)
                else:
                    if not self.app.selected:
                        log("End of add_card_to_campaign (nothing done)")
                        return

                    # Multiples need a different iid in the treeview, so append a number.
                    if self.app.selected["name"] + "_0" not in self.treeviewCampaign.get_children():
                        self.treeviewCampaign.insert(parent="", iid=self.app.selected["name"] + "_0", values=(self.app.selected["name"], "Encounter", self.app.selected["level"]), index="end")
                        iidSuffix = "_0"
                    else:
                        i = max([int(item[item.rindex("_") + 1:]) for item in self.treeviewCampaign.get_children() if item[:item.rindex("_")] == self.app.selected["name"]])
                        self.treeviewCampaign.insert(parent="", iid=self.app.selected["name"] + "_" + str(i+1), values=(self.app.selected["name"], "Encounter", self.app.selected["level"]), index="end")
                        iidSuffix = "_" + str(i+1)

                    # Build the dictionary that will be saved to JSON if this campaign is saved.
                    card = {
                        "type": "encounter",
                        "name": self.app.selected["name"] + (" (TSC)" if self.app.selected["expansion"] == "The Sunless City" and self.app.selected["name"] in set(["Broken Passageway", "Central Plaza"]) else ""),
                        "expansion": self.app.selected["expansion"],
                        "level": self.app.selected["level"],
                        "enemies": self.app.encounterTab.newEnemies,
                        "rewardTreasure": self.app.encounterTab.rewardTreasure,
                        "iid": self.app.selected["name"] + iidSuffix
                    }

                    self.campaign.append(card)

                log("End of add_card_to_campaign")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def add_card_to_v2_campaign_list(self, name, event=None):
            """
            Adds an encounter card to the v2 campaign generator list.
            """
            try:
                log("Start of add_card_to_v2_campaign_list")

                card = {
                    "type": "encounter",
                    "name": name,
                    "expansion": self.app.selected["expansion"],
                    "level": self.app.selected["level"],
                    "enemies": self.app.encounterTab.newEnemies,
                    "rewardTreasure": self.app.encounterTab.rewardTreasure
                }

                log("End of add_card_to_v2_campaign_list")

                return card
            except Exception as e:
                error_popup(self.root, e)
                raise


        def add_random_boss_to_campaign(self, level):
            """
            Adds a random boss to the campaign, visible in the campaign treeview.
            """
            try:
                log("Start of add_random_boss_to_campaign, level={}".format(str(level)))

                availableBosses = [boss for boss in bosses if bosses[boss]["level"] == level and bosses[boss]["expansions"] & self.app.availableExpansions]
                if not availableBosses:
                    log("End of add_random_boss_to_campaign (no bosses to choose from)")
                    return
                selectedBoss = choice(availableBosses)

                # Multiples need a different iid in the treeview, so append a number.
                if selectedBoss + "_0" not in self.treeviewCampaign.get_children():
                    self.treeviewCampaign.insert(parent="", iid=selectedBoss + "_0", values=(selectedBoss, "Boss", bosses[selectedBoss]["level"]), index="end")
                    iidSuffix = "_0"
                else:
                    i = max([int(item[item.rindex("_") + 1:]) for item in self.treeviewCampaign.get_children() if item[:item.rindex("_")] == selectedBoss])
                    self.treeviewCampaign.insert(parent="", iid=selectedBoss + "_" + str(i+1), values=(selectedBoss, "Boss", bosses[selectedBoss]["level"]), index="end")
                    iidSuffix = "_" + str(i+1)

                # Build the dictionary that will be saved to JSON if this campaign is saved.
                card = {
                    "name": selectedBoss,
                    "type": "boss",
                    "level": level,
                    "iid": selectedBoss + iidSuffix
                }

                self.campaign.append(card)

                log("End of add_random_boss_to_campaign")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def add_boss_to_campaign(self):
            """
            Adds a boss to the campaign, visible in the campaign treeview.
            """
            try:
                log("Start of add_boss_to_campaign")

                # If a menu item that isn't a boss (e.g. --Mini Boss--) is selected in the combobox, don't do anything.
                if self.selectedBoss.get() not in bosses:
                    log("End of add_boss_to_campaign (nothing done)")
                    return

                # Multiples need a different iid in the treeview, so append a number.
                if self.selectedBoss.get() + "_0" not in self.treeviewCampaign.get_children():
                    self.treeviewCampaign.insert(parent="", iid=self.selectedBoss.get() + "_0", values=(self.selectedBoss.get(), "Boss", bosses[self.selectedBoss.get()]["level"]), index="end")
                    iidSuffix = "_0"
                else:
                    i = max([int(item[item.rindex("_") + 1:]) for item in self.treeviewCampaign.get_children() if item[:item.rindex("_")] == self.selectedBoss.get()])
                    self.treeviewCampaign.insert(parent="", iid=self.selectedBoss.get() + "_" + str(i+1), values=(self.selectedBoss.get(), "Boss", bosses[self.selectedBoss.get()]["level"]), index="end")
                    iidSuffix = "_" + str(i+1)

                # Build the dictionary that will be saved to JSON if this campaign is saved.
                card = {
                    "name": self.selectedBoss.get(),
                    "type": "boss",
                    "level": bosses[self.selectedBoss.get()]["level"],
                    "iid": self.selectedBoss.get() + iidSuffix
                }

                self.campaign.append(card)

                log("End of add_boss_to_campaign")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def delete_card_from_campaign(self, event=None):
            """
            Delete a card from the campaign.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of delete_card_from_campaign")

                # If the button is clicked with no selection, do nothing.
                if not self.treeviewCampaign.selection():
                    log("End of delete_card_from_campaign (nothing done)")
                    return

                # Remove the deleted cards from the campaign list and treeview.
                for item in self.treeviewCampaign.selection():
                    self.campaign = [c for c in self.campaign if c["iid"] != item]
                    self.treeviewCampaign.delete(item)

                # Remove the image displaying a deleted card.
                clear_other_tab_images(self.app, "encounters", "campaign")
                clear_other_tab_images(self.app, "events", "campaign")

                log("End of delete_card_from_campaign")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def save_campaign(self):
            """
            Save the campaign to a JSON file that can be loaded later.
            """
            try:
                log("Start of save_campaign")

                # Prompt user to save the file.
                campaignName = filedialog.asksaveasfile(mode="w", initialdir=baseFolder + "\\lib\\dsbg_shuffle_saved_campaigns".replace("\\", pathSep), defaultextension=".json")

                # If they canceled it, do nothing.
                if not campaignName:
                    log("End of save_campaign (nothing done)")
                    return

                with open(campaignName.name, "w") as campaignFile:
                    dump(self.campaign, campaignFile)

                log("End of save_campaign (saved to " + str(campaignFile) + ")")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def load_campaign(self):
            """
            Load a campaign from a JSON file, clearing the current campaign treeview and replacing
            it with the data from the JSON file.
            """
            try:
                log("Start of load_campaign")

                # Prompt the user to find the campaign file.
                campaignFile = filedialog.askopenfilename(initialdir=baseFolder + "\\lib\\dsbg_shuffle_saved_campaigns".replace("\\", pathSep), filetypes = [(".json", ".json")])

                # If the user did not select a file, do nothing.
                if not campaignFile:
                    log("End of load_campaign (file dialog canceled)")
                    return

                # If the user did not select a JSON file, notify them that that was an invalid file.
                if os.path.splitext(campaignFile)[1] != ".json":
                    self.app.set_bindings_buttons_menus(False)
                    PopupWindow(self.root, labelText="Invalid DSBG-Shuffle campaign file.", firstButton="Ok")
                    self.app.set_bindings_buttons_menus(True)
                    log("End of load_campaign (invalid file)")
                    return

                log("Loading file " + campaignFile)

                with open(campaignFile, "r") as f:
                    self.campaign = load(f)

                # Check to see if there are any invalid names or levels in the JSON file.
                # This is about as sure as I can be that you can't load random JSON into the app.
                if any([(item["name"] not in self.app.encounters and item["name"] not in bosses and item["name"] not in events) or item["type"] not in set(["encounter", "boss", "event"]) or item["level"] not in set([1, 2, 3, 4, "Mini Boss", "Main Boss", "Mega Boss", " "]) for item in self.campaign]):
                    self.app.set_bindings_buttons_menus(False)
                    PopupWindow(self.root, labelText="Invalid DSBG-Shuffle campaign file.", firstButton="Ok")
                    self.app.set_bindings_buttons_menus(True)
                    self.campaign = []
                    log("End of load_campaign (invalid file)")
                    return

                # Remove existing campaign elements.
                for item in self.treeviewCampaign.get_children():
                    self.treeviewCampaign.delete(item)

                # Create the campaign from the campaign list.
                for item in self.campaign:
                    self.treeviewCampaign.insert(parent="", iid=item["iid"], values=(item["name"], item["type"][0].upper() + item["type"][1:], item["level"]), index="end")

                log("End of load_campaign (loaded from " + str(campaignFile) + ")")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def move_up(self):
            """
            Move an item up in the campaign treeview, with corresponding movement in the campaign list.
            """
            try:
                log("Start of move_up")

                leaves = self.treeviewCampaign.selection()
                for i in leaves:
                    self.treeviewCampaign.move(i, self.treeviewCampaign.parent(i), self.treeviewCampaign.index(i) - 1)
                    self.campaign.insert(self.treeviewCampaign.index(i) + 1, self.campaign.pop(self.treeviewCampaign.index(i)))

                log("End of move_up")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def move_down(self, leaves=None):
            """
            Move an item down in the campaign treeview, with corresponding movement in the campaign list.
            """
            try:
                log("Start of move_down")

                if not leaves:
                    leaves = self.treeviewCampaign.selection()
                for i in reversed(leaves):
                    self.treeviewCampaign.move(i, self.treeviewCampaign.parent(i), self.treeviewCampaign.index(i) + 1)
                    self.campaign.insert(self.treeviewCampaign.index(i) - 1, self.campaign.pop(self.treeviewCampaign.index(i)))

                log("End of move_down")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def load_campaign_card(self, event=None):
            """
            When an encounter in the campaign is clicked on, display the encounter
            and enemies that were originally saved.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of load_campaign_card")

                if self.app.notebook.tab(self.app.notebook.select(), "text") == "Campaign":
                    clear_other_tab_images(self.app, "encounters", "campaign")
                    clear_other_tab_images(self.app, "events", "campaign")

                self.app.selected = None
                self.app.encounterTab.rewardTreasure = None
                self.app.display.unbind("<Button 1>")

                tree = event.widget

                # Don't update the image shown if you've selected more than one card.
                if len(tree.selection()) != 1:
                    log("End of load_campaign_card (not updating image)")
                    return
                
                # Remove keyword tooltips from the previous card shown, if there are any.
                for tooltip in self.app.tooltips:
                    tooltip.destroy()

                # Get the card selected.
                campaignCard = [e for e in self.campaign if e["iid"] == tree.selection()[0]][0]

                if campaignCard["type"] == "encounter":
                    self.app.encounterTab.rewardTreasure = campaignCard.get("rewardTreasure")

                    log("\tOpening " + baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + campaignCard["name"] + str(self.app.numberOfCharacters) + ".json")

                    # Get the enemy slots for this card.
                    with open(baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + campaignCard["name"] + str(self.app.numberOfCharacters) + ".json") as alternativesFile:
                        alts = load(alternativesFile)

                    # Create the encounter card with saved enemies and tooltips.
                    self.app.encounterTab.newEnemies = campaignCard["enemies"]
                    self.app.encounterTab.edit_encounter_card(campaignCard["name"], campaignCard["expansion"], campaignCard["level"], alts["enemySlots"])
                elif campaignCard["type"] == "boss":
                    # Create and display the boss image.
                    self.app.create_image(campaignCard["name"] + ".jpg", "encounter", 4)
                    self.app.displayImages["encounters"][self.app.display]["image"] = ImageTk.PhotoImage(self.app.displayImage)
                    self.app.displayImages["encounters"][self.app.display]["activeTab"] = None
                    self.app.display.image = self.app.displayImages["encounters"][self.app.display]["image"]
                    self.app.display.config(image=self.app.displayImages["encounters"][self.app.display]["image"])
                elif campaignCard["type"] == "event":
                    self.app.eventTab.load_event(campaign=True, treeviewCampaign=tree)

                log("End of load_campaign_card")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def print_encounters(self):
            """
            Export campaign encounters to a PDF.
            """
            try:
                log("Start of print_encounters")

                self.forPrinting = True
                self.encountersToPrint = []
                campaignEncounters = [e for e in self.campaign if e["type"] == "encounter"]

                if not campaignEncounters:
                    log("End of print_encounters (nothing done)")
                    p = PopupWindow(self.root, "There are no encounter cards to print!", firstButton="Ok")
                    self.root.wait_window(p)
                    return

                for encounter in campaignEncounters:
                    # These are the card sizes in mm
                    if encounter["expansion"] in {
                        "Dark Souls The Board Game",
                        "Darkroot",
                        "Executioner Chariot",
                        "Explorers",
                        "Iron Keep",
                        "Asylum Demon",
                        "Black Dragon Kalameet",
                        "Gaping Dragon",
                        "Guardian Dragon",
                        "Manus, Father of the Abyss",
                        "Old Iron King",
                        "The Four Kings",
                        "The Last Giant",
                        "Vordt of the Boreal Valley"}:
                        if encounter["level"] == 4:
                            encounter["width"] = 63
                            encounter["height"] = 88
                        else:
                            encounter["width"] = 42
                            encounter["height"] = 63
                    else:
                        encounter["width"] = 70
                        encounter["height"] = 120

                # Add cards to a list associated with their type/size.
                encounterCount = 0
                eCount = 0
                v1Normal = []
                l = [e for e in campaignEncounters if e["type"] == "encounter" and e["width"] == 42]
                for i in range(0, len(l), 18):
                    v1Normal.append(l[i:i+18])
                    encounterCount += len(l[i:i+18])

                v1Level4 = []
                l = [e for e in campaignEncounters if e["type"] == "encounter" and e["width"] == 63]
                for i in range(0, len(l), 9):
                    v1Level4.append(l[i:i+9])
                    encounterCount += len(l[i:i+9])

                v2 = []
                l = [e for e in campaignEncounters if e["type"] == "encounter" and e["width"] == 70]
                for i in range(0, len(l), 6):
                    v2.append(l[i:i+6])
                    encounterCount += len(l[i:i+6])

                encountersToPrint = [v1Normal, v1Level4, v2]

                buffer = 5
                pdf = FPDF(unit="mm")
                pdf.set_margins(buffer, buffer, buffer)

                progress = PopupWindow(self.root, labelText="Creating PDF...", progressBar=True, progressMax=encounterCount, loadingImage=True)

                # Loop through the card lists and add them to pages.
                for e, encounterList in enumerate(encountersToPrint):
                    if e == 0:
                        standardCards = 11
                        columnBreaks = {3, 7, 11}
                    elif e == 1:
                        standardCards = 8
                        columnBreaks = {2, 5}
                    elif e == 2:
                        standardCards = 1
                        columnBreaks = {1}
                        buffer = 3

                    for page in encounterList:
                        pdf.add_page()
                        x = buffer
                        y = buffer
                        pdf.set_x(x)
                        pdf.set_y(y)

                        for i, encounter in enumerate(page):
                            # Get the encounter.
                            campaignEncounter = [e for e in self.campaign if e["name"] == encounter["name"]]
                            self.app.encounterTab.rewardTreasure = campaignEncounter[0].get("rewardTreasure")

                            log("\tOpening " + baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + campaignEncounter[0]["name"] + str(self.app.numberOfCharacters) + ".json")
                            # Get the enemy slots for this encounter.
                            with open(baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + campaignEncounter[0]["name"] + str(self.app.numberOfCharacters) + ".json") as alternativesFile:
                                alts = load(alternativesFile)

                            # Create the encounter card with saved enemies and tooltips.
                            self.app.encounterTab.newEnemies = campaignEncounter[0]["enemies"]
                            self.app.encounterTab.edit_encounter_card(campaignEncounter[0]["name"], campaignEncounter[0]["expansion"], campaignEncounter[0]["level"], alts["enemySlots"])

                            # Stage the encounter image
                            log("\tStaging " + encounter["name"] + ", level " + str(encounter["level"]) + " from " + encounter["expansion"])
                            imageStage = ImageTk.getimage(self.app.displayImages["encounters"][self.app.display]["image"])

                            if i > standardCards:
                                imageStage = imageStage.rotate(90, Image.NEAREST, expand=1)
                            imageStage.save(baseFolder + "\\lib\\dsbg_shuffle_image_staging\\".replace("\\", pathSep) + encounter["name"] + ".png")

                            log("\tAdding " + encounter["name"] + " to PDF at (" + str(x) + ", " + str(y) + ") with width of " + str(encounter["width" if not i > standardCards else "height"]))
                            pdf.image(baseFolder + "\\lib\\dsbg_shuffle_image_staging\\".replace("\\", pathSep) + encounter["name"] + ".png", x=x, y=y, type="PNG", w=encounter["width" if not i > standardCards else "height"])

                            if i < standardCards:
                                if i in columnBreaks:
                                    x += encounter["width"] + buffer
                                    y = buffer
                                else:
                                    y += encounter["height"] + buffer
                            elif i == standardCards:
                                x += encounter["width"] + buffer
                                y = buffer
                            else:
                                y += encounter["width"] + buffer

                            eCount += 1
                            progress.progressVar.set(eCount)
                            self.root.update_idletasks()

                progress.destroy()

                # Prompt user to save the file.
                pdfOutput = filedialog.asksaveasfile(mode="w", initialdir=baseFolder + "\\lib\\dsbg_shuffle_exports".replace("\\", pathSep), defaultextension=".pdf")

                # If they canceled it, do nothing.
                if not pdfOutput:
                    log("End of print_encounters (nothing done)")
                    return
                
                progress = PopupWindow(self.root, labelText="Saving PDF, please wait...", loadingImage=True)

                pdf.output(pdfOutput.name)

                progress.destroy()

                self.forPrinting = False

                log("End of print_encounters")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def v1_campaign(self, event=None):
            """
            Generates a random V1 campaign.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of v1_campaign")

                if self.campaign:
                    PopupWindow(self.root, labelText="Please remove all campaign items first.", firstButton="Ok")
                    return

                mega = False
                
                progress = PopupWindow(self.root, labelText="Generating encounters...", loadingImage=True)
                
                encounterList = [encounter for encounter in self.app.encounters if (
                    all([
                        any([frozenset(expCombo).issubset(self.app.availableExpansions) for expCombo in self.app.encounters[encounter]["expansionCombos"]["1"]]),
                        any([frozenset(expCombo).issubset(self.app.availableExpansions) for expCombo in self.app.encounters[encounter]["expansionCombos"]["2"]]),
                        True if "3" not in self.app.encounters[encounter]["expansionCombos"] else any([frozenset(expCombo).issubset(self.app.availableExpansions) for expCombo in self.app.encounters[encounter]["expansionCombos"]["3"]]),
                        self.app.encounters[encounter]["expansion"] in self.app.v1Expansions
                            ]))]

                self.add_random_boss_to_campaign(level="Mini Boss")
                self.add_random_boss_to_campaign(level="Main Boss")
                self.add_random_boss_to_campaign(level="Mega Boss")

                if len(self.campaign) == 3:
                    mega = True

                for level in bosses[self.campaign[0]["name"]]["encounters"]:
                    self.app.encounterTab.random_encounter(level=level, encounterList=encounterList)
                    self.add_card_to_campaign()

                for level in bosses[self.campaign[1]["name"]]["encounters"]:
                    self.app.encounterTab.random_encounter(level=level, encounterList=encounterList)
                    self.add_card_to_campaign()

                if mega:
                    for level in bosses[self.campaign[2]["name"]]["encounters"]:
                        self.app.encounterTab.random_encounter(level=level, encounterList=encounterList)
                        self.add_card_to_campaign()
                        
                    boss3 = (self.campaign[2]["name"] + "_0",)

                    for _ in range(9):
                        self.move_down(leaves=boss3)

                boss1 = (self.campaign[0]["name"] + "_0",)
                boss2 = (self.campaign[1]["name"] + "_0",)

                for _ in range(8):
                    self.move_down(leaves=boss2)

                for _ in range(4):
                    self.move_down(leaves=boss1)

                progress.destroy()

                log("End of v1_campaign")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def v2_campaign(self, event=None):
            """
            Generates a random V2 campaign, piece by piece.
            """
            try:
                log("Start of v2_campaign")

                level1Cnt = len([e for e in self.campaign if e["level"] == 1])

                if not self.campaign and level1Cnt > 0:
                    self.v2Campaign = {
                        1: [],
                        2: [],
                        3: [],
                        4: []
                    }
                elif [e for e in self.campaign if e["type"] != "event"] and level1Cnt == 0:
                    PopupWindow(self.root, labelText="Please remove all campaign items first.", firstButton="Ok")
                    return
                
                clear_other_tab_images(self.app, "encounters", "campaign")

                mega = self.generate_v2_campaign_encounters()

                if level1Cnt < 3:
                    self.v2_campaign_pick_encounter(1)
                    return

                if len([e for e in self.campaign if e["level"] == 2]) < 1:
                    self.v2_campaign_pick_encounter(2)
                    return
                
                if not [e for e in self.campaign if e["level"] == "Mini Boss"]:
                    self.add_random_boss_to_campaign(level="Mini Boss")
                    return

                if len([e for e in self.campaign if e["level"] == 2]) < 3:
                    self.v2_campaign_pick_encounter(2)
                    return

                if len([e for e in self.campaign if e["level"] == 3]) < 2:
                    self.v2_campaign_pick_encounter(3)
                    return
                
                if not [e for e in self.campaign if e["level"] == "Main Boss"]:
                    self.add_random_boss_to_campaign(level="Main Boss")
                    return

                if mega:
                    if len([e for e in self.campaign if e["level"] == 4]) < 1:
                        self.v2_campaign_pick_encounter(4)
                        return
                        
                    if not [e for e in self.campaign if e["level"] == "Mega Boss"]:
                        self.add_random_boss_to_campaign(level="Mega Boss")
                        return

                log("End of v2_campaign")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def v2_campaign_pick_encounter(self, level):
            """
            Prompts the user to choose which encounter to keep.
            """
            try:
                log("Start of generate_v2_campaign_encounters")

                if len(self.v2Campaign[level]) < 2:
                    self.generate_v2_campaign_encounters()

                leftEncounter = self.v2Campaign[level].pop()
                rightEncounter = self.v2Campaign[level].pop()

                self.load_v2_campaign_card(leftEncounter)
                self.load_v2_campaign_card(rightEncounter, True)
            
                p = PopupWindow(self.master, labelText="Which encounter do you want to play?", rightButton=True, leftButton=True)
                self.root.wait_window(p)
                
                clear_other_tab_images(self.app, "encounters", "campaign", self.app.display2)

                if p.answer:
                    self.load_v2_campaign_card(leftEncounter)
                else:
                    self.load_v2_campaign_card(rightEncounter)

                self.add_card_to_campaign()

                log("End of generate_v2_campaign_encounters")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def generate_v2_campaign_encounters(self):
            """
            Generate encounters for the v2 campaign generator.
            """
            try:
                log("Start of generate_v2_campaign_encounters")
                
                clear_other_tab_images(self.app, "encounters", "campaign")
                clear_other_tab_images(self.app, "events", "campaign")

                mega = True if any([boss for boss in bosses if (
                    bosses[boss]["level"] == "Mega Boss"
                    and bosses[boss]["expansions"] & self.app.availableExpansions)]) else False
                level1Cnt = len([e for e in self.campaign if e["level"] == 1])
                level2Cnt = len([e for e in self.campaign if e["level"] == 2])
                level3Cnt = len([e for e in self.campaign if e["level"] == 3])
                level4Cnt = len([e for e in self.campaign if e["level"] == 4])

                if (
                    (level1Cnt < 3 and len(self.v2Campaign[1]) < 2)
                    or (level2Cnt < 3 and len(self.v2Campaign[2]) < 2)
                    or (level3Cnt < 2 and len(self.v2Campaign[3]) < 2)
                    or (mega and level4Cnt < 1 and len(self.v2Campaign[4]) < 2)
                    ):
                    progress = PopupWindow(self.root, labelText="Generating encounters...", loadingImage=True)

                    if mega and level4Cnt < 1 and len(self.v2Campaign[4]) < 2:
                        encounterListLevel4 = [encounter for encounter in self.app.encounters if (
                            all([
                                any([frozenset(expCombo).issubset(self.app.availableExpansions) for expCombo in self.app.encounters[encounter]["expansionCombos"]["1"]]),
                                any([frozenset(expCombo).issubset(self.app.availableExpansions) for expCombo in self.app.encounters[encounter]["expansionCombos"]["2"]]),
                                True if "3" not in self.app.encounters[encounter]["expansionCombos"] else any([frozenset(expCombo).issubset(self.app.availableExpansions) for expCombo in self.app.encounters[encounter]["expansionCombos"]["3"]]),
                                self.app.encounters[encounter]["level"] == 4
                                    ]))]
                
                        self.v2_campaign_add_encounters(encounterListLevel4, 4, 1, 2)

                    if (
                        level1Cnt < 3
                        or level2Cnt < 3
                        or level3Cnt < 2
                        ):
                        encounterList = [encounter for encounter in self.app.encounters if (
                            all([
                                any([frozenset(expCombo).issubset(self.app.availableExpansions) for expCombo in self.app.encounters[encounter]["expansionCombos"]["1"]]),
                                any([frozenset(expCombo).issubset(self.app.availableExpansions) for expCombo in self.app.encounters[encounter]["expansionCombos"]["2"]]),
                                True if "3" not in self.app.encounters[encounter]["expansionCombos"] else any([frozenset(expCombo).issubset(self.app.availableExpansions) for expCombo in self.app.encounters[encounter]["expansionCombos"]["3"]]),
                                self.app.encounters[encounter]["expansion"] in self.app.v2Expansions
                                    ]))]

                        if len(self.v2Campaign[1]) < 2:
                            self.v2_campaign_add_encounters(encounterList, 1, 3, 6)

                        if len(self.v2Campaign[2]) < 2:
                            self.v2_campaign_add_encounters(encounterList, 2, 3, 6)

                        if len(self.v2Campaign[3]) < 2:
                            self.v2_campaign_add_encounters(encounterList, 3, 2, 4)

                    progress.destroy()

                log("End of generate_v2_campaign_encounters")

                return mega
            except Exception as e:
                error_popup(self.root, e)
                raise


        def v2_campaign_add_encounters(self, encounterList, level, levelCnt, encCnt):
            """
            Generate encounters for the v2 campaign generator.
            """
            try:
                log("Start of v2_campaign_add_encounters")
                
                while len(self.v2Campaign[level]) < (encCnt if len([e for e in self.campaign if e["level"] == level]) < levelCnt else 2):
                    self.app.encounterTab.random_encounter(level=level, encounterList=encounterList)
                    # Make sure we don't get two of the same name
                    name = self.app.selected["name"] + (" (TSC)" if self.app.selected["expansion"] == "The Sunless City" and self.app.selected["name"] in set(["Broken Passageway", "Central Plaza"]) else "")
                    if name in set([c["name"] for c in self.v2Campaign[level]]) or name in set([e["name"] for e in self.campaign]):
                        continue
                    self.v2Campaign[level].append(self.add_card_to_v2_campaign_list(name))

                log("End of v2_campaign_add_encounters")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def load_v2_campaign_card(self, card, right=False):
            """
            Display pre-generated v2 encounter card.
            """
            try:
                log("Start of load_v2_campaign_card")

                self.app.selected = card
                self.app.encounterTab.rewardTreasure = None
                self.app.display.unbind("<Button 1>")
                
                if not right:
                    # Remove keyword tooltips from the previous card shown, if there are any.
                    for tooltip in self.app.tooltips:
                        tooltip.destroy()

                self.app.encounterTab.rewardTreasure = card.get("rewardTreasure")

                log("\tOpening " + baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + card["name"] + str(self.app.numberOfCharacters) + ".json")

                # Get the enemy slots for this card.
                with open(baseFolder + "\\lib\\dsbg_shuffle_encounters\\".replace("\\", pathSep) + card["name"] + str(self.app.numberOfCharacters) + ".json") as alternativesFile:
                    alts = load(alternativesFile)

                    # Create the encounter card with saved enemies and tooltips.
                    self.app.encounterTab.newEnemies = card["enemies"]
                    self.app.encounterTab.edit_encounter_card(card["name"], card["expansion"], card["level"], alts["enemySlots"], right=right, campaignGen=True)

                log("End of load_v2_campaign_card")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def v2_campaign_gravestone(self):
            """
            Display pre-generated v2 encounter card.
            """
            try:
                log("Start of v2_campaign_gravestone")

                if not len([e for e in self.campaign if e["level"] == 1]):
                    log("End of v2_campaign_gravestone (nothing done)")
                    return

                mega = self.generate_v2_campaign_encounters()

                if len([e for e in self.campaign if e["level"] == 1]) < 3:
                    level = 1
                elif len([e for e in self.campaign if e["level"] == 2]) < 3:
                    level = 2
                elif len([e for e in self.campaign if e["level"] == 3]) < 2:
                    level = 3
                elif mega and len([e for e in self.campaign if e["level"] == 4]) < 1:
                    level = 4
                else:
                    log("End of v2_campaign_gravestone (nothing done)")
                    return
                
                encounter = self.v2Campaign[level].pop()

                self.load_v2_campaign_card(encounter)
            
                p = PopupWindow(self.master, labelText="Keep or discard this encounter card?", keepButton=True, discardButton=True)
                self.root.wait_window(p)

                if p.answer:
                    self.v2Campaign[level].append(encounter)

                log("End of v2_campaign_gravestone")
            except Exception as e:
                error_popup(self.root, e)
                raise

except Exception as e:
    log(e, exception=True)
    raise