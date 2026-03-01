import streamlit as st
import json
import re
from pathlib import Path

st.set_page_config(
    page_title="卷次详情 - 八闽通志",
    page_icon="📖",
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
            'number': num
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

def highlight_keywords(text, keywords):
    if not keywords:
        return text
    result = text
    for kw in keywords:
        pattern = re.compile(re.escape(kw), re.IGNORECASE)
        result = pattern.sub(f'<span class="highlight-keyword">{kw}</span>', result)
    return result

query_params = st.query_params
vol_id = query_params.get("vol", None)

if not vol_id:
    vol_id = st.selectbox(
        "选择卷次查看详情",
        options=list(load_all_data().keys()),
        index=0
    )

data = load_all_data()
vol_data = data.get(vol_id)

if not vol_data:
    st.error("未找到该卷数据")
    st.stop()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');

.stApp {{
    background-color: #FDFCF0;
    font-family: 'Noto Serif SC', 'Songti SC', 'SimSun', serif;
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: 'Noto Serif SC', 'Songti SC', 'SimSun', serif !important;
    color: #2C3E50 !important;
}}

.stMarkdown p {{
    font-family: 'Noto Serif SC', 'Songti SC', 'SimSun', serif;
    font-size: 16px;
    line-height: 1.8;
    color: #34495E;
}}

.volume-card {{
    background: white;
    border: 1px solid #DDD8CC;
    border-radius: 8px;
    padding: 20px;
    margin: 10px 0;
}}

.stat-box {{
    background: linear-gradient(145deg, #FDFCF0, #F5F0E0);
    border-left: 4px solid #B8A882;
    padding: 15px;
    border-radius: 0 8px 8px 0;
}}

.ad-placeholder {{
    background: #F5F5F5;
    border: 2px dashed #CCCCCC;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    color: #999999;
    font-size: 12px;
    min-height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.sidebar-ad {{
    background: #F5F5F5;
    border: 2px dashed #CCCCCC;
    border-radius: 8px;
    padding: 15px;
    text-align: center;
    color: #999999;
    font-size: 11px;
    min-height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.nav-button {{
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
}}

.nav-button:hover {{
    background: #EDE9DB;
}}

.section-title {{
    font-size: 20px;
    font-weight: 600;
    color: #2C3E50;
    margin: 15px 0 10px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid #B8A882;
}}

.highlight-keyword {{
    background-color: #FFF3CD;
    padding: 2px 4px;
    border-radius: 3px;
    font-weight: 600;
}}

.info-box {{
    background: linear-gradient(135deg, #FAF8F0 0%, #F5F2E8 100%);
    border: 1px solid #E8E4D9;
    border-radius: 8px;
    padding: 20px;
    margin: 15px 0;
}}

.entity-tag {{
    display: inline-block;
    padding: 4px 10px;
    margin: 3px;
    background: #FDFCF0;
    border: 1px solid #B8A882;
    border-radius: 15px;
    font-size: 13px;
    color: #7F8C8D;
}}

div[data-testid="stExpander"] {{
    background: #FAF8F0;
    border: 1px solid #E8E4D9;
    border-radius: 8px;
}}

.stButton > button {{
    background-color: #B8A882;
    color: white;
    border: none;
    border-radius: 6px;
    font-family: 'Noto Serif SC', serif;
}}

.stButton > button:hover {{
    background-color: #A09070;
}}

.breadcrumb {{
    padding: 10px 0;
    margin-bottom: 20px;
    font-size: 14px;
    color: #7F8C8D;
}}

.breadcrumb a {{
    color: #B8A882;
    text-decoration: none;
}}

.breadcrumb a:hover {{
    text-decoration: underline;
}}
</style>
""", unsafe_allow_html=True)

volumes = get_volume_list()
current_idx = next((i for i, v in enumerate(volumes) if v['id'] == vol_id), 0)
prev_vol = volumes[current_idx - 1] if current_idx > 0 else None
next_vol = volumes[current_idx + 1] if current_idx < len(volumes) - 1 else None

st.markdown(f"""
<div class="breadcrumb">
    <a href="/">首页</a> &gt; <a href="/library">书库</a> &gt; {vol_data.get('title', vol_id)}
</div>
""", unsafe_allow_html=True)

col_nav1, col_title, col_nav2 = st.columns([1, 2, 1])

with col_nav1:
    if prev_vol:
        st.markdown(f"[← 上一卷](?vol={prev_vol['id']})", unsafe_allow_html=True)
    else:
        st.write("")

with col_title:
    st.markdown(f"""
    <div style="text-align: center;">
        <h1 style="font-size: 28px; margin-bottom: 5px;">📖 {vol_data.get('title', vol_id)}</h1>
        <p style="color: #7F8C8D; font-size: 14px;">八闽通志 · 第 {current_idx + 1} 卷</p>
    </div>
    """, unsafe_allow_html=True)

with col_nav2:
    if next_vol:
        st.markdown(f"[下一卷 →](?vol={next_vol['id']})", unsafe_allow_html=True)
    else:
        st.write("")

st.markdown("---")

col_main, col_sidebar = st.columns([2, 1])

with col_main:
    st.markdown('<div class="ad-placeholder">📺 AdSense 广告位 - 文章顶部 (728x90)</div>', unsafe_allow_html=True)
    
    st.markdown("### 📝 现代摘要")
    summary = vol_data.get("modern_summary", "暂无摘要")
    st.markdown(f"""
    <div class="info-box">
        <p style="font-size: 16px; line-height: 1.8; margin: 0;">{summary}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📜 校订正文")
    full_text = vol_data.get("cleaned_full_text", "暂无正文内容")
    st.markdown(f"""
    <div class="volume-card" style="font-size: 16px; line-height: 2; text-align: justify;">
        {full_text}
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("查看原文格式"):
        st.markdown(f"> {full_text}")

with col_sidebar:
    st.markdown('<div class="sidebar-ad">📺 AdSense 广告位 - 侧边栏 (300x250)</div>', unsafe_allow_html=True)
    
    st.markdown("### 🗺️ 地理层级")
    hierarchy = vol_data.get("location_hierarchy", {})
    if hierarchy:
        st.markdown("""
        <div class="info-box" style="padding: 15px;">
        """, unsafe_allow_html=True)
        for loc, details in hierarchy.items():
            if details:
                st.markdown(f"**{loc}**")
                if isinstance(details, dict):
                    for k, v in details.items():
                        st.write(f"  • {k}: {v}")
            else:
                st.write(f"📍 {loc}")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("暂无地理信息")
    
    st.markdown("### 👤 人物职官")
    entities = vol_data.get("key_entities", [])
    if entities:
        st.markdown("""
        <div class="info-box" style="padding: 15px;">
        """, unsafe_allow_html=True)
        for e in entities[:15]:
            name = e.get('name', '')
            role = e.get('role', '')
            if name:
                st.markdown(f'<span class="entity-tag">{name} ({role})</span>', unsafe_allow_html=True)
        if len(entities) > 15:
            st.markdown(f"... 共 {len(entities)} 人")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("暂无人物信息")
    
    st.markdown("### 📚 文献引用")
    quotes = vol_data.get("historical_quotes", [])
    if quotes:
        st.markdown("""
        <div class="info-box" style="padding: 15px;">
        """, unsafe_allow_html=True)
        for q in quotes[:10]:
            source = q.get('source', '')
            author = q.get('author', '')
            if source:
                st.write(f"• 《{source}》" + (f" - {author}" if author else ""))
        if len(quotes) > 10:
            st.markdown(f"... 共 {len(quotes)} 条引用")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("暂无引用信息")
    
    st.markdown("### 📊 卷次信息")
    st.markdown("""
    <div class="info-box" style="padding: 15px;">
    """, unsafe_allow_html=True)
    st.write(f"• 人物职官: {len(entities)}")
    st.write(f"• 文献引用: {len(quotes)}")
    st.write(f"• 地理条目: {len(hierarchy)}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

col_prev, col_library, col_search = st.columns(3)

with col_prev:
    if prev_vol:
        st.markdown(f"[← 上一卷: {prev_vol['title']}](?vol={prev_vol['id']})", unsafe_allow_html=True)

with col_library:
    st.markdown("[📚 返回书库](/library)", unsafe_allow_html=True)

with col_search:
    if next_vol:
        st.markdown(f"[下一卷: {next_vol['title']} →](?vol={next_vol['id']})", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #95A5A6; font-size: 13px;">
    <p>© 2024 八闽通志数据库 · 基于学术目的构建</p>
</div>
""", unsafe_allow_html=True)
