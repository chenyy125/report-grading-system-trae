#!/usr/bin/env python3
"""文档解析模块 - 支持docx和pdf文件解析"""

import os
from pathlib import Path

def parse_document(file_path):
    """解析文档文件，返回文本内容和图片信息"""
    ext = Path(file_path).suffix.lower()
    
    if ext == '.docx':
        return parse_docx(file_path)
    elif ext == '.pdf':
        return parse_pdf(file_path)
    elif ext in ('.txt', '.md'):
        return parse_text(file_path)
    else:
        return {'text': '', 'images': [], 'error': f'不支持的文件格式: {ext}'}

def parse_docx(file_path):
    """解析docx文件"""
    try:
        from docx import Document
        
        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])
        
        images = []
        for rel in doc.part.rels.values():
            if 'image' in rel.target_ref:
                images.append({'name': rel.target_ref, 'type': 'docx_image'})
        
        return {'text': text, 'images': images, 'error': None}
    except Exception as e:
        return {'text': '', 'images': [], 'error': str(e)}

def parse_pdf(file_path):
    """解析pdf文件"""
    try:
        import pdfplumber
        
        with pdfplumber.open(file_path) as pdf:
            text = '\n'.join([page.extract_text() or '' for page in pdf.pages])
            images = []
            for i, page in enumerate(pdf.pages):
                for img in page.images:
                    images.append({
                        'name': f'page_{i+1}_img_{len(images)+1}',
                        'type': 'pdf_image',
                        'width': img['width'],
                        'height': img['height']
                    })
        
        return {'text': text, 'images': images, 'error': None}
    except Exception as e:
        return {'text': '', 'images': [], 'error': str(e)}

def parse_text(file_path):
    """解析文本文件"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        return {'text': text, 'images': [], 'error': None}
    except Exception as e:
        return {'text': '', 'images': [], 'error': str(e)}

def extract_images_from_docx(docx_path, output_dir):
    """从docx文件中提取图片"""
    try:
        from docx import Document
        import zipfile
        
        os.makedirs(output_dir, exist_ok=True)
        images = []
        
        with zipfile.ZipFile(docx_path, 'r') as zf:
            for name in zf.namelist():
                if name.startswith('word/media/'):
                    img_name = os.path.basename(name)
                    img_path = os.path.join(output_dir, img_name)
                    with open(img_path, 'wb') as f:
                        f.write(zf.read(name))
                    images.append(img_path)
        
        return images
    except Exception as e:
        return []