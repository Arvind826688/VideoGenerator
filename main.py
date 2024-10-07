# main.py

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from video_generation import generate_video_from_topic

class VideoGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    # Initialize the GUI
    def initUI(self):
        self.setWindowTitle("Video Generator")
        self.setGeometry(300, 300, 400, 200)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Label
        self.label = QLabel("Enter the Topic:")
        self.label.setFont(QFont("Arial", 14))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        # Text input field
        self.text_input = QLineEdit(self)
        self.text_input.setFont(QFont("Arial", 12))
        layout.addWidget(self.text_input)
        
        # Submit button
        self.submit_button = QPushButton("Generate Video", self)
        self.submit_button.setFont(QFont("Arial", 12))
        self.submit_button.clicked.connect(self.on_submit)
        layout.addWidget(self.submit_button)
        
        # Status label
        self.status_label = QLabel("", self)
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Set the layout
        self.setLayout(layout)

    # Function to handle Submit button click
    def on_submit(self):
        topic = self.text_input.text()
        if topic:
            self.status_label.setText("Generating video... please wait.")
            self.repaint()  # Refresh the GUI to show the message

            # Call the video generation function
            try:
                generate_video_from_topic(topic)
                self.status_label.setText("Video generated successfully!")
            except Exception as e:
                self.status_label.setText(f"Error: {str(e)}")
        else:
            self.status_label.setText("Please enter a topic.")

# Main function to run the app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoGeneratorApp()
    window.show()
    sys.exit(app.exec_())
