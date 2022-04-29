import time
import matplotlib.pyplot as plt
import engine_connection as ec

if __name__ == '__main__':
    answear = input("Запустить отрисовку графика? Y/N")
    if answear == "Y":
        engine_list = ["gikou","Kristallweizen","YaneuraOu","nozomi"]
        win_mas = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        f = open('new_output_2ris_test18_5.txt','r')
        count = 0
        k = 0
        for line in f:
            line = line.replace('\n','')
            if line[:5] in ['gikou','Krist','Yaneu','nozom']:
                win_mas[count][k] = int(line.split(' ')[2])
                k += 1
            if line in ["900000 5000","300000 10000"]:
                print("?")
                count += 1
                k = 0
        # win_mas[0] = [6, 23, 30, 11]
        # win_mas[1] = [21, 25, 25, 19]
        # win_mas[2] = [36, 24, 11, 17]

        title_mas = ["25 мин. (0 с)","15 мин. (5 с)","5 мин. (10 с)"]
        fig, axes = plt.subplots(nrows = 1, ncols = 3)
        for i in range(3):
            axes[i].set_title(title_mas[i], fontsize=16)
            axes[i].set_xlabel("Движок", fontsize=14)
            axes[i].set_ylabel("Количество побед, шт.", fontsize=14)
            rect = axes[i].bar(engine_list,win_mas[i],0.9,label='Количество побед',color=["#FFF9CD"])
            axes[i].legend()
        plt.show()
    else:
        time_of_work = []
        f = open('new_output_2ris_test18.txt', 'a')
        engine_list = ["gikou","Kristallweizen-wcsc29-avx2","YaneuraOu_NNUE-tournament-clang++-avx2","nozomi"]
        aa = list(map(lambda x:x*1000,[1500,900,300]))
        cc = list(map(lambda x:x*1000,[0,5,10]))

        for table_iterator in range(3):
            time_sum = 0
            eng_time_param = [0,0,0,0]
            eng_win_counter = [0,0,0,0]
            eng_stalemate_counter = [0,0,0,0]
            f.write(str(aa[table_iterator])+' '+str(cc[table_iterator]) + "\n")
            for k1 in range(4):
                for k2 in range(k1+1,4):
                    print(k1,k2)
                    eng1 = ec.Engine(engine_list[k1])
                    eng2 = ec.Engine(engine_list[k2])

                    for i in range(3): #(100) ~17 - 102
                        moves_order = []

                        a = aa[table_iterator]
                        b = aa[table_iterator]
                        c = cc[table_iterator]
                        while True and len(moves_order) < 320:
                            start_time = time.time()
                            move = eng1.make_move(moves_order,a,b,c)
                            dt = (time.time() - start_time) * 1000
                            a -= dt
                            if move == "resign":
                                eng_win_counter[k2] += 1
                                print('')
                                break
                            moves_order.append(move)
                            print(moves_order[-1], end=" ")
                            
                            start_time = time.time()
                            move = eng2.make_move(moves_order,a,b,c)
                            dt = (time.time() - start_time) * 1000
                            b -= dt
                            if move == "resign":
                                eng_win_counter[k1] += 1
                                print('')
                                break
                            moves_order.append(move)
                            print(moves_order[-1], end=" ")
                        if len(moves_order)>=320:
                            eng_stalemate_counter[k1] += 1
                            eng_stalemate_counter[k2] += 1
                        print("End")
                    eng_time_param[k1] += eng1.get_time_for_test()
                    eng_time_param[k2] += eng2.get_time_for_test()
                    eng1.end()
                    eng2.end()
                if k1 == 3:
                    for i in range(4):
                        f.write(str(engine_list[i]) + " ")
                        f.write("Победы: " + str(eng_win_counter[i]) + " ")
                        f.write("Ничиьи: " +str(eng_stalemate_counter[i]) + "\n")
                time_sum += eng_time_param[k1]
            f.write(str(float('{:.3f}'.format(time_sum))) + "\n")
    f.close()