
import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout
)

from PySide6.QtCore import Qt


class LoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("Smart Parking System")
        self.showMaximized()

        # Main widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main title
        title = QLabel("SMART PARKING")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Parking Management System")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setFixedHeight(45)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )
        self.password_input.setFixedHeight(45)

        # Login button
        login_button = QPushButton("LOGIN")
        login_button.setFixedHeight(45)

        # Message
        self.message = QLabel("")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        layout = QVBoxLayout()

        layout.setContentsMargins(40, 55, 40, 55)
        layout.setSpacing(18)

        layout.addWidget(title)
        layout.addWidget(subtitle)

        layout.addSpacing(25)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(self.message)

        central_widget.setLayout(layout)

        # Application styling
        self.setStyleSheet("""

            QMainWindow {
                background-color: #14213D;
            }

            QLabel {
                color: white;
            }

            QLabel:first-child {
                font-size: 28px;
                font-weight: bold;
            }

            QLineEdit {
                background-color: white;
                color: #14213D;
                border: 2px solid #DCE3EA;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 2px solid #3A86FF;
            }

            QPushButton {
                background-color: #3A86FF;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #2563EB;
            }

            QPushButton:pressed {
                background-color: #1D4ED8;
            }

        """)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())
