import random
import matplotlib.pyplot as plt

def simulation(tagteam = False):
    customers = [ [12, 40], [31, 32], [63,55], [95,48], [99,18], [154,50], [198,47], [221,18], [304,28], [346,54], [411,40], [455, 72], [537, 12] ]
    queue = []
    time, server_busy_time, trainee_busy_time = 0, 0, 0
    results = []

    while (True):
        if (time >= customers[0][0]):
            queue.append(customers.pop(0))

        if (queue and time >= server_busy_time):
            customer = queue.pop(0)
            server_busy_time = time + customer[1]
            customer_wait = time - customer[0]
            results.append([server_busy_time, customer_wait])

        if (tagteam and queue and time >= trainee_busy_time):
            other_customer = queue.pop(0)
            trainee_busy_time = time + other_customer[1]
            other_customer_wait = time - other_customer[0]
            results.append([server_busy_time, other_customer_wait])

        if(not customers):
            break
        
        time += 1
    
    return results

results_solo = simulation(tagteam = False)
results_tagteam = simulation(tagteam = True)

plt.plot(results_solo)
plt.plot(results_tagteam)
plt.legend(["departure (solo)", "wait (solo)", "deparature (tagteam)", "wait (tagteam)"])
plt.show()