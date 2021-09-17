import math

import matplotlib.pyplot as plt
import numpy as np

# считываем результаты из txt файлов, полученных от запуска
# data_processing.py на разных машинах, рисуем график,
# считаем среднее и отклонение

if __name__ == '__main__':
    # fig, axs = plt.subplots(3, sharex=True, sharey=True)
    # fig.suptitle("Оценка ходов движком", fontsize=16)
    # for i in range(3):
    #     axs[i].set_xlabel("Номер хода", fontsize=14)
    #     axs[i].set_ylabel("cp", fontsize=14)
    #     axs[i].minorticks_on()
    #     axs[i].grid(which="major",linewidth=1.2)
    #     axs[i].grid(which="minor",linestyle = ':')

    colors = ['r','g','b']
    hws = ['pc','gpc','nb']
    number = 0
    
    rcp_calculation_mas = []
    scp_calculation_mas = []
    gcp_calculation_mas = []
    for i in range(63):
        scp_calculation_mas.append([])
    for i in range(64):
        gcp_calculation_mas.append([])
    for i in range(127):
        rcp_calculation_mas.append([])

    for hw in range(3):
        for i in range(20):
            f_name = "{0}/Y_output_(67, 'ottfoekst')_0_{1}.txt".format(hws[hw],i) # 17
            real_cp = [] # средний
            best_next_move_sente = [] # верхний
            best_next_move_gote = [] # нижний
            dot_mas = [[],[]]
            f = open(f_name,'r')
            iterator = 0
            sign = [1,-1]
            move_buf = ""
            for line in f:
                line_mas = line.replace('\n','').split(' ')
                if line[0] != ' ':
                    # print(' '.join(line_mas))
                    pass
                else:
                    if iterator%2 == 0:
                        temp_cp = float(line_mas[-1])*sign[iterator//2%2]
                        real_cp.append(temp_cp)
                        rcp_calculation_mas[len(real_cp)-1].append(temp_cp)
                        move_buf = line_mas[1]
                    else:
                        iter = (iterator//2+1)%2
                        if iter == 1:
                            temp_cp = float(line_mas[-1])*sign[iter]
                            best_next_move_gote.append(temp_cp)
                            gcp_calculation_mas[len(best_next_move_gote)-1].append(temp_cp)
                        else:
                            temp_cp = float(line_mas[-1])*sign[iter]
                            best_next_move_sente.append(temp_cp)
                            scp_calculation_mas[len(best_next_move_sente)-1].append(temp_cp)
                        if move_buf == line_mas[-2]:
                            dot_mas[0].append((iterator+1)//2)
                            dot_mas[1].append(line_mas[-1])
                    iterator += 1
            f.close()
            # print(dot_mas)
            iterator = (iterator+1)//2
            number = iterator
    #         if i == 0:
    #             axs[0].scatter(np.arange(1.5,iterator+0.5,2.0),best_next_move_sente,c=colors[hw],s=20*(3-hw)+10,label=hws[hw])
    #             axs[1].scatter(range(0,iterator),real_cp,c=colors[hw],s=20*(3-hw)+10,label=hws[hw])
    #             axs[2].scatter(np.arange(0.5,iterator+1.5,2.0),best_next_move_gote,c=colors[hw],s=20*(3-hw)+10,label=hws[hw])
    #         else:
    #             axs[0].scatter(np.arange(1.5,iterator+0.5,2.0),best_next_move_sente,c=colors[hw],s=20*(3-hw)+10)
    #             axs[1].scatter(range(0,iterator),real_cp,c=colors[hw],s=20*(3-hw)+10)
    #             axs[2].scatter(np.arange(0.5,iterator+1.5,2.0),best_next_move_gote,c=colors[hw],s=20*(3-hw)+10)
    # axs[0].legend()
    # axs[1].legend()
    # axs[2].legend()

    # fig, ax = plt.subplots()
    # fig.suptitle("Оценка ходов движком", fontsize=16)
    # ax.set_xlabel("Номер хода", fontsize=14)
    # ax.set_ylabel("cp", fontsize=14)
    # ax.minorticks_on()
    # ax.grid(which="major",linewidth=1.2)
    # ax.grid(which="minor",linestyle = ':')
    # legend = []
    mas_for_difference_mean = []
    mas_for_difference_std = []
    del_absol_mas_differ = []
    graf_for_three = dict.fromkeys(hws)
    graf_for_three['pc'] = {'mean':[],'std':[],'delta':[]}
    graf_for_three['gpc'] = {'mean':[],'std':[],'delta':[]}
    graf_for_three['nb'] = {'mean':[],'std':[],'delta':[]}
    
    rcp_calculation_mas = np.array(rcp_calculation_mas)
    gcp_calculation_mas = np.array(gcp_calculation_mas)
    scp_calculation_mas = np.array(scp_calculation_mas)
    mean_rcp_mas = []
    std_rcp_mas = []
    del_absol_mas = []
    ind = 0
    for move in rcp_calculation_mas:
        # move = list(map(lambda x: x/3500,move))
        temp_mean = np.mean(move)
        mean_rcp_mas.append(temp_mean)
        std_rcp_mas.append(np.std(move))
        del_2_rcp = sum(list(map(lambda x:(x-temp_mean)**2,move)))
        del_random = 2*math.sqrt(del_2_rcp/(60*59))
        del_absol_mas.append(100*del_random/abs(temp_mean))
        # if ind == 0:
        #     ax.scatter([ind]*20,move[:20],c=colors[0],s=40,label=hws[0])
        #     ax.scatter([ind]*20,move[20:40],c=colors[1],s=30,label=hws[1])
        #     ax.scatter([ind]*20,move[40:],c=colors[2],s=20,label=hws[2])
        # else:
        #     ax.scatter([ind]*20,move[:20],c=colors[0],s=40)
        #     ax.scatter([ind]*20,move[20:40],c=colors[1],s=30)
        #     ax.scatter([ind]*20,move[40:],c=colors[2],s=20)
        z = 1.282 # для 95%
        n = ((np.std(move))**2 * z**2) / (10**2)
        print(round(n))
        if ind > 0:
            diff = rcp_calculation_mas[ind]-rcp_calculation_mas[ind-1]
            mas_for_difference_mean.append(np.mean(diff))
            mas_for_difference_std.append(np.std(diff))
            temp_mean = np.mean(diff)
            del_2_cp = sum(list(map(lambda x:(x-temp_mean)**2,diff)))
            del_random = 2*math.sqrt(del_2_cp/(60*59))
            del_absol_mas_differ.append(100*del_random/abs(temp_mean))

        for i in range(3):
            temp_mean = np.mean(move[20*i:20*(i+1)])
            graf_for_three[hws[i]]['mean'].append(np.mean(move[20*i:20*(i+1)]))
            graf_for_three[hws[i]]['std'].append(np.std(move[20*i:20*(i+1)]))  
            del_2_rcp = sum(list(map(lambda x:(x-temp_mean)**2,move[20*i:20*(i+1)])))
            del_random = 2.09*math.sqrt(del_2_rcp/(20*19))
            delta = 100*del_random/abs(temp_mean)
            graf_for_three[hws[i]]['delta'].append(delta)
            # ax.text(ind,np.mean(move[20*i:20*(i+1)]),str(round(delta))+'%',fontsize=10)
        ind += 1
    gdel_absol_mas = []
    for move in gcp_calculation_mas:
        temp_mean = np.mean(move)
        del_2_gcp = sum(list(map(lambda x:(x-temp_mean)**2,move)))
        del_random = 2*math.sqrt(del_2_gcp/(60*59))
        gdel_absol_mas.append(100*del_random/abs(temp_mean))
    sdel_absol_mas = []
    for move in scp_calculation_mas:
        temp_mean = np.mean(move)
        del_2_scp = sum(list(map(lambda x:(x-temp_mean)**2,move)))
        del_random = 2*math.sqrt(del_2_scp/(60*59))
        sdel_absol_mas.append(100*del_random/abs(temp_mean))
    mean_rcp_mas = np.array(mean_rcp_mas)
    std_rcp_mas = np.array(std_rcp_mas)
    delta = (1-0.8/2)*(std_rcp_mas/math.sqrt(60))
    # print(del_absol_mas)
    print('мин, ср и макс относительной погрешности',min(del_absol_mas),np.mean(del_absol_mas),max(del_absol_mas))
    # ax.errorbar(range(0,number), mean_rcp_mas, delta, linestyle='None', marker=None, capsize=6, ecolor='k',label='error')
    # ax.legend()
    print('мин, ср и макс среднего арифм',min(mean_rcp_mas),np.mean(mean_rcp_mas),max(mean_rcp_mas))
    print('мин, ср и макс отклонения',min(std_rcp_mas),np.mean(std_rcp_mas),max(std_rcp_mas))
    for i in range(3):
        temp = graf_for_three[hws[i]]['delta']
        print('мин, ср и макс относит погрешн по компам',str(hws[i]),min(temp),np.mean(temp),max(temp))
        # print(list(map(lambda x:round(x),temp)))
    # print(list(map(lambda x:round(x),gdel_absol_mas)))
    # print(list(map(lambda x:round(x),del_absol_mas)))
    # print(list(map(lambda x:round(x),sdel_absol_mas)))
    print('###########')
    print('мин, ср и макс ср разностей',min(mas_for_difference_mean),np.mean(mas_for_difference_mean),max(mas_for_difference_mean))
    print('мин, ср и макс откл разностей',min(mas_for_difference_std),np.mean(mas_for_difference_std),max(mas_for_difference_std))
    print('мин, ср и макс погрешность разностей',min(del_absol_mas_differ),np.mean(del_absol_mas_differ),max(del_absol_mas_differ))
    # print(list(map(lambda x:round(x),mas_for_difference_mean)))
    # print(list(map(lambda x:round(x),mas_for_difference_std)))
    # print(list(map(lambda x:round(x),del_absol_mas_differ)))
    
    print('###########')
    print('мин, ср и макс относ погрешн готе',min(gdel_absol_mas),np.mean(gdel_absol_mas),max(gdel_absol_mas))
    print('мин, ср и макс относ погрешн сенте',min(sdel_absol_mas),np.mean(sdel_absol_mas),max(sdel_absol_mas))

    # # интервалы
    # fig, ax = plt.subplots()
    # fig.suptitle("Оценка ходов движком", fontsize=16)
    # ax.set_xlabel("Номер хода", fontsize=14)
    # ax.set_ylabel("cp", fontsize=14)
    # ax.minorticks_on()
    # ax.grid(which="major",linewidth=1.2)
    # ax.grid(which="minor",linestyle = ':')
    # legend = []
    # for i in range(3):
    #     # mean
    #     # ax.scatter(range(0,number),np.array(graf_for_three[hws[i]]['mean']),label=hws[i])
    #     ax.errorbar(range(0,number),
    #             np.array(graf_for_three[hws[i]]['mean']),
    #             np.array(graf_for_three[hws[i]]['std']),
    #             linestyle='None', elinewidth=9-i*3,
    #             label=hws[i])
    # ax.legend()

    plt.show()