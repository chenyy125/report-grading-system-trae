#!/usr/bin/env python3
"""内容比对模块 - 计算文档相似度和图片匹配度"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compare_documents(ref_text, stu_text):
    """比较两份文档的内容相似度"""
    if not ref_text or not stu_text:
        return 0.0
    
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([ref_text, stu_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except Exception as e:
        return 0.0

def compare_images(ref_images, stu_images):
    """比较图片匹配度"""
    ref_count = len(ref_images)
    stu_count = len(stu_images)
    
    if ref_count == 0:
        return {'ratio': 1.0, 'match_count': stu_count, 'total_count': stu_count}
    
    ratio = min(1.0, stu_count / ref_count)
    match_count = min(stu_count, ref_count)
    
    return {
        'ratio': ratio,
        'match_count': match_count,
        'ref_count': ref_count,
        'stu_count': stu_count
    }

def compare_structure(ref_text, stu_text):
    """比较文档结构完整性"""
    ref_sections = extract_sections(ref_text)
    stu_sections = extract_sections(stu_text)
    
    matched_sections = sum(1 for sec in stu_sections if sec in ref_sections)
    total_sections = max(len(ref_sections), len(stu_sections))
    
    if total_sections == 0:
        return 0.0
    
    return matched_sections / total_sections

def extract_sections(text):
    """从文本中提取章节标题"""
    sections = []
    keywords = ['实训目的', '实验目的', '目的',
                '实训步骤', '实验步骤', '步骤',
                '实验结果', '结果分析', '结果',
                '问题反思', '心得体会', '总结',
                '参考文献', '附录']
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        for kw in keywords:
            if kw in line and len(line) < 50:
                sections.append(kw)
                break
    
    return list(set(sections))

def analyze_image_content(image_path):
    """分析图片内容（简化版）"""
    try:
        from PIL import Image
        
        img = Image.open(image_path)
        return {
            'width': img.width,
            'height': img.height,
            'format': img.format,
            'size_bytes': os.path.getsize(image_path) if os.path.exists(image_path) else 0
        }
    except Exception as e:
        return {'error': str(e)}