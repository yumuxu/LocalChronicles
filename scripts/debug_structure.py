import re

CATEGORIES = {
    "地理", "食货", "选举", "秩官", "人物", "艺文", "杂志", "寺观", "古迹", "兵防", "祥异", "丛谈", "外纪", "学校", "封爵", "宫室", "桥梁"
}

def is_category(line):
    """Check if line is a Category header"""
    clean_line = line.strip()
    return clean_line in CATEGORIES

lines = [
    "地理",
    "  地理  ",
    "地理\n",
    "人物",
    "建置沿革",
    "卷之一"
]

for line in lines:
    print(f"'{line.strip()}': {is_category(line)}")

# Check file content
file_path = r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 上册\八闽通志（修订本） 上册_ocr_result.txt"
with open(file_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if "地理" in line and len(line.strip()) < 5:
            print(f"Line {i+1}: '{line.strip()}' -> {is_category(line)}")
            # Show bytes
            print(f"Bytes: {line.strip().encode('utf-8')}")
        if i > 5000: break # Check first 5000 lines (Volume 1 starts around there?)
