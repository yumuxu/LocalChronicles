import streamlit as st
import json
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

st.set_page_config(
    page_title="八闽通志 - 福建古籍数据库",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path(__file__).parent / "structured_data"

def load_all_data() -> Dict[str, Any]:
    if 'data_cache' not in st.session_state:
        st.session_state.data_cache = {}
        for json_file in DATA_DIR.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                st.session_state.data_cache[json_file.stem] = json.load(f)
    return st.session_state.data_cache

def get_volume_list() -> List[Dict[str, Any]]:
    data = load_all_data()
    volumes = []
    for vol_name, vol_data in data.items():
        match = re.search(r'卷(\d+)', vol_name)
        num = int(match.group(1)) if match else 999
        volumes.append({
            'id': vol_name,
            'title': vol_data.get('title', vol_name),
            'number': num,
            'summary': vol_data.get('modern_summary', '')[:100]
        })
    volumes.sort(key=lambda x: x['number'])
    return volumes

def get_statistics() -> Dict[str, int]:
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

def search_data(query: str) -> List[Dict[str, Any]]:
    data = load_all_data()
    results = []
    query_lower = query.lower()
    
    for vol_name, vol_data in data.items():
        score = 0
        matched_fields = []
        
        full_text = vol_data.get("cleaned_full_text", "").lower()
        if query_lower in full_text:
            score += 10
            matched_fields.append("正文")
        
        title = vol_data.get("title", "").lower()
        if query_lower in title:
            score += 5
            matched_fields.append("标题")
        
        hierarchy_str = json.dumps(vol_data.get("location_hierarchy", {}), ensure_ascii=False).lower()
        if query_lower in hierarchy_str:
            score += 3
            matched_fields.append("地理")
        
        for entity in vol_data.get("key_entities", []):
            if query_lower in entity.get("name", "").lower():
                score += 2
                matched_fields.append("人物")
                break
        
        for quote in vol_data.get("historical_quotes", []):
            if query_lower in quote.get("source", "").lower():
                score += 2
                matched_fields.append("引用")
                break
        
        if score > 0:
            results.append({
                "vol_id": vol_name,
                "title": vol_data.get("title", ""),
                "score": score,
                "matched_fields": matched_fields,
                "data": vol_data
            })
    
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def highlight_text(text: str, query: str) -> str:
    if not query:
        return text
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(f"**`{query}`**", text)

def render_header():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');
    
    .main {
        background-color: #FDFCF0;
    }
    
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
    
    .academic-card {
        background: linear-gradient(135deg, #FAF8F0 0%, #F5F2E8 100%);
        border: 1px solid #E8E4D9;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .volume-card {
        background: white;
        border: 1px solid #DDD8CC;
        border-radius: 6px;
        padding: 15px;
        margin: 8px 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .volume-card:hover {
        border-color: #B8A882;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .stat-box {
        background: linear-gradient(145deg, #FDFCF0, #F5F0E0);
        border-left: 4px solid #B8A882;
        padding: 15px;
        border-radius: 0 8px 8px 0;
    }
    
    .ad-placeholder {
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
    }
    
    .sidebar-ad {
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
    
    .nav-button.active {
        background: #B8A882;
        color: white;
    }
    
    .section-title {
        font-size: 24px;
        font-weight: 600;
        color: #2C3E50;
        margin: 20px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #B8A882;
    }
    
    .feature-icon {
        font-size: 32px;
        margin-bottom: 8px;
    }
    
    .highlight-keyword {
        background-color: #FFF3CD;
        padding: 2px 6px;
        border-radius: 3px;
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

def render_sidebar():
    stats = get_statistics()
    
    with st.sidebar:
        st.markdown("### 📊 数据统计")
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("总卷数", stats["total_volumes"])
        st.metric("地名总数", stats["total_place_names"])
        st.metric("文献引用", stats["total_quotes"])
        st.metric("人物职官", stats["total_entities"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📚 卷次导航")
        volumes = get_volume_list()
        
        for vol in volumes[:10]:
            st.markdown(f"""
            <a href="/volume?vol={vol['id']}" target="_self" style="text-decoration: none;">
                <div class="nav-button">
                    📖 {vol['title']}
                </div>
            </a>
            """, unsafe_allow_html=True)
        
        if len(volumes) > 10:
            with st.expander(f"查看更多卷次 ({len(volumes) - 10})"):
                for vol in volumes[10:]:
                    st.markdown(f"""
                    <a href="/volume?vol={vol['id']}" target="_self" style="text-decoration: none;">
                        <div class="nav-button">
                            📖 {vol['title']}
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🔗 快速链接")
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

def main():
    render_header()
    render_sidebar()
    
    st.markdown("""
    <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #FDFCF0 0%, #F5F2E8 100%); border-radius: 12px; margin-bottom: 30px;">
        <h1 style="font-size: 42px; margin-bottom: 15px; color: #2C3E50 !important;">📚 八闽通志</h1>
        <h3 style="font-weight: 400; color: #7F8C8D; margin-bottom: 20px;">福建古籍数据库 · 文献检索平台</h3>
        <p style="font-size: 16px; color: #95A5A6; max-width: 600px; margin: 0 auto;">
            收录《八闽通志》全部43卷内容，提供智能检索、分类浏览、原文阅读等核心功能
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="academic-card" style="text-align: center;">
            <div class="feature-icon">🔍</div>
            <h4>智能检索</h4>
            <p style="font-size: 14px; color: #7F8C8D;">支持全文搜索、关键词高亮、多维度筛选</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<a href="/search"><button style="width: 100%; padding: 10px; background: #B8A882; color: white; border: none; border-radius: 6px; cursor: pointer;">进入检索</button></a>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="academic-card" style="text-align: center;">
            <div class="feature-icon">📚</div>
            <h4>书库浏览</h4>
            <p style="font-size: 14px; color: #7F8C8D;">43卷完整典籍，按卷次分类，支持详情跳转</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<a href="/library"><button style="width: 100%; padding: 10px; background: #B8A882; color: white; border: none; border-radius: 6px; cursor: pointer;">进入书库</button></a>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="academic-card" style="text-align: center;">
            <div class="feature-icon">📝</div>
            <h4>原创博文</h4>
            <p style="font-size: 14px; color: #7F8C8D;">学术研究、文献解读、文化漫谈</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<a href="/articles"><button style="width: 100%; padding: 10px; background: #B8A882; color: white; border: none; border-radius: 6px; cursor: pointer;">阅读博文</button></a>', unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="academic-card" style="text-align: center;">
            <div class="feature-icon">📖</div>
            <h4>随机阅读</h4>
            <p style="font-size: 14px; color: #7F8C8D;">随机选取一卷，体验古籍阅读乐趣</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("随机阅读"):
            import random
            volumes = get_volume_list()
            if volumes:
                random_vol = random.choice(volumes)
                st.markdown(f'<meta http-equiv="refresh" content="0;URL=/volume?vol={random_vol["id"]}">', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title">🔥 热门推荐</h2>', unsafe_allow_html=True)
    
    volumes = get_volume_list()
    hot_volumes = [v for v in volumes if '地理' in v['title'] or '食货' in v['title']][:6]
    
    cols = st.columns(3)
    for i, vol in enumerate(hot_volumes):
        with cols[i % 3]:
            st.markdown(f"""
            <a href="/volume?vol={vol['id']}" style="text-decoration: none;">
                <div class="volume-card">
                    <h4 style="margin: 0 0 8px 0; color: #2C3E50;">📖 {vol['title']}</h4>
                    <p style="font-size: 13px; color: #7F8C8D; margin: 0;">{vol['summary']}...</p>
                </div>
            </a>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px; color: #95A5A6; font-size: 13px;">
        <p>© 2024 八闽通志数据库 · 基于学术目的构建 · 数据仅供研究使用</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
