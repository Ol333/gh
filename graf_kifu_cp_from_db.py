import matplotlib.pyplot as plt
import numpy as np
import random

import rab_with_db as rwd

if __name__ == '__main__':
    kf_list = rwd.table_list("Kifu")
    for number in random.sample(range(len(kf_list)),10):
        rcp_mas = []
        # number = 7
        # kf_list = rwd.table_list("Kifu")
        # print(kf_list[number])
        # import shogi.KIF
        # print(shogi.KIF.Parser.parse_str(kf_list[number][1])[0]['win'])
        g_moves = rwd.get_cp(number,0)
        s_moves = rwd.get_cp(number,1)
        print(len(g_moves),len(s_moves))
        for g,s in zip(g_moves,s_moves):
            rcp_mas.append(g[0])
            rcp_mas.append((-1)*s[0])
        rcp_mas = np.array(rcp_mas)
        print(len(rcp_mas))

        fig, ax = plt.subplots()
        fig.suptitle("Оценка ходов движком", fontsize=16)
        ax.set_xlabel("Номер хода", fontsize=14)
        ax.set_ylabel("cp", fontsize=14)
        ax.minorticks_on()
        ax.grid(which="major",linewidth=1.2)
        ax.grid(which="minor",linestyle = ':')
        ax.scatter(range(0,len(rcp_mas)),rcp_mas,label=number)
        ax.legend()
        plt.show()