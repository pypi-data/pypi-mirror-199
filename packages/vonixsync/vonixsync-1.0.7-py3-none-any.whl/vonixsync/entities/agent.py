from sqlalchemy import Column, String, Integer, BOOLEAN, VARCHAR, Numeric
from ..configs import Base


def agent_instance(table_name):
    class Agent(Base):
        __tablename__ = table_name
        __table_args__ = {"extend_existing": True}
        agent_id = Column(Integer, primary_key=True, autoincrement=False)
        name = Column(VARCHAR(256))
        nickname = Column(VARCHAR(256), nullable=True)
        active = Column(BOOLEAN)
        default_queue = Column(VARCHAR(128))

    return Agent
