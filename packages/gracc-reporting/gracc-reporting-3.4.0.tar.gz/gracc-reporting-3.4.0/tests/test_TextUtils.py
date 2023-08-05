import unittest
import pandas as pd
from io import StringIO

import gracc_reporting.TextUtils as TextUtils


class TestTextUtils(unittest.TestCase):

    def setUp(self):
        self.header = ["first", "second", "third", "forth", "with,comma"]
        self.text_utils = TextUtils.TextUtils(self.header)
        self.example_data = {"first": ['c1r1', 'c1r2'],
                             "second": ['c2r1', 'c2r2'], 
                             "forth": [10, 42], 
                             "third": ['c3r1', 'c3r2'],
                             "with,comma": ['c4r1', 'c4,r2']}

    def test_table_text(self):
        text = self.text_utils.printAsTextTable("text", self.example_data)
        print(text)

    def test_table_html(self):
        text = self.text_utils.printAsTextTable("html", self.example_data)
        print(text)

    def test_table_csv(self):
        text = self.text_utils.printAsTextTable("csv", self.example_data)
        # Read in the data back to pandas dataframe
        df = pd.read_csv(StringIO(text))
        self.assertListEqual(self.header, list(df.columns))
        print(text)



