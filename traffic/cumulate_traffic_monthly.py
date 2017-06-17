import csv
import os
import sys

from datetime import datetime

from collections import Counter
import matplotlib.pyplot as plt

if len(sys.argv[1]) < 2:
    print('Directory have to be specified')
    exit()
path = sys.argv[1]
files = os.listdir(path)

cumulative = Counter()
for file in files:
    timeseries = []
    with open('{}/{}'.format(path, file), 'r') as fd:
        reader = csv.reader(fd)
        next(reader)
        # row = [datetime, value]
        for row in reader:
            cumulative[datetime.strptime(row[0], '%Y/%m')] += int(row[1])

sorted_series = sorted(cumulative.items())

with open('traffic_by_month.csv', 'w+') as fd:
    writer = csv.writer(fd)
    writer.writerow(['timestamp', 'commits'])

    for timestamp, value in sorted_series:
        row = (timestamp.strftime('%Y/%m'), value)
        writer.writerow(row)

plt.scatter(*zip(*sorted_series))
plt.grid()
plt.show()
