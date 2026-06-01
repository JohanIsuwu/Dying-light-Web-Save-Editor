import subprocess
import json
import os
import stat

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EDITOR_EXE = os.path.join(BASE_DIR, "editor_linux")
TEMP_JSON = os.path.join(BASE_DIR, "temp_editor_data.json")

def check_editor():
    if not os.path.exists(EDITOR_EXE):
        raise FileNotFoundError(f"Missing executable: {EDITOR_EXE}")
    
    st = os.stat(EDITOR_EXE)
    os.chmod(EDITOR_EXE, st.st_mode | stat.S_IEXEC)

def decrypt_save(sav_path):
    check_editor()
    cmd = [EDITOR_EXE, "sample", sav_path, f"--patch={TEMP_JSON}"]
    subprocess.run(cmd, check=True)
    
    with open(TEMP_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if os.path.exists(TEMP_JSON):
        os.remove(TEMP_JSON)
        
    return data

def compile_save(sav_path, data, output_path):
    check_editor()
    
    with open(TEMP_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
    cmd = [EDITOR_EXE, "update", sav_path, f"--patch={TEMP_JSON}", f"--output={output_path}"]
    subprocess.run(cmd, check=True)
    
    if os.path.exists(TEMP_JSON):
        os.remove(TEMP_JSON)