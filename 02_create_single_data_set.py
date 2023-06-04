import pandas as pd
import glob
from datetime import datetime

# load csvs
path = r'path\to\data'
all_files = glob.glob(path + "/*.csv")

# create dfs and concat
list = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    list.append(df)

frame = pd.concat(list, axis=0, ignore_index=True)

# remove duplicates
frame = frame.drop_duplicates(subset='url')

# delete unwanted columns
frame = frame.drop(frame.columns[[0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]], axis=1)

# date variable
datex = frame['date'].to_list()
datey = [s.replace('.', '') for s in datex]

date_new = [datetime.strptime(x, '%d%m%y') for x in datey]

date_final = [x.strftime('%Y-%m-%d') for x in date_new]

# add new date variales to to dataframe
frame['new_date'] = date_final
frame = frame.drop(['date'], axis=1)
frame = frame.rename(columns={'new_date': 'date'})
frame = frame[['date', 'title', 'url', 'text']]

# sort by date
frame = frame.sort_values(by='date')

# store in csv
frame.to_csv('jf_full_raw.csv')
