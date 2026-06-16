#!/usr/bin/env python3
"""配置模块 - 管理系统配置"""

import json
import os

DEFAULT_CONFIG = {
    'weights': {
        'images': 50,
        'structure': 20,
        'content': 30
    },
    'image_thresholds': {
        'excellent': 0.8,
        'good': 0.6,
        'medium': 0.4,
        'pass': 0.2
    },
    'supported_formats': ['.docx', '.pdf', '.doc', '.txt', '.md', '.rtf', '.odt'],
    'output_formats': ['json', 'html'],
    'project_types': {
        'default': {
            'name': '通用项目',
            'features': ['图1', '图2', '图3', '图4', '图5']
        },
        'project_lena': {
            'name': 'Lena图像处理',
            'features': ['原始图像', '灰度图', '直方图均衡化', '滤波处理', '边缘检测']
        },
        'project_pedestrian': {
            'name': '行人检测',
            'features': ['行人检测图1', '行人检测图2', '行人检测图3', '行人检测图4', '行人检测图5']
        },
        'project_rag': {
            'name': 'RAG问答系统',
            'features': ['系统架构图', '流程图', '测试结果图', '性能对比图']
        }
    },
    'cross_submission_threshold': 0.3,
    'batch_processing_enabled': True,
    'auto_detect_project': True
}

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f'配置文件加载失败，使用默认配置: {e}')
                return DEFAULT_CONFIG
        else:
            return DEFAULT_CONFIG
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f'配置文件保存失败: {e}')
            return False
    
    def get_weights(self):
        """获取评分权重"""
        return self.config.get('weights', DEFAULT_CONFIG['weights'])
    
    def set_weights(self, weights):
        """设置评分权重"""
        self.config['weights'] = weights
        return self.save_config()
    
    def get_project_types(self):
        """获取项目类型列表"""
        return self.config.get('project_types', DEFAULT_CONFIG['project_types'])
    
    def get_project_features(self, project_id):
        """获取指定项目的特征列表"""
        project_types = self.get_project_types()
        return project_types.get(project_id, {}).get('features', [])
    
    def get_supported_formats(self):
        """获取支持的文件格式"""
        return self.config.get('supported_formats', DEFAULT_CONFIG['supported_formats'])
    
    def get_image_thresholds(self):
        """获取图片阈值配置"""
        return self.config.get('image_thresholds', DEFAULT_CONFIG['image_thresholds'])
    
    def get_cross_threshold(self):
        """获取交错作业检测阈值"""
        return self.config.get('cross_submission_threshold', DEFAULT_CONFIG['cross_submission_threshold'])
    
    def is_batch_enabled(self):
        """是否启用批量处理"""
        return self.config.get('batch_processing_enabled', True)
    
    def is_auto_detect_enabled(self):
        """是否启用自动检测项目类型"""
        return self.config.get('auto_detect_project', True)

config_manager = ConfigManager()