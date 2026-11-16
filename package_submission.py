import os
import zipfile
from pathlib import Path

def make_submission_zip(student_id="25127344"):
    base_dir = Path(__file__).resolve().parent
    zip_path = base_dir / f"{student_id}.zip"
    
    files_to_include = [
        "app.py",
        "rag.py",
        "firebase_client.py",
        "knowledge_base.json",
        "requirements.txt",
        ".env.example",
        ".gitignore",
        "README.md",
        "test_rag.py"
    ]
    
    print(f"Creating submission archive: {zip_path.name}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for fname in files_to_include:
            fpath = base_dir / fname
            if fpath.exists():
                zipf.write(fpath, arcname=fname)
                print(f" + Added {fname}")
            else:
                print(f" ! Warning: file not found: {fname}")
                
    print(f"\nCreated successfully! Archive size: {os.path.getsize(zip_path)} bytes.")
    
    # Verify contents
    with zipfile.ZipFile(zip_path, "r") as zipf:
        namelist = zipf.namelist()
        print("\nVerifying archive contents:")
        for name in namelist:
            print(f" - {name}")
        if ".env" in namelist:
            raise RuntimeError("CRITICAL ERROR: .env is in the zip file!")
        else:
            print("\n[OK] .env is NOT in the archive. Safe for submission.")

if __name__ == "__main__":
    make_submission_zip()
