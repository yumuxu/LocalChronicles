import streamlit as st

st.set_page_config(
    page_title="服务条款 - 八闽通志",
    page_icon="📋",
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
    <h1 style="font-size: 36px; margin-bottom: 10px; color: #2C3E50 !important;">📋 服务条款</h1>
    <p style="font-size: 16px; color: #7F8C8D; margin-bottom: 0;">使用本平台的服务条款和条件</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📋 服务条款")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        欢迎使用<strong>八闽通志数据库</strong>（以下简称"本平台"）。在使用本平台之前，请仔细阅读以下服务条款。通过访问或使用本平台，即表示您同意接受本服务条款的约束。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📜 服务内容")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        本平台提供以下服务：
    </p>
    <ul style="line-height: 2; margin-left: 20px;">
        <li><strong>古籍检索</strong>：提供《八闽通志》全部43卷的全文检索功能</li>
        <li><strong>书库浏览</strong>：按卷次浏览和查看古籍内容</li>
        <li><strong>详情阅读</strong>：查看单卷的详细内容、结构化信息和现代摘要</li>
        <li><strong>原创内容</strong>：提供与古籍相关的学术研究和分析文章</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("### ⚖️ 使用规范")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        您在使用本平台时，应当遵守以下规范：
    </p>
    <ul style="line-height: 2; margin-left: 20px;">
        <li><strong>合法使用</strong>：仅将本平台用于学术研究和学习目的，不得用于任何非法活动</li>
        <li><strong>尊重版权</strong>：尊重《八闽通志》原文的版权，不进行未授权的复制和传播</li>
        <li><strong>文明交流</strong>：在评论和交流中保持文明礼貌，不得发布违法违规内容</li>
        <li><strong>禁止攻击</strong>：不得试图攻击、入侵或破坏本平台的正常运行</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("### ⚠️ 免责声明")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        <strong>1. 数据准确性</strong><br>
        本平台尽可能确保数据的准确性，但不保证数据的完整性和实时性。用户在使用数据前应与原文进行核对。
    </p>
    <p class="content-text">
        <strong>2. 服务可用性</strong><br>
        本平台会尽力保持服务的连续性，但不保证服务随时可用。对于因服务中断造成的任何损失，我们不承担责任。
    </p>
    <p class="content-text">
        <strong>3. 外部链接</strong><br>
        本平台可能包含指向第三方网站的链接，我们对这些网站的内容和可用性不承担责任。
    </p>
    <p class="content-text">
        <strong>4. 使用风险</strong><br>
        用户应自行承担使用本平台的风险。在法律允许的范围内，我们不对任何直接或间接损失负责。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### �识 知识产权")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        <strong>1. 平台内容</strong><br>
        本平台的设计、代码、结构等知识产权归本平台所有。
    </p>
    <p class="content-text">
        <strong>2. 《八闽通志》原文</strong><br>
        《八闽通志》原文为公共领域文献，任何人可自由使用。但本平台对原文的数字化、整理和结构化工作享有相应权益。
    </p>
    <p class="content-text">
        <strong>3. 原创内容</strong><br>
        本平台发布的原创文章和分析内容，版权归原作者所有。引用时请注明出处。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🔒 账户和安全")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        本平台为开放式文献检索平台，<strong>不需要用户注册账户</strong>。但我们建议用户：
    </p>
    <ul style="line-height: 2; margin-left: 20px;">
        <li>保护个人设备安全，避免他人未经授权使用</li>
        <li>如发现任何安全漏洞或异常，及时与我们联系</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📝 服务变更")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        我们保留随时修改或终止本平台服务的权利，无需事先通知。在法律允许的范围内，本平台保留对服务条款的最终解释权。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📧 联系我们")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        如果您对服务条款有任何疑问，或需要报告违规行为，请通过<a href="/contact">联系方式</a>与我们联系。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div style="text-align: center; padding: 20px; color: #95A5A6; font-size: 13px;">
    <p>© 2024 八闽通志数据库 · 基于学术目的构建</p>
</div>
""", unsafe_allow_html=True)
