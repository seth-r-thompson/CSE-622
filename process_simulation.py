import numpy.random as rng
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

trials = 1000000
times = []
for i in range(0,trials):
    # deteriministic nodes
    time_2 = rng.uniform(4,6)
    time_5 = 6
    time_6 = time_5 + rng.uniform(8,10)
    
    # variable nodes
    time_3 = max(time_2 + 6, time_5 + 8)
    time_4 = max(time_2 + rng.uniform(6,8), time_3 + rng.triangular(4,8,10), time_5 + 11)

    # final time
    time_7 = max(time_4 + 4, time_6 + rng.uniform(9,10))
    times.append(time_7)

# plot data
data = pd.DataFrame(times, columns=["Time"])
sns.histplot(data=data, x="Time")
plt.show()

sns.boxplot(data=data, y="Time")
plt.show()