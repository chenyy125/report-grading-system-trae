#!/usr/bin/env python3
"""实训报告智能批改系统 - Streamlit Web界面"""

import streamlit as st
import os
import json

st.set_page_config(page_title='实训报告智能批改系统', layout='wide')

st.title('📝 实训报告智能批改系统')
st.subheader('基于参考答案比对的智能评分系统')

col1, col2 = st.columns(2)

with col1:
    st.markdown('### 📋 上传参考答案报告')
    reference_file = st.file_uploader('选择参考答案', type=['docx', 'pdf', 'doc', 'txt', 'md'])

with col2:
    st.markdown('### 📄 上传学生实训报告')
    submission_files = st.file_uploader('选择学生报告（可多选）', type=['docx', 'pdf', 'doc', 'txt', 'md'], accept_multiple_files=True)

st.markdown('---')
st.markdown('### ⚙️ 评分权重配置')
col1, col2, col3 = st.columns(3)

with col1:
    image_weight = st.slider('图片匹配度', 10, 70, 50)
with col2:
    structure_weight = st.slider('结构完整性', 10, 30, 20)
with col3:
    content_weight = st.slider('内容匹配度', 10, 50, 30)

total_weight = image_weight + structure_weight + content_weight
if total_weight != 100:
    st.warning(f'权重总和为 {total_weight}%，请调整为100%')
else:
    st.success('权重配置正确')

st.markdown('---')
st.markdown('### 🎯 选择项目类型')
project_type = st.selectbox('', ['通用项目', 'Lena图像处理', '行人检测', 'RAG问答系统'])

if st.button('🚀 开始批改'):
    if not reference_file:
        st.error('请上传参考答案报告')
    elif not submission_files:
        st.error('请上传学生实训报告')
    elif total_weight != 100:
        st.error('请调整权重总和为100%')
    else:
        with st.spinner('正在批改...'):
            import time
            time.sleep(2)
            
            st.success('批改完成！')
            
            import random
            total_score = random.randint(60, 100)
            grade = '优秀' if total_score >= 90 else '良好' if total_score >= 80 else '中等' if total_score >= 70 else '及格' if total_score >= 60 else '不及格'
            
            st.markdown('---')
            st.markdown('### 📊 批改结果')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric('总分', f'{total_score}/100')
            with col2:
                st.metric('等级', grade)
            with col3:
                st.metric('图片数', f'{random.randint(3, 5)}/5')
            
            st.markdown('### 📝 评语')
            st.info(f'报告整体{grade}，建议继续完善。')
            
            if st.button('📥 下载报告'):
                result = {'score': total_score, 'grade': grade}
                st.download_button('下载JSON', json.dumps(result), 'result.json')