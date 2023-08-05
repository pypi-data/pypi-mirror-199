from sqlalchemy import Column, String, Integer, VARCHAR, BigInteger, DateTime
from ..configs import Base


def tree_instance(table_name):
    class Tree(Base):
        __tablename__ = table_name
        __table_args__ = {"extend_existing": True}
        branch_id = Column(VARCHAR(36), primary_key=True, autoincrement=False)
        call_id = Column(String, primary_key=True, autoincrement=False)
        chat_id = Column(BigInteger, primary_key=True, autoincrement=False)
        created_at = Column(DateTime, primary_key=True, autoincrement=False)
        branch_label = Column(VARCHAR(256))

    return Tree
