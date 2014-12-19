# История = (р1 + р2) / 4, где
# р1 и р2 итоги последних двух матчей:
#    0 - проигрыш
#    1 - ничья
#    2 - победа


import useful_functions as uf
import re


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


def get_all_history(path="./extracted_history_13_14.txt"):
    """Extracting all history to file"""
    with open(path, 'w', encoding='windows-1251') as handle:
        soup = uf.get_soup()
        print("Starting extracting history")
        handle.write('name1\tname2\thistory\tresult\n')
        matches = soup.findAll(attrs={'class': '_res'})
        for cnt, match in enumerate(matches):
            ref = 'http://www.championat.com' + match.findAll('a')[0]['href']
            print(cnt + 1)
            history = get_history(ref)
            if history is not None:
                handle.write('\t'.join(str(e) for e in history) + '\n')
            if cnt % 5 == 0:
                handle.flush()
        print("History extracting finished")