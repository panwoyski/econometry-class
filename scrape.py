import requests
import sys
import random
import time

products = [
    'odoo',
    'openbravo',
    'openconcerto',
    'postbooks',
    'jfire',
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
    'p_d_54761', #freedom-erp
]

base_url = 'https://www.openhub.net/p/{}/analyses/latest/commits_history'

for product in products:
    url = base_url.format(product)
    # print(url)
    r = requests.get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'})
    if r.status_code != 200:
        print("{}: Status code: {}, body {}".format(url, r.status_code, r.content))
        sys.exit(1)

    with open('raw/' + product + ".json", 'w+') as f:
        for chunk in r:
            f.write(chunk)

    print('Writing {}'.format(product))

    time.sleep(random.randint(2, 5))
