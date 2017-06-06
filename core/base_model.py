import os
import sqlite3

DB_FILE_NAME = 'app.db'


def get_sqlscript(sql_file):
    """
    Geting file for for papulate db
    :sql_file: name file with sql script
    """
    with open(sql_file) as f:
        sql = f.read()
        return sql


def db_create(dbfile):
    """
    Created db for application or tetsting
    :dbfile: string - db file name
    """
    try:
        con = sqlite3.connect(dbfile)
        cur = con.cursor()
        sql = get_sqlscript('db_populate.sql')
        if sql:
            cur.executescript(sql)
    except sqlite3.DatabaseError as e:
        print("DBError", e)
        raise e
    else:
        con.commit()
    finally:
        if cur:
            cur.close()
        if con:
            con.close()


class DB():
    """
    Wrapper for sqlite3.connect

    Should use a singleton pattern, but not critical for this application.
    Implements a context manager interface
    """
    def __init__(self):
        if not os.path.exists(DB_FILE_NAME):
            db_create(DB_FILE_NAME)
        self.con = sqlite3.connect(DB_FILE_NAME)

    def raw_sql(self, sql):
        """
        Wrapp for sqlite3.connect.cursor
        :return: - dictionary of result fetchall() and lastrowid if there is
        """
        cur = self.con.cursor()
        try:
            cur.execute(sql)
            data = cur.fetchall()
            self.con.commit()
            return {'data': data, 'lastid': cur.lastrowid}
        except sqlite3.DatabaseError as e:
            print("DBError", e)
            raise e
        finally:
            cur.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.con:
            self.con.close()
