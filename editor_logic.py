import subprocess
import json
import os

EDITOR_EXE = "./editor_linux"
TEMP_JSON = "temp_editor_data.json"

def check_editor():
    if not os.path.exists(EDITOR_EXE):
        raise FileNotFoundError("editor.exe introuvable dans le dossier racine.")

def decrypt_save(sav_path):
    check_editor()
    cmd = f'"{EDITOR_EXE}" sample "{sav_path}" --patch="{TEMP_JSON}"'
    subprocess.run(cmd, shell=True, check=True)
    with open(TEMP_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    os.remove(TEMP_JSON)
    return data

def compile_save(sav_path, data, output_path):
    check_editor()
    with open(TEMP_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    cmd = f'"{EDITOR_EXE}" update "{sav_path}" --patch="{TEMP_JSON}" --output="{output_path}"'
    subprocess.run(cmd, shell=True, check=True)
    if os.path.exists(TEMP_JSON):
        os.remove(TEMP_JSON)