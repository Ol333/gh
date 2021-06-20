import sys

import shogi.KIF

import rab_with_db as rwd
import engine_connection as ec

if __name__ == "__main__":
    run_counter = int(sys.argv[1])
    kf_list = rwd.table_list("Kifu")
    # print(kf_list[0])

    for i_kifu in range(run_counter,run_counter+100):
        print('запуск ',run_counter,' кифу')
        kif = shogi.KIF.Parser.parse_str(kf_list[i_kifu][1])[0]
        eng = ec.Engine("YaneuraOu_NNUE-tournament-clang++-avx2")

        start_pos = ""
        for i in range(len(kif['moves'])):
            # найти cp за лучший рекомендуемый следующий ход
            temp_because_yaneoura_besit = eng.cp_of_next_move(start_pos, depth=17)
            if temp_because_yaneoura_besit[1] == -111111111:
                bst_mov = temp_because_yaneoura_besit[0]
                mov_cp = eng.cp_of_current_move(start_pos, bst_mov, depth=17)
            else:
                bst_mov,mov_cp = temp_because_yaneoura_besit
            # найти cp за текущий ход
            cur_res = eng.cp_of_current_move(start_pos, kif['moves'][i], depth=17)
            # записать в бд
            rwd.move_add(kf_list[i_kifu][0],i,mov_cp,bst_mov,cur_res)
            start_pos += ' ' + kif['moves'][i]
        eng.end()