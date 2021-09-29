import sys
import math
import numpy as np
import shogi.KIF

import rab_with_db as rwd
import engine_connection as ec

z_85 = 1.00
e = 10

if __name__ == "__main__":
    run_counter = int(sys.argv[1])
    kf_list = rwd.table_list("Kifu")
    # print(kf_list[0])

    # for i_kifu in range(run_counter,run_counter+1000):
    for i_kifu in range(run_counter,run_counter+1):
        print('запуск ',i_kifu,' кифу')
        try:
            kif = shogi.KIF.Parser.parse_str(kf_list[i_kifu][1])[0]
        except Exception as ex:
            f = open('wrong_kifu.txt', 'a')
            f.write(str(i_kifu) + '\n') #вывести в файл номер неправильного кифу
            f.close()
        eng = ec.Engine("YaneuraOu_NNUE-tournament-clang++-avx2")

        start_pos = ""
        for i in range(len(kif['moves'])):
        # for i in range(10):
            n = 0
            needed_n = 10
            sample_bst_mov = []
            sample_mov_cp = []
            mov_cp_std = 0
            while n <= needed_n:
                # найти cp за лучший рекомендуемый следующий ход
                temp_because_yaneoura_besit = eng.cp_of_next_move(start_pos, depth=17)
                if temp_because_yaneoura_besit[1] == -111111111:
                    bst_mov = temp_because_yaneoura_besit[0]
                    mov_cp = eng.cp_of_current_move(start_pos, bst_mov, depth=17)
                else:
                    bst_mov,mov_cp = temp_because_yaneoura_besit
                sample_bst_mov.append(bst_mov)
                sample_mov_cp.append(mov_cp)
                n += 1
                if n == 10:
                    mov_cp_std = np.array(sample_mov_cp).std()
                if n == needed_n:
                    temp_np_array = np.array(sample_mov_cp)
                    needed_n = math.ceil(((z_85*mov_cp_std)/e)**2)
                    print('изменили needed_n',z_85,mov_cp_std,e)
                    mov_cp_std = temp_np_array.std()
            mov_cp = np.array(sample_mov_cp).mean()
            print(sample_mov_cp)
            print(len(set(sample_bst_mov)),'разных ходов')
            print("mov_cp",mov_cp)
            print("needed_n",needed_n)
            # bst_mov = найти ближайший mov_cp из sample_mov_cp и взять по индексу bst_mov ### а верно ли это вообще ?
            # отсортировать копию и бинарным поиском...

            # # найти cp за текущий ход
            # cur_res = eng.cp_of_current_move(start_pos, kif['moves'][i], depth=17)

            # # записать в бд
            # # провести больше запусков, чтобы получить число поточнее..................................................
            # rwd.move_add(kf_list[i_kifu][0],i,mov_cp,bst_mov,cur_res)
            start_pos += ' ' + kif['moves'][i]
        eng.end()