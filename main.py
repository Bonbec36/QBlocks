import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtWidgets import QLabel,QStackedWidget, QListWidget, QListWidgetItem, QHBoxLayout
from PyQt6 import QtCore

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application avec page d'accueil")
        self.setGeometry(100, 100, 600, 400)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_page = WelcomePage()
        self.another_page = AnotherPage()

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.another_page)

        self.home_page.button.clicked.connect(self.show_another_page)
        self.another_page.button.clicked.connect(self.show_home_page)

    def show_another_page(self):
        self.stacked_widget.setCurrentWidget(self.another_page)

    def show_home_page(self):
        self.stacked_widget.setCurrentWidget(self.home_page)


class WelcomePage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.welcome_label = QLabel("Bienvenue sur Quantum Blocks !")
        self.welcome_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.welcome_label)

        self.button = QPushButton("Aller au lab")
        layout.addWidget(self.button)


class AnotherPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.label = QLabel("Quantum Labs !")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

            # Créez quelques objets Item
        items = [
            Item("H", ""),
            Item("X", ""),
            Item("Psi", "")
        ]

                # Création d'une boîte horizontale pour contenir la liste et l'espace réservé
        hbox_layout = QHBoxLayout()

        # Créez un QListWidget pour afficher la liste d'objets
        list_widget = QListWidget()
        list_widget.resize(50, 300)

        for item in items:
            list_item = QListWidgetItem(f"{item.name} - {item.description}")
            list_widget.addItem(list_item)

        spacer_label = QLabel()
        spacer_label.setFixedSize(500, 300)  # Largeur : 50 pixels, Hauteur : 300 pixels

        # Ajoutez le QLabel et le QListWidget à la boîte horizontale
        hbox_layout.addWidget(list_widget)
        hbox_layout.addWidget(spacer_label)

        layout.addLayout(hbox_layout)

        self.button = QPushButton("Retour à l'accueil")
        layout.addWidget(self.button)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
