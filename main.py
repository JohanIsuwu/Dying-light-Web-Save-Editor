from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil
import os
import stat
import editor_logic
import constants

app = FastAPI()

os.makedirs("static", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

class SaveData(BaseModel):
    filename: str
    data: dict

@app.get("/api/constants")
async def get_constants():
    items_db = constants.get_valid_items()
    return {
        "skills": constants.HARDCODED_SKILLS,
        "buffs": constants.HARDCODED_BUFFS,
        "craftplans": constants.HARDCODED_CRAFTPLANS,
        "itemsDatabase": items_db,
        "itemsList": sorted(list(items_db.keys()))
    }

@app.post("/api/upload-cli")
async def upload_cli(file: UploadFile = File(...)):
    cli_path = os.path.join("uploads", "editor_cli")
    with open(cli_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        st = os.stat(cli_path)
        os.chmod(cli_path, st.st_mode | stat.S_IEXEC)
    except:
        pass
    return {"status": "success"}

@app.post("/api/upload")
async def upload_save(file: UploadFile = File(...)):
    file_path = os.path.join("uploads", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        data = editor_logic.decrypt_save(file_path)
        return {"filename": file.filename, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/save")
async def save_changes(payload: SaveData):
    input_path = os.path.join("uploads", payload.filename)
    output_path = os.path.join("uploads", f"mod_{payload.filename}")
    
    if not os.path.exists(input_path):
        raise HTTPException(status_code=404, detail="Original save file not found")
        
    try:
        editor_logic.compile_save(input_path, payload.data, output_path)
        return FileResponse(path=output_path, filename=f"mod_{payload.filename}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))