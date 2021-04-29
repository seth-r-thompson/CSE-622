import collections
import functools
import operator
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import size
import seaborn as sns
import pandas as pd
import numpy as np
import numpy.random as rand

sizes = [100, 1000, 10000] # party sizes
durations = [10, 20, 40] # party durations
trials = 1000

def party(size, duration):
    shape = {0 : [size - 1, 1, 0]} # state of party at each minute
    percent = {0 : round(100 * (1 / size), 2)} # percent who've heard rumor at each minute

    students = np.zeros(size) # number of times each student had heard rumor
    students[0] = 1 # starting point

    for minute in range(1, duration + 1):
        rand.shuffle(students) # randomize array order

        for j in range(size//2):
            # both students are rumor spreaders
            if students[j] == 1 and students[j + size//2] == 1:
                students[j] += rand.choice([0,1])
                students[j + size//2] += rand.choice([0,1])
            # only first student is rumor spreader
            elif students[j] == 1:
                students[j + size//2] += rand.choice([0,1])
            # only second student is rumor spreader
            elif students[j + size//2] == 1: 
                students[j] += rand.choice([0,1])

        shape[minute] = [np.count_nonzero(students == 0), np.count_nonzero(students == 1), np.count_nonzero(students >= 2)]
        percent[minute] = round(100 * (np.count_nonzero(students > 0) / size), 2)

    return shape, percent

experiments = {}
for duration in durations:
    for size in sizes:
        parties, experiment = [], []

        # conduct trials
        for i in range(trials):
            shape, percent = party(size, duration)
            parties.append(percent)
        
        # calculate average across trials
        for minute, percent in sorted(dict(functools.reduce(operator.add, map(collections.Counter, parties))).items()):
            experiment.append(round(percent / trials,2))
        
        experiments[str(size) + " ppl " + str(duration) + " min"] = experiment

data = pd.DataFrame.from_dict(experiments, orient='index').transpose()
palette = iter(sns.husl_palette(9))

i = 0
for experiment in data:
    i += 1
    plt.subplot(3,3, i)
    
    for other in data:
        plt.plot(data[other], color='grey', linewidth=0.5, alpha=0.25)

    plt.plot(data[experiment], color=next(palette), linewidth=2, label=experiment)
    plt.title(experiment)

plt.show()