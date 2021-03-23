import time
import subprocess

import shogi.KIF

import rab_with_db as rwd

# l = rwd.player_list()
# print(len(l))

# 66 yukitakahashi
l = rwd.players_kifu_list(66)[0]

kif = shogi.KIF.Parser.parse_str(l)[0]
print(kif['names'][shogi.BLACK])
print(kif['names'][shogi.WHITE])
print(kif['moves']) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
print(kif['win'])

l = l.split('\n')
date = l[1][5:]
conditions = (l[3][5:], l[4][4:])
print(date)
print(conditions)

################################################################################################

# Shogidokoro_with_engine/Kristallweizen/Kristallweizen-wcsc29-avx2'
# Lesserkai"
cmd = "gikou"
f = open('output_{}.txt'.format(str(float('{:.3f}'.format(time.time())))), 'w')

process = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Tell engine to use the USI
process.stdin.write('usi\r\n'.encode())
process.stdin.flush()
while line_usi := process.stdout.readline().decode('utf8'):
    if line_usi == 'usiok\r\n':
        print(line_usi, end='')
        break

# This is used to synchronize the engine with the GUI
process.stdin.write('isready\r\n'.encode())
process.stdin.flush()
while line_usi := process.stdout.readline().decode('utf8'):
    if line_usi == 'readyok\r\n':
        print(line_usi, end='')
        break

# # # option
# process.stdin.write('setoption name WriteDebugLog value true\r\n'.encode())
# process.stdin.flush()  

# This is sent to the engine when the next search (started with position and go) will be from a different game.
process.stdin.write('usinewgame\r\n'.encode())
process.stdin.flush()

start_time = time.time()
start_pos = ""
# Set up the position described in sfenstring on the internal board and play the moves on the internal board.
for i in range(len(kif['moves'])):
    # найти cp за текущий ход
    temp_str = 'position startpos moves ' + start_pos + '\r\n'
    print(start_pos.count(' '))
    f.write(str(start_pos.count(' ')) + ") поиск cp за реальный ход........ " + str(kif['moves'][i]))
    process.stdin.write((temp_str).encode())
    process.stdin.flush()
    process.stdin.write(("go infinite searchmoves " + kif['moves'][i] + '\r\n').encode())
    process.stdin.flush()
    time.sleep(10)
    process.stdin.write('stop\r\n'.encode())
    process.stdin.flush()
    out_max_res = -111111111
    while line_end1 := process.stdout.readline().decode('utf8'):
        if line_end1.find('bestmove') > -1:
            f.write(' /// ' + str(out_max_res) + '\n')
            break
        else:
            temp = line_end1.split(' ')
            if i == 1:
                f.write(line_end1)
            # # либо считать среднее, либо выбирать НаИбОлЬшЕе
            if 'cp' in temp:
                temp_max = int(temp[temp.index('cp') + 1])
                if out_max_res < temp_max:
                    out_max_res = temp_max
            else:
                f.write(line_end1)
    # найти cp за лучший следующий ход
    start_pos += ' ' + kif['moves'][i]
    temp_str = 'position startpos moves ' + start_pos + '\r\n'
    print(start_pos.count(' '))
    f.write(str(start_pos.count(' ')) + ') ' + str(start_pos[-4:]) + " лучший следующий ход........")
    process.stdin.write((temp_str).encode())
    process.stdin.flush()
    process.stdin.write('go infinite\r\n'.encode())
    process.stdin.flush()
    time.sleep(10)
    process.stdin.write('stop\r\n'.encode())
    process.stdin.flush()
    out_variants = {}
    while line_end2 := process.stdout.readline().decode('utf8'):
        if line_end2.find('bestmove') > -1:
            # print(line_end2.replace('\r\n',''), end=' ')
            best_move = line_end2.split(' ')[1].replace('\r\n','')
            f.write(" /// " + str(best_move) + ' ' + str(out_variants[best_move]) + '\n')
            break
        else:
            # # либо считать среднее, либо выбирать НаИбОлЬшЕе
            temp = line_end2.split(' ')
            if i == 1:
                f.write(line_end2)
            # print(temp)
            if 'cp' in temp and 'pv' in temp:
                temp_cp = temp[temp.index('cp') + 1]
                temp_pv = temp[temp.index('pv') + 1].replace('\r\n','')
                if (temp_pv in out_variants and out_variants[temp_pv] > temp_cp) or (not temp_pv in out_variants):
                    out_variants[temp_pv] = temp_cp
            else:
                f.write(line_end2)
process.kill()
res_time = time.time() - start_time
res_min = str(res_time // 60)
res_sec = str(float('{:.3f}'.format(res_time % 60)))
f.write(res_min + " minutes, " + res_sec + " seconds")
f.close()