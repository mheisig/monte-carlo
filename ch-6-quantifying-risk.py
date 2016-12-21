"""
Python implementation of the most basic Monte Carlo simulation in "How to Measure Anything." This
simulates the lease of a machine for a manufacturing facility. Variables are randomly sampled from
normal distributions. This also models a 10% chance of a contract loss at a random month in the year
with a value of 1000 units/month.abs

This generates a histogram chart of the distribution of total savings for 10,000 simulation iterations.
"""
import numpy
import pylab

SIMULATIONS = 10000
BREAK_EVEN = 400000

# maintenance savings
ms_lower = 10
ms_upper = 20

# labor savings
ls_lower = -2
ls_upper = 8

# raw material savings
rms_lower = 3
rms_upper = 9

# production level
pl_lower = 15000
pl_upper = 35000

def sample_normal_dist(lower, upper):
    """
    Returns sample from a 90% CI range with a normal distribution shape

    lower -- 90% CI lower bound
    upper -- 90% CI upper bound
    """
    mean = (upper + lower) / 2
    sd = (upper - lower) / 3.29
    return numpy.random.normal(loc=mean, scale=sd)

def sample_binary_dist(p):
    """
    Samples a binary distribution

    p -- probability that it will return 1
    """
    return numpy.random.binomial(1, p)

vals = []
for i in range(0, SIMULATIONS):
    ms = sample_normal_dist(ms_lower, ms_upper)
    ls = sample_normal_dist(ls_lower, ls_upper)
    rms = sample_normal_dist(rms_lower, rms_upper)
    pl = sample_normal_dist(pl_lower, pl_upper)

    savings = (ms + ls + rms) * pl
    
    # simulate 10% probability of a 1000 unit/month contract loss
    if (sample_binary_dist(0.1)):
        savings = savings - (1000 * numpy.random.randint(0, high=12))

    vals.append(savings)
    
break_even_count = len([1 for i in vals if i > BREAK_EVEN])
break_even_perc = break_even_count / SIMULATIONS * 100
over_100k = len([1 for i in vals if i > BREAK_EVEN - 100000])
over_100k_perc = over_100k / SIMULATIONS * 100
max_savings = len([1 for i in vals if i > 1000000])
max_savings_perc = max_savings / SIMULATIONS * 100

print('Number of simulations that break even: {}/{}'.format(break_even_count, SIMULATIONS))
print('Probability of loss: {0:.2f}%'.format(100 - break_even_perc))
print('Probability of loss > $100k: {0:.2f}%'.format(100 - over_100k_perc))
print('Probability of savings > $1m: {}%'.format(max_savings_perc))

pylab.hist(vals, bins=100)
pylab.show()