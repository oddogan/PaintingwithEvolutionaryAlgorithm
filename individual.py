import gene, random, cv2
import numpy as np
import random
from datetime import datetime
random.seed(datetime.now())

RAD_MIN = 1
RAD_MAX = 50

class Individual():

    def __init__(self, width, height, channels, num_genes):
        # Default values
        self.fitness = 1
        self.image = None

        # Source image's properties
        self.width = width
        self.height = height
        self.channels = channels

        # Individual chromosome properties
        self.numberGenes = num_genes
        self.chromosome = []

        # Initialize the genes in the chromosome
        for i in range(num_genes):
            while True:
                # Initialize the radius value
                radius = random.randint(RAD_MIN, RAD_MAX)

                # Initialize the center point
                center = [random.randint(-radius, width+radius), random.randint(-radius, height+radius)]

                colors = []

                # Initalize the color channels between 0 and 255
                for ch in range(self.channels):
                    colors.append(random.randint(0,255))
                # Initialize the alpha value between 0 and 1
                colors.append(random.random())

                newGene = gene.Gene(center, radius, colors, width, height)

                if newGene.valid:
                    break
            
            # Initialize a new gene with randomly calculated values
            self.chromosome.append(newGene)
        
        # Sort the genes according to their radius
        self.sortGenes()

    # Draw the image corresponding to the individual's solution
    def drawImage(self):
        # Create a blank image with 0 channel values
        self.image = np.zeros((self.height, self.width, self.channels), np.uint8)
        # Convert the black image to a white image
        self.image[:] = (255, 255, 255)

        for indGene in self.chromosome:
            overlay = self.image.copy()
            overlay = cv2.circle(overlay, indGene.center, indGene.radius, indGene.colors, thickness=-1)
            self.image = cv2.addWeighted(self.image, 1-indGene.alpha, overlay, indGene.alpha, 0.0)

        return self.image

    # Evaluate the image and the fitness of the individual
    def evalFitness(self, source):
        
        if self.fitness != 1: 
            # If the fitness is calculated previously, don't calculate again
            return self.fitness
        else:
            self.sortGenes()
            self.drawImage()
            # Use the fitness formula given in the manual
            fitness = 0
            for i in range(self.width):
                for j in range(self.height):
                    for k in range(self.channels):
                        fitness = fitness - (int(source[i][j][k]) - int(self.image[i][j][k]))**2
        
            self.fitness = fitness

        return self.fitness
    
    def getGeneRadius(self, gene):
        return gene.radius

    def sortGenes(self):
        self.chromosome.sort(reverse = True, key = self.getGeneRadius)