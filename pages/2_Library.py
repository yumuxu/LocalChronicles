import streamlit as st
import json
import re
from pathlib import Path

st.set_page_config(
    page_title="书库 - 八闽通志",
    page_icon="📚",
    layout="wide"
)

DATA_DIR = Path(__file__).parent / "structured_data"

def load_all_data():
    if 'data_cache' not in st.session_state:
        st.session_state.data_cache = {}
        for json_file in DATA_DIR.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                st.session_state.data_cache[json_file.stem] = json.load(f)
    return st.session_state.data_cache

def get_volume_list():
    data = load_all_data()
    volumes = []
    for vol_name, vol_data in data.items():
        match = re.search(r'卷(\d+)', vol_name)
        num = int(match.group(1)) if match else 999
        volumes.append({
            'id': vol_name,
            'title': vol_data.get('title', vol_name),
            'number': num,
            'summary': vol_data.get('modern_summary', '')[:150],
            'hierarchy': vol_data.get('location_hierarchy', {}),
            'entity_count': len(vol_data.get('key_entities', [])),
            'quote_count': len(vol_data.get('historical_quotes', []))
        })
    volumes.sort(key=lambda x: x['number'])
    return volumes

def get_statistics():
    data = load_all_data()
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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');

.stApp {
    background-color: #FDFCF0;
    font-family: 'Noto Serif SC', 'Songti SC', 'SimSun', serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Noto Serif SC', 'Songti SC', 'SimSun', serif !important;
    color: #2C3E50 !important;
}

.stMarkdown p {
    font-family: 'Noto Serif SC', 'Songti SC', 'SimSun', serif;
    font-size: 16px;
    line-height: 1.8;
    color: #34495E;
}

.volume-card {
    background: white;
    border: 1px solid #DDD8CC;
    border-radius: 8px;
    padding: 20px;
    margin: 10px 0;
    transition: all 0.3s ease;
}

.volume-card:hover {
    border-color: #B8A882;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}

.volume-number {
    display: inline-block;
    background: linear-gradient(135deg, #B8A882 0%, #A09070 100%);
    color: white;
    padding: 4px 12px;
    border-radius: 15px;
    font-size: 13px;
    font-weight: 600;
    margin-right: 10px;
}

.stat-box {
    background: linear-gradient(145deg, #FDFCF0, #F5F0E0);
    border-left: 4px solid #B8A882;
    padding: 15px;
    border-radius: 0 8px 8px 0;
}

.nav-button {
    display: block;
    padding: 12px 16px;
    margin: 4px 0;
    background: transparent;
    border: none;
    border-radius: 6px;
    color: #34495E;
    text-align: left;
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'Noto Serif SC', serif;
    font-size: 15px;
}

.nav-button:hover {
    background: #EDE9DB;
}

.section-title {
    font-size: 24px;
    font-weight: 600;
    color: #2C3E50;
    margin: 20px 0 15px 0;
    padding-bottom: 10px;
    border-bottom: 2px solid #B8A882;
}

.filter-tag {
    display: inline-block;
    padding: 6px 14px;
    margin: 4px;
    background: #FAF8F0;
    border: 1px solid #E8E4D9;
    border-radius: 20px;
    font-size: 13px;
    color: #7F8C8D;
    cursor: pointer;
    transition: all 0.2s;
}

.filter-tag:hover, .filter-tag.active {
    background: #B8A882;
    color: white;
    border-color: #B8A882;
}

.search-highlight {
    background-color: #FFF3CD;
    padding: 2px 4px;
    border-radius: 3px;
    font-weight: 600;
}

div[data-testid="stExpander"] {
    background: #FAF8F0;
    border: 1px solid #E8E4D9;
    border-radius: 8px;
}

.stButton > button {
    background-color: #B8A882;
    color: white;
    border: none;
    border-radius: 6px;
    font-family: 'Noto Serif SC', serif;
}

.stButton > button:hover {
    background-color: #A09070;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📊 数据统计")
    stats = get_statistics()
    st.markdown('<div class="stat-box">', unsafe_allow_html=True)
    st.metric("总卷数", stats["total_volumes"])
    st.metric("地名总数", stats["total_place_names"])
    st.metric("文献引用", stats["total_quotes"])
    st.metric("人物职官", stats["total_entities"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔗 快速导航")
    st.markdown("""
    <a href="/" style="text-decoration: none;"><div class="nav-button">🏠 首页</div></a>
    <a href="/search" style="text-decoration: none;"><div class="nav-button">🔍 智能检索</div></a>
    <a href="/library" style="text-decoration: none;"><div class="nav-button">📚 书库</div></a>
    <a href="/articles" style="text-decoration: none;"><div class="nav-button">📝 博文</div></a>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📄 法律信息")
    st.markdown("""
    <a href="/about" style="text-decoration: none;"><div class="nav-button">ℹ️ 关于我们</div></a>
    <a href="/privacy" style="text-decoration: none;"><div class="nav-button">🔒 隐私政策</div></a>
    <a href="/terms" style="text-decoration: none;"><div class="nav-button">📋 服务条款</div></a>
    <a href="/contact" style="text-decoration: none;"><div class="nav-button">✉️ 联系方式</div></a>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 30px 20px; background: linear-gradient(135deg, #FDFCF0 0%, #F5F2E8 100%); border-radius: 12px; margin-bottom: 30px;">
    <h1 style="font-size: 36px; margin-bottom: 10px; color: #2C3E50 !important;">📚 书籍目录</h1>
    <p style="font-size: 16px; color: #7F8C8D; margin-bottom: 0;">浏览《八闽通志》全部43卷典籍</p>
</div>
""", unsafe_allow_html=True)

volumes = get_volume_list()

category_keywords = {
    "地理": ["地理", "山川", "建宁", "福州", "泉州", "漳州", "汀州", "延平", "邵武", "兴化", "福宁"],
    "食货": ["食货", "田赋", "水利", "户口"],
    "职官": ["封爵", "职官", "选举"],
    "人物": ["人物", "列女"],
    "学校": ["学校"],
    "其他": []
}

def get_category(title):
    for cat, keywords in category_keywords.items():
        for kw in keywords:
            if kw in title:
                return cat
    return "其他"

col_filter, col_search = st.columns([3, 1])

with col_filter:
    st.markdown("### 📂 按类别筛选")
    selected_category = st.radio(
        "选择类别",
        ["全部", "地理", "食货", "职官", "人物", "学校", "其他"],
        horizontal=True,
        label_visibility="collapsed"
    )

with col_search:
    st.markdown("### 🔍 搜索书名")
    search_vol = st.text_input("搜索", placeholder="输入卷名...", label_visibility="collapsed")

filtered_vols = volumes

if selected_category != "全部":
    filtered_vols = [v for v in filtered_vols if get_category(v['title']) == selected_category]

if search_vol:
    filtered_vols = [v for v in filtered_vols if search_vol in v['title']]

st.markdown(f"### 📋 共 {len(filtered_vols)} 卷")

for vol in filtered_vols:
    category = get_category(vol['title'])
    
    st.markdown(f"""
    <a href="/volume?vol={vol['id']}" style="text-decoration: none;">
        <div class="volume-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div style="flex: 1;">
                    <span class="volume-number">卷 {vol['number']:02d}</span>
                    <span class="filter-tag">{category}</span>
                    <h3 style="margin: 10px 0 8px 0; color: #2C3E50; display: inline;">📖 {vol['title']}</h3>
                    <p style="color: #7F8C8D; font-size: 14px; margin: 5px 0;">{vol['summary']}...</p>
                </div>
                <div style="text-align: right; min-width: 120px;">
                    <div style="font-size: 12px; color: #95A5A6;">
                        <div>👤 {vol['entity_count']} 人物</div>
                        <div>📚 {vol['quote_count']} 引用</div>
                    </div>
                </div>
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

if not filtered_vols:
    st.info("没有找到匹配的卷次")

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #95A5A6; font-size: 13px;">
    <p>© 2024 八闽通志数据库 · 基于学术目的构建</p>
</div>
""", unsafe_allow_html=True)
