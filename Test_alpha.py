from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDialogButtonBox


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        # Création des widgets
        self.number_label = QLabel("Entrez un nombre:")
        self.number_edit = QLineEdit()
        self.item_label = QLabel("Choisissez un élément:")
        self.item_combobox = QComboBox()
        self.item_combobox.addItems(["Item 1", "Item 2", "Item 3"])  # Ajoutez vos éléments ici

        # Boutons de la boîte de dialogue
        buttons = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Placement des widgets dans la boîte de dialogue
        layout = QVBoxLayout()
        layout.addWidget(self.number_label)
        layout.addWidget(self.number_edit)
        layout.addWidget(self.item_label)
        layout.addWidget(self.item_combobox)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

    def get_data(self):
        return self.number_edit.text(), self.item_combobox.currentText()


if __name__ == "__main__":
    app = QApplication([])

    dialog = SettingsDialog(None)
    if dialog.exec_() == QDialog.Accepted:
        number, item = dialog.get_data()
        print("Nombre entré:", number)
        print("Élément choisi:", item)
