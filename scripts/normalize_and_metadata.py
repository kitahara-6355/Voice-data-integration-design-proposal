# normalize_and_metadata.py
# Usage: python normalize_and_metadata.py
import os, csv, shutil, datetime
from pathlib import Path

SRC = Path('storage/raw')
DST = Path('storage/processed')
DST.mkdir(parents=True, exist_ok=True)

rows = []
for root, dirs, files in os.walk(SRC):
    for fn in files:
        p = Path(root) / fn
        # Skip empty or very small files
        if p.stat().st_size < 10:
            continue
        st = p.stat()
        mtime = datetime.datetime.fromtimestamp(st.st_mtime)
        date = mtime.strftime('%Y-%m-%d')
        ext = p.suffix.lower()
        safe_name = f"{date}_unknown_{p.name}"

        sub_dir_map = {
            '.m4a': 'audio',
            '.wav': 'audio',
            '.txt': 'text',
            '.pdf': 'pdf',
        }

        sub_dir_name = sub_dir_map.get(ext, 'other')
        sub = DST / sub_dir_name

        sub.mkdir(parents=True, exist_ok=True)
        dst_path = sub / safe_name
        shutil.copy2(p, dst_path)
        rows.append({
            'original_path': str(p),
            'stored_path': str(dst_path),
            'file_name': safe_name,
            'file_type': ext.strip('.'),
            'date_recorded': date,
            'size_bytes': st.st_size
        })

if rows:
    with open(DST / "metadata.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Normalization complete. metadata.csv created at {DST / 'metadata.csv'}")
else:
    print("No files found to process in 'storage/raw'.")
