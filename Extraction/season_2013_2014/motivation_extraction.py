# Мотивация рассчитывается по следующей формуле:
# если дерби или  тур > 33 и dist <= 3 - 1 для обеих команд
# иначе если тур > 16
#     если 1 - (dist / 3) / left < 0 или > 1 вернуть 0
#     иначе вернуть 1 - (dist / 3) / left


import useful_functions as uf
import re


TOURS = 39
key_positions = {1, 2, 3, 4, 5, 6, 17, 18}
derbies = {'Арсенал': {'Тоттенхэм Хотспур', 'Челси'},
           'Ливерпуль': {'Эвертон'},
           'Манчестер Юнайтед': {'Манчестер Сити', 'Ливерпуль'},
           'Сандерленд': {'Ньюкасл Юнайтед'}
           }


def get_key_pos_scores(soup):
    res = set()
    for i, team in enumerate(soup):
        if i - 1 in key_positions:
            res.add(int(team.findAll(text=re.compile('[0-9]+'))[-1]))
    return res


def get_motivation(url, driver):
    """Getting motivation for the match"""
    soup = uf.get_soup(url)
    res = []

    #: adding names
    res += uf.get_names(soup)
    teams = res

    #: magic with names and derbies
    for i in {0, 1}:
        if res[i] in derbies and res[1 - i] in derbies[res[i]]:
            res = res + [1, 1]
            return res

    #: season end or start
    tour = uf.get_tour_number(soup)
    if tour > 33:
        res += [1, 1]
        return res
    if tour < 16:
        res += [0, 0]
        return res

    #: moving to statto
    date = uf.get_date(soup)
    statto = uf.get_statto_soup(driver, date)
    statto_all = statto.findAll('form')[1].findAll('tr')
    statto_teams = [uf.championat_statto[x] for x in teams]

    #: getting teams scores and key positions points
    info = uf.get_statto_teams_info(statto_teams[0], statto_teams[1], statto)
    team1_score = uf.get_statto_score(info[0])
    team2_score = uf.get_statto_score(info[1])
    key_pos_scores = get_key_pos_scores(statto_all)

    #: getting min distance to key position for each team
    dist1 = min(list(filter(lambda x: x, [abs(x - team1_score) for x in key_pos_scores])))
    dist2 = min(list(filter(lambda x: x, [abs(x - team2_score) for x in key_pos_scores])))

    #: finally getting res
    left = TOURS - tour
    val = 1 - (dist1 / 3) / left
    if val < 0 or val > 1:
        res.append(0)
    else:
        res.append(val)
    val = 1 - (dist2 / 3) / left
    if val < 0 or val > 1:
        res.append(0)
    else:
        res.append(val)
    return res


def get_all_motivation(path="./extracted_motivation_13_14.txt"):
    """Getting all motivation"""
    with uf.ChromeDriver() as driver, open(path, 'w', encoding='windows-1251') as handle:
        soup = uf.get_soup()
        handle.write("name1\tname2\tmotivation1\tmotivation2\n")
        matches = soup.findAll(attrs={'class': '_res'})
        for cnt, match in enumerate(matches):
            print(cnt + 1)
            trying = 0
            error = False
            while True:
                try:
                    motivation = get_motivation('http://www.championat.com' + match.findAll('a')[0]['href'], driver)
                    break
                except Exception as e:
                    trying += 1
                    print('On try {0} smth went wrong: {1}'.format(trying, e))
                    if trying == 5:
                        print('I give up; shit happens. Check it out!')
                        print(e)
                        error = True
                        break
                    continue
            if error:
                continue
            handle.write('\t'.join(str(e) for e in motivation) + '\n')
            if cnt % 5 == 4:
                handle.flush()
        print("Extraction completed")
        handle.flush()