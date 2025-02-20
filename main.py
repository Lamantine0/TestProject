
from fastapi import Depends, FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy import select
from Data.database import ContextDB
from Data.settings_db import db_manager
from fastapi.templating import Jinja2Templates


app = FastAPI()



class Todo_list:

    
    @app.on_event("startup")
    async def startup():

        await db_manager.create_tables()
        

    @app.get("/", response_class=HTMLResponse)
    async def read_form(request : Request):

        templates = Jinja2Templates(directory="templates")

        return templates.TemplateResponse("todo_form.html", {"request": request})
    

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


    @app.get("/table_todo", response_class=HTMLResponse)
    async def table_page(request : Request):

        templates = Jinja2Templates(directory="templates")

        return templates.TemplateResponse("table_todo.html", {"request": request})   

            
    @app.get("/get_todo")
    async def get_todo(request: Request):

        async with db_manager.localsession()() as db:

            get_todo = await db.execute(select(ContextDB))

            list_todo = get_todo.scalars().all()

            if not list_todo:

                return JSONResponse(content={"message": "Лист пустой"}, status_code=204)
            
            return list_todo

            

    @app.get("/get_todo_by_id/")
    async def get_by_id(id : int):

        async with db_manager.localsession()() as db:


            get_by_id = await db.execute(select(ContextDB).where(ContextDB.id == id))

            todo = get_by_id.scalars().first()

            if not todo:

                return("ID не найдено")


            return todo
                

    @app.delete("/delete_todo_by_id/")
    async def delete_todo(id: int):

        async with db_manager.localsession()() as db:

            delete_todo_id = await db.execute(select(ContextDB).where(ContextDB.id == id))

            if not delete_todo_id:

                return ("ID TODO удалено или не найдено")

            db.delete(delete_todo_id.first())

            await db.commit()

            return (f"TOdO с ID : {id} удалена") 

            
            
    


