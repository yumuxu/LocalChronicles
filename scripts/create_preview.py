import json

input_file = r"f:\adsense\LocalChronicles\fujian\八闽通志_refined.json"
output_file = r"f:\adsense\LocalChronicles\fujian\八闽通志_refined_preview.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Take first 5 items
preview_data = data[:5]

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(preview_data, f, ensure_ascii=False, indent=2)

print(f"Preview created at {output_file}")
