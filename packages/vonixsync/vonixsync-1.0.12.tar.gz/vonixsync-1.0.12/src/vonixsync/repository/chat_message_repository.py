from ..configs import DBconnectionHandler
from ..entities import chat_message_instance


class ChatMessageRepository:
    def __init__(self, database, tablename, echo=False):
        self.__database = DBconnectionHandler(database, echo)
        self.__table_name = tablename

    def insert(
        self,
        chat_id,
        message_id,
        message,
        direction,
        created_at,
        delivered_at,
        readed_at,
        answered_at,
        type,
    ):
        with self.__database as db:
            data_insert = chat_message_instance(self.__table_name)(
                chat_id=chat_id,
                message_id=message_id,
                message=message,
                direction=direction,
                created_at=created_at,
                delivered_at=delivered_at,
                readed_at=readed_at,
                answered_at=answered_at,
                type=type,
            )
            db.session.merge(data_insert)
            db.session.commit()
