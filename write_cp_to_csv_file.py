import matplotlib.pyplot as plt
import numpy as np

import rab_with_db as rwd
import csv
import shogi.KIF

if __name__ == '__main__':
    db = rwd.DbConnection("shogi_dblocM.db") # изменить БД - источник
    kf_list = db.table_list("Kifu")
    f = open('dblm_1.csv', 'w') # изменить БД - приемник
    writer = csv.writer(f)
    writer.writerow(['id_pl','id_kif','time','cp','id'])
    
    # for kf in range(10):
    for kf in range(len(kf_list)):
        rcp_mas = []
        number = kf_list[kf][0]        
        kif = shogi.KIF.Parser.parse_str(kf_list[kf][1])[0]
        g_pl = db.player_idbylogin(kif['names'][shogi.BLACK])
        s_pl = db.player_idbylogin(kif['names'][shogi.WHITE])
        g_moves = db.get_cp(number,0)
        s_moves = db.get_cp(number,1) # долго за счет этих постоянных обращений к бд
        print(len(g_moves),len(s_moves))
        prev_cp = 0
        ch = False
        for i in range(len(kif['moves'])):
            if i%2 == 0:
                if i == 0:
                    rcp_mas.append((g_pl,g_moves[i//2][2]))
                    prev_cp = g_moves[i//2][2]
                else:
                    rcp_mas.append((g_pl,g_moves[i//2][2] + prev_cp))
                    prev_cp = g_moves[i//2][2]
            else:
                rcp_mas.append((s_pl,prev_cp + s_moves[i//2][2]))
                prev_cp = s_moves[i//2][2]
        # for i in range(len(g_moves)):
        #     rcp_mas.append((g_pl,g_moves[i][2],i*2))
        # for i in range(len(s_moves)):
        #     rcp_mas.append((s_pl,(-1)*s_moves[i][2],i*2+1))
        rcp_mas = np.array(rcp_mas)
        
        for i in range(len(rcp_mas)):
            writer.writerow([str(rcp_mas[i][0]),str(number),str(i),str(rcp_mas[i][1]),str(rcp_mas[i][0])+' '+str(number)])
    
    f.close()

# if __name__ == '__main__':
#     db = rwd.DbConnection("shogi_dblocM.db")
#     kf_list = db.table_list("Kifu")
#     mov_list = db.table_list("Move")
#     f = open('dblm_2_move.csv', 'w')
#     writer = csv.writer(f)
#     writer.writerow(['id_kif','numb','rec_mov','rec_cp','real_cp'])
#     iter = 0
    
#     # for kf in range(10):
#     for kf in range(len(kf_list)):
#         number = kf_list[kf][0]  
#         kif = shogi.KIF.Parser.parse_str(kf_list[kf][1])[0]
#         prev_cp = 0
#         while iter < len(mov_list) and mov_list[iter][1] == number:
#             numb = mov_list[iter][2]
#             is_matches = False # а это будет работать?
#             if kif['moves'][numb] == mov_list[iter][3]:
#                 is_matches = True
#             rec_cp = (0 if is_matches else (mov_list[iter][4] - mov_list[iter][5])) # а стоит ли его обнулять?
#             real_cp = mov_list[iter][5] + prev_cp
#             prev_cp = mov_list[iter][5]
#             writer.writerow([str(mov_list[iter][1]), str(numb), str(is_matches), str(rec_cp), str(real_cp)])
#             iter += 1
    
#     f.close()