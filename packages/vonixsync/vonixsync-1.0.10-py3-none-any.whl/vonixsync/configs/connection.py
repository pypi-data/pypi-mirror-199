from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBconnectionHandler:
    def __init__(self, connection_string, echo):
        self.__connection_string = connection_string
        self.__echo = echo
        self.__engine = self.__create_database_engine()

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string, echo=self.__echo)
        return engine

    def get_engine(self):
        return self.__engine

    def db_config(self):
        return self.__connection_string

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


class DBConfigs:
    def __init__(
        self,
        database_manager,
        user,
        password,
        hostname,
        database,
        port,
    ):
        self.__database_manager = database_manager
        self.__user = user
        self.__password = password
        self.__hostname = hostname
        self.__database = database
        self.__port = port
        self.connect = self.configure()

    def configure(self):
        if self.__database_manager == "postgres":
            return f"postgresql+psycopg2://{self.__user}:{self.__password}@{self.__hostname}:{self.__port}/{self.__database}"

        if self.__database_manager == "mysql":
            return f"mysql+mysqlconnector://{self.__user}:{self.__password}@{self.__hostname}:{self.__port}/{self.__database}"
