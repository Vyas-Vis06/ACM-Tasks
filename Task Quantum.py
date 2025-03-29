from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Step 1: Define the Oracle function (Marking the correct answer)
def grover_oracle(n):
    qc = QuantumCircuit(n)
    qc.z(n-1)  # Flip the phase of the correct answer (let's assume it's |11> in 2-qubit case)
    return qc

# Step 2: Apply Grover Diffusion Operator (Amplifies the correct answer)
def grover_diffuser(n):
    qc = QuantumCircuit(n)
    qc.h(range(n))  # Apply Hadamard gates
    qc.x(range(n))  # Apply X gates (inversion about mean)
    qc.h(n-1)       # Hadamard on the last qubit
    qc.mcx(list(range(n-1)), n-1)  # Multi-controlled NOT
    qc.h(n-1)       # Hadamard on the last qubit
    qc.x(range(n))  # Apply X gates
    qc.h(range(n))  # Apply Hadamard gates
    return qc

# Step 3: Build the full Grover's Algorithm circuit
n = 2  # Number of qubits
grover_circuit = QuantumCircuit(n, n)

# Initialize in Superposition
grover_circuit.h(range(n))

# Apply Oracle
grover_circuit.append(grover_oracle(n).to_gate(), range(n))

# Apply Diffusion Operator
grover_circuit.append(grover_diffuser(n).to_gate(), range(n))

# Measurement
grover_circuit.measure(range(n), range(n))

# Step 4: Run the Circuit on a Quantum Simulator
simulator = Aer.get_backend('aer_simulator')
tqc = transpile(grover_circuit, simulator)
qobj = assemble(tqc)
result = simulator.run(qobj).result()
counts = result.get_counts()

# Step 5: Show the Results
print("Measurement Results:", counts)
plot_histogram(counts)
plt.show()
