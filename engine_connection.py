import time
import math
import subprocess
import matplotlib.pyplot as plt

class Connector:
    def send_command(self, process, command, expectation):
        process.stdin.write((command+'\r\n').encode())
        process.stdin.flush()
        res = ""
        while line_usi := process.stdout.readline().decode('utf8'):
            if line_usi == (expectation+'\r\n'):
                return line_usi
        return res

    def send_command_without_output(self, process, command):
        process.stdin.write((command+'\r\n').encode())
        process.stdin.flush()
    
    def send_command_bestmove(self, process, command):
        process.stdin.write((command+'\r\n').encode())
        process.stdin.flush()
        res = ""
        while line_usi := process.stdout.readline().decode('utf8'):
            if line_usi.find("bestmove") != -1:
                return line_usi.split(' ')[1].replace("\r\n",'')
            else:
                res += line_usi
        return res
    
    def get_max_bestmove(self,process):
        out_max_res = -111111111
        while line_end := process.stdout.readline().decode('utf8'):
            if line_end.find('bestmove') > -1:
                return out_max_res
            else:
                temp = line_end.split(' ')
                if 'cp' in temp:
                    temp_max = int(temp[temp.index('cp') + 1])
                    if out_max_res < temp_max:
                        out_max_res = temp_max
        print("вообще-то сюда не должно приходить...")
        return out_max_res

    def get_best_move(self,process):
        out_variants = {}
        while line_end := process.stdout.readline().decode('utf8'):
            if line_end.find('bestmove') > -1:
                best_move = line_end.split(' ')[1].replace('\r\n','')
                return (best_move,out_variants[best_move])
            else:
                temp = line_end.split(' ')
                if 'cp' in temp and 'pv' in temp:
                    temp_cp = temp[temp.index('cp') + 1]
                    temp_pv = temp[temp.index('pv') + 1].replace('\r\n','')
                    if (temp_pv in out_variants and out_variants[temp_pv] > temp_cp) or (not temp_pv in out_variants):
                        out_variants[temp_pv] = temp_cp
        print("вообще-то сюда не должно приходить 2...")
        return 0

class Engine:
    def __init__(self,eng_adress):
        self.Adress = eng_adress
        self.Time_for_test = 0
        self.Time_for_test_depth = 0
        self.process = subprocess.Popen(eng_adress, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.con = Connector()
        self.con.send_command(self.process,"usi","usiok")
        self.con.send_command(self.process,"isready","readyok")
        # # # option
        # process.stdin.write('setoption name WriteDebugLog value true\r\n'.encode())
        self.con.send_command_without_output(self.process,"usinewgame")
    
    def get_adress(self):
        return self.Adress
    
    def get_time_for_test(self):
        return self.Time_for_test

    def get_time_for_test_depth(self):
        return self.Time_for_test_depth

    def make_move(self,moves_order,a,b,c):        
        self.con.send_command_without_output(self.process,"position startpos moves " + ' '.join(moves_order))
        temp_str = "go btime {0} wtime {1} byoyomi {2}".format(a,b,c)
        temp_time = time.time()
        out = self.con.send_command_bestmove(self.process,temp_str)
        self.Time_for_test += time.time() - temp_time
        return out
        
    def not_end(self,res):
        self.con.send_command_without_output(self.process,"gameover "+res)
    
    def end(self):
        self.con.send_command_without_output(self.process,"quit")
        self.process.kill()
        self.process.wait()

    def make_certain_depth_move(self,moves_order,depth):        
        self.con.send_command_without_output(self.process,"position startpos moves " + ' '.join(moves_order))
        temp_str = "go depth {0} btime {1} wtime {1} byoyomi {2}".format(depth,0,100000000)
        temp_time = time.time()
        out = self.con.send_command_bestmove(self.process,temp_str)
        self.Time_for_test_depth += time.time() - temp_time
        return out

    def cp_of_current_move(self,start_pos,move):
        print(start_pos.count(' '))
        position_str = 'position startpos moves ' + start_pos + '\r\n'
        self.con.send_command_without_output(self.process,position_str)
        go_str = "go infinite searchmoves " + move + '\r\n'
        self.con.send_command_without_output(self.process,go_str)
        time.sleep(10)
        stop_str = 'stop\r\n'
        self.con.send_command_without_output(self.process,stop_str)
        # # выбираем наибольшее (можно попробовать среднее)
        return self.con.get_max_bestmove(self.process)        
    
    def cp_of_next_move(self,start_pos):
        print(start_pos.count(' '))
        position_str = 'position startpos moves ' + start_pos + '\r\n'
        self.con.send_command_without_output(self.process,position_str)
        go_str = 'go infinite\r\n'
        self.con.send_command_without_output(self.process,go_str)
        time.sleep(10)
        stop_str = 'stop\r\n'
        self.con.send_command_without_output(self.process,stop_str)
        # # выбираем наибольшее (можно попробовать среднее)
        return self.con.get_best_move(self.process)

if __name__ == '__main__':
    max_depth = 8
    time_of_work = []
    stalemate_list = [[],[],[],[]]
    engine_list = ["gikou","Kristallweizen-wcsc29-avx2","YaneuraOu_KPPT-tournament-clang++-avx2","nozomi"]
    eng_time_param = [[0]*max_depth, [0]*max_depth, [0]*max_depth, [0]*max_depth]
    counter_of_moves = []
    for i in range(max_depth):
        counter_of_moves.append([0,0])

    for depth_counter in range(max_depth):
        for k1 in range(4):
            for k2 in range(k1+1,4):
                print(k1,k2)
                eng1 = Engine(engine_list[k1])
                eng2 = Engine(engine_list[k2])

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
        for j in range(max_depth):
            count = max_depth
            if j in stalemate_list[i]:
                count -= stalemate_list[i].count(j)
            eng_time_param[i][j] = eng_time_param[i][j] / count

    f = open('new_output.txt', 'w')
    for i in range(4):
        f.write(str(i)+"\n")
        for j in range(max_depth):
            f.write(str(float('{:.3f}'.format(eng_time_param[i][j]))) + "\n")
    time_mas_labels = []
    for i in range(max_depth):
        counter_of_moves[i] = counter_of_moves[i][0]/counter_of_moves[i][1]
        time_mas_labels.append(counter_of_moves[i])
        f.write("среднее время "+str(i)+' - '+str(counter_of_moves[i])+'\n')
        counter_of_moves[i] = math.log(counter_of_moves[i],30)
    f.close()
    
    fig, ax = plt.subplots()

    ax.set_title("Важный график зависимости времени размышлений от глубины поиска хода", fontsize=16)
    ax.set_xlabel("время, потраченное движком на ходы в течение игры, с", fontsize=14)
    ax.set_ylabel("глубина поиска лучшего хода", fontsize=14)
    ax.grid(which="major",linewidth=1.2)
    ax.plot(range(1,max_depth+1),eng_time_param[0],label="gikou")
    ax.plot(range(1,max_depth+1),eng_time_param[1],label="Kristallweizen-wcsc29-avx2")
    ax.plot(range(1,max_depth+1),eng_time_param[2],label="YaneuraOu_KPPT-tournament-clang++-avx2")
    ax.plot(range(1,max_depth+1),eng_time_param[3],label="nozomi")
    rect = ax.bar(range(1,max_depth+1),counter_of_moves,0.9,label='Общее количество ходов',color=["#FFF9CD"])
    ax.bar_label(rect,time_mas_labels,padding=3)
    ax.legend()
    ax.tick_params(which='major', length=10, width=1)

    plt.show()

# if __name__ == '__main__':
#     time_of_work = []
#     f = open('new_output_2ris_test18.txt', 'a')
#     engine_list = ["gikou","Kristallweizen-wcsc29-avx2","YaneuraOu_KPPT-tournament-clang++-avx2","nozomi"]

#     aa = list(map(lambda x:x*1000,[1500,900,300]))
#     cc = list(map(lambda x:x*1000,[0,5,10]))

#     time_sum = 0

#     for table_iterator in range(3):
#         eng_time_param = [0,0,0,0]
#         eng_win_counter = [0,0,0,0]
#         eng_stalemate_counter = [0,0,0,0]
#         f.write(str(aa[table_iterator])+' '+str(cc[table_iterator]) + "\n")
#         for k1 in range(4):
#             for k2 in range(k1+1,4):
#                 print(k1,k2)
#                 eng1 = Engine(engine_list[k1])
#                 eng2 = Engine(engine_list[k2])

#                 for i in range(3): #(100) ~17 - 102
#                     moves_order = []

#                     a = aa[table_iterator]
#                     b = aa[table_iterator]
#                     c = cc[table_iterator]
#                     while True and len(moves_order) < 320:
#                         start_time = time.time()
#                         move = eng1.make_move(moves_order,a,b,c)
#                         dt = time.time() - start_time
#                         a -= dt
#                         if move == "resign":
#                             eng_win_counter[k1] += 1
#                             print('')
#                             eng1.not_end("win")
#                             eng2.not_end("lose")
#                             break
#                         moves_order.append(move)
#                         print(moves_order[-1], end=" ")
                        
#                         start_time = time.time()
#                         move = eng2.make_move(moves_order,a,b,c)
#                         dt = time.time() - start_time
#                         b -= dt
#                         if move == "resign":
#                             eng_win_counter[k2] += 1
#                             print('')            
#                             eng1.not_end("lose")
#                             eng2.not_end("win")
#                             break
#                         moves_order.append(move)
#                         print(moves_order[-1], end=" ")
#                     if len(moves_order)>=320:
#                         eng_stalemate_counter[k1] += 1
#                         eng_stalemate_counter[k2] += 1
#                     print("End")
#                 eng_time_param[k1] += eng1.get_time_for_test()
#                 eng_time_param[k2] += eng2.get_time_for_test()
#                 eng1.end()
#                 eng2.end()
#             for i in range(4):
#                 f.write(str(engine_list[i]) + " ")
#                 f.write("Победы: " + str(eng_win_counter[i]) + "")
#                 f.write("Ничиьи: " +str(eng_stalemate_counter[i]) + "\n")
#             time_sum += eng_time_param[k1]
#         f.write(str(float('{:.3f}'.format(time_sum))) + "\n")
# f.close()