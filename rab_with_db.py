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

def player_add(login):
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

def kifu_list():
    mas = []
    cur.execute("SELECT id,kifu FROM Kifu")
    temp = ''
    wrong_kifu = [633,638,1120,4497,4760,6552,7500,9201,9883,9884,9886,
    11173,12535,12961,13204,13705,16835,18186,25261,26205,26213,25261,
    26205,26213,29813,29814,29817,40767,40778,43680,55099]
    for a in cur.fetchall():
        if a[1] == temp or a[1] == '' or a[0] in wrong_kifu:
            mas.append(a[0])
            kifu_del(a[0])
            p_id_mas = participation_playerbykifu(a[0])
            participation_del(p_id_mas[0][0])
            participation_del(p_id_mas[1][0])
            if len(players_kifu_list(p_id_mas[0][1])) == 0:
                player_del(p_id_mas[0][1])
            if len(players_kifu_list(p_id_mas[1][1])) == 0:
                player_del(p_id_mas[1][1])
        temp = a[1]
    return mas

def participation_add(player_id,kifu_id):
    cur.execute("""INSERT into Participation values
                    (null,?,?)""",(player_id,kifu_id))
    con.commit()
    return cur.lastrowid

def participation_del(id):
    cur.execute(f"DELETE FROM Participation WHERE id='{id}'")
    con.commit()

def participation_playerbykifu(kifu_id):
  cur.execute(f"SELECT id,id_Player FROM Participation WHERE id_Kifu='{kifu_id}'")
  mas = []
  for a in cur.fetchall():
    mas.append((a[0],a[1]))
  return mas

def player_list():
    mas = []
    cur.execute("SELECT login FROM Player")
    for a in cur.fetchall():
        mas.append(a[0])
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