import unittest
import bqhus
from dotenv import load_dotenv

load_dotenv()


class TestSelect(unittest.TestCase):
    def test_select_with_no_params(self):
        query = "SELECT 1"
        task = bqhus.select(query)
        self.assertEqual(query, task.query)

    def test_select(self):
        query = "SELECT word FROM `bigquery-public-data.samples.shakespeare` order by rand() limit 5"
        words = bqhus.select(query).as_dicts()
        self.assertEqual(len(words), 5)


if __name__ == "__main__":
    unittest.main()
