import csv
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class DataNotFound(RuntimeError):
    pass

class Scraper:
    def __init__(self):
        self.resource = 'https://www.semrush.com/info/{}'
        binary = FirefoxBinary('/usr/lib/firefox/firefox')
        self.driver = webdriver.Firefox(firefox_binary=binary)

    def scrape_data(self, page):
        resource = 'https://www.semrush.com/info/{}'.format(page)
        self.driver.get(resource)

        series = self.driver.find_element_by_class_name('highcharts-markers.highcharts-tracker')
        elements = series.find_elements_by_tag_name('path')


        retry_counter = 0
        while True:
            try:
                self.driver.find_element_by_class_name('highcharts-container.notes-container.notes-container_small')
                break
            except:
                retry_counter += 1
                time.sleep(0.1)
                if retry_counter > 150:
                    raise DataNotFound

        print('\tContent loading took {} s'.format(retry_counter * 0.1))
        results = []
        for element in elements:
            hover = ActionChains(self.driver).move_to_element(element)
            hover.perform()
            # time.sleep(0.5)
            try:
                origin = self.driver.find_element_by_class_name(
                    'highcharts-container.notes-container.notes-container_small')
                record = origin.find_elements_by_xpath(r"*[@class='highcharts-tooltip']/span")[0].text.split('\n')
                results.append(self.parse_record(record))
            except Exception as e:
                print(e)

        results.sort(key=lambda x: x[0])
        return results

    @staticmethod
    def parse_record(record):
        from datetime import datetime
        timestring, trafficstring, paidtrafficstring = record
        timestamp = datetime.strptime(timestring, '%b %Y')
        traffic_value = int(trafficstring.split(' ')[1].replace(',', ''))
        paid_traffic_value = int(paidtrafficstring.split(' ')[2].replace(',', ''))

        return timestamp, traffic_value, paid_traffic_value


def main():
    import csv
    site_infos = []
    with open('sites.csv', 'r') as fd:
        reader = csv.reader(fd)
        for row in reader:
            site_infos.append(row)

    import os
    already_parsed = os.listdir('csv_traffic')

    scraper = Scraper()
    for project, website in site_infos:
        if '{}.csv'.format(project) in already_parsed:
            print('Already parsed project ({}, {}) '.format(project, website))
            continue
        print('Scraping project ({}, {})...'.format(project, website))
        try:
            data = scraper.scrape_data(website)
        except DataNotFound:
            print('\tNo contents to scrape')
            continue

        storage_formatted_data = [(dt.strftime('%Y/%m'), traffic, ptraffic) for dt, traffic, ptraffic in data]

        with open('csv_traffic/{}.csv'.format(project), 'w') as fd:
            writer = csv.writer(fd)
            writer.writerow(['timestamp', 'traffic', 'paid traffic'])

            for record in storage_formatted_data:
                writer.writerow(record)

if __name__ == '__main__':
    main()
