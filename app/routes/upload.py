from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import shutil
import aiofiles
import os

# Router untuk upload
router = APIRouter()

# Direktori untuk menyimpan file
UPLOAD_DIRECTORY = Path("uploaded_files")
UPLOAD_DIRECTORY.mkdir(exist_ok=True)  # Membuat folder jika belum ada

@router.post("/upload-map-sketch/")
async def upload_map_sketch(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        return {"error": "Invalid file type. Please upload an image."}
    
    file_path = UPLOAD_DIRECTORY / file.filename
    async with aiofiles.open(file_path, 'wb') as buffer:
        while content := await file.read(1024 * 1024):
            await buffer.write(content)
    
    return {"filename": file.filename}


@router.get("/get-map-sketch/{filename}")
async def get_map_sketch(filename: str):
    file_path = UPLOAD_DIRECTORY / filename
    if not file_path.exists():
        return {"error": "File not found."}
    return FileResponse(file_path)

# Endpoint baru untuk mendapatkan daftar semua file
@router.get("/list-map-sketches/")
async def list_map_sketches():
    try:
        # Ambil daftar semua file di direktori
        files = os.listdir(UPLOAD_DIRECTORY)
        # Filter hanya file gambar (opsional)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        return JSONResponse(content={"files": image_files})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint untuk menghapus file
@router.delete("/delete-map-sketch/{filename}")
async def delete_map_sketch(filename: str):
    file_path = UPLOAD_DIRECTORY / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    
    try:
        os.remove(file_path)
        return {"message": f"File {filename} berhasil dihapus."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint untuk memperbarui file
@router.put("/update-map-sketch/{filename}")
async def update_map_sketch(filename: str, file: UploadFile = File(...)):
    file_path = UPLOAD_DIRECTORY / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    try:
        # Hapus file lama
        os.remove(file_path)
        # Simpan file baru
        async with aiofiles.open(file_path, 'wb') as buffer:
            while content := await file.read(1024 * 1024):
                await buffer.write(content)
        
        return {"message": f"File {filename} berhasil diperbarui.", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
