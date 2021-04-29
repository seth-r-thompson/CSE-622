import matplotlib.pyplot as plt
from numpy.core.numeric import NaN
from numpy.lib.function_base import average
import seaborn as sns
import pandas as pd
import numpy as np
import numpy.random as rng

# experiment fixed variables
capacity = 12 # max elevator capacity
travel = [[NaN, 1, 1.5, 1.75], [1, NaN, .5, .75], [1.5, .5, NaN, .5], [1.75, .5, .25, NaN]] # travel times between floors
wait = 0.5 # opening time of elevator
end = 60 # ending time (60 minutes elapsed)
interval = 0.25 # how much time passes each loop
trials = 10000 # number of trials
multiple_elevators = False

# evaluation metrics
waits, stairs, lasts, lens = [], [], [], []
q_shapes, e_shapes, s_shapes, wrk_per_min, wrk = [], [], [], [], []
e_shapes_2 = []

for i in range(0, trials):
    # simulation variables
    time = 0 # starting time (0 minutes elapsed)
    elevator = [] # people in the elevator
    queue = [] # people in line on ground floor
    floor = 0 # current floor elevator is on
    next_floors = [] # floors elevator is going to
    next_free_time = 0 # the next time the elevator is free to do a new task
    
    # metrics tracked
    total_workers = 0 # total workers who were generated
    total_wait = 0 # total wait time of all workers
    last_board = 0 # last time a worker boarder
    queue_lens = [0, 0, 0] # amount of people in line at 8:30, 8:45, and 9
    stair_users = [0, 0, 0] # amount of people that take stairs to floors 2/3/4 on a given day

    # other metrics
    queue_shape = [] # amount of workers in line each time interval
    elevator_shape = [] # amount of workers in elevator each time interval
    stair_shape = [] # amount of workers that took stairs in each time interval
    
    # stuff for elevator 2 if enabled
    elevator_shape_2 = []
    elevator_2 = []
    floor_2 = 0
    next_free_time_2 = 0
    next_floors_2 = []

    while True:        
        # update metrics
        total_wait += len(queue) * interval
        queue_shape.append(len(queue))
        elevator_shape.append(len(elevator))
        elevator_shape_2.append(len(elevator_2))
        stair_shape.append(sum(stair_users))
        if time == 30: # at 8:30
            queue_lens[0] = len(queue)
        if time == 45: # at 8:45
            queue_lens[1] = len(queue)
        if time == 60: # at 9:00
            queue_lens[2] = len(queue)

        # if a minute has gone buy, generate new workers
        # if int(time) == time:
        if True:
            # new = rng.exponential(scale=6) # random number of new workers
            new = rng.exponential(scale=6/4)
            total_workers += new # update metric
            # create the new workers
            for worker in range(0, int(new)):
                worker = rng.choice([1,2,3]) # worker destination
                # will worker use stairs?
                if len(queue) > capacity and ((worker == 1 and rng.rand() <= 0.5) or (worker == 2 and rng.rand() <= 0.33) or (worker == 3 and rng.rand() <= 0.1)):
                        stair_users[worker-1] += 1
                # if not, add workers to queue
                else:
                    queue.append(worker)

        # if first elevator is free, next task
        if time >= next_free_time:
            # if on ground floor and empty, board
            if floor == 0 and not elevator:
                next_free_time = time + 0.5 # time elevator is stopped
                # board workers until full
                while len(elevator) < capacity and len(queue) > 0:
                    worker = queue.pop(0) # FIFO
                    elevator.append(worker) 
                    # worker makes floor request if not already made
                    if worker not in next_floors:
                        next_floors.append(worker)
                    last_board = time # update metric

            # elif on other floor, unboard
            elif floor in next_floors:
                next_free_time = time + 0.5 # time elevator is stopped
                next_floors.remove(floor) # remove floor from requests
                # unboard workers
                elevator = [worker for worker in elevator if worker != floor]         

            # else find next location
            else:
                # if floors remainings, go nearest
                if next_floors:
                    next_floor = min(next_floors)
                # else return to ground floor
                else:
                    next_floor = 0
                # travel to next floor
                next_free_time = time + travel[floor][next_floor] # time elevator takes to go to next floor
                floor = next_floor

        # if second elevator is free and enabled, next task
        if time >= next_free_time_2 and multiple_elevators:
            # if on ground floor and empty, board
            if floor_2 == 0 and not elevator_2:
                next_free_time_2 = time + 0.5 # time elevator is stopped
                # board workers until full
                while len(elevator_2) < capacity and len(queue) > 0:
                    worker = queue.pop(0) # FIFO
                    elevator_2.append(worker) 
                    # worker makes floor request if not already made
                    if worker not in next_floors_2:
                        next_floors_2.append(worker)
                    last_board = time # update metric

            # elif on other floor, unboard
            elif floor_2 in next_floors_2:
                next_free_time_2 = time + 0.5 # time elevator is stopped
                next_floors_2.remove(floor_2) # remove floor from requests
                # unboard workers
                elevator_2 = [worker for worker in elevator_2 if worker != floor_2]         

            # else find next location
            else:
                # if floors remainings, go nearest
                if next_floors_2:
                    next_floor_2 = min(next_floors_2)
                # else return to ground floor
                else:
                    next_floor_2 = 0
                # travel to next floor
                next_free_time_2 = time + travel[floor_2][next_floor_2] # time elevator takes to go to next floor
                floor_2 = next_floor_2

        # increment time
        time += interval

        # stop simulation
        if time > end:
            break

    # sum up metrics
    waits.append(total_wait / total_workers)
    stairs.append(sum(stair_users))
    lasts.append(last_board)
    lens.append(queue_lens)

    q_shapes.append(queue_shape)
    e_shapes.append(elevator_shape)
    e_shapes_2.append(elevator_shape_2)
    s_shapes.append(stair_shape)
    wrk_per_min.append(total_workers / time)
    wrk.append(total_workers)

print("Average wait:", average(waits))
print("Average stair users:", average(stairs))
print("Average last board:", average(lasts))

len_830, len_845, len_900 = 0,0,0
for queue in lens:
    len_830 += queue[0]
    len_845 += queue[1]
    len_900 += queue[2]

print("Average queue at 8 30:", len_830/trials)
print("Average queue at 8 45:", len_845/trials)
print("Average queue at 9 00:", len_900/trials)

print("Average worker per min", average(wrk_per_min), " which made ", average(wrk))

plt.violinplot(waits, showmeans=True, showextrema=True, showmedians=True)
plt.show()
plt.violinplot(stairs, showmeans=True, showextrema=True, showmedians=True)
plt.show()
plt.violinplot(lasts, showmeans=True, showextrema=True, showmedians=True)
plt.show()

plt.plot(range(0,60*60+15,15), np.mean(np.array(q_shapes), axis=0), label="in queue")
if not multiple_elevators:
    plt.plot(range(0,60*60+15,15), np.mean(np.array(e_shapes), axis=0), label="in elevator")
else:
    plt.plot(range(0,60*60+15,15), np.mean(np.array(e_shapes), axis=0), label="in elevator 1")
    plt.plot(range(0,60*60+15,15), np.mean(np.array(e_shapes_2), axis=0), label="in elevator 2")
plt.plot(range(0,60*60+15,15), np.mean(np.array(s_shapes), axis=0), label="took stairs")
plt.legend()
plt.show()