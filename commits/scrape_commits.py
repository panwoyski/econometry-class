import requests
import sys
import random
import time
import bs4

products = [
    'odoo',
    'oca',
    'kivitendo',
    'openbravo',
    'openconcerto',
    'postbooks',
    'jfire',
    'promet-erp',
    'dolibarr',
    'weberp',
    'tryton',
    'adempiere',
    'erp5',
    'Apache-OFBiz',
    'project-open',
    'ledger-smb',
    'gedemin',
    'compiere',
    'metasfresh',
    'mediboard',
    'iDempiere',
    'opentaps',
    'tutos',
    'erpnext',
    'ekylibre',
    'projecterp',
    'web-erp',
    'mixerp',
    'qcadoo-mes',
    'xendra',
    'xerpdotnet',
    'libertya',
    'erpstore',
    'drupalerp',
    'jallinone',
    'daflan',
    'easyerpsystem',
    'inoERP',
    'dnet_ebusiness_suite',
    'sereneerp',
    'siipapw-ex',
    'p_d_54761',  # freedom-erp
]

base_data_url = 'https://www.openhub.net/p/{}/analyses/latest/commits_history'
base_page_url = 'https://www.openhub.net/p/{}'

for product in products:
    data_url = base_data_url.format(product)
    r = requests.get(data_url, stream=True, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'})

    if r.status_code != 200:
        print("{}: Status code: {}, body {}".format(data_url, r.status_code, r.content))
        sys.exit(1)

    page_url = base_page_url.format(product)
    req = requests.get(page_url, stream=True, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'})

    if req.status_code != 200:
        print("{}: Status code: {}, body {}".format(page_url, req.status_code, req.content))
        sys.exit(1)

    soup = bs4.BeautifulSoup(req.content, 'html.parser')
    tag_spec = {'href': '/p/{}'.format(product), 'style': 'color: black'}
    tag = soup.find_all('a', tag_spec)
    product_friendly_name = tag[0].contents[0]

    with open('raw/' + product + ".json", 'wb+') as f:
        for chunk in r:
            f.write(chunk)

    print('Scraping {}'.format(product_friendly_name))

    time.sleep(random.randint(2, 5))
