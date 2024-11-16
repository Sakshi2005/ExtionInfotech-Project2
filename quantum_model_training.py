# Import required libraries
import numpy as np
from qiskit import Aer
from qiskit.circuit.library import ZZFeatureMap
from qiskit_machine_learning.kernels import QuantumKernel
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_classification

# Create a larger dataset
X, y = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define a deeper Quantum Feature Map
feature_map = ZZFeatureMap(feature_dimension=2, reps=3, entanglement='full')

# Define Quantum Kernel with AerSimulator
backend = Aer.get_backend('statevector_simulator')
quantum_kernel = QuantumKernel(feature_map=feature_map, quantum_instance=backend)

# Train the Quantum Kernel SVM with tuned hyperparameters
qsvm = SVC(kernel=quantum_kernel.evaluate, C=10, gamma='scale')
qsvm.fit(X_train, y_train)

# Evaluate the Model
y_pred = qsvm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Display Results
print(f"Quantum Kernel SVM Accuracy: {accuracy * 100:.2f}%")
