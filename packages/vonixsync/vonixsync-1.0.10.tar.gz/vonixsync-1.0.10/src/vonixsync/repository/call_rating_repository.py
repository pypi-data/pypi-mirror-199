from ..configs import DBconnectionHandler
from ..entities import call_rating_instance


class CallRatingRepository:
    def __init__(self, database, tablename, echo=False):
        self.__database = DBconnectionHandler(database, echo)
        self.__table_name = tablename

    def insert(self, call_id, property, insert_time, rate):
        with self.__database as db:
            data_insert = call_rating_instance(self.__table_name)(
                call_id=call_id, property=property, insert_time=insert_time, rate=rate
            )
            db.session.merge(data_insert)
            db.session.commit()
