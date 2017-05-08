import csv
import os

from datetime import datetime

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
        # row = [datetime, value]
        for row in reader:
            timeseries.append((datetime.strptime(row[0], '%Y/%m').year, int(row[1])))

    for year, values in groupby(timeseries, lambda record: record[0]):
        year_sum = sum([value for _, value in values])
        cumulative[year] += year_sum

sorted_series = sorted(cumulative.items())

with open('commits.csv', 'w+') as fd:
    writer = csv.writer(fd)
    writer.writerow(['year', 'commits'])

    for row in sorted_series:
        writer.writerow(row)

plt.scatter(*zip(*sorted_series))
plt.grid()
plt.show()
