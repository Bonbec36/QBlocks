from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.primitives import Sampler
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

from Classes import Block
import matplotlib.pyplot as plt

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
            if isinstance(grid[j][i], Block):
                if grid[j][i].identifier == '0' and grid[0][i].identifier == '2':
                    qc.h(list_quantum_register[i])
                elif grid[j][i].identifier == '1' and grid[0][i].identifier == '2':
                    qc.x(list_quantum_register[i])
                elif grid[j][i].identifier == '5' and grid[0][i].identifier == '2':
                    qc.y(list_quantum_register[i])
                elif grid[j][i].identifier == '6' and grid[0][i].identifier == '2':
                    qc.z(list_quantum_register[i])
                elif grid[j][i].identifier == '4' and grid[0][i].identifier == '2':
                    connected_calssical_register = grid[j][i].find_block_by_identifier(grid, grid[j][i].classical_output)
                    qc.measure(list_quantum_register[i], list_classical_register[connected_calssical_register.get_grid_position()[1]])
                elif grid[j][i].identifier == '7' and grid[0][i].identifier == '2' and grid[0][i+1].identifier == '2':
                    qc.cx(list_quantum_register[i], list_quantum_register[i+1])
                elif grid[j][i].identifier == '8' and grid[0][i].identifier == '2' and grid[0][i+1].identifier == '2':
                    qc.cx(list_quantum_register[i+1], list_quantum_register[i])
    print(qc.draw())

    return qc

def simulate_quantum_circuit(circuit):


    sim_ideal = AerSimulator()

        # Execute and get counts
    result = sim_ideal.run(circuit, shots=1000, memory=True).result()
    counts = result.get_counts(0)

    fig = plot_histogram(counts)
    return fig
