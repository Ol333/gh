import numpy as np
import shogi.KIF
import rab_with_db as rwd      # shogi_db (9).db


if __name__ == '__main__':
    # там где прям мат, стоит поставить resigns...
    # сколько ничьих??? >30? <50?  ------ проверить, что эти ребята не сгруппированы в тех играх, которые анализируются в analisis.ipynb
    # по скольким можно четко решить, кто победитель?
    
    game_for_player = []
    db = rwd.DbConnection("shogi_dblocM.db")
    # player_table = db.table_list("Player")
    # for i in player_table:
    #     players_kifu_list = db.players_kifu_list(i[0],False)
    #     game_for_player.append(len(players_kifu_list))
    #     players_kifu_list = list(map(lambda x:x[1],players_kifu_list))

    # pdict = {}
    # part = db.table_list("Participation")
    # stack = [(0,0,0)]
    # for p in part:
    #     pid,pid_p,pid_k = p
    #     last_pop = stack.pop()
    #     if last_pop[-1] == pid_k:
    #         a = min(last_pop[1],pid_p)
    #         b = max(last_pop[1],pid_p)
    #         if not ((a,b) in pdict.keys()):
    #             pdict[(a,b)] = []
    #         pdict[(a,b)].append(pid_k)
    #     else:
    #         stack.append(last_pop)
    #         stack.append(p)
    # print(len(pdict), "пар игроков")

    kf_list = db.table_list("Kifu")
    # for k in kf_list:
    #     if len(shogi.KIF.Parser.parse_str(k[1])[0]["moves"]) == 0:
    #         print(k[0],end=', ')

    # important_kifu_count = 0
    # none_count = 0

    # for k,v in pdict.items():
    #     if len(v) > 50:
    #         for kifu_game in v:
    #             important_kifu_count += 1
    #             kif_ind = [a for a,b in enumerate(kf_list) if b[0] == kifu_game][0]
    #             temp = shogi.KIF.Parser.parse_str(kf_list[kif_ind][1])[0]['win']
    #             if temp == None:
    #                 none_count += 1

    # print(important_kifu_count,none_count)
    # print(round(100*none_count/important_kifu_count,2))

    


    none_count = []
    f = open("output.txt",'w')
    for num in range(len(kf_list)):
        try:
            # temp = shogi.KIF.Parser.parse_str(kf_list[num][1])[0]['win']
            if shogi.KIF.Parser.parse_str(kf_list[num][1])[0]['sfen'] != 'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1':
                # print('емае')
                f.write(str(kf_list[num][0])+', ')
                none_count.append(kf_list[num][0])
            # if temp == None:
            #     none_count.append(kf_list[num][0])
            #     f.write(str(kf_list[num][0])+', ')
        except Exception as ex:
            print(kf_list[num][0],end=', ')

    print(len(kf_list),len(none_count))
    print(round(100*len(none_count)/len(kf_list),2))

    # print(none_count)
    f.close()