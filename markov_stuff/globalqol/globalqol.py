import pandas as pd

df = pd.read_csv('extremepoverty.csv')
df['pov_change'] = df['Number of people living in extreme poverty (OWID based on World Bank (2016) and Bourguignon and Morrisson (2002))'].diff()
df['Year'] = pd.to_datetime(df['Year'], format='%Y')

df = df.set_index('Year')

df.to_csv('test.csv')

print(df)
