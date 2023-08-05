from sqlalchemy import Column, String, VARCHAR, DateTime
from ..configs import Base


def call_rating_instance(table_name):
    class CallRating(Base):
        __tablename__ = table_name
        __table_args__ = {"extend_existing": True}
        call_id = Column(VARCHAR(128), primary_key=True, autoincrement=False)
        property = Column(
            VARCHAR(256), primary_key=True, autoincrement=False, default=""
        )
        insert_time = Column(DateTime, primary_key=True, autoincrement=False)
        rate = Column(String, default="")

    return CallRating
