import random as rand
import matplotlib.pyplot as plt
import seaborn as sb
import pandas as pd

# function to run the experiment
def interviews(trial = 1000000, question = 20, fixed_choice = False, choice = 5):
    scores = []
    
    for i in range(0, trial):
        correct = 0

        for j in range(0, question):
            answer = rand.randint(1,5)
            guess = rand.randint(1,5)

            if (fixed_choice):
                answer = choice # replace random answer with the fixed answer

            if (answer == guess):
                correct += 1

        scores.append(correct / question)
    
    return scores

scores_rand = interviews() # random answer each time
scores_fixed = interviews(fixed_choice = True) # answer is always 5

# box plots
fig, axis = plt.subplots()
axis.boxplot(scores_rand, positions = [1])
axis.boxplot(scores_fixed, positions = [2])
axis.set_xticklabels(["Random\nAnswer", "Fixed\nAnswer"])

# violin plots to show distribution
violins = plt.violinplot([scores_rand, scores_fixed])
for partname in ("cbars","cmins","cmaxes"):
    violins[partname].set_edgecolor("black") # fix colors so overlap isn't bad

plt.show()