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


def do_nothing(event=None):
    pass