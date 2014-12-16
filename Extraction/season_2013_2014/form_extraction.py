# Форма рассчитывается по формуле
# sum / 10, где
# sum - сумма очков за матч:
#    2 за победу
#    1 за ничью
#    0 за поражение

import re
from season_2013_2014 import useful_functions as uf


def get_form(url):
    """Gets teams and their forms from url"""
    soup = uf.get_soup(url)
    res = []

    #: adding names
    res += uf.get_names(soup)

    # : counting form
    history = []
    for i in soup.findAll(attrs={'class': re.compile('(_win)|(_tie)|(_lose)')}):
        history.append(i['class'])
    if len(history) < 10:
        return None
    elif len(history) < 12:
        start1 = 0
        start2 = 5
    else:
        start1 = 1
        start2 = 7
    form1 = 0
    form2 = 0
    for i in range(start1, start1 + 5):
        if history[i] == ['_win']:
            form1 += 2
        elif history[i] == ['_tie']:
            form1 += 1
    for i in range(start2, start2 + 5):
        if history[i] == ['_win']:
            form2 += 2
        elif history[i] == ['_tie']:
            form2 += 1
    form1 /= 10
    form2 /= 10
    res = res + [form1] + [form2]

    #: adding result
    res += uf.get_results(soup)

    return res


def get_all_forms(path="./extracted_form_13_14.txt"):
    """Extracting all form to file"""
    with open(path, "w", encoding='windows-1251') as handle:
        soup = uf.get_soup()
        cnt = 0
        print("Starting extracting forms")
        handle.write('name1\tname2\tform1\tform2\tresult\n')
        for i in soup.findAll(attrs={'class': '_res'}):
            cnt += 1
            print(cnt)
            form = get_form('http://www.championat.com' + i.findAll('a')[0]['href'])
            if form is not None:
                handle.write('\t'.join(str(e) for e in form) + '\n')
            if cnt % 5 == 0:
                handle.flush()
        print("Forms extraction finished")