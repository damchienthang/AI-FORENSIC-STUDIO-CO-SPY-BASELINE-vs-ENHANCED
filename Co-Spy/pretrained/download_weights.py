import os
import sys
import zipfile
import requests

PRETRAINED_DIR = os.path.abspath(r"c:\Nam 4 ki 1\Xu ly anh\BTL\Co-Spy\pretrained")
os.makedirs(PRETRAINED_DIR, exist_ok=True)

files = [
    ("progan.zip", "https://huggingface.co/ruojiruoli/Co-Spy-Pretrained-Weights/resolve/main/progan.zip"),
    ("sd-v1_4.zip", "https://huggingface.co/ruojiruoli/Co-Spy-Pretrained-Weights/resolve/main/sd-v1_4.zip")
]

for filename, url in files:
    zip_path = os.path.join(PRETRAINED_DIR, filename)
    target_folder_name = filename.replace(".zip", "")
    target_folder = os.path.join(PRETRAINED_DIR, target_folder_name)
    
    if os.path.exists(target_folder) and os.listdir(target_folder):
        print(f"{target_folder_name} already exists and is not empty. Skipping.")
        continue

    print(f"Downloading {filename} from {url}...")
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        downloaded = 0
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        sys.stdout.write(f"\r{filename}: {downloaded / (1024*1024):.1f}/{total_size / (1024*1024):.1f} MB ({(downloaded/total_size)*100:.1f}%)")
                    else:
                        sys.stdout.write(f"\r{filename}: {downloaded / (1024*1024):.1f} MB")
                    sys.stdout.flush()
    print(f"\nExtracting {filename}...")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(PRETRAINED_DIR)
    
    if os.path.exists(zip_path):
        os.remove(zip_path)
    print(f"{filename} successfully downloaded and extracted!")

print("All weights are ready!")

