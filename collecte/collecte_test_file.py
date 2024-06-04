import json
import os

if __name__ == '__main__':

    RAW_DATA_PATH = os.getenv("RAW_DATA_PATH")
    
    data = {"ok": "ok"}

    path = os.path.join(RAW_DATA_PATH, "test")
    if not os.path.exists(path):
        os.mkdir(path)
        
    file_path = f"{path}/test.json"

    with open(file_path, 'w') as output_file:
        json.dump(data, output_file, indent=2, ensure_ascii=False)