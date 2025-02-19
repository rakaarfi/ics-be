import os
from pathlib import Path

import aiofiles
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse


# Router untuk upload
router = APIRouter()

# Direktori untuk menyimpan file
cwd = os.getcwd()
UPLOAD_DIRECTORY = Path.cwd() / "src/infrastructure/storage/uploaded_files"
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIRECTORY / file.filename
    async with aiofiles.open(file_path, "wb") as buffer:
        while content := await file.read(1024 * 1024):
            await buffer.write(content)
    return {"filename": file.filename}


@router.get("/get/{filename}")
async def get_file(filename: str):
    file_path = UPLOAD_DIRECTORY / filename
    if not file_path.exists():
        return {"error": "File not found."}
    return FileResponse(file_path)


# Endpoint baru untuk mendapatkan daftar semua file
@router.get("/list/")
async def list_files():
    try:
        # Ambil daftar semua file di direktori
        files = os.listdir(UPLOAD_DIRECTORY)
        return JSONResponse(content={"files": files})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint untuk menghapus file
@router.delete("/delete/{filename}")
async def delete_file(filename: str):
    file_path = UPLOAD_DIRECTORY / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    try:
        os.remove(file_path)
        return {"message": f"File {filename} berhasil dihapus."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint untuk memperbarui file
@router.put("/update/{filename}")
async def update_file(filename: str, file: UploadFile = File(...)):
    file_path = UPLOAD_DIRECTORY / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    try:
        # Hapus file lama
        os.remove(file_path)
        # Simpan file baru
        async with aiofiles.open(file_path, "wb") as buffer:
            while content := await file.read(1024 * 1024):
                await buffer.write(content)
        return {
            "message": f"File {filename} berhasil diperbarui.",
            "filename": file.filename,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    