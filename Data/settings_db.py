import asyncio
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class Settings_db:

    def __init__(self, DATABASE_URL):

        self.DATABASE_URL=DATABASE_URL

        self.async_engine = None

        self.async_session = None # Необязательный параметр

        self.create_table = self.create_tables # Создание таблицы без вызова метода в конструкторе


    def engine_create(self):

        self.async_engine = create_async_engine(

            self.DATABASE_URL, # url к нашей базе данных

            echo=True,

        )

        return self.async_engine    



    def localsession(self):

        self.async_session = async_sessionmaker(


            autoflush=False, # ручная отправка изменений в базу данных

            bind=self.async_engine, # Подключение к базе данных

             class_= AsyncSession,

            expire_on_commit=False, 
            
            )
    
        return self.async_session
    

    async def create_tables(self):
        """Создание всех таблиц в базе данных."""
        if self.async_engine is None:
            raise ValueError("Сначала создайте движок с помощью engine_create()")
        
        async with self.async_engine.begin() as conn:

            await conn.run_sync(Base.metadata.create_all)



db_manager = Settings_db("sqlite+aiosqlite:///./todo_list.db")

db_manager.engine_create()

db_manager.localsession()






class Base(DeclarativeBase):

    pass