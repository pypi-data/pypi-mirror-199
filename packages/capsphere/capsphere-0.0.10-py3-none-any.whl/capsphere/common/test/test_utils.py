import unittest
import json
from capsphere.common.utils import get_file_format, read_config
from capsphere.common.test.resources.data import FILE_NAME_1, FILE_NAME_2, FILE_NAME_3


class TestUtils(unittest.TestCase):

    banks = ["AmBank", "CIMB", "Maybank",
             "Maybank Islamic", "Alliance", "Hong Leong",
             "RHB", "RHB Islamic", "Public Bank"]

    def test_valid_file_split(self):
        pdf_file = get_file_format(FILE_NAME_1)
        img_file = get_file_format(FILE_NAME_2)
        self.assertEqual(pdf_file, 'pdf')
        self.assertEqual(img_file, 'img')

    def test_invalid_file_split(self):
        with self.assertRaises(ValueError) as cm:
            get_file_format(FILE_NAME_3)
        self.assertEqual("Unrecognised filename format 'invalid.file.extension': "
                         "Unable to split strings",
                         str(cm.exception))

    # def test_read_config(self):
    #     data = read_config()
    #     with open('./resources/test_schema.json') as f:
    #         test_data = json.load(f)
    #         self.assertEqual(data, test_data)




