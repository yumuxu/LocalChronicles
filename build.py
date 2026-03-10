#!/usr/bin/env python3
"""
Build script for Ba Min Tong Zhi static site.
Generates HTML pages from Jinja2 templates and structured JSON data.
"""

import json
import os
import re
import random
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown import markdown
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "structured_data"
TEMPLATE_DIR = PROJECT_ROOT / "templates"
DIST_DIR = PROJECT_ROOT / "dist"

def load_all_data():
    """Load all JSON files from structured_data directory."""
    data = {}
    for json_file in DATA_DIR.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data[json_file.stem] = json.load(f)
    return data

def get_volume_list(data):
    """Extract volume list with metadata."""
    volumes = []
    for vol_name, vol_data in data.items():
        match = re.search(r'卷(\d+)', vol_name)
        num = int(match.group(1)) if match else 999
        
        tags = []
        title = vol_data.get('title', vol_name)
        if '地理' in title:
            tags.append('Geography')
        if '食货' in title:
            tags.append('Economy')
        if '封爵' in title:
            tags.append('Nobility')
        if '水利' in title:
            tags.append('Water')
        
        volumes.append({
            'id': vol_name,
            'title': title,
            'number': num,
            'summary': vol_data.get('modern_summary', '')[:150],
            'tags': tags,
            'subtitle': vol_data.get('subtitle', ''),
            'category': vol_data.get('category', 'Historical'),
            'data': vol_data
        })
    
    volumes.sort(key=lambda x: x['number'])
    return volumes

def get_statistics(data):
    """Calculate statistics from data."""
    stats = {
        "total_volumes": len(data),
        "total_place_names": 0,
        "total_quotes": 0,
        "total_entities": 0
    }
    for vol_data in data.values():
        stats["total_place_names"] += len(vol_data.get("geomorphic_features", []))
        stats["total_quotes"] += len(vol_data.get("historical_quotes", []))
        stats["total_entities"] += len(vol_data.get("key_entities", []))
    return stats

def get_locations(vol_data):
    """Extract geographic locations from volume data."""
    locations = set()
    hierarchy = vol_data.get('location_hierarchy', {})
    for region, counties in hierarchy.items():
        locations.add(region)
        if isinstance(counties, dict):
            locations.update(counties.keys())
    return list(locations)[:10]

def get_related_volumes(current_vol_id, volumes):
    """Get adjacent volumes for navigation."""
    current_num = None
    for vol in volumes:
        if vol['id'] == current_vol_id:
            current_num = vol['number']
            break
    
    if current_num is None:
        return []
    
    related = []
    for vol in volumes:
        if vol['number'] == current_num + 1:
            related.append(vol)
            break
    
    return related[:2]

def format_content(vol_data):
    """Format volume content for display."""
    parts = []
    
    cleaned_text = vol_data.get('cleaned_full_text', '')
    if cleaned_text:
        segments = split_into_segments(cleaned_text)
        for i, segment in enumerate(segments):
            if not segment.strip():
                continue
            
            is_header = is_section_header(segment)
            if is_header:
                parts.append(f'''
                <h2 class="text-2xl font-bold text-primary mt-12 mb-6 pb-2 border-b border-primary/20 flex items-center gap-3">
                    <span class="material-symbols-outlined text-xl">bookmark</span>
                    {segment.strip()}
                </h2>
                ''')
            else:
                parts.append(f'''
                <p class="leading-8 mb-8 text-lg text-charcoal/90 dark:text-slate-300 font-serif text-justify indent-8">
                    {segment.strip()}
                </p>
                ''')
    
    quotes = vol_data.get('historical_quotes', [])
    if quotes:
        for quote in quotes[:3]:
            source = quote.get('source', 'Unknown')
            content = quote.get('content', '')
            if content:
                parts.append(f'''
                <div class="my-12 border-l-4 border-primary bg-primary/5 p-8 rounded-r-lg">
                    <p class="mb-4 text-xl font-serif leading-loose text-charcoal dark:text-white italic">
                        "{content[:300]}{'...' if len(content) > 300 else ''}"
                    </p>
                    <div class="flex items-center gap-2 text-sm font-medium uppercase tracking-wide text-primary">
                        <span class="h-px w-8 bg-primary"></span>
                        {source}
                    </div>
                </div>
                ''')
    
    return '\n'.join(parts) or '<p class="leading-loose mb-6 text-lg">Content available in the digital archive.</p>'


def split_into_segments(text):
    """Split text into logical segments based on section headers and paragraphs."""
    import re
    
    text = text.replace('卷之一', '').replace('卷之二', '').replace('卷之三', '')
    
    header_patterns = [
        '建置沿革', '州郡', '分野', '山川', '城池', '公署', '学校', '科举',
        '人物', '艺文', '风俗', '物产', '贡赋', '兵制', '驿传', '关隘',
        '桥梁', '寺观', '祠庙', '陵墓', '古迹'
    ]
    
    for header in header_patterns:
        text = text.replace(header, f'\n###{header}###\n')
    
    lines = text.split('\n')
    segments = []
    current_segment = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('###') and line.endswith('###'):
            if current_segment:
                combined = smart_join(current_segment)
                if combined:
                    segments.append(combined)
                current_segment = []
            segments.append(line[3:-3])
        else:
            current_segment.append(line)
            combined = ''.join(current_segment)
            
            if is_good_split_point(combined):
                segments.append(combined)
                current_segment = []
            elif len(combined) > 1200:
                split_pos = find_best_split(combined)
                if split_pos > 0:
                    segments.append(combined[:split_pos])
                    current_segment = [combined[split_pos:]]
    
    if current_segment:
        combined = smart_join(current_segment)
        if combined:
            segments.append(combined)
    
    return segments[:30]


def smart_join(segments):
    """Join segments while keeping parentheses together."""
    import re
    if not segments:
        return ''
    
    text = ''.join(segments)
    
    text = re.sub(r'([^。])(\n)(\s*)([^。])', r'\1\4', text)
    text = re.sub(r'（\s*([^）]*?)\s*）', lambda m: '（' + m.group(1).replace('\n', '').replace(' ', '') + '）', text)
    text = re.sub(r'\s+', '', text)
    
    return text


def is_good_split_point(text):
    """Check if this is a good point to split the text."""
    import re
    
    if not text:
        return False
    
    if text.endswith('。') or text.endswith('！') or text.endswith('？'):
        open_parens = text.count('（')
        close_parens = text.count('）')
        
        if open_parens == close_parens:
            return True
        
        if open_parens < close_parens:
            return True
        
        if open_parens > close_parens:
            last_para = text.rfind('（')
            last_close = text.rfind('）')
            if last_close > last_para:
                return True
        
        bracket_balance = text.count('[') - text.count(']')
        if bracket_balance <= 0 and len(text) > 400:
            return True
    
    return False


def find_best_split(text):
    """Find the best position to split text."""
    import re
    
    if not text:
        return 0
    
    candidates = []
    
    for match in re.finditer(r'[。！？]\s*', text):
        pos = match.end()
        open_parens = text[:pos].count('（')
        close_parens = text[:pos].count('）')
        
        if open_parens == close_parens:
            candidates.append(pos)
    
    for match in re.finditer(r'[,，]\s*', text):
        pos = match.end()
        if 300 < pos < len(text) - 100:
            open_parens = text[:pos].count('（')
            close_parens = text[:pos].count('）')
            if open_parens == close_parens:
                return pos
    
    if candidates:
        for c in reversed(candidates):
            if 200 < c < len(text) - 100:
                return c
    
    last_period = text.rfind('。')
    if last_period > 200:
        return last_period + 1
    
    return len(text) // 2


def is_section_header(text):
    """Check if text is a section header."""
    import re
    header_indicators = [
        '沿革', '分野', '山川', '城池', '公署', '学校', '科举', '人物',
        '艺文', '风俗', '物产', '贡赋', '兵制', '驿传', '关隘', '桥梁',
        '寺观', '祠庙', '陵墓', '古迹', '地理'
    ]
    text = text.strip()
    if len(text) <= 20:
        for indicator in header_indicators:
            if indicator in text:
                return True
    return False

def build_volume_page(vol, volumes, env):
    """Build individual volume page."""
    vol_data = vol['data']
    
    locations = get_locations(vol_data)
    related = get_related_volumes(vol['id'], volumes)
    key_entities = vol_data.get('key_entities', [])
    
    content = format_content(vol_data)
    
    template = env.get_template('volume.html')
    html = template.render(
        title=vol['title'],
        subtitle=vol.get('subtitle', ''),
        category=vol.get('category', 'Historical'),
        summary=vol_data.get('modern_summary', ''),
        content=content,
        locations=locations,
        key_entities=key_entities,
        related_volumes=related,
        description=vol_data.get('modern_summary', '')[:160]
    )
    
    output_path = DIST_DIR / "volume" / f"{vol['id']}.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"  Generated: {output_path}")

def build_index_page(volumes, stats, env):
    """Build home page."""
    template = env.get_template('index.html')
    html = template.render(
        title="八闽通志 - Digital Archive",
        description="Digital archive of Ba Min Tong Zhi (八闽通志), a comprehensive Ming Dynasty chronicle of Fujian province.",
        volumes=volumes,
        stats=stats
    )
    
    with open(DIST_DIR / "index.html", 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Generated: {DIST_DIR / 'index.html'}")

def build_library_page(volumes, env):
    """Build library/volume list page."""
    template = env.get_template('library.html')
    html = template.render(
        title="Library - All Volumes",
        description="Browse all 43 volumes of Ba Min Tong Zhi",
        volumes=volumes
    )
    
    with open(DIST_DIR / "library.html", 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Generated: {DIST_DIR / 'library.html'}")

def build_search_page(volumes, query, env):
    """Build search results page."""
    results = []
    query_lower = query.lower() if query else ""
    
    if query_lower:
        for vol in volumes:
            vol_data = vol['data']
            score = 0
            matched_fields = []
            
            title = vol.get('title', '').lower()
            if query_lower in title:
                score += 10
                matched_fields.append('Title')
            
            summary = vol_data.get('modern_summary', '').lower()
            if query_lower in summary:
                score += 5
                matched_fields.append('Summary')
            
            full_text = vol_data.get('cleaned_full_text', '').lower()
            if query_lower in full_text:
                score += 3
                matched_fields.append('Content')
            
            if score > 0:
                results.append({
                    'id': vol['id'],
                    'title': vol['title'],
                    'number': vol['number'],
                    'summary': vol['summary'],
                    'matched_fields': matched_fields,
                    'score': score
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
    
    template = env.get_template('search.html')
    html = template.render(
        title="Search",
        description="Search the Ba Min Tong Zhi archive",
        query=query or "",
        results=results
    )
    
    with open(DIST_DIR / "search.html", 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Generated: {DIST_DIR / 'search.html'}")

def generate_search_index(volumes):
    """Generate Fuse.js search index."""
    search_index = []
    
    for vol in volumes:
        vol_data = vol['data']
        search_index.append({
            'id': vol['id'],
            'title': vol['title'],
            'number': vol['number'],
            'summary': vol['summary'],
            'content': vol_data.get('cleaned_full_text', '')[:5000],
            'category': vol.get('category', ''),
            'tags': vol.get('tags', [])
        })
    
    with open(DIST_DIR / "search_index.json", 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)
    
    print(f"  Generated: {DIST_DIR / 'search_index.json'}")

def main():
    print("=" * 60)
    print("Ba Min Tong Zhi - Static Site Generator")
    print("=" * 60)
    
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    
    print("\n[1/6] Loading data...")
    data = load_all_data()
    print(f"  Loaded {len(data)} volume data files")
    
    print("\n[2/6] Processing volumes...")
    volumes = get_volume_list(data)
    stats = get_statistics(data)
    print(f"  Processed {len(volumes)} volumes")
    
    print("\n[3/6] Setting up Jinja2 environment...")
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    print("\n[4/6] Generating pages...")
    
    print("  Building index.html...")
    build_index_page(volumes, stats, env)
    
    print("  Building library.html...")
    build_library_page(volumes, env)
    
    print("  Building search.html...")
    build_search_page(volumes, "", env)
    
    print("  Building volume pages...")
    for vol in volumes:
        build_volume_page(vol, volumes, env)
    
    print("\n[5/6] Generating search index...")
    generate_search_index(volumes)
    
    print("\n[6/6] Copying static assets...")
    static_dir = DIST_DIR
    static_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 60)
    print(f"Build complete! Output directory: {DIST_DIR}")
    print("=" * 60)
    
    print("\nTo preview locally:")
    print(f"  cd {DIST_DIR}")
    print("  python -m http.server 8000")
    print("\nTo deploy to Vercel:")
    print("  vercel --prod")

if __name__ == "__main__":
    main()
