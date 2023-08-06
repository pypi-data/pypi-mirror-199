def help():
    print("Welcome to QuSBT!")
    print("\n")
    print("You can provide the root of the configuration to run qusbt.")
    print("Here is the template of the configuration file.")

    template = '''
[program]
root= 
;(Required)
;Description: The absolute root of your quantum program file.
num_qubit= 
;(Required)
;Description: The total number of qubit of your quantum program.
inputID= 
;(Required)
;Description: The IDs of input qubits.
;Format: A non-repeating sequence separated by commas.
outputID= 
;(Required)
;Description: The IDs of output qubits which are the qubits to be measured.
;Format: A non-repeating sequence separated by commas.

[qusbt_configuration]
beta=
;(Optional)
;Description: The percentage of possible inputs as the number of test cases in a test suite.
M=
;(Optional)
;Description: The number of test cases in a test suite.
;Attention: You should use either 'beta' or 'M'. We use 'beta' as 0.05 by default.

[GA_parameter]
population_size= 
;(Optional) 
;Description: The population size in GA, population_size=10 by default.
offspring_population_size= 
;(Optional)
;Description: The offspring population size in GA, offspring_population_size=10 by default.
max_evaluations=
;(Optional)
;Description: The maximum evaluations in GA, max_evaluations=500 by default.
mutation_probability=
;(Optional)
;Description: mutation probability in GA, mutation_probability=1.0/M, 'M' is the size of a test suite by default.
mutation_distribution_index=
;(Optional)
;Description: mutation distribution in GA, mutation_distribution_index=20 by default.
crossover_probability=
;(Optional)
;Description: crossover probability in GA, crossover_probability=0.9 by default.
crossover_distribution_index=
;(Optional)
;Description: crossover probability in GA, crossover_distribution_index=20 by default.

[program_specification]
;Description: The program specification.
;Format:input string (binary),output string (binary)=probability
;Example:
;00,1=0.5
;00,0=0.5
;01,1=0.5
;01,0=0.5
;or
;0-,-=0.5
;Attention: '-' can refer to both '0' and '1'.
'''
    print(template)
    print('\n')

    print("Here is the example of the configuration file and the quantum program file.")

    example = '''
[program]
root=C:\IQ.py
num_qubit=10
inputID=0,1,2,3,4,5,6,7,8,9
outputID=0,1,2,3,4,5,6,7,8,9

[qusbt_configuration]
beta=0.05
confidence_level=0.01

[GA_parameter]
population_size=10
offspring_population_size=10
max_evaluations=500  

[program_specification]
----------,----------=0.0009765625
    '''
    program = '''
import math

def swap_registers(circuit, n):
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit

def qft_rotations(circuit, qubit, p):
    for j in range(qubit + 1, 10):
        circuit.cu1(math.pi/2**(p), qubit, j)
        p += 1
    circuit.barrier()
    return circuit

def run(qc):
    n = 10
    swap_registers(qc,n)
    for qubit in range(n):
        qc.h(qubit)
        p = 1
        qft_rotations(qc,qubit,p)

    qc.measure([0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9])
    '''
    print(example)
    print("Here is the example of the quantum program file.")
    print(program)

if __name__ == '__main__':
    help()



