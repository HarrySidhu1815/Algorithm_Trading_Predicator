from PySide6.QtWidgets import QApplication
from ui.gui import MainWindow


WIN_WIDTH = 1000
WIN_HEIGHT = 500


def run():
    # Create the application
    app = QApplication([])

    # Create and show the main window
    window = MainWindow()
    window.resize(WIN_WIDTH, WIN_HEIGHT)
    window.show()

    # Execute the application
    app.exec()


if __name__ == '__main__':
    run()