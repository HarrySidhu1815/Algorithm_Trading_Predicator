from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QComboBox, QLabel, QTextEdit
from core.controller import Relay
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QFileSystemWatcher, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Algorithm Trading Graph Printing Application") # Setting the title of the window
        self.controller = Relay(self)  # Bind controller
        
        central_widget = QWidget() # Creating a central widget
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout() # Creating the layout
        
        stock = ["AAPL", "AMD", "AMZN", "BA", "BABA", "BAC", "C", "CSCO", "CVX", "DIS", "F", "GE", "GOOGL", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "META", "MSFT", "NFLX", "NVDA", "PFE", "PLTR", "T", "TSLA", "VZ", "WMT", "XOM"]

        # Add heading
        heading = QLabel("Welcome to the Application")
        heading.setObjectName("mainHeading")
        layout.addWidget(heading, alignment=Qt.AlignHCenter)

        # Add paragraph
        paragraph = QLabel(
            "This is a simple application focusing on the design and pattern used for the application. "
            "You can predict the prices of the any stocks in a given list"
            "We will enhance the appearance and functionality of the application in the future"
        )
        paragraph.setWordWrap(True)  # Enable word wrapping for multiline text
        paragraph.setObjectName("paragraph")
        layout.addWidget(paragraph)
        
        # Stock selection dropdown
        self.stock_dropdown = QComboBox()
        self.stock_dropdown.addItems(stock)
        self.stock_dropdown.setObjectName("stockDropdown")
        
        layout.addWidget(QLabel("Select Stock:"))
        layout.addWidget(self.stock_dropdown)
        
        # Creating the button
        button = QPushButton("Start Process")
        button.setObjectName("startProcess")
        button.clicked.connect(self.start_process)
        layout.addWidget(button, alignment=Qt.AlignHCenter)
        
        # Logging area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setObjectName("logArea")
        layout.addWidget(self.log_area)
        
        # Graph placeholder
        self.graph_label = QLabel("Graph will appear here")
        self.graph_label.setScaledContents(True)
        self.graph_label.setObjectName("graph")

        layout.addWidget(self.graph_label)

        # Setting the layout for the central widget
        central_widget.setLayout(layout)
        
        # Watch the QSS file for changes
        self.watcher = QFileSystemWatcher(["styles.qss"])
        self.watcher.fileChanged.connect(self.apply_styles)

        # Apply the initial styles
        self.apply_styles()

    # Delegation
    def start_process(self):
        self.controller.start_process()
    
    def get_stock_selection(self):
        return self.stock_dropdown.currentText()

    def display_graph(self, graph_path):
        self.graph_label.setPixmap(QPixmap(graph_path))
    
    def log_message(self, message: str):
        # Update the logging area with a new message.
        self.log_area.append(message)
        
    def apply_styles(self):
        try:
            with open("styles.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("QSS file not found.")
