import csv
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# resource = 'https://www.semrush.com/info/dolibarr.com'
# binary = FirefoxBinary('/usr/lib/firefox/firefox')
# firefox = webdriver.Firefox(firefox_binary=binary)
# firefox.get(resource)

# # time.sleep(5)
# series = firefox.find_element_by_class_name('highcharts-markers.highcharts-tracker')
# elements = series.find_elements_by_tag_name('path')
# # time.sleep(0.1)
#
# retry_counter = 0
# while True:
#     try:
#         firefox.find_element_by_class_name('highcharts-container.notes-container.notes-container_small')
#         break
#     except:
#         retry_counter += 1
#         time.sleep(0.1)
#
# print('Content loading took {} s'.format(retry_counter * 0.1))
#
# for element in elements:
#     hover = ActionChains(firefox).move_to_element(element)
#     hover.perform()
#     # time.sleep(0.5)
#     try:
#         origin = firefox.find_element_by_class_name('highcharts-container.notes-container.notes-container_small')
#         print(origin.find_elements_by_xpath(r"*[@class='highcharts-tooltip']/span")[0].text.split('\n'))
#     except Exception as e:
#         print(e)


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

        print('Content loading took {} s'.format(retry_counter * 0.1))
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
        traffic_value = int(trafficstring.split(' ')[1])
        paid_traffic_value = int(paidtrafficstring.split(' ')[2])

        return timestamp, traffic_value, paid_traffic_value


def main():
    scraper = Scraper()
    from pprint import pprint
    data = scraper.scrape_data('dolibarr.com')
    import matplotlib.pyplot as plt
    plt.scatter([x[0] for x in data], [x[1] for x in data])
    plt.show()

if __name__ == '__main__':
    main()
