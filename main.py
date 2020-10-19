import sys
from PyQt5.QtWidgets import QApplication
from gui import Window


def main():
    app = QApplication([])
    win = Window()
    win.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
