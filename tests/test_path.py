# diagnostic.py - Run this first to see your file structure
import os
import glob

print("=== CHECKING YOUR FILE STRUCTURE ===")
print(f"Current working directory: {os.getcwd()}")

# Check data directory
data_dir = "./data"
if os.path.exists(data_dir):
    print(f"\n📁 Files in '{data_dir}' folder:")
    files = os.listdir(data_dir)
    for file in files:
        full_path = os.path.join(data_dir, file)
        print(f"  - {file} (size: {os.path.getsize(full_path) if os.path.isfile(full_path) else 'folder'})")
else:
    print(f"\n❌ Data directory '{data_dir}' not found!")

# Check for any Excel files
print(f"\n🔍 Searching for Excel files:")
excel_files = glob.glob("**/*.xlsx", recursive=True) + glob.glob("**/*.xls", recursive=True)
if excel_files:
    for file in excel_files:
        print(f"  - {file}")
else:
    print("  No Excel files found!")
