import csv
import os

from datetime import datetime

from collections import Counter
import itertools
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
            cumulative[datetime.strptime(row[0], '%Y/%m')] += int(row[1])

sorted_series = sorted(cumulative.items())

with open('commits_by_month.csv', 'w+') as fd:
    writer = csv.writer(fd)
    writer.writerow(['timestamp', 'commits'])

    for timestamp, value in sorted_series:
        row = (timestamp.strftime('%Y/%m'), value)
        writer.writerow(row)

plt.scatter(*zip(*sorted_series))
plt.grid()
plt.show()
