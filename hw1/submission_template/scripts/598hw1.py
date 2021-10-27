

# Congming Liao 260790998 

import pandas as pd
import re

# DATA_Collection
rawdata = pd.read_csv('data/IRAhandle_tweets_1.csv', header = 0, converters = {'id': str}, usecols = ['tweet_id', 'publish_date', 'content', 'language'], nrows = 10000)

# Task 1: keep tweets that are in English
df = rawdata[rawdata['language'] == 'English']
# Task 2: keep tweets that don’t contain a question 
df = df[df['content'].str.contains('\?') == False]


# DATA ANNOTATION
# delete the language col because we do not need it anymore
df.drop('language', axis=1, inplace=True)

# Task 1: add feature "trump_mention" 
trump_mention = []
for tweet in df['content']:
    if bool(re.search("[^a-zA-Z]Trump[^a-zA-Z]", tweet)):
        trump_mention.append(True)
    else:
        trump_mention.append(False)
df['trump_mention'] = trump_mention

# Task 2: Rearrange the order of the cols and save
df= df[['tweet_id','publish_date','content','trump_mention']]
df.to_csv('dataset.tsv', sep = '\t', index = False)


# ## ANALYSIS ##

frac = 0.0
# calculate the fraction
count = 0
for e in df['trump_mention']:
    if e:
        count = count+ 1;
frac = count / len(df.index)

data = {'result': ['frac-trump-mentions'], 'value': [round(frac,3)]}  
resultDF = pd.DataFrame(data)
resultDF.to_csv('results.tsv', sep = '\t', index = False)
print(round(frac,3))


