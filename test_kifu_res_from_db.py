import numpy as np
import shogi.KIF
import rab_with_db as rwd      # shogi_db (9).db


if __name__ == '__main__':
    # там где прям мат, стоит поставить resigns...
    # сколько ничьих??? >30? <50?  ------ проверить, что эти ребята не сгруппированы в тех играх, которые анализируются в analisis.ipynb
    # по скольким можно четко решить, кто победитель?
    
    game_for_player = []
    player_table = rwd.table_list("Player")
    for i in player_table:
        players_kifu_list = rwd.players_kifu_list(i[0],False)
        game_for_player.append(len(players_kifu_list))
        players_kifu_list = list(map(lambda x:x[1],players_kifu_list))

    pdict = {}
    part = rwd.table_list("Participation")
    stack = [(0,0,0)]
    for p in part:
        pid,pid_p,pid_k = p
        last_pop = stack.pop()
        if last_pop[-1] == pid_k:
            a = min(last_pop[1],pid_p)
            b = max(last_pop[1],pid_p)
            if not ((a,b) in pdict.keys()):
                pdict[(a,b)] = []
            pdict[(a,b)].append(pid_k)
        else:
            stack.append(last_pop)
            stack.append(p)
    print(len(pdict), "пар игроков")

    kf_list = rwd.table_list("Kifu")
    important_kifu_count = 0
    none_count = 0

    for k,v in pdict.items():
        if len(v) > 50:
            for kifu_game in v:
                important_kifu_count += 1
                kif_ind = [a for a,b in enumerate(kf_list) if b[0] == kifu_game][0]
                temp = shogi.KIF.Parser.parse_str(kf_list[kif_ind][1])[0]['win']
                if temp == None:
                    none_count += 1

    # for num in range(len(kf_list)):
    #     temp = shogi.KIF.Parser.parse_str(kf_list[num][1])[0]['win']
    #     if temp == None:
    #         none_count += 1
    print(important_kifu_count,none_count)
    print(round(100*none_count/important_kifu_count,2))