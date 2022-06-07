import shogi.KIF

class Kifu_translator:
    figures_list = ['歩', '王','玉', '飛', '角', '金', '銀', '桂', '香', '龍', '馬', '全', '圭', '杏', 'と']

    def __init__(self):
        self.board = shogi.Board()
        self.movesSequence = ''

    def posToDesk(self, s):
        if s != '':
            self.board.push(shogi.Move.from_usi(s))
            self.movesSequence += ' ' + s
        res = []
        res.append([])
        desk = self.board.kif_str().split('\n')[3:12]
        for i in range(len(desk)):
            desk[i] = desk[i][1:-2] 
        for i in range(len(desk)):
            k = 0
            j = 0
            while k < len(desk[i]):
                if desk[i][k] == 'v':
                    res[0].append([1,j,i,desk[i][k+1]])
                    k += 2
                    j += 1
                elif desk[i][k] == '・':
                    k += 1
                    j += 1
                elif desk[i][k] in self.figures_list:
                    res[0].append([0,j,i,desk[i][k]])
                    k += 1
                    j += 1
                else:
                    k += 1
        res.append(self.board.kif_str().split('\n')[0].split('：')[1].split('\u3000')[1:])
        res.append(self.board.kif_str().split('\n')[-1].split('：')[1].split('\u3000')[1:])
        return res

    def addMove(self, s):
        print('move', s)
        print('is legal move:',shogi.Move.from_usi(s) in self.board.legal_moves)
        self.board.push_usi(s)
        # print(self.board.kif_str())
        print('is stalemate:', self.board.is_stalemate())
        print('is mate:', self.board.is_game_over())

    def getBoard(self):
        # return self.board.sfen()
        return self.movesSequence