import pandas as pd


#: Godlike total merging
with open('extracted_form_13_14.txt', 'r') as data:
    form = pd.read_table(data, header=0)

with open('extracted_concentration_13_14.txt', 'r') as data:
    concentration = pd.read_table(data, header=0)

with open('extracted_goal_score_diff_13_14.txt', 'r') as data:
    goal_score_diff = pd.read_table(data, header=0)

with open('extracted_history_13_14.txt', 'r') as data:
    history = pd.read_table(data, header=0)

with open('extracted_motivation_13_14.txt', 'r') as data:
    motivation = pd.read_table(data, header=0)

res = pd.merge(form, concentration, on=['name1', 'name2'])
res = pd.merge(res, goal_score_diff, on=['name1', 'name2'])
res = pd.merge(res, history, on=['name1', 'name2', 'result'])
res = pd.merge(res, motivation, on=['name1', 'name2'])

res.to_csv('extracted_13_14.txt', sep='\t', index=False)