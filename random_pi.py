import numpy as np
import matplotlib.pyplot as plt

# simulation variables
sample = 100000000

# setup
hit_count = 0
x_hits = []
y_hits = []
x_miss = []
y_miss = []

# generate uniform random distribution of numbers
x = np.random.uniform(-1,1,sample)
y = np.random.uniform(-1,1,sample)

# calculate hits or misses
for i in range(0, sample):
    dist = (x[i]**2 + y[i]**2)

    if dist < 1:
        hit_count += 1
        x_hits.append(x[i])
        y_hits.append(y[i])
    else:
        x_miss.append(x[i])
        y_miss.append(y[i])

# calculate pi
pi = 4.0 * (hit_count / sample)

# add hits and misses
plt.scatter(x_hits, y_hits, color="r", label = "hits = " + str(hit_count))
plt.scatter(x_miss, y_miss, color="b", label = "miss = " + str(sample - hit_count))

# add circle for reference
circle = plt.Circle((0,0), 1, fill = False, label = "pi ≈ " + str(pi))
plt.gca().add_patch(circle)

# show plot
plt.legend(loc="upper right")
plt.show()