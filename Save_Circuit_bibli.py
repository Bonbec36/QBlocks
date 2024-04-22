import pickle
from Classes import Block

# Créez une liste d'objets Block
blocks = [
    Block(identifier="2", position=(0, 0), logical_number=1, image_path="images/Psi.png"),
    Block(identifier="2", position=(0, 50), logical_number=2, image_path="images/Psi.png"),
    Block(identifier="0", position=(50, 0), logical_number=3, image_path="images/H_gate.png"),
    Block(identifier="3", position=(0, 100), logical_number=4, image_path="images/Cb_A.png"),
    Block(identifier="3", position=(0, 150), logical_number=5, image_path="images/Cb_A.png"),
    Block(identifier="7", position=(100, 0), logical_number=6, image_path="images/CX_gate.png", shape=2),
    Block(identifier="4", position=(150, 0), logical_number=7, image_path="images/Mesure.png", classical_output=4),
    Block(identifier="4", position=(200, 50), logical_number=8, image_path="images/Mesure.png", classical_output=5),
    # Ajoutez plus de blocs au besoin
]

# Nom du fichier pour stocker les données
filename = "files/bibliotheque/Entangled_BD.pkl"

# Écrire les objets Block dans le fichier
with open(filename, "wb") as f:
    pickle.dump(blocks, f)

# Lecture des objets Block à partir du fichier
with open(filename, "rb") as f:
    loaded_blocks = pickle.load(f)

# Affichage des objets chargés
for block in loaded_blocks:
    print(block.identifier, block.position, block.logical_number, block.image_path)
