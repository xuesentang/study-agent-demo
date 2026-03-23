"""
数据库模块
使用SQLite持久化学习进度
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, List
import os


class Database:
    """数据库管理类"""
    
    def __init__(self, db_path: str = "study_agent.db"):
        self.db_path = db_path
        self._init_db()
    
    def _get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_db(self):
        """初始化数据库表"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # 学习会话表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_sessions (
                session_id TEXT PRIMARY KEY,
                state TEXT NOT NULL,
                chapter_id TEXT NOT NULL,
                current_chain_index INTEGER DEFAULT 0,
                current_keypoint_index INTEGER DEFAULT 0,
                completed_keypoints TEXT DEFAULT '[]',
                wrong_attempts TEXT DEFAULT '{}',
                total_questions INTEGER DEFAULT 0,
                correct_answers INTEGER DEFAULT 0,
                start_time TEXT NOT NULL,
                last_update TEXT NOT NULL
            )
        """)
        
        # 学习记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                action_type TEXT NOT NULL,
                content TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES study_sessions(session_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_session(self, session_data: Dict) -> bool:
        """保存学习会话"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO study_sessions (
                    session_id, state, chapter_id, current_chain_index,
                    current_keypoint_index, completed_keypoints, wrong_attempts,
                    total_questions, correct_answers, start_time, last_update
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_data['session_id'],
                session_data['state'],
                session_data.get('chapter_id', 'ch1'),
                session_data.get('current_chain_index', 0),
                session_data.get('current_keypoint_index', 0),
                json.dumps(session_data.get('completed_keypoints', [])),
                json.dumps(session_data.get('wrong_attempts', {})),
                session_data.get('total_questions', 0),
                session_data.get('correct_answers', 0),
                session_data.get('start_time', datetime.now().isoformat()),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"保存会话失败: {e}")
            return False
    
    def load_session(self, session_id: str) -> Optional[Dict]:
        """加载学习会话"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT * FROM study_sessions WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'session_id': row['session_id'],
                    'state': row['state'],
                    'chapter_id': row['chapter_id'],
                    'current_chain_index': row['current_chain_index'],
                    'current_keypoint_index': row['current_keypoint_index'],
                    'completed_keypoints': json.loads(row['completed_keypoints']),
                    'wrong_attempts': json.loads(row['wrong_attempts']),
                    'total_questions': row['total_questions'],
                    'correct_answers': row['correct_answers'],
                    'start_time': row['start_time']
                }
            return None
            
        except Exception as e:
            print(f"加载会话失败: {e}")
            return None
    
    def delete_session(self, session_id: str) -> bool:
        """删除学习会话"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "DELETE FROM study_sessions WHERE session_id = ?",
                (session_id,)
            )
            
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"删除会话失败: {e}")
            return False
    
    def get_all_sessions(self) -> List[Dict]:
        """获取所有会话"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM study_sessions ORDER BY last_update DESC")
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
            
        except Exception as e:
            print(f"获取会话列表失败: {e}")
            return []


# 全局数据库实例
_db_instance = None

def get_db() -> Database:
    """获取数据库单例"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance