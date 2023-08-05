from ..configs import DBconnectionHandler
from ..entities import call_instance

from sqlalchemy import select
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

from sqlalchemy import (
    Column,
    Table,
    Integer,
    VARCHAR,
    MetaData,
    DateTime,
)

meta = MetaData()


class CallRepository:
    def __init__(self, database, tablename, echo=False):
        self.__database = DBconnectionHandler(database, echo)
        self.__table_name = tablename
        self.__metadata_table = Table(
            self.__table_name,
            meta,
            Column("call_id", VARCHAR(128), primary_key=True),
            Column("queue_id", VARCHAR(128), primary_key=True, index=True),
            Column("direction", VARCHAR(12)),
            Column("offers", Integer, default=0),
            Column("caller_id", VARCHAR(30), index=True),
            Column("caller_info", VARCHAR(30)),
            Column("hold_secs", Integer, default=0),
            Column("talk_secs", Integer, default=0),
            Column("ring_secs", Integer, default=0),
            Column("status", VARCHAR(16), index=True),
            Column("status_cause", VARCHAR(255)),
            Column("locality", VARCHAR(256), default=""),
            Column("call_type", VARCHAR(256)),
            Column("trunking", VARCHAR(256)),
            Column("carrier", VARCHAR(256)),
            Column("exit_key", Integer),
            Column("initial_position", Integer),
            Column("abandon_position", Integer),
            Column("start_time", DateTime, index=True),
            Column("answer_time", DateTime),
            Column("hangup_time", DateTime),
            Column("transferred_to", VARCHAR(255)),
            Column("agent_id", Integer, index=True),
        )

    def insert(
        self,
        call_id,
        queue_id,
        direction,
        offers,
        caller_id,
        caller_info,
        hold_secs,
        talk_secs,
        ring_secs,
        status,
        status_cause,
        locality,
        call_type,
        trunking,
        carrier,
        exit_key,
        initial_position,
        abandon_position,
        start_time,
        answer_time,
        hangup_time,
        transferred_to,
        agent_id,
    ):
        with self.__database as db:
            data_insert = call_instance(self.__table_name)(
                call_id=call_id,
                queue_id=queue_id,
                direction=direction,
                offers=offers,
                caller_id=caller_id,
                caller_info=caller_info,
                hold_secs=hold_secs,
                talk_secs=talk_secs,
                ring_secs=ring_secs,
                status=status,
                status_cause=status_cause,
                locality=locality,
                call_type=call_type,
                trunking=trunking,
                carrier=carrier,
                exit_key=exit_key,
                initial_position=initial_position,
                abandon_position=abandon_position,
                start_time=start_time,
                answer_time=answer_time,
                hangup_time=hangup_time,
                transferred_to=transferred_to,
                agent_id=agent_id,
            )
            db.session.merge(data_insert)
            db.session.commit()

    def select_date(self, query_timestamp):
        with self.__database as db:
            statement = select(
                func.max(self.__metadata_table.c["start_time"]).label("last_date")
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
