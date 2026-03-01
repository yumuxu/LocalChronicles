import streamlit as st

st.set_page_config(
    page_title="隐私政策 - 八闽通志",
    page_icon="🔒",
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
    <h1 style="font-size: 36px; margin-bottom: 10px; color: #2C3E50 !important;">🔒 隐私政策</h1>
    <p style="font-size: 16px; color: #7F8C8D; margin-bottom: 0;">保护您的隐私权益</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📋 隐私政策")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        <strong>八闽通志数据库</strong>（以下简称"本平台"）非常重视用户的隐私保护。本隐私政策旨在向您说明我们如何收集、使用、存储和保护您的个人信息。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📝 信息收集")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        <strong>1. 自动收集的信息</strong><br>
        当您访问本平台时，我们的服务器会自动记录一些基本信息，包括但不限于：
    </p>
    <ul style="line-height: 2; margin-left: 20px;">
        <li>您的IP地址</li>
        <li>浏览器类型和操作系统</li>
        <li>访问时间和日期</li>
        <li>您访问的页面</li>
    </ul>
    <p class="content-text">
        <strong>2. 您主动提供的信息</strong><br>
        本平台为静态文献展示平台，<strong>不要求用户注册账号</strong>，也不收集您的个人敏感信息（如姓名、电话、邮箱等）。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 💻 信息使用")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        我们收集的信息仅用于以下目的：
    </p>
    <ul style="line-height: 2; margin-left: 20px;">
        <li><strong>改进服务</strong>：分析用户访问数据，优化网站结构和内容</li>
        <li><strong>安全保障</strong>：监测和防止恶意攻击，保障平台安全运行</li>
        <li><strong>统计用途</strong>：生成访问统计报告，用于学术研究</li>
    </ul>
    <p class="content-text">
        <strong>注意</strong>：本平台<strong>不</strong>将任何用户信息用于广告推送或商业营销。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🍪 Cookie技术")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        本平台可能使用Cookie技术来改善用户体验。Cookie是存储在您设备上的小型文本文件，用于记录您的偏好设置等信息。您可以通过浏览器设置拒绝Cookie，但这可能会影响某些功能的使用。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🔐 信息保护")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        我们采取合理的技术和管理措施来保护您的信息安全：
    </p>
    <ul style="line-height: 2; margin-left: 20px;">
        <li>使用安全协议加密传输</li>
        <li>限制数据访问权限</li>
        <li>定期安全检查和更新</li>
    </ul>
    <p class="content-text">
        但请注意，互联网传输无法保证100%安全，我们无法绝对保证您信息的安全。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🔗 第三方链接")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        本平台可能包含指向第三方网站的链接。我们对这些第三方网站的隐私 practices 不承担责任。建议您在访问这些网站时查看其隐私政策。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📧 联系我们")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        如果您对本隐私政策有任何疑问，或希望了解更多关于信息保护的内容，请通过<a href="/contact">联系方式</a>与我们联系。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📅 政策更新")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        我们可能会不时更新本隐私政策。任何重大变更都将在本页面公布。建议您定期查看以了解最新信息。
    </p>
    <p style="color: #95A5A6; margin-top: 15px;">
        最后更新日期：2024年1月
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #95A5A6; font-size: 13px;">
    <p>© 2024 八闽通志数据库 · 基于学术目的构建</p>
</div>
""", unsafe_allow_html=True)
