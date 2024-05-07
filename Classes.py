from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QDialogButtonBox



class Block:
    """
    C'est une classe qui s'occupe de gerer la position des blocks et tous leurs paramètres
    """
    def __init__(self, identifier, position, logical_number, image_path, shape=1, classical_output=None):
        self.identifier = identifier
        self.position = position
        self.classical_output = classical_output
        self.logical_number = logical_number
        self.image_path = image_path
        self.shape = shape
        self.shadow = [(int(self.position[0]/50), int(self.position[1]/50) + i ) for i in range(self.shape)]

        
        if shape > 1:
            self.remplissage = {"Block relie" : self.logical_number}
            
    def set_new_position(self, new_pos):
        self.position = new_pos
        self.shadow = [(int(self.position[0]/50), int(self.position[1]/50) + i ) for i in range(self.shape)]


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
        result = [[x.logical_number == lg_number if isinstance(x, Block) else None for x in row] for row in matrix ]
        block = [matrix[i][j] for i, row in enumerate(result) for j, value in enumerate(row) if value is True][0]

        return block
    
    def get_grid_position(self):
        return (round(self.position[0]/50), round(self.position[1]/50))
    

class CircuitItem:
    def __init__(self, name, description, image_path, circuit=1, block_file=None):
        self.name = name
        self.description = description
        self.image_path = image_path
        self.circuit = circuit
        self.block_file = block_file 

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
    
    
class SandboxParamsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setWindowTitle("Paramètre de la grille")
        
        # Éléments de la fenêtre de dialogue
        self.label = QLabel("Entrez la taille de la grille :")
        self.text_edit = QLineEdit()
        self.cancel_button = QPushButton("Annuler")
        self.save_button = QPushButton("Sauvegarder")
        self.input_number = 6

        self.cancel_button.clicked.connect(self.cancel_order)
        self.save_button.clicked.connect(self.save_number)
        
        # Layout de la fenêtre de dialogue
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.cancel_button)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)

    def cancel_order(self):
        self.accept()

    def save_number(self):
        self.parent_window.taille_globale = int(self.text_edit.text())
        self.accept()
    
    def get_number(self):
        return int(self.input_number)
    
class ResultPlotDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_window = parent

        # Création des widgets
        self.number_label = QLabel("Entrez un nombre:")
        self.number_edit = QLineEdit()
        self.item_label = QLabel("Choisissez un élément:")
        self.item_combobox = QComboBox()
        self.item_combobox.addItems(['statevector', 'stabilizer', 'extended_stabilizer', 
                                     'density_matrix','matrix_product_state'])  # Ajoutez vos éléments ici

        # Boutons de la boîte de dialogue
        self.cancel_button = QPushButton("Annuler")
        self.save_button = QPushButton("Sauvegarder")

        self.cancel_button.clicked.connect(self.cancel_params)
        self.save_button.clicked.connect(self.save_params)
        

        # Placement des widgets dans la boîte de dialogue
        layout = QVBoxLayout()
        layout.addWidget(self.number_label)
        layout.addWidget(self.number_edit)
        layout.addWidget(self.item_label)
        layout.addWidget(self.item_combobox)
        layout.addWidget(self.cancel_button)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_params(self):
        try:
            self.parent_window.RPS_shots = int(self.number_edit.text())
        except ValueError:
            self.parent_window.RPS_shots += 0
        self.parent_window.RPS_qbit_methods = self.item_combobox.currentText()
        self.accept()
    
    def cancel_params(self):
        self.accept()


    def get_data(self):
        return int(self.number_edit.text()), self.item_combobox.currentText()