import sys
import time

import shogi.KIF

import rab_with_db as rwd
import engine_connection as ec

if __name__ == "__main__":
    run_counter = int(sys.argv[1])
    print(run_counter, type(run_counter))
    pl_list = rwd.player_list() # зачем?..
    # print(len(pl_list))

    for i_player in range(run_counter,run_counter+1): #запускаем по одному человеку за запуск
        # 66 yukitakahashi
        pl_kif_list = rwd.players_kifu_list(i_player)
        for i_kif in range(1): #pl_kif_list:
        # l = rwd.players_kifu_list(66)[0]
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
            
            for j in range(10): # for j in range(10,20)
                eng = ec.Engine("YaneuraOu_NNUE-tournament-clang++-avx2")
                f = open('Y_output_{0}_{1}_{2}.txt'.format(pl_list[i_player],i_kif,j), 'w')

                start_time = time.time()
                start_pos = ""
                for i in range(len(kif['moves'])):
                    # найти cp за лучший рекомендуемый следующий ход
                    temp_because_yaneoura_besit = eng.cp_of_next_move(start_pos, depth=5)
                    if temp_because_yaneoura_besit[1] == -111111111:
                        bst_mov = temp_because_yaneoura_besit[0]
                        mov_cp = eng.cp_of_current_move(start_pos, bst_mov, depth=5)
                    else:
                        bst_mov,mov_cp = temp_because_yaneoura_besit
                    f.write(" /// " + str(bst_mov) + ' ' + str(mov_cp) + '\n') #вывести в бд
                    # найти cp за текущий ход
                    cur_res = eng.cp_of_current_move(start_pos, kif['moves'][i], depth=5)
                    f.write(' '+ kif['moves'][i] + ' /// ' + str(cur_res) + '\n') #вывести в бд
                    start_pos += ' ' + kif['moves'][i]
                eng.end()
                res_time = time.time() - start_time
                res_min = str(res_time // 60)
                res_sec = str(float('{:.3f}'.format(res_time % 60)))
                f.write(res_min + " minutes, " + res_sec + " seconds")
                f.close()


# в процессе изменяется .db