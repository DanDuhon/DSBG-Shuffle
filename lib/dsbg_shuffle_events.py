try:
    import os
    import tkinter as tk
    from json import dump, load
    from PIL import ImageTk
    from random import shuffle
    from tkinter import filedialog, ttk

    from dsbg_shuffle_utility import PopupWindow, clear_other_tab_images, error_popup, log, set_display_bindings_by_tab, baseFolder, pathSep 


    events = {
        "Alluring Skull": {"name": "Alluring Skull", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Big Pilgrim's Key": {"name": "Big Pilgrim's Key", "count": 1, "expansions": set(["The Sunless City"])},
        "Blacksmith's Trial": {"name": "Blacksmith's Trial", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Bleak Bonfire Ascetic": {"name": "Bleak Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Bloodstained Bonfire Ascetic": {"name": "Bloodstained Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Cracked Bonfire Ascetic": {"name": "Cracked Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Firekeeper's Boon": {"name": "Firekeeper's Boon", "count": 2, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Fleeting Glory": {"name": "Fleeting Glory", "count": 2, "expansions": set(["Painted World of Ariamis"])},
        "Forgotten Supplies": {"name": "Forgotten Supplies", "count": 2, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Frozen Bonfire Ascetic": {"name": "Frozen Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Green Blossom": {"name": "Green Blossom", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Hearty Bonfire Ascetic": {"name": "Hearty Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Lifegem": {"name": "Lifegem", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Lost Envoy": {"name": "Lost Envoy", "count": 1, "expansions": set(["The Sunless City"])},
        "Lost to Time": {"name": "Lost to Time", "count": 1, "expansions": set(["The Sunless City"])},
        "Martial Bonfire Ascetic": {"name": "Martial Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Obscured Knowledge": {"name": "Obscured Knowledge", "count": 1, "expansions": set(["Painted World of Ariamis"])},
        "Pine Resin": {"name": "Pine Resin", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Princess Guard": {"name": "Princess Guard", "count": 1, "expansions": set(["The Sunless City"])},
        "Rare Vagrant": {"name": "Rare Vagrant", "count": 1, "expansions": set(["Painted World of Ariamis"])},
        "Repair Powder": {"name": "Repair Powder", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Rite of Rekindling": {"name": "Rite of Rekindling", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Scout Ahead": {"name": "Scout Ahead", "count": 2, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Scrying Stone": {"name": "Scrying Stone", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Skeletal Reforging": {"name": "Skeletal Reforging", "count": 2, "expansions": set(["Tomb of Giants"])},
        "Stolen Artifact": {"name": "Stolen Artifact", "count": 2, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Trustworthy Promise": {"name": "Trustworthy Promise", "count": 2, "expansions": set(["Tomb of Giants"])},
        "Undead Merchant": {"name": "Undead Merchant", "count": 2, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Unhallowed Offering": {"name": "Unhallowed Offering", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])},
        "Virulent Bonfire Ascetic": {"name": "Virulent Bonfire Ascetic", "count": 1, "expansions": set(["Painted World of Ariamis", "Tomb of Giants", "The Sunless City"])}
    }


    class EventsFrame(ttk.Frame):
        def __init__(self, app, root):
            super(EventsFrame, self).__init__()
            self.app = app
            self.root = root
            
            self.currentEvent = None
            self.currentEventNum = 0
            self.eventDeck = []
            
            self.eventTabButtonsFrame = ttk.Frame(self)
            self.eventTabButtonsFrame.pack()
            self.eventTabEventListTreeviewFrame = ttk.Frame(self)
            self.eventTabEventListTreeviewFrame.pack(fill="both", expand=True)
            self.eventTabButtonsFrame2 = ttk.Frame(self)
            self.eventTabButtonsFrame2.pack()
            self.eventTabButtonsFrame3 = ttk.Frame(self)
            self.eventTabButtonsFrame3.pack()
            self.eventTabEventDeckTreeviewFrame = ttk.Frame(self)
            self.eventTabEventDeckTreeviewFrame.pack(fill="both", expand=True)
            self.eventTabDeckFrame = ttk.Frame(self)
            self.eventTabDeckFrame.pack(fill="both", expand=True)
            
            self.addEventButton = ttk.Button(self.eventTabButtonsFrame, text="Add Event(s)", width=16, command=self.add_event_to_deck)
            self.addEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)

            self.deleteEventButton = ttk.Button(self.eventTabButtonsFrame2, text="Remove Event", width=16, command=self.delete_event_from_deck)
            self.deleteEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.resetEventButton = ttk.Button(self.eventTabButtonsFrame2, text="Reset Event Deck", width=16, command=self.reset_event_deck)
            self.resetEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.loadEventDeckButton = ttk.Button(self.eventTabButtonsFrame2, text="Load Event Deck", width=16, command=self.load_event_deck)
            self.loadEventDeckButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.saveEventDeckButton = ttk.Button(self.eventTabButtonsFrame2, text="Save Event Deck", width=16, command=self.save_event_deck)
            self.saveEventDeckButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            
            self.drawEventButton = ttk.Button(self.eventTabButtonsFrame3, text="Draw Event Card", width=16, command=self.draw_from_event_deck)
            self.drawEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.shuffleEventButton = ttk.Button(self.eventTabButtonsFrame3, text="Shuffle Into Deck", width=16, command=self.return_event_card_to_deck)
            self.shuffleEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.bottomEventButton = ttk.Button(self.eventTabButtonsFrame3, text="Return To Bottom", width=16, command=self.return_event_card_to_bottom)
            self.bottomEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            self.topEventButton = ttk.Button(self.eventTabButtonsFrame3, text="Return To Top", width=16, command=self.return_event_card_to_top)
            self.topEventButton.pack(side=tk.LEFT, anchor=tk.CENTER, padx=5, pady=5)
            
            self.scrollbarTreeviewEventList = ttk.Scrollbar(self.eventTabEventListTreeviewFrame)
            self.scrollbarTreeviewEventList.pack(side="right", fill="y")
            self.scrollbarTreeviewEventDeck = ttk.Scrollbar(self.eventTabEventDeckTreeviewFrame)
            self.scrollbarTreeviewEventDeck.pack(side="right", fill="y")
            self.create_event_treeviews()


        def create_event_treeviews(self):
            """
            Create the event list and event deck treeviews where users can see event cards.
            """
            try:
                log("Start of create_event_treeviews")
                
                self.treeviewEventList = ttk.Treeview(
                    self.eventTabEventListTreeviewFrame,
                    selectmode="extended",
                    columns=("Core Set", "Name", "Count"),
                    yscrollcommand=self.scrollbarTreeviewEventList.set,
                    height=12 if self.root.winfo_screenheight() > 1000 else 10
                )
                
                self.treeviewEventList.pack(expand=True, fill="both")
                self.scrollbarTreeviewEventList.config(command=self.treeviewEventList.yview)
                
                self.treeviewEventList.column("#0", width=30)
                self.treeviewEventList.column("#1", width=155)
                self.treeviewEventList.column("#2", width=170)

                self.treeviewEventList.heading("Core Set", text="Core Set", anchor=tk.W)
                self.treeviewEventList.heading("Name", text="Name", anchor=tk.W)
                self.treeviewEventList.heading("Count", text="Count", anchor=tk.W)
                self.treeviewEventList.column("Core Set", anchor=tk.W)
                self.treeviewEventList.column("Name", anchor=tk.W)
                self.treeviewEventList.column("Count", anchor=tk.W)
                
                self.treeviewEventList.bind("<<TreeviewSelect>>", self.load_event)
                self.treeviewEventList.bind("<Control-a>", lambda *args: self.treeviewEventList.selection_add(self.treeviewEventList.get_children()))

                for coreSet in sorted(self.app.coreSets - set(["Dark Souls The Board Game"])):
                    self.treeviewEventList.insert(parent="", iid=coreSet, values=(coreSet, "", ""), index="end", tags=False)
                    for event in [event for event in events if coreSet in events[event]["expansions"]]:
                        self.treeviewEventList.insert(parent=coreSet, iid=event + "_" + coreSet, values=("", event, events[event]["count"]), index="end", tags=True)
                
                self.treeviewEventDeck = ttk.Treeview(
                    self.eventTabEventDeckTreeviewFrame,
                    selectmode="extended",
                    columns=("Event Deck", "Drawn Order"),
                    yscrollcommand=self.scrollbarTreeviewEventDeck.set,
                    height=12 if self.root.winfo_screenheight() > 1000 else 10
                )
                
                self.treeviewEventDeck.pack(expand=True, fill="both")
                self.scrollbarTreeviewEventDeck.config(command=self.treeviewEventDeck.yview)

                minwidth = self.treeviewEventDeck.column('#0', option='minwidth')
                self.treeviewEventDeck.column('#0', width=minwidth)

                self.treeviewEventDeck.heading("Event Deck", text="Event Deck", anchor=tk.W)
                self.treeviewEventDeck.heading("Drawn Order", text="Drawn Order", anchor=tk.W)
                self.treeviewEventDeck.column("Event Deck", anchor=tk.W, width=180)
                self.treeviewEventDeck.column("Drawn Order", anchor=tk.W, width=248)
                
                self.treeviewEventDeck.bind("<<TreeviewSelect>>", self.load_event)
                self.treeviewEventDeck.bind("<Control-a>", lambda *args: self.treeviewEventDeck.selection_add(self.treeviewEventDeck.get_children()))

                log("End of create_event_treeviews")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def load_event(self, event=None, campaign=False, treeviewCampaign=None):
            try:
                log("Start of load_event, campaign={}", str(campaign))
                
                set_display_bindings_by_tab(self.app)

                clear_other_tab_images(self.app, "encounters", "encounters")
                
                # Get the event selected.
                if event:
                    tree = event.widget

                    # Don't update the image shown if you've selected more than one encounter.
                    if len(tree.selection()) != 1:
                        log("End of load_event (not updating image)")
                        return
                    
                    if tree == self.treeviewEventList and len(self.treeviewEventDeck.selection()) > 0:
                        for selection in self.treeviewEventDeck.selection():
                            self.treeviewEventDeck.selection_remove(selection)
                    elif tree == self.treeviewEventDeck and len(self.treeviewEventList.selection()) > 0:
                        for selection in self.treeviewEventList.selection():
                            self.treeviewEventList.selection_remove(selection)
                    
                    eventSelected = tree.selection()[0]
                elif campaign:
                    eventSelected = treeviewCampaign.selection()[0]
                else:
                    eventSelected = self.currentEvent

                if "_" in eventSelected:
                    eventSelected = eventSelected[:eventSelected.index("_")]

                if eventSelected not in events:
                    log("End of load_event (core set selected)")
                    return

                # Remove keyword tooltips from the previous image shown, if there are any.
                for tooltip in self.app.tooltips:
                    tooltip.destroy()

                # Create and display the event image.
                self.app.create_image(events[eventSelected]["name"] + ".jpg", "encounter", 4)
                displayPhotoImage = ImageTk.PhotoImage(self.app.displayImage)
                self.app.display.image = displayPhotoImage
                self.app.display.config(image=displayPhotoImage)
                self.app.displayImages["events"][self.app.display]["images"] = displayPhotoImage
                self.app.displayImages["events"][self.app.display]["name"] = events[eventSelected]["name"]
                self.app.displayImages["events"][self.app.display]["activeTab"] = "events"

                log("End of load_event")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def save_event_deck(self):
            """
            Save the event deck to a JSON file that can be loaded later.
            """
            try:
                log("Start of save_event_deck")

                # Prompt user to save the file.
                deckName = filedialog.asksaveasfile(mode="w", initialdir=baseFolder + "\\lib\\dsbg_shuffle_saved_event_decks".replace("\\", pathSep), defaultextension=".json")

                # If they canceled it, do nothing.
                if not deckName:
                    log("End of save_event_deck (nothing done)")
                    return
                
                deckData = [self.treeviewEventDeck.item(event) for event in self.treeviewEventDeck.get_children()]
                eventDeckCopy = [event for event in self.eventDeck]

                for item in deckData:
                    i = [event[:event.index("_")] for event in eventDeckCopy].index(item["values"][0])
                    item["eventDeckEntry"] = eventDeckCopy.pop(i)

                with open(deckName.name, "w") as deckFile:
                    dump(deckData, deckFile)

                log("End of save_event_deck (saved to " + str(deckFile) + ")")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def load_event_deck(self):
            """
            Load an event deck from a JSON file, clearing the current deck treeview and replacing
            it with the data from the JSON file.
            """
            try:
                log("Start of load_event_deck")

                # Prompt the user to find the campaign file.
                deckFile = filedialog.askopenfilename(initialdir=baseFolder + "\\lib\\dsbg_shuffle_saved_event_decks".replace("\\", pathSep), filetypes = [(".json", ".json")])

                # If the user did not select a file, do nothing.
                if not deckFile:
                    log("End of load_event_deck (file dialog canceled)")
                    return
                
                # If the user did not select a JSON file, notify them that that was an invalid file.
                if os.path.splitext(deckFile)[1] != ".json":
                    self.set_bindings_buttons_menus(False)
                    PopupWindow(self.master, labelText="Invalid DSBG-Shuffle event deck file.", firstButton="Ok")
                    self.set_bindings_buttons_menus(True)
                    log("End of load_event_deck (invalid file)")
                    return
                
                log("Loading file " + deckFile)

                with open(deckFile, "r") as f:
                    self.deckData = load(f)

                # Check to see if there are any invalid names or levels in the JSON file.
                # This is about as sure as I can be that you can't load random JSON into the app.
                if any([
                    any([item["eventDeckEntry"][:item["eventDeckEntry"].index("_")] not in events for item in self.deckData]),
                    any([item["values"][0] not in events for item in self.deckData])
                    ]):
                    self.set_bindings_buttons_menus(False)
                    PopupWindow(self.master, labelText="Invalid DSBG-Shuffle event deck file.", firstButton="Ok")
                    self.set_bindings_buttons_menus(True)
                    log("End of load_event_deck (invalid file)")
                    return
                
                # Remove existing event deck elements.
                for item in self.treeviewEventDeck.get_children():
                    self.treeviewEventDeck.delete(item)

                # Create the event deck.
                self.eventDeck = [item["eventDeckEntry"] for item in self.deckData]
                for item in self.deckData:
                    self.treeviewEventDeck.insert(parent="", iid=item["eventDeckEntry"], values=item["values"], index="end")
                    if item["values"][1] and item["values"][1] > self.currentEventNum:
                        self.currentEventNum = item["values"][1]

                log("End of load_event_deck (loaded from " + str(deckFile) + ")")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def sort_event_deck_treeview(self):
            try:
                log("Start of sort_event_deck_treeview")

                # Sort the event deck so that cards that have been drawn are at the top,
                # in order of most recently drawn.
                l = [(0 if not self.treeviewEventDeck.item(k)["values"][1] else self.treeviewEventDeck.item(k)["values"][1], k) for k in self.treeviewEventDeck.get_children()]
                l.sort(key=lambda x: (-x[0], x[1]))
                for index, (val, k) in enumerate(l):
                    self.treeviewEventDeck.move(k, "", index)

                log("End of sort_event_deck_treeview")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def add_event_to_deck(self, event=None):
            """
            Adds an event card to the event deck, visible in the event deck treeview.
            """
            try:
                log("Start of add_event_to_deck")
                
                for selection in list(self.treeviewEventList.selection()):
                    eventSelected = self.treeviewEventList.item(selection)["values"][1 if self.treeviewEventList.item(selection)["values"][1] else 0]

                    # If an expansion is selected, add the events under that expansion.
                    if eventSelected in self.app.coreSets:
                        for event in self.treeviewEventList.get_children(eventSelected):
                            # Add an event for each copy of the card that exists.
                            for x in range(events[event[:event.index("_")]]["count"]):
                                if self.treeviewEventDeck.exists(event[:event.index("_")] + "_" + str(x)):
                                    continue
                                self.treeviewEventDeck.insert(parent="", iid=event[:event.index("_")] + "_" + str(x), values=(event[:event.index("_")], ""), index="end", tags=False)
                                self.eventDeck.append(event[:event.index("_")] + "_" + str(x))
                    else:
                        # Add an event for each copy of the card that exists.
                        for x in range(events[eventSelected]["count"]):
                            if self.treeviewEventDeck.exists(eventSelected + "_" + str(x)):
                                continue
                            self.treeviewEventDeck.insert(parent="", iid=eventSelected + "_" + str(x), values=(eventSelected, ""), index="end", tags=False)
                            self.eventDeck.append(eventSelected + "_" + str(x))

                self.sort_event_deck_treeview()

                shuffle(self.eventDeck)

                log("End of add_event_to_deck")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def delete_event_from_deck(self, event=None):
            """
            Delete an event from the event deck.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of delete_event_from_deck")
                
                # If the button is clicked with no selection, do nothing.
                if not self.treeviewEventDeck.selection():
                    log("End of delete_event_from_deck (nothing done)")
                    return
                
                # Remove the deleted encounters from the treeview.
                for item in self.treeviewEventDeck.selection():
                    if self.treeviewEventDeck.item(item)["values"][1]:
                        self.currentEventNum -= 1
                        for event in self.treeviewEventDeck.get_children():
                            if self.treeviewEventDeck.item(event)["values"][1] and self.treeviewEventDeck.item(event)["values"][1] > self.treeviewEventDeck.item(item)["values"][1]:
                                self.treeviewEventDeck.item(event, values=(self.treeviewEventDeck.item(event)["values"][0], self.treeviewEventDeck.item(event)["values"][1] - 1))

                    self.treeviewEventDeck.delete(item)
                    self.eventDeck.remove(item)

                # Remove the image displaying a deleted encounter.
                self.app.display.config(image="")
                self.app.displayImages["events"][self.app.display]["images"] = None
                self.app.displayImages["events"][self.app.display]["name"] = None
                self.app.displayImages["events"][self.app.display]["activeTab"] = None
                self.app.display2.config(image="")
                self.app.displayImages["events"][self.app.display2]["images"] = None
                self.app.displayImages["events"][self.app.display2]["name"] = None
                self.app.displayImages["events"][self.app.display2]["activeTab"] = None
                self.app.display3.config(image="")
                self.app.displayImages["events"][self.app.display3]["images"] = None
                self.app.displayImages["events"][self.app.display3]["name"] = None
                self.app.displayImages["events"][self.app.display3]["activeTab"] = None

                shuffle(self.eventDeck)

                log("End of delete_event_from_deck")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def reset_event_deck(self, event=None):
            """
            Essentially shuffles all drawn cards back into the deck.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of reset_event_deck")
                
                # Set events to not be drawn yet.
                for item in self.treeviewEventDeck.get_children():
                    self.treeviewEventDeck.item(item, values=(self.treeviewEventDeck.item(item)["values"][0], ""))

                self.sort_event_deck_treeview()

                # Remove the image displaying a deleted encounter.
                self.app.display.config(image="")
                self.app.displayImages["events"][self.app.display]["images"] = None
                self.app.displayImages["events"][self.app.display]["name"] = None
                self.app.displayImages["events"][self.app.display]["activeTab"] = None
                self.app.display2.config(image="")
                self.app.displayImages["events"][self.app.display2]["images"] = None
                self.app.displayImages["events"][self.app.display2]["name"] = None
                self.app.displayImages["events"][self.app.display2]["activeTab"] = None
                self.app.display3.config(image="")
                self.app.displayImages["events"][self.app.display3]["images"] = None
                self.app.displayImages["events"][self.app.display3]["name"] = None
                self.app.displayImages["events"][self.app.display3]["activeTab"] = None
                
                self.currentEvent = None
                self.currentEventNum = 0

                shuffle(self.eventDeck)

                log("End of reset_event_deck")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def draw_from_event_deck(self, event=None):
            """
            "Draw" the top card from the virtual deck and display it.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of draw_from_event_deck")
                
                # If the button is clicked with no drawn event card, do nothing.
                if not self.eventDeck or not [eventCard for eventCard in self.eventDeck if not self.treeviewEventDeck.item(eventCard)["values"][1]]:
                    log("End of draw_from_event_deck (nothing done)")
                    return

                self.currentEvent = [eventCard for eventCard in self.eventDeck if not self.treeviewEventDeck.item(eventCard)["values"][1]][0]
                self.currentEventNum += 1
                self.load_event()
                self.treeviewEventDeck.item(self.currentEvent, values=(self.treeviewEventDeck.item(self.currentEvent)["values"][0], self.currentEventNum))

                self.sort_event_deck_treeview()

                log("End of draw_from_event_deck")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def return_event_card_to_deck(self, event=None):
            """
            Shuffles the selected card back into the deck.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of return_event_card_to_deck")
                
                # If the button is clicked with no event card selected, do nothing.
                if not self.treeviewEventDeck.selection() or len(self.treeviewEventDeck.selection()) > 1:
                    log("End of return_event_card_to_deck (nothing done)")
                    return
                
                card = self.treeviewEventDeck.selection()[0]
                
                # If the button is clicked with no event card selected, do nothing.
                if not self.treeviewEventDeck.item(card)["values"][1]:
                    log("End of return_event_card_to_deck (nothing done)")
                    return

                shuffle(self.eventDeck)
                self.app.display.config(image="")
                self.app.displayImages["events"][self.app.display]["images"] = None
                self.app.displayImages["events"][self.app.display]["name"] = None
                self.app.displayImages["events"][self.app.display]["activeTab"] = None
                self.app.display2.config(image="")
                self.app.displayImages["events"][self.app.display2]["images"] = None
                self.app.displayImages["events"][self.app.display2]["name"] = None
                self.app.displayImages["events"][self.app.display2]["activeTab"] = None
                self.app.display3.config(image="")
                self.app.displayImages["events"][self.app.display3]["images"] = None
                self.app.displayImages["events"][self.app.display3]["name"] = None
                self.app.displayImages["events"][self.app.display3]["activeTab"] = None

                # Reduce the Drawn Order value of more recently drawn cards by 1.
                for eventCard in self.treeviewEventDeck.get_children():
                    if self.treeviewEventDeck.item(eventCard)["values"][1] and self.treeviewEventDeck.item(eventCard)["values"][1] > self.treeviewEventDeck.item(card)["values"][1]:
                        self.treeviewEventDeck.item(eventCard, values=(self.treeviewEventDeck.item(eventCard)["values"][0], self.treeviewEventDeck.item(eventCard)["values"][1]-1))
                self.treeviewEventDeck.item(card, values=(self.treeviewEventDeck.item(card)["values"][0], ""))
                self.currentEvent = None
                self.currentEventNum -= 1

                self.sort_event_deck_treeview()

                shuffle(self.eventDeck)

                log("End of return_event_card_to_deck")
            except Exception as e:
                error_popup(self.root, e)
                raise


        def return_event_card_to_bottom(self, event=None):
            """
            Puts the selected card on the bottom of the virtual deck.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of return_event_card_to_bottom")
                
                # If the button is clicked with no event card selected, do nothing.
                if not self.treeviewEventDeck.selection() or len(self.treeviewEventDeck.selection()) > 1:
                    log("End of return_event_card_to_bottom (nothing done)")
                    return
                
                card = self.treeviewEventDeck.selection()[0]
                
                # If the button is clicked with no event card selected, do nothing.
                if not self.treeviewEventDeck.item(card)["values"][1]:
                    log("End of return_event_card_to_deck (nothing done)")
                    return

                self.eventDeck.remove(card)
                self.eventDeck.append(card)
                self.app.display.config(image="")
                self.app.displayImages["events"][self.app.display]["images"] = None
                self.app.displayImages["events"][self.app.display]["name"] = None
                self.app.displayImages["events"][self.app.display]["activeTab"] = None
                self.app.display2.config(image="")
                self.app.displayImages["events"][self.app.display2]["images"] = None
                self.app.displayImages["events"][self.app.display2]["name"] = None
                self.app.displayImages["events"][self.app.display2]["activeTab"] = None
                self.app.display3.config(image="")
                self.app.displayImages["events"][self.app.display3]["images"] = None
                self.app.displayImages["events"][self.app.display3]["name"] = None
                self.app.displayImages["events"][self.app.display3]["activeTab"] = None

                # Reduce the Drawn Order value of more recently drawn cards by 1.
                for eventCard in self.treeviewEventDeck.get_children():
                    if self.treeviewEventDeck.item(eventCard)["values"][1] and self.treeviewEventDeck.item(eventCard)["values"][1] > self.treeviewEventDeck.item(card)["values"][1]:
                        self.treeviewEventDeck.item(eventCard, values=(self.treeviewEventDeck.item(eventCard)["values"][0], self.treeviewEventDeck.item(eventCard)["values"][1]-1))
                self.treeviewEventDeck.item(card, values=(self.treeviewEventDeck.item(card)["values"][0], ""))
                self.currentEvent = None
                self.currentEventNum -= 1

                self.sort_event_deck_treeview()

                log("End of return_event_card_to_bottom")
            except Exception as e:
                error_popup(self.root, e)
                raise

        def return_event_card_to_top(self, event=None):
            """
            Puts the selected card on the top of the virtual deck.

            Optional Parameters:
                event: tkinter.Event
                    The tkinter Event that is the trigger.
            """
            try:
                log("Start of return_event_card_to_top")
                
                # If the button is clicked with no event card selected, do nothing.
                if not self.treeviewEventDeck.selection() or len(self.treeviewEventDeck.selection()) > 1:
                    log("End of return_event_card_to_top (nothing done)")
                    return
                
                card = self.treeviewEventDeck.selection()[0]
                
                # If the button is clicked with no event card selected, do nothing.
                if not self.treeviewEventDeck.item(card)["values"][1]:
                    log("End of return_event_card_to_deck (nothing done)")
                    return

                self.eventDeck.remove(card)
                self.eventDeck.insert(0, card)
                self.app.display.config(image="")
                self.app.displayImages["events"][self.app.display]["images"] = None
                self.app.displayImages["events"][self.app.display]["name"] = None
                self.app.displayImages["events"][self.app.display]["activeTab"] = None
                self.app.display2.config(image="")
                self.app.displayImages["events"][self.app.display2]["images"] = None
                self.app.displayImages["events"][self.app.display2]["name"] = None
                self.app.displayImages["events"][self.app.display2]["activeTab"] = None
                self.app.display3.config(image="")
                self.app.displayImages["events"][self.app.display3]["images"] = None
                self.app.displayImages["events"][self.app.display3]["name"] = None
                self.app.displayImages["events"][self.app.display3]["activeTab"] = None
                
                # Reduce the Drawn Order value of more recently drawn cards by 1.
                for eventCard in self.treeviewEventDeck.get_children():
                    if self.treeviewEventDeck.item(eventCard)["values"][1] and self.treeviewEventDeck.item(eventCard)["values"][1] > self.treeviewEventDeck.item(card)["values"][1]:
                        self.treeviewEventDeck.item(eventCard, values=(self.treeviewEventDeck.item(eventCard)["values"][0], self.treeviewEventDeck.item(eventCard)["values"][1]-1))
                self.treeviewEventDeck.item(card, values=(self.treeviewEventDeck.item(card)["values"][0], ""))
                self.currentEvent = None
                self.currentEventNum -= 1

                self.sort_event_deck_treeview()

                log("End of return_event_card_to_top")
            except Exception as e:
                error_popup(self.root, e)
                raise

except Exception as e:
    log(e, exception=True)
    raise