import pandas as pd
import pickle
import re
from pprint import pprint
train = pd.read_csv('../data/train.csv')




class Word:

    def __init__(self, raw_string, veracity):
        self.string = self._clean(raw_string)
        self.paper_counter = 1
        self.true_papers = int(veracity)
        self.false_papers = int(not veracity)

        self.p_word_given_true = None
        self.p_word_given_false = None


    def _clean(self, raw_word_string):
        word = raw_word_string
        remove_characters = ['%', "$", "€", ":", "!", ".", ",", "`", "?", "#", "@", "*", "”"]

        for c in word:
            if c in remove_characters:
                word = word.replace(c, " ")
                word = word.strip()

        return word.upper()

    def __eq__(self, other):
        return self.string == other.string

    def __hash__(self):
        return hash(self.string)

words = {

}
TOTAL_PAPERS = 0
FALSE_PAPERS = 0
TRUE_PAPERS = 0
for i, row in train.iterrows():

    if not isinstance(row['text'], str):
        continue

    raw_text = row['text'].split()
    veracity = row['true_news']

    TOTAL_PAPERS += 1
    if veracity:
        TRUE_PAPERS += 1
    else:
        FALSE_PAPERS += 1

    for raw_word in raw_text:
        word = Word(raw_word, veracity)
        if word in words:
            words[word].paper_counter += 1
            words[word].true_papers += int(veracity)
            words[word].false_papers += int(not veracity)
        else:
            words[word] = word



for word in words.values():
    word.p_word_given_true = word.true_papers / TRUE_PAPERS
    word.p_word_given_false = word.false_papers / FALSE_PAPERS


words['TOTAL_PAPERS'] = TOTAL_PAPERS
words['FALSE_PAPERS'] = FALSE_PAPERS
words['TRUE_PAPERS'] = TRUE_PAPERS

with open('model.p', "wb") as model_file:
    pickle.dump(words, model_file)
