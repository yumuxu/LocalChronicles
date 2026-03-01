# 八闽通志检索系统

基于《八闽通志》古籍的结构化数据检索平台

## 功能特性

- 📚 **全局搜索** - 支持关键词全文检索（建宁府、屯田、曾巩等）
- 📖 **卷次导航** - 侧边栏快速跳转指定卷
- 📊 **统计概览** - 查看数据统计信息
- 🎯 **结果高亮** - 搜索结果关键词高亮显示
- 📄 **双栏阅读** - 左侧正文，右侧结构化信息

## 运行方式

### 方式一：直接运行（推荐）

```bash
pip install streamlit
streamlit run app.py
```

### 方式二：使用 Python 脚本

```bash
python run_app.py
```

### 方式三：使用虚拟环境

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行
streamlit run app.py
```

## 项目结构

```
LocalChronicles/
├── app.py                 # Streamlit 主程序
├── requirements.txt       # Python 依赖
├── run_app.py            # 启动脚本
├── structured_data/      # 结构化 JSON 数据
│   ├── 卷01_地理.json
│   ├── 卷02.json
│   └── ...
└── volumes/              # 原始分卷文本
    ├── 卷01_地理.txt
    ├── 卷02.txt
    └── ...
```

## 访问地址

启动后访问: http://localhost:8501

## 搜索示例

- "建宁府" - 搜索福州府相关记载
- "山川" - 搜索山川地理
- "宋" - 搜索宋代相关记载
- "曾巩" - 搜索历史人物
