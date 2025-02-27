
from fastapi import  FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from httpx import AsyncByteStream
from sqlalchemy import TableValuedAlias, select, delete, update
from Data.database import ContextDB
from Data.settings_db import db_manager
from fastapi.templating import Jinja2Templates
from Test.jinja import page

app = FastAPI()



class Todo_list:

    
    @app.on_event("startup")
    async def startup():

        await db_manager.create_tables()
        
    # Методы для отрисовки html
    @app.get("/get_form", response_class=HTMLResponse) # теперь адрес выглядит так http://127.0.0.1:8000/get_form 
    async def read_form(request : Request):


        return page.TemplateResponse("todo_form.html", {"request": request})
    

    @app.get("/table_todo", response_class=HTMLResponse)
    async def table_page(request : Request):

        async with db_manager.localsession()() as db:

            get_todo = await db.execute(select(ContextDB))

            list_todo = get_todo.scalars().all()

            if not list_todo:

                return JSONResponse(content={"message": "Лист пустой"}, status_code=204)
            

            templates = Jinja2Templates(directory="templates")
            
            return templates.TemplateResponse("table_todo.html", {"request": request, "list_todo": list_todo})

    
    #Создание todo
    @app.post("/create_todo")
    async def create(request: Request,  title : str = Form(), description : str = Form()):

       async with db_manager.localsession()() as db:

            create_todo = ContextDB(title = title, description = description)

            if not create_todo:

                return ("Пользователь не создан")
            
            db.add(create_todo)

            await db.commit()

            await db.refresh(create_todo)

            return RedirectResponse(url='/table_todo', status_code=303)
            

    @app.get("/get_todo_by_id/")
    async def get_by_id(id : int):

        async with db_manager.localsession()() as db:


            get_by_id = await db.execute(select(ContextDB).where(ContextDB.id == id))

            todo = get_by_id.scalars().first()

            if not todo:

                return("ID не найдено")


            return todo
                

    @app.post("/delete_todo_by_id/{id}")
    async def delete_todo(id: int):

        async with db_manager.localsession()() as db:

            delete_todo_id = await db.execute(delete(ContextDB).where(ContextDB.id == id))

            if not delete_todo_id:

                return ("ID TODO удалено или не найдено")
            
            await db.commit()

            return RedirectResponse(url='/table_todo', status_code=303)

    @app.get("/edit_todo/", response_class=HTMLResponse)
    async def edit_todo_form(request: Request):


            return page.TemplateResponse("edit_todo.html", {"request": request})

            
    @app.post("/update_todo/{id}")
    async def update_todo(request: Request,  id : int, title : str = Form()  , description: str = Form()):

        async with db_manager.localsession()() as db:

            update_query = await db.execute(select(ContextDB)
                                            .where(ContextDB.id == id))
                                        

            if not update_query:

                raise HTTPException(status_code=400, detail="Нет данных для обновления")
            
            await db.execute(
            update(ContextDB)
            .where(ContextDB.id == id)
            .values(title=title, description=description)
        ) 

            await db.commit()

            return page.TemplateResponse("edit_todo.html", {"request": request, "todo": update_query})


            




            


