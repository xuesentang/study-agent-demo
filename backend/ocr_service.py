"""
OCR 图片识别服务
支持图片中的文字和公式识别
"""

from paddleocr import PaddleOCR
from typing import List, Dict
import tempfile
import os
import base64
from io import BytesIO
from PIL import Image


class OCRService:
    """OCR服务类"""
    
    def __init__(self):
        # 初始化OCR引擎
        # use_angle_cls=True 支持旋转文字识别
        # lang='ch' 中文识别
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='ch',
            show_log=False  # 减少日志输出
        )
    
    def recognize_image(self, image_data: bytes) -> Dict:
        """
        识别图片中的文字
        
        Args:
            image_data: 图片二进制数据
            
        Returns:
            识别结果，包含文字列表和坐标信息
        """
        # 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            tmp.write(image_data)
            tmp_path = tmp.name
        
        try:
            # 执行OCR
            result = self.ocr.ocr(tmp_path, cls=True)
            
            # 解析结果
            texts = []
            boxes = []
            scores = []
            
            if result and result[0]:
                for line in result[0]:
                    if line:
                        box = line[0]  # 文字框坐标
                        text = line[1][0]  # 识别文字
                        score = line[1][1]  # 置信度
                        
                        texts.append(text)
                        boxes.append(box)
                        scores.append(score)
            
            return {
                "success": True,
                "texts": texts,
                "full_text": "\n".join(texts),
                "boxes": boxes,
                "scores": scores,
                "text_count": len(texts)
            }
            
        finally:
            # 清理临时文件
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def recognize_base64(self, base64_string: str) -> Dict:
        """
        识别Base64编码的图片
        
        Args:
            base64_string: Base64编码的图片数据
            
        Returns:
            识别结果
        """
        # 移除可能的data URL前缀
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # 解码
        image_data = base64.b64decode(base64_string)
        
        return self.recognize_image(image_data)
    
    def recognize_formula(self, image_data: bytes) -> Dict:
        """
        识别数学公式（简化版，实际可用专门公式识别模型）
        
        Args:
            image_data: 图片二进制数据
            
        Returns:
            识别结果
        """
        result = self.recognize_image(image_data)
        
        # 简单的公式字符映射
        formula_hints = []
        full_text = result.get("full_text", "")
        
        # 检测可能的公式特征
        if any(c in full_text for c in ['∫', '∑', '∏', '√', 'lim', '→', '∞']):
            formula_hints.append("检测到积分/极限符号")
        if any(c in full_text for c in ['α', 'β', 'γ', 'θ', 'π']):
            formula_hints.append("检测到希腊字母")
        if any(c in full_text for c in ['²', '³', 'ⁿ', '√']):
            formula_hints.append("检测到上下标/根号")
        
        result["formula_hints"] = formula_hints
        result["is_likely_formula"] = len(formula_hints) > 0
        
        return result


# 全局OCR服务实例
_ocr_instance = None

def get_ocr_service() -> OCRService:
    """获取OCR服务单例"""
    global _ocr_instance
    if _ocr_instance is None:
        print("🔄 正在初始化OCR引擎，首次加载可能需要一些时间...")
        _ocr_instance = OCRService()
        print("✅ OCR引擎初始化完成")
    return _ocr_instance