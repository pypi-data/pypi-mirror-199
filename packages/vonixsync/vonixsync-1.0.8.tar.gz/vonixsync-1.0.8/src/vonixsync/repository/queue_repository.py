from ..configs import DBconnectionHandler
from ..entities import queue_instance


class QueueRepository:
    def __init__(self, database, table_name, echo=False):
        self.__database = DBconnectionHandler(database, echo)
        self.__table_name = table_name

    def insert(self, queue_id, name, description, is_in, is_out, is_auto, dialer_mode):
        with self.__database as db:
            data_insert = queue_instance(self.__table_name)(
                queue_id=queue_id,
                name=name,
                description=description,
                is_in=is_in,
                is_out=is_out,
                is_auto=is_auto,
                dialer_mode=dialer_mode,
            )
            db.session.merge(data_insert)
            db.session.commit()
