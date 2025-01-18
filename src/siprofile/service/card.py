from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId
from typing import Optional, List
from ..models.models import Card
from ..models.database import cards_collection

router = APIRouter()


@router.post("/create", response_model=Card)
async def create_card(card: Card):
    card.created_at = datetime.now()
    card.updated_at = datetime.now()
    card_dict = card.dict()
    result = await cards_collection.insert_one(card_dict)
    card_dict["_id"] = str(result.inserted_id)
    return card_dict


@router.put("/update", response_model=Card)
async def update_card(
    card_id: str,
    name: Optional[str] = None,
    job: Optional[str] = None,
    labels: Optional[List[str]] = None,
    files: Optional[List[str]] = None,
    link: Optional[str] = None,
):
    card = await cards_collection.find_one({"_id": ObjectId(card_id)})
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    update_data = {}
    if name:
        update_data["name"] = name
    if job:
        update_data["job"] = job
    if labels:
        update_data["labels"] = labels
    if files:
        update_data["files"] = files
    if link:
        update_data["link"] = link
    update_data["updated_at"] = datetime.now()
    await cards_collection.update_one({"_id": ObjectId(card_id)}, {"$set": update_data})
    card.update(update_data)
    return card


@router.delete("/delete")
async def delete_card(card_id: str):
    result = await cards_collection.delete_one({"_id": ObjectId(card_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Card not found")
    return {"detail": "Card deleted"}


@router.get("/get", response_model=Card)
async def get_card(card_id: str):
    card = await cards_collection.find_one({"_id": ObjectId(card_id)})
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card


@router.put("/enable", response_model=Card)
async def enable_card(card_id: str):
    card = await cards_collection.find_one({"_id": ObjectId(card_id)})
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    await cards_collection.update_one(
        {"_id": ObjectId(card_id)}, {"$set": {"state": "ACTIVE"}}
    )
    await cards_collection.update_many(
        {"_id": {"$ne": ObjectId(card_id)}}, {"$set": {"state": "DEACTIVE"}}
    )
    card["state"] = "ACTIVE"
    return card


@router.put("/disable", response_model=Card)
async def disable_card(card_id: str):
    card = await cards_collection.find_one({"_id": ObjectId(card_id)})
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    await cards_collection.update_one(
        {"_id": ObjectId(card_id)}, {"$set": {"state": "DEACTIVE"}}
    )
    card["state"] = "DEACTIVE"
    return card
