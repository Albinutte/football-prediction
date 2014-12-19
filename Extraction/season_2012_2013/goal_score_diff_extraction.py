# Формулы:
#     для разницы мячей:
#         0.5 + раз_мяч / (2 * макс_раз_мяч),
#         где раз_мяч - разница мячей,
#         макс_раз_мяч - разница мячей лидера
#         ПО ЭТОМУ, БЛИН, ПОКАЗАТЕЛЮ
#         и последнего;
#     для разницы очков:
#         0.5 + раз_оч / (2 * макс_раз_оч),
#         где раз_оч - разница очков,
#         макс_раз_оч - разница очков первого и
#         последнего


import re
import useful_functions as uf


def get_values(soup):
    """Getting goal dif and score from tiny soup"""
    texts = soup.findAll(text=re.compile('[0-9]+'))
    res = texts[-2:]
    for cnt, num in enumerate(res):
        res[cnt] = int(num)
    return res


def get_goal_pos_diff(driver, url):
    """Getting score and difference"""
    res = []
    soup = uf.get_soup(url)

    #: getting match date and team names
    date = uf.get_date(soup)
    teams = uf.get_names(soup)
    res += teams

    #: moving to statto url
    statto = uf.get_statto_soup(driver, date)
    statto_teams = [uf.championat_statto[x] for x in teams]

    #: getting teams goal_diff and score_diff
    values = [0, 0]
    values[0], values[1], first, last, first_goals, last_goals = \
        uf.get_statto_teams_info(statto_teams[0], statto_teams[1], statto)

    #: getting actual numbers from string values
    for i in range(len(values)):
        values[i] = get_values(values[i])
    first = get_values(first)
    last = get_values(last)
    first_goals = get_values(first_goals)
    last_goals = get_values(last_goals)

    #: counting result
    goal_diff = 0.5 + (values[0][0] - values[1][0]) / (2 * (first_goals[0] - last_goals[0]))
    pos_diff = 0.5 + (values[0][1] - values[1][1]) / (2 * (first[1] - last[1]))

    res += [goal_diff, pos_diff]
    return res


def get_all_goal_pos_diff(path="./extracted_goal_score_diff.txt"):
    "Getting all goal and pos diff"
    with uf.ChromeDriver() as driver, open(path, 'w') as handle:
        soup = uf.get_soup()
        handle.write("name1\tname2\tgoal_diff\tscore_diff\n")
        matches = soup.findAll(attrs={'class': '_res'})
        print("Starting extracting goal and score diffs")

        for cnt, match in enumerate(matches):
            print(cnt + 1)
            trying = 0
            error = False
            while True:
                try:
                    goal_pos_diff = get_goal_pos_diff(driver, 'http://www.championat.com' + match.findAll('a')[0]['href'])
                    break
                except Exception as e:
                    trying += 1
                    print('On try {0} smth went wrong: {1}'.format(trying, e))
                    if trying == 5:
                        print('I give up; date is probably too early')
                        error = True
                        break
                    continue
            if error:
                continue
            handle.write('\t'.join(str(e) for e in goal_pos_diff) + '\n')
            if cnt % 5 == 4:
                handle.flush()

        print("Extraction completed")