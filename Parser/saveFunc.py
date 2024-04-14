import json
from sqlalchemy import Connection
from Database.engine import add_record

def database_save_center(data:dict):
    add_record(data)

def saveJson(data:list, i:int):
    with open(f"Parser/DATA/ShoppingCenterData{i}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False) 

def saveImg(img, name:str):
    with open(f"Parser/DATA/IMG/{name}.jpg", "wb") as file:
        file.write(img)