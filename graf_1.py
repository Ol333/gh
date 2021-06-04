import matplotlib.pyplot as plt
import engine_connection as ec

if __name__ == '__main__':
    answear = input("Запустить отрисовку графика? Y/N")
    if answear == "Y":
        max_depth = 17
        eng_time_param = []
        f = open('new_output_1ris_check — копия.txt','r')
        counter = 0
        time_mas = []
        time_mas_labels = []
        for line in f:
            line = line.replace('\n','')
            if "среднее" in line:
                temp = float(line.split(' ')[-1])
                time_mas_labels.append(round(temp))
                time_mas.append(temp)
            else:
                if line == str(counter):
                    eng_time_param.append([])
                    counter += 1
                else:
                    eng_time_param[counter-1].append(float(line))

        fig, ax = plt.subplots()
        ax.set_title("Важный график зависимости времени размышлений от глубины поиска хода", fontsize=16)
        ax.set_xlabel("глубина поиска лучшего хода", fontsize=14)
        ax.set_ylabel("время, потраченное движком на ходы в течение игры, с", fontsize=14)
        ax.grid(which="major",linewidth=1.2)
        ax.plot(range(1,max_depth+1),eng_time_param[0],label="gikou")
        ax.plot(range(1,max_depth+1),eng_time_param[1],label="Kristallweizen")
        ax.plot(range(1,max_depth+1),eng_time_param[2],label="YaneuraOu")
        ax.plot(range(1,max_depth+1),eng_time_param[3],label="nozomi")

        rect = ax.bar(range(1,max_depth+1),time_mas,0.9,label='Общее количество ходов',color=["#E6DD26"])
        ax.bar_label(rect,time_mas_labels,padding=3)

        ax.legend()
        ax.tick_params(which='major', length=10, width=1)
        plt.show()
    else:
        start_depth = 15
        max_depth = 17
        stalemate_list = [[],[],[],[]]
        engine_list = ["gikou","Kristallweizen-wcsc29-avx2","YaneuraOu_NNUE-tournament-clang++-avx2","nozomi"]
        eng_time_param = [[0]*max_depth, [0]*max_depth, [0]*max_depth, [0]*max_depth]
        counter_of_moves = []
        for i in range(max_depth):
            counter_of_moves.append([0,0])

        for depth_counter in range(start_depth,max_depth):
            for k1 in range(4):
                for k2 in range(k1+1,4):
                    print(k1,k2)
                    eng1 = ec.Engine(engine_list[k1])
                    eng2 = ec.Engine(engine_list[k2])

                    for i in range(10):
                        moves_order = []
                        while True and len(moves_order) < 320:
                            move = eng1.make_certain_depth_move(moves_order,depth_counter+1)
                            if move == "resign":
                                eng1.not_end("win")
                                eng2.not_end("lose")
                                break
                            moves_order.append(move)
                            
                            move = eng2.make_certain_depth_move(moves_order,depth_counter+1)
                            if move == "resign":
                                eng1.not_end("lose")
                                eng2.not_end("win")
                                break
                            moves_order.append(move)
                        print("End")
                    if len(moves_order)<320:
                        eng_time_param[k1][depth_counter] += eng1.get_time_for_test_depth()
                        eng_time_param[k2][depth_counter] += eng2.get_time_for_test_depth()
                        counter_of_moves[depth_counter][0] += len(moves_order)
                        counter_of_moves[depth_counter][1] += 1
                    else:
                        stalemate_list[k1].append(depth_counter)
                        stalemate_list[k2].append(depth_counter)
                    eng1.end()
                    eng2.end()
        for i in range(4):
            for j in range(start_depth,max_depth):
                count = max_depth-start_depth
                if j in stalemate_list[i]:
                    count -= stalemate_list[i].count(j)
                eng_time_param[i][j] = eng_time_param[i][j] / count

        f = open('new_output.txt', 'w')
        for i in range(4):
            f.write(str(i)+"\n")
            for j in range(start_depth,max_depth):
                f.write(str(float('{:.3f}'.format(eng_time_param[i][j]))) + "\n")
        time_mas_labels = []
        for i in range(start_depth,max_depth):
            counter_of_moves[i] = counter_of_moves[i][0]/counter_of_moves[i][1]
            time_mas_labels.append(counter_of_moves[i])
            f.write("среднее ходов "+str(i)+' - '+str(counter_of_moves[i])+'\n')
        f.close()
        
        fig, ax = plt.subplots()
        ax.set_title("Важный график зависимости времени размышлений от глубины поиска хода", fontsize=16)
        ax.set_xlabel("время, потраченное движком на ходы в течение игры, с", fontsize=14)
        ax.set_ylabel("глубина поиска лучшего хода", fontsize=14)
        ax.grid(which="major",linewidth=1.2)
        ax.plot(range(1,max_depth+1),eng_time_param[0],label="gikou")
        ax.plot(range(1,max_depth+1),eng_time_param[1],label="Kristallweizen")
        ax.plot(range(1,max_depth+1),eng_time_param[2],label="YaneuraOu")
        ax.plot(range(1,max_depth+1),eng_time_param[3],label="nozomi")
        rect = ax.bar(range(1,max_depth+1),counter_of_moves,0.9,label='Общее количество ходов',color=["#FFF9CD"])
        ax.bar_label(rect,time_mas_labels,padding=3)
        ax.legend()
        ax.tick_params(which='major', length=10, width=1)
        plt.show()        