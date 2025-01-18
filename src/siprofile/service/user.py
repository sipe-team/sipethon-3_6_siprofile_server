from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..models.models import (
    User,
    RequestCreateUser,
    RequestUpdateUser,
    RequestDeleteUser,
    RequestGetUser,
)
from ..models.database import users_collection
from ..utils.utils import generate_id, hash_password

router = APIRouter()


@router.post("/create", response_model=User)
async def create_user(user: RequestCreateUser):
    if user.password:
        user.password = hash_password(user.password)
    user_dict = user.dict()
    user_dict["created_at"] = datetime.now()
    user_dict["last_accessed_at"] = datetime.now()
    user_dict["user_id"] = generate_id(prefix="user")
    await users_collection.insert_one(user_dict)
    return User(**user_dict)


@router.put("/update", response_model=User)
async def update_user(user: RequestUpdateUser):
    print(user.user_id)
    user_data = await users_collection.find_one({"user_id": user.user_id})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.dict(exclude_unset=True)
    if update_data.get("name"):
        update_data["name"] = update_data["name"].strip()
    if update_data.get("password"):
        update_data["password"] = hash_password(update_data["password"])
    if update_data.get("profile_image"):
        # 프로필 이미지 업로드 로직 추가
        update_data["profile_image"] = update_data["profile_image"].strip()
    update_data["last_accessed_at"] = datetime.now()
    await users_collection.update_one({"user_id": user.user_id}, {"$set": update_data})
    user_data.update(update_data)
    return User(**user_data)


@router.delete("/delete")
async def delete_user(user: RequestDeleteUser):
    result = await users_collection.delete_one({"user_id": user.user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/get", response_model=User)
async def get_user(user: RequestGetUser):
    user_data = await users_collection.find_one({"user_id": user.user_id})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user_data)
