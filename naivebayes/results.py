import pandas as pd

df = pd.read_csv('results.csv')
#df['correct'] = df.apply(lambda r: r['true_news'] is r['model_results'], axis=1)

total_correct = df['correct'].value_counts()
print(df['correct'].sum())
print(df['correct'].sum() / len(df))


# df.to_csv("results.csv")