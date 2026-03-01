import json
import re
import os

def clean_text(text):
    text = re.sub(r'\[(\d+)\]', r'[\1]', text)
    text = re.sub(r'\[\]', '', text)
    text = re.sub(r'[\-]+', '', text)
    text = re.sub(r'\s+', '', text)
    return text

def extract_location_hierarchy(full_text):
    hierarchy = {}
    
    prefectures = ['福州府', '建宁府', '泉州府', '漳州府', '汀州府', '延平府', '邵武府', '兴化府', '福宁州']
    
    for prefecture in prefectures:
        if prefecture in full_text:
            hierarchy[prefecture] = {}
            counties = re.findall(rf'{prefecture}([^{prefecture}]+?)(?:府|州)县', full_text)
            if counties:
                county_list = re.findall(r'([^\u4e00-\u9fff。，、\n]+?)县', counties[0])
                for county in county_list:
                    if county and len(county) > 0:
                        hierarchy[prefecture][county] = {}
    
    return hierarchy

def extract_historical_quotes(full_text):
    quotes = []
    
    book_refs = re.findall(r'《([^》]+)》', full_text)
    for book in list(set(book_refs))[:10]:
        quotes.append({
            "author": "未知",
            "source": book,
            "content": f"引用自《{book}》"
        })
    
    return quotes

def extract_time_events(full_text):
    events = []
    
    years = re.findall(r'([宋元明]+)(\d+)年', full_text)
    for dynasty, year in years[:10]:
        events.append({
            "dynasty": dynasty,
            "year": year,
            "event": "行政变更/地理命名"
        })
    
    return events

def extract_key_entities(full_text):
    entities = []
    
    names = re.findall(r'([\u4e00-\u9fff]{2,4})《[^》]+》', full_text)
    for name in list(set(names))[:10]:
        entities.append({
            "name": name,
            "role": "历史人物"
        })
    
    officials = re.findall(r'([\u4e00-\u9fff]{2,4})(郡守|县令|知州|节度使|刺史)', full_text)
    for name, title in list(set(officials))[:10]:
        entities.append({
            "name": name,
            "role": title
        })
    
    return entities

def extract_geomorphic(full_text):
    features = []
    
    mountains = re.findall(r'([\u4e00-\u9fff]+山)', full_text)
    rivers = re.findall(r'([\u4e00-\u9fff]+溪|[\u4e00-\u9fff]+江|[\u4e00-\u9fff]+水)', full_text)
    
    for m in list(set(mountains))[:20]:
        features.append(m)
    for r in list(set(rivers))[:20]:
        features.append(r)
    
    return features[:30]

def generate_summary(full_text, title):
    summary = f"本卷为《八闽志》记载"
    
    prefectures = ['福州府', '建宁府', '泉州府', '漳州府', '汀州府', '延平府', '邵武府', '兴化府']
    pref_count = sum(1 for p in prefectures if p in full_text)
    summary += f"涉及{pref_count}个府级行政区划，描述山川地理。"
    
    if '分野' in full_text:
        summary += "涉及天文分野。"
    if '人物' in title:
        summary = f"本卷主要记载福建历史人物及职官信息。"
    
    return summary[:150]

def process_volume_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    full_text = ''.join(lines)
    
    title_match = re.search(r'八闽通志卷之(\d+)([^\n]+)', lines[0] if lines else '')
    if title_match:
        vol_num = title_match.group(1)
        category = title_match.group(2).strip() if title_match.group(2) else '地理'
        title = f"八闽通志卷之{vol_num} {category}"
    else:
        title = "八闽通志"
    
    cleaned_text = clean_text(full_text)
    
    result = {
        "title": title,
        "location_hierarchy": extract_location_hierarchy(cleaned_text),
        "historical_quotes": extract_historical_quotes(full_text),
        "time_and_events": extract_time_events(full_text),
        "key_entities": extract_key_entities(full_text),
        "geomorphic_features": extract_geomorphic(cleaned_text),
        "modern_summary": generate_summary(full_text, title),
        "cleaned_full_text": cleaned_text[:5000] + "..." if len(cleaned_text) > 5000 else cleaned_text
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result

if __name__ == "__main__":
    volumes_dir = r"f:\adsense\LocalChronicles\volumes"
    output_dir = r"f:\adsense\LocalChronicles\structured_data"
    
    files = [f for f in os.listdir(volumes_dir) if f.endswith('.txt')]
    files.sort()
    
    print(f"找到 {len(files)} 个文件，开始处理...")
    
    for i, filename in enumerate(files):
        input_file = os.path.join(volumes_dir, filename)
        output_file = os.path.join(output_dir, filename.replace('.txt', '.json'))
        
        try:
            process_volume_file(input_file, output_file)
            print(f"[{i+1}/{len(files)}] 已处理: {filename}")
        except Exception as e:
            print(f"[{i+1}/{len(files)}] 处理失败: {filename} - {e}")
    
    print(f"\n完成！共处理 {len(files)} 个文件")
