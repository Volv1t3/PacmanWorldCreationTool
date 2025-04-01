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
# !-------------------------------------
import os

from PyQt5.QtCore import QFile, Qt, QRect, QRectF, QEvent
from PyQt5.QtGui import QTextBlock, QFont, QColor, QPen, QMouseEvent
from PyQt5.QtWidgets import (
    QMainWindow,
    QRadioButton,
    QButtonGroup,
    QSplitter,
    QVBoxLayout,
    QGridLayout,
    QMenuBar,
    QMenu,
    QAction, QWidget, QApplication, QFileDialog, QMessageBox, QLabel, QHBoxLayout, QGraphicsScene, QGraphicsView,
    QGraphicsSceneMouseEvent)
from mistune.plugins.table import ALIGN_RIGHT

from Models.PacmanGrid import PacmanGrid


class PaintingMode:
    SINGLE_CELL_PAINTING_MODE = 0
    MULTI_CELL_PAINTING_MODE = 1
    SINGLE_CELL_ERASURE_MODE = 2
    MULTI_CELL_ERASURE_MODE = 3


class PacmanGridCreationToolView(QMainWindow):
    def __init__(self):
        # ! 1. Required call to initialize the backend for Qt
        super().__init__();
        # ! 2. Setting up view information, sizing, constraints, view title, etc.
        self.setWindowTitle("Pacman Grid Creation Tool "
                            "- Santiago Arellano - eVolvLabs")  # ? Defines main Window title
        self.setBaseSize(1200, 500);
        super().setMinimumSize(1200, 500);
        self.setStyleSheet("background-color: #FFFFF; color: black;");  # ? Defines main window background color

        # ! 3. Setting up internal instance variables like in Java!
        self.internalColorDefinitions: dict[str, str] = {
            '#00001F': '001F',  # Borders are now blue!
            '#FFDE59': '6767',  # Pacman remains yellow
            '#E4080A': 'F08A',  # Ghost One stays red
            '#5DE2E7': '1BFE',  # Ghost two is cyan!
            '#EFC3CA': 'FDDC',  # Ghost three is pink!
            '#7DDA58': '0F00',  # Ghost four is green!
            '#FFFFFF': 'FFFF',  # Normal PowerUps are  now white!
            '#FE9900': 'F5A0'  # Eat Others PowerUps is now yellow!
        }
        self.internalColorLabels: list[str] = ["Color For Borders",
                                               "Color For Pacman",
                                               "Color For Ghost One",
                                               "Color For Ghost Two",
                                               "Color For Ghost Three",
                                               "Color For Ghost Four",
                                               "Color For Normal Power Ups",
                                               "Color For Eat Others Power Ups"]
        self.colorButtonGroup: QButtonGroup = QButtonGroup(self)
        self.internallySelectedColor: str = ""
        self.internalPacmanGridInstance: PacmanGrid = PacmanGrid()
        self.menuBarForExportingOptions: QMenuBar = None;
        self.splitterForHorizontalMovement: QSplitter = None;
        self.vBoxForButtonPlacement: QVBoxLayout = None;
        self.gridLayoutForSelection: QGridLayout = None;
        # ! 4. Setting up main application UI
        self.centralWidgetForLayoutHandling: QWidget = QWidget();
        self.setCentralWidget(self.centralWidgetForLayoutHandling)
        self.__init__UI__()

    def __init__UI__(self):
        # ? 1. Configuring the menu information for exporting the data.
        self.__configuring__menu__information__()

        # ? 2. In PyQT we need to add components into a Layout, which is kind of like Android, in a way,
        # ? and onto this layout we need to add different components that can help us create the look and feel
        # ? of our application. JavaFX is much simpler but everyone seems to want to use python nowadays.
        hBoxLayoutForButtonsAndGrid: QHBoxLayout = QHBoxLayout(self)
        hBoxLayoutForButtonsAndGrid.setSpacing(20)
        hBoxLayoutForButtonsAndGrid.setContentsMargins(10, 10, 10, 10)
        hBoxLayoutForButtonsAndGrid.setAlignment(self, Qt.AlignVCenter)
        hBoxLayoutForButtonsAndGrid.setDirection(QHBoxLayout.Direction.LeftToRight)

        # ? 3. Within ths horizontal layout I need to add one side panel for the buttons that will
        # ? hold the connection to all colors in our app. Instead of directly adding widgets into the layout
        # ? Qt recommends we add a widget before and group elements within that group before we add elements
        # ? to the main view in general. This is mirrored in the gridview
        buttonWidget = QWidget()
        self.vBoxForButtonPlacement = QVBoxLayout(buttonWidget)
        self.vBoxForButtonPlacement.setSpacing(20)
        buttonWidget.setStyleSheet(
            """
            QWidget {
                background-color: beige;
                border: 2px solid #00001F;
                border-radius: 10px;
                padding: 10px;
            }
            """
        )
        self.vBoxForButtonPlacement.setDirection(QVBoxLayout.Direction.TopToBottom)
        self.vBoxForButtonPlacement.setAlignment(self, Qt.AlignVCenter | Qt.AlignTop)

        #? 4. Somewhat like Android, we have a GridLayout instead of a GridPane, the cols and rows are NOT
        #? defined by default, that is what our initial configuration method takes care of. You have to create
        #? each cell by default with some content. One idea was to use a graphics view, kind of create a cute graphics view
        #? but although the visuals were good the controllers were horrible. Instead I ended up working with cells (widgets)
        #? where all I do is handle listeners for clicks.
        gridWidget = QWidget()
        self.gridLayoutForSelection = QGridLayout(gridWidget)
        self.gridLayoutForSelection.setContentsMargins(0, 0, 0, 0)

        #? 5. This is the splitter section, this is similar to a SplitPane in JavaFX, only that it does not show up
        #?until you pass over it, I am going to try make it visible
        self.splitterForHorizontalMovement = QSplitter(self)
        self.splitterForHorizontalMovement.addWidget(buttonWidget)
        self.splitterForHorizontalMovement.addWidget(gridWidget)
        self.splitterForHorizontalMovement.setStyleSheet("""
            QSplitter::handle {
                background-color: transparent;
                border-right: 2px dashed black;
                width: 4px;
                height: 100%;
            }
        """)
        self.splitterForHorizontalMovement.setHandleWidth(4)
        self.splitterForHorizontalMovement.setChildrenCollapsible(False)

        #?6. Now we add the splitter to the original main layout
        hBoxLayoutForButtonsAndGrid.addWidget(self.splitterForHorizontalMovement)

        #? 7. Add the main layout into the central widget where all UI elements are rendered
        self.centralWidget().setLayout(hBoxLayoutForButtonsAndGrid)

        #? 8. Configuration calls
        self.__configuring_vBoxWithButtons()
        self.__configuring_gridViewWithCells()

    def __configuring__menu__information__(self) -> None:
        # ? 1. Creating a MenuBar that will be handled by the application MainWindow
        self.menuBarForExportingOptions = self.menuBar()
        # ? 2. Creating a Menu that can hold two menu items, one to export to file and one to export
        # ? down to the clipboard
        # Step one: create a menu, this is the easy part as we are doing the same as JavaFX
        menuForExportingOptions: QMenu = self.menuBarForExportingOptions.addMenu("Exporting Layout Options")
        menuForExportingOptions.setStyleSheet("""
            QMenu {
                background-color: beige;
                color: black;
                border: 1px solid black;
                padding: 5px;
                border-radius: 5px;
            }
            """)
        menuItemForClipboardExporting = QAction("Export To Clipboard", self)
        menuItemForFileExporting = QAction("Export To TXT File", self)
        menuForExportingOptions.addAction(menuItemForClipboardExporting)
        menuForExportingOptions.addAction(menuItemForFileExporting)
        menuItemForClipboardExporting.triggered.connect(self.__handle_user_exporting_to_clipboard_event)
        menuItemForFileExporting.triggered.connect(self.__handle_user_exporting_to_file_event)

    def __handle_user_exporting_to_clipboard_event(self) -> None:
        # ? 1. The first thing we need to do here is access the clipboard
        clipboardObjectForExporting = QApplication.clipboard()

        # ? 2. We load now the text that comes from the internal object
        clipboardObjectForExporting.setText(self.internalPacmanGridInstance.__str__())

    def __handle_user_exporting_to_file_event(self) -> None:
        # ? 1. Similarly to JavaFX FileChooser dialog, we need to use a FileDialog here
        fileDialogForUserToDefineWhereToSaveTXT: QFileDialog = QFileDialog(self,
                                                                           "Save your Grid Layout TXT File to...",
                                                                           os.path.expanduser('~'))
        # ! This method defines that the user should be shown Any and all files in their system, we could set it to folders,
        # ! but I think this is a good start
        fileDialogForUserToDefineWhereToSaveTXT.setFileMode(QFileDialog.FileMode.AnyFile)
        # ! This method defines that the user should be shown only TXT files
        fileDialogForUserToDefineWhereToSaveTXT.setNameFilter("Text Files (*.txt)")
        # ! This method defines that the user can only save files, they can't open them, in JavaFX we were used to
        # ! both saving and opening, kjust like this!!!
        fileDialogForUserToDefineWhereToSaveTXT.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        # ! This last configuration method tells the program to add the .txt suffix if the user simply enters a name!
        # ! quite handy
        fileDialogForUserToDefineWhereToSaveTXT.setDefaultSuffix("txt")

        # ? 2. We now await for the user to define a name
        if fileDialogForUserToDefineWhereToSaveTXT.exec() == QFileDialog.DialogCode.Accepted:
            # ? 2.1 We grab the file names, either selected or inputted by the user
            selectedFileNames: list[str] = fileDialogForUserToDefineWhereToSaveTXT.selectedFiles()
            # ? 2.2 We grab the first file name, this is the one that the user selected or inputted
            selectedFileName: str = selectedFileNames[0]
            print(selectedFileNames)
            print(selectedFileName)
            if len(selectedFileName) > 0:
                # ? 2.3 We now need to write the file, we need to open it, write to it, and close it
                fileToWriteTo: QFile = QFile(selectedFileName)
                if fileToWriteTo.open(QFile.OpenModeFlag.WriteOnly):
                    # ? 2.4 We now need to write the file, we need to write the text to the file
                    fileToWriteTo.write(self.internalPacmanGridInstance.__str__().encode('utf-8'))
                    fileToWriteTo.close()
                else:
                    # ? 2.5 If the file could not be opened, we need to show an error message
                    QMessageBox.critical(self, "Error", "Could not open file to write to")
        elif fileDialogForUserToDefineWhereToSaveTXT.exec() == QFileDialog.DialogCode.Rejected:
            # ? 2.3 If the user cancels the dialog, we need to do nothing
            return

    def __configuring_vBoxWithButtons(self) -> None:
        # Increase the spacing between elements
        self.vBoxForButtonPlacement.setSpacing(20)
        self.vBoxForButtonPlacement.setContentsMargins(10, 10, 10, 10)

        # Modify the text block
        textBlock = QLabel("Choose a color by clicking on its icon")
        textBlock.setFont(QFont("Microsoft YaHei UI", 14, QFont.Bold))
        textBlock.setStyleSheet("""
            QLabel {
                color: black;
                padding: 5px;
                margin-bottom: 10px;
            }
        """)
        textBlock.setWordWrap(True)
        textBlock.setFixedWidth(200)
        self.vBoxForButtonPlacement.addWidget(textBlock)

        for i, (color, name) in enumerate(zip(self.internalColorDefinitions.keys(), self.internalColorLabels)):
            radioButton = QRadioButton(name)
            radioButton.setStyleSheet(f"""
                QRadioButton {{
                    background-color: #CECECE;
                    color: black;
                    padding: 5px;
                    margin: 5px;
                }}
                QRadioButton::indicator {{
                    width: 15px;
                    height: 15px;
                    color: {color};
                }}
                QRadioButton::indicator:unchecked {{
                    border: 2px solid {color};
                    border-radius: 9px;
                    background-color: transparent;
                }}
                QRadioButton::indicator:checked {{
                    border: 2px solid {color};
                    border-radius: 9px;
                    background-color: {color};
                }}
            """)
            self.colorButtonGroup.addButton(radioButton, i)
            self.vBoxForButtonPlacement.addWidget(radioButton, i + 1, Qt.AlignTop | Qt.AlignLeft)

        self.colorButtonGroup.buttonClicked.connect(self.handle_radio_button_for_colors_clicked)

    def __configuring_gridViewWithCells(self) -> None:
        self.is_painting: bool = False;
        self.painting_mode: int = PaintingMode.SINGLE_CELL_PAINTING_MODE;
        self.last_painted_cell: tuple[int, int] = (-1, -1);
        # ? Lets create a 16x16 view within the gridcell to handle both column and row
        for row in range(0, 16, 1):
            for col in range(0, 16, 1):
                # ? 1. Create a cell to store the data, add a listener and change colors depending on user
                # ? selection
                cellForColoring: QWidget = QWidget()
                cellForColoring.setMouseTracking(True)
                cellForColoring.setFixedSize(30, 30)
                # ! 1.1 Give the base color and width
                cellForColoring.setStyleSheet("""
                   QWidget {
                    background-color: whitesmoke;
                    border: 1px solid lightgray;
                }
                QWidget:hover {
                    background-color: #e0e0e0;
                }
                """)
                # ? 2. Store the cell's info into the cell such that we can use it later to put the information
                # ? in the model
                cellForColoring.row = row
                cellForColoring.col = col
                # ? 3. Conectamos con un listener para poder registrar los cambios de la app,
                cellForColoring.mousePressEvent = lambda event, r=row, c=col: (
                    self.handle_cell_clicked_for_painting(event,r, c))
                cellForColoring.mouseDoubleClickEvent = lambda event, r=row,c=col: (
                    self.handle_cell_clicked_for_painting(event, r, c))
                cellForColoring.mouseReleaseEvent = lambda event, r=row, c=col: (
                    self.handle_mouse_release())
                cellForColoring.mouseMoveEvent = lambda event, r=row, c=col: (
                    self.handle_mouse_move(event, r, c))
                # ? 4. Add the cell to the grid
                self.gridLayoutForSelection.addWidget(cellForColoring, row, col)

    def handle_radio_button_for_colors_clicked(self, buttonSelected: QRadioButton) -> None:
        index: int = self.colorButtonGroup.id(buttonSelected)
        self.internallySelectedColor = list(self.internalColorDefinitions.keys())[index]

    def handle_mouse_release(self):
        self.is_painting = False
        self.last_painted_cell = (-1, -1)

    def handle_mouse_move(self, event: QMouseEvent, row: int, col: int) -> None:

        # Check if we're in brush mode (Ctrl pressed) and left button is being held
        if (event.modifiers() & Qt.KeyboardModifier.ControlModifier and
                self.painting_mode == PaintingMode.MULTI_CELL_PAINTING_MODE):
            # Avoid painting the same cell multiple times
            if (row, col) != self.last_painted_cell:
                self.cell_painting(row, col)
                self.last_painted_cell = (row, col)
        elif (event.modifiers() & Qt.KeyboardModifier.ControlModifier and
                self.painting_mode == PaintingMode.MULTI_CELL_ERASURE_MODE):
            if (row, col) != self.last_painted_cell:
                self.clear_painting(row, col)

    def handle_cell_clicked_for_painting(self, eventFromCell: QMouseEvent,
                                         rowFromCell: int,
                                         colFromCell: int):
        if (eventFromCell.button() == Qt.MouseButton.RightButton and
                eventFromCell.type() == QMouseEvent.MouseButtonDblClick):
            self.clear_entire_graph()
            eventFromCell.accept()
            return
        elif eventFromCell.button() == Qt.MouseButton.LeftButton:
            self.painting_mode = (PaintingMode.MULTI_CELL_PAINTING_MODE
                                  if eventFromCell.modifiers() &
                                     Qt.KeyboardModifier.ControlModifier
                                  else PaintingMode.SINGLE_CELL_PAINTING_MODE)
            self.is_painting = True
            self.cell_painting(rowFromCell, colFromCell)
        elif eventFromCell.button() == Qt.MouseButton.RightButton:
            self.painting_mode = (PaintingMode.MULTI_CELL_ERASURE_MODE
                                  if eventFromCell.modifiers() &
                                     Qt.KeyboardModifier.ControlModifier
                                  else PaintingMode.SINGLE_CELL_ERASURE_MODE)
            self.is_painting = True
            self.clear_painting(rowFromCell, colFromCell)





    def cell_painting(self, rowFromCell: int, colFromCell: int) -> None:
        if not self.internallySelectedColor:
            QMessageBox.warning(
                self,
                "No Color Selected",
                "Please select a color from the tools before painting.",
                QMessageBox.StandardButton.Ok
            )
            return
        validationResults: bool = self.internalPacmanGridInstance.setValueOnGridCell(
            rowFromCell, colFromCell, self.internallySelectedColor
        )
        if validationResults:
            # ? Update cell visual style to match selected color
            cell: QWidget = (self.gridLayoutForSelection.itemAtPosition
                             (rowFromCell, colFromCell).widget())
            cell.setStyleSheet(f"""
                QWidget {{
                    background-color: {self.internallySelectedColor};
                    border: 1px solid gray;
                }}
                """)
        else:
            QMessageBox.warning(
                self,
                "Invalid Placement",
                "You cannot place a color here.",
                QMessageBox.StandardButton.Ok
            )


    def clear_painting(self, rowFromCell: int, colFromCell: int):
        # ? We here clear the view from the color, this can be useful to delete information quickly
        # ? or to clear a cell
        self.internalPacmanGridInstance.clearValueFromGridCell(rowFromCell, colFromCell)
        cell: QWidget = (self.gridLayoutForSelection.itemAtPosition
                         (rowFromCell, colFromCell).widget())
        cell.setStyleSheet("""
                        QWidget {
                            background-color: whitesmoke;
                            border: 1px solid lightgrey;
                        }
                        """)
    def clear_entire_graph(self):
        # ? We here clear the view from the color, this can be useful to delete information quickly
        # ? or to clear a cell
        for row in range(0, 16, 1):
            for col in range(0, 16, 1):
                cell: QWidget = (self.gridLayoutForSelection.itemAtPosition
                                 (row, col).widget())
                cell.setStyleSheet("""
                                QWidget {
                                    background-color: whitesmoke;
                                    border: 1px solid lightgrey;
                                }
                                """)
                self.internalPacmanGridInstance.clearValueFromGridCell(row, col)

