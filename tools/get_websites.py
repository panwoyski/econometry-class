import requests
import bs4
import sys
import time
import random


projects = [
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
agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'

base_data_url = "https://www.openhub.net/p/{}"

for project in projects:
    print('Finding homepage for {}...'.format(project))
    data_url = base_data_url.format(project)

    r = requests.get(data_url, stream=True, headers={'User-Agent': agent})

    if r.status_code != 200:
        print("{}: Status code: {}, body {}".format(data_url, r.status_code, r.content))
        sys.exit(1)

    soup = bs4.BeautifulSoup(r.content, 'html.parser')
    tag_spec = {'itemprop': 'url'}

    def predicate(tag):
        matching = True
        matching &= tag.name == 'a'
        matching &= 'href' in tag.attrs.keys()
        matching &= ('itemprop', 'url') in tag.attrs.items()
        import re
        matching &= bool(re.compile('Homepage').search(tag.text))
        return matching

    tag = soup.find_all(predicate)
    href = ''
    if not len(tag):
        print('Pagename not found')
        continue
    elif len(tag) > 2:
        print('Multiple matching tags: {}'.format(tag))
    else:
        href = tag[0].attrs['href']
        print(href)

    with open('websites_full.csv', 'a') as fd:
        fd.write('{},"https://www.openhub.net/p/{}","{}"\n'.format(project, project, href))

    time.sleep(random.randint(2, 5))
