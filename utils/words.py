import json
import os


# http://www.psychpage.com/learning/library/assess/feelings.html
def load_words():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'words.json')) as f:
        json_words = json.load(f)
        return json_words
