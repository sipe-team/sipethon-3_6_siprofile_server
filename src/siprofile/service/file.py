from fastapi import APIRouter, HTTPException
from typing import Optional, Dict
from ..models.models import File
from ..models.database import files_collection
from fastapi import FastAPI, HTTPException
from google.cloud import storage
from datetime import timedelta, datetime
import os

app = FastAPI()

# GCS Bucket Name
BUCKET_NAME = "siprofile"
router = APIRouter()


@router.get("/generate-presigned-url")
async def update_file(object_name: str, expiration_minutes: int = 15):
    """
        Presigned URL 생성 API
        - object_name: 업로드할 파일의 이름
        - expiration_minutes: Presigned URL의 만료 시간(기본 15분)
        """
    try:
        # GCS 클라이언트 생성
        client = storage.Client.from_service_account_json("src/resources/service-account-key.json")
        # client = storage.Client()
        # 버킷 가져오기
        bucket = client.bucket(BUCKET_NAME)
        # 객체(blob) 가져오기
        blob = bucket.blob(object_name)
        # Presigned URL 생성
        presigned_url = blob.generate_signed_url(
            version='v4',
            expiration=timedelta(minutes=expiration_minutes),
            method="PUT",  # 업로드용 URL
        )
        return {"url": presigned_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
