# 部署指南：将应用上传到网上

## 方法一：Streamlit Cloud（推荐，完全免费）

### 步骤1：准备必要的文件

确保你的项目目录包含以下文件：
```
fanxiu/
├── app.py                          # Streamlit应用
├── requirements.txt                # Python依赖
├── extra_survival_trees_model.pkl  # 训练好的模型
├── model_info.json                 # 模型信息
└── README.md                       # 说明文档
```

### 步骤2：推送到GitHub

1. 在你的项目目录初始化Git仓库：
```bash
cd C:\Users\YQL\Desktop\fanxiu
git init
```

2. 创建.gitignore文件（排除大文件）：
```bash
echo "data.csv" >> .gitignore
echo "*.pyc" >> .gitignore
echo "__pycache__" >> .gitignore
echo "*.pkl" >> .gitignore
echo "survival_analysis_results_*" >> .gitignore
```

3. 添加文件到Git：
```bash
git add app.py requirements.txt README.md
git add .gitignore
```

4. 提交更改：
```bash
git commit -m "Initial commit: Prostate cancer survival prediction app"
```

5. 在GitHub上创建新仓库（访问 https://github.com/new）

6. 关联远程仓库并推送：
```bash
git remote add origin https://github.com/你的用户名/仓库名.git
git branch -M main
git push -u origin main
```

### 步骤3：在Streamlit Cloud部署

1. 访问：https://share.streamlit.io/
2. 点击 "New app"
3. 填写信息：
   - **Repository**: 选择你的GitHub仓库
   - **Branch**: main
   - **Main file path**: app.py
4. 点击 "Deploy" 

5. **重要**：由于模型文件太大，需要直接上传到Streamlit Cloud
   - 部署后，在应用页面点击 "..." → "Files"
   - 上传 `extra_survival_trees_model.pkl` 和 `model_info.json`

### 步骤4：完成

等待几分钟，你的应用就会在以下地址可用：
`https://你的用户名-仓库名-app.streamlit.app`

---

## 方法二：Render（免费tier）

### 步骤1：创建GitHub仓库（同上）

### 步骤2：修改app.py文件

在app.py顶部添加（用于Web服务器）：
```python
import sys
import os
sys.path.append(os.path.dirname(__file__))
```

### 步骤3：在Render部署

1. 访问：https://render.com/
2. 注册并登录
3. 点击 "New +" → "Web Service"
4. 连接GitHub仓库
5. 配置：
   - **Runtime**: Python 3
   - **Build Command**: pip install -r requirements.txt
   - **Start Command**: streamlit run app.py --server.port=$PORT
6. 点击 "Deploy"

---

## 方法三：自己的服务器（VPS）

### 使用Docker部署

1. 创建Dockerfile：
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY extra_survival_trees_model.pkl .
COPY model_info.json .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. 构建并运行：
```bash
docker build -t prostate-cancer-app .
docker run -p 8501:8501 prostate-cancer-app
```

3. 访问：http://你的服务器IP:8501

---

## 方法四：Hugging Face Spaces（免费）

### 步骤1：创建Hugging Face账号

访问：https://huggingface.co/join

### 步骤2：创建新的Space

1. 点击右上角 "+" → "New Space"
2. 配置：
   - **Space name**: 自己取名
   - **License**: 选择
   - **SDK**: Streamlit
   - **Public**: 勾选

### 步骤3：上传文件

上传以下文件到Space：
- app.py
- requirements.txt
- extra_survival_trees_model.pkl
- model_info.json

### 步骤4：等待部署

访问你的Space地址即可看到应用

---

## 常见问题

### Q1: 模型文件太大，Git推不上去怎么办？
**A1:** 使用Git LFS或直接上传到云平台：
```bash
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git commit -m Track pkl files with Git LFS
git push
```

### Q2: Streamlit Cloud免费额度限制？
**A2:** 免费3小时内CPU时间/月，适合演示。如需更多使用：
- 升级到Professional（$20/月）
- 使用自己的服务器部署

### Q3: 如何自定义域名？
**A3:** 
- Streamlit Cloud：在Settings → Advanced→ Custom domain
- 需要：域名+ CNAME记录指向 `*.streamlit.app`

### Q4: 应用运行慢怎么办？
**A4:** 
- 减少模型复杂度
- 使用缓存：`@st.cache_data`
- 优化数据加载

---

## 推荐方案总结

| 方案 | 费用 | 难度 | 推荐度 |
|------|------|------|--------|
| Streamlit Cloud | 免费 | 简单 | ⭐⭐⭐⭐⭐ |
| Hugging Face | 免费 | 简单 | ⭐⭐⭐⭐⭐ |
| Render | 免费/付费 | 中等 | ⭐⭐⭐⭐ |
| 自己服务器 | 付费 | 困难 | ⭐⭐⭐ |

**建议首次部署使用Streamlit Cloud或Hugging Face，简单快速且完全免费！**
