import asyncpg
import asyncio

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

    async def create_pool(self):
        try:
            self.connection_pool = await asyncpg.create_pool(
                min_size=self.minconn,
                max_size=self.maxconn,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.dbname
            )
            print("Connection pool created successfully")
        except Exception as e:
            print(f"Error creating connection pool: {e}")

    async def get_connection(self):
        if self.connection_pool is None:
            await self.create_pool()
        try:
            return await self.connection_pool.acquire()
        except Exception as e:
            print(f"Error getting connection from pool: {e}")

    async def release_connection(self, connection):
        try:
            await self.connection_pool.release(connection)
            # print("Connection released successfully")
        except Exception as e:
            print(f"Error releasing connection to pool: {e}")

    async def close_all_connections(self):
        try:
            await self.connection_pool.close()
            # print("All connections closed successfully")
        except Exception as e:
            print(f"Error closing all connections: {e}")

