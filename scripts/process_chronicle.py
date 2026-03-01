import re
import json
import os

# Configuration
INPUT_FILES = [
    r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 上册\八闽通志（修订本） 上册_ocr_result.txt",
    r"f:\adsense\LocalChronicles\fujian\八闽通志（修订本） 下册\八闽通志（修订本） 下册_ocr_result.txt"
]
OUTPUT_FILE = r"f:\adsense\LocalChronicles\fujian\八闽通志_refined.json"

# Patterns
PAGE_SEPARATOR = re.compile(r"^--- .*?_page_\d+\.png ---$")
FOOTNOTE_PATTERN = re.compile(r"\[\d+\]")

# Strict Volume Pattern: Must start with 八闽通志 to avoid TOC
# Allow spaces in volume number (e.g. "卷之 七 十")
JUAN_PATTERN = re.compile(r"^\s*八闽通志\s*卷之\s*([一二三四五六七八九十百\s]+)(.*)$")

NOISE_PATTERNS = [
    re.compile(r"^\s*八闽通志\s*$"),
    re.compile(r"^\s*（修订本）\s*$"),
    re.compile(r"^\s*[上下]册\s*$"),
    re.compile(r"^\s*\d+\s*$"), # Pure numbers
    re.compile(r"^\s*第\s*\d+\s*页\s*$"),
    re.compile(r"^\s*###\s*[.…_]+\s*$"),
    re.compile(r"^\s*\(\d+\)\s*$"),
    re.compile(r"^\s*H通心\s*$"),
    re.compile(r"^\s*社电\s*$"),
    re.compile(r"^\s*15日N7.*$"),
    re.compile(r"^\s*ISBN.*$"),
    re.compile(r"^\s*定价：.*$"),
    re.compile(r"^\s*目录\s*$"),
    re.compile(r"^\s*八闽通志序.*$"),
    re.compile(r"^\s*八闽通志凡例.*$"),
    re.compile(r"^\s*OCR Results.*$"),
    re.compile(r"^\s*===+.*$"),
    re.compile(r"^--- .*?_page_\d+\.png ---$"),
]

# Prefectures and Counties
PREFECTURES = {
    "福州府", "建宁府", "泉州府", "漳州府", "汀州府", "延平府", "邵武府", "兴化府", "福宁州",
    "福建等处承宣布政使司", "福建都指挥使司", "福建行都指挥使司", "福建等处提刑按察司", # Top level
    "怀安县", "长乐县", "连江县", "福清县", "古田县", "永福县", "闽清县", "罗源县", # Fuzhou
    "瓯宁县", "浦城县", "建阳县", "松溪县", "崇安县", "政和县", # Jianning
    "晋江县", "同安县", "德化县", "永春县", "安溪县", "惠安县", "南安县", # Quanzhou
    "龙溪县", "漳浦县", "龙岩县", "南靖县", "长泰县", # Zhangzhou
    "长汀县", "宁化县", "上杭县", "武平县", "清流县", "连城县", # Tingzhou
    "南平县", "将乐县", "沙县", "尤溪县", "顺昌县", "永安县", # Yanping
    "邵武县", "光泽县", "泰宁县", "建宁县", # Shaowu
    "莆田县", "仙游县", # Xinghua
    "宁德县", "福安县", "寿宁县" # Funing
}

# Categories (Main + Sub)
CATEGORIES = {
    "地理", "食货", "选举", "秩官", "人物", "艺文", "杂志", "寺观", "古迹", "兵防", "祥异", "丛谈", "外纪", "学校", "封爵", "宫室", "桥梁", "建置",
    "建置沿革", "郡名", "分野", "疆域", "形胜", "风俗", "里至", "山川", "城池", "坊市", "乡都", "户口", "土贡", "财赋", "潮汐",
    "公署", "郡县", "职官", "名宦", "流寓", "孝义", "节烈", "隐逸", "方技", "释老", "仙释", "物产"
}

# Common Products
PRODUCTS = {
    "茶", "荔枝", "龙眼", "橄榄", "纸", "铁", "银", "盐", "鱼", "瓷器", "丝", "棉", "漆", "杉木", "笋", "香菇", "茶叶", "布", "绢"
}

class ChronicleProcessor:
    def __init__(self):
        self.output_data = []
        self.buffer = []
        self.current_volume = ""
        self.current_prefecture = ""
        self.current_category = ""
    
    def clean_line(self, line):
        line = line.strip()
        for pattern in NOISE_PATTERNS:
            if pattern.match(line):
                return ""
        
        # Remove Footnotes [1], [2] etc.
        line = FOOTNOTE_PATTERN.sub("", line)

        # OCR Corrections (Contextual)
        if "偏" in line and ("建" in line or "州" in line or "政" in line):
             line = line.replace("偏", "福")
        
        return line

    def _cn_to_int(self, cn_num):
        mapping = {
            '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
            '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
            '百': 100
        }
        if not cn_num: return 0
        
        total = 0
        temp = 0
        for char in cn_num:
            if char in mapping:
                val = mapping[char]
                if val == 10 or val == 100:
                    if temp == 0: temp = 1
                    total += temp * val
                    temp = 0
                else:
                    temp = val
        total += temp
        return total

    def extract_entities(self, text):
        entities = {
            "locations": [],
            "people": [],
            "products": []
        }
        
        # Locations
        for loc in PREFECTURES:
            if loc in text:
                if loc not in entities["locations"]:
                    entities["locations"].append(loc)
        
        # Products
        for prod in PRODUCTS:
            if prod in text:
                if prod not in entities["products"]:
                    entities["products"].append(prod)

        return entities

    def flush_buffer(self):
        if not self.buffer:
            return
            
        text = "\n".join(self.buffer).strip()
        if not text:
            self.buffer = []
            return
        
        # If we haven't found a volume yet, and the text is short/garbage, skip it
        # But if it's the preface (before Vol 1), we might want to keep it if it's meaningful?
        # The user wants structured data. Unstructured preface might be noise.
        # Let's STRICTLY require a volume to be set before outputting.
        if not self.current_volume:
            self.buffer = []
            return

        entities = self.extract_entities(text)
        
        # Generate English Summary Template
        # "Records regarding [Category] in [Prefecture] (Vol. [X]). First sentence: [Extract...]"
        vol_str = self.current_volume.replace("卷之", "")
        vol_int = self._cn_to_int(vol_str)
        pref = self.current_prefecture or "Fujian General"
        cat = self.current_category or "General"
        
        # Extract first meaningful sentence
        first_sentence = text.split("。")[0].replace("\n", " ").strip()
        if len(first_sentence) > 50:
            first_sentence = first_sentence[:50] + "..."
            
        summary = f"Records regarding {cat} in {pref} (Vol. {vol_int}). Excerpt: {first_sentence}"
        
        entry = {
            "meta": {
                "volume": self.current_volume,
                "prefecture": self.current_prefecture,
                "category": self.current_category
            },
            "content": {
                "original_text": text,
                "summary": summary,
                "entities": entities
            }
        }
        
        self.output_data.append(entry)
        self.buffer = []

    def process_line(self, line):
        line = self.clean_line(line)
        if not line:
            return

        # 1. Check for Volume Header (Strict)
        juan_match = JUAN_PATTERN.match(line)
        if juan_match:
            vol_raw = juan_match.group(1)
            vol_num = re.sub(r'\s+', '', vol_raw)
            if vol_raw != vol_num:
                print(f"DEBUG: Found volume with spaces: '{vol_raw}' -> '{vol_num}'")
            
            new_volume = f"卷之{vol_num}"
            remainder = juan_match.group(2).strip()
            
            # Skip running headers (same volume)
            if new_volume == self.current_volume:
                # If explicitly starts with 八闽通志 (which regex enforces), it's a NEW section start
                # UNLESS it's a duplicate of the header we just processed?
                # Usually running headers don't have "八闽通志" prefix in the middle of text, 
                # but might appear at top of page.
                # Since we filter NOISE "八闽通志", the regex only matches "八闽通志卷之..."
                # If this appears on top of page, it IS a running header if volume is same.
                pass
                # Actually, checking grep results, "八闽通志卷之X" appears exactly once per volume usually?
                # No, wait. 
                # Vol 1 file has 43 matches.
                # Vol 2 file has 44 matches.
                # Total 87. 
                # Total volumes 87.
                # This means "八闽通志卷之X" appears EXACTLY ONCE per volume start.
                # So if we see it, it IS a new volume or the start of the current volume.
                # If new_volume == current_volume, it might be a repeat (e.g. page break split?).
                # But since count matches exactly, we can treat it as a definitive marker.
                # We flush and update.
            
            self.flush_buffer()
            self.current_volume = new_volume
            # Optional: Reset category/prefecture on new volume?
            # Often the first line after volume header is category.
            # Let's keep them until overwritten.
            
            if remainder and remainder in CATEGORIES:
                self.current_category = remainder
            return

        # If no volume set yet, skip (TOC/Preface)
        if not self.current_volume:
            return

        # 2. Check for Split/Merged Headers
        # e.g. "山川泉州府"
        found_cat = None
        for cat in CATEGORIES:
            if line.startswith(cat):
                found_cat = cat
                break
        
        if found_cat:
            remainder = line[len(found_cat):].strip()
            # If remainder is empty, simple category match
            if not remainder:
                if line == self.current_category:
                    return # Skip running header
                self.flush_buffer()
                self.current_category = line
                return
            
            # If remainder is a prefecture
            if remainder in PREFECTURES:
                self.flush_buffer()
                self.current_category = found_cat
                self.current_prefecture = remainder
                return

        # 3. Check for Prefecture Header (Exact)
        if line in PREFECTURES:
            if line == self.current_prefecture:
                return
            self.flush_buffer()
            self.current_prefecture = line
            return
        
        # 4. Check for Category Header (Exact - if not caught by split check)
        if line in CATEGORIES:
            if line == self.current_category:
                return
            self.flush_buffer()
            self.current_category = line
            return

        # 5. Accumulate Text
        self.buffer.append(line)

    def process_files(self):
        print("Starting processing...")
        for file_path in INPUT_FILES:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue
                
            print(f"Reading {file_path}...")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    self.process_line(line)
        
        self.flush_buffer()
        
        # Write Output
        print(f"Writing output to {OUTPUT_FILE}...")
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.output_data, f, ensure_ascii=False, indent=2)
        print("Done.")

if __name__ == "__main__":
    processor = ChronicleProcessor()
    processor.process_files()
