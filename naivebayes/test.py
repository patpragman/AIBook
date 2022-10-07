import pickle
import pandas as pd
from train import Word



with open("model.p", "rb") as model_file:
    words = pickle.load(model_file)


def categorize(text) -> bool:

    # P(True News | words_in_paper) = P(True News) * * * ....
    p_true_given_word = (words['TRUE_PAPERS'] / words['TOTAL_PAPERS'])
    # P(False News | words_in_paper) = P(False News) * * * ....
    p_false_given_word = (words['FALSE_PAPERS'] / words['TOTAL_PAPERS'])

    if not isinstance(text, str):
        return False

    for raw_word in text.split():
        word = Word(raw_word, True)

        if word in words:
            p_true_given_word *= words[word].p_word_given_true
            p_false_given_word *= words[word].p_word_given_false

    if p_true_given_word >= p_false_given_word:
        return True
    else:
        return False


testing_data = pd.read_csv("../data/test.csv")

testing_data['model_results'] = testing_data.apply(lambda r: categorize(r['text']), axis=1)

testing_data.to_csv("results.csv", index=False)