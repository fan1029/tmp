import psycopg2
from psycopg2 import pool
from serviceConfig import POSTGRES_DB, POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT

class PostgresConnectionPool:


    def __init__(self, minconn, maxconn, dbname, user, password, host, port):
        self.minconn = minconn
        self.maxconn = maxconn
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection_pool = None

    def create_pool(self):
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                self.minconn,
                self.maxconn,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.dbname
            )
        except Exception as e:
            print(f"Error creating connection pool: {e}")

    def get_connection(self):
        if self.connection_pool is None:
            self.create_pool()
        try:
            return self.connection_pool.getconn()
        except Exception as e:
            print(f"Error getting connection from pool: {e}")

    def release_connection(self, connection):
        try:
            self.connection_pool.putconn(connection)
        except Exception as e:
            print(f"Error releasing connection to pool: {e}")

    def close_all_connections(self):
        try:
            self.connection_pool.closeall()
        except Exception as e:
            print(f"Error closing all connections: {e}")


# 写一个上面数据库连接类的上下文管理类
pool1= PostgresConnectionPool(2, 300, POSTGRES_DB, POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT)
class PostgresConnectionContextManager:
    def __init__(self):
        self.pool = pool1
        self.conn = None

    def __enter__(self):
        self.conn = self.pool.get_connection()
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.pool.release_connection(self.conn)


# # Example usage
if __name__ == "__main__":
    # poolDev = PostgresConnectionPool(1, 5, "dev", "postgres", "123456", "localhost", "5432")
    # p2 = PostgresConnectionPool(1, 5, "dev", "postgres", "123456", "localhost", "5432")
    # print(poolDev is p2)
    with PostgresConnectionContextManager() as cursor:
        cursor.execute("SELECT row_to_json(asset) FROM asset")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    # conn = pool.get_connection()
    # cursor = conn.cursor()
    # cursor.execute("SELECT row_to_json(asset) FROM asset")
    # # postgres将结果以json返回
    #
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    # pool.release_connection(conn)
    # pool.close_all_connections()
