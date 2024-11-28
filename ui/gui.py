from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting the title of the window
        self.setWindowTitle("Single Button UI")

        # Creating a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Creating the layout
        layout = QVBoxLayout()

        # Creating the button
        button = QPushButton("Click Me")
        layout.addWidget(button)

        # Setting the layout for the central widget
        central_widget.setLayout(layout)