from dis import disassemble
from ortools.algorithms import pywrapknapsack_solver

from itertools import islice # islice() function in itertools module make iterating through the iterables like lists and strings very easily

import timeit # This module provides a simple way to find the execution time of small bits of Python code.

import time

import pandas as pd

testCases = [
    'n00050',
    'n00100',
    'n00200',
    'n00500',
    'n01000'
]
groupTestCases = [
    '00Uncorrelated',
    '01WeaklyCorrelated',
    '02StronglyCorrelated',
    '03InverseStronglyCorrelated',
    '04AlmostStronglyCorrelated',
    '05SubsetSum',
    '06UncorrelatedWithSimilarWeights',
    '07SpannerUncorrelated',
    '08SpannerWeaklyCorrelated',
    '09SpannerStronglyCorrelated',
    '10MultipleStronglyCorrelated',
    '11ProfitCeiling',
    '12Circle',
]

col = [
    "Group",
    "Case",
    "Total value",
    "Total weight",
    "Runtime (s)",
    "Optimal (Y/N)"
]

index = 1

result = []

for groupTestCase in groupTestCases:
    
    for testCase in testCases:
        
        filepath = ".\choose_groupTestcases/" + groupTestCase + '/'

        a = open(filepath + "Result " + str(index) + ".txt", "a+")
        res = open(".\saveResult/Result.txt", "a+") # output to result.txt

        capacities = []
        values = []
        weights = [[]]
        f = open(filepath + testCase + '.kp')
        lines = f.read().splitlines()
                        
        capacities.append(int(lines[2]))
        for line in islice(lines, 4, None):
            data = line.split()
            values.append(int(data[0]))
            weights[0].append(int(data[1]))

        solver = pywrapknapsack_solver.KnapsackSolver (
            pywrapknapsack_solver.KnapsackSolver.
            KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample'
        )

        solver.Init(values, weights, capacities)
        time_limit = 120.0
        solver.set_time_limit(time_limit)


        start = time.time()
        computed_value = solver.Solve()
        end = time.time()

        packed_items = []
        packed_weights = []
        total_weight = 0
        string = str(testCase + '.kp\nTotal value = ' + str(computed_value))
        a.write(string + '\n')
        res.write(string + '\n')

        for i in range(len(values)):
            if solver.BestSolutionContains(i):
                packed_items.append(i)
                packed_weights.append(weights[0][i])
                total_weight += weights[0][i]


        a.write (
              'Total weight: '+ str(total_weight) + '\n'
            + 'Packed items: '+ str(packed_items) + '\n' 
            + 'Packed_weights: '+ str(packed_weights) + '\n'
            + 'Runtime: ' + str(round(end - start, 4)) + 's' + '\n\n'
        )
        res.write (
            groupTestCase + '\n'
            + 'Total weight: '+ str(total_weight) + '\n'
            + 'Packed items: '+ str(packed_items) + '\n' 
            + 'Packed_weights: '+ str(packed_weights) + '\n'
            + 'Runtime: ' + str(round(end - start, 4)) + 's' + '\n\n'
        )
        print (
            'Group: ' + groupTestCase
            + ' | ' + 'Case: ' + testCase + '.kp'
            + ' | ' + 'Value: ' + str(computed_value)
            + ' | ' + 'Weight: ' + str(total_weight)
            + ' | ' + 'Time: ' + str(end - start) + 's'
        )

        opt = 'No'
        if (end - start) <= time_limit: opt = 'Yes'

        result.append([
            groupTestCase,
            testCase,
            computed_value,
            total_weight,
            round((end - start), 6),
            opt
        ])

    print("-------------------------------------------------------------------------------------------------------------------------------------")

    index += 1
    a.close()

def save_csv(data, column):
    df = pd.DataFrame(data, columns=column)
    df.to_csv('saveResult/Result.csv')

save_csv(result, col)