import re
import os
import shutil

input_file = r"f:\adsense\LocalChronicles\fujian\知识库\八闽通志（修订本） 上册_ocr_result.txt"
output_dir = r"f:\adsense\LocalChronicles\volumes"

if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

chinese_nums = {'一':1, '二':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9, '十':10,
                '十一':11, '十二':12, '十三':13, '十四':14, '十五':15, '十六':16, '十七':17, '十八':18, '十九':19, '二十':20,
                '二十一':21, '二十二':22, '二十三':23, '二十四':24, '二十五':25, '二十六':26, '二十七':27, '二十八':28, '二十九':29, '三十':30,
                '三十一':31, '三十二':32, '三十三':33, '三十四':34, '三十五':35, '三十六':36, '三十七':37, '三十八':38, '三十九':39, '四十':40,
                '四十一':41, '四十二':42, '四十三':43}

category_order = [
    '地理', '风俗', '物产', '食货', '水利', '宫室', '寺观', '古迹', '丘墓',
    '秩官', '学校', '选举', '封爵', '人物', '艺文', '坛庙', '恤政', '辨疑', '拾遗'
]

def is_noise_line(line):
    line = line.strip()
    if not line:
        return True
    if re.match(r'^--- .+_page_\d+\.png ---$', line):
        return True
    if re.match(r'^[0-9]{1,3}$', line):
        return True
    if re.match(r'^ISBN[\s：:]*[\d\-]+$', line, re.IGNORECASE):
        return True
    if re.match(r'^定价[：:\s]*[\d.]+元?$', line, re.IGNORECASE):
        return True
    if re.match(r"^15日N7-211-05048-9$", line):
        return True
    if re.match(r'^9"787211"050482$', line):
        return True
    if re.match(r'^定价：80\.00元$', line):
        return True
    return False

def merge_paragraphs(lines):
    merged = []
    for line in lines:
        line = line.rstrip('\n')
        if not line:
            merged.append('')
            continue
        if merged and merged[-1] and line:
            if (line[0].isalpha() or line[0] in '的一是不了人我在有他这为之来' or 
                (len(line) > 0 and '\u4e00' <= line[0] <= '\u9fff')):
                merged[-1] = merged[-1] + line
            else:
                merged.append(line)
        else:
            merged.append(line)
    return merged

def extract_category(volume_lines):
    for line in volume_lines[:3]:
        line = line.strip()
        for cat in category_order:
            if cat in line:
                return cat
    return ''

def chinese_to_number(cn_str):
    cn_str = cn_str.strip()
    if cn_str in chinese_nums:
        return chinese_nums[cn_str]
    return None

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

volume_pattern = re.compile(r'^八闽通志卷之(.+)$')
volume_positions = []

for i, line in enumerate(lines):
    match = volume_pattern.match(line.strip())
    if match:
        cn_num = match.group(1)
        vol_num = chinese_to_number(cn_num)
        if vol_num:
            volume_positions.append((i, vol_num))

volume_positions.sort(key=lambda x: x[0])

seen_vols = set()
unique_positions = []
for pos, vol_num in volume_positions:
    if vol_num not in seen_vols:
        seen_vols.add(vol_num)
        unique_positions.append((pos, vol_num))
        print(f"找到卷 {vol_num} 在行 {pos+1}")

volume_positions = unique_positions

print(f"\n共找到 {len(volume_positions)} 卷\n")

for idx, (pos, vol_num) in enumerate(volume_positions):
    if idx + 1 < len(volume_positions):
        end_pos = volume_positions[idx + 1][0]
    else:
        end_pos = len(lines)
    
    volume_lines = lines[pos:end_pos]
    
    clean_lines = []
    for line in volume_lines:
        if not is_noise_line(line):
            clean_lines.append(line)
    
    merged_lines = merge_paragraphs(clean_lines)
    
    category = extract_category(volume_lines)
    if category:
        filename = f"卷{vol_num:02d}_{category}.txt"
    else:
        filename = f"卷{vol_num:02d}.txt"
    
    output_path = os.path.join(output_dir, filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(merged_lines))
    
    print(f"已保存: {filename} ({len(merged_lines)} 行)")

print(f"\n完成！共生成 {len(volume_positions)} 个文件")
