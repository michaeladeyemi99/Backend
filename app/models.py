from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import db


class User(db.Model):
    __tablename__ = "users"
    user_id = mapped_column(Integer, primary_key=True)
    user_name = mapped_column(String(50), unique=True, nullable=False)
    user_email = mapped_column(String(50), unique=True, nullable=False)
    user_UID = mapped_column(String(50), unique=True, nullable=False)

    # One to many relationship --- (a user can have many boards)
    boards = relationship("Board", back_populates="user")

class Board(db.Model):
    __tablename__ = "boards"
    board_id = mapped_column(Integer, primary_key=True)
    board_name = mapped_column(String(50), unique=True, nullable=False)
    user_id = mapped_column(ForeignKey("users.user_id"), nullable=False)

    # One to many relationship ======> A user can have many boards
    user = relationship("User", back_populates="boards")

    # One to many ====> A board can have several columns
    columns = relationship("Column", back_populates="board")


class Column(db.Model):
    __tablename__ = "columns"
    column_id = mapped_column(Integer, primary_key=True)
    column_name = mapped_column(String(50), unique=True, nullable=False)
    column_order_id = mapped_column(Integer, nullable=False)
    board_id = mapped_column(ForeignKey("boards.board_id"), nullable= False)

    # One to many relationship =====> A Board can have several columns
    board = relationship("Board", back_populates="columns")

    # One to many ====> A column can have many task
    tasks = relationship("Task", back_populates="column")

class Task(db.Model):
    __tablename__ = "tasks"
    task_id = mapped_column(Integer, primary_key=True)
    task_name = mapped_column(String(50), unique=True, nullable=False)
    task_description = mapped_column(String, nullable=False)
    task_order_id = mapped_column(Integer, nullable=False)
    column_id = mapped_column(ForeignKey("columns.column_id"), nullable=False)

    # One to many relationship as a column can have multiple Tasks
    column = relationship("Column", back_populates="tasks")