import tkinter as tk
import logging
import webbrowser
import platform
from tkinter import ttk
from PIL import Image, ImageTk, ImageFont
from os import path
from PIL import ImageFont
from dsbg_functions import center


if platform.system() == "Windows":
    pathSep = "\\"
else:
    pathSep = "/"

baseFolder = path.dirname(__file__).replace("\\lib".replace("\\", pathSep), "")
if platform.system() == "Windows":
    font = ImageFont.truetype(baseFolder + "\\lib\\Adobe Caslon Pro Semibold.ttf", 12)
else:
    font = ImageFont.truetype("./Adobe Caslon Pro Semibold.ttf", 12)


class CustomAdapter(logging.LoggerAdapter):
        """
        Used for logging.
        """
        def process(self, msg, kwargs):
            my_context = kwargs.pop("caller", self.extra["caller"])
            return "[%s] %s" % (my_context, msg), kwargs


class CreateToolTip(object):
    """
    A tooltip that displays while the user is hovered over a particular Label.
    """
    def __init__(self, widget, text="widget info"):
        self.waittime = 500     # miliseconds
        self.wraplength = 225   # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hide_tip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.show_tip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def show_tip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # Creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = ttk.Label(self.tw, text=self.text, font=(font, 12), justify="left", relief="solid", borderwidth=1, wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


class PopupWindow(tk.Toplevel):
    """
    A popup window that displays a message for the user.

    Optional parameters:
        labelText: String
            The message to be displayed in the popup window.

        firstButton: Boolean
            Whether to show the Ok button.

        secondButton: Boolean
            Whether to show the second button.

        progressBar: Boolean
            Whether to show the progress bar for app loading.

        loadingImage: Boolean
            Whether to show the loading image.
    """
    def __init__(self, root, labelText=None, firstButton=False, secondButton=False, progressBar=False, progressMax=None, loadingImage=False):
        tk.Toplevel.__init__(self, root)
        self.attributes('-alpha', 0.0)
        self.popupFrame = ttk.Frame(self, padding=(20, 10))
        self.popupFrame.pack()
        label = ttk.Label(self.popupFrame, text=labelText)
        label.grid(column=0, row=1, columnspan=2, padx=20, pady=20)
        self.wait_visibility()
        self.grab_set_global()
        label.focus_force()

        if firstButton:
            button = ttk.Button(self.popupFrame, text="OK", command=self.destroy)
            button.grid(column=0, row=2, padx=20, pady=20)

        if secondButton:
            button2 = ttk.Button(self.popupFrame, text="Quit and take me there!", command=root.destroy)
            button2.grid(column=1, row=2, padx=20, pady=20)
            button2.bind("<Button 1>", lambda e: webbrowser.open_new("https://github.com/DanDuhon/DSBG-Shuffle/releases"))

        if loadingImage:
            loadingImage = ImageTk.PhotoImage(Image.open(baseFolder + "\\lib\\bonfire.png".replace("\\", pathSep)), Image.Resampling.LANCZOS)
            loadingLabel = ttk.Label(self.popupFrame)
            loadingLabel.image = loadingImage
            loadingLabel.config(image=loadingImage)
            loadingLabel.grid(column=0, row=0, columnspan=2, padx=20, pady=20)

        if progressBar:
            self.progressVar = tk.DoubleVar()
            progressBar = ttk.Progressbar(self.popupFrame, variable=self.progressVar, maximum=progressMax, length=150)
            progressBar.grid(row=3, column=0, columnspan=2)

        center(self)
        self.attributes('-alpha', 1.0)


class HelpWindow(object):
    """
    Window that just displays text about how to use the app.
    """
    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        top.attributes('-alpha', 0.0)
        top.wait_visibility()
        top.grab_set_global()

        self.helpTextFrame = ttk.Frame(top, padding=(0, 0, 0, 10))
        self.helpTextFrame.grid(row=0, column=0, padx=15, pady=(10, 0), sticky="w")

        helpText = "Encounters Tab\n"
        helpText += "You can either select an encounter from the list or click the \"Random\n"
        helpText += "Level x\" buttons. Once an encounter card has been loaded, you can click\n"
        helpText += "on the card or use the \"s\" key to reshuffle the encounter's enemies and\n"
        helpText += "treasure reward, if any.\n\n"
        helpText += "If you try to shuffle the enemies and nothing happens, there's probably\n"
        helpText += "only one combination available! Many encounters with a single enemy have\n"
        helpText += "no alternatives, even with all sets activated.\n\n"
        helpText += "Mousing over keywords (in bold and italics) and icons in the Objectives\n"
        helpText += "and Special Rules sections will display the name or rules for that keyword.\n\n"
        helpText += "Campaign Tab\n"
        helpText += "You can build your own campaign by adding encounters to it. You can also\n"
        helpText += "save and load campaigns. You may only have one of each encounter name,\n"
        helpText += "but there are no restrictions beyond that. Encounters added to a campaign\n"
        helpText += "are frozen so you cannot shuffle the enemies. You can also print (non-boss)\n"
        helpText += "encounter cards in the campaign. Front side only (fow now?) so use sleeves!\n\n"
        helpText += "Events Tab\n"
        helpText += "Here you can browse event cards and build an event deck. Event cards are\n"
        helpText += "listed in the upper box and the event deck is in the lower box. Events can\n"
        helpText += "be added individually or via core set. Event cards are limited in number\n"
        helpText += "to how many are found in a single core set (e.g. the deck can't contain\n"
        helpText += "more than two Firekeeper's Boon cards).\n\n"
        helpText += "Using the Draw Event Card button will display a random card from the deck\n"
        helpText += "that hasn't been drawn yet. That card can be shuffled back into the deck\n"
        helpText += "or put on the bottom of the deck. These buttons only work for the last\n"
        helpText += "drawn card - not a selected one. There's no Return to Top button because\n"
        helpText += "that card is technically still on top so such a button would literally do\n"
        helpText += "nothing.\n\n"
        helpText += "Settings\n"
        helpText += "In the settings menu, you can enable the different core sets/expansions\n"
        helpText += "that add enemies or basic treasure to the game. These are the only sets\n"
        helpText += "listed on purpose as they are the ones that add non-boss enemies or\n"
        helpText += "additional characters.\n"
        helpText += "Some settings have tooltips, so hover over them for an explanation!"
        self.helpTextLabel = ttk.Label(self.helpTextFrame, text=helpText)
        self.helpTextLabel.grid()

        self.helpButtonsFrame = ttk.Frame(top, padding=(0, 0, 0, 10))
        self.helpButtonsFrame.grid(row=1, column=0, padx=15, pady=(10, 0), sticky="w")
        self.helpButtonsFrame.columnconfigure(index=0, weight=1)

        self.okButton = ttk.Button(self.helpButtonsFrame, text="OK", width=14, command=self.top.destroy)
        self.okButton.grid(column=0, row=0, padx=5)

        center(top)
        top.attributes('-alpha', 1.0)


class VerticalScrolledFrame(ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the "interior" attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=interior, anchor=tk.NW)
        self.interior.bind("<Enter>", self._bound_to_mousewheel)
        self.interior.bind("<Leave>", self._unbound_to_mousewheel)
        self.interior.bind("<Configure>", lambda event, canvas=self.interior: self.on_frame_configure(canvas))

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the canvas"s width to fit the inner frame.
                self.canvas.config(width=interior.winfo_reqwidth())
        interior.bind("<Configure>", _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Update the inner frame"s width to fill the canvas.
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
        self.canvas.bind("<Configure>", _configure_canvas)


    def on_frame_configure(self, canvas):
        """Reset the scroll region to encompass the inner frame"""
        canvas.configure(scrollregion=canvas.bbox("all"))


    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)


    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")


    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")