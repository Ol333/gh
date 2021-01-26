import rab_with_db as rwd

l = rwd.player_list()
# print(l)
# 66 yukitakahashi
l = rwd.players_kifu_list(66)
print(len(l))
for i in l:
    ind = i.index("手数----指手---------消費時間--")
    print(i[:ind])
    print(i[ind:ind+59])
#Dolphin - Kristallweizen-kai