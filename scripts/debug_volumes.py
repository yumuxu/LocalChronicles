import re

input_file = r"f:\adsense\LocalChronicles\fujian\知识库\八闽通志（修订本） 上册_ocr_result.txt"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"总行数: {len(lines)}")

volume_pattern = re.compile(r'^八闽通志卷之(\d+)$')

for i, line in enumerate(lines[665:675]):
    print(f"行 {i+665}: '{line.strip()}'")
    match = volume_pattern.match(line.strip())
    print(f"  匹配: {match}")
