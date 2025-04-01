import sys

from PyQt5.QtWidgets import QApplication
from Views.GridCreationToolView import PacmanGridCreationToolView


def main()-> None:
    application: QApplication = QApplication([])
    window: PacmanGridCreationToolView = PacmanGridCreationToolView()
    window.show()
    sys.exit(application.exec())


if __name__ == '__main__':
    main()
