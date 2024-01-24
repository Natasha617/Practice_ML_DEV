from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем экземпляр движка базы данных (замените 'sqlite:///example.db' на ваше соединение)
engine = create_engine('sqlite:///database.db', echo=True)

# Создаем экземпляр метаданных
metadata = MetaData()

# Создаем базовый класс для моделей
Base = declarative_base(metadata=metadata)


# Определяем модель пользователя
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    login = Column(String(30), unique=True, index=True)
    password = Column(String(100))


# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Создаем сессию для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем сессию
db = SessionLocal()

# Пример добавления пользователя
new_user = User(name='John Doe', login='john_doe', password='secure_password')
db.add(new_user)
db.commit()
db.close()
