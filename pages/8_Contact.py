import streamlit as st

st.set_page_config(
    page_title="联系方式 - 八闽通志",
    page_icon="✉️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://font.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');

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

.contact-card {
    background: white;
    border: 1px solid #DDD8CC;
    border-radius: 8px;
    padding: 20px;
    margin: 15px 0;
    text-align: center;
}

.contact-icon {
    font-size: 36px;
    margin-bottom: 10px;
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
    <h1 style="font-size: 36px; margin-bottom: 10px; color: #2C3E50 !important;">✉️ 联系方式</h1>
    <p style="font-size: 16px; color: #7F8C8D; margin-bottom: 0;">联系我们，获取更多帮助</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📬 联系方式")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        我们欢迎您通过以下方式与我们取得联系：
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="contact-card">
        <div class="contact-icon">📧</div>
        <h4>电子邮件</h4>
        <p style="color: #7F8C8D; font-size: 14px;">contact@bamin-tongzhi.com</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="contact-card">
        <div class="contact-icon">💬</div>
        <h4>社交媒体</h4>
        <p style="color: #7F8C8D; font-size: 14px;">微信公众号：八闽通志</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="contact-card">
        <div class="contact-icon">📍</div>
        <h4>项目地址</h4>
        <p style="color: #7F8C8D; font-size: 14px;">福建省福州市</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 💬 常见问题")

with st.expander("Q: 如何引用本平台的数据？"):
    st.markdown("""
    <p>引用本平台数据时，建议注明"八闽通志数据库"及访问日期。如涉及原文内容，请与原始文献核对后引用。</p>
    """, unsafe_allow_html=True)

with st.expander("Q: 本平台的数据可以商业使用吗？"):
    st.markdown("""
    <p>本平台数据仅供学术研究和学习交流使用，不建议用于商业目的。如有特殊需求，请联系我们协商。</p>
    """, unsafe_allow_html=True)

with st.expander("Q: 如何报告数据错误？"):
    st.markdown("""
    <p>我们尽可能确保数据准确性，但古籍整理过程中难免有误。请通过上述联系方式报告错误，并注明具体卷次和内容。</p>
    """, unsafe_allow_html=True)

with st.expander("Q: 你们提供API接口吗？"):
    st.markdown("""
    <p>目前暂不提供API接口。如有学术合作需求，欢迎联系我们洽谈。</p>
    """, unsafe_allow_html=True)

st.markdown("### 📝 反馈表单")

with st.form("contact_form"):
    col_form1, col_form2 = st.columns(2)
    
    with col_form1:
        name = st.text_input("您的姓名")
    with col_form2:
        email = st.text_input("电子邮箱")
    
    subject = st.selectbox("反馈主题", ["问题反馈", "数据纠错", "合作建议", "其他"])
    
    message = st.text_area("留言内容", height=150)
    
    submitted = st.form_submit_button("提交反馈")
    
    if submitted:
        if name and email and message:
            st.success("感谢您的反馈！我们会尽快处理。")
        else:
            st.warning("请填写完整信息")

st.markdown("---")

st.markdown("### ⏰ 响应时间")

st.markdown("""
<div class="info-box">
    <p class="content-text">
        我们通常会在 <strong>1-3 个工作日</strong> 内回复您的邮件。对于复杂问题，可能需要更长时间，我们会尽快处理。
    </p>
    <p class="content-text">
        感谢您的理解和支持！
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #95A5A6; font-size: 13px;">
    <p>© 2024 八闽通志数据库 · 基于学术目的构建</p>
</div>
""", unsafe_allow_html=True)
