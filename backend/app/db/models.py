from sqlalchemy import Column, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)

    user_gpts = relationship("User_gpt", back_populates="owner")


class User_gpt(Base):
    __tablename__ = "user_gpts"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    gpt_id = Column(String, primary_key=True)

    owner = relationship("User", back_populates="user_gpts")

    # __table_args__ = (
    #     UniqueConstraint('user_id', 'gpt_id', name='uq_user_gpt'),
    # )

    def __str__(self):
        return f"User_gpt(user_id={self.user_id}, gpt_id={self.gpt_id})"
