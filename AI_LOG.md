# AI_LOG.md - Trae交互记录

## 记录1：项目架构设计
**问题**：如何设计一个实训报告智能批改系统的架构？

**Trae回答**：
```
推荐架构：
1. document_parser.py - 文档解析模块（支持docx, pdf）
2. comparator.py - 内容比对模块
3. scorer.py - 评分模块
4. feedback_generator.py - 评语生成模块
5. main.py - 命令行入口
6. app.py - Streamlit Web界面
```

**理解与修改**：采用模块化设计，每个模块职责清晰，便于后续扩展和维护。

## 记录2：文档解析实现
**问题**：如何解析docx和pdf文件中的文本和图片？

**Trae回答**：
```python
from docx import Document
import pdfplumber

def parse_docx(file_path):
    doc = Document(file_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

def parse_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = '\n'.join([page.extract_text() for page in pdf.pages])
    return text
```

**理解与修改**：使用python-docx和pdfplumber库，分别处理docx和pdf格式。

## 记录3：内容相似度计算
**问题**：如何计算两份文档的内容相似度？

**Trae回答**：
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return similarity
```

**理解与修改**：使用TF-IDF向量化和余弦相似度计算，能有效衡量文本相似度。

## 记录4：图片处理与分析
**问题**：如何检测报告中的图片并评估？

**Trae回答**：
```python
from docx import Document
from PIL import Image

def extract_images_from_docx(file_path):
    doc = Document(file_path)
    images = []
    for rel in doc.part.rels.values():
        if 'image' in rel.target_ref:
            images.append(rel.target_ref)
    return images

def analyze_image(image_path):
    img = Image.open(image_path)
    return {'width': img.width, 'height': img.height, 'format': img.format}
```

**理解与修改**：提取docx中的图片，分析图片尺寸和格式信息。

## 记录5：个性化评语生成
**问题**：如何根据评分结果生成个性化评语？

**Trae回答**：
```python
def generate_feedback(score_data):
    feedback = []
    if score_data['images_score'] >= 90:
        feedback.append('图片内容与参考答案高度匹配')
    else:
        feedback.append(f'图片匹配度有待提高（得分{score_data["images_score"]}）')
    return feedback
```

**理解与修改**：根据各维度得分生成针对性的评语，包含优点和改进建议。