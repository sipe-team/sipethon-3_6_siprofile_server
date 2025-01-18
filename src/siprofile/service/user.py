from fastapi import APIRouter, HTTPException
from datetime import datetime
from hashlib import sha256
from bson import ObjectId
from ..models.models import User
from ..models.database import users_collection
from typing import Optional

router = APIRouter()


# 비밀번호 해시 함수
def hash_password(password: str) -> str:
    return sha256(password.encode()).hexdigest()


@router.post("/create", response_model=User)
async def create_user(user: User):
    if user.password:
        user.password = hash_password(user.password)
    user.created_at = datetime.now()
    user.last_accessed_at = datetime.now()
    user_dict = user.dict()
    result = await users_collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return user_dict


@router.put("/update", response_model=User)
async def update_user(
    user_id: str,
    name: Optional[str] = None,
    password: Optional[str] = None,
    profile_image: Optional[str] = None,
):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = {}
    if name:
        update_data["name"] = name
    if password:
        update_data["password"] = hash_password(password)
    if profile_image:
        update_data["profile_image"] = profile_image
    update_data["last_accessed_at"] = datetime.now()
    await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    user.update(update_data)
    return user


@router.delete("/delete")
async def delete_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}


@router.get("/get", response_model=User)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
