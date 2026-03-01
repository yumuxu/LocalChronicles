import json
import re

def chinese_to_int(cn_num):
    # Handle basic Chinese numbers for volume numbering
    # e.g. 一, 二, 十, 十一, 二十, 一百
    mapping = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '百': 100
    }
    
    if not cn_num:
        return 0
        
    # Simple cases
    if cn_num in mapping:
        return mapping[cn_num]
        
    # Complex cases
    total = 0
    temp = 0
    for char in cn_num:
        if char in mapping:
            val = mapping[char]
            if val == 10 or val == 100:
                if temp == 0:
                    temp = 1
                total += temp * val
                temp = 0
            else:
                temp = val
    total += temp
    return total

with open(r"f:\adsense\LocalChronicles\fujian\八闽通志_refined.json", "r", encoding="utf-8") as f:
    data = json.load(f)

volumes = sorted(list(set(d["meta"]["volume"] for d in data)))
vol_map = {}

for vol in volumes:
    match = re.search(r"卷之(.+)", vol)
    if match:
        num_str = match.group(1).strip()
        num = chinese_to_int(num_str)
        vol_map[num] = vol

found_nums = sorted(vol_map.keys())
print(f"Found {len(found_nums)} unique volume numbers.")
print(f"Max volume found: {found_nums[-1] if found_nums else 0}")

expected = set(range(1, 88)) # Assuming 87 volumes
found = set(found_nums)
missing = sorted(list(expected - found))

if missing:
    print(f"Missing volumes ({len(missing)}): {missing}")
else:
    print("All volumes 1-87 found.")

# Check for duplicates or weird mappings
seen = {}
for vol in volumes:
    match = re.search(r"卷之(.+)", vol)
    if match:
        num_str = match.group(1).strip()
        num = chinese_to_int(num_str)
        if num in seen:
            print(f"Duplicate mapping for {num}: {seen[num]} and {vol}")
        seen[num] = vol
