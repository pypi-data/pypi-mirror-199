import unittest
import pprint
from src.analyser_hj3415.db import chk_db
from src.analyser_hj3415.db import mongo

addr = "mongodb://192.168.0.173:27017"
client = mongo.connect_mongo(addr)


class ChkDBTest(unittest.TestCase):
    def test_chk_integrity_cxxx_invalid(self):
        # 없는 종목
        print(chk_db.chk_integrity_corps(client, '000000'))

    def test_chk_integrity_cxxx(self):
        print(chk_db.chk_integrity_corps(client, '005930'))

    def test_chk_integrity_cxxx_all(self):
        print(chk_db.chk_integrity_corps(client, 'all'))

    def test_sync_mongo_with_krx(self):
        chk_db.sync_mongo_with_krx(client)

    def test_make_parts(self):
        pprint.pprint(chk_db.make_parts(client, 20))