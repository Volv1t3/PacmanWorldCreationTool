#!------------------------------------
"""
@Author: Santiago Arellano
@Date: 28th March 2025
@Description: The following file contains information pertaining the main specification for the Pacman grid creation
tool view. It contains functions defined such that the view is managed appropriately, including small controller
implementations to handle view modifications and backend connections. The idea of this file is to implement the following:
1. Clear component layout that includes:
    1) side panel for color choosing (left view),
    2) side panel for grid manipulation (right view)
    3) top menu item buttons for exporting into clipboard or file
2. Clear backend communication to procure the translation of the grid to a text based clipboard intent, or file based
intent.
"""
#!-------------------------------------
from PyQt5.QtWidgets import (
                            QApplication,
                            QMainWindow,
                            QRadioButton,
                            QButtonGroup,
                            QSplitter,
                            QVBoxLayout,
                            QGridLayout,
                            QMenuBar,
                            QMenu,
                            QAction)



class PacmanGridCreationToolView(QMainWindow):
    def __init__(self):
        super().__init__();