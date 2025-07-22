class DBconnector:
    def __init__(self, engine_name, user, password, host, port, database):
        self.engine_name = engine_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        if 'mysql' in self.engine_name:
            self.pymysql_connection()
            
        elif 'postgres' in self.engine_name:
            self.psycopg_connection()
        
        self.sqlalchemy_connection()
        
    # pymysql connection 메소드
    def pymysql_connection(self):
        import pymysql
        self.pymysql_conn = pymysql.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=int(self.port),
            database=self.database,
            charset='utf8'
        )
        
    # psycopg2 connection 메소드
    def psycopg_connection(self):
        import psycopg2
        self.psycopg_conn = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            dbname=self.database,
            )
        
    # sqlalchemy connection 메소드
    def sqlalchemy_connection(self):
        from sqlalchemy import create_engine
        self.sql_conn = create_engine(f"{self.engine_name}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}")