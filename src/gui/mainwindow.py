"""
Main window of the application
"""

import sys

from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Local imports
from scraper import retrieve_album_lists


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Disc List Scout: Music Discovery")
        self.setGeometry(100, 100, 600, 400)  # x, y, width, height

        layout = QVBoxLayout()

        # Album input field and label
        self.album_input = QLineEdit(self)
        album_label = QLabel("Enter Album Name:", self)
        layout.addWidget(album_label)
        layout.addWidget(self.album_input)

        # Retrieve button
        self.retrieve_button = QPushButton("Find Lists", self)
        layout.addWidget(self.retrieve_button)

        # Status information display
        self.status_label = QLabel("Status: Ready", self)
        layout.addWidget(self.status_label)

        # Setting the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect buttons to functions (to be implemented)
        self.retrieve_button.clicked.connect(self.retrieve_album_lists)

    def retrieve_album_lists(self):
        album_name = self.album_input.text()
        result = retrieve_album_lists(album_name)
        self.status_label.setText(result)


# For testing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
