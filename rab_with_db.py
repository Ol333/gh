# -*- coding: utf-8 -*-
import sqlite3

con = sqlite3.connect("shogi_db.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")

def player_check_add(login):
    # проверить на существование
    cur.execute(f"SELECT id FROM Player WHERE login='{login}'")
    for a in cur.fetchall():
        if a != None:
            a = a[0]
            return a
        else:
            break
    cur.execute("""INSERT into Player values
                    (null,?)""",(login,))
    con.commit()
    return cur.lastrowid

def player_del(login):
    cur.execute(f"DELETE FROM Player WHERE login='{login}'")
    con.commit()

def kifu_add(kifu):
    cur.execute("""INSERT into Kifu values
                    (null,?)""",(kifu,))
    con.commit()
    return cur.lastrowid

def kifu_del(id):
    cur.execute(f"DELETE FROM Kifu WHERE id={id}")
    con.commit()

def participation_add(player_id,kifu_id):
    cur.execute("""INSERT into Participation values
                    (null,?,?)""",(player_id,kifu_id))
    con.commit()
    return cur.lastrowid

def participation_del(id):
    cur.execute(f"DELETE FROM Participation WHERE id_Kifu='{id}'")
    con.commit()

def table_list(table_name):
    mas = []
    cur.execute("SELECT * FROM {}".format(table_name))
    for a in cur.fetchall():
        mas.append(a)
    return mas

def player_idbylogin(login):
  cur.execute(f"SELECT id FROM Player WHERE login='{login}'")
  for a in cur.fetchall():
    a = a[0]
    return a

def player_loginbyid(id):
  cur.execute(f"SELECT login FROM Player WHERE id='{id}'")
  for a in cur.fetchall():
    a = a[0]
    return a

def players_kifu_list(id):
    mas = []
    res = []
    cur.execute(f"SELECT id_Kifu FROM Participation WHERE id_Player={id}")
    for a in cur.fetchall():
        mas.append(a[0])
    for a in mas:
        cur.execute(f"SELECT kifu FROM Kifu WHERE id={a}")
        for aa in cur.fetchall():
            res.append(aa[0])
    return res

def move_add(kifu_id,numb,rec_cp,rec_pv,real_cp): #добавить всякое для таблицы Move
    cur.execute("""INSERT into Move values
                    (null,?,?,?,?,?)""",(kifu_id,numb,rec_cp,rec_pv,real_cp))
    con.commit()
    return cur.lastrowid

def get_cp(kifu_id,color):
    mas = []
    cur.execute(f"""SELECT recommended_move,recommended_evaluate,real_evaluate 
                    FROM Move
                    WHERE id_Kifu='{kifu_id}' AND number%2 = {color}""")
    for a in cur.fetchall():
        mas.append(a)
    return mas

# ##вывод всех таблиц
# def print_tabl():
#   cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
#   tables = cur.fetchall()
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
