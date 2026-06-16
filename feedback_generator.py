#!/usr/bin/env python3
"""评语生成模块 - 根据评分结果生成个性化评语"""

class FeedbackGenerator:
    """评语生成器"""
    
    def __init__(self):
        self.strength_templates = {
            'images_high': ['图片内容与参考答案高度匹配', '图片数量充足，符合要求'],
            'images_medium': ['图片内容基本匹配', '图片数量基本符合要求'],
            'structure_high': ['报告结构完整，章节划分合理', '章节安排逻辑清晰'],
            'structure_medium': ['报告结构基本完整', '章节划分较为合理'],
            'content_high': ['内容与参考答案高度一致', '技术描述准确'],
            'content_medium': ['内容基本匹配参考答案', '核心知识点覆盖']
        }
        
        self.weakness_templates = {
            'images_low': ['图片数量不足', '部分图片内容与参考答案存在差异'],
            'structure_low': ['报告结构不够完整', '章节划分需要调整'],
            'content_low': ['部分内容需要完善', '技术描述不够准确']
        }
        
        self.suggestion_templates = [
            '建议检查并修正图片内容，确保与参考答案一致',
            '建议补充缺失的图片',
            '建议在答辩前通读报告，检查内容完整性',
            '准备3-6分钟的答辩展示，重点说明实验过程',
            '建议参考参考答案完善报告结构'
        ]
    
    def generate_feedback(self, score_result, comparison_details):
        """生成完整的评语"""
        strengths = self._generate_strengths(score_result, comparison_details)
        weaknesses = self._generate_weaknesses(score_result, comparison_details)
        suggestions = self._generate_suggestions(score_result, comparison_details)
        summary = self._generate_summary(score_result, comparison_details)
        
        return {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'suggestions': suggestions,
            'summary': summary
        }
    
    def _generate_strengths(self, score_result, details):
        """生成优点列表"""
        strengths = []
        
        if score_result['image_score'] >= 40:
            strengths.extend(self.strength_templates['images_high'])
        elif score_result['image_score'] >= 30:
            strengths.extend(self.strength_templates['images_medium'])
        
        if score_result['structure_score'] >= 16:
            strengths.extend(self.strength_templates['structure_high'])
        elif score_result['structure_score'] >= 12:
            strengths.extend(self.strength_templates['structure_medium'])
        
        if score_result['content_score'] >= 24:
            strengths.extend(self.strength_templates['content_high'])
        elif score_result['content_score'] >= 18:
            strengths.extend(self.strength_templates['content_medium'])
        
        return strengths[:3]
    
    def _generate_weaknesses(self, score_result, details):
        """生成不足列表"""
        weaknesses = []
        
        if score_result['image_score'] < 30:
            weaknesses.extend(self.weakness_templates['images_low'])
        
        if score_result['structure_score'] < 12:
            weaknesses.extend(self.weakness_templates['structure_low'])
        
        if score_result['content_score'] < 18:
            weaknesses.extend(self.weakness_templates['content_low'])
        
        return weaknesses[:3]
    
    def _generate_suggestions(self, score_result, details):
        """生成改进建议"""
        suggestions = []
        
        if score_result['image_score'] < 40:
            suggestions.append(self.suggestion_templates[0])
            suggestions.append(self.suggestion_templates[1])
        
        if score_result['structure_score'] < 16:
            suggestions.append(self.suggestion_templates[4])
        
        suggestions.append(self.suggestion_templates[2])
        suggestions.append(self.suggestion_templates[3])
        
        return suggestions[:4]
    
    def _generate_summary(self, score_result, details):
        """生成总结评语"""
        total = score_result['total_score']
        grade = score_result['grade']
        
        if total >= 90:
            return f'🎉 报告完美（得分: {total}）！内容与参考答案完全一致，所有图片内容匹配，结构完整。恭喜！'
        elif total >= 80:
            return f'报告整体{grade}（得分: {total}）。图片内容基本匹配，结构完整，建议继续完善细节。'
        elif total >= 70:
            return f'报告整体{grade}（得分: {total}）。图片数量基本符合要求，部分内容需要完善。建议参考参考答案进行修改。'
        elif total >= 60:
            return f'报告整体{grade}（得分: {total}）。图片匹配度和内容完整性有待提高，建议仔细检查并修正。'
        else:
            return f'报告未达到及格标准（得分: {total}）。图片数量不足，内容与参考答案差异较大，请重新完成报告。'
    
    def generate_detailed_comments(self, score_result, weights):
        """生成详细评语"""
        comments = []
        
        comments.append({
            'category': '图片匹配度',
            'score': score_result['image_score'],
            'max_score': weights.get('images', 50),
            'comment': self._get_image_comment(score_result['image_score'])
        })
        
        comments.append({
            'category': '结构完整性',
            'score': score_result['structure_score'],
            'max_score': weights.get('structure', 20),
            'comment': self._get_structure_comment(score_result['structure_score'])
        })
        
        comments.append({
            'category': '内容匹配度',
            'score': score_result['content_score'],
            'max_score': weights.get('content', 30),
            'comment': self._get_content_comment(score_result['content_score'])
        })
        
        return comments
    
    def _get_image_comment(self, score):
        if score >= 40:
            return '图片内容与参考答案高度匹配，数量充足'
        elif score >= 30:
            return '图片内容基本匹配，数量符合要求'
        elif score >= 15:
            return '部分图片内容需要调整'
        else:
            return '图片数量不足，内容需要完善'
    
    def _get_structure_comment(self, score):
        if score >= 16:
            return '报告结构完整，章节划分合理'
        elif score >= 12:
            return '报告结构基本完整'
        else:
            return '报告结构需要完善'
    
    def _get_content_comment(self, score):
        if score >= 24:
            return '内容与参考答案高度一致'
        elif score >= 18:
            return '内容基本匹配，核心知识点覆盖'
        else:
            return '内容需要进一步完善'