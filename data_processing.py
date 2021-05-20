import sys
import time
import subprocess
import datetime

import shogi.KIF

import rab_with_db as rwd
import engine_connection as enc

if __name__ == "__main__":
    run_counter = sys.argv[1:]
    #print(run_counter)
    pl_list = rwd.player_list()
    print(len(pl_list))

    for i_player in range(run_counter,run_counter+1): #запускаем по одному человеку за запуск
        # 66 yukitakahashi
        pl_kif_list = rwd.players_kifu_list(pl_list[i_player])
        for i_kif in pl_kif_list:
    ##        l = rwd.players_kifu_list(66)[0]
            l = pl_kif_list[i_kif]

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
            ##date = datetime.datetime.strptime(date,"%Y/%m/%d")

            eng = enc.Engine("gikou")
            f = open('output_{0}_{1}.txt'.format(pl_list[i_player],i_kif), 'w')

            start_time = time.time()
            start_pos = ""
            for i in range(len(kif['moves'])):
                # найти cp за текущий ход
                cur_res = eng.cp_of_current_move(start_pos,kif['moves'][i])
                f.write(' /// ' + str(cur_res) + '\n') #вывести в бд
                # найти cp за лучший следующий ход
                start_pos += ' ' + kif['moves'][i]
                bst_mov,mov_cp = eng.cp_of_next_move(start_pos)
                f.write(" /// " + str(bst_mov) + ' ' + str(mov_cp) + '\n') #вывести в бд
            eng.end()
            res_time = time.time() - start_time
            res_min = str(res_time // 60)
            res_sec = str(float('{:.3f}'.format(res_time % 60)))
            f.write(res_min + " minutes, " + res_sec + " seconds")
            f.close()


# в процессе изменяется .db
