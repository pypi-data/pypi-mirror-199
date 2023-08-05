from ..configs import DBconnectionHandler
from ..entities import profiler_instance


class ProfilerRepository:
    def __init__(self, database, tablename, echo=False):
        self.__database = DBconnectionHandler(database, echo)
        self.__table_name = tablename

    def insert(
        self,
        field_id,
        call_id,
        chat_id,
        created_at,
        field_name,
        field_value,
    ):
        with self.__database as db:
            data_insert = profiler_instance(self.__table_name)(
                field_id=field_id,
                call_id=call_id,
                chat_id=chat_id,
                created_at=created_at,
                field_name=field_name,
                field_value=field_value,
            )
            db.session.merge(data_insert)
            db.session.commit()
