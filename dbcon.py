import mysql.connector

# def getdbconn():
#         #conn_pool = psycopg2.pool.SimpleConnectionPool(1, 20,user = "postgres",password = "root",host = "127.0.0.1",port = "5432",database = "happdev")
#         #conn_pool = mysql.connector.connect(host="127.0.0.1", user="root", password="",database="macrocosmic",autocommit=True)
#         conn_pool = mysql.connector.connect(host="localhost", user="root",password="Radha@1234",database="shopifydb",autocommit=True)
#         if(conn_pool):
#
#             return conn_pool


#
# def mycus():
#     '''
#     this data is from config file where all credential for mysql connection is their
#     '''
#
#     mydb = mysql.connector.connect(host="188.166.247.24", user="root", passwd="DB0dataplayer", database="shopifydb")
#     return mydb


def mycus():
    '''
    this data is from config file where all credential for mysql connection is their
    '''

    mydb = mysql.connector.connect(host="localhost", user="root", passwd="Radha@1234", database="shopifydb")
    return mydb
