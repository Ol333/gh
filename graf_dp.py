import matplotlib.pyplot as plt

if __name__ == '__main__':
    fig, ax = plt.subplots()
    ax.set_title("Важный график зависимости", fontsize=16)
    ax.set_xlabel("Ход", fontsize=14)
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
    colors1 = ['#ED665A', '#EDDD8A', '#5AED9C', '#6F66ED']
    colors2 = ['#F03322', '#F2CC02', '#02F26D', '#1B0CF2']
    # colors3 = ['#F03322', '#F2CC02', '#02F26D', '#1B0CF2']
    # f_name_mas = ['output_1616496450_352.txt','output_1616563311.492.txt',
    #             # 'output_1616558184.706.txt','output_1616492912.095.txt',
    #             'output_1616488774.948.txt','output_1616484920.451.txt']
    f_name_mas = ["q_output_(67, 'ottfoekst')_0.txt"]
    for i in range(len(f_name_mas)):
        real_cp = []
        best_next_move_b = [] # уточнить, кто - кто
        best_next_move_w = [] # совпадает ли
        dot_mas = [[],[]]
        f = open(f_name_mas[i],'r')
        iterator = 0
        sign = [1,-1]
        for line in f:
            line_mas = line.replace('\n','').split(' ')
            if line[0] != ' ':
                print(' '.join(line_mas))
            else:
                if iterator%2 == 0:
                    real_cp.append(int(line_mas[-1])*sign[iterator//2%2])
                else:
                    iter = (iterator//2+1)%2
                    if iter == 1:
                        best_next_move_b.append(int(line_mas[-1])*sign[iter])
                    else:
                        best_next_move_w.append(int(line_mas[-1])*sign[iter])
                    if line_mas[1] == line_mas[-2]:
                        dot_mas[0].append((iterator+1)//2)
                        dot_mas[1].append(line_mas[-1])
                iterator += 1

        f.close()
        print(dot_mas)
        iterator = (iterator+1)//2
        ax.plot(range(0,iterator),real_cp,label="поиск cp за реальный ход"+str(f_name_mas[i]))
        ax.plot(range(1,iterator+1,2),best_next_move_b,label="лучший следующий ход сенте"+str(f_name_mas[i]),marker='o')
        ax.plot(range(2,iterator+1,2),best_next_move_w,label="лучший следующий ход готе"+str(f_name_mas[i]),marker='o')
        # ax.plot(range(0,iterator),real_cp,label="поиск cp за реальный ход"+str(f_name_mas[i]),color=colors1[i])
        # ax.plot(range(1,iterator+1),best_next_move,label="лучший следующий ход"+str(f_name_mas[i]),color=colors2[i])
        # ax.scatter(dot_mas[0],dot_mas[1],label="Совпадение хода"+str(f_name), s=40, marker='o')
        ax.scatter(dot_mas[0],dot_mas[1], s=40, marker='o')
        
    ax.legend()
    plt.show()