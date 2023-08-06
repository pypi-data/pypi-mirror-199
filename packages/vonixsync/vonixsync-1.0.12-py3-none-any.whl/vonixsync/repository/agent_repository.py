from ..configs import DBconnectionHandler
from ..entities import agent_instance


class AgentsRepository:
    def __init__(self, database, table_name, echo=False):
        self.__database = DBconnectionHandler(database, echo)
        self.__table_name = table_name

    def insert(self, agent_id, name, nickname, active, default_queue):
        with self.__database as db:
            data_insert = agent_instance(self.__table_name)(
                agent_id=agent_id,
                name=name,
                nickname=nickname,
                active=active,
                default_queue=default_queue,
            )
            db.session.merge(data_insert)
            db.session.commit()
