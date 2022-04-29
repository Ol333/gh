import matplotlib.pyplot as plt
import engine_connection as ec

if __name__ == '__main__':
    answear = input("Запустить отрисовку графика? Y/N")
    if answear == "Y":
        max_depth = 12
        engine_list_for_graphic = ["gikou","Kristallweizen","nozomi"]
        counter_of_moves = [[0]*max_depth,[0]*max_depth,[0]*max_depth]
        print(counter_of_moves)
        f = open('new_output_3ris.txt','r')
        count = 0
        for line in f:
            line = line.replace('\n','')
            if line[:5] in ['gikou','Krist','Yaneu','nozom']:
                count += 1
            else:
                temp = line.split(' ')
                counter_of_moves[count][int(temp[2])] = int(temp[4])
        # counter_of_moves = [ [81,47,61,81,87,105,87,95,139,115],
        #                     [67,99,93,91,103,119,89,117,93,73],
        #                     [23,83,75,57,139,87,101,101,101,103]]

        fig,ax = plt.subplots()
        ax.set_xlabel("Глубина поиска лучшего хода", fontsize=14)
        ax.set_ylabel("Среденее количество ходов в партии", fontsize=14)
        ax.grid(which="major",linewidth=1.2)
        for k in range(3):
            ax.plot(range(1,max_depth+1),counter_of_moves[k],label=engine_list_for_graphic[k])
        ax.tick_params(which='major', length=10, width=1)
        ax.legend()
        plt.show()
    else:
        max_depth = 12
        engine_list = ["gikou","Kristallweizen-wcsc29-avx2","nozomi"]
        engine_list_for_graphic = ["gikou","Kristallweizen","nozomi"]
        counter_of_moves = [[],[],[]]
        eng_win_counter = [[],[],[]]
        eng_stalemate_counter = [[],[],[]]
        for i in range(3):
            for _ in range(max_depth):
                counter_of_moves[i].append([0,0])
                eng_win_counter[i].append(0)
                eng_stalemate_counter[i].append(0)

        for depth_counter in range(max_depth):
            print(depth_counter)
            for k2 in range(3):
                print(k2)
                eng1 = ec.Engine("YaneuraOu_NNUE-tournament-clang++-avx2")
                eng2 = ec.Engine(engine_list[k2])

                for i in range(10):
                    moves_order = []
                    while True and len(moves_order) < 320:
                        move = eng1.make_certain_depth_move(moves_order,17)
                        if move == "resign":
                            eng_win_counter[k2][depth_counter] += 1
                            break
                        moves_order.append(move)
                        
                        move = eng2.make_certain_depth_move(moves_order,depth_counter+1)
                        if move == "resign":
                            break
                        moves_order.append(move)
                    print("End")
                if len(moves_order)<320:
                    counter_of_moves[k2][depth_counter][0] += len(moves_order)
                    counter_of_moves[k2][depth_counter][1] += 1
                else:
                    eng_stalemate_counter[k2][depth_counter] += 1
                eng1.end()
                eng2.end()

        f = open('new_output_3ris.txt', 'w')
        for k in range(3):
            f.write(str(engine_list[k])+'\n')
            for i in range(max_depth):
                counter_of_moves[k][i] = counter_of_moves[k][i][0]/counter_of_moves[k][i][1]
                f.write("среднее время "+str(i)+' - '+str(counter_of_moves[k][i])+" победы - "+str(eng_win_counter[k][i])+" ничьи - "+str(eng_stalemate_counter[k][i])+'\n')
        f.close()
            
        fig,ax = plt.subplots()
        ax.set_xlabel("Глубина поиска лучшего хода", fontsize=14)
        ax.set_ylabel("Среденее количество ходов в партии", fontsize=14)
        ax.grid(which="major",linewidth=1.2)
        for k in range(3):
            ax.plot(range(1,max_depth+1),counter_of_moves[k],label=engine_list_for_graphic[k])
        ax.tick_params(which='major', length=10, width=1)
        ax.legend()
        plt.show()