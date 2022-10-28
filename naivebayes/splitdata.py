import pandas as pd
import os


# we don't want to split the dataset into training data and testing data
fake_stories = pd.concat([
    pd.read_csv("../data/DataSet_Misinfo_FAKE.csv", usecols=['text']),
    pd.read_csv("../data/EXTRA_RussianPropagandaSubset.csv")]
).sample(frac=1).reset_index()
fake_stories['true_news'] = False
true_stories = pd.read_csv("../data/DataSet_Misinfo_TRUE.csv", usecols=['text'])
true_stories['true_news'] = True

# number of stories
N = 1390
fake_stories = fake_stories[0: N]
true_stories = true_stories[0: N]

print('there are', len(fake_stories), 'fake stories')
print('there are', len(true_stories), 'true stories')



all_data = pd.concat([fake_stories, true_stories], axis=0).sample(frac=1).reset_index()

# shuffle the dataa
training_data = all_data.sample(frac=0.5)
validation_data = all_data.drop(training_data.index)

training_data.to_csv("../data/train.csv")
validation_data.to_csv("../data/test.csv")
