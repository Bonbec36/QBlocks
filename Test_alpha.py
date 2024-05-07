import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel, QColorDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Paramètres")

        self.parent = parent

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.background_label = QLabel("Couleur d'arrière-plan :")
        self.layout.addWidget(self.background_label)

        self.background_color = QColor(self.parent.bg_color)

        self.color_button = QPushButton("Choisir une couleur")
        self.color_button.clicked.connect(self.choose_color)
        self.layout.addWidget(self.color_button)

    def choose_color(self):
        color = QColorDialog.getColor(self.background_color, self, "Choisir une couleur")
        if color.isValid():
            self.background_color = color

    def save_settings(self):
        self.parent.bg_color = self.background_color.name()
        self.parent.setStyleSheet(f"background-color: {self.parent.bg_color};")
        self.accept()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Annuler les modifications",
            "Êtes-vous sûr de vouloir annuler les modifications ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fenêtre principale")
        self.setGeometry(300, 300, 400, 200)

        self.bg_color = "#000000"
        self.setStyleSheet(f"background-color: {self.bg_color};")

        self.settings_button = QPushButton("Modifier les paramètres")
        self.settings_button.clicked.connect(self.open_settings_dialog)
        self.settings_button.setGeometry(160, 80, 180, 30)

        self.setCentralWidget(self.settings_button)

    def open_settings_dialog(self):
        dialog = SettingsDialog(self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())