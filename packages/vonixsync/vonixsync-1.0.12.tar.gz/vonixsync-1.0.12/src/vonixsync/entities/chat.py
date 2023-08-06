from sqlalchemy import BigInteger, VARCHAR, Integer, DateTime, Column
from ..configs import Base


def chat_instance(table_name):
    class Chat(Base):
        __tablename__ = table_name
        __table_args__ = {"extend_existing": True}
        chat_id = Column(BigInteger, primary_key=True)
        agent_id = Column(BigInteger, index=True)
        queue_id = Column(VARCHAR(128), index=True)
        source = Column(VARCHAR(36))
        source_id = Column(VARCHAR(256))
        name = Column(VARCHAR(256))
        direction = Column(VARCHAR(12))
        status = Column(VARCHAR(36))
        hold_secs = Column(Integer, default=0)
        talk_secs = Column(Integer, default=0)
        chat_secs = Column(Integer, default=0)
        created_at = Column(DateTime, index=True)
        answered_at = Column(DateTime, index=True)
        finished_at = Column(DateTime, index=True)

    return Chat
