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
    font2 = ImageFont.truetype(baseFolder + "\\lib\\OptimusPrinceps.ttf", 24)
    font3 = ImageFont.truetype(baseFolder + "\\lib\\OptimusPrinceps.ttf", 30)
    fontEncounterName = ImageFont.truetype(baseFolder + "\\lib\\OptimusPrinceps.ttf", 28)
    fontFlavor = ImageFont.truetype(baseFolder + "\\lib\\Adobe Caslon Pro Semibold Italic.ttf", 12)
else:
    font = ImageFont.truetype("./Adobe Caslon Pro Semibold.ttf", 12)
    font2 = ImageFont.truetype("./OptimusPrinceps.ttf", 24)
    font3 = ImageFont.truetype("./OptimusPrinceps.ttf", 30)
    fontEncounterName = ImageFont.truetype("./OptimusPrinceps.ttf", 28)
    fontFlavor = ImageFont.truetype("./Adobe Caslon Pro Semibold Italic.ttf", 12)


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

        yesButton: Boolean
            Whether to show the yes button.

        noButton: Boolean
            Whether to show the no button.

        progressBar: Boolean
            Whether to show the progress bar for app loading.

        loadingImage: Boolean
            Whether to show the loading image.
    """
    def __init__(self, root, labelText=None, firstButton=False, secondButton=False, yesButton=False, noButton=False, ornsteinButton=False, smoughButton=False, leftButton=False, rightButton=False, keepButton=False, discardButton=False, progressBar=False, progressMax=None, loadingImage=False):
        tk.Toplevel.__init__(self, root)
        self.attributes('-alpha', 0.0)
        self.popupFrame = ttk.Frame(self, padding=(20, 10))
        self.popupFrame.pack()
        self.label = ttk.Label(self.popupFrame, text=labelText)
        self.label.grid(column=0, row=1, columnspan=2, padx=20, pady=20)
        self.wait_visibility()
        self.grab_set()
        self.answer = None

        if firstButton:
            button = ttk.Button(self.popupFrame, text="OK", command=self.destroy)
            button.grid(column=0, row=2, padx=20, pady=20)

        if secondButton:
            button2 = ttk.Button(self.popupFrame, text="Quit and take me there!", command=root.destroy)
            button2.grid(column=1, row=2, padx=20, pady=20)
            button2.bind("<Button 1>", lambda e: webbrowser.open_new("https://github.com/DanDuhon/DSBG-Shuffle/releases"))

        if yesButton:
            button = ttk.Button(self.popupFrame, text="Yes", command=self.yes)
            button.grid(column=0, row=2, padx=20, pady=20)

        if noButton:
            button = ttk.Button(self.popupFrame, text="No", command=self.no)
            button.grid(column=1, row=2, padx=20, pady=20)

        if leftButton:
            button = ttk.Button(self.popupFrame, text="Left", command=self.yes)
            button.grid(column=0, row=2, padx=20, pady=20)

        if rightButton:
            button = ttk.Button(self.popupFrame, text="Right", command=self.no)
            button.grid(column=1, row=2, padx=20, pady=20)

        if keepButton:
            button = ttk.Button(self.popupFrame, text="Keep", command=self.yes)
            button.grid(column=0, row=2, padx=20, pady=20)

        if discardButton:
            button = ttk.Button(self.popupFrame, text="Discard", command=self.no)
            button.grid(column=1, row=2, padx=20, pady=20)

        if ornsteinButton:
            button = ttk.Button(self.popupFrame, text="Ornstein", command=self.yes)
            button.grid(column=0, row=2, padx=20, pady=20)

        if smoughButton:
            button = ttk.Button(self.popupFrame, text="Smough", command=self.no)
            button.grid(column=1, row=2, padx=20, pady=20)

        if loadingImage:
            loadingImage = ImageTk.PhotoImage(Image.open(baseFolder + "\\lib\\bonfire.png".replace("\\", pathSep)), Image.Resampling.LANCZOS)
            loadingLabel = ttk.Label(self.popupFrame)
            loadingLabel.image = loadingImage
            loadingLabel.config(image=loadingImage)
            loadingLabel.grid(column=0, row=0, columnspan=2, padx=20, pady=20)

        if progressBar:
            self.progressVar = tk.DoubleVar()
            self.progressBar = ttk.Progressbar(self.popupFrame, variable=self.progressVar, maximum=progressMax, length=150)
            self.progressBar.grid(row=3, column=0, columnspan=2)

        center(self)
        self.attributes('-alpha', 1.0)


    def yes(self):
        self.destroy()
        self.answer = True


    def no(self):
        self.destroy()
        self.answer = False


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


def set_display_bindings_by_tab(app, smoughActive=False):
    tab = app.notebook.tab(app.notebook.select(), "text")
    # Don't change bindings on the campaign tab.
    if tab == "Campaign":
        return
    
    if tab == "Encounters":
        app.displayTopLeft.bind("<Button 1>", app.encounterTab.shuffle_enemies)

        app.displayTopRight.unbind("<Button 1>")
        app.displayTopRight.unbind("<Shift-Button 1>")
        app.displayTopRight.unbind("<Shift-Button 3>")
        app.displayTopRight.unbind("<Control-1>")
        app.displayTopRight.unbind("<Shift-Control-1>")

        app.displayBottomRight.unbind("<Button 1>")
        app.displayBottomRight.unbind("<Shift-Button 1>")
        app.displayBottomRight.unbind("<Shift-Button 3>")
        app.displayBottomRight.unbind("<Control-1>")
        app.displayBottomRight.unbind("<Shift-Control-1>")
    elif tab == "Events":
        app.displayTopLeft.unbind("<Button 1>")

        app.displayTopRight.unbind("<Button 1>")
        app.displayTopRight.unbind("<Shift-Button 1>")
        app.displayTopRight.unbind("<Shift-Button 3>")
        app.displayTopRight.unbind("<Control-1>")
        app.displayTopRight.unbind("<Shift-Control-1>")

        app.displayBottomRight.unbind("<Button 1>")
        app.displayBottomRight.unbind("<Shift-Button 1>")
        app.displayBottomRight.unbind("<Shift-Button 3>")
        app.displayBottomRight.unbind("<Control-1>")
        app.displayBottomRight.unbind("<Shift-Control-1>")
    elif tab == "Behavior Variants":
        app.displayTopLeft.bind("<Button 1>", app.variantsTab.apply_difficulty_modifier)

        app.displayTopRight.bind("<Button 1>", app.variantsTab.apply_difficulty_modifier)
        app.displayTopRight.unbind("<Shift-Button 1>")
        app.displayTopRight.unbind("<Shift-Button 3>")
        app.displayTopRight.unbind("<Control-1>")
        app.displayTopRight.unbind("<Shift-Control-1>")

        if smoughActive:
            app.displayBottomRight.bind("<Button 1>", app.variantsTab.apply_difficulty_modifier)
        else:
            app.displayBottomRight.unbind("<Button 1>")
            app.displayBottomRight.unbind("<Shift-Button 1>")
            app.displayBottomRight.unbind("<Shift-Button 3>")
            app.displayBottomRight.unbind("<Control-1>")
            app.displayBottomRight.unbind("<Shift-Control-1>")
    elif tab == "Behavior Decks":
        app.displayTopLeft.unbind("<Button 1>")

        app.displayTopRight.bind("<Button 1>", lambda event, x=1: app.behaviorDeckTab.lower_health(event=event, amount=x))
        app.displayTopRight.bind("<Shift-Button 1>", lambda event, x=5: app.behaviorDeckTab.lower_health(event=event, amount=x))
        app.displayTopRight.bind("<Button 3>", lambda event, x=1: app.behaviorDeckTab.raise_health(event=event, amount=x))
        app.displayTopRight.bind("<Shift-Button 3>", lambda event, x=5: app.behaviorDeckTab.raise_health(event=event, amount=x))
        app.displayTopRight.bind("<Control-1>", lambda event, x=1: app.behaviorDeckTab.raise_health(event=event, amount=x))
        app.displayTopRight.bind("<Shift-Control-1>", lambda event, x=5: app.behaviorDeckTab.raise_health(event=event, amount=x))

        if smoughActive:
            app.displayBottomRight.bind("<Button 1>", lambda event, x=1: app.behaviorDeckTab.lower_health(event=event, amount=x))
            app.displayBottomRight.bind("<Shift-Button 1>", lambda event, x=5: app.behaviorDeckTab.lower_health(event=event, amount=x))
            app.displayBottomRight.bind("<Button 3>", lambda event, x=1: app.behaviorDeckTab.raise_health(event=event, amount=x))
            app.displayBottomRight.bind("<Shift-Button 3>", lambda event, x=5: app.behaviorDeckTab.raise_health(event=event, amount=x))
            app.displayBottomRight.bind("<Control-1>", lambda event, x=1: app.behaviorDeckTab.raise_health(event=event, amount=x))
            app.displayBottomRight.bind("<Shift-Control-1>", lambda event, x=5: app.behaviorDeckTab.raise_health(event=event, amount=x))
        else:
            app.displayBottomRight.unbind("<Button 1>")
            app.displayBottomRight.unbind("<Shift-Button 1>")
            app.displayBottomRight.unbind("<Shift-Button 3>")
            app.displayBottomRight.unbind("<Control-1>")
            app.displayBottomRight.unbind("<Shift-Control-1>")



def clear_other_tab_images(app, lookupTab, activeTab, name=None, onlyDisplay=None):
    if not getattr(app, "displayTopLeft", None):
        return

    app.displayKing1.grid_forget()
    app.displayKing2.grid_forget()
    app.displayKing3.grid_forget()
    app.displayKing4.grid_forget()

    for e in [e for e in app.behaviorDeckTab.decks if "healthTrackers" in app.behaviorDeckTab.decks[e]]:
        for h in app.behaviorDeckTab.decks[e]["healthTrackers"]:
            h.grid_forget()

    displays = [app.displayTopLeft, app.displayTopRight, app.displayBottomLeft, app.displayBottomRight]
    for display in displays:
        if onlyDisplay and display != onlyDisplay:
            continue
        if (
            display.image
            and (display.image != app.displayImages[lookupTab][display]["image"]
                    or app.displayImages[lookupTab][display]["activeTab"] != activeTab
                    or (name and name not in app.displayImages[lookupTab][display]["name"]))
            ):
            display.config(image="")
            display.image=None
            app.displayImages[lookupTab][display]["image"] = None
            app.displayImages[lookupTab][display]["name"] = None
            app.displayImages[lookupTab][display]["activeTab"] = None


def error_popup(root, e):
    log(e, exception=True)
    p = PopupWindow(root, "Error detected!\n\nPlease open a Github issue describing what you were doing\nand include the dsbg_shuffle_log file!  Thanks!\n\nRegardless, please close and reopen the app.", firstButton="Ok")
    root.wait_window(p)


def do_nothing(event=None):
    pass