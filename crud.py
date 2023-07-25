from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy import cast, String
from uuid import UUID
from models import Dish, Submenu, Menu


def get_menu(db: Session, id: UUID):
    menu = db.query(Menu).filter(cast(Menu.id, String) == str(id)).first()
    if menu is None:
        return JSONResponse(content={"detail":"menu not found"}, status_code=404)
    else:
        submenus_count = len(menu.submenus)
        dishes_count = sum([len(submenu.dishes) for submenu in menu.submenus])
        return JSONResponse(content={"id": str(menu.id), "title": menu.title, "description": menu.description, "dishes_count": dishes_count, "submenus_count": submenus_count}, status_code=200)

def create_menu(db: Session, title: str, description: str):
    menu = Menu(title=title, description=description)
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return JSONResponse(content={"id": str(menu.id), "title": menu.title, "description": menu.description}, status_code=201)

def update_menu(db: Session, id: UUID, title: str, description: str):
    menu = db.query(Menu).filter(cast(Menu.id, String) == str(id)).first()
    if title is not None:
        menu.title = title
    if description is not None:
        menu.description = description
    db.commit()
    menu = db.query(Menu).filter(cast(Menu.id, String) == str(id)).first()
    return JSONResponse(content={"id": str(menu.id), "title": menu.title, "description": menu.description}, status_code=200)

def delete_menu(db: Session, id: UUID):
    menu = db.query(Menu).filter(cast(Menu.id, String) == str(id)).first()
    db.delete(menu)
    db.commit()
    return JSONResponse(content={"id": str(menu.id), "title": menu.title, "description": menu.description}, status_code=200)

def get_submenu(db: Session, menu_id: UUID, submenu_id: UUID):
    submenu = db.query(Submenu).filter(cast(Submenu.id, String) == str(submenu_id), Submenu.menu_id == menu_id).first()
    if submenu is None:
        return JSONResponse(content={"detail":"submenu not found"}, status_code=404)
    else:
        dishes_count = len(submenu.dishes)
        return JSONResponse(content={"id": str(submenu.id), "title": submenu.title, "description": submenu.description, "dishes_count": dishes_count}, status_code=200)

def create_submenu(db: Session, title: str, description: str, menu_id: UUID):
    submenu = Submenu(title=title, description=description, menu_id=menu_id)
    menu = db.query(Menu).filter(cast(Menu.id, String) == str(menu_id)).first()
    menu.submenus.append(submenu)
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return JSONResponse(content={"id": str(submenu.id), "title": submenu.title, "description": submenu.description}, status_code=201)

def update_submenu(db: Session, id: UUID, title: str, description: str):
    submenu = db.query(Submenu).filter(cast(Submenu.id, String) == str(id)).first()
    if title is not None:
        submenu.title = title
    if description is not None:
        submenu.description = description
    db.commit()
    submenu = db.query(Submenu).filter(cast(Submenu.id, String) == str(id)).first()
    return JSONResponse(content={"id": str(submenu.id), "title": submenu.title, "description": submenu.description}, status_code=200)

def delete_submenu(db: Session, id: UUID):
    submenu = db.query(Submenu).filter(cast(Submenu.id, String) == str(id)).first()
    db.delete(submenu)
    db.commit()
    return JSONResponse(content={"id": str(submenu.id), "title": submenu.title, "description": submenu.description}, status_code=200)

def get_dishes(db: Session, dish_id: UUID, submenu_id: UUID):
    dish = db.query(Dish).filter(cast(Dish.id, String) == str(dish_id), Dish.submenu_id == submenu_id).first()
    if dish is None:
        return JSONResponse(content={"detail":"dish not found"}, status_code=404)
    else:
        return JSONResponse(content={"id": str(dish.id), "title": dish.title, "description": dish.description, "price": dish.price}, status_code=200)

def create_dish(db: Session, title: str, price: str, description: str, submenu_id: UUID):
    dish = Dish(title=title, description=description, price=price, submenu_id=submenu_id)
    submenu = db.query(Submenu).filter(cast(Submenu.id, String) == str(submenu_id)).first()
    submenu.dishes.append(dish)
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return JSONResponse(content={"id": str(dish.id), "title": dish.title, "description": dish.description, "price": dish.price}, status_code=201)

def update_dish(db: Session, id: UUID, title: str, price: float, description: str):
    dish = db.query(Dish).filter(cast(Dish.id, String) == str(id)).first()
    if title is not None:
        dish.title = title
    if description is not None:
        dish.description = description
    if price is not None:
        dish.price = price
    db.commit()
    dish = db.query(Dish).filter(cast(Dish.id, String) == str(id)).first()
    return JSONResponse(content={"id": str(dish.id), "title": dish.title, "description": dish.description, "price": dish.price}, status_code=200)

def delete_dish(db: Session, id: UUID):
    dish = db.query(Dish).filter(cast(Dish.id, String) == str(id)).first()
    db.delete(dish)
    db.commit()
    return JSONResponse(content={"id": str(dish.id), "title": dish.title, "description": dish.description, "price": dish.price}, status_code=200)