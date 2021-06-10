import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

if __name__ == '__main__':
    fig, ax = plt.subplots()
    ax.set_title("Оценка ходов движком", fontsize=16)
    ax.set_xlabel("Номер хода", fontsize=14)
    ax.set_ylabel("cp", fontsize=14)
    ax.minorticks_on()
    ax.grid(which="major",linewidth=1.2)
    ax.grid(which="minor",linestyle = ':')

    # f = open('output_1616496450_352.txt','r') # Гпк
    # f = open('output_1616563311.492.txt','r') # ноут
    # f = open('output_1616558184.706.txt','r') # пк
    # f = open('output_1616492912.095.txt','r') # пк
    # f = open('output_1616488774.948.txt','r') # пк
    # f = open('output_1616484920.451.txt','r') # пк
    colors0 = ['b','r']
    colors00 = ['tab:blue','tab:red']
    colors1 = ['#ED665A', '#EDDD8A', '#5AED9C', '#6F66ED']
    colors2 = ['#F03322', '#F2CC02', '#02F26D', '#1B0CF2']
    # colors3 = ['#F03322', '#F2CC02', '#02F26D', '#1B0CF2']
    # f_name_mas = ['output_1616496450_352.txt','output_1616563311.492.txt',
    #             # 'output_1616558184.706.txt','output_1616492912.095.txt',
    #             'output_1616488774.948.txt','output_1616484920.451.txt']
    f_name_mas = ["q_output_(67, 'ottfoekst')_0.txt"]
    for i in range(len(f_name_mas)):
        real_cp = []
        best_next_move_sente = [] # синий
        best_next_move_sente.append(0.0)
        best_next_move_gote = [] # красный
        dot_mas = [[],[]]
        f = open(f_name_mas[i],'r')
        iterator = 0
        sign = [1,-1]
        move_buf = ""
        for line in f:
            line_mas = line.replace('\n','').split(' ')
            if line[0] != ' ':
                print(' '.join(line_mas))
            else:
                if iterator%2 == 0:
                    real_cp.append(float(line_mas[-1])*sign[iterator//2%2])
                    move_buf = line_mas[1]
                else:
                    iter = (iterator//2+1)%2
                    if iter == 1:
                        best_next_move_gote.append(float(line_mas[-1])*sign[iter])
                        best_next_move_gote.append(float(line_mas[-1])*sign[iter])
                    else:
                        best_next_move_sente.append(float(line_mas[-1])*sign[iter])
                        best_next_move_sente.append(float(line_mas[-1])*sign[iter])
                    if move_buf == line_mas[-2]:
                        dot_mas[0].append((iterator+1)//2)
                        dot_mas[1].append(line_mas[-1])
                iterator += 1
        f.close()
        print(dot_mas)
        iterator = (iterator+1)//2
        best_next_move_gote.pop()
        # best_next_move_sente = np.array(best_next_move_sente)
        # real_cp = np.array(real_cp)
        # best_next_move_gote = np.array(best_next_move_gote)
        # print(len(best_next_move_sente),len(real_cp),len(best_next_move_gote))
        index_mas = ['лучший следующий ход сенте','поиск cp за реальный ход','лучший следующий ход готе']
        temp_list = np.array([best_next_move_sente,real_cp,best_next_move_gote])
        data = pd.DataFrame(temp_list, columns=range(0,iterator), index=index_mas)
        heatmap_plot = sns.heatmap(data, vmin=-3000, vmax=3000, center=0, cmap= 'coolwarm')
        # print(len(best_next_move_sente),len(real_cp),len(best_next_move_gote))
        
        # # ax.plot(range(0,iterator),real_cp,label="поиск cp за реальный ход "+str(f_name_mas[i]))
        # ax.bar(range(0,iterator,2),real_cp_sente,label="поиск cp за реальный ход сенте "+str(f_name_mas[i]),color=colors00[0])
        # ax.bar(range(1,iterator,2),real_cp_gote,label="поиск cp за реальный ход готе "+str(f_name_mas[i]),color=colors00[1])
        # ax.plot(np.arange(1.5,iterator+0.5,2.0),best_next_move_sente,label="лучший следующий ход сенте "+str(f_name_mas[i]),marker='o',color=colors0[0])        
        # ax.plot(np.arange(0.5,iterator+1.5,2.0),best_next_move_gote,label="лучший следующий ход готе "+str(f_name_mas[i]),marker='o',color=colors0[1])
        # # ax.plot(range(0,iterator),real_cp,label="поиск cp за реальный ход"+str(f_name_mas[i]),color=colors1[i])
        # # ax.plot(range(1,iterator+1),best_next_move,label="лучший следующий ход"+str(f_name_mas[i]),color=colors2[i])
        # # ax.scatter(dot_mas[0],dot_mas[1],label="Совпадение хода"+str(f_name), s=40, marker='o')
        # ax.scatter(dot_mas[0],dot_mas[1], s=40, marker='o')
        
    ax.legend()
    plt.show()