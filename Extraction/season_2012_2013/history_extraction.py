# История = (р1 + р2) / 4, где
# р1 и р2 итоги последних двух матчей:
#    0 - проигрыш
#    1 - ничья
#    2 - победа


import re

from season_2012_2013 import useful_functions as uf


def get_winner(logo, soup):
    """Getting winner by logo and soup(match)"""
    team = soup.find(attrs={'class': '_right _top'}).find('img')['src']
    score = soup.find(attrs={'class': '_center _nowrap'}).find('a').text
    score = re.findall(r'\d+', score)
    if logo == team and \
        score[0] > score[1] or \
            logo != team and score[0] < score[1]:
                return 2
    elif score[0] == score[1]:
        return 1
    else:
        return 0


def get_history(url):
    """Getting history from url"""
    soup = uf.get_soup(url)

    # : adding names
    res = []
    for i in soup.findAll(attrs={'class': 'match__team__name'}):
        res.append(i.text)

    # : getting history
    logo = soup.find(attrs={'class': re.compile('match__timeline__team__icon')})['src']
    soup2 = soup.find(attrs={'class': 'table match__history__table'})
    if soup2 is None:
        return None
    soup2 = soup2.findAll('tr', limit=2)
    h = 0
    for i in soup2:
        h += get_winner(logo, i)
    h /= 4
    res.append(h)

    #: adding result
    res += uf.get_results(soup)

    return res


def get_all_history(path="./extracted_history.txt"):
    """Extracting all history to file"""
    handle = open(path, 'w')
    soup = uf.get_soup()
    cnt = 0
    print("Starting extracting history")
    handle.write('name1\tname2\thistory\tresult\n')
    for i in soup.findAll(attrs={'class': 'norm'}):
        cnt += 1
        print(cnt)
        form = get_history('http://www.championat.com' + i['href'])
        if form is not None:
            handle.write('\t'.join(str(e) for e in form) + '\n')
        if cnt % 5 == 0:
            handle.flush()
    print("History extracting finished")
    handle.flush()
    handle.close()