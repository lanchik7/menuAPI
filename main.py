from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crud import *
from baseModels import *


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1302@localhost/restaurant_menu"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Menu.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


@app.get('/api/v1/menus/')
def get_all_menus(db: Session = Depends(get_db)):
    return db.query(Menu).all()

@app.get('/api/v1/menus/{menu_id}/')
def gt_menu(menu_id: UUID, db: Session = Depends(get_db)):
    res = get_menu(id=menu_id, db=db)
    return res

@app.post('/api/v1/menus/')
def cr_menu(menu_data: MenuCreate, db: Session = Depends(get_db)):
    res = create_menu(title=menu_data.title, description=menu_data.description, db=db)
    return res

@app.delete('/api/v1/menus/{menu_id}/')
def del_menu(menu_id:UUID, db: Session = Depends(get_db)):
    res = delete_menu(id=menu_id, db=db)
    return res

@app.patch('/api/v1/menus/{menu_id}/')
def updaate_menu(menu_id: UUID,menu_data: MenuCreate, db: Session = Depends(get_db)):
    res = update_menu(id=menu_id, title=menu_data.title, description=menu_data.description, db=db)
    return res

@app.get('/api/v1/menus/{menu_id}/submenus/')
def get_all_submenu(db: Session = Depends(get_db)):
    return db.query(Submenu).all()

@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/')
def gt_menu(menu_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)):
    res = get_submenu(menu_id=menu_id, submenu_id=submenu_id, db=db)
    return res

@app.post('/api/v1/menus/{menu_id}/submenus/')
def cr_submenu(menu_id: UUID,submenu_data: SubMenuCreate, db: Session = Depends(get_db)):
    res = create_submenu(menu_id=menu_id, title=submenu_data.title, description=submenu_data.description, db=db)
    return res

@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/')
def updaate_submenu(submenu_id: UUID, menu_data: SubMenuCreate, db: Session = Depends(get_db)):
    res = update_submenu(id=submenu_id, title=menu_data.title, description=menu_data.description, db=db)
    return res

@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/')
def del_submenu(submenu_id:UUID, db: Session = Depends(get_db)):
    res = delete_submenu(id=submenu_id, db=db)
    return res

@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/')
def get_all_dishes(db: Session = Depends(get_db)):
    return db.query(Dish).all()

@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/')
def gt_dish(dish_id: UUID, submenu_id: UUID, db: Session = Depends(get_db)):
    res = get_dishes(submenu_id=submenu_id, dish_id=dish_id, db=db)
    return res

@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/')
def cr_dish(dish_data: DishCreate, submenu_id: UUID, db: Session = Depends(get_db)):
    res = create_dish(submenu_id=submenu_id, title=dish_data.title, description=dish_data.description, price=dish_data.price, db=db)
    return res

@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/')
def updaate_dish(dish_id: UUID, dish_data: DishCreate, db: Session = Depends(get_db)):
    res = update_dish(id=dish_id, title=dish_data.title, description=dish_data.description,price=dish_data.price, db=db)
    return res

@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/')
def del_dish(dish_id:UUID, db: Session = Depends(get_db)):
    res = delete_dish(id=dish_id, db=db)
    return res