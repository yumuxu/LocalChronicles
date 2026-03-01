import json

with open(r"f:\adsense\LocalChronicles\fujian\八闽通志_refined.json", "r", encoding="utf-8") as f:
    data = json.load(f)

volumes = sorted(list(set(d["meta"]["volume"] for d in data)))
print(f"Total entries: {len(data)}")
print(f"Unique volumes: {len(volumes)}")
print("Volumes found:", volumes)

# Print a sample entry with products if any
print("\n--- Sample Entry with Products ---")
found_prod = False
for entry in data:
    if entry["content"]["entities"]["products"]:
        print(json.dumps(entry, ensure_ascii=False, indent=2))
        found_prod = True
        break

if not found_prod:
    print("No entries with products found.")

# Print a sample entry to check Summary
print("\n--- Sample Entry for Summary Check ---")
if data:
    print(json.dumps(data[0], ensure_ascii=False, indent=2))
