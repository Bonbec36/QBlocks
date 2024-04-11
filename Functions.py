from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import Sampler
from qiskit.visualization import plot_histogram

"""
grid = [[(None, None), ('2', 0), ('3', 1), (None, None), (None, None)], 
        [(None, None), ('1', 3), (None, None), (None, None), (None, None)],
        [(None, None), ('4', 2), (None, None), (None, None), (None, None)], 
        [(None, None), (None, None), (None, None), (None, None), (None, None)], 
        [(None, None), (None, None), (None, None), (None, None), (None, None)]]
"""

def convert_grid_to_quantum_circuit(grid):
    list_quantum_register = [None for _ in grid[0]]
    list_classical_register = [None for _ in grid[0]]

    quantum_register_name_number = 0
    classical_register_name_number = 0
    for i in range(len(grid[0])):
        if grid[0][i] is not None:
            if grid[0][i].identifier == '2':
                list_quantum_register[i] = QuantumRegister(1, f"q{quantum_register_name_number}")
                quantum_register_name_number += 1
            elif grid[0][i].identifier == '3':
                list_classical_register[i] = ClassicalRegister(1, f"c{classical_register_name_number}")
                classical_register_name_number += 1
    liste_register = list_quantum_register+list_classical_register
    cleared_list_tegister = [i for i in liste_register if i is not None]
        
    qc = QuantumCircuit(*cleared_list_tegister)
    
    for j in range(1, len(grid)-1):
        for i in range(len(grid[0])):
            if grid[j][i] is not None:
                if grid[j][i].identifier == '0' and grid[0][i].identifier == '2':
                    qc.h(list_quantum_register[i])
                elif grid[j][i].identifier == '1' and grid[0][i].identifier == '2':
                    qc.x(list_quantum_register[i])
                elif grid[j][i].identifier == '4' and grid[0][i].identifier == '2':
                    connected_calssical_register = grid[j][i].find_block_by_identifier(grid, grid[j][i].classical_output)
                    qc.measure(list_quantum_register[i], list_classical_register[connected_calssical_register.get_grid_position()[1]])
    print(qc.draw())

    return qc

def simulate_quantum_circuit(circuit):
    print(circuit)

"""
X = QuantumRegister(1, "X")
Y = QuantumRegister(1, "Y")
A = ClassicalRegister(1, "A")
B = ClassicalRegister(1, "B")

circuit = QuantumCircuit(Y, X, B, A)
circuit.h(Y)
circuit.cx(Y, X)
circuit.measure(Y, B)
circuit.measure(X, A)

print(circuit.draw())
"""
