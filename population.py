import random, copy
from individual import Individual
from gene import Gene
from datetime import datetime
random.seed(datetime.now())

RAD_MIN = 1
RAD_MAX = 50

class Population():

    def __init__(self, source, size, width, height, channels, num_genes, elitist, frac_elites, frac_parents):
        self.size = size
        self.width = width
        self.height = height
        self.channels = channels
        self.individuals = []
        self.buffer = []
        self.best = None
        self.num_genes = num_genes
        self.source = source
        self.elitist = elitist
        if self.elitist:
            self.elite_count = int(self.size * frac_elites)
        self.frac_parents = frac_parents
        self.parent_count = int(self.size * self.frac_parents)
        if self.parent_count % 2 == 1:
            self.parent_count += 1

        for i in range(self.size):
            self.individuals.append(Individual(width, height, channels, num_genes))

    def evalPopulation(self):

        for ind in self.individuals:
            ind.evalFitness(self.source)
        
        self.sortIndividuals()
        self.best = self.individuals[0]

        return self.best.fitness

    def getFitness(self, ind):
        return ind.fitness

    def sortIndividuals(self):
        self.individuals.sort(reverse = True, key = self.getFitness)

    # The implementation of the tournament selection
    def tournamentSelection(self, tmsize):
        # nonElites = self.individuals[self.elite_count:]
        nonElites = self.individuals
        best = nonElites[random.randint(0, len(nonElites)-1)] # The first competitor
        best.evalFitness(self.source)

        while(tmsize > 1):
            ind = nonElites[random.randint(0, len(nonElites)-1)] # Randomly select a competitor

            if ind.evalFitness(self.source) > best.fitness: # Determine competitor with best fitness
                best = ind

            tmsize = tmsize - 1
        
        winner = copy.deepcopy(best)

        return winner # Return the best competitor
    
    # The selection algorithm for the population
    def populationSelect(self, tmsize):
        remaining = self.size
        self.buffer = []

        if self.elitist:
            for elite in range(self.elite_count):
                sel_elite = copy.deepcopy(self.individuals[elite])
                self.buffer.append(sel_elite)
                remaining = remaining - 1

        while(remaining > 0):
            self.buffer.append(self.tournamentSelection(tmsize))
            remaining = remaining - 1
        
        while(remaining < self.size):
            self.individuals[remaining] = self.buffer[remaining]
            remaining = remaining + 1

    # The individual crossover function
    def individualCross(self, ind1, ind2):
        for gene in range(self.num_genes):
            if random.random() < 0.5:
                ind1.chromosome[gene], ind2.chromosome[gene] = ind2.chromosome[gene], ind1.chromosome[gene] 
                ind1.fitness = 1
                ind2.fitness = 1

    # The population crossover function
    def populationCross(self):
        if self.elitist:
            for parent in range(0, self.parent_count-1, 2):
                self.individualCross(self.individuals[self.elite_count + parent], self.individuals[self.elite_count + parent+1])

    # The individual mutation function
    def individualMutation(self, ind, probability, method):
        if method == 'unguided':
            while random.random() < probability:
                self.indUnguidedMutation(ind.chromosome[random.randint(0, self.num_genes-1)])
                ind.fitness = 1
                print("Mutated!")
        elif method == 'guided':
            while random.random() < probability:
                self.indGuidedMutation(ind.chromosome[random.randint(0, self.num_genes-1)])
                ind.fitness = 1
        else:
            print("Unknown mutation type! Options: guided or unguided")
            return

    # The unguided mutation
    def indUnguidedMutation(self, gene):
        while True:
                # Initialize the radius value
                radius = random.randint(RAD_MIN, RAD_MAX)

                # Initialize the center point
                center = [random.randint(-radius, self.width+radius), random.randint(-radius, self.height+radius)]

                colors = []

                # Initalize the color channels between 0 and 255
                for ch in range(self.channels):
                    colors.append(random.randint(0,255))
                # Initialize the alpha value between 0 and 1
                colors.append(random.random())

                newGene = Gene(center, radius, colors, self.width, self.height)

                if newGene.valid:
                    break
        gene = newGene

    # The guided mutation
    def indGuidedMutation(self, gene):
        x = gene.center[0]
        y = gene.center[1]
        radius = gene.radius
        color = gene.colors
        alpha = gene.alpha

        gene.center[0] = random.randint(x - self.width/4, x + self.width/4)
        gene.center[1] = random.randint(x - self.height/4, x + self.height/4)
        gene.radius = random.randint(max(radius - 10, RAD_MIN), min(radius + 10, RAD_MAX))
        while(not gene.collision(0, 0, self.width, self.height, gene.center[0], gene.center[1], gene.radius)):
            gene.center[0] = random.randint(x - self.width/4, x + self.width/4)
            gene.center[1] = random.randint(x - self.height/4, x + self.height/4)
            gene.radius = random.randint(max(radius - 10, RAD_MIN), min(radius + 10, RAD_MAX))

        for i in range(3):
            gene.colors[i] = random.randint(max(0, color[i] - 64), min(255, color[i] + 64))

        gene.alpha = random.uniform(max(0, alpha - 0.25), min(1, alpha + 0.25))
        
    # The population mutation function
    def populationMutation(self, probability, method):
        for ind in self.individuals[self.elite_count:]:
            self.individualMutation(ind, probability, method)
