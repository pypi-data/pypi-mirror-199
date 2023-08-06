from ..configs import DBconnectionHandler
from ..entities import agent_pause_instance
from sqlalchemy import select
from sqlalchemy import func
from datetime import datetime, timedelta, timezone
from sqlalchemy import (
    Column,
    Table,
    BigInteger,
    SmallInteger,
    VARCHAR,
    MetaData,
    DateTime,
)

meta = MetaData()


class AgentPauseRepository:
    def __init__(self, database, tablename, echo=False):
        self.__database = DBconnectionHandler(database, echo)
        self.__table_name = tablename
        self.__metadata_table = Table(
            self.__table_name,
            meta,
            Column("agent_id", BigInteger, primary_key=True, autoincrement=False),
            Column("queue_id", VARCHAR(128), primary_key=True, autoincrement=False),
            Column("date", DateTime, primary_key=True, nullable=True),
            Column(
                "pause_reason_id", SmallInteger, primary_key=True, autoincrement=False
            ),
            Column("pause_secs", BigInteger, default=0),
        )

    def insert(self, agent_id, queue_id, date, pause_secs, pause_reason_id):
        with self.__database as db:
            data_insert = agent_pause_instance(self.__table_name)(
                agent_id=agent_id,
                queue_id=queue_id,
                date=date,
                pause_secs=pause_secs,
                pause_reason_id=pause_reason_id,
            )
            db.session.merge(data_insert)
            db.session.commit()

    def select_date(self, query_timestamp):
        with self.__database as db:
            statement = select(
                func.max(self.__metadata_table.c["date"]).label("last_date")
            )

            for row in db.session.execute(statement):
                if row[0] is None:
                    if query_timestamp is not None:
                        return query_timestamp

                    yesterday = datetime.now() - timedelta(days=1)
                    return int(yesterday.timestamp())

                timestamp_from_database = int(
                    row[0].replace(tzinfo=timezone.utc).timestamp()
                )
                return timestamp_from_database

            db.session.commit()
