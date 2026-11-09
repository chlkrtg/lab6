from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel, Field

from app.logger import logger

router = APIRouter(prefix="/items", tags=["items"])

fake_db: dict[int, dict] = {
    1: {"name": "Foo", "price": 50.2},
    2: {"name": "Телефон", "price": 50.2},
}


class Item(BaseModel):
    name: str = Field(..., title="Название", json_schema_extra={"example": "Ноутбук"})
    price: float = Field(..., gt=0, title="Цена", json_schema_extra={"example": 199.99})
    is_offer: bool | None = Field(None, title="Акционный товар")


@router.get("/{item_id}")
def read_item(
        item_id: int = Path(..., title="ID товара", ge=1),
        q: str | None = Query(None, title="Поисковый запрос", max_length=50),
):
    logger.info("GET /items/%s q=%s", item_id, q)

    if item_id not in fake_db:
        logger.warning("Item %s not found", item_id)
        raise HTTPException(status_code=404, detail="Item not found")

    return {"item_id": item_id, "item": fake_db[item_id], "q": q}


@router.post("/", response_model=Item)
def create_item(item: Item):
    logger.info("POST /items/ name=%s", item.name)

    for existing_item in fake_db.values():
        if existing_item["name"] == item.name:
            logger.warning("Item with name '%s' already exists", item.name)
            raise HTTPException(
                status_code=409,
                detail=f"Item with name '{item.name}' already exists",
            )
    new_id = max(fake_db.keys(), default=0) + 1
    fake_db[new_id] = item.model_dump()

    return item


@router.put("/{item_id}", response_model=Item)
def update_item(
        item: Item,
        item_id: int = Path(..., title="ID товара", ge=1)  # Потом параметры пути
):
    logger.info("PUT /items/%s name=%s", item_id, item.name)

    if item_id not in fake_db:
        logger.warning("Item %s not found for update", item_id)
        raise HTTPException(status_code=404, detail="Item not found")

    for other_id, other in fake_db.items():
        if other_id != item_id and other["name"] == item.name:
            logger.warning("Update failed: Item with name '%s' already exists", item.name)
            raise HTTPException(
                status_code=409,
                detail=f"Item with name '{item.name}' already exists",
            )

    fake_db[item_id] = item.model_dump()
    logger.info("Item %s updated successfully", item_id)

    return item