import sqlite3 as sql
from getpass import getpass


class DBInterface:
  def __init__(self, sqlite_db):
    self.sqlite_db = sqlite_db

  def run_closing_query(self, query, params=(), fetch="all"):
    return self.__run_closing_query(query, params=params, fetch="all")

  def __run_closing_query(self, query, params=(), fetch="all"):
    results = None
    with sql.connect(self.sqlite_db) as con:
      cur = con.cursor()
      print(params)
      print(type(params))
      cur.execute(query, tuple(params))
      if (fetch == "all"):
        results = cur.fetchall()
    return results

def populate(usernames):
  dbi       = DBInterface("users.db")
  statement = """SELECT username FROM user WHERE username = ?"""
  for username in usernames:
    user_in_db = len(dbi.run_closing_query(statement, (username, ), fetch="all")) > 0
    if (not user_in_db):
      # add user
      print("Add user in here")
  pass

def get_password():
  plaintext  = getpass()
  #ciphertext =
  return plaintext 

def do_login(username):
  dbi       = DBInterface("users.db")
  password  = get_password()
  statement = """SELECT username FROM user WHERE username = ? AND password = ?"""
  params    = (username, password)

  matches = dbi.run_closing_query(statement, params=params)
  if (len(matches) < 1): 
    return False
  return True
