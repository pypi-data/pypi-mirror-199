__author__ = 'marsson87'
__author_name__ = 'Marek Torberntsson'
__author_email__ = 'marsson87@gmail.com'

from tkinter import *

from preferencesgui import PreferencesGUI


def create_gui(config_json_filename, title=None, width=None, height=None, debug=False):
    # Manage passed arguments
    if not title:
        title = "Flexible Preferences GUI"
    # Set default window size if not defined in class instance
    if not width:
        width = 500
    if not height:
        height = 300

    root = Tk()

    root.resizable(False, False)  # This code helps to disable windows from resizing

    # Remove the Title bar of the window
    # root.overrideredirect(True)

    PreferencesGUI(root, config_json_filename, title, width, height, debug)

    root.unbind_all('<<NextWindow>>')  # Unbinding the behavior that causes Tab Cycling
    root.mainloop()


if __name__ == "__main__":
    create_gui(config_json_filename='conf.json')
