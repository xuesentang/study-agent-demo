from enum import Enum, auto
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
import json


class StudyState(Enum):
    """学习状态枚举"""
    IDLE = "idle"                           # 初始状态
    SHOWING_ROUTE = "showing_route"         # 展示学习路线
    LEARNING_CHAIN = "learning_chain"       # 学习串联知识点
    LEARNING_KEYPOINT = "learning_keypoint" # 学习高频考点
    TESTING = "testing"                     # 做题测试
    REVIEWING = "reviewing"                 # 错题复习
    COMPLETED = "completed"                 # 学习完成


@dataclass
class KeyPoint:
    """高频考点数据类"""
    id: str
    name: str
    content: str           # 讲解内容（≤200字）
    question: str          # 测试题目
    answer: str            # 正确答案
    hint: str              # 提示
    difficulty: str = "medium" 
    backup_questions: List[Dict] = field(default_factory=list)  # 备份题目列表
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "question": self.question,
            "answer": self.answer,
            "hint": self.hint,
            "difficulty": self.difficulty
        }


@dataclass
class ChainPoint:
    """串联知识点数据类"""
    id: str
    name: str
    content: str           # 讲解内容（≤100字）
    next_connection: str   # 与下一个知识点的关联
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "next_connection": self.next_connection
        }


@dataclass
class Chapter:
    """章节数据类"""
    id: str
    title: str
    description: str
    estimated_time: int    # 预计学习时间（分钟）
    chain_points: List[ChainPoint]
    keypoints: List[KeyPoint]
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "estimated_time": self.estimated_time,
            "chain_points": [cp.to_dict() for cp in self.chain_points],
            "keypoints": [kp.to_dict() for kp in self.keypoints]
        }


# 预定义的学习内容（第一章：函数与极限）
DEFAULT_CHAPTER = Chapter(
    id="ch1",
    title="第一章 随机试验与随机事件",
    description="概率论与数理统计的基础，理解随机事件和随机试验的概念是后续学习的关键",
    estimated_time=20,
    chain_points=[
        ChainPoint(
            id="cp1",
            name="随机现象与确定性现象的概念",
            content="确定性现象：在给定条件下，某一结果一定会出现的现象，例如，任意三角形的内角和是多少度。随机现象：在一定条件下，有多种可能的结果且无法预知哪一个结果将会出现的现象，如随意投掷一枚硬币，落地时哪一面朝上。随机现象显著特点：对于随机现象进行一次或少数几次观察，其可能结果中出现哪一个是具有偶然性的；但是大量观察时，会发现所出现的结果具有一定的规律性。",
            next_connection="理解随机现象是理解随机试验的基础"
        ),
        ChainPoint(
            id="cp2",
            name="随机试验的定义和特点",
            content="是什么？为找出随机现象的内在规律而进行的大量、重复的试验。特点：可重复性、可观察性、不确定性。例如：为了解潮汐现象，每天同一时间测量同一河段的水位高低。",
            next_connection="理解随机试验是理解样本空间的基础"
        ),
        ChainPoint(
            id="cp3",
            name="样本空间的定义",
            content="一般地，把随机试验的每一种可能的结果称为一个样本点，称所有样本点的全体为该试验的样本空间，记为S（或Ω）.例如：①将一枚硬币抛掷两次，观察正面H、反面T出现的情况，则其样本点有四个，即正正、正反、反正和反反，样本空间S={（H，H），（H，T），（T，H），（T，T）}。",
            next_connection="掌握随机试验和样本空间的概念是理解随机事件的基础"
        ),
        ChainPoint(
            id="cp4",
            name="事件的分类，引出随机事件",
            content="在随机试验中，人们除了关心试验的结果本身外，往往还关心试验的结果是否具备某一指定的可观察的特征.在概率论中，把具有某一可观察特征的随机试验的结果称为事件.事件可分为以下三类：（1）随机事件，指在试验中可能发生也可能不发生的事件。（2）必然事件（3）不可能事件",
            next_connection="掌握事件的分类是理解事件的集合表示的基础"
        ),
        ChainPoint(
            id="cp5",
            name="事件的集合表示",
            content="样本空间S是随机试验的所有可能结果（样本点）的集合，每一个样本点是该集合的一个元素.一个事件是由具有该事件所要求的特征的那些可能结果所构成的，所以，一个事件是对应于S中具有相应特征的样本点所构成的集合，它是S的一个子集合.于是，任何一个事件都可以用S的某个子集来表示。仅含一个样本点的事件为基本事件；含有两个或两个以上样本点的事件为复合事件。",
            next_connection="掌握事件的集合表示后就可以开始学习随机事件的关系及运算"
        )
    ],
    keypoints=[
        KeyPoint(
            id="kp1",
            name="随机事件的关系和运算",
            content="随机事件的关系：包含、相等、和事件（A+B）、积事件（A*B）、差事件（A-B）、互斥（有A必无B）、对立（A∪B=Ω，且A∩B=Ø）随机事件的运算：①交换律　A∪B=B∪A，A∩B=B∩A.②结合律　（A∪B）∪C=A∪（B∪C），（A∩B）∩C=A∩（B∩C）.③分配律　（A∪B）∩C=（A∩C）∪（B∩C），（A∩B）∪C=（A∪C）∩（B∪C）",
            question="指出下列事件中哪些是必然事件？哪些是不可能事件？哪些是随机事件？A=“一副扑克牌中随机地抽出一张是黑桃”​；B=“没有水分，水稻种子发芽”​；C=“一副扑克牌中随机地抽出14张，至少有两种花色”​（除大小王）",
            answer="C是必然事件，B是不可能事件，A是随机事件",
            hint="根据生活经验判断即可",
            difficulty="easy",
            backup_questions=[
                {
                    "question": "如果事件A与事件B互斥，是否必有A与B互逆？反之如何？试举例说明.",
                    "answer": "A与B互斥，不一定有A与B互逆，因为互逆代表对立，而互斥只是代表不同时发生。如扔骰子，扔出6和扔出1是互斥事件，但是它们的并集不是全集，因此不是对立事件。反之，A与B互逆，则A与B必定互斥。还是扔骰子，扔3次扔出123点和扔出456点互逆，也是互斥事件。",
                    "hint": "根据随机事件的关系判断即可",
                    "difficulty": "easy"
                }
            ]
        )
        
    ]
)


class StudySession:
    """
    学习会话类
    管理用户的学习状态和进度
    """
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.state = StudyState.IDLE
        self.chapter = DEFAULT_CHAPTER
        
        # 学习进度
        self.current_chain_index = 0
        self.current_keypoint_index = 0
        self.completed_keypoints: Set[str] = set[Any]()
        self.wrong_attempts: Dict[str, int] = {}
        
        # 统计
        self.start_time = datetime.now()
        self.total_questions = 0
        self.correct_answers = 0
        
        # 当前测试的答案（用于复习状态）
        self.current_question_answer: Optional[str] = None
        self._current_backup_answer: Optional[str] = None  # 添加这行
    
    def get_progress(self) -> Dict:
        """获取当前学习进度"""
        total_keypoints = len(self.chapter.keypoints)
        completed = len(self.completed_keypoints)
        
        return {
            "completed": completed,
            "total": total_keypoints,
            "percentage": (completed / total_keypoints * 100) if total_keypoints > 0 else 0,
            "current_state": self.state.value,
            "elapsed_time": (datetime.now() - self.start_time).seconds // 60
        }
    
    def get_next_action(self) -> Dict[str, Any]:
        """
        根据当前状态决定下一步动作
        返回包含消息类型和内容的字典
        """
        if self.state == StudyState.IDLE:
            return self._show_route()
        
        elif self.state == StudyState.SHOWING_ROUTE:
            return self._start_chain_learning()
        
        elif self.state == StudyState.LEARNING_CHAIN:
            return self._start_keypoint_learning()
        
        elif self.state == StudyState.LEARNING_KEYPOINT:
            return self._show_question()
        
        elif self.state == StudyState.TESTING:
            return {
                "type": "waiting_answer",
                "content": "请输入你的答案..."
            }
        
        elif self.state == StudyState.REVIEWING:
            return self._show_review()
        
        elif self.state == StudyState.COMPLETED:
            return self._show_completion()
        
        return {
            "type": "error",
            "content": "未知状态，请重新开始"
        }
    
    def _show_route(self) -> Dict:
        """展示学习路线"""
        self.state = StudyState.SHOWING_ROUTE
        
        progress = self.get_progress()
        
        content = f"""📚 {self.chapter.title}

{self.chapter.description}

📋 学习内容：
• 串联知识点：{len(self.chapter.chain_points)} 个
• 高频考点：{len(self.chapter.keypoints)} 个

⏱️ 预计用时：{self.chapter.estimated_time} 分钟
📊 当前进度：{progress['completed']}/{progress['total']}

准备好开始学习了吗？回复"开始"进入学习流程。"""
        
        return {
            "type": "show_route",
            "content": content,
            "progress": progress,
            "chapter": self.chapter.to_dict()
        }
    
    def _start_chain_learning(self) -> Dict:
        """开始串联知识点学习"""
        if self.current_chain_index >= len(self.chapter.chain_points):
            # 串联知识点学习完成，进入考点学习
            self.state = StudyState.LEARNING_KEYPOINT
            return self._start_keypoint_learning()
        
        self.state = StudyState.LEARNING_CHAIN
        chain = self.chapter.chain_points[self.current_chain_index]
        
        content = f"""🔗 串联知识点 ({self.current_chain_index + 1}/{len(self.chapter.chain_points)})

【{chain.name}】

{chain.content}

💡 与后续关联：{chain.next_connection}

理解了这个概念吗？回复"继续"进入下一步。"""
        
        return {
            "type": "chain_knowledge",
            "content": content,
            "chain_point": chain.to_dict(),
            "progress": self.get_progress()
        }
    
    def _start_keypoint_learning(self) -> Dict:
        """开始高频考点学习"""
        if self.current_keypoint_index >= len(self.chapter.keypoints):
            # 所有考点学习完成
            self.state = StudyState.COMPLETED
            return self._show_completion()
        
        self.state = StudyState.LEARNING_KEYPOINT
        kp = self.chapter.keypoints[self.current_keypoint_index]
        
        # 如果已经做过这道题且正确，跳过
        if kp.id in self.completed_keypoints:
            self.current_keypoint_index += 1
            return self._start_keypoint_learning()
        
        content = f"""📌 高频考点 ({self.current_keypoint_index + 1}/{len(self.chapter.keypoints)})

【{kp.name}】
难度：{'⭐' * (1 if kp.difficulty == 'easy' else 2 if kp.difficulty == 'medium' else 3)}

{kp.content}

理解了吗？回复"懂了"开始做题测试。"""
        
        return {
            "type": "keypoint",
            "content": content,
            "keypoint": kp.to_dict(),
            "progress": self.get_progress()
        }
    
    def _show_question(self) -> Dict:
        """展示测试题目"""
        self.state = StudyState.TESTING
        kp = self.chapter.keypoints[self.current_keypoint_index]
        self.current_question_answer = kp.answer
        
        content = f"""📝 练习题

{kp.question}

请直接输入你的答案："""
        
        return {
            "type": "question",
            "content": content,
            "keypoint_id": kp.id,
            "progress": self.get_progress()
        }
    
    def check_answer(self, user_answer: str) -> Dict:
        """
        检查用户答案 - 使用大模型进行智能评估
        答错后显示正确答案并测试备用题目
        
        Args:
            user_answer: 用户输入的答案
            
        Returns:
            包含结果类型、内容和下一步动作的字典
        """
        if self.state != StudyState.TESTING and self.state != StudyState.REVIEWING:
            return {
                "type": "error",
                "content": "当前不是答题状态"
            }
        
        kp = self.chapter.keypoints[self.current_keypoint_index]
        self.total_questions += 1
        
        # 使用大模型评估答案正确性
        is_correct = self._evaluate_answer_with_llm(user_answer, kp)
        
        if is_correct:
            # ==================== 回答正确 ====================
            self.correct_answers += 1
            self.completed_keypoints.add(kp.id)
            self.wrong_attempts.pop(kp.id, None)  # 清除错误记录
            self._current_backup_answer = None  # 清除备用答案
            
            # 进入下一个知识点
            self.current_keypoint_index += 1
            
            if self.current_keypoint_index >= len(self.chapter.keypoints):
                # 所有知识点完成
                self.state = StudyState.COMPLETED
                return {
                    "type": "correct",
                    "content": "✅ 回答正确！",
                    "next_action": self._show_completion()
                }
            else:
                # 继续下一个知识点
                self.state = StudyState.LEARNING_CHAIN
                return {
                    "type": "correct",
                    "content": "✅ 回答正确！进入下一个考点...",
                    "next_action": self._start_keypoint_learning()
                }
        else:
            # ==================== 回答错误 ====================
            self.wrong_attempts[kp.id] = self.wrong_attempts.get(kp.id, 0) + 1
            
            # 检查是否有备用题目
            if kp.backup_questions and self.wrong_attempts[kp.id] <= len(kp.backup_questions):
                # 有备用题目，测试新题
                backup = kp.backup_questions[self.wrong_attempts[kp.id] - 1]
                self._current_backup_answer = backup["answer"]
                
                content = f"""❌ 回答错误。

💡 正确答案是：{kp.answer}

📝 新题目：{backup["question"]}

请回答："""
                
                self.state = StudyState.TESTING  # 保持在测试状态
                return {
                    "type": "wrong_new_question",
                    "content": content,
                    "progress": self.get_progress()
                }
            else:
                # 没有备用题目，进入下一考点
                self.current_keypoint_index += 1
                self._current_backup_answer = None
                
                if self.current_keypoint_index >= len(self.chapter.keypoints):
                    self.state = StudyState.COMPLETED
                    return {
                        "type": "wrong",
                        "content": f"❌ 回答错误。正确答案是：{kp.answer}",
                        "next_action": self._show_completion()
                    }
                else:
                    self.state = StudyState.LEARNING_CHAIN
                    return {
                        "type": "wrong",
                        "content": f"❌ 回答错误。正确答案是：{kp.answer}\n\n进入下一考点...",
                        "next_action": self._start_keypoint_learning()
                    }


    def _evaluate_answer_with_llm(self, user_answer: str, kp) -> bool:
        """
        使用大模型评估答案正确性
        
        Args:
            user_answer: 用户答案
            kp: 当前考点对象
            
        Returns:
            True表示答案正确，False表示错误
        """
        import os
        from openai import OpenAI
        
        # 获取正确答案（原题或备用题目）
        if hasattr(self, '_current_backup_answer') and self._current_backup_answer:
            correct_answer = self._current_backup_answer
            question_text = kp.backup_questions[self.wrong_attempts.get(kp.id, 1) - 1]["question"]
        else:
            correct_answer = kp.answer
            question_text = kp.question
        
        # 初始化OpenAI客户端
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
        
        # 构建评估提示词
        prompt = f"""请判断学生的答案是否正确。

【题目】
{question_text}

【标准答案】
{correct_answer}

【学生答案】
{user_answer}

【判断标准】
1. 如果学生答案与标准答案语义相同（即使表述不同、顺序不同），回答"正确"
2. 如果学生答案缺少关键信息或意思不完全，回答"错误"
3. 如果学生答案与标准答案意思相反或完全不同，回答"错误"

【示例】
标准答案："C是必然事件，B是不可能事件，A是随机事件"
学生答案："C必然事件，B不可能事件，A随机事件" → 正确（表述方式不同，语义相同）

请仅回答一个字："正确" 或 "错误"

判断结果："""
        
        try:
            response = client.chat.completions.create(
                model="qwen-turbo",  # 或其他可用模型
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # 低温度，确定性输出
                max_tokens=10
            )
            result = response.choices[0].message.content.strip()
            print(f"[LLM评估] 用户答案: {user_answer[:30]}... | 结果: {result}")
            
            # 解析结果
            is_correct = "正确" in result or "right" in result.lower()
            return is_correct
            
        except Exception as e:
            print(f"[LLM评估失败] {e}")
            # 降级为简单字符串匹配
            user_ans = user_answer.strip().lower().replace(" ", "").replace("，", "").replace(",", "")
            correct_ans = correct_answer.strip().lower().replace(" ", "").replace("，", "").replace(",", "")
            
            # 简单的包含判断
            return (
                user_ans == correct_ans or
                correct_ans in user_ans or
                user_ans in correct_ans
            )
    
    def _show_completion(self) -> Dict:
        """展示学习完成"""
        progress = self.get_progress()
        accuracy = (self.correct_answers / self.total_questions * 100) if self.total_questions > 0 else 0
        
        content = f"""🎉 恭喜完成本章学习！

📊 学习报告：
• 学习章节：{self.chapter.title}
• 完成考点：{progress['completed']}/{progress['total']}
• 正确率：{accuracy:.1f}%
• 用时：{progress['elapsed_time']} 分钟
• 错题次数：{sum(self.wrong_attempts.values())}

💪 继续加油！建议复习错题，巩固薄弱环节。

回复"重新开始"可以再次学习本章。"""
        
        return {
            "type": "completed",
            "content": content,
            "report": {
                "chapter": self.chapter.title,
                "completed": progress['completed'],
                "total": progress['total'],
                "accuracy": accuracy,
                "elapsed_time": progress['elapsed_time'],
                "wrong_attempts": dict(self.wrong_attempts)
            }
        }
    
    def handle_input(self, user_input: str) -> Dict:
        """
        处理用户输入
        根据当前状态和输入内容决定下一步动作
        """
        user_input = user_input.strip().lower()
        
        # 特殊命令处理
        if user_input in ['重新开始', 'reset']:
            self.__init__(self.session_id)
            return self._show_route()
        
        if user_input in ['进度', 'progress']:
            progress = self.get_progress()
            return {
                "type": "info",
                "content": f"当前进度：{progress['completed']}/{progress['total']} ({progress['percentage']:.1f}%)\n已用时：{progress['elapsed_time']} 分钟"
            }
        
        if user_input in ['帮助', 'help']:
            return {
                "type": "info",
                "content": """可用命令：
• "开始" - 开始学习
• "继续" / "懂了" - 确认理解，进入下一步
• "进度" - 查看学习进度
• "重新开始" - 重置学习进度
• "帮助" - 显示此帮助信息"""
            }
        
        # 状态流转控制
        if self.state == StudyState.SHOWING_ROUTE:
            if user_input in ['开始', 'start', 'ok', '好的']:
                return self._start_chain_learning()
            else:
                return {
                    "type": "info",
                    "content": "请回复\"开始\"进入学习流程，或回复\"帮助\"查看可用命令"
                }
        
        elif self.state == StudyState.LEARNING_CHAIN:
            if user_input in ['继续', '下一', '懂了', 'ok', 'yes']:
                self.current_chain_index += 1
                return self._start_chain_learning()
            else:
                return {
                    "type": "info",
                    "content": "理解了这个概念吗？回复\"继续\"进入下一步"
                }
        
        elif self.state == StudyState.LEARNING_KEYPOINT:
            if user_input in ['懂了', '开始做题', 'ok', 'yes', '开始']:
                return self._show_question()
            else:
                return {
                    "type": "info",
                    "content": "理解了这个考点吗？回复\"懂了\"开始做题测试"
                }
        
        elif self.state == StudyState.TESTING or self.state == StudyState.REVIEWING:
            # 检查答案
            result = self.check_answer(user_input)
            return result
        
        elif self.state == StudyState.COMPLETED:
            if user_input in ['重新开始', 'reset']:
                self.__init__(self.session_id)
                return self._show_route()
            else:
                return {
                    "type": "info",
                    "content": "学习已完成！回复\"重新开始\"可以再次学习"
                }
        
        # 默认：返回当前状态
        return self.get_next_action()


# 全局会话存储（生产环境应使用Redis或数据库）
_sessions: Dict[str, StudySession] = {}


def get_or_create_session(session_id: str) -> StudySession:
    """获取或创建学习会话"""
    if session_id not in _sessions:
        _sessions[session_id] = StudySession(session_id)
    return _sessions[session_id]


def get_session(session_id: str) -> Optional[StudySession]:
    """获取已存在的会话"""
    return _sessions.get(session_id)


def delete_session(session_id: str) -> bool:
    """删除会话"""
    if session_id in _sessions:
        del _sessions[session_id]
        return True
    return False


def get_all_sessions() -> Dict[str, Dict]:
    """获取所有会话的摘要信息"""
    return {
        sid: {
            "session_id": sid,
            "state": session.state.value,
            "progress": session.get_progress()
        }
        for sid, session in _sessions.items()
    }