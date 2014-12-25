import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


train = pd.read_table('../Extraction/full_extracted.txt', encoding='windows-1251')
y_train = np.array(train['result'])
x_train = train.drop(['result', 'name1', 'name2'], axis=1)

#: form_dif dependence
y_good = [form1 - form2 for form1, form2, res in zip(train['form1'], train['form2'], train['result']) if res == 1]
form_dif = train['form1'] - train['form2']
y_all = [1 / list(form_dif).count(form) for form in y_good]
plt.figure('Form hist')
plt.hist(y_good, weights=y_all, color='green')
plt.xlabel('Form difference')
plt.ylabel('Win rate')
plt.savefig('form_dependence.png')


#: goal_dif dependence
matches_won = len([x for x in train['result'] if x == 1])
res = []
for cnt, row in enumerate(train.values):
    dif = row[7]
    res.append(sum([x / matches_won for x, y in zip(train['result'], train['goal_diff']) if x == 1 and y < dif]))
plt.figure('Goal diff plot')
plt.plot(train['goal_diff'], res, '.')
plt.xlabel('Goal diff')
plt.ylabel('Win rate')
plt.savefig('goal_dif_dependence.png')


#: score_dif dependence
res = []
for cnt, row in enumerate(train.values):
    dif = row[8]
    res.append(sum([x / matches_won for x, y in zip(train['result'], train['score_diff']) if x == 1 and y < dif]))
plt.figure('Score diff plot')
plt.plot(train['score_diff'], res, '.')
plt.xlabel('Score diff')
plt.ylabel('Win rate')
plt.savefig('score_dif_dependence.png')