import os
from pathlib import Path

import aiofiles
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image
import imghdr

# Router untuk upload
router = APIRouter()

# Direktori untuk menyimpan file
cwd = os.getcwd()
UPLOAD_DIRECTORY = Path.cwd() / "src/infrastructure/storage/uploaded_files"
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


def get_image_format(file_path):
    """Mendeteksi format gambar menggunakan Pillow"""
    try:
        with Image.open(file_path) as img:
            return img.format.lower()  # Mengembalikan format seperti 'jpeg', 'png', 'avif', dll.
    except Exception as e:
        print(f"Error membaca gambar: {e}")
        return None
    

async def convert_avif_to_jpg(file_path: Path):
    """Konversi file AVIF ke JPG menggunakan Pillow"""
    try:
        img = Image.open(file_path)
        converted_path = file_path.with_suffix(".jpg")
        img.convert("RGB").save(converted_path, "JPEG")
        return converted_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Konversi AVIF gagal: {str(e)}")


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIRECTORY / file.filename
    async with aiofiles.open(file_path, "wb") as buffer:
        while content := await file.read(1024 * 1024):
            await buffer.write(content)
            
    # Deteksi jenis file setelah tersimpan
    file_type = get_image_format(file_path)
    print(file_type, "-------------")
    # Jika file AVIF, lakukan konversi ke JPG
    if file_type == "avif":
        converted_path = await convert_avif_to_jpg(file_path)
        os.remove(file_path)  # Hapus file asli (opsional)
        print(converted_path.name)
        return {
            "message": f"File {file.filename} diunggah dan dikonversi ke JPEG.",
            "filename": converted_path.name,
        }
        
    return {"message": f"File {file.filename} berhasil diunggah.", "filename": file.filename}


@router.get("/get/{filename}")
async def get_file(filename: str):
    """Mengambil file berdasarkan nama"""
    file_path = UPLOAD_DIRECTORY / filename
    if not file_path.exists():
        return {"error": "File not found."}
    return FileResponse(file_path)


# Endpoint baru untuk mendapatkan daftar semua file
@router.get("/list/")
async def list_files():
    """Mendapatkan daftar semua file dalam direktori upload"""
    try:
        # Ambil daftar semua file di direktori
        files = os.listdir(UPLOAD_DIRECTORY)
        return JSONResponse(content={"files": files})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint untuk menghapus file
@router.delete("/delete/{filename}")
async def delete_file(filename: str):
    """Menghapus file berdasarkan nama"""
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
    """Memperbarui file dengan file baru"""
    file_path = UPLOAD_DIRECTORY / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    try:
        os.remove(file_path) # Hapus file lama
        
        # Simpan file baru
        async with aiofiles.open(file_path, "wb") as buffer:
            while content := await file.read(1024 * 1024):
                await buffer.write(content)
                
        # Deteksi jenis file setelah tersimpan
        file_type = imghdr.what(file_path)

        # Jika file AVIF, lakukan konversi ke JPG
        if file_type == "avif":
            converted_path = await convert_avif_to_jpg(file_path)
            os.remove(file_path)  # Hapus file asli (opsional)
            return {
                "message": f"File {filename} diperbarui dan dikonversi ke JPEG.",
                "filename": converted_path.name,
            }    
                
        return {
            "message": f"File {filename} berhasil diperbarui.",
            "filename": file.filename,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    