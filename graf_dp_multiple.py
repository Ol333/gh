import matplotlib.pyplot as plt
import numpy as np
import scipy as sp

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

            # axs[0].scatter(np.arange(1.5,iterator+0.5,2.0),best_next_move_sente,c=colors[hw])
            # axs[1].scatter(range(0,iterator),real_cp,c=colors[hw])
            # axs[2].scatter(np.arange(0.5,iterator+1.5,2.0),best_next_move_gote,c=colors[hw])
    
    graf_for_three = dict.fromkeys(hws)
    graf_for_three['pc'] = {'mean':[],'std':[]}
    graf_for_three['gpc'] = {'mean':[],'std':[]}
    graf_for_three['nb'] = {'mean':[],'std':[]}
    rcp_calculation_mas = np.array(rcp_calculation_mas)
    gcp_calculation_mas = np.array(gcp_calculation_mas)
    scp_calculation_mas = np.array(scp_calculation_mas)
    mean_rcp_mas = []
    std_rcp_mas = []
    for move in rcp_calculation_mas:
        mean_rcp_mas.append(np.mean(move))
        std_rcp_mas.append(np.std(move))
        graf_for_three['pc']['mean'].append(np.mean(move[:20]))
        graf_for_three['pc']['std'].append(np.std(move[:20]))
        graf_for_three['gpc']['mean'].append(np.mean(move[20:40]))
        graf_for_three['gpc']['std'].append(np.std(move[20:40]))
        graf_for_three['nb']['mean'].append(np.mean(move[40:]))
        graf_for_three['nb']['std'].append(np.std(move[40:]))
    mean_rcp_mas = np.array(mean_rcp_mas)
    std_rcp_mas = np.array(std_rcp_mas)
    print('мин, ср и макс среднего арифм',min(mean_rcp_mas),np.mean(mean_rcp_mas),max(mean_rcp_mas))
    print('мин, ср и макс отклонения',min(std_rcp_mas),np.mean(std_rcp_mas),max(std_rcp_mas))
    
    fig, ax = plt.subplots()
    fig.suptitle("Оценка ходов движком", fontsize=16)
    ax.set_xlabel("Номер хода", fontsize=14)
    ax.set_ylabel("cp", fontsize=14)
    ax.minorticks_on()
    ax.grid(which="major",linewidth=1.2)
    ax.grid(which="minor",linestyle = ':')
    for i in range(3):
        ax.errorbar(range(0,number),
                np.array(graf_for_three[hws[i]]['mean']),
                np.array(graf_for_three[hws[i]]['std']),
                linestyle='None', marker='.',
                ecolor=colors[i], #сделать что-то с цветами
                elinewidth=9-i*3)

    fig, ax = plt.subplots()
    fig.suptitle("Оценка ходов движком", fontsize=16)
    ax.set_xlabel("Номер хода", fontsize=14)
    ax.set_ylabel("cp", fontsize=14)
    ax.minorticks_on()
    ax.grid(which="major",linewidth=1.2)
    ax.grid(which="minor",linestyle = ':')
    ax.errorbar(range(0,number),mean_rcp_mas,std_rcp_mas,linestyle='None', marker='.')
    fx = np.linspace(0, number, number)    
    fp, residuals, rank, sv, rcond = np.polyfit(range(0,number),mean_rcp_mas, 5, full=True)
    f = sp.poly1d(fp)
    ax.plot(fx, f(fx), linewidth=2)
    # axs[1].plot(fx, f(fx), linewidth=2)



    fig, ax = plt.subplots()
    fig.suptitle("Оценка ходов движком", fontsize=16)
    ax.set_xlabel("Номер хода", fontsize=14)
    ax.set_ylabel("cp", fontsize=14)
    ax.minorticks_on()
    ax.grid(which="major",linewidth=1.2)
    ax.grid(which="minor",linestyle = ':')
    ax.scatter(range(0,number-1),mean_rcp_mas[:-1],c=colors[hw])
    legend = []
    fx = sp.linspace(0, number-1, 1000)
    for d in range(0,15):
        fp, residuals, rank, sv, rcond = np.polyfit(range(0,number-1),mean_rcp_mas[:-1], d, full=True)
        print("Параметры модели: %s" % fp)
        f = sp.poly1d(fp)
        print(f)

        ax.plot(fx, f(fx), linewidth=2, label=d)
        legend.append("d=%i" % f.order)

    # print('rcp')
    # for move in rcp_calculation_mas:
    #     print(np.mean(move),np.std(move))
    # print('gcp')
    # for move in gcp_calculation_mas:
    #     print(np.mean(move),np.std(move))
    # print('scp')
    # for move in scp_calculation_mas:
    #     print(np.mean(move),np.std(move))
    ax.legend()
    plt.show()