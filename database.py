from psycopg2 import pool


class Database:
    __connection_pool = None

    @classmethod
    def initialise(cls,**kwargs):
        cls.__connection_pool = pool.SimpleConnectionPool(72,100,**kwargs)

    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls,connection):
        Database.__connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        Database.__connection_pool.closeall()


class CursorFromConnectionFromPool:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connection(self.connection)


def TabelMaken(tabelnaam, tabelformaat):
    with CursorFromConnectionFromPool() as cursor:
        cursor.execute('DROP TABLE IF EXISTS {s}'.format(s=tabelnaam,))
        cursor.execute('CREATE TABLE {m} AS TABLE {n} with NO DATA '.format(m=tabelnaam,n=tabelformaat,))
    #print("wordt er een lege tabel aangemaakt {:<34}".format(tabelnaam))


def save_to_table(table,*args):
        args = filter(None, args)
        for row in args:
            with CursorFromConnectionFromPool() as cursor:
                cursor.execute(
                    'INSERT INTO {t} VALUES ( {r} )'.format(t=table,r=row))

