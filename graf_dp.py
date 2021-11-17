import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

# if __name__ == '__main__':
#     all_moves_real = pd.DataFrame()
#     all_moves_pv = pd.DataFrame()
#     fig, ax = plt.subplots()
#     ax.set_title("Оценка ходов 666 партии движком", fontsize=16)
#     ax.set_xlabel("Номер хода", fontsize=14)
#     ax.set_ylabel("cp", fontsize=14)
#     ax.minorticks_on()
#     ax.grid(which="major",linewidth=1.2)
#     ax.grid(which="minor",linestyle = ':')

#     for i in range(1,20):
#         f_name = "666/666_{}.txt".format(i)
#         dot_mas_real = [[],[]]
#         dot_mas_pv = [[],[]]

#         f = open(f_name,'r')
#         iterator = 0
#         for line in f:
#             line_mas = line.replace('\n','').split(' ')
#             line_mas.remove(line_mas[0])
#             line_mas.remove(line_mas[1])
#             line_mas = list(map(int,line_mas))
#             if iterator%2 != 0:
#                 line_mas[1] = -line_mas[1]
#                 line_mas[2] = -line_mas[2]
#             dot_mas_pv[1].append(line_mas[1])
#             dot_mas_pv[0].append(line_mas[0])
#             dot_mas_real[1].append(line_mas[2])
#             dot_mas_real[0].append(line_mas[0])
#             iterator += 1

#         f.close()
#         ax.scatter(dot_mas_pv[0],dot_mas_pv[1], s=70, marker='*', color='g')
#         ax.scatter(dot_mas_real[0],dot_mas_real[1], s=70, marker='*', color='b')
#         all_moves_real[i] = dot_mas_real[1]
#         all_moves_pv[i] = dot_mas_pv[1]
#     plt.show()
#     all_moves_real["std"] = list(np.array(all_moves_real.iloc[i]).std() for i in range(76))
#     all_moves_pv["std"] = list(np.array(all_moves_pv.iloc[i]).std() for i in range(76))
#     print("максимальное отклонение по реальным оценкам",max(all_moves_real["std"]))
#     print("максимальное отклонение по предсказаниям",max(all_moves_pv["std"]))
    
#     all_moves_real["относительная погрешность"] = [0] * 76
#     all_moves_pv["относительная погрешность"] = [0] * 76
#     for i in range(76):
#         move = np.array(all_moves_real.iloc[i])
#         temp_mean = np.mean(move)
#         del_2_rcp = sum(list(map(lambda x:(x-temp_mean)**2,move)))
#         del_random = 2*math.sqrt(del_2_rcp/(19*18))
#         all_moves_real.loc[i,"относительная погрешность"] = 100*del_random/abs(temp_mean)
        
#         move = np.array(all_moves_pv.iloc[i])
#         temp_mean = np.mean(move)
#         del_2_rcp = sum(list(map(lambda x:(x-temp_mean)**2,move)))
#         del_random = 2*math.sqrt(del_2_rcp/(19*18))
#         if temp_mean != 0:
#             all_moves_pv.loc[i,"относительная погрешность"] = 100*del_random/abs(temp_mean)

#     print("максимальная относительная погрешность по реальным оценкам",max(all_moves_real["относительная погрешность"]))
#     print("максимальная относительная погрешность по предсказаниям",max(all_moves_pv["относительная погрешность"]))
        

if __name__ == '__main__':
    colors0 = ['b','r']
    colors00 = ['tab:blue','tab:red']
    f_name = "Y_output_(67, 'ottfoekst')_0_0.txt"
    real_cp_sente = []        # синий
    real_cp_gote = []        # красный
    best_next_move_sente = [] # синий
    best_next_move_gote = [] # красный
    dot_mas = [[],[]]

    fig, ax = plt.subplots()
    ax.set_title("Оценка ходов движком "+str(f_name), fontsize=16)
    ax.set_xlabel("Номер хода", fontsize=14)
    ax.set_ylabel("cp", fontsize=14)
    ax.minorticks_on()
    ax.grid(which="major",linewidth=1.2)
    ax.grid(which="minor",linestyle = ':')

    f = open(f_name,'r')
    iterator = 0
    sign = [1,-1]
    move_buf = ""
    for line in f:
        line_mas = line.replace('\n','').split(' ')
        if line[0] != ' ':
            print(' '.join(line_mas))
        else:
            if iterator%2 == 0:
                iter = (iterator//2)%2
                move_buf = line_mas[-2]
                if iter == 0:
                    best_next_move_sente.append(int(line_mas[-1])*sign[iter])
                else:
                    best_next_move_gote.append(int(line_mas[-1])*sign[iter])
            else:
                if iterator//2 % 2 == 0:
                    real_cp_sente.append(int(line_mas[-1])*sign[iterator//2%2])
                else:
                    real_cp_gote.append(int(line_mas[-1])*sign[iterator//2%2])
                if move_buf == line_mas[1]:
                    dot_mas[0].append(int(iterator//2))
                    dot_mas[1].append(int(line_mas[-1])*sign[iterator//2%2])
            iterator += 1

    f.close()
    print(dot_mas)
    iterator = (iterator+1)//2
    ax.bar(range(0,iterator,2),real_cp_sente,label="поиск cp за реальный ход сенте",color=colors00[0])
    ax.bar(range(1,iterator,2),real_cp_gote,label="поиск cp за реальный ход готе",color=colors00[1])
    ax.plot(np.arange(-0.5,iterator+0.5,2.0),best_next_move_sente,label="лучший следующий ход сенте",marker="o",color=colors0[0])        
    ax.plot(np.arange(0.5,iterator-0.5,2.0),best_next_move_gote,label="лучший следующий ход готе",marker="o",color=colors0[1])
    ax.scatter(dot_mas[0],dot_mas[1],label="Совпадение хода "+str(len(dot_mas[0]))+" шт.", s=70, marker='*', color='g')
    ax.legend()
    plt.show()