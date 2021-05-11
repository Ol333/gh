import time
import subprocess

import shogi.KIF

import rab_with_db as rwd
import engine_connection as enc

# l = rwd.player_list()
# print(len(l))

# 66 yukitakahashi
l = rwd.players_kifu_list(66)[0]

kif = shogi.KIF.Parser.parse_str(l)[0]
print(kif['names'][shogi.BLACK])
print(kif['names'][shogi.WHITE])
print(kif['moves']) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
print(kif['win'])

l = l.split('\n')
date = l[1][5:]
conditions = (l[3][5:], l[4][4:])
print(date)
print(conditions)

################################################################################################

eng = enc.Engine("gikou")
f = open('output_{}.txt'.format(str(float('{:.3f}'.format(time.time())))), 'w')

start_time = time.time()
start_pos = ""
for i in range(len(kif['moves'])):
    # найти cp за текущий ход
    cur_res = eng.cp_of_current_move(start_pos,kif['moves'][i])
    f.write(' /// ' + str(cur_res) + '\n')  
    # найти cp за лучший следующий ход
    start_pos += ' ' + kif['moves'][i]
    bst_mov,mov_cp = eng.cp_of_next_move(start_pos)
    f.write(" /// " + str(bst_mov) + ' ' + str(mov_cp) + '\n')
eng.end()
res_time = time.time() - start_time
res_min = str(res_time // 60)
res_sec = str(float('{:.3f}'.format(res_time % 60)))
f.write(res_min + " minutes, " + res_sec + " seconds")
f.close()