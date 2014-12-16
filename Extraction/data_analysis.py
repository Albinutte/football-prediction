import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


train = pd.read_table('full_extracted.txt', encoding='windows-1251')
y_train = np.array(train['result'])
x_train = train.drop(['result', 'name1', 'name2'], axis=1)

#: form_dif dependence
y_good = [form1 - form2 for form1, form2, res in zip(train['form1'], train['form2'], train['result']) if res == 1]
form_dif = train['form1'] - train['form2']
y_all = [1 / list(form_dif).count(form) for form in y_good]
#plt.hist(y_good, weights=y_all, color='green')
#plt.show()

#: goal_dif dependence
#plt.plot(train['goal_diff'], train['result'], 'o')
#plt.show()

#: score_dif dependenct
plt.plot(train['score_diff'], train['result'], 'o')
plt.show()