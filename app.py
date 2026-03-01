import streamlit as st
import json
import os
import re
import random
from pathlib import Path
from typing import Dict, Any, List, Optional

st.set_page_config(
    page_title="八闽通志·数字典藏平台",
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
            'summary': vol_data.get('modern_summary', '')[:150]
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

def get_recommended_articles() -> List[Dict[str, Any]]:
    data = load_all_data()
    articles = []
    for vol_name, vol_data in data.items():
        if vol_data.get('modern_summary'):
            articles.append({
                'id': vol_name,
                'title': vol_data.get('title', vol_name),
                'summary': vol_data.get('modern_summary', '')[:200],
                'category': vol_data.get('category', '古籍研究')
            })
    random.shuffle(articles)
    return articles[:6]

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

def render_custom_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Serif:ital,wght@0,400;0,600;1,400&display=swap');
    
    /* 全局背景 - 宣纸色 */
    .stApp {
        background-color: #FDFCF0;
    }
    
    /* 主容器背景 */
    .main {
        background-color: #FDFCF0;
    }
    
    /* 所有文字使用衬线体 */
    body, .stApp, div, p, span {
        font-family: 'Noto Serif SC', 'Noto Serif', 'Songti SC', 'SimSun', 'Times New Roman', serif !important;
    }
    
    /* 标题样式 */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Noto Serif SC', 'Noto Serif', 'Songti SC', 'SimSun', serif !important;
        color: #2C3E50 !important;
        font-weight: 600;
    }
    
    /* 正文样式 - 增加行间距 */
    .stMarkdown p, .stText, p {
        font-family: 'Noto Serif SC', 'Noto Serif', serif !important;
        font-size: 16px;
        line-height: 1.9 !important;
        color: #34495E;
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #FAF8F0;
        border-right: 1px solid #E8E4D9;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        font-family: 'Noto Serif SC', serif;
    }
    
    /* 隐藏 Streamlit 冗余信息 */
    footer, header, .stDeployButton, [data-testid="stToolbar"] {
        display: none !important;
    }
    
    /* 移除顶部 padding */
    .block-container {
        padding-top: 1rem !important;
    }
    
    /* 学术卡片样式 */
    .academic-card {
        background: linear-gradient(145deg, #FFFFFF 0%, #F8F6ED 100%);
        border: 1px solid #E0DCD0;
        border-radius: 8px;
        padding: 24px;
        margin: 12px 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    
    .academic-card:hover {
        border-color: #C4B898;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    
    /* 卷次卡片样式 */
    .volume-card {
        background: #FFFFFF;
        border: 1px solid #DDD8CC;
        border-radius: 6px;
        padding: 18px;
        margin: 10px 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .volume-card:hover {
        border-color: #B8A882;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        transform: translateY(-3px);
    }
    
    /* 统计框 */
    .stat-box {
        background: linear-gradient(145deg, #FDFCF0, #F5F0E0);
        border-left: 4px solid #B8A882;
        padding: 16px;
        border-radius: 0 8px 8px 0;
    }
    
    /* 广告占位 - 页面底部 */
    .ad-placeholder-bottom {
        background: linear-gradient(135deg, #F8F6ED 0%, #F0EDE3 100%);
        border: 2px dashed #C4B898;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        color: #8B8577;
        font-size: 13px;
        min-height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 40px;
        margin-bottom: 20px;
    }
    
    /* 广告占位 - 侧边栏 */
    .ad-placeholder-sidebar {
        background: linear-gradient(135deg, #F8F6ED 0%, #F0EDE3 100%);
        border: 2px dashed #C4B898;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        color: #8B8577;
        font-size: 11px;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
    }
    
    /* 导航按钮 */
    .nav-button {
        display: block;
        padding: 14px 18px;
        margin: 6px 0;
        background: transparent;
        border: none;
        border-radius: 8px;
        color: #4A4A4A;
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
        background: #C4B898;
        color: #FFFFFF;
    }
    
    /* 区块标题 */
    .section-title {
        font-size: 26px;
        font-weight: 600;
        color: #2C3E50;
        margin: 30px 0 20px 0;
        padding-bottom: 12px;
        border-bottom: 3px solid #C4B898;
    }
    
    /* 功能图标 */
    .feature-icon {
        font-size: 36px;
        margin-bottom: 12px;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background-color: #B8A882;
        color: white;
        border: none;
        border-radius: 6px;
        font-family: 'Noto Serif SC', serif;
        padding: 10px 20px;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #A09070;
        border-color: #A09070;
    }
    
    /* 搜索框样式 */
    .stTextInput > div > div > input {
        font-family: 'Noto Serif SC', serif;
        font-size: 16px;
    }
    
    /* 折叠面板 */
    div[data-testid="stExpander"] {
        background: #FAF8F0;
        border: 1px solid #E8E4D9;
        border-radius: 8px;
    }
    
    /* 首页巨幅标题 */
    .hero-title {
        font-size: 56px;
        font-weight: 700;
        color: #2C3E50 !important;
        margin-bottom: 10px;
        letter-spacing: 4px;
    }
    
    .hero-subtitle {
        font-size: 22px;
        font-weight: 400;
        color: #7F8C8D;
        margin-bottom: 30px;
        letter-spacing: 2px;
    }
    
    /* 推荐文章卡片 */
    .article-card {
        background: #FFFFFF;
        border-left: 4px solid #C4B898;
        border-radius: 4px;
        padding: 20px;
        margin: 12px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .article-card h4 {
        margin-bottom: 8px;
        color: #2C3E50;
    }
    
    .article-card p {
        font-size: 14px;
        color: #7F8C8D;
        line-height: 1.7;
    }
    
    .article-card .category {
        display: inline-block;
        background: #F5F0E0;
        color: #8B8577;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 12px;
        margin-bottom: 8px;
    }
    
    /* 响应式设计 - 移动端 */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 32px !important;
            letter-spacing: 2px;
        }
        
        .hero-subtitle {
            font-size: 16px !important;
        }
        
        .section-title {
            font-size: 20px;
        }
        
        .academic-card {
            padding: 16px;
        }
        
        .volume-card {
            padding: 12px;
        }
        
        [data-testid="stSidebar"] {
            width: 100% !important;
        }
    }
    
    /* 滚动条美化 */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F5F2E8;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #C4B898;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    stats = get_statistics()
    
    with st.sidebar:
        st.markdown("### 📚 导航菜单")
        st.markdown("""
        <a href="/" style="text-decoration: none;"><div class="nav-button">🏠 首页</div></a>
        <a href="/search" style="text-decoration: none;"><div class="nav-button">🔍 智能检索</div></a>
        <a href="/library" style="text-decoration: none;"><div class="nav-button">📖 分卷阅览</div></a>
        <a href="/articles" style="text-decoration: none;"><div class="nav-button">📊 学术研究</div></a>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📈 数据统计")
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("总卷数", stats["total_volumes"])
            st.metric("地名总数", stats["total_place_names"])
        with col2:
            st.metric("文献引用", stats["total_quotes"])
            st.metric("人物职官", stats["total_entities"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📋 卷次目录")
        volumes = get_volume_list()
        
        for vol in volumes[:8]:
            st.markdown(f"""
            <a href="/volume?vol={vol['id']}" target="_self" style="text-decoration: none;">
                <div class="nav-button" style="font-size: 14px;">
                    📖 {vol['title']}
                </div>
            </a>
            """, unsafe_allow_html=True)
        
        if len(volumes) > 8:
            with st.expander(f"查看全部 {len(volumes)} 卷"):
                for vol in volumes[8:]:
                    st.markdown(f"""
                    <a href="/volume?vol={vol['id']}" target="_self" style="text-decoration: none;">
                        <div class="nav-button" style="font-size: 14px;">
                            📖 {vol['title']}
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### ℹ️ 关于")
        st.markdown("""
        <a href="/about" style="text-decoration: none;"><div class="nav-button">👤 关于我们</div></a>
        <a href="/privacy" style="text-decoration: none;"><div class="nav-button">🔒 隐私政策</div></a>
        <a href="/terms" style="text-decoration: none;"><div class="nav-button">📜 服务条款</div></a>
        <a href="/contact" style="text-decoration: none;"><div class="nav-button">✉️ 联系方式</div></a>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown('<div class="ad-placeholder-sidebar">📢 Sponsored Content<br><br>广告位招商中</div>', unsafe_allow_html=True)

def render_footer():
    st.markdown("---")
    st.markdown("""
    <div class="ad-placeholder-bottom">
        📢 Sponsored Content — 广告位招商中
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 30px 20px; color: #8B8577; font-size: 13px; border-top: 1px solid #E8E4D9; margin-top: 20px;">
        <p style="font-family: 'Noto Serif SC', serif;">© 2024 八闽通志·数字典藏平台 · 学术文献数据库</p>
        <p style="font-size: 12px; color: #A9A299;">数据仅供学术研究使用 · 基于《八闽通志》古籍文献数字化整理</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    render_custom_theme()
    render_sidebar()
    
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px 40px 20px; background: linear-gradient(180deg, #FDFCF0 0%, #F8F6ED 100%); border-radius: 16px; margin-bottom: 40px;">
        <h1 class="hero-title">八闽通志</h1>
        <h2 class="hero-subtitle">数字典藏平台</h2>
        <p style="font-size: 17px; color: #6B6565; max-width: 700px; margin: 0 auto; line-height: 1.8; font-family: 'Noto Serif SC', serif;">
            收录明代福建省志《八闽通志》全部43卷内容<br>
            致力于古籍数字化保护与学术研究传播
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="academic-card" style="text-align: center;">
            <div class="feature-icon">🔍</div>
            <h4 style="margin-bottom: 10px;">智能检索</h4>
            <p style="font-size: 14px; color: #7F8C8D;">全文检索、关键词高亮、多维度筛选</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<a href="/search"><button style="width: 100%;">进入检索 →</button></a>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="academic-card" style="text-align: center;">
            <div class="feature-icon">📖</div>
            <h4 style="margin-bottom: 10px;">分卷阅览</h4>
            <p style="font-size: 14px; color: #7F8C8D;">43卷完整典籍，按卷次分类</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<a href="/library"><button style="width: 100%;">进入书库 →</button></a>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="academic-card" style="text-align: center;">
            <div class="feature-icon">📊</div>
            <h4 style="margin-bottom: 10px;">学术研究</h4>
            <p style="font-size: 14px; color: #7F8C8D;">文献解读、数据分析、学术探讨</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<a href="/articles"><button style="width: 100%;">查看研究 →</button></a>', unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="academic-card" style="text-align: center;">
            <div class="feature-icon">🎲</div>
            <h4 style="margin-bottom: 10px;">随机阅读</h4>
            <p style="font-size: 14px; color: #7F8C8D;">随机选取一卷，开启阅读之旅</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("随机阅读"):
            volumes = get_volume_list()
            if volumes:
                random_vol = random.choice(volumes)
                st.markdown(f'<meta http-equiv="refresh" content="0;URL=/volume?vol={random_vol["id"]}">', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title">📖 推荐阅读</h2>', unsafe_allow_html=True)
    
    articles = get_recommended_articles()
    
    cols = st.columns(2)
    for i, article in enumerate(articles):
        with cols[i % 2]:
            st.markdown(f"""
            <a href="/volume?vol={article['id']}" style="text-decoration: none;">
                <div class="article-card">
                    <span class="category">{article.get('category', '古籍研究')}</span>
                    <h4>📜 {article['title']}</h4>
                    <p>{article['summary']}...</p>
                </div>
            </a>
            """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title">🔥 热门卷次</h2>', unsafe_allow_html=True)
    
    volumes = get_volume_list()
    hot_volumes = [v for v in volumes if '地理' in v['title'] or '食货' in v['title']][:6]
    
    cols = st.columns(3)
    for i, vol in enumerate(hot_volumes):
        with cols[i % 3]:
            st.markdown(f"""
            <a href="/volume?vol={vol['id']}" style="text-decoration: none;">
                <div class="volume-card">
                    <h4 style="margin: 0 0 10px 0; color: #2C3E50;">📖 {vol['title']}</h4>
                    <p style="font-size: 13px; color: #7F8C8D; margin: 0; line-height: 1.6;">{vol['summary']}...</p>
                </div>
            </a>
            """, unsafe_allow_html=True)
    
    render_footer()

if __name__ == "__main__":
    main()
