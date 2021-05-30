import cv2, csv
import numpy as np
from population import Population

num_inds = 50 # Number of individuals
num_genes = 50 # Number of genes
tm_size = 5 # Tournament size
elitist = True # Whether the population is elitist or not
frac_elites = 0.2 # Number of individuals advancing without change
frac_parents = 0.6 # Number of parents to be used in crossover
mutation_prob = 0.2 # Mutation probability
mutation_type = 'guided' # Mutation type (guided or unguided)
num_generations = 10000 # Number of maximum generations

# Import the image and get the properties
image = cv2.imread('painting.png')
(height, width, channels) = image.shape

csvfile = "data/test_num_inds/50/fitness.csv"

# Initialize the population
population = Population(image, num_inds, width, height, channels, num_genes, elitist, frac_elites, frac_parents)
fitness_values = []

while((population.evalPopulation() < 0) and (num_generations > 0)):

    if(num_generations % 1000 == 0):
        cv2.imwrite('data/test_num_inds/50/image{0}_{1}.png'.format(10000-num_generations, abs(population.best.fitness)), population.best.image)
    print(f"Generation {10001 - num_generations}: {population.best.fitness}")

    population.populationSelect(tm_size)
    population.populationCross()
    population.populationMutation(mutation_prob, mutation_type)

    fitness_values.append(population.best.fitness)
    num_generations -= 1

print(f"Last Generation {10000 - num_generations}: {population.best.fitness}")

with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in fitness_values:
        writer.writerow([val])

cv2.imwrite('data/test_num_inds/50/final_image{0}_{1}.png'.format(10000-num_generations, abs(population.best.fitness)), population.best.image)
cv2.imshow("ImageLast", population.best.image)
cv2.waitKey(0)



