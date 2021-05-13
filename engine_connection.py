import time
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

if __name__ == '__main__':
    max_depth = 15
    time_of_work = []
    stalemate_list = [[],[],[],[]]
    engine_list = ["gikou","Kristallweizen-wcsc29-avx2","YaneuraOu_KPPT-tournament-clang++-avx2","nozomi"]
    eng_time_param = [[0]*max_depth, [0]*max_depth, [0]*max_depth, [0]*max_depth]

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

fig, ax = plt.subplots()

ax.set_title("Важный график зависимости времени размышлений от глубины поиска хода", fontsize=16)
ax.set_xlabel("время, потраченное движком на ходы в течение игры, с", fontsize=14)
ax.set_ylabel("глубина поиска лучшего хода", fontsize=14)
ax.grid(which="major",linewidth=1.2)
ax.plot(range(1,11),eng_time_param[0],label="gikou")
ax.plot(range(1,11),eng_time_param[1],label="Kristallweizen-wcsc29-avx2")
ax.plot(range(1,11),eng_time_param[2],label="YaneuraOu_KPPT-tournament-clang++-avx2")
ax.plot(range(1,11),eng_time_param[3],label="nozomi")
ax.legend()
ax.tick_params(which='major', length=10, width=1)

plt.show()

# if __name__ == '__main__':
#     time_of_work = []
#     f = open('new_output.txt', 'a')
#     engine_list = ["gikou","Kristallweizen-wcsc29-avx2","YaneuraOu_KPPT-tournament-clang++-avx2","nozomi"]
#     eng_time_param = [0,0,0,0]

#     for k1 in range(4):
#         for k2 in range(k1+1,4):
#             print(k1,k2)
#             eng1 = Engine(engine_list[k1])
#             eng2 = Engine(engine_list[k2])

#             for i in range(3):
#                 moves_order = []

#                 # a = 300000
#                 # b = 300000
#                 a = 0
#                 b = 0
#                 c = 100
#                 while True:
#                     start_time = time.time()
#                     move = eng1.make_move(moves_order,a,b,c)
#                     dt = time.time() - start_time
#                     a -= dt
#                     if move == "resign":
#                         f.write(eng1.get_adress() + " win\n")
#                         print('')
#                         eng1.not_end("win")
#                         eng2.not_end("lose")
#                         break
#                     moves_order.append(move)
#                     print(moves_order[-1], end=" ")
                    
#                     start_time = time.time()
#                     move = eng2.make_move(moves_order,a,b,c)
#                     dt = time.time() - start_time
#                     b -= dt
#                     if move == "resign":
#                         f.write(eng2.get_adress() + " win\n")
#                         print('')            
#                         eng1.not_end("lose")
#                         eng2.not_end("win")
#                         break
#                     moves_order.append(move)
#                     print(moves_order[-1], end=" ")

#                 print("End")
#             eng_time_param[k1] += eng1.get_time_for_test()
#             eng_time_param[k2] += eng2.get_time_for_test()
#             eng1.end()
#             eng2.end()
# for i in range(4):
#     f.write(str(i)+str(float('{:.3f}'.format(eng_time_param[i]))) + "\n")
# f.close()