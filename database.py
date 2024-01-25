from sqlalchemy import create_engine, Column, Integer, String, MetaData, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db', echo=True)
metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    login = Column(String(30), unique=True, index=True)
    password = Column(String(100))
    balance = Column(Float, default=5000.0)


Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

# Добавляем несколько пользователей с указанием суммы денег на счету
users_data = [
    {'name': 'John', 'login': 'john', 'password': '1234', 'balance': 100.0},
    {'name': 'Jane', 'login': 'jane', 'password': 'qwerty', 'balance': 100.0},
    {'name': 'Bob', 'login': 'bob', 'password': 'password123', 'balance': 100.0},
]

for user_data in users_data:
    new_user = User(**user_data)
    db.add(new_user)

db.commit()
db.close()
