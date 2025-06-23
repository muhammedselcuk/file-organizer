import sys
from PySide6.QtWidgets import QApplication
from src.gui import FileOrganizerApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec())