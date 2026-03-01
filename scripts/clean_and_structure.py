import re
import os

# Configuration
INPUT_FILES = [
    r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 上册\八闽通志（修订本） 上册_ocr_result.txt",
    r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 下册\八闽通志（修订本） 下册_ocr_result.txt"
]
OUTPUT_FILE = r"f:\adsense\LocalChronicles\fujian\八闽通志_refined.md"

# Patterns
PAGE_SEPARATOR = re.compile(r"^--- .*?_page_\d+\.png ---$")
# Allow optional text after the Juan number (e.g. Category name or content)
JUAN_PATTERN = re.compile(r"^\s*八?闽?通?志?卷之([一二三四五六七八九十百]+)(.*)$")
# Common headers/footers to remove
NOISE_PATTERNS = [
    re.compile(r"^\s*八闽通志\s*$"),
    re.compile(r"^\s*（修订本）\s*$"),
    re.compile(r"^\s*[上下]册\s*$"),
    re.compile(r"^\s*\d+\s*$"), # Pure numbers (page numbers)
    re.compile(r"^\s*第\s*\d+\s*页\s*$"),
    re.compile(r"^\s*###\s*[.…_]+\s*$"), # OCR noise like ### ...
    re.compile(r"^\s*\(\d+\)\s*$"), # Page numbers like (123)
    re.compile(r"^\s*H通心\s*$"), # Weird OCR artifact seen in logs
]

# Known Categories for Semantic Structure
CATEGORIES = {
    "地理", "食货", "选举", "秩官", "人物", "艺文", "杂志", "寺观", "古迹", "兵防", "祥异", "丛谈", "外纪", "学校", "封爵", "宫室", "桥梁", "建置",
    "建置沿革", "郡名", "分野", "疆域", "形胜", "风俗", "里至", "山川", "城池", "坊市", "乡都", "户口", "土贡", "财赋", "潮汐",
    "福州府", "建宁府", "泉州府", "漳州府", "汀州府", "延平府", "邵武府", "兴化府", "福宁州"
}

def clean_remainder(text):
    """Clean the remainder text after Volume header"""
    if not text:
        return ""
    # Remove common noise chars
    cleaned = re.sub(r"[.…_]", "", text).strip()
    return cleaned

def extract_categories(line):
    """Check if line contains one or more Category headers"""
    clean_line = line.strip()
    if clean_line in CATEGORIES:
        return [clean_line]
    
    # Check for concatenation of 2 categories (e.g. "山川泉州府")
    if len(clean_line) <= 10: # Only check short lines
        for i in range(2, len(clean_line)):
            part1 = clean_line[:i]
            part2 = clean_line[i:]
            if part1 in CATEGORIES and part2 in CATEGORIES:
                return [part1, part2]
    return []

def cn_to_arabic(cn_str):
    """Simple Chinese number to Arabic conversion for checking continuity"""
    cn_map = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '百': 100}
    val = 0
    temp_val = 0
    for char in cn_str:
        n = cn_map.get(char)
        if n is None: continue 
        
        if n == 100:
            val += temp_val * 100 if temp_val > 0 else 100
            temp_val = 0
        elif n == 10:
            val += temp_val * 10 if temp_val > 0 else 10
            temp_val = 0
        else:
            temp_val = n
    val += temp_val
    return val

def clean_and_structure():
    print(f"Starting refinement process...")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
        out_f.write("# 八闽通志 (Refined)\n\n")
        
        current_juan = 0
        
        for file_path in INPUT_FILES:
            if not os.path.exists(file_path):
                print(f"Warning: File not found {file_path}")
                continue
                
            print(f"Processing {os.path.basename(file_path)}...")
            
            with open(file_path, 'r', encoding='utf-8') as in_f:
                for line in in_f:
                    line = line.strip()
                    if not line: continue

                    # 1. Skip Page Separators
                    if PAGE_SEPARATOR.match(line):
                        continue
                        
                    # 2. Skip Noise (Headers/Footers)
                    is_noise = False
                    for pattern in NOISE_PATTERNS:
                        if pattern.match(line):
                            if "地理" in line:
                                print(f"DEBUG: Noise match '{line}' with pattern {pattern.pattern}")
                            is_noise = True
                            break
                    if is_noise:
                        continue
                    
                    # 3. Check for Structure (Juan)
                    juan_match = JUAN_PATTERN.match(line)
                    if juan_match:
                        juan_str = juan_match.group(1)
                        remainder = juan_match.group(2).strip()
                        
                        try:
                            juan_num = cn_to_arabic(juan_str)
                            
                            # Logic to handle repeated headers and outliers
                            if juan_num <= current_juan:
                                # Special case: Detect restart of volume numbering (e.g. TOC -> Content)
                                # If the drop is significant (e.g. > 5), assume it's a valid restart
                                if (current_juan - juan_num) > 5:
                                    print(f"  Detected volume sequence restart (drop {current_juan}->{juan_num}) at line: {line}")
                                    # Accept it
                                else:
                                    continue # Skip repeated or minor backward jumps (errors)
                            
                            # Heuristic: Only allow reasonable jumps (e.g. +1 to +10) to avoid OCR noise
                            # Exception: First header found (current_juan == 0)
                            if current_juan > 0 and (juan_num - current_juan) > 10:
                                print(f"  Skipping suspicious jump: Volume {current_juan} -> {juan_num} in {line}")
                                continue

                            # Valid new volume
                            out_f.write(f"\n## 卷之{juan_str} (Volume {juan_num})\n\n")
                            
                            cleaned_remainder = clean_remainder(remainder)
                            if cleaned_remainder:
                                out_f.write(f"### {cleaned_remainder}\n\n")
                            
                            current_juan = juan_num
                            continue # Skip writing the raw line
                        except:
                            pass # If conversion fails, write as is
                    
                    # 4. Check for Category
                    categories = extract_categories(line)
                    if categories:
                        for cat in categories:
                            out_f.write(f"### {cat}\n")
                        continue

                    # 5. Write Content
                    out_f.write(line + "\n")

    print(f"Refinement complete. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_and_structure()
