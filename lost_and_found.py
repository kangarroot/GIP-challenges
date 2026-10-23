from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum

app = FastAPI()
class Category(str, Enum):
    ELECTRONICS = "electronics"
    WALLETS_BAGS = "wallets_bags"
    KEYS = "keys"
    CLOTHING = "clothing"
    DOCUMENTS = "documents"
    JEWELRY = "jewelry"
    PETS = "pets"
    OTHER = "other"

class ItemType(str, Enum):
    LOST = "lost"
    FOUND = "found"
class Item(BaseModel):
    name: str
    category: Category
    type: ItemType 
    recovery: bool 
    description: str
    
items = {}
lost_items = {}
found_items = {}
def Match(item_id):
    item = items[item_id]
    if item.recovery:
        return
    if item.type == ItemType.FOUND:
        for id, i in lost_items.items():
            if i.category == item.category and i.name == item.name:
                items[item_id].recovery = True 
                found_items.pop(item_id)
                lost_items.pop(id)
                return "Item recovered" 
    else:
        for id, i in found_items.items():
            if i.category == item.category and i.name == item.name:
                items[item_id].recovery = True 
                found_items.pop(id)
                lost_items.pop(item_id)
                return "Item recovered"
    return "No match found"

@app.get("/")
def home():
    return {"message": "API is running"}

@app.get("/items/search")
def get_items(category: Category = None, type: ItemType = None, recovery: bool = None):
    result = {}
    for id, item in items.items():
        if (category == item.category or category is None) and (type == item.type or type is None) and (recovery is None or recovery == item.recovery):
            result[id] = item
    return result

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.post("/items/{item_id}/report")
def report_item(item_id: int, item: Item):
    if item_id in items:
        raise HTTPException(status_code=409, detail="An item with this id already exists")
    if item.type == ItemType.LOST:
        lost_items[item_id] = item
    else:
        found_items[item_id] = item
    items[item_id] = item
    return item

@app.patch("/items/{item_id}/recover")
def recover_item(item_id: int):
    if not item_id in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return Match(item_id)


@app.patch("/items/{item_id}")
def update(item_id, category: Category = None, name: str = None, description: str = None):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    if items[item_id].type == ItemType.LOST 
        if category != None:
            items[item_id].category = category
            lost_items[item_id].category = category
        if name != None:
            items[item_id].name = name
            lost_items[item_id].name = name 
        if description != None:
            items[item_id].description = description
            lost_items[item_id].description = description
    else:
        if category != None:
            items[item_id].category = category
            found_items[item_id].category = category
        if type != None:
            items[item_id].type = type
            found_items[item_id].type = type 
        if description != None:
            items[item_id].description = description
            found_items[item_id].description = description
    return items[item_id]


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    items.pop(item_id, None)
    found_items.pop(item_id, None)
    lost_items.pop(item_id, None)
    return {"deleted": item_id}
