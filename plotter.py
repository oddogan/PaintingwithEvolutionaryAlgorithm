import matplotlib.pyplot as plt
import numpy as np
import csv

all_fitnesses = []
fitness = []

# The test name and parameters to be plotted
test_name = "mutation_prob"
test_values = [0.1, 0.2, 0.5, 0.8]

# Figure settings
figure, axis = plt.subplots(1, 2)
axis.flat[0].set(ylabel='Fitness')
for ax in axis.flat:
    ax.set(xlabel='Generation')
figure.suptitle(f"Fitness value comparison of various <{test_name}>")

# Open the test results and add them to the list
for i in test_values:
    with open(f'data/test_{test_name}/{i}/fitness.csv', newline='') as f:
        reader = csv.reader(f)
        for value in reader:
            fitness.append(int(''.join(value)))
        all_fitnesses.append(fitness)
        fitness = []

# Plot the results with range 0-1000th generation and 1000-10000th generation in different plots
for i in range(len(test_values)):
    axis[0].plot(np.arange(0, 1000, 1), all_fitnesses[i][:1000], label=str(test_values[i]))
    axis[1].plot(np.arange(1000, 10000, 1), all_fitnesses[i][1000:], label=str(test_values[i]))

axis[0].legend()
axis[1].legend()

# Save the results
plt.savefig(f'data/test_{test_name}/result.png')
plt.show()

