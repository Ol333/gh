import numpy as np
from scipy.stats import norm

import engine_connection as ec

class SomeAnalisisStuff(ec.Engine):
    def __init__(self, eng):
        self.eng = eng
        self.fspm = 0
        self.fbmc = 0
        self.sspm = 0
        self.sbmc = 0
        self.classificator = MovesClassificator()

    def moveDiffrence(self, start_pos, last_cp, move_count):
        move = start_pos.split(' ')[-1]
        start_pos = start_pos[:-len(move)]
        mov_cp = self.eng.cp_of_current_move(start_pos, move, depth=17)[0]
        
        if move_count % 2 == 0:
            temp_sign = 1
        else:
            temp_sign = -1
        print(temp_sign, end=' ')
        if move_count != 1:
            print(mov_cp, last_cp, last_cp + mov_cp)
            mov_cp_diff = last_cp + mov_cp
        else:
            mov_cp_diff = mov_cp
            print('-', mov_cp ,last_cp, '-')
        return mov_cp, mov_cp_diff

    def ver_raspr_rasn(self, fx, fy, n):
        sum = 0
        for m in range(-2*max(len(fx), len(fy)), 2*max(len(fx), len(fy))+1):
            if m in fy and n+m in fx:
                sum += fy[m]*fx[n+m]
        return sum

    def ferreira(self, first_pl_strength):
        hd1 = dict.fromkeys(range(min(first_pl_strength), max(first_pl_strength)+1))
        for q in hd1.keys():
            q_count = first_pl_strength.count(q)
            if q_count != 0:
                hd1[q] = float(q_count)/len(first_pl_strength)
            else:
                hd1[q] = 0
        hd_eng = {0:1}
        sum = 0
        for i in range(1, len(hd1) + 1):
            sum += self.ver_raspr_rasn(hd1, hd_eng, i)
        expected_score = 0.5 * self.ver_raspr_rasn(hd1, hd_eng, 0) + sum
        z = norm.ppf(expected_score)
        d = z * 200 * 2**(0.5)
        return round(d,2)

    def yamashita(self, pl_numb, mov_cp_diff):
        # среднее значение только проигрышей
        # можно реализовать обрезку 40 первых ходов и оценку разницы между двумя наилучшими ходами...
        
        if pl_numb == 0:
            res = self.fspm
            if mov_cp_diff < 0:
                res = round(((self.fspm * self.fbmc) + mov_cp_diff) / (self.fbmc + 1), 2)
            self.fspm = res
            self.fbmc += 1
        else:
            res = self.sspm
            if mov_cp_diff < 0:
                res = round(((self.sspm * self.sbmc) + mov_cp_diff) / (self.sbmc + 1), 2)
            self.sspm = res
            self.sbmc += 1
        return round(res*(-3148)+4620, 2)
    
    def yamashita_fp(self):
        # print('yamashita_fp', self.fspm)
        return str(round(self.fspm*(-3148)+4620,2))

    def yamashita_sp(self):
        # print('yamashita_sp', self.sspm)
        return str(round(self.sspm*(-3148)+4620, 2))

    def moveClass(self, cur_mov_cp, mov_cp_diff, start_pos):
        # найти cp за лучший рекомендуемый следующий ход
        temp_because_yaneoura_besit = self.eng.cp_of_next_move(start_pos, depth=17)
        if temp_because_yaneoura_besit[1] == -111111111:
            bst_mov = temp_because_yaneoura_besit[0]
            mov_cp = self.eng.cp_of_current_move(start_pos, bst_mov, depth=17)[0]
        else:
            bst_mov,mov_cp = temp_because_yaneoura_besit
            mov_cp = int(min(abs(mov_cp),10000)*np.sign(mov_cp))
        return (self.classificator.predict([mov_cp_diff, mov_cp-cur_mov_cp]), mov_cp)

class MovesClassificator:
    def __init__(self):
        pass

    def predict(self, X):
        if X[0] > 0 and X[1] < 0:
            return 'Отлично'
        elif X[0] > -10000 and X[1] < 10000:
            return 'Хорошо' 
        else:
            return 'Плохо'