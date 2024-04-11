
import sys
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

#___________________________________________________________________________________________________

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGraphicsView 
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QListWidget, QListWidgetItem
from PyQt6.QtWidgets import QGraphicsItem, QPushButton, QGraphicsRectItem, QGraphicsLineItem, QGraphicsSimpleTextItem
from PyQt6.QtWidgets import QWidget, QDialog, QLabel, QLineEdit, QMenu, QMenuBar

from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QColor, QDragMoveEvent, QTransform, QPen
from PyQt6.QtGui import QFont, QAction, QImage
from PyQt6.QtCore import Qt, QDataStream, QIODevice, QEvent, QTimer, QPointF, QRectF, QLineF
from PyQt6.QtCore import QMimeData

#____________________________________________________________________
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import Sampler
from qiskit.visualization import plot_histogram, circuit_drawer
from Functions import convert_grid_to_quantum_circuit, simulate_quantum_circuit



class Block:
    """
    C'est une classe qui s'occupe de gerer la position des blocks et tous leurs paramètres
    """
    def __init__(self, identifier, position, logical_number, image_path):
        self.identifier = identifier
        self.position = position
        self.logical_number = logical_number
        self.image_path = image_path

        if self.identifier == "4":
            self.classical_output = 0


    @staticmethod
    def find_block_by_identifier(matrix, lg_number):
        """
        Recherche un bloc dans une matrice à partir de son identifiant.

        Args:
            matrix (list[list[Block]]): La matrice contenant les blocs.
            identifier (int): L'identifiant du bloc à rechercher.

        Returns:
            Block: Le bloc correspondant à l'identifiant, ou None si aucun bloc avec cet identifiant n'est trouvé.
        """
        result = [[x.logical_number == lg_number if x is not None else None for x in row] for row in matrix ]
        block = [matrix[i][j] for i, row in enumerate(result) for j, value in enumerate(row) if value is True][0]

        return block
    
    def get_grid_position(self):
        return (round(self.position[0]/50), round(self.position[1]/50))

class ItemSprite:
    """
    C'est une classe qui s'occupe de gerer la position des items
    """
    def __init__(self, item_name, item_description, image_path, identifiant):
        self.name = item_name
        self.description = item_description
        self.image_path = image_path
        self.identifiant = identifiant


class NumberInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Enter a Number")
        layout = QVBoxLayout()
        self.number_input = QLineEdit()
        layout.addWidget(QLabel("Enter a number:"))
        layout.addWidget(self.number_input)
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def get_number(self):
        return int(self.number_input.text()) if self.exec() else None
    
class SandboxGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.saved_items = []  # Initialisation de la liste saved_items
        self.scene_grid_save = None
        if self.parent_window.SBGV_saved_scene is None:
            self.current_scene = SandboxScene(self.parent_window)  # Créez la scène initiale
            self.setScene(self.current_scene)
        else:
            self.current_scene = self.parent_window.SBGV_saved_scene

    def save_scene_elements(self):
        self.parent_window.SBGV_saved_blocks = [block for row in self.scene().grid for block in row if block is not None]
        self.parent_window.SBGV_saved_scene = self.current_scene

    def restore_scene_elements(self):
        # Exemple de restauration d'éléments de scène
        self.setScene(self.parent_window.SBGV_saved_scene)
        #self.scene().restore_grid(self.parent_window.SBGV_saved_blocks)

    def run_graph(self):
        print(self.scene())
        self.scene().run_graph()
        self.parent_window.result_histogram = simulate_quantum_circuit(self.parent_window.circuit_quantique)



class QuantumGraphGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setScene(QuantumGraphScene(self.parent_window))
        self.saved_items = []  # Initialisation de la liste saved_items

    def save_scene_elements(self):
        # Exemple de sauvegarde d'éléments de scène
        items = self.scene().items()
        self.saved_items = [item for item in items]
        #print("Saved items in View 1:", self.saved_items)

    def restore_scene_elements(self):
        # Exemple de restauration d'éléments de scène
        for item in self.saved_items:
            self.scene().addItem(item)
        #print("Restored items in View 1:", self.saved_items)

    def run_graph(self):
        print("second")

class ResultplotGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setScene(ResultPlotScene(self.parent_window, self))
        self.saved_items = []  # Initialisation de la liste saved_items
        self.setGeometry(0, 0, 200, 200)

    def save_scene_elements(self):
        # Exemple de sauvegarde d'éléments de scène
        items = self.scene().items()
        self.saved_items = [item for item in items]
        #print("Saved items in View 1:", self.saved_items)

    def restore_scene_elements(self):
        # Exemple de restauration d'éléments de scène
        for item in self.saved_items:
            self.scene().addItem(item)
        #print("Restored items in View 1:", self.saved_items)

    def run_graph(self):
        print("second")


class SandboxScene(QGraphicsScene):
    """
    C'est une classe qui permet de gérer la sandbox, c'est à dire l'endroit où l'on place les blocks
    """
    def __init__(self, parent_window, grid_size=(6, 6)):
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
    
    def add_block(self, block, restore=False):
        grid_x, grid_y = self.pixel_to_grid(block.position)

        print(self)

        if self.grid[grid_x][grid_y] is None:
            self.grid[grid_x][grid_y] = block
            block.position = self.grid_to_pixel(grid_x, grid_y)
        else:
            new_x, new_y = self.find_nearest_valid_position(grid_x, grid_y)
            self.grid[new_x][new_y] = block
            block.position = self.grid_to_pixel(new_x, new_y)

        pixmap = QPixmap(block.image_path)
        scaled_pixmap = pixmap.scaled(50, 50)
        pixmap_item = QGraphicsPixmapItem(scaled_pixmap)
        pixmap_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        pixmap_item.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        pixmap_item.setPos(*block.position)

        self.addItem(pixmap_item)

        # Définir l'attribut 'id' pour le QGraphicsPixmapItem
        pixmap_item.id = block.identifier  # Utilisez l'identifiant du bloc comme ID

        

        

         # Ajouter un carré gris clair en dessous de l'image du bloc
        rect_item = QGraphicsRectItem(0, 0, 12, 16, pixmap_item)
        rect_item.setBrush(QColor(200, 200, 200))

        # Ajouter le numéro au-dessus de l'image du bloc
        number_text = QGraphicsSimpleTextItem(str(block.logical_number), pixmap_item)
        font = QFont()
        font.setPointSize(12)
        number_text.setFont(font)
        number_text.setBrush(QColor("black"))
        number_text.setPos(0, 0)

        if block.identifier == "4" and restore == False:
            number_dialog = NumberInputDialog()
            block.classical_output = number_dialog.get_number()


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
        self.block_info_grid = [[None for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]

        # Parcourir la grille principale et mettre à jour la grille d'informations sur les blocs
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self.grid[i][j] is not None:
                    self.block_info_grid[i][j] = self.grid[i][j]
        # Afficher la grille d'informations sur les blocs
        self.parent_window.circuit_quantique = convert_grid_to_quantum_circuit(self.block_info_grid)
        

    # Redéfinissez les méthodes de clic et de glissement
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Vérifiez si un objet est sélectionné
            item = self.itemAt(event.scenePos(), QTransform())
            if isinstance(item, QGraphicsPixmapItem):
                # Enregistrez la position initiale de l'objet
                self.initial_position = item.pos()
        # Appeler la fonction mousePressEvent de la classe parent
        super().mousePressEvent(event)

    def find_nearest_valid_position(self, grid_x, grid_y):
            """
            Fonction qui trouve la place libre pour un qblock déplacé
            """
            n = self.parent_window.taille_globale
            for dz in range(n+1):
                for dx in range(-dz, dz):
                    for dy in range(-dz, dz):
                        new_x = grid_x + dx
                        new_y = grid_y + dy
                        if self.is_valid_position(new_x, new_y) and self.grid[new_x][new_y] is None:
                            return new_x, new_y
            return None


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

                if self.grid[grid_x][grid_y] is None:
                    # Mettez à jour la grille avec le nouvel emplacement de l'objet
                    initial_grid_x, initial_grid_y = self.pixel_to_grid((int(self.initial_position.x()), int(self.initial_position.y())))
                    current_grid_x, current_grid_y = self.pixel_to_grid((int(new_position.x()), int(new_position.y())))
                    if self.is_valid_position(initial_grid_x, initial_grid_y) and self.is_valid_position(current_grid_x, current_grid_y):
                        self.grid[grid_x][grid_y] = self.grid[initial_grid_x][initial_grid_y]
                        self.grid[initial_grid_x][initial_grid_y] = None

                        #On actualise la position du block
                        self.grid[grid_x][grid_y].position = (int(new_position.x()), int(new_position.y())) 
                else:
                    #Pour ne pas supperposer les qblocks
                    new_x, new_y = self.find_nearest_valid_position(grid_x, grid_y) 
                    new_position = QPointF(new_x * 50, new_y * 50)
                    item.setPos(new_position)
                    # Mettez à jour la grille avec le nouvel emplacement de l'objet
                    initial_grid_x, initial_grid_y = self.pixel_to_grid((int(self.initial_position.x()), int(self.initial_position.y())))
                    current_grid_x, current_grid_y = self.pixel_to_grid((int(new_position.x()), int(new_position.y())))
                    if self.is_valid_position(initial_grid_x, initial_grid_y) and self.is_valid_position(current_grid_x, current_grid_y):
                        self.grid[new_x][new_y] = self.grid[initial_grid_x][initial_grid_y]
                        self.grid[initial_grid_x][initial_grid_y] = None

                        #On actualise la position du block
                        self.grid[new_x][new_y].position = (int(new_position.x()), int(new_position.y())) 

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

    def restore_grid(self, liste_bocks):

        for block in liste_bocks:
            self.add_block(block)


class QuantumGraphScene(QGraphicsScene):
    def __init__(self, parent_window):
        self.parent_window = parent_window
        super().__init__()
        self.setSceneRect(0, 0, 800, 600)  # Définir la taille de la scène

    # Dessiner le circuit quantique
        pixmap = self.draw_circuit(self.parent_window.circuit_quantique)

        pixmap_item = QGraphicsPixmapItem(pixmap)

        self.addItem(pixmap_item)

    def draw_circuit(self, circuit):
        # Créer une représentation graphique du circuit avec matplotlib
        fig, ax = plt.subplots()
        qc_image = circuit_drawer(circuit, output='mpl', ax=ax)

        # Convertir l'image matplotlib en QImage
        canvas = FigureCanvas(fig)
        canvas.draw()

        # Convertir le canevas en une image QImage
        width, height = canvas.get_width_height()
        image = QImage(canvas.buffer_rgba(), width, height, QImage.Format.Format_ARGB32)

        # Convertir l'image QImage en une image pixmap
        pixmap = QPixmap.fromImage(image)

        return pixmap
    
class ResultPlotScene(QGraphicsScene):
    def __init__(self, parent_window, parent_graphicsview):
        self.parent_window = parent_window
        self.parent_graphicsview = parent_graphicsview
        super().__init__()
        #self.setSceneRect() # Définir la taille de la scène

    # Dessiner le circuit quantique
        pixmap = self.plot_result(self.parent_window.result_histogram)

        pixmap_item = QGraphicsPixmapItem(pixmap)

        self.addItem(pixmap_item)

    def plot_result(self, histogram):

        # Convertir l'image matplotlib en QImage
        canvas = FigureCanvas(histogram)
        canvas.draw()

        # Convertir le canevas en une image QImage
        width, height = canvas.get_width_height()
        image = QImage(canvas.buffer_rgba(), width, height, QImage.Format.Format_ARGB32)

        # Convertir l'image QImage en une image pixmap
        pixmap = QPixmap.fromImage(image).scaled(500, 400)

        return pixmap


class AnotherWindow(QWidget):
    """
    C'est la page principale, là ou il y a les itemps et la sandbox
    """
    def __init__(self, items):
        super().__init__()

        self.block_count = 0
        self.taille_globale = 5
        self.circuit_quantique = None
        self.SBGV_saved_blocks = []
        self.SBGV_saved_scene = None

        
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

        

        self.graphics_vbox_layout = QVBoxLayout()

        self.graph_buttons_layout = QHBoxLayout()

        button_scene1 = QPushButton("Labs")
        button_scene1.clicked.connect(self.show_sandbox_graphview)
        self.graph_buttons_layout.addWidget(button_scene1)

        button_scene2 = QPushButton("Circuit")
        button_scene2.clicked.connect(self.show_quantum_graphview)
        self.graph_buttons_layout.addWidget(button_scene2)

        button_scene3 = QPushButton("Mesures")
        button_scene3.clicked.connect(self.show_result_graphview)
        self.graph_buttons_layout.addWidget(button_scene3)

        self.graphics_vbox_layout.addLayout(self.graph_buttons_layout)
        # Créer une QGraphicsView pour la zone de sandbox
        self.current_view = SandboxGraphicsView(parent=self)

        self.graphics_vbox_layout.addWidget(self.current_view)

        button_run_graph = QPushButton("Run")
        button_run_graph.clicked.connect(self.current_view.run_graph)
        self.graphics_vbox_layout.addWidget(button_run_graph)

        button_clear_graph = QPushButton("Clear graph")
        button_clear_graph.clicked.connect(self.current_view.scene().clear_scene)
        self.graphics_vbox_layout.addWidget(button_clear_graph)

        hbox_layout.addLayout(self.graphics_vbox_layout)

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
        self.current_view.scene().add_block(block)
        self.block_count += 1
        print(f"block count : {self.block_count}")

    def show_sandbox_scene(self):
        # Restaurer les éléments de la scène sandbox principale
        self.sandbox_scene.clear_scene()
        for item in self.main_sandbox_items:
            self.sandbox_scene.add_item(item)

    def closeEvent(self, event):
        # Sauvegardez les éléments de la scène sandbox principale lorsque la fenêtre se ferme
        #self.main_sandbox_items = self.sandbox_scene.get_items()
        event.accept()


    def show_quantum_graphview(self):
        if isinstance(self.current_view, SandboxGraphicsView) or isinstance(self.current_view, ResultplotGraphicsView):
            self.current_view.save_scene_elements()
        self.current_view = QuantumGraphGraphicsView(self)


        self.graphics_vbox_layout.replaceWidget(self.graphics_vbox_layout.itemAt(1).widget(), self.current_view)
        self.current_view.restore_scene_elements()

    def show_sandbox_graphview(self):
        if isinstance(self.current_view, QuantumGraphGraphicsView) or isinstance(self.current_view, ResultplotGraphicsView):
            self.current_view.save_scene_elements()
        self.current_view = SandboxGraphicsView(self)


        self.graphics_vbox_layout.replaceWidget(self.graphics_vbox_layout.itemAt(1).widget(), self.current_view)
        self.current_view.restore_scene_elements()

    def show_result_graphview(self):
        if isinstance(self.current_view, QuantumGraphGraphicsView) or isinstance(self.current_view, SandboxGraphicsView):
            self.current_view.save_scene_elements()
        self.current_view = ResultplotGraphicsView(self)


        self.graphics_vbox_layout.replaceWidget(self.graphics_vbox_layout.itemAt(1).widget(), self.current_view)
        self.current_view.restore_scene_elements()


    def do_nothing(self):
        print("do nothing")


def main():
    app = QApplication(sys.argv)

    # Créez quelques objets ItemSprite
    items = [
        ItemSprite("H", "", "images/H_gate.png", "0"),
        ItemSprite("X", "", "images/X_gate.png", "1"),
        ItemSprite("Psi", "", "images/Psi.png", "2"),
        ItemSprite("Cb", "", "images/Cb_A.png", "3"),
        ItemSprite("Ms", "", "images/Mesure.png", "4")
    ]

    another_window = AnotherWindow(items)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
