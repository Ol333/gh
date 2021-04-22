import time
import subprocess

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
        self.process = subprocess.Popen(eng_adress, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.con = Connector()
        self.con.send_command(self.process,"usi","usiok")
        self.con.send_command(self.process,"isready","readyok")
        # # # option
        # process.stdin.write('setoption name WriteDebugLog value true\r\n'.encode())
        self.con.send_command_without_output(self.process,"usinewgame")
    
    def make_move(self,moves_order,a,b,c):
        self.con.send_command_without_output(self.process,"position startpos moves " + ' '.join(moves_order))
        temp_str = "go btime {0} wtime {1} byoyomi {2}".format(a,b,c)
        out = self.con.send_command_bestmove(self.process,temp_str)
        return out
        
    def not_end(self,res):
        self.con.send_command_without_output(self.process,"gameover "+res)
    
    def end(self):
        self.con.send_command_without_output(self.process,"quit")
        self.process.kill()
        self.process.wait()


if __name__ == '__main__':
    f = open('new_output.txt', 'a')

    eng1 = Engine("gikou")
    eng2 = Engine("YaneuraOu_KPPT-tournament-clang++-avx2")

    for i in range(10):
        moves_order = []

        # a = 300000
        # b = 300000
        a = 0
        b = 0
        c = 100
        while True:
            start_time = time.time()
            move = eng1.make_move(moves_order,a,b,c)
            dt = time.time() - start_time
            a -= dt
            if move == "resign":
                f.write("eng1 win\n")
                print('')
                eng1.not_end("win")
                eng2.not_end("lose")
                break
            moves_order.append(move)
            print(moves_order[-1], end=" ")
            
            start_time = time.time()
            move = eng2.make_move(moves_order,a,b,c)
            dt = time.time() - start_time
            b -= dt
            if move == "resign":
                f.write("eng2 win\n")
                print('')            
                eng1.not_end("lose")
                eng2.not_end("win")
                break
            moves_order.append(move)

            print(moves_order[-1], end=" ")
        print("End")
    eng1.end()
    eng2.end()
    f.close()