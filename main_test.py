
import sys
from time import sleep

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGraphicsView 
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QListWidget, QListWidgetItem, QWidget
from PyQt6.QtWidgets import QGraphicsItem, QPushButton, QGraphicsRectItem, QGraphicsLineItem
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QColor, QDragMoveEvent, QTransform, QPen
from PyQt6.QtCore import Qt, QMimeData, QDataStream, QIODevice, QEvent, QTimer, QPointF, QRectF

#____________________________________________________________________
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import Sampler
from qiskit.visualization import plot_histogram
from Functions import convert_grid_to_quantum_circuit


class Block:
    """
    C'est une classe qui s'occupe de gerer la position des blocks et tous leurs paramètres
    """
    def __init__(self, identifier, position, logical_number, image_path):
        self.identifier = identifier
        self.position = position
        self.logical_number = logical_number
        self.image_path = image_path

class ItemSprite:
    """
    C'est une classe qui s'occupe de gerer la position des items
    """
    def __init__(self, item_name, item_description, image_path, identifiant):
        self.name = item_name
        self.description = item_description
        self.image_path = image_path
        self.identifiant = identifiant

class SandboxScene(QGraphicsScene):
    """
    C'est une classe qui permet de gérer la sandbox, c'est à dire l'endroit où l'on place les blocks
    """
    def __init__(self, parent_window, grid_size=(10, 10)):
        super().__init__()
        self.grid_size = grid_size
        self.parent_window = parent_window
        self.scale = 50
        self.stream_number = 0
        self.grid = [[None for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]
        self.block_lines = {}  # Initialisation de l'attribut block_lines

        self.add_grid()

    def add_grid(self):
        # Définir la couleur de la grille
        grid_color = QColor(200, 200, 200, 100)  # Gris clair

        # Parcourir toutes les cellules de la grille
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                # Créer un rectangle pour chaque cellule de la grille
                rect = QGraphicsRectItem(i * 50, j * 50, 50, 50)
                rect.setPen(grid_color)  # Définir la couleur de la bordure
                rect.setBrush(QColor(255, 255, 255, 0))  # Définir la couleur de fond (transparent)
                self.addItem(rect)  # Ajouter le rectangle à la scène

    
    #Ajouter le flux quantique
    def add_quantum_stream(self, start_point, stream_id):
        line = QGraphicsLineItem(start_point[0] + 0.5 * self.scale, start_point[1] + 0.5 * self.scale,
                                self.grid_size[1] * 50, start_point[1] + 0.5 * self.scale)
        pen = QPen(QColor("blue"))
        pen.setWidth(2)
        line.setPen(pen)

        # Définir l'identifiant du flux pour cette ligne
        #line.setData(0, "2")  # Identifier le bloc associé à ce flux
        line.setData(1, stream_id)  # Identifier ce flux en particulier

        self.addItem(line)

        """
        if block_id in self.block_lines:
            self.block_lines[block_id].append(line)
        else:
            self.block_lines[block_id] = [line]
        """

    """def add_classical_stream(self, start_point, block_id, stream_id):
        line = QGraphicsLineItem(start_point[0] + 0.5 * self.scale, start_point[1] + 0.5 * self.scale,
                                 self.grid_size[1] * 50, start_point[1] + 0.5 * self.scale)
        pen = QPen(QColor("magenta"))
        pen.setWidth(1)
        line.setPen(pen)
        self.addItem(line)

        # Définir l'identifiant du flux pour cette ligne
        line.setData(0, block_id)  # Identifier le bloc associé à ce flux
        line.setData(1, stream_id)  # Identifier ce flux en particulier


        if block_id in self.block_lines:
            self.block_lines[block_id].append(line)
        else:
            self.block_lines[block_id] = [line]
            """
    
    def add_block(self, block):
        grid_x, grid_y = self.pixel_to_grid(block.position)

        pixmap = QPixmap(block.image_path)
        scaled_pixmap = pixmap.scaled(50, 50)
        pixmap_item = QGraphicsPixmapItem(scaled_pixmap)
        pixmap_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        pixmap_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.addItem(pixmap_item)

        # Définir l'attribut 'id' pour le QGraphicsPixmapItem
        pixmap_item.id = block.identifier  # Utilisez l'identifiant du bloc comme ID

        self.grid[grid_x][grid_y] = block
        block.position = self.grid_to_pixel(grid_x, grid_y)

        # Définir l'identifiant du bloc comme une donnée sur l'élément pixmap
        pixmap_item.setData(0, block.identifier)

        """if block.identifier == "2":
            self.add_quantum_stream(block.position, stream_id=self.stream_number)
            self.stream_number += 1
"""
        """
        elif block.identifier == "3":
            self.add_classical_stream(block.position, block_id=block.identifier, stream_id=self.stream_number)
            self.stream_number += 1"""


    def pixel_to_grid(self, position):
        grid_x = position[0] // 50
        grid_y = position[1] // 50
        return grid_x, grid_y

    def grid_to_pixel(self, grid_x, grid_y):
        pixel_x = grid_x * 50
        pixel_y = grid_y * 50
        return pixel_x, pixel_y

    def is_valid_position(self, grid_x, grid_y):
        return 0 <= grid_x < self.grid_size[0] and 0 <= grid_y < self.grid_size[1]

    def clear_scene(self):
        self.clear()
        self.grid = [[None for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]
        # Créer une grille contenant des tuples (identifiant, indice) pour chaque position
        self.block_info_grid = [[(None, None) for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]

        self.add_grid()

        # Déterminer les dimensions de la grille en pixels
        grid_width_pixels = self.grid_size[0] * 50
        grid_height_pixels = self.grid_size[1] * 50

        # Centrer la scène par rapport à la grille
        scene_center_x = grid_width_pixels / 2
        scene_center_y = grid_height_pixels / 2

        # Définir un nouveau rectangle de scène qui englobe toute la grille et la centrer
        scene_rect = QRectF(0, 0, grid_width_pixels, grid_height_pixels)
        self.setSceneRect(scene_rect)

        self.parent_window.block_count = 0 

    def run_graph(self):
        # Créer une grille contenant des tuples (identifiant, indice) pour chaque position
        self.block_info_grid = [[(None, None) for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]

        # Parcourir la grille principale et mettre à jour la grille d'informations sur les blocs
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self.grid[i][j] is not None:
                    self.block_info_grid[i][j] = (self.grid[i][j].identifier, self.grid[i][j].logical_number)

        # Afficher la grille d'informations sur les blocs
        convert_grid_to_quantum_circuit(self.block_info_grid)
        

    # Redéfinissez les méthodes de clic et de glissement
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Vérifiez si un objet est sélectionné
            item = self.itemAt(event.scenePos(), QTransform())
            if isinstance(item, QGraphicsPixmapItem):
                # Enregistrez la position initiale de l'objet
                self.initial_position = item.pos()


        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Vérifiez si un objet est sélectionné
            item = self.itemAt(event.scenePos(), QTransform())
            if isinstance(item, QGraphicsPixmapItem):
                # Récupérez la position finale de l'objet
                final_position = item.pos()
                # Convertissez les coordonnées finales en coordonnées de la grille
                grid_x = round(final_position.x() / 50)
                grid_y = round(final_position.y() / 50)
                # Convertissez les coordonnées de la grille en coordonnées de pixels
                new_position = QPointF(grid_x * 50, grid_y * 50)
                # Déplacez l'objet vers les nouvelles coordonnées
                item.setPos(new_position)

                # Mettez à jour la grille avec le nouvel emplacement de l'objet
                initial_grid_x, initial_grid_y = self.pixel_to_grid((int(self.initial_position.x()), int(self.initial_position.y())))
                current_grid_x, current_grid_y = self.pixel_to_grid((int(new_position.x()), int(new_position.y())))
                if self.is_valid_position(initial_grid_x, initial_grid_y) and self.is_valid_position(current_grid_x, current_grid_y):
                    self.grid[current_grid_x][current_grid_y] = self.grid[initial_grid_x][initial_grid_y]
                    self.grid[initial_grid_x][initial_grid_y] = None


        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        """if event.button() == Qt.MouseButton.LeftButton:
            item = self.itemAt(event.scenePos(), QTransform())
            # Récupérer l'identifiant du bloc à partir des données de l'élément pixmap
            identifier = item.data(0)
            if isinstance(item, QGraphicsPixmapItem) and identifier == "2":
                position = item.pos()  # Récupérer la position sous forme de QPointF
                position_tuple = (position.x(), position.y()) 
                stream_line = self.add_quantum_stream(position_tuple, stream_id=self.stream_number)

                self.block_lines[self.stream_number] = stream_line

                print(self.block_lines)
                pass"""
        print("mouse double clicked")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            # Supprimer le bloc sélectionné
            selected_items = self.selectedItems()
            for item in selected_items:
                if isinstance(item, QGraphicsPixmapItem):
                    # Supprimer le bloc de la grille
                    position = item.pos()
                    grid_x = round(position.x() / 50)
                    grid_y = round(position.y() / 50)
                    self.grid[grid_x][grid_y] = None
                    # Supprimer le bloc de la scène
                    self.removeItem(item)


class AnotherWindow(QWidget):
    """
    C'est la page principale, là ou il y a les itemps et la sandbox
    """
    def __init__(self, items):
        super().__init__()

        self.block_count = 0
        self.taille_globale = 5
        self.setFixedSize(800, 600)

        layout = QVBoxLayout(self)

        self.setWindowTitle("Quantum Labs")

        # Créer un layout horizontal pour placer la liste et la zone de sandbox côte à côte
        hbox_layout = QHBoxLayout()

        # Créer un QListWidget pour afficher la liste des éléments
        self.list_widget = QListWidget()
        self.list_widget.setFixedSize(100, 600)
        for item in items:
            list_item = QListWidgetItem(f"{item.name}{item.description}")
            list_item.setData(Qt.ItemDataRole.UserRole, item)  # Attachez l'objet ItemSprite à l'élément de liste
            self.list_widget.addItem(list_item)
        hbox_layout.addWidget(self.list_widget)

        

        graphics_vbox_layout = QVBoxLayout()

        # Créer une QGraphicsView pour la zone de sandbox
        self.sandbox_view = QGraphicsView()
        self.sandbox_scene = SandboxScene(self, grid_size=(self.taille_globale, self.taille_globale))
        self.sandbox_view.setScene(self.sandbox_scene)
        graphics_vbox_layout.addWidget(self.sandbox_view)

        button_run_graph = QPushButton("Run")
        button_run_graph.clicked.connect(self.sandbox_scene.run_graph)
        graphics_vbox_layout.addWidget(button_run_graph)

        button_clear_graph = QPushButton("Clear graph")
        button_clear_graph.clicked.connect(self.sandbox_scene.clear_scene)
        graphics_vbox_layout.addWidget(button_clear_graph)

        hbox_layout.addLayout(graphics_vbox_layout)

        layout.addLayout(hbox_layout)


        # Connecter le signal itemClicked à la méthode create_block lorsque l'utilisateur clique sur un élément de la liste
        self.list_widget.itemClicked.connect(self.create_block)

        self.show()

        """ Timer et fonction d'analyse
        self.timer = QTimer()
        self.timer.timeout.connect(self.analyze_scene)
        self.timer.start(10000) """



    def create_block(self, item):
        item_sprite = item.data(Qt.ItemDataRole.UserRole)
        print(f"Create block {item_sprite.name}")
        block = Block(identifier=item_sprite.identifiant, position=(0, 0), logical_number=self.block_count, image_path=item_sprite.image_path)
        self.sandbox_scene.add_block(block)
        self.block_count += 1
        print(f"block count : {self.block_count}")

    def analyze_scene(self):
        # Analyser la scène ici
        print("Analyzing the scene...")

def main():
    app = QApplication(sys.argv)

    # Créez quelques objets ItemSprite
    items = [
        ItemSprite("H", "", "H_gate.png", "0"),
        ItemSprite("X", "", "X_gate.png", "1"),
        ItemSprite("Psi", "", "Psi.png", "2"),
        ItemSprite("Cb", "", "Cb_A.png", "3"),
        ItemSprite("Ms", "", "Mesure.png", "4")
    ]

    another_window = AnotherWindow(items)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
