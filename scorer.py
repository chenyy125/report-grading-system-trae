#!/usr/bin/env python3
"""评分模块 - 根据比对结果计算分数"""

class ReportScorer:
    """报告评分器"""
    
    def __init__(self, weights=None):
        self.weights = weights or {
            'images': 50,
            'structure': 20,
            'content': 30
        }
    
    def calculate_score(self, comparison_result):
        """计算总分"""
        image_score = self._calculate_image_score(comparison_result.get('image_comparison', {}))
        structure_score = self._calculate_structure_score(comparison_result.get('structure_similarity', 0))
        content_score = self._calculate_content_score(comparison_result.get('content_similarity', 0))
        
        total = image_score + structure_score + content_score
        
        return {
            'image_score': image_score,
            'structure_score': structure_score,
            'content_score': content_score,
            'total_score': total,
            'grade': self._get_grade(total)
        }
    
    def _calculate_image_score(self, image_comparison):
        """计算图片匹配度分数"""
        ratio = image_comparison.get('ratio', 0)
        
        if ratio >= 0.8:
            return self.weights['images']
        elif ratio >= 0.6:
            return int(self.weights['images'] * 0.8)
        elif ratio >= 0.4:
            return int(self.weights['images'] * 0.6)
        elif ratio >= 0.2:
            return int(self.weights['images'] * 0.3)
        else:
            return 0
    
    def _calculate_structure_score(self, similarity):
        """计算结构完整性分数"""
        return int(self.weights['structure'] * similarity)
    
    def _calculate_content_score(self, similarity):
        """计算内容匹配度分数"""
        return int(self.weights['content'] * similarity)
    
    def _get_grade(self, total_score):
        """根据总分获取等级"""
        if total_score >= 90:
            return '优秀'
        elif total_score >= 80:
            return '良好'
        elif total_score >= 70:
            return '中等'
        elif total_score >= 60:
            return '及格'
        else:
            return '不及格'
    
    def check_cross_submission(self, ref_features, stu_features, threshold=0.3):
        """检测是否交错作业"""
        common_features = set(ref_features) & set(stu_features)
        similarity = len(common_features) / max(len(ref_features), len(stu_features))
        return similarity < threshold

def calculate_weighted_score(image_ratio, structure_similarity, content_similarity, weights=None):
    """便捷函数：计算加权分数"""
    weights = weights or {'images': 50, 'structure': 20, 'content': 30}
    
    scorer = ReportScorer(weights)
    result = scorer.calculate_score({
        'image_comparison': {'ratio': image_ratio},
        'structure_similarity': structure_similarity,
        'content_similarity': content_similarity
    })
    
    return result