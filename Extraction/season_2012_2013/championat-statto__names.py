from season_2012_2013 import useful_functions as uf


champ = uf.get_soup("http://www.championat.com/football/_england/548/table/all.html")
champ = champ.find(attrs={'class': 'sport__tables'})
champ = champ.findAll('a')
res_champ = []
for i in range(0, len(champ), 7):
    res_champ.append(champ[i].text)

statto = uf.get_soup("http://www.statto.com/football/stats/england/premier-league/2012-2013/table")
statto = statto.findAll(attrs={'class': 'team'})[1:]
res_statto = []
for i in statto:
    res_statto.append(i.text)

res = {}
for i in range(len(res_champ)):
    res[res_champ[i]] = res_statto[i]
print(res)