from .settings_db import Base 
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class ContextDB(Base):

    __tablename__ = "todo_list"

    id : Mapped[int] = mapped_column(primary_key=True, index=True) #primary_key первичный ключ 

    title : Mapped[str] = mapped_column(String(35), index=True)

    description : Mapped[str] = mapped_column(index=True)


#Base.metadata.create_all(bind=Settings_db.engine_create)



