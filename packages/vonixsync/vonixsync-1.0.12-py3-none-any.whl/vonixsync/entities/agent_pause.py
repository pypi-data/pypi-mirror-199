from sqlalchemy import Column, VARCHAR, DateTime, BigInteger, Integer, SmallInteger
from ..configs import Base


def agent_pause_instance(table_name):
    class AgentPause(Base):
        __tablename__ = table_name
        __table_args__ = {"extend_existing": True}
        agent_id = Column(Integer, primary_key=True, autoincrement=False)
        queue_id = Column(VARCHAR(128), primary_key=True, autoincrement=False)
        date = Column(DateTime, primary_key=True, nullable=True)
        pause_reason_id = Column(SmallInteger, primary_key=True, autoincrement=False)
        pause_secs = Column(BigInteger, default=0)

    return AgentPause
