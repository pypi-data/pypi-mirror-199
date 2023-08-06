from ..configs import DBconnectionHandler
from ..entities import agent__event_instance

from sqlalchemy import select
from sqlalchemy import func

from sqlalchemy import (
    Column,
    Table,
    Integer,
    VARCHAR,
    MetaData,
    DateTime,
)

meta = MetaData()


class AgentEventRepository:
    def __init__(self, database, tablename, echo=False):
        self.__database = DBconnectionHandler(database, echo)
        self.__table_name = tablename
        self.__metadata_table = Table(
            self.__table_name,
            meta,
            Column("agent_event_id", Integer, primary_key=True, autoincrement=False),
            Column("date", DateTime),
            Column("queue_id", VARCHAR(128)),
            Column("agent_id", Integer),
            Column("event", VARCHAR(16)),
            Column("reason", VARCHAR(256), default=None),
            Column("extension_id", VARCHAR(12), default=None),
        )

    def insert(
        self, agent_event_id, date, queue_id, agent_id, event, reason, extension_id
    ):
        with self.__database as db:
            data_insert = agent__event_instance(self.__table_name)(
                agent_event_id=agent_event_id,
                date=date,
                queue_id=queue_id,
                agent_id=agent_id,
                event=event,
                reason=reason,
                extension_id=extension_id,
            )
            db.session.merge(data_insert)
            db.session.commit()

    def select_agent_event_id(self):
        with self.__database as db:
            statement = select(
                func.max(self.__metadata_table.c["agent_event_id"]).label(
                    "last_agent_event_id"
                )
            )
            for row in db.session.execute(statement):
                return row[0]

            db.session.commit()
