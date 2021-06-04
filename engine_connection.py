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
        
    def not_end(self,res): # необязательная команда
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