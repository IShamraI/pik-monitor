#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import pickle
import datetime
import urllib2
import optparse

reload(sys)  
sys.setdefaultencoding('utf-8')
block = [381154, 399695, 399728, 399718, 399740, 399632, 399599, 399576, 399609, 399714, 399693, 380971, 381155, 381208, 399629, 399684, 399572, 399719, 381083, 381003, 381079, 381264, 381057, 381150, 380978, 381210, 399631, 399575, 399680, 399613, 399589, 381220, 380896, 380897, 399545, 381034]
# url='https://api.pik.ru/v2/flat?block_id=2&bulk_id=4101,3966&price_from=&price_to=&floor_from=&floor_to=&area_from=&area_to=&rooms=3,2&penthouse=&settlement=&finish=0&settlement_fact=&initial_payment=&monthly_payment=&page=0&order=&price_million=0&index_by=statistics&images=1&metadata=1&layouts=1&type=1,2'
url='https://api.pik.ru/v2/flat?block_id=2&bulk_id=4101,3966&price_from=2145634&price_to=4861909&floor_from=&floor_to=&area_from=&area_to=&rooms=3,2&penthouse=&settlement=&finish=1&settlement_fact=&initial_payment=&monthly_payment=&page=0&order=price&price_million=0&index_by=statistics&images=1&metadata=1&layouts=1&type=1,2'
class Flat(object):
    prices = []
    def __init__(self, raw_flat):
        self.id = raw_flat['id']
        self.guid = raw_flat['guid']
        self.status = raw_flat['status']
        self.floor = raw_flat['floor']
        self.section = raw_flat['section']['number']
        self.rooms = raw_flat['rooms']
        self.price = raw_flat['price']
        self.min_price = raw_flat['price']
        self.max_price = raw_flat['price']
        self.prices.append(self.price)
        self.discount = raw_flat['discount']
        self.area = raw_flat['area']
        self.area_price = int(self.price/self.area)
        self.number_on_floor = raw_flat['section']['number']
        self.building = raw_flat['bulk']['name'].encode('utf8')
        self.img = raw_flat['layout']['flat_plan_png']

    def update(self, new_data):
        price = new_data['price']
        if price != self.prices[-1]:
            old = self.price
            self.prices.append(price)
            self.price = price
            self.area_price = int(self.price/self.area)
            if self.min_price > price:
                self.min_price = price
            if self.max_price < price:
                self.max_price = price
            print "{0} - Обновлено( {1} --> {2})".format(self.__str__(), old, self.price)

    def __eq__(self, other):
        return self.price == other.price
    
    def __lt__(self, other):
        return self.price < other.price

    def __str__(self):
        return "Квартира({0:^7})[{10}] - {2}:{12}(Этаж: {1:>2}; Комнат: {7}; Площадь: {5:<4}) Цена: {3} (Мин: {8}; Макс {9}; Кв.м.: {6})\n\tlink: https://www.pik.ru/obninsk/moskovsky_kvartal/flats/{10};\n\timg: {11}".format(
            self.status, self.floor, self.building, self.price, self.discount, self.area, self.area_price, self.rooms, self.min_price, self.max_price, self.id, self.img, self.section
        )

def dump(data):
    with open('.cache', 'wb') as cache:
        pickle.dump(data, cache)

def load():
    try:
        with open('.cache', 'rb') as cache:
            return pickle.loads(cache)
    except:
        return {}

def main():

    # """
    # Main __doc__
    # """

    # print __doc__

    # date = datetime.datetime.now()
    # env_data = dict(
    #     user=os.environ['USER'],
    #     port=os.environ.get('S_REG_PORT_NO', '1000').replace('000',''),
    #     date=date.strftime("%Y-%m-%d"),
    #     path=os.path.dirname(os.path.abspath(__file__)))

    # options = optparse.OptionParser(usage='%prog [options]', description='HTML e-mails sender')
    # options.add_option('-c', '--config', type='str',
    #     default=os.path.join(env_data["path"], "postman.yaml"), help='Config file')
    # options.add_option('-o', '--outgoing', type='str',
    #     default=os.path.join(env_data["path"], "outgoing"), help='Folder with outgoing messages')
    # options.add_option('-s', '--subject', type='str', default=None, help='Set custom subject')
    # options.add_option('-t', '--test', action="store_true", default=False, help='Test mode')
    # options.add_option('-d', '--debug', action="store_true", default=False, help='Debug mode')
    # options.add_option('-a', '--clean_attachments', action="store_false", default=True, help='')

    # opts, args = options.parse_args()

    flats = load()

    request = urllib2.Request(url)
    try:
        json_result = urllib2.urlopen(request).read()
    except urllib2.HTTPError as e:
        error_message = e.read()
        print "HTTP Error"
        # print error_message.strip()
    except urllib2.URLError as e:
        error_message = e.reason
        print "URL Error"
        # print str(error_message).strip()
    result = json.loads(json_result)
    for flat in result['flats']:
        if flat['bulk']['settlement_year'] != 2020: continue
        _id = flat['id']
        if _id in block:
            try:
                del flats[_id]
            except:
                pass
            continue
        if _id not in flats:
            flats[_id] = Flat(flat)
        else:
            flats[_id].update(flat)
    
    # flats.sort(key=lambda x: x.price)
    dump(flats)
    _flats = flats.values()
    _flats.sort(key=lambda x: x.area_price)
    # print flats
    for i, _flat in enumerate(_flats):
        print '{0:>2}'.format(i+1), _flat

if __name__ == '__main__':
    sys.exit(main())
