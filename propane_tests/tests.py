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
        self.text_file = path(__file__).dirname() / 'data/sample_file.txt'
        self.pdf_file = path(__file__).dirname() / 'data/pdf.pdf'

    def file_test(self):
        sha = calc_sha(self.text_file)
        self.assertEqual(sha, 'vT1r++RPA38dW9pHoJR9jJX8SEW4I+XM69Ro2iio8W8=')

        sha = calc_sha(self.pdf_file)
        self.assertEqual(sha, 'FsSFkVFwNY2F1TYH5t75fgRV7cUgNuZTCjjdHl93+qY=')

    def string_test(self):
        s = open(self.text_file, mode='rb').read()
        sha = calc_sha(s)
        self.assertEqual(sha, 'vT1r++RPA38dW9pHoJR9jJX8SEW4I+XM69Ro2iio8W8=')

        s = open(self.pdf_file, mode='rb').read()
        sha = calc_sha(s)
        self.assertEqual(sha, 'FsSFkVFwNY2F1TYH5t75fgRV7cUgNuZTCjjdHl93+qY=')

    def stream_test(self):
        with open(self.text_file, mode='rb') as f:
            sha = calc_sha(f)
        self.assertEqual(sha, 'vT1r++RPA38dW9pHoJR9jJX8SEW4I+XM69Ro2iio8W8=')

        with open(self.pdf_file, mode='rb') as f:
            sha = calc_sha(f)
        self.assertEqual(sha, 'FsSFkVFwNY2F1TYH5t75fgRV7cUgNuZTCjjdHl93+qY=')


class StringsTests(TestCase):
    def test_camel_case(self):
        result = space_out_camel_case('DMLSServicesOtherBSTextLLC')
        self.assertEqual(result, 'DMLS Services Other BS Text LLC')
