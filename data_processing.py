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
        # остается вопрос по мультимодальности, но вроде такое не встречается
            print("предсказание :")
            needed_n = 10
            mov_dict = {}
            sample_bst_mov = []
            sample_mov_cp = []
            mov_cp_std = 0
            temp_key = ''
            temp_max_len = 0
            while len(sample_mov_cp) <= needed_n:
                # найти cp за лучший рекомендуемый следующий ход
                temp_because_yaneoura_besit = eng.cp_of_next_move(start_pos, depth=17)
                if temp_because_yaneoura_besit[1] == -111111111:
                    bst_mov = temp_because_yaneoura_besit[0]
                    mov_cp = eng.cp_of_current_move(start_pos, bst_mov, depth=17)
                else:
                    bst_mov,mov_cp = temp_because_yaneoura_besit
                sample_bst_mov.append(bst_mov)
                sample_mov_cp.append(mov_cp)
                if not (bst_mov in mov_dict.keys()):
                    mov_dict[bst_mov] = []
                mov_dict[bst_mov].append(mov_cp)
                if len(sample_mov_cp) == needed_n:
                    temp_key = ''
                    temp_max_len = 0
                    for k,v in mov_dict.items():
                        if len(v) > temp_max_len:
                            temp_max_len = len(v)
                            temp_key = k
                    mov_cp_std = np.array(mov_dict[temp_key]).std()
                    needed_n = math.ceil((((z_85*mov_cp_std)/e)**2) * (len(sample_mov_cp)/temp_max_len))
                    print('изменили needed_n',"std",mov_cp_std,"new n:",needed_n, 'итерация №',len(sample_mov_cp))
            mov_cp = round(np.array(mov_dict[temp_key]).mean())
            bst_mov = temp_key
            print(mov_dict)
            print(len(mov_dict),'разных ходов.',"Выбрали pv: ",bst_mov)
            print("mov_cp",mov_cp)
            print("needed_n mov_cp",needed_n)

            print("оценка :")
            needed_n = 10
            sample_cur_res = []
            cur_res_std = 0
            while len(sample_cur_res) <= needed_n:
                # найти cp за текущий ход
                cur_res = eng.cp_of_current_move(start_pos, kif['moves'][i], depth=17)
                sample_cur_res.append(cur_res)
                if len(sample_cur_res) == needed_n:
                    cur_res_std = np.array(sample_cur_res).std()
                    needed_n = math.ceil(((z_85*cur_res_std)/e)**2)
                    print('изменили needed_n','std = ',cur_res_std,"new n:",needed_n, 'итерация №',len(sample_cur_res))
            cur_res = round(np.array(sample_cur_res).mean())
            # print(sample_cur_res)
            print("cur_res",cur_res)
            print("needed_n cur_res",needed_n)
            print()

            # # записать в бд
            # # провести больше запусков, чтобы получить число поточнее..................................................
            # rwd.move_add(kf_list[i_kifu][0],i,mov_cp,bst_mov,cur_res)
            start_pos += ' ' + kif['moves'][i]
        eng.end()