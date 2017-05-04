import csv
import os

from collections import Counter
from itertools import groupby
import matplotlib.pyplot as plt


files = os.listdir('csv_commits')

cumulative = Counter()
for file in files:
    timeseries = []
    with open('csv_commits/' + file, 'r') as fd:
        reader = csv.reader(fd)
        next(reader)
        # row = [year, month, value]
        for row in reader:
            timeseries.append((int(row[0]), int(row[2])))

    for year, values in groupby(timeseries, lambda record: record[0]):
        year_sum = sum([value for _, value in values])
        cumulative[year] += year_sum

final_timeseries = sorted(cumulative.items())

plt.plot(*zip(*final_timeseries))
plt.grid()
plt.show()
