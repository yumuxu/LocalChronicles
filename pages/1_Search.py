import streamlit as st
import json
import re
from pathlib import Path

st.set_page_config(
    page_title="智能检索 - 八闽通志",
    page_icon="🔍",
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
            'summary': vol_data.get('modern_summary', '')[:100]
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

def search_data(query):
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

def highlight_text(text, query):
    if not query:
        return text
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return pattern.sub(f"**`{query}`**", text)

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

.academic-card {
    background: linear-gradient(135deg, #FAF8F0 0%, #F5F2E8 100%);
    border: 1px solid #E8E4D9;
    border-radius: 8px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
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

.search-highlight {
    background-color: #FFF3CD;
    padding: 2px 4px;
    border-radius: 3px;
    font-weight: 600;
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
    <h1 style="font-size: 36px; margin-bottom: 10px; color: #2C3E50 !important;">🔍 智能检索</h1>
    <p style="font-size: 16px; color: #7F8C8D; margin-bottom: 0;">输入关键词搜索《八闽通志》全部内容</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    search_query = st.text_input(
        "搜索关键词",
        placeholder="如：建宁府、福州府、曾巩、学校...",
        label_visibility="collapsed"
    )
with col2:
    st.write("")
    st.write("")
    search_btn = st.button("🔍 搜索", type="primary")

hot_keywords = ["建宁府", "福州府", "泉州府", "漳州府", "山川", "学校", "人物", "田赋", "风俗"]

st.markdown("### 🔥 热门关键词")
cols = st.columns(5)
for i, keyword in enumerate(hot_keywords):
    with cols[i % 5]:
        if st.button(keyword, key=f"hot_{keyword}"):
            search_query = keyword

if search_query:
    results = search_data(search_query)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #FAF8F0 0%, #F5F2E8 100%); 
                border: 1px solid #E8E4D9; border-radius: 8px; padding: 15px; margin: 20px 0;">
        <h3 style="margin: 0; color: #2C3E50;">📊 搜索结果</h3>
        <p style="margin: 5px 0 0 0; color: #7F8C8D;">找到 <strong style="color: #B8A882;">{len(results)}</strong> 条匹配记录</p>
    </div>
    """, unsafe_allow_html=True)
    
    if results:
        for result in results:
            with st.expander(f"📖 {result['title']} (匹配字段: {', '.join(result['matched_fields'])})", expanded=True):
                col_left, col_right = st.columns([2, 1])
                
                with col_left:
                    st.markdown("#### 📝 正文内容")
                    full_text = result["data"].get("cleaned_full_text", "")
                    highlighted = highlight_text(full_text, search_query)
                    st.markdown(f"> {highlighted}")
                
                with col_right:
                    st.markdown("#### 🏛️ 结构化信息")
                    
                    st.markdown("**📍 地理层级**")
                    hierarchy = result["data"].get("location_hierarchy", {})
                    if hierarchy:
                        for loc, details in hierarchy.items():
                            st.write(f"• {loc}")
                    else:
                        st.write("无")
                    
                    st.markdown("**👤 人物职官**")
                    entities = result["data"].get("key_entities", [])
                    if entities:
                        for e in entities[:5]:
                            st.write(f"• {e.get('name', '')} ({e.get('role', '')})")
                    else:
                        st.write("无")
                    
                    st.markdown("**📚 文献引用**")
                    quotes = result["data"].get("historical_quotes", [])
                    if quotes:
                        for q in quotes[:3]:
                            st.write(f"• 《{q.get('source', '')}》")
                    else:
                        st.write("无")
                    
                    st.markdown("---")
                    st.markdown(f"**🔗 [查看完整卷次详情 →](/volume?vol={result['vol_id']})**", unsafe_allow_html=True)
    else:
        st.info("未找到匹配结果，请尝试其他关键词")
        
        st.markdown("### 💡 建议")
        st.markdown("""
        - 检查关键词拼写
        - 尝试使用更通用的关键词
        - 减少搜索词数量
        """)
else:
    st.markdown("""
    <div class="academic-card" style="text-align: center; padding: 40px;">
        <h3 style="color: #7F8C8D;">👆 请输入关键词开始搜索</h3>
        <p style="color: #95A5A6;">支持搜索：正文、标题、地理、人物、文献引用</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📖 检索示例")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **搜索：建宁府**
        
        可找到涉及建宁府地理、历史、人物等相关内容的卷次。
        """)
        
    with col2:
        st.markdown("""
        **搜索：山川**
        
        可找到涉及福建各地山川地理的卷次内容。
        """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #95A5A6; font-size: 13px;">
    <p>© 2024 八闽通志数据库 · 基于学术目的构建</p>
</div>
""", unsafe_allow_html=True)
