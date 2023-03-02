from array import *
import random

bestVal = 0

#fitness function
def fitness(individual, data, maxWeight, avgRatio, avgVal):
       value = 0
       weight = 0
       for i in range(len(individual)):
              if(individual[i] == 1):
                     value += int(data[i+1][2])
                     weight += int(data[i+1][1])
       
       print("Evaluating fitness, value: ",value," weight: ",weight," avgVal: ",avgVal, " maxWeight ", maxWeight)
       
       #edge case
       if(weight == 0):
              return 0.1
       
       score = value/avgVal
       
       if(float(weight)/maxWeight > 0.5 and float(weight) < maxWeight):
              score += .5
       
       if(score >= 1):
              score -= 1
              score *= 10
              score += 1
       
       score += float(random.randint(0,1))/10
       # else:
       #        temp = 1 - score
       #        temp *= 10
       #        score -= temp
       
       global bestVal
       if weight > maxWeight:
              score -= score / 10
       else:
              if(value > bestVal):
                     bestVal = value
       
       print("Score",score)
       print("Current Best Value",bestVal)
       return score

#quicksort implementation
def partition(array, low, high, arr2):
        pivot = array[high]
        i = low - 1
        for j in range(low, high):
              if array[j] >= pivot:
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
numItems = int(numItems)
maxWeight = int(maxWeight)

#create initial population
rows, cols = (100, numItems)
currPop = [[0 for i in range(cols)] for j in range(rows)]

totalValue = 0
totalRatio = 0
count = 0
for i in range(100):
       for j in range (numItems):
              currPop[i][j] = random.randint(0,1)

#evaluate fitness of initial population
currScores = [0 for i in range(100)]

totalValue = 0
totalWeight = 0
count = 0
for i in range(100):
       for j in range(numItems):
              if(currPop[i][j] == 1):
                     totalWeight += int(oData[j+1][1])
                     totalValue += int(oData[j+1][2])
                     count += 1

for i in range(100):
       if(totalWeight == 0):
              currScores[i] = 0
       else:
              currScores[i] = fitness(currPop[i], oData, maxWeight, float(totalValue)/totalWeight, float(totalValue)/100)
# print(currScores)


quickSort(currScores, 0, 99, currPop)

best = currPop[0]

# print("\n\nAfter sorting\n\n")


# print(currScores)

#All other generations
for k in range(199):
       print("In ",k," generation")
       #build intermediate population using remainder stochastic sampling
       midPop = [[0 for i in range(cols)] for j in range(rows)]
       
       #popLeft denotes the number of slots still to be filled in the intermediate population, the program moves on once popLeft reaches 100
       popLeft = 0
       
       #very fit genotypes get added to intermediate population
       for i in range(100):
              if(currScores[i] >= 1.0):             #good genotypes get immediately added into intermediate population
                     midPop[popLeft] = currPop[i]
                     popLeft += 1
              else:                                 #bad genotypes do not immediately get moved into intermediate, but still have a chance later
                     break
       
       #fill remaining spots proportionally
       count = 0
       while(popLeft < 100):
              if(count == 100): #reached end of population, restart to continue filling intermediate population
                     count = 0
              if(currScores[count] % 1 > random.random()): #randomly proportionally add genotype to intermediate population
                     midPop[popLeft] = currPop[count]
                     popLeft += 1
              count += 1
       
       #print("\n\nNew intermediate population\n\n")
       
       #built new current population through recombination
       count = 0
       for i in range(50):
              #randomly choose two parents from intermediate population
              donor1 = midPop[random.randint(0, 99)]
              donor2 = midPop[random.randint(0, 99)]
              
              #randomly recombine or pass parents through unchanged
              if(random.randint(0,10) == 1):
                     currPop[count] = donor1
                     currPop[count + 1] = donor2
              
              #recombination
              else:
                     split = random.randint(0, numItems)
                     for j in range(numItems):
                            if(j < split): #before crossover
                                   currPop[count][j] = donor1[j]
                                   currPop[count+1][j] = donor2[j]
                            else: #after crossover
                                   currPop[count][j] = donor2[j]
                                   currPop[count+1][j] = donor1[j]
              
              #randomly mutate some genes of first child
              for j in range(numItems):
                     if(random.random() <= 0.005): # if mutation, flip bit
                            if(currPop[count] == 0):
                                   currPop[count][j] = 1
                            else:
                                   currPop[count][j] = 0

              #randomly mutate some genes of second child
              for j in range(numItems):
                     if(random.random() <= 0.005): # if mutation, flip bit
                            if(currPop[count+1] == 0):
                                   currPop[count+1][j] = 1
                            else:
                                   currPop[count+1][j] = 0
              
              #after children are created, count += 2 to prep for next children
              count += 2

       # for i in range(100):
       #        print(currPop[i])

       #recalculate fitness
       totalValue = 0
       totalWeight = 0
       count = 0
       for i in range(100):
              for j in range(numItems):
                     if(currPop[i][j] == 1):
                            totalWeight += int(oData[j+1][1])
                            totalValue += int(oData[j+1][2])
                            count += 1
       
       for i in range(100):
              if(totalWeight == 0):
                     currScores[i] = 0
              else:
                     currScores[i] = fitness(currPop[i], oData, maxWeight, float(totalValue)/totalWeight, float(totalValue)/100)
       #print(currScores)


       quickSort(currScores, 0, 99, currPop)

       best = currPop[0]

       #print("\n\nAfter sorting\n\n")


       #print(currScores)

print("The highest value found was ", bestVal)