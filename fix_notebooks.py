import json
from pathlib import Path

def fix_notebook(path: Path):
    try:
        nb = json.loads(path.read_text(encoding="utf-8"))
        if "metadata" in nb and "widgets" in nb["metadata"]:
            nb["metadata"].pop("widgets", None)
            path.write_text(json.dumps(nb, indent=2), encoding="utf-8")
            print(f"✔ Fixed: {path}")
        else:
            print(f"– Skipped (clean): {path}")
    except Exception as e:
        print(f"✖ Error in {path}: {e}")

root = Path(".")  # proje root'u

for notebook in root.rglob("*.ipynb"):
    fix_notebook(notebook)

print("\n🎉 All notebooks processed.")
