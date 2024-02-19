import inspect
import logging
import tkinter as tk
import platform
import webbrowser
from os import path
from PIL import Image, ImageTk, ImageFont
from tkinter import ttk


class CustomAdapter(logging.LoggerAdapter):
    """
    Used for logging.
    """
    def process(self, msg, kwargs):
        my_context = kwargs.pop("caller", self.extra["caller"])
        return "[%s] %s" % (my_context, msg), kwargs


if platform.system() == "Windows":
    pathSep = "\\"
    windowsOs = True
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter("%(asctime)s|%(levelname)s|%(message)s", "%d/%m/%Y %H:%M:%S")
    fh = logging.FileHandler(path.dirname(path.realpath(__file__)) + "\\dsbg_shuffle_log.txt".replace("\\", pathSep), "w")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    adapter = CustomAdapter(logger, {"caller": ""})
    logger.setLevel(logging.DEBUG)
else:
    pathSep = "/"
    windowsOs = False

baseFolder = path.dirname(__file__).replace("\\lib".replace("\\", pathSep), "")
if windowsOs:
    font = ImageFont.truetype(baseFolder + "\\lib\\Adobe Caslon Pro Semibold.ttf", 12)
else:
    font = ImageFont.truetype("./Adobe Caslon Pro Semibold.ttf", 12)


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
        self.label = ttk.Label(self.popupFrame, text=labelText)
        self.label.grid(column=0, row=1, columnspan=2, padx=20, pady=20)
        self.wait_visibility()
        self.grab_set_global()
        self.label.focus_force()

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

        helpText = "There's a wiki on the Github page now!\n\n"
        helpText += "Encounters Tab\n"
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
        helpText += "You can build your own campaign by adding encounters and/or events to it.\n"
        helpText += "You can also save and load campaigns. Encounters added to a campaign\n"
        helpText += "are frozen so you cannot shuffle the enemies. You can also print (non-boss)\n"
        helpText += "encounter cards in the campaign. Front side only so use sleeves!\n\n"
        helpText += "Events Tab\n"
        helpText += "Here you can browse event cards and build an event deck. Event cards are\n"
        helpText += "listed in the upper box and the event deck is in the lower box. Events can\n"
        helpText += "be added individually or via core set. Event cards are limited in number\n"
        helpText += "to how many are found in a single core set (e.g. the deck can't contain\n"
        helpText += "more than two Firekeeper's Boon cards).\n\n"
        helpText += "Using the Draw Event Card button will display a random card from the deck\n"
        helpText += "that hasn't been drawn yet. It will also keep track of what cards were\n"
        helpText += "drawn and in what order. Cards can be returned to the top or bottom of\n"
        helpText += "the deck or shuffled back in. The reset button shuffles all drawn cards\n"
        helpText += "back into the deck.\n\n"
        helpText += "Settings\n"
        helpText += "In the settings menu, you can enable the different core sets/expansions.\n"
        helpText += "These are the only sets listed on purpose as they are the ones that add\n"
        helpText += "non-boss enemies, additional characters, or common treasure.\n"
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


def center(win):
    """
    Centers a tkinter window

    Required Parameters:
        win: tkinter window
            The main window or Toplevel window to center.
    """
    win.update_idletasks()
    width = win.winfo_width()
    frmWidth = win.winfo_rootx() - win.winfo_x()
    winWidth = width + 2 * frmWidth
    height = win.winfo_height()
    titlebarHeight = win.winfo_rooty() - win.winfo_y()
    winHeight = height + titlebarHeight + frmWidth
    x = win.winfo_screenwidth() // 2 - winWidth // 2
    y = win.winfo_screenheight() // 2 - winHeight // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def enable_binding(bindKey, method, root):
    """
    Sets a keyboard shortcut.

    Required Parameters:
        bindKey: String
            The key combination to be bound to a method.

        method: method/function
            The method or function to run when the key combination is pressed.
    """
    return root.bind_all("<" + bindKey + ">", method)


def log(message, exception=False):
    if windowsOs:
        if exception:
            adapter.exception(message)
            return
        
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        adapter.debug(message, caller=calframe[1][3])


def error_popup(root, e):
    log(e, exception=True)
    p = PopupWindow(root, "Error detected!\n\nPlease open a Github issue describing what you were doing\nand include the dsbg_shuffle_log file!  Thanks!", firstButton="Ok")
    root.wait_window(p)


def do_nothing(event=None):
    pass