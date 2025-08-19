import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import subprocess

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gesture Control App")
        self.setGeometry(300, 100, 500, 400)  # Bigger window
        self.setStyleSheet("background-color: #1E1E2F; color: white;")

        central_widget = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("Gesture Control App")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("margin-bottom: 30px;")
        layout.addWidget(title)

        # Start Gesture Control Button
        self.start_btn = QPushButton("▶ Start Gesture Control")
        self.start_btn.setFont(QFont("Arial", 14))
        self.start_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            """
        )
        self.start_btn.clicked.connect(self.start_gesture_app)
        layout.addWidget(self.start_btn)

        # Settings Button
        settings_btn = QPushButton("⚙ Settings")
        settings_btn.setFont(QFont("Arial", 14))
        settings_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2196F3;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            """
        )
        settings_btn.clicked.connect(self.open_settings)
        layout.addWidget(settings_btn)

        # About Button
        about_btn = QPushButton("ℹ About")
        about_btn.setFont(QFont("Arial", 14))
        about_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #FF9800;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #FB8C00;
            }
            """
        )
        about_btn.clicked.connect(self.open_about)
        layout.addWidget(about_btn)

        # Status Label
        self.status_label = QLabel("Status: Idle")
        self.status_label.setFont(QFont("Arial", 12))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("margin-top: 20px; color: #FFEB3B;")
        layout.addWidget(self.status_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_gesture_app(self):
        # Launch your gesture app
        try:
            subprocess.Popen(
                r"C:\Users\Sheeja Narayanan\Downloads\hand_tracking_project\gesture-app\dist\app.exe"
            )
            self.status_label.setText("Status: Running Gesture App")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    def open_settings(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Settings")
        dlg.setGeometry(350, 150, 300, 200)
        label = QLabel("Settings options will go here.", dlg)
        label.setAlignment(Qt.AlignCenter)
        dlg.exec()

    def open_about(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("About")
        dlg.setGeometry(350, 150, 300, 200)
        label = QLabel("Gesture Control App\nVersion 1.0\nBy Anusha", dlg)
        label.setAlignment(Qt.AlignCenter)
        dlg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())
