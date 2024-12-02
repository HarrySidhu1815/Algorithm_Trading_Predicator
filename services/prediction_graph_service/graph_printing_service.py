import matplotlib.pyplot as plt
from typing import Any
from core.observer import EventObserver
from other import events
from core.observer import EventPublisher

class GraphPrintingService(EventObserver):
    def __init__(self, relay_callback, publisher: EventPublisher):
        self.relay_callback = relay_callback
        self.publisher = publisher

    def on_event(self, event: Any) -> None:
        if self.is_interested_in(event):
            symbol = event['symbol']
            print(f"[GraphPrintingService] Received data for {symbol}. Generating graphs...")

            # Extract the data
            target_1D_predictions = event['target_1D_predictions']
            target_5D_predictions = event['target_5D_predictions']
            target_1D_original_data = event['target_1D_original_data']
            target_5D_original_data = event['target_5D_original_data']

            # Plot graphs and save as image
            graph_path = "output_graph.png"
            self.plot_graph(
                target_1D_original_data,
                target_1D_predictions,
                target_5D_original_data,
                target_5D_predictions,
                graph_path,
                title=f"Stock Predictions for {symbol}",
            )

            # Notify Relay with the graph path
            self.relay_callback(graph_path)
            
            # Notify that the graph is printed
            self.publisher.publish({
                'type': events.GRAPH_PRINTED,
            })

    def is_interested_in(self, event: Any) -> bool:
        return event.get('type') == 'ML_UPDATED'

    def plot_graph(self, original_1D, predicted_1D, original_5D, predicted_5D, save_path, title):
        # Plot a combined graph comparing original and predicted values for 1D and 5D.
        plt.figure(figsize=(12, 6))

        # Subplot for 1D predictions
        plt.subplot(1, 2, 1)
        plt.plot(original_1D, label="Original 1D", color="blue")
        plt.plot(predicted_1D, label="Predicted 1D", color="orange", linestyle="--")
        plt.title("1D Predictions")
        plt.xlabel("Time Steps")
        plt.ylabel("Target Value")
        plt.legend()

        # Subplot for 5D predictions
        plt.subplot(1, 2, 2)
        plt.plot(original_5D, label="Original 5D", color="green")
        plt.plot(predicted_5D, label="Predicted 5D", color="red", linestyle="--")
        plt.title("5D Predictions")
        plt.xlabel("Time Steps")
        plt.ylabel("Target Value")
        plt.legend()

        plt.suptitle(title)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
