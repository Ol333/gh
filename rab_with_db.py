# -*- coding: utf-8 -*-
import sqlite3

con = sqlite3.connect("shogi_db.db")
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
    cur.execute(f"DELETE FROM Participation WHERE id='{id}'")
    con.commit()

def player_list():
    mas = []
    cur.execute("SELECT * FROM Player")
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