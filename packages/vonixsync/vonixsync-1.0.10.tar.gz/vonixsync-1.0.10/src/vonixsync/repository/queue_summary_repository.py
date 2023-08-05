from ..configs import DBconnectionHandler
from ..entities import queue_summary_instance

from sqlalchemy import select
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

from sqlalchemy import (
    Column,
    Table,
    VARCHAR,
    MetaData,
    DateTime,
    BigInteger,
)

meta = MetaData()


class QueueSummaryRepository:
    def __init__(self, database, tablename, echo=False):
        self.__database = DBconnectionHandler(database, echo)
        self.__table_name = tablename
        self.__metadata_table = Table(
            self.__table_name,
            meta,
            Column("queue_id", VARCHAR(128), primary_key=True, autoincrement=False),
            Column("date", DateTime, primary_key=True, autoincrement=False),
            Column("in_completed", BigInteger, default=0),
            Column("in_transferred", BigInteger, default=0),
            Column("in_abandoned", BigInteger, default=0),
            Column("in_completed_sla", BigInteger, default=0),
            Column("in_abandoned_sla", BigInteger, default=0),
            Column("out_completed", BigInteger, default=0),
            Column("out_transferred", BigInteger, default=0),
            Column("out_discarded", BigInteger, default=0),
            Column("auto_completed", BigInteger, default=0),
            Column("auto_transferred", BigInteger, default=0),
            Column("auto_discarded", BigInteger, default=0),
            Column("auto_abandoned", BigInteger, default=0),
            Column("in_call_secs", BigInteger, default=0),
            Column("out_call_secs", BigInteger, default=0),
            Column("auto_call_secs", BigInteger, default=0),
            Column("in_hold_secs_completed", BigInteger, default=0),
            Column("in_hold_secs_abandoned", BigInteger, default=0),
            Column("out_try_secs_completed", BigInteger, default=0),
            Column("out_try_secs_discarded", BigInteger, default=0),
            Column("auto_hold_secs_completed", BigInteger, default=0),
            Column("auto_hold_secs_abandoned", BigInteger, default=0),
            Column("auto_try_secs_completed", BigInteger, default=0),
            Column("auto_try_secs_discarded", BigInteger, default=0),
        )

    def insert(
        self,
        queue_id,
        date,
        in_completed,
        in_transferred,
        in_abandoned,
        in_completed_sla,
        in_abandoned_sla,
        out_completed,
        out_transferred,
        out_discarded,
        auto_completed,
        auto_transferred,
        auto_discarded,
        auto_abandoned,
        in_call_secs,
        out_call_secs,
        auto_call_secs,
        in_hold_secs_completed,
        in_hold_secs_abandoned,
        out_try_secs_completed,
        out_try_secs_discarded,
        auto_hold_secs_completed,
        auto_hold_secs_abandoned,
        auto_try_secs_completed,
        auto_try_secs_discarded,
    ):
        with self.__database as db:
            data_insert = queue_summary_instance(self.__table_name)(
                queue_id=queue_id,
                date=date,
                in_completed=in_completed,
                in_transferred=in_transferred,
                in_abandoned=in_abandoned,
                in_completed_sla=in_completed_sla,
                in_abandoned_sla=in_abandoned_sla,
                out_completed=out_completed,
                out_transferred=out_transferred,
                out_discarded=out_discarded,
                auto_completed=auto_completed,
                auto_transferred=auto_transferred,
                auto_discarded=auto_discarded,
                auto_abandoned=auto_abandoned,
                in_call_secs=in_call_secs,
                out_call_secs=out_call_secs,
                auto_call_secs=auto_call_secs,
                in_hold_secs_completed=in_hold_secs_completed,
                in_hold_secs_abandoned=in_hold_secs_abandoned,
                out_try_secs_completed=out_try_secs_completed,
                out_try_secs_discarded=out_try_secs_discarded,
                auto_hold_secs_completed=auto_hold_secs_completed,
                auto_hold_secs_abandoned=auto_hold_secs_abandoned,
                auto_try_secs_completed=auto_try_secs_completed,
                auto_try_secs_discarded=auto_try_secs_discarded,
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
