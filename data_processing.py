import time
import subprocess
import rab_with_db as rwd
import shogi.KIF

# l = rwd.player_list()
# print(len(l))

# 66 yukitakahashi
l = rwd.players_kifu_list(66)[0]
# print(len(l[0]))
# print(l[0])

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

cmd = 'C:/Users/Olga/Downloads/Shogidokoro_with_engine/Kristallweizen/Kristallweizen-wcsc29-avx2'
process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# try:
#     outs, errs = process.communicate('usi\n'.encode(), timeout=15)
#     print(outs.decode('utf8'))
#     outs, errs = process.communicate('isready\n'.encode(), timeout=15)
#     print(outs.decode('utf8'))
#     outs, errs = process.communicate('usinewgame\n'.encode(), timeout=15)
#     print(outs.decode('utf8'))
#     for i in range(len(kif['moves'])):        
#         outs, errs = process.communicate(('position startpos moves' + ' '.join(kif['moves'][:i+1]) + '\n').encode(), timeout=15)
#         outs, errs = process.communicate('go infinite\n'.encode(), timeout=15)
#         time.sleep(10)
#         outs, errs = process.communicate('stop\n'.encode(), timeout=15)
#         print(outs.decode('utf8'))
# except subprocess.TimeoutExpired:
#     process.kill()
#     outs, errs = process.communicate()

# Tell engine to use the USI
process.stdin.write('usi\n'.encode())
process.stdin.flush()
while line := process.stdout.readline().decode('utf8'):
    if line == 'usiok\r\n':
        print(line, end='')
        break
# This is used to synchronize the engine with the GUI
process.stdin.write('isready\n'.encode())
process.stdin.flush()
time.sleep(1)
temp_line = process.stdout.readline().decode('utf8')
while temp_line != 'readyok\r\n':
    temp_line = process.stdout.readline().decode('utf8')
print('wtf')
# This is sent to the engine when the next search (started with position and go) will be from a different game.
process.stdin.write('usinewgame\n'.encode())
print('usinewgame')
# Set up the position described in sfenstring on the internal board and play the moves on the internal board.
for i in range(len(kif['moves'])):
    temp_str = 'position startpos moves ' + ' '.join(kif['moves'][:i+1]) + '\n'
    process.stdin.write(('position startpos moves ' + ' '.join(kif['moves'][:i+1]) + '\n').encode())
    process.stdin.flush()
    process.stdin.write('go infinite\n'.encode())
    process.stdin.flush()
    time.sleep(10)
    process.stdin.write('stop\n'.encode())
    process.stdin.flush()
    while line := process.stdout.readline().decode('utf8'):
        if line.find('bestmove') > -1:
            print(line, end='')
            break
time.sleep(1)
process.kill()