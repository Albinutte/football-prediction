# Извлечение фактора "концентрация":
# 1 - 2 * 0.х, где
# х зависит от последнего матча,
# проигранного слабой команде
# (находящейся на 7 или больше позиций ниже);
# последний матч => х = 5, матч назад => х = 4 etc


import re

from selenium import webdriver
from season_2012_2013 import useful_functions as uf


def get_loses(team, soup):
    """Getting list of rivals and date of lost matches"""
    res = []
    matches = soup.findAll(attrs={'class': "match__team__tournirs__i"})
    num = 0
    for i in soup.findAll(attrs={'class': re.compile('(_win)|(_tie)|(_lose)')}):
        num += 1
    for i, cnt in zip(matches, range(len(matches))):
        if i.find(attrs={'class': '_lose'}):
            title = i.find('span')['title']
            round = int(title.split('-')[0].split('.')[-1])
            if round == 1:
                continue
            parts = title.split('.')
            date = '.'.join([parts[0], parts[1], parts[2]])
            teams = title.split('-')[1:]
            teams[0] = teams[0].split('.')[-1][1:-1]
            teams[1] = teams[1].split('(')[0][1:-1]
            if teams[0] == team:
                rival = teams[1]
            else:
                rival = teams[0]

            res.append({'date': date, 'rival': rival,
                        'match': cnt, 'total': num})
    return res


def get_concentration(driver, url):
    """Gets concentration from url"""
    soup = uf.get_soup(url)
    res = []

    #: getting names
    names = uf.get_names(soup)
    res += names

    #: getting list of matches lost recently
    history = []
    for i in soup.findAll(attrs={'class': "match__team__tournirs"}):
        history.append(i)
    loses = []
    for cnt, i in zip(range(len(names)), history):
        loses.append(get_loses(names[cnt], i))

    #: getting last lose to loser
    losers_loses = [0, 0]
    for team, cnt in zip(loses, range(2)):
        for match in team:
            statto = uf.get_statto_soup(driver, match['date'])
            teams = [uf.championat_statto[names[cnt]], uf.championat_statto[match['rival']]]
            statto_info = uf.get_statto_teams_info(teams[0], teams[1], statto)[:2]
            if uf.get_statto_teams_pos_diff(statto_info[0], statto_info[1]) < -7:
                losers_loses[cnt] = 6 - match['total'] + match['match']

    #: getting answer
    coef = [1 - x / 5 for x in losers_loses]
    res += coef
    return res


def get_all_concentration(path="./extracted_concentration.txt"):
    "Getting all concentration"
    driver = webdriver.Chrome()
    handle = open(path, 'w')
    soup = uf.get_soup()
    handle.write("name1\tname2\tconcentration1\tconcentration2\n")
    matches = soup.findAll(attrs={'class': '_res'})
    print("Starting extracting concentraion")

    for cnt, match in enumerate(matches):
        print(cnt + 1)
        trying = 0
        error = False
        while True:
            try:
                goal_pos_diff = get_concentration(driver, 'http://www.championat.com' + match['href'])
                break
            except Exception as e:
                trying += 1
                print('On try {0} smth went wrong: {1}'.format(trying, e))
                if trying == 5:
                    # winsound.Beep(2000, 2000)
                    print('Oh, well:\n\t', 'http://www.championat.com' + match['href'])
                    error = True
                    break
                continue
        if error:
            continue
        handle.write('\t'.join(str(e) for e in goal_pos_diff) + '\n')
        if cnt % 5 == 4:
            handle.flush()

    print("Extraction completed")
    handle.flush()
    handle.close()
    driver.close()


def test(url):
    """Testing on particular match"""
    driver = webdriver.Chrome()
    print(get_concentration(driver, url))
    driver.close()


get_all_concentration()