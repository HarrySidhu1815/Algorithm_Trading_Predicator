from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QComboBox, QLabel
from core.controller import Relay
from PySide6.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Single Button UI") # Setting the title of the window
        self.controller = Relay(self)  # Bind controller
        
        central_widget = QWidget() # Creating a central widget
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout() # Creating the layout
        
        stock = ["AAPL", "AMD", "AMZN", "BA", "BABA", "BAC", "C", "CSCO", "CVX", "DIS", "F", "GE", "GOOGL", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "META", "MSFT", "NFLX", "NVDA", "PFE", "PLTR", "T", "TSLA", "VZ", "WMT", "XOM"]

        # Stock selection dropdown
        self.stock_dropdown = QComboBox()
        self.stock_dropdown.addItems(stock)  # Example stocks
        layout.addWidget(QLabel("Select Stock:"))
        layout.addWidget(self.stock_dropdown)
        
        # Creating the button
        button = QPushButton("Start Process")
        button.clicked.connect(self.start_process)
        layout.addWidget(button)
        
        # Graph placeholder
        self.graph_label = QLabel("Graph will appear here")
        self.graph_label.setScaledContents(True)  # Ensure the graph scales properly
        layout.addWidget(self.graph_label)

        # Setting the layout for the central widget
        central_widget.setLayout(layout)

    # Delegation
    def start_process(self):
        self.controller.start_process()
    
    def get_stock_selection(self):
        return self.stock_dropdown.currentText()

    def display_graph(self, graph_path):
        self.graph_label.setPixmap(QPixmap(graph_path))
