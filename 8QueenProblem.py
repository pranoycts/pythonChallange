# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 15:04:50 2020

@author: Pranoy Ghosh :  ID 260615

Steps:
    1. Initial Population
    2. Applying Fitness Function
    3. Selecting parents
    4. Crossover of parents to produce new generation
    5. Mutation of new generation
    6. Repeat until solution is reached     
"""

import random

#making random chromosomes 
def initial_population(size): 
    return [ random.randint(0, size-1) for _ in range(size) ]

def calculate_fitness(chromosome):
    horizontal_collisions = sum([chromosome.count(queen)-1 for queen in chromosome])/2
    diagonal_collisions = 0

    n = len(chromosome)
    left_diagonal = [0] * 2*n
    right_diagonal = [0] * 2*n
    for i in range(n):
        left_diagonal[i + chromosome[i] - 1] += 1
        right_diagonal[len(chromosome) - i + chromosome[i] - 2] += 1

    diagonal_collisions = 0
    for i in range(2*n-1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i]-1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i]-1
        diagonal_collisions += counter / (n-abs(i-n+1))
    
    return int(maxFitness - (horizontal_collisions + diagonal_collisions))

def select_for_reproduce(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"

def selection_probability(chromosome, fitness):
    return fitness(chromosome) / maxFitness

#doing cross_over between two chromosomes
def reproduce(x, y): 
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]

# randomly changing the value of a random index of a chromosome
def apply_mutation(x):  
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(0, n - 1)
    x[c] = m
    return x

def genetic_queen(population, fitness):
    mutation_probability = 0.03
    new_population = []
    probabilities = [selection_probability(n, fitness) for n in population]
    # 3.Selecting parents
    for i in range(len(population)):
        x = select_for_reproduce(population, probabilities) #best chromosome 1
        y = select_for_reproduce(population, probabilities) #best chromosome 2
        # 4. Crossover of parents to produce new generation
        child = reproduce(x, y) 
        if random.random() < mutation_probability:
            # 5. Mutation of new generation
            child = apply_mutation(child)
        print_chromosome(child)
        new_population.append(child)
        if fitness(child) == maxFitness:
            break
    return new_population

def print_chromosome(chrom):
    print("Chromosome = {},  Fitness Score = {}"
        .format(str(chrom), calculate_fitness(chrom)))

if __name__ == "__main__":
    noOfQueen = 8
    maxFitness = (noOfQueen*(noOfQueen-1))/2
    # 1.Initial Population
    population = [initial_population(noOfQueen) for _ in range(100)]    
    generation = 1
    
    #print(population)
    
    # 2.Applying Fitness Function
    while not maxFitness in [calculate_fitness(chrom) for chrom in population]:
        print("=== Generation {} ===".format(generation))
        population = genetic_queen(population, calculate_fitness)
        print("")
        print("Maximum Fitness = {}".format(max([calculate_fitness(n) for n in population])))
        generation += 1
    chrom_out = []
    print("Solved in Generation {} !".format(generation-1))
    for chrom in population:
        if calculate_fitness(chrom) == maxFitness:
            print("");
            print("One of the solutions: ")
            chrom_out = chrom
            print_chromosome(chrom)
            
    
