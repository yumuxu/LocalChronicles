import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="博文 - 八闽通志",
    page_icon="📝",
    layout="wide"
)

articles = [
    {
        "id": 1,
        "title": "《八闽通志》概述：福建现存最早的省志",
        "category": "学术研究",
        "date": "2024-01-15",
        "excerpt": "《八闽通志》是福建省现存最早的地方志，由明代黄仲昭编纂，成书于明弘治二年（1489年）...",
        "content": """《八闽通志》是福建省现存最早的地方志，由明代黄仲昭编纂，成书于明弘治二年（1489年）。

黄仲昭（1425-1502），名潜，以字行，福建莆田人。他历时数十年，参阅大量史料，终于完成了这部涵盖福建八府一州的大型地方志。

本书凡八十七卷，分为地理、食货、秩官、选举、人物、学校、典礼、兵制、外志等门类，系统记载了明代福建的自然地理、历史沿革、社会经济、文化教育等各方面的情况。

《八闽通志》的编纂体例严谨，资料丰富，对后世福建地方志的编纂产生了深远影响，也是研究福建历史文化的宝贵资料。""",
        "tags": ["八闽通志", "地方志", "黄仲昭", "明代"]
    },
    {
        "id": 2,
        "title": "八闽地理志：福建八府的历史变迁",
        "category": "地理研究",
        "date": "2024-01-20",
        "excerpt": "宋代福建分为福州、建州、泉州、漳州、汀州、南剑州、邵武军、兴化军，至元代改为路，明代改为府...",
        "content": """宋代福建行政区的设置经历了多次变迁。

宋代福建分为福州、建州、泉州、漳州、汀州、南剑州、邵武军、兴化军，共八州军。其中福州为帅府，建州为望郡。

元代至元十五年（1278年），改建州为建宁路，其他州军也陆续改为路。

明代改路为府，福建设福州府、建宁府、泉州府、漳州府、汀州府、延平府、邵武府、兴化府、福宁州，形成八府一州的格局。

清代沿用明制，只是将福宁州升为福宁府。

《八闽通志》地理卷详细记载了各府州的沿革、疆域、山川、风俗等内容，是研究福建历史地理的重要文献。""",
        "tags": ["地理", "行政區劃", "府", "历史"]
    },
    {
        "id": 3,
        "title": "从《八闽通志》看明代福建教育",
        "category": "教育研究",
        "date": "2024-02-01",
        "excerpt": "明代福建教育发达，书院众多，《八闽通志·学校》卷详细记载了各府州县的儒学、书院、社学等...",
        "content": """明代福建教育在中国教育史上占有重要地位。

据《八闽通志》记载，明代福建各府州县均设有儒学，作为官办教育机构。此外，还有大量的书院和社学。

福州府设有福州府学和闽县、侯官县学；建宁府设有建宁府学和建阳县学等。各县学设有教谕、训导等学官，负责教育管理。

书院方面，著名的有福州的鳌峰书院、建阳的考亭书院等。这些书院不仅是教育场所，也是学术交流的中心。

明代福建科举成绩优异，进士人数众多，这与发达的教育体系密切相关。《八闽通志》学校卷为我们提供了明代福建教育的详细资料。""",
        "tags": ["教育", "书院", "儒学", "科举"]
    },
    {
        "id": 4,
        "title": "福建海上丝绸之路的兴衰",
        "category": "经济研究",
        "date": "2024-02-10",
        "excerpt": "泉州自宋代以来就是著名的海港，《八闽通志》记载了明代福建对外贸易的繁荣景象...",
        "content": """福建是中国海上丝绸之路的重要起点。

宋代，泉州成为当时世界第一大港，号为“东方第一大港”。元代马可·波罗曾盛赞泉州港的繁荣。

明代实行海禁政策，但福建沿海的对外贸易并未完全中断。《八闽通志》食货卷记载了福建的市舶、海运等情况。

明代后期，私人海外贸易逐渐兴起，漳州月港成为福建最主要的对外贸易港口。

清代康熙年间解除海禁后，厦门成为福建对外贸易的中心。

《八闽通志》为我们了解明代及之前福建的对外经济交流提供了珍贵的历史资料。""",
        "tags": ["海丝", "对外贸易", "泉州", "港口"]
    },
    {
        "id": 5,
        "title": "闽南文化的历史源流",
        "category": "文化研究",
        "date": "2024-02-15",
        "excerpt": "闽南文化是中华文化的重要组成部分，《八闽通志》风俗卷详细记载了明代福建各府州的风俗习惯...",
        "content": """闽南文化是以闽南民系为主体，创造传承的物质与精神文化的总和。

闽南文化的形成经历了漫长的历史过程。闽南地区早在秦汉时期就与中原有交往，两晋南北朝时期大量中原移民南迁，带来了先进的中原文化。

唐宋时期，闽南地区经济文化快速发展，形成了独特的闽南文化。明清时期，闽南文化随着移民传播到台湾、东南亚等地。

《八闽通志》风俗卷记载了明代闽南地区的生活习俗、岁时节令、婚丧嫁娶等方面的内容，是我们了解闽南文化的重要文献。

闽南文化具有鲜明的特点：重商、敢闯、重教、崇文。这些特点在《八闽通志》中都有所体现。""",
        "tags": ["闽南文化", "风俗", "移民", "传统"]
    },
    {
        "id": 6,
        "title": "《八闽通志》人物卷中的福建先贤",
        "category": "人物研究",
        "date": "2024-02-20",
        "excerpt": "《八闽通志》人物卷记载了大量福建历史上的杰出人物，包括理学家、文学家、科学家等...",
        "content": """《八闽通志》人物卷是全书的重要组成部分，记载了福建历史上各类杰出人物。

理学方面，有朱熹门下的黄干、陈淳等闽学传人。朱熹曾在福建讲学授徒，形成了著名的闽学学派。

文学方面，有柳永、黄伯思等词人、学者。柳永是宋代著名词人，被誉为“词宗”。

科技方面，有苏颂、宋慈等著名人物。苏颂主持编写了《新仪象法要》，是宋代科技的重要成就；宋慈是著名法医学家，所著《洗冤集录》是世界上最早的法医学专著。

此外，还有大量的抗元、抗清英雄，以及孝子、节妇等。

《八闽通志》人物卷为我们研究福建历史人物提供了丰富的资料。""",
        "tags": ["人物", "先贤", "理学", "文化"]
    }
]

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

.article-card {
    background: white;
    border: 1px solid #DDD8CC;
    border-radius: 8px;
    padding: 25px;
    margin: 15px 0;
    transition: all 0.3s ease;
}

.article-card:hover {
    border-color: #B8A882;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}

.category-tag {
    display: inline-block;
    padding: 4px 12px;
    background: linear-gradient(135deg, #B8A882 0%, #A09070 100%);
    color: white;
    border-radius: 15px;
    font-size: 12px;
    margin-right: 10px;
}

.date-tag {
    color: #95A5A6;
    font-size: 13px;
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

.stat-box {
    background: linear-gradient(145deg, #FDFCF0, #F5F0E0);
    border-left: 4px solid #B8A882;
    padding: 15px;
    border-radius: 0 8px 8px 0;
}

.section-title {
    font-size: 24px;
    font-weight: 600;
    color: #2C3E50;
    margin: 20px 0 15px 0;
    padding-bottom: 10px;
    border-bottom: 2px solid #B8A882;
}

.content-text {
    font-size: 16px;
    line-height: 2;
    text-align: justify;
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
    st.markdown("### 📊 文章统计")
    st.markdown('<div class="stat-box">', unsafe_allow_html=True)
    st.metric("文章总数", len(articles))
    categories = list(set(a['category'] for a in articles))
    st.metric("文章分类", len(categories))
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
    <h1 style="font-size: 36px; margin-bottom: 10px; color: #2C3E50 !important;">📝 原创博文</h1>
    <p style="font-size: 16px; color: #7F8C8D; margin-bottom: 0;">学术研究、文献解读、文化漫谈</p>
</div>
""", unsafe_allow_html=True)

categories = ["全部"] + sorted(list(set(a['category'] for a in articles)))
selected_category = st.radio("选择分类", categories, horizontal=True, label_visibility="collapsed")

filtered_articles = articles if selected_category == "全部" else [a for a in articles if a['category'] == selected_category]

st.markdown(f"### 📋 共 {len(filtered_articles)} 篇文章")

for article in filtered_articles:
    st.markdown(f"""
    <div class="article-card">
        <div style="margin-bottom: 10px;">
            <span class="category-tag">{article['category']}</span>
            <span class="date-tag">📅 {article['date']}</span>
        </div>
        <h3 style="margin: 10px 0; color: #2C3E50;">{article['title']}</h3>
        <p style="color: #7F8C8D; font-size: 15px; margin: 10px 0;">{article['excerpt']}</p>
        <div style="margin-top: 15px;">
            {" ".join([f'<span style="display: inline-block; padding: 3px 10px; margin-right: 5px; background: #FAF8F0; border: 1px solid #E8E4D9; border-radius: 12px; font-size: 12px; color: #7F8C8D;">#{tag}</span>' for tag in article['tags']])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("阅读全文"):
        st.markdown(f'<div class="content-text">{article["content"]}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #95A5A6; font-size: 13px;">
    <p>© 2024 八闽通志数据库 · 基于学术目的构建</p>
</div>
""", unsafe_allow_html=True)
