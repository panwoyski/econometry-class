import json
import os
from collections import Counter
import matplotlib.pyplot as plt
import datetime

files = os.listdir('raw')

cumulative = Counter()
for file in files:
    with open('raw/' + file, 'r') as fd:
        data = json.load(fd)
    timeseries = data['series'][0]['data']
    count = Counter({timestamp: value for timestamp, value in timeseries})
    cumulative += count

plt.plot(*zip(*(sorted(cumulative.items()))))
plt.show()
