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

# cmd = 'C:/Users/Olga/Downloads/Shogidokoro_with_engine/Kristallweizen/Kristallweizen-wcsc29-avx2'
cmd = "C:/Users/Olga/Downloads/LesserkaiSrc/LesserkaiSrc/x64/Debug/Lesserkai"

process = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Tell engine to use the USI
process.stdin.write('usi\r\n'.encode())
process.stdin.flush()
while line_usi := process.stdout.readline().decode('utf8'):
    if line_usi == 'usiok\r\n':
        print(line_usi, end='')
        break

# # # option
# process.stdin.write('setoption name WriteDebugLog value true\r\n'.encode())
# process.stdin.flush()  

# This is sent to the engine when the next search (started with position and go) will be from a different game.
process.stdin.write('usinewgame\r\n'.encode())
process.stdin.flush()
print('usinewgame end')

# Set up the position described in sfenstring on the internal board and play the moves on the internal board.
for i in range(len(kif['moves'])):
    temp_str = 'position startpos moves ' + ' '.join(kif['moves'][:i+1]) + '\r\n'
    print(temp_str[:-2], " ход........ ", end="")
    process.stdin.write(('position startpos moves ' + ' '.join(kif['moves'][:i+1]) + '\r\n').encode())
    process.stdin.flush()
    process.stdin.write('go infinite\r\n'.encode())
    process.stdin.flush()
    time.sleep(10)
    process.stdin.write('stop\r\n'.encode())
    process.stdin.flush()
    out_variants = {}
    while line_end := process.stdout.readline().decode('utf8'):
        if line_end.find('bestmove') > -1:
            print(line_end.replace('\r\n',''), end='')
            print('///',out_variants[line_end.split(' ')[-1].replace('\r\n','')])
            break
        else:
            temp = line_end.split(' ')
            if temp[1] == 'time':
                # либо считать среднее, либо выбирать наибольшее
                if 'depth' in temp:
                    out_variants[temp[11].replace('\r\n','')] = temp[9]
                else:
                    out_variants[temp[11].replace('\r\n','')] = temp[7]
process.kill()