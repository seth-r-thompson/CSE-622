import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

data = [0.06, 0.08, 0.1, 0.21, 0.27, 0.28, 0.34, 0.36, 0.37, 0.46, 0.61, 0.62, 0.7, 0.79, 0.82, 0.88, 0.89, 0.92, 0.94, 0.98]

# bins = [2, 1, 3, 3, 1, 0, 2, 2, 3, 3]
# sum = 0

# for bin in bins:
#     sum += (bin-2)**2 / 2

# print(sum)

this_year = [20, 22, 13, 2, 2]
last_year = [10, 19, 25, 4, 1]

sum = 0
for i in range(0,5):
    sum += (this_year[i] - last_year[i])**2 / last_year[i]

print(sum)

result = stats.chisquare(data, None, 9)
print(result)

# plt.hist(data, bins=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
# plt.show()