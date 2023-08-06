from sqlalchemy import Column, Integer, VARCHAR, DateTime
from ..configs import Base


def call_instance(table_name):
    class Call(Base):
        __tablename__ = table_name
        __table_args__ = {"extend_existing": True}
        call_id = Column(VARCHAR(128), primary_key=True)
        queue_id = Column(VARCHAR(128), primary_key=True, index=True)
        direction = Column(VARCHAR(12))
        offers = Column(Integer, default=0)
        caller_id = Column(VARCHAR(30), index=True)
        caller_info = Column(VARCHAR(30))
        hold_secs = Column(Integer, default=0)
        talk_secs = Column(Integer, default=0)
        ring_secs = Column(Integer, default=0)
        status = Column(VARCHAR(16), index=True)
        status_cause = Column(VARCHAR(255))
        locality = Column(VARCHAR(256), default="")
        call_type = Column(VARCHAR(256))
        trunking = Column(VARCHAR(256))
        carrier = Column(VARCHAR(256), nullable=True)
        exit_key = Column(Integer)
        initial_position = Column(Integer)
        abandon_position = Column(Integer)
        start_time = Column(DateTime, index=True)
        answer_time = Column(DateTime)
        hangup_time = Column(DateTime)
        transferred_to = Column(VARCHAR(255))
        agent_id = Column(Integer, index=True)

    return Call
