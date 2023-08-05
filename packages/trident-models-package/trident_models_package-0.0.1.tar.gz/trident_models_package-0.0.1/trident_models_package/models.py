from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List

class Base(DeclarativeBase):
    pass


class Tweet(Base):
    __tablename__ = "tweets"

    tweet_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    tag_id: Mapped[int] = mapped_column(ForeignKey("category_tags.tag_id"))
    content: Mapped[str] = mapped_column(String(100))
    privacy: Mapped[int] = mapped_column(Boolean)
    created: Mapped[str] = mapped_column(DateTime)


    user: Mapped["User"] = relationship(back_populates="tweets")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="tweets")

    def toObj(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Tag(Base):
    __tablename__ = "category_tags"

    tag_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    tweets: Mapped[List["Tweet"]] = relationship("Tweet", back_populates="tag")


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(220))

    tweets: Mapped[List["Tweet"]] = relationship(back_populates="user")
