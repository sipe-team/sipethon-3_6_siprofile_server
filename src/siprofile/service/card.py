import logging
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..models.models import (
    Card,
    RequestCreateCard,
    RequestUpdateCard,
    RequestDeleteCard,
    RequestGetCard,
    RequestEnableCard,
    RequestDisableCard,
    RequestListCards,
)
from ..models.database import cards_collection
from ..utils.utils import generate_id

_LOGGER = logging.getLogger(__name__)

router = APIRouter()


@router.post("/create", response_model=Card)
async def create_card(card: RequestCreateCard):
    card_dict = card.dict()
    card_dict["created_at"] = datetime.now()
    card_dict["updated_at"] = datetime.now()
    card_dict["card_id"] = generate_id(prefix="card")
    await cards_collection.insert_one(card_dict)
    return Card(**card_dict)


@router.put("/update", response_model=Card)
async def update_card(card: RequestUpdateCard):
    card_data = await cards_collection.find_one({"card_id": card.card_id})
    if not card_data:
        raise HTTPException(status_code=404, detail="Card not found")
    update_data = card.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.now()
    await cards_collection.update_one({"card_id": card.card_id}, {"$set": update_data})
    card_data.update(update_data)
    return Card(**card_data)


@router.delete("/delete")
async def delete_card(card: RequestDeleteCard):
    result = await cards_collection.delete_one({"card_id": card.card_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Card not found")


@router.get("/get", response_model=Card)
async def get_card(card: RequestGetCard):
    card_data = await cards_collection.find_one({"card_id": card.card_id})
    if not card_data:
        raise HTTPException(status_code=404, detail="Card not found")
    return Card(**card_data)


@router.put("/enable", response_model=Card)
async def enable_card(card: RequestEnableCard):
    card_data = await cards_collection.find_one({"card_id": card.card_id})
    if not card_data:
        raise HTTPException(status_code=404, detail="Card not found")
    await cards_collection.update_one(
        {"card_id": card.card_id}, {"$set": {"state": "ACTIVE"}}
    )
    card_data["state"] = "ACTIVE"
    return Card(**card_data)


@router.put("/disable", response_model=Card)
async def disable_card(card: RequestDisableCard):
    card_data = await cards_collection.find_one({"card_id": card.card_id})
    if not card_data:
        raise HTTPException(status_code=404, detail="Card not found")
    await cards_collection.update_one(
        {"card_id": card.card_id}, {"$set": {"state": "DEACTIVE"}}
    )
    card_data["state"] = "DEACTIVE"
    return Card(**card_data)


@router.get("/list", response_model=Dict[str, Any])
async def list_cards(
    job: Optional[str] = None,
    state: Optional[str] = None,
    labels: Optional[List[str]] = Query(None),
    user_id: Optional[str] = None
):
    query_dict = {}
    if job:
        query_dict["job"] = job
    if state:
        query_dict["state"] = state
    if labels:
        query_dict["labels"] = {"$in": labels}
    if user_id:
        query_dict["user_id"] = user_id

    _LOGGER.info(f"query_dict: {query_dict}")

    cards_cursor = cards_collection.find(query_dict)
    cards = await cards_cursor.to_list(length=100)
    total_count = await cards_collection.count_documents(query_dict)

    return {"results": [Card(**card) for card in cards], "total_count": total_count}
