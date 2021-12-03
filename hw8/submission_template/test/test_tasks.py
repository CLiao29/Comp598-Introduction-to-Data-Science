import unittest
from pathlib import Path
import os, sys
import json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
from src.compile_word_counts import word_count
from src.compute_pony_lang import tf_idf

class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        print("\n")

    def test_task1(self):
        print("RUNNING TEST FOR TASK 1")
        with open (self.true_word_counts) as f:
            truth_dict = json.load(f)
        test_dict = word_count(self.mock_dialog)
        self.assertEqual(test_dict,truth_dict)
        print("OK")

    def test_task2(self):
        print("RUNNING TEST FOR TASK 2")
        with open (self.true_tf_idfs) as f1:
            truth_dict = json.load(f1)
        f1.close()
        with open (self.true_word_counts) as f2:
            word_count = json.load(f2)
        f2.close()

        # build up test dict by calculating tf-idf
        test_dict = {"twilight sparkle": {},
            "applejack": {},
            "rarity": {},
            "pinkie pie": {},
            "rainbow dash": {},
            "fluttershy": {}}
        for pony,pony_words in word_count.items():
            for word,count in pony_words.items():
                test_dict[pony][word] = round(tf_idf(word,pony,word_count),2)
        self.assertEqual(test_dict,truth_dict)
        print("OK")
        
    
if __name__ == '__main__':
    unittest.main()