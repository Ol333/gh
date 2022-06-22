# -*- coding: utf-8 -*-
import sqlite3

class DbConnection:
    con = None
    cur = None

    def __init__(self,name):
        # con = sqlite3.connect("shogi_db.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        # self.con = sqlite3.connect("shogi_db (9).db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.con = sqlite3.connect(name, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.cur = self.con.cursor()
        self.cur.execute("PRAGMA foreign_keys = ON")

    def player_check_add(self,login):
        # проверить на существование
        self.cur.execute(f"SELECT id FROM Player WHERE login='{login}'")
        for a in self.cur.fetchall():
            if a != None:
                a = a[0]
                return a
            else:
                break
        self.cur.execute("""INSERT into Player values
                        (null,?)""",(login,))
        self.con.commit()
        return self.cur.lastrowid

    def player_del(self,login):
        self.cur.execute(f"DELETE FROM Player WHERE login='{login}'")
        self.con.commit()

    def kifu_add(self,kifu):
        self.cur.execute("""INSERT into Kifu values
                        (null,?)""",(kifu,))
        self.con.commit()
        return self.cur.lastrowid

    def kifu_del(self,id):
        self.cur.execute(f"DELETE FROM Kifu WHERE id={id}")
        self.con.commit()

    def participation_add(self,player_id,kifu_id):
        self.cur.execute("""INSERT into Participation values
                        (null,?,?)""",(player_id,kifu_id))
        self.con.commit()
        return self.cur.lastrowid

    def participation_del(self,id):
        self.cur.execute(f"DELETE FROM Participation WHERE id_Kifu='{id}'")
        self.con.commit()

    def table_list(self,table_name):
        mas = []
        self.cur.execute("SELECT * FROM {}".format(table_name))
        for a in self.cur.fetchall():
            mas.append(a)
        return mas

    def player_idbylogin(self,login):
        self.cur.execute(f"SELECT id FROM Player WHERE login='{login}'")
        for a in self.cur.fetchall():
            a = a[0]
            return a

    def player_loginbyid(self,id):
        self.cur.execute(f"SELECT login FROM Player WHERE id='{id}'")
        for a in self.cur.fetchall():
            a = a[0]
            return a

    def players_kifu_list(self,id,li):
        mas = []
        res = []
        self.cur.execute(f"SELECT id_Kifu,id_Player FROM Participation WHERE id_Player={id}")
        for a in self.cur.fetchall():
            mas.append(a)
        if li:
            for a in mas:
                self.cur.execute(f"SELECT kifu FROM Kifu WHERE id={a[0]}")
                for aa in self.cur.fetchall():
                    res.append(aa[0])
            return res
        else:
            return mas

    def move_add(self,kifu_id,numb,rec_cp,rec_pv,real_cp): #добавить всякое для таблицы Move
        self.cur.execute("""INSERT into Move values
                        (null,?,?,?,?,?)""",(kifu_id,numb,rec_pv,rec_cp,real_cp))
        self.con.commit()
        return self.cur.lastrowid

    def get_cp(self,kifu_id,color):
        mas = []
        self.cur.execute(f"""SELECT recommended_move,recommended_evaluate,real_evaluate 
                        FROM Move
                        WHERE id_Kifu='{kifu_id}' AND number%2 = {color}""")
        for a in self.cur.fetchall():
            mas.append(a)
        return mas

    def save_game(self, pl1, pl2, moves):
        pl1 = self.player_check_add(pl1)
        pl2 = self.player_check_add(pl2)
        kif_id = self.kifu_add('')
        print(pl1, pl2, kif_id)
        part1 = self.participation_add(pl1, kif_id)
        part2 = self.participation_add(pl2, kif_id)
        for m in moves:
            self.move_add(kif_id, m[0], m[1], m[2], m[3])

    def pl_and_kifu(self, pl_id):
        mas = []
        res = []
        self.cur.execute(f"SELECT id_Kifu,id_Player FROM Participation WHERE id_Player={pl_id}")
        for a in self.cur.fetchall():
            mas.append(a)
        for a in mas:
            res.append([])
            self.cur.execute(f"SELECT kifu FROM Kifu WHERE id={a[0]}")
            for aa in self.cur.fetchall():
                res[-1].append(aa[0])
                res[-1].append(a[0])
            self.cur.execute(f"SELECT id_Player FROM Participation WHERE id_Kifu={a[0]}")
            for aaa in self.cur.fetchall():
                res[-1].append(aaa[0])
        return res

    def get_kifu(self, id):
        res = []
        self.cur.execute(f"SELECT kifu FROM Kifu WHERE id={id}")
        for aa in self.cur.fetchall():
            res.append(aa[0])
        return res

    # ##вывод всех таблиц
    # def print_tabl(self):
    #   self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #   tables = self.cur.fetchall()
    #   for table_name in tables:
    #     table_name = table_name[0]
    #     table = pd.read_sql_query("SELECT * from %s" % table_name, con)
    #     print(table)
    #
    # ##print_tabl()
    # ##mkFlag_upd(3)
    # ##thiStat_upd(2,'ждет первого обжига')
    # ##user_add('',0,'qwerty')
    # ##print(mk_list())
