import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    fig, ax = plt.subplots()
    ax.set_title("Оценка ходов движком", fontsize=16)
    ax.set_xlabel("Номер хода", fontsize=14)
    ax.set_ylabel("cp", fontsize=14)
    ax.minorticks_on()
    ax.grid(which="major",linewidth=1.2)
    ax.grid(which="minor",linestyle = ':')

    colors0 = ['b','r']
    colors00 = ['tab:blue','tab:red']
    f_name = "q_output_(67, 'ottfoekst')_0.txt"
    real_cp_sente = []        # синий
    real_cp_gote = []        # красный
    best_next_move_sente = [] # синий
    best_next_move_gote = [] # красный
    dot_mas = [[],[]]

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
                if iterator//2 % 2 == 0:
                    real_cp_sente.append(int(line_mas[-1])*sign[iterator//2%2])
                else:
                    real_cp_gote.append(int(line_mas[-1])*sign[iterator//2%2])
                move_buf = line_mas[1]
            else:
                iter = (iterator//2+1)%2
                if iter == 1:
                    best_next_move_gote.append(int(line_mas[-1])*sign[iter])
                else:
                    best_next_move_sente.append(int(line_mas[-1])*sign[iter])
                if move_buf == line_mas[-2]:
                    dot_mas[0].append((iterator+1)//2)
                    dot_mas[1].append(line_mas[-1])
            iterator += 1

    f.close()
    print(dot_mas)
    iterator = (iterator+1)//2
    # ax.plot(range(0,iterator),real_cp,label="поиск cp за реальный ход "+str(f_name_mas[i]))
    ax.bar(range(0,iterator,2),real_cp_sente,label="поиск cp за реальный ход сенте "+str(f_name),color=colors00[0])
    ax.bar(range(1,iterator,2),real_cp_gote,label="поиск cp за реальный ход готе "+str(f_name),color=colors00[1])
    ax.plot(np.arange(1.5,iterator+0.5,2.0),best_next_move_sente,label="лучший следующий ход сенте "+str(f_name),marker='o',color=colors0[0])        
    ax.plot(np.arange(0.5,iterator+1.5,2.0),best_next_move_gote,label="лучший следующий ход готе "+str(f_name),marker='o',color=colors0[1])
    ax.scatter(dot_mas[0],dot_mas[1],label="Совпадение хода"+str(f_name), s=40, marker='o', color='g')
    ax.legend()
    plt.show()