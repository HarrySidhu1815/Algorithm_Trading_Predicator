from core.observer import EventPublisher
from services.data_services.data_fetching_service import DataFetchingService
from services.data_services.data_preprocessing_service import DataPreprocessingService
from services.data_services.MarketDatabaseHandler import MarketDatabaseHandler
from services.ml_service.modelTrainingService import ModelTrainingService
from services.ml_service.MLModel import MLModel
from services.prediction_graph_service.graph_printing_service import GraphPrintingService
from other import events
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
connection_string = os.getenv("MONGO_URI")

class Relay():
    def __init__(self, window):
        self.gui = window
        self.publisher = EventPublisher(self.gui.log_message)

    def start_process(self):
        stock_symbol = self.gui.get_stock_selection()
        repository = MarketDatabaseHandler("mongodb+srv://Anmol:Anmol22g@stocks.cf9te.mongodb.net/Stocks?retryWrites=true&w=majority&ssl=true")
        
        model = MLModel()
        data_fetching_service = DataFetchingService(repository, self.publisher)
        data_preprocessing_service = DataPreprocessingService(repository, self.publisher)
        model_training_service = ModelTrainingService(repository, self.publisher, model)
        graph_printing_service = GraphPrintingService(self.display_graph_in_gui, self.publisher)
        
        self.publisher.subscribe(data_fetching_service)
        self.publisher.subscribe(data_preprocessing_service)
        self.publisher.subscribe(model_training_service)
        self.publisher.subscribe(graph_printing_service)
              
        self.publisher.publish({'type': events.START_PROCESS, 'symbol': stock_symbol})
    
    def display_graph_in_gui(self, graph_path):
        print(f"[Relay] Forwarding graph to GUI: {graph_path}")
        self.gui.display_graph(graph_path)
        