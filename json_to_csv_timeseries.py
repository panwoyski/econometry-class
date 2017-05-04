import json
import os
from datetime import datetime

import csv

files = os.listdir('raw')
print(len(files))

for file in files:
    with open('raw/' + file, 'r') as fd:
        data = json.load(fd)
    # [[unix_time, commit value]...]
    timeseries = data['series'][0]['data']

    formatted_timeseries = []
    for timestamp, value in timeseries:
        dt_time = datetime.utcfromtimestamp(timestamp/1000)
        formatted_timeseries.append((dt_time.year, dt_time.month, value))

    with open('csv_commits/' + file.split('.')[0] + '.csv', 'w+') as fd:
        writer = csv.writer(fd)
        writer.writerow(['year', 'month', 'commits'])

        for row in formatted_timeseries:
            writer.writerow(row)
