import csv
import os
from datetime import datetime

from collections import Counter
from itertools import groupby

import matplotlib.pyplot as plt

path = 'csv_traffic/scrape-201706082337'
files = os.listdir(path)

cumulative = Counter()
for file in files:
    timeseries = []
    with open('{}/{}'.format(path, file), 'r') as fd:
        reader = csv.reader(fd)
        next(reader)
        for timestamp, traffic, _foo in reader:
            year = datetime.strptime(timestamp, "%Y/%m").year
            timeseries.append((year, int(traffic)))

    for year, values in groupby(timeseries, lambda x: x[0]):
        year_sum = sum(value for _bar, value in values)
        cumulative[year] += year_sum

sorted_series = sorted(cumulative.items())
print(sorted_series)

with open('traffic.csv', 'w') as fd:
    writer = csv.writer(fd)
    writer.writerow(['year', 'traffic'])

    for row in sorted_series:
        writer.writerow(row)

plt.scatter(*zip(*sorted_series))
plt.grid()
plt.show()
