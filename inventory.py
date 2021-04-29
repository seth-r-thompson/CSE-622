import random
import matplotlib.pyplot as plt

def next_order(day):
    return random.randint(1,4) + day # uses mersenne twister for random numbers

# number of trials
max_trial = 100
trial = 1

# inventory variables
init_q1 = 49 # initial quantity of item 1
init_q2 = 56 # initial quantity of item 2
p1 = 7 # purchase order size for item 1
p2 = 8 # purchase order size for item 2

line1 = []
line2 = []

while (trial <= max_trial):
    # initialize trial variables
    day = 0
    o1 = next_order(day)
    o2 = next_order(day)

    # reset quantities
    q1 = init_q1
    q2 = init_q2

    while (q1 > 0 or q2 > 0):
        # check if item 1 order comes in
        if (day == o1 and q1>0):
            q1 -= p1
            o1 = next_order(day)

        # check if item 2 order comes in
        if (day == o2 and q2>0):
            q2 -= p2
            o2 = next_order(day)

        # record values in graph
        if len(line1) > day:
            line1[day] += q1
        else:
            line1.append(q1)

        if len(line2) > day:
            line2[day] += q2
        else:
            line2.append(q2)

        # increment day
        day += 1

    trial += 1

# calculate averages
for i in range(0, len(line1) - 1):
    line1[i] = line1[i] / trial
for i in range(0, len(line2) - 1):
    line2[i] = line2[i] / trial

# plot lines
plt.plot(line1, label = "Item 1")
plt.plot(line2, label = "Item 2")
plt.xlabel("Days")
plt.ylabel("Quantity")
plt.legend()
plt.show()