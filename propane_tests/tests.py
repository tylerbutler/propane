# coding=utf-8
from unittest import TestCase
from path import path
from propane.datastructures import CaseInsensitiveDict
from propane.filetools import calc_sha
from propane.strings import space_out_camel_case

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

class CaseInsensitiveDictTests(TestCase):
    def setUp(self):
        self.normal_dict = {
            'One': 1,
            'Two': 2
        }
        self.cid = CaseInsensitiveDict(self.normal_dict)

    def access_test(self):
        self.assertEqual(self.cid['one'], self.cid['OnE'])
        self.assertIs(self.cid.get('not_present', None), None)

    def assignment_test(self):
        self.cid['Three'] = 3
        self.assertEqual(self.cid['three'], 3)


class FileToolsTests(TestCase):
    def setUp(self):
        self.file = path(__file__).dirname() / '__init__.py'

    def file_test(self):
        sha = calc_sha(self.file)
        self.assertEqual(sha, 'ch4UW+fLIszntC4GJ6WiqqgGwFlztsVIH/nit7M7P40=')

    def string_test(self):
        s = open(self.file, mode='rb').read()
        sha = calc_sha(s)
        self.assertEqual(sha, 'ch4UW+fLIszntC4GJ6WiqqgGwFlztsVIH/nit7M7P40=')

    def stream_test(self):
        with open(self.file, mode='rb') as f:
            sha = calc_sha(f)
        self.assertEqual(sha, 'ch4UW+fLIszntC4GJ6WiqqgGwFlztsVIH/nit7M7P40=')

class StringsTests(TestCase):
    def test_camel_case(self):
        result = space_out_camel_case('DMLSServicesOtherBSTextLLC')
        self.assertEqual(result, 'DMLS Services Other BS Text LLC')
