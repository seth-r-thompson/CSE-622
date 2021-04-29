import numpy.random as rand
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd

# simple path class for mutability as parameter
class path:
    choices = ""
    weight = 0

    def update(self, choice, weight):
        self.choices += str(choice)
        if (choice != 7):
            self.choices += " "
        self.weight += weight

    def unpack(self):
        return [self.choices, self.weight]

# region branches

def from_1(path):
    path.update(1, 0)
    next = rand.choice([2,5])
    
    if (next == 2):
        path.update(2, rand.uniform(4,6))
        return from_2(path)
    elif (next == 5):
        path.update(5, 6)
        return from_5(path)

def from_2(path):
    next = rand.choice([3,4])

    if (next == 3):
        path.update(3, 6)
        return from_3(path)
    elif (next == 4):
        path.update(4, rand.uniform(6,8))
        return from_4(path)

def from_3(path):
    path.update(4, rand.triangular(4,8,10))
    return from_4(path)

def from_4(path):
    path.update(7, 4)
    return path # end reached

def from_5(path):
    next = rand.choice([3, 4, 6])

    if (next == 3):
        path.update(3,8)
        return from_3(path)
    elif (next == 4):
        path.update(4,11)
        return from_4(path)
    elif (next == 6):
        path.update(6,rand.uniform(8,10))
        return from_6(path)

def from_6(path):
    path.update(7, rand.uniform(9,10))
    return path # end reached

# endregion

# run trials
paths, trials = [], 1000000
for i in range(0, trials):
    paths.append(from_1(path()).unpack())

# plot data
data = list(tuple(pd.DataFrame(paths, columns = ["Path", "Time"]).groupby("Path"))) # tabularized data grouped by the path
palette = iter(sb.husl_palette(len(data))) # create enough colors for each group
for group in data:
    if (group[0] == "1 5 4 7"):
        continue # skip this group; since it's always 21, it skews the chart
    sb.histplot(label=group[0], data = group[1], x="Time", color=next(palette))
plt.legend()
plt.show()