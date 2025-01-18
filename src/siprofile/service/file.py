from fastapi import APIRouter, HTTPException
from typing import Optional, Dict
from ..models.models import File
from ..models.database import files_collection

router = APIRouter()


@router.put("/update", response_model=File)
async def update_file(file_id: str, reference: Optional[Dict[str, str]] = None):
    file = await files_collection.find_one({"file_id": file_id})
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    update_data = {}
    if reference:
        update_data["reference"] = reference
    await files_collection.update_one({"file_id": file_id}, {"$set": update_data})
    file.update(update_data)
    return file


@router.delete("/delete")
async def delete_file(file_id: str):
    result = await files_collection.delete_one({"file_id": file_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="File not found")
    return {"detail": "File deleted"}


@router.get("/get", response_model=File)
async def get_file(file_id: str):
    file = await files_collection.find_one({"file_id": file_id})
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file
