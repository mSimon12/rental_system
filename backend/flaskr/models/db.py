from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey

Base = declarative_base()

db = SQLAlchemy(model_class=Base)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(50), unique=True, nullable=False)

    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, role={self.role!r})>"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    stock_size = Column(Integer, nullable=False)
    available = Column(Integer)

    rentals = relationship("ItemRentControl", back_populates="item")

    def __repr__(self):
        return f"<Item(id={self.id}, item={self.item!r}, stock={self.stock_size}, available={self.available})>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    role = relationship("Role", back_populates="users")
    rentals = relationship("ItemRentControl", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username!r}, email={self.email!r}, role_id={self.role_id})>"


class ItemRentControl(Base):
    __tablename__ = "items_rent_control"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rent_date = Column(Date, nullable=False)
    return_date = Column(Date)

    item = relationship("Item", back_populates="rentals")
    user = relationship("User", back_populates="rentals")

    def __repr__(self):
        return (
            f"<ItemRentControl(id={self.id}, item_id={self.item_id}, "
            f"user_id={self.user_id}, rent_date={self.rent_date}, return_date={self.return_date})>"
        )
