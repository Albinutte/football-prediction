import pandas as pd


with open('./season_2012_2013/extracted.txt', 'r') as data:
    extracted = pd.read_table(data)

with open('./season_2013_2014/extracted_13_14.txt', 'r') as data:
    extracted_13_14 = pd.read_table(data)

full_extracted = pd.concat([extracted, extracted_13_14])
full_extracted.to_csv('full_extracted.txt', sep='\t', index=False)