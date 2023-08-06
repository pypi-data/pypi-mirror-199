from ..configs import DBconnectionHandler
from ..entities import agent_summary_instance

from sqlalchemy import select
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

from sqlalchemy import (
    Column,
    Table,
    BigInteger,
    VARCHAR,
    MetaData,
    DateTime,
)

meta = MetaData()


class AgentSummaryRepository:
    def __init__(self, database, tablename, echo=False):
        self.__database = DBconnectionHandler(database, echo)
        self.__table_name = tablename
        self.__metadata_table = Table(
            self.__table_name,
            meta,
            Column("agent_id", BigInteger, primary_key=True, autoincrement=False),
            Column("queue_id", VARCHAR(128), primary_key=True, autoincrement=False),
            Column("date", DateTime, primary_key=True, autoincrement=False),
            Column("in_completed", BigInteger, default=0),
            Column("out_completed", BigInteger, default=0),
            Column("out_discarded", BigInteger, default=0),
            Column("auto_completed", BigInteger, default=0),
            Column("rejections", BigInteger, default=0),
            Column("login_secs", BigInteger, default=0),
            Column("pause_secs", BigInteger, default=0),
            Column("in_ring_secs", BigInteger, default=0),
            Column("out_ring_secs", BigInteger, default=0),
            Column("in_call_secs", BigInteger, default=0),
            Column("out_call_secs", BigInteger, default=0),
            Column("auto_call_secs", BigInteger, default=0),
            Column("call_secs", BigInteger, default=0),
            Column("ring_secs", BigInteger, default=0),
        )

    def insert(
        self,
        agent_id,
        queue_id,
        date,
        in_completed,
        out_completed,
        out_discarded,
        auto_completed,
        rejections,
        login_secs,
        pause_secs,
        in_ring_secs,
        out_ring_secs,
        in_call_secs,
        out_call_secs,
        auto_call_secs,
        call_secs,
        ring_secs,
    ):
        with self.__database as db:
            data_insert = agent_summary_instance(self.__table_name)(
                agent_id=agent_id,
                queue_id=queue_id,
                date=date,
                in_completed=in_completed,
                out_completed=out_completed,
                out_discarded=out_discarded,
                auto_completed=auto_completed,
                rejections=rejections,
                login_secs=login_secs,
                pause_secs=pause_secs,
                in_ring_secs=in_ring_secs,
                out_ring_secs=out_ring_secs,
                in_call_secs=in_call_secs,
                out_call_secs=out_call_secs,
                auto_call_secs=auto_call_secs,
                call_secs=call_secs,
                ring_secs=ring_secs,
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
