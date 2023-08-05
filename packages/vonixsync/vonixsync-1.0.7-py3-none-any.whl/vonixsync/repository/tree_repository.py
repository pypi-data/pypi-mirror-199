from ..configs import DBconnectionHandler
from ..entities import tree_instance


class TreeRepository:
    def __init__(self, database, tablename, echo=False):
        self.__database = DBconnectionHandler(database, echo)
        self.__table_name = tablename

    def insert(
        self,
        branch_id,
        call_id,
        chat_id,
        created_at,
        branch_label,
    ):
        with self.__database as db:
            data_insert = tree_instance(self.__table_name)(
                branch_id=branch_id,
                call_id=call_id,
                chat_id=chat_id,
                created_at=created_at,
                branch_label=branch_label,
            )
            db.session.merge(data_insert)
            db.session.commit()
