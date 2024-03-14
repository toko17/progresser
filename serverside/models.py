from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    first_name = Column(String, index=True)
    last_name = Column(String, index=True)

    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    disabled = Column(Boolean, default=False, index=True)
    
    organisations = relationship("Organisation", back_populates="users")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Organisation(Base):
    __tablename__ = "organisations"

    uuid = Column(String, primary_key=True, index=True)

    title = Column(String, unique=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User", back_populates="organisations")
    tables = relationship("Table", back_populates="organisation")


class Table(Base):
    __tablename__ = "tables"

    uuid = Column(String, primary_key=True, index=True)

    title = Column(String, index=True)

    organisation_uuid = Column(String, ForeignKey("organisations.uuid"))

    organisation = relationship("Organisation", back_populates="tables")
    lists = relationship("List", back_populates="tables")


class List(Base):
    __tablename__ = "lists"

    uuid = Column(String, primary_key=True, index=True)

    title = Column(String, index=True)
    subtitle = Column(String, index=True)

    table_uuid = Column(String, ForeignKey("tables.uuid"))

    tables = relationship("Table", back_populates="lists")
    tasks = relationship("Task", back_populates="list")


class Task(Base):
    __tablename__ = "tasks"

    uuid = Column(String, primary_key=True, index=True)

    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(String, index=True)
    created_at = Column(DateTime)

    list_uuid = Column(String, ForeignKey("lists.uuid"))

    list = relationship("List", back_populates="tasks")
    subtasks = relationship("Subtask", back_populates="task")


class Subtask(Base):
    __tablename__ = "subtasks"

    uuid = Column(String, primary_key=True, index=True)

    title = Column(String, index=True)
    description = Column(String, index=True)
    priority = Column(String, index=True)
    created_at = Column(DateTime)

    task_uuid = Column(String, ForeignKey("tasks.uuid"))
    
    task = relationship("Task", back_populates="subtasks")
