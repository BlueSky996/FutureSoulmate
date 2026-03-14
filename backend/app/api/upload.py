from fastapi import APIRouter, UploadFile, File
import uuid
import shutil

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    filename = f"uploads/{uuid.uuid4()}.jpg"

    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"image_url": filename}