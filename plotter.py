import matplotlib.pyplot as plt
import csv

fitness = []

with open('images/exp4/fitness.csv', newline='') as f:
    reader = csv.reader(f)
    for value in reader:
        fitness.append(int(''.join(value)))

plt.plot(fitness)
plt.show()

