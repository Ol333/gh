import rab_with_db as rwd
import shogi.KIF

l = rwd.player_list()
# print(l)
# 66 yukitakahashi
l = rwd.players_kifu_list(66)
print(len(l))
for i in l:
    kif = shogi.KIF.Parser.parse_str(i)[0]
    print(kif['names'][shogi.BLACK])
    print(kif['names'][shogi.WHITE])
    print(kif['moves']) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    print(kif['win'])

    break

