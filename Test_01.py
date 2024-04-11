from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QPushButton, QVBoxLayout, QWidget, QLabel


class CustomGraphicsView1(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene())
        self.setSceneRect(0, 0, 400, 300)
        self.title_label = QLabel("View 1")
        self.scene().addWidget(self.title_label)
        self.saved_items = []  # Initialisation de la liste saved_items

    def save_scene_elements(self):
        # Exemple de sauvegarde d'éléments de scène
        items = self.scene().items()
        self.saved_items = [item for item in items]
        print("Saved items in View 1:", self.saved_items)

    def restore_scene_elements(self):
        # Exemple de restauration d'éléments de scène
        for item in self.saved_items:
            self.scene().addItem(item)
        print("Restored items in View 1:", self.saved_items)


class CustomGraphicsView2(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene())
        self.setSceneRect(0, 0, 400, 300)
        self.title_label = QLabel("View 2")
        self.scene().addWidget(self.title_label)
        self.saved_items = []  # Initialisation de la liste saved_items

    def save_scene_elements(self):
        # Exemple de sauvegarde d'éléments de scène
        items = self.scene().items()
        self.saved_items = [item for item in items]
        print("Saved items in View 2:", self.saved_items)

    def restore_scene_elements(self):
        # Exemple de restauration d'éléments de scène
        for item in self.saved_items:
            self.scene().addItem(item)
        print("Restored items in View 2:", self.saved_items)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.current_view = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        button_view1 = QPushButton("View 1")
        button_view1.clicked.connect(self.show_view1)
        layout.addWidget(button_view1)

        button_view2 = QPushButton("View 2")
        button_view2.clicked.connect(self.show_view2)
        layout.addWidget(button_view2)

        self.current_view = CustomGraphicsView1()
        layout.addWidget(self.current_view)

        self.setLayout(layout)

    def show_view1(self):
        if isinstance(self.current_view, CustomGraphicsView2):
            self.current_view.save_scene_elements()
        self.current_view = CustomGraphicsView1()
        self.layout().replaceWidget(self.layout().itemAt(2).widget(), self.current_view)
        self.current_view.restore_scene_elements()

    def show_view2(self):
        if isinstance(self.current_view, CustomGraphicsView1):
            self.current_view.save_scene_elements()
        self.current_view = CustomGraphicsView2()
        self.layout().replaceWidget(self.layout().itemAt(2).widget(), self.current_view)
        self.current_view.restore_scene_elements()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
