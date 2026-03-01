import re
import os

files = [
    r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 上册\八闽通志（修订本） 上册_ocr_result.txt",
    r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 下册\八闽通志（修订本） 下册_ocr_result.txt"
]

juan_pattern = re.compile(r"卷之([一二三四五六七八九十百]+)")
category_pattern = re.compile(r"^[\u4e00-\u9fa5]{2,4}$") # Simple guess for now

def analyze_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Analyzing {os.path.basename(file_path)}...")
    juan_counts = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            # Check for Juan
            match = juan_pattern.search(line)
            if match:
                juan = match.group(0)
                juan_counts[juan] = juan_counts.get(juan, 0) + 1
                if juan_counts[juan] < 3:
                    print(f"  Found potential Juan marker: {line}")

    print(f"  Total unique Juan markers found: {len(juan_counts)}")
    # Print sorted juan to see if they are sequential
    print(f"  Juan list: {sorted(juan_counts.keys())}")

for f in files:
    analyze_file(f)
