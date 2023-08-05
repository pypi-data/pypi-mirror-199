from sqlalchemy import Column, VARCHAR, DateTime, BigInteger, Integer
from ..configs import Base


def agent_summary_instance(table_name):
    class AgentSummary(Base):
        __tablename__ = table_name
        __table_args__ = {"extend_existing": True}
        agent_id = Column(Integer, primary_key=True, autoincrement=False)
        queue_id = Column(VARCHAR(128), primary_key=True, autoincrement=False)
        date = Column(DateTime, primary_key=True, autoincrement=False)

        in_completed = Column(BigInteger, default=0)
        out_completed = Column(BigInteger, default=0)
        out_discarded = Column(BigInteger, default=0)
        auto_completed = Column(BigInteger, default=0)

        rejections = Column(BigInteger, default=0)
        login_secs = Column(BigInteger, default=0)
        pause_secs = Column(BigInteger, default=0)

        in_ring_secs = Column(BigInteger, default=0)
        out_ring_secs = Column(BigInteger, default=0)
        in_call_secs = Column(BigInteger, default=0)
        out_call_secs = Column(BigInteger, default=0)
        auto_call_secs = Column(BigInteger, default=0)
        call_secs = Column(BigInteger, default=0)
        ring_secs = Column(BigInteger, default=0)

    return AgentSummary
