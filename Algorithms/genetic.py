from array import *
import random

#fitness function
def fitness(individual, data):
       #evaluate that individual somehow
       score = random.randint(0,100)
       return score

#quicksort implementation
def partition(array, low, high, arr2):
        pivot = array[high]
        i = low - 1
        for j in range(low, high):
              if array[j] <= pivot:
                     i = i+1
                     (array[i], array[j]) = (array[j], array[i])
                     (arr2[i], arr2[j]) = (arr2[j], arr2[i])
        (array[i+1], array[high]) = (array[high], array[i+1])
        (arr2[i+1], arr2[high]) = (arr2[high], arr2[i+1])
        return i + 1

def quickSort(array, low, high, arr2):
       if low < high:
              pi = partition(array, low, high, arr2)
              quickSort(array, low, pi-1, arr2)
              quickSort(array, pi+1, high, arr2)

#file input
def read_file(filename):
        data = []
        with open(filename) as f:
            for line in f:
                    data.append(list(map(str, line.strip().split(','))))
        return data

filename = "Datasets/knapsack_testcases-final/test400.kp"
oData = read_file(filename)

numItems = oData[0][0]
maxWeight = oData[0][1]

#create initial population
initPop = [100][numItems]

for i in range(100):
        for j in range (numItems):
               initPop[i][j] = random.randint(0,1)

#evaluate fitness of initial population
initScores = [100]

for i in range(100):
       initScores[i] = fitness(initPop[i], oData)

print("[" + initScores[0])
for i  in range(1, 100):
       print(initScores[i] + ",")
print("]\n")
quickSort(initScores, 0, 99, initPop)

print("[" + initScores[0])
for i  in range(1, 100):
       print(initScores[i] + ",")
print("]\n")