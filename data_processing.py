import time
import subprocess
# from os import startfile

# from psutil import process_iter
import psutil
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

cmd = 'C:/Users/Olga/Downloads/Shogidokoro_with_engine/Kristallweizen/Kristallweizen-wcsc29-avx2'
# a = startfile(cmd)

# time.sleep(2)
# print(a)

# for proc in process_iter():
#     if proc.name() == cmd.split("/")[-1]:
#         proc.kill()

process = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Tell engine to use the USI
process.stdin.write('usi\r\n'.encode())
process.stdin.flush()
while line_usi := process.stdout.readline().decode('utf8'):
    if line_usi == 'usiok\r\n':
        print(line_usi, end='')
        break

# # option
process.stdin.write('setoption name WriteDebugLog value true\r\n'.encode())
process.stdin.flush()
# process.stdin.write('setoption name USI_Ponder value true\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name USI_Hash value 256\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name Threads value 4\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name Hash value 16\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name MultiPV value 1\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name SkillLevel value 20\r\n'.encode())
# process.stdin.flush()
# # process.stdin.write('setoption name WriteDebugLog value false\r\n'.encode())
# # process.stdin.flush()
# process.stdin.write('setoption name NetworkDelay value 120\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name NetworkDelay2 value 1120\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name MinimumThinkingTime value 2000\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name SlowMover value 100\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name MaxMovesToDraw value 0\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name DepthLimit value 0\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name NodesLimit value 0\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name Contempt value 2\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name ContemptFromBlack value false\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name EnteringKingRule value CSARule27\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name EvalDir value eval\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name NarrowBook value false\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name BookMoves value 16\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name BookIgnoreRate value 0\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name BookFile value standard_book.db\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name BookDir value book\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name BookEvalDiff value 30\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name BookEvalBlackLimit value 0\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name BookEvalWhiteLimit value -140\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name BookDepthLimit value 16\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name BookOnTheFly value false\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name ConsiderBookMoveCount value false\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name PvInterval value 300\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name ResignValue value 99999\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name nodestime value 0\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name Param1 value 0\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name Param2 value 0\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name ConsiderationMode value false\r\n'.encode())
# process.stdin.flush()
# process.stdin.write('setoption name OutputFailLHPV value true\r\n'.encode())
# process.stdin.flush()

# This is used to synchronize the engine with the GUI
process.stdin.write('isready\r\n'.encode())
process.stdin.flush()
# while process.stdout.
time.sleep(2)
temp_line = process.stdout.readline().decode('utf8')
while temp_line != 'readyok\r\n':
    time.sleep(2)
    print(temp_line)
    temp_line = process.stdout.readline().decode('utf8')
print('isready end')
# process.stdout.flush()

# This is sent to the engine when the next search (started with position and go) will be from a different game.
process.stdin.write('usinewgame\r\n'.encode())
process.stdin.flush()
print('usinewgame end')

# Set up the position described in sfenstring on the internal board and play the moves on the internal board.
for i in range(len(kif['moves'])):
    temp_str = 'position startpos moves ' + ' '.join(kif['moves'][:i+1]) + '\r\n'
    print(temp_str)
    process.stdin.write(('position startpos moves ' + ' '.join(kif['moves'][:i+1]) + '\r\n').encode())
    # process.stdin.flush()
    print('pos end')
    process.stdin.write('go infinite\r\n'.encode())
    print('go end')
    # process.stdin.flush()
    time.sleep(10)
    process.stdin.write('stop\r\n'.encode())
    print('stop end')
    process.stdin.flush()
    while line_end := process.stdout.readline().decode('utf8'):
        print(line_end)
        if line_end.find('bestmove') > -1:
            print(line_end, end='')
            break

process.kill()