import streamlit as st

st.set_page_config(
    page_title="关于我们 - 八闽通志",
    page_icon="ℹ️",
    layout="wide"
)

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

.info-box {
    background: linear-gradient(135deg, #FAF8F0 0%, #F5F2E8 100%);
    border: 1px solid #E8E4D9;
    border-radius: 8px;
    padding: 25px;
    margin: 20px 0;
}

.content-text {
    font-size: 16px;
    line-height: 2;
    text-align: justify;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
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
    <h1 style="font-size: 36px; margin-bottom: 10px; color: #2C3E50 !important;">ℹ️ 关于我们</h1>
    <p style="font-size: 16px; color: #7F8C8D; margin-bottom: 0;">了解八闽通志数据库</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📚 项目简介")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        <strong>八闽通志数据库</strong>是一个基于《八闽通志》古籍文献构建的数字化检索平台。《八闽通志》是福建省现存最早的地方志，由明代黄仲昭编纂，成书于明弘治二年（1489年）。
    </p>
    <p class="content-text">
        本项目旨在通过现代信息技术，将这部珍贵的福建古籍数字化、结构化，方便学者和爱好者检索、研究和使用。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🎯 项目目标")

st.markdown("""
- **文献保护**：通过数字化手段保护和研究福建古籍
- **学术研究**：为历史研究者提供便捷的检索工具
- **文化传播**：让更多人了解和认识福建的历史文化
- **教育普及**：为学生和教育工作者提供学习资源
""")

st.markdown("### 📊 数据来源")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        本网站所有数据均来自《八闽通志》原文，包括：
    </p>
    <ul style="line-height: 2;">
        <li>地理：府、州、县的地理沿革和山川</li>
        <li>食货：田赋、户口、水利等经济资料</li>
        <li>人物：历史人物和职官信息</li>
        <li>学校：教育机构和书院</li>
        <li>选举：科举和选举制度</li>
        <li>其他：典礼、兵制、外志等内容</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("### ⚠️ 使用声明")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        1. 本网站数据仅供学术研究和学习交流使用，请勿用于商业目的。<br>
        2. 本网站不保证数据的完整性和准确性，使用前请核对原文。<br>
        3. 引用本网站数据请注明来源。<br>
        4. 如有任何问题或建议，请联系我们。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #95A5A6; font-size: 13px;">
    <p>© 2024 八闽通志数据库 · 基于学术目的构建</p>
</div>
""", unsafe_allow_html=True)
