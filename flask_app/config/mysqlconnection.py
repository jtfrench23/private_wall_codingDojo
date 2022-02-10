import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        connection= pymysql.connect(host='localhost',
                                    user='root',
                                    password='frenchfrench',
                                    db=db,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor,
                                    autocommit = True)
        self.connection=connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try: 
                query=cursor.mogrify(query, data)
                print("running query:", query)

                cursor.execute(query,data)
                if query.lower().find("insert")>=0:
                    #insert queries will return number of row
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select")>=0:
                    result=cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
            except Exception as e:
                print("something went wrong", e)
                return False
            finally:
                self.connection.close()
    

def connectToMySQL(db):
    return MySQLConnection(db)

