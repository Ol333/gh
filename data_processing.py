import sys
import math
import numpy as np
import shogi.KIF

import rab_with_db as rwd
import engine_connection as ec

if __name__ == "__main__":
    run_counter = int(sys.argv[1])
    # run_counter = 12
    db10 = rwd.DbConnection("shogi_db10000.db")
    db40 = rwd.DbConnection("shogi_db40000.db")
    dblm = rwd.DbConnection("shogi_dblocM.db")
    kf_list = db10.table_list("Kifu")

    for i_kifu in range(run_counter,run_counter+5000):
    # for i_kifu in range(run_counter,run_counter+2):
        print('запуск ',i_kifu,' кифу!')
        try:
            kif = shogi.KIF.Parser.parse_str(kf_list[i_kifu][1])[0]
        except Exception as ex:
            f = open('wrong_kifu.txt', 'a')
            f.write(str(i_kifu) + '\n') #вывести в файл номер неправильного кифу
            f.close()
        eng = ec.Engine("YaneuraOu_NNUE-tournament-clang++-avx2")

        start_pos = ""
        for i in range(len(kif['moves'])):
            # найти cp за лучший рекомендуемый следующий ход
            temp_because_yaneoura_besit = eng.cp_of_next_move(start_pos, depth=17)
            if temp_because_yaneoura_besit[1] == -111111111:
                bst_mov = temp_because_yaneoura_besit[0]
                mov_cp, mov_cp_40000, mov_cp_localMax = eng.cp_of_current_move(start_pos, bst_mov, depth=17)
            else:
                bst_mov,mov_cp = temp_because_yaneoura_besit
                mov_cp_40000 = mov_cp
                mov_cp_localMax = mov_cp
                mov_cp = int(min(abs(mov_cp),10000)*np.sign(mov_cp))              
            # найти cp за текущий ход
            cur_res, cur_res_40000, cur_res_localMax = eng.cp_of_current_move(start_pos, kif['moves'][i], depth=17)

            # # записать в бд
            db10.move_add(kf_list[i_kifu][0],i,bst_mov,int(mov_cp),int(cur_res))
            db40.move_add(kf_list[i_kifu][0],i,bst_mov,mov_cp_40000,cur_res_40000)
            dblm.move_add(kf_list[i_kifu][0],i,bst_mov,mov_cp_localMax,cur_res_localMax)            
            start_pos += ' ' + kif['moves'][i]
        eng.end()