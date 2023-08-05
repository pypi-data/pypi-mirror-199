import sys
from sqlalchemy import (
    Column,
    Table,
    Integer,
    VARCHAR,
    BOOLEAN,
    BigInteger,
    MetaData,
    SmallInteger,
    DateTime,
    String,
    Numeric,
    Index,
    TEXT,
    create_engine,
)
from sqlalchemy.exc import OperationalError
from ..utils import bcolors, ConnectionDatabaseError


def create_database(
    database_connection,
    agent_event_table_name="",
    agent_pause_table_name="",
    agent_summary_table_name="",
    agent_table_name="",
    call_rating_table_name="",
    calls_table_name="",
    chat_message_table_name="",
    chat_table_name="",
    profiler_table_name="",
    queue_summary_table_name="",
    queue_table_name="",
    tree_table_name="",
    echo=False,
):
    engine = create_engine(database_connection, echo=echo)
    meta = MetaData()

    if agent_table_name != "":
        agent = Table(
            agent_table_name,
            meta,
            Column("agent_id", Numeric(11), primary_key=True, autoincrement=False),
            Column("name", VARCHAR(256)),
            Column("nickname", VARCHAR(256), nullable=True),
            Column("active", BOOLEAN),
            Column("default_queue", VARCHAR(128)),
        )
        try:
            meta.create_all(engine)
        except OperationalError as error:
            print(f"Database_connection_error: {error}")
            sys.exit(1)

    if agent_event_table_name != "":
        agent_event = Table(
            agent_event_table_name,
            meta,
            Column("agent_event_id", Integer, primary_key=True, autoincrement=False),
            Column("date", DateTime),
            Column("queue_id", VARCHAR(128)),
            Column("agent_id", Integer),
            Column("event", VARCHAR(16)),
            Column("reason", VARCHAR(256), default=None),
            Column("extension_id", VARCHAR(12), default=None),
        )
        meta.create_all(engine)

    if queue_table_name != "":
        queue = Table(
            queue_table_name,
            meta,
            Column("queue_id", VARCHAR(128), primary_key=True, autoincrement=False),
            Column("name", VARCHAR(256)),
            Column("description", VARCHAR(128), default=""),
            Column("is_in", Integer),
            Column("is_out", Integer),
            Column("is_auto", Integer),
            Column("dialer_mode", VARCHAR(36), default="dialerMode"),
        )
        Index("queue_id_index", queue.c.queue_id)
        meta.create_all(engine)

    if agent_summary_table_name != "":
        agent_summary = Table(
            agent_summary_table_name,
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
        try:
            meta.create_all(engine)
        except OperationalError as error:
            print(f"Database_connection_error: {error}")
            sys.exit(1)

    if queue_summary_table_name != "":
        queue_summary = Table(
            queue_summary_table_name,
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

    try:
        meta.create_all(engine)
    except OperationalError as error:
        error_value = error.__dict__["orig"]
        print(
            f"\n\n{bcolors.FAIL}Database_connection_error:\n\n{bcolors.WHITE}{error_value}\n"
        )
        sys.exit(1)

    if agent_pause_table_name != "":
        agent_pause = Table(
            agent_pause_table_name,
            meta,
            Column("agent_id", BigInteger, primary_key=True, autoincrement=False),
            Column("queue_id", VARCHAR(128), primary_key=True, autoincrement=False),
            Column("date", DateTime, primary_key=True, nullable=True),
            Column(
                "pause_reason_id", SmallInteger, primary_key=True, autoincrement=False
            ),
            Column("pause_secs", BigInteger, default=0),
        )
        meta.create_all(engine)

    if call_rating_table_name != "":
        call_rating = Table(
            call_rating_table_name,
            meta,
            Column("call_id", VARCHAR(128), primary_key=True, autoincrement=False),
            Column(
                "property",
                VARCHAR(256),
                primary_key=True,
                autoincrement=False,
                default="",
            ),
            Column("insert_time", DateTime, primary_key=True, autoincrement=False),
            Column("rate", VARCHAR(128), default=""),
        )
        meta.create_all(engine)

    if calls_table_name != "":
        call = Table(
            calls_table_name,
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
        Index("caller_id_index", call.c.caller_id)
        Index("status_index", call.c.status)
        Index("start_time_index", call.c.start_time)
        Index("agent_id_index", call.c.agent_id)
        meta.create_all(engine)

    if chat_table_name != "":
        chat = Table(
            chat_table_name,
            meta,
            Column("chat_id", BigInteger, primary_key=True),
            Column("agent_id", BigInteger, index=True),
            Column("queue_id", VARCHAR(128), index=True),
            Column("source", VARCHAR(36)),
            Column("source_id", VARCHAR(256)),
            Column("name", VARCHAR(256)),
            Column("direction", VARCHAR(12)),
            Column("status", VARCHAR(36)),
            Column("hold_secs", Integer, default=0),
            Column("talk_secs", Integer, default=0),
            Column("chat_secs", Integer, default=0),
            Column("created_at", DateTime, index=True),
            Column("answered_at", DateTime, index=True),
            Column("finished_at", DateTime, index=True),
        )
        Index("agent_id_chat_index", chat.c.agent_id)
        Index("created_at_id_index", chat.c.created_at)
        Index("queue_id_chat_table_name_index", chat.c.queue_id)
        Index("finished_at_index", chat.c.finished_at)
        Index("answered_at_index", chat.c.answered_at)
        meta.create_all(engine)

    if chat_message_table_name != "":
        chat_message = Table(
            chat_message_table_name,
            meta,
            Column("message_id", BigInteger, primary_key=True),
            Column("chat_id", BigInteger, index=True),
            Column("message", TEXT),
            Column("direction", VARCHAR(128)),
            Column("created_at", DateTime, index=True),
            Column("delivered_at", DateTime),
            Column("readed_at", DateTime),
            Column("answered_at", DateTime),
            Column("type", VARCHAR(16)),
        )
        Index("created_at_chat_message_index", chat_message.c.created_at)
        Index("chat_id_index", chat_message.c.chat_id)
        meta.create_all(engine)

    if profiler_table_name != "":
        profiler = Table(
            profiler_table_name,
            meta,
            Column("field_id", BigInteger, primary_key=True, autoincrement=False),
            Column("call_id", VARCHAR(128), primary_key=True, autoincrement=False),
            Column("chat_id", BigInteger, primary_key=True, autoincrement=False),
            Column("created_at", DateTime, primary_key=True, autoincrement=False),
            Column("field_name", VARCHAR(256)),
            Column("field_value", VARCHAR(128)),
        )
        meta.create_all(engine)

    if tree_table_name != "":
        tree = Table(
            tree_table_name,
            meta,
            Column("branch_id", VARCHAR(36), primary_key=True, autoincrement=False),
            Column("call_id", VARCHAR(128), primary_key=True, autoincrement=False),
            Column("chat_id", BigInteger, primary_key=True, autoincrement=False),
            Column("created_at", DateTime, primary_key=True, autoincrement=False),
            Column("branch_label", VARCHAR(256)),
        )
        meta.create_all(engine)
    return print(
        f"\n\n{bcolors.OKGREEN}The tables were created with success{bcolors.WHITE}\n\n"
    )
