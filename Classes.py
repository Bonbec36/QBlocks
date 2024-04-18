class Block:
    """
    C'est une classe qui s'occupe de gerer la position des blocks et tous leurs paramètres
    """
    def __init__(self, identifier, position, logical_number, image_path, shape=1):
        self.identifier = identifier
        self.position = position
        self.logical_number = logical_number
        self.image_path = image_path
        self.shape = shape
        self.shadow = [(int(self.position[0]/50), int(self.position[1]/50) + i ) for i in range(self.shape)]

        if self.identifier == "4":
            self.classical_output = 0

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