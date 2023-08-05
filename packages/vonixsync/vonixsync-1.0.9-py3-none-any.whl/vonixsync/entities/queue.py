from sqlalchemy import Column, String, Integer, VARCHAR
from ..configs import Base


def queue_instance(table_name):
    class Queue(Base):
        __tablename__ = table_name
        __table_args__ = {"extend_existing": True}
        queue_id = Column(String, primary_key=True, autoincrement=False)
        name = Column(VARCHAR(256))
        description = Column(String, default="")
        is_in = Column(Integer)
        is_out = Column(Integer)
        is_auto = Column(Integer)
        dialer_mode = Column(VARCHAR(36), default="dialerMode")

    return Queue
