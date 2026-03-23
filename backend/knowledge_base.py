"""
RAG 知识库模块
支持从文本文件加载、智能切分、向量存储和检索
"""

import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import os
import re
from pathlib import Path

class KnowledgeBase:
    """知识库类"""
    
    def __init__(self, collection_name: str = "probability_stats"):
        """
        初始化知识库
        
        Args:
            collection_name: 集合名称
        """
        # 使用持久化存储（数据保存在磁盘）
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # 获取或创建集合
        try:
            self.collection = self.client.get_collection(collection_name)
            print(f"✅ 已加载现有知识库: {collection_name}")
        except:
            self.collection = self.client.create_collection(collection_name)
            print(f"✅ 创建新知识库: {collection_name}")
        
        # 加载嵌入模型
        print("🔄 加载嵌入模型...")
        self.encoder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("✅ 嵌入模型加载完成")
    
    def load_documents(self, docs_dir: str = "documents") -> int:
        """
        从目录加载所有文本文件
        
        Args:
            docs_dir: 文档目录路径
            
        Returns:
            加载的文档数量
        """
        docs_path = Path(docs_dir)
        if not docs_path.exists():
            print(f"❌ 目录不存在: {docs_dir}")
            print("💡 请创建 documents/ 文件夹并添加 .txt 文件")
            return 0
        
        txt_files = list(docs_path.glob("*.txt"))
        if not txt_files:
            print(f"⚠️ 目录中没有 .txt 文件: {docs_dir}")
            return 0
        
        total_chunks = 0
        
        for txt_file in txt_files:
            print(f"\n📄 正在处理: {txt_file.name}")
            try:
                # 读取文件内容
                content = txt_file.read_text(encoding='utf-8')
                
                # 提取章节信息
                chapter_title = txt_file.stem  # 文件名作为章节标题
                
                # 智能切分
                chunks = self.split_by_sections(content, chapter_title)
                
                # 添加到知识库
                if chunks:
                    self.add_chunks_to_collection(chunks)
                    total_chunks += len(chunks)
                    print(f"   ✅ 已添加 {len(chunks)} 个知识点")
                
            except Exception as e:
                print(f"   ❌ 处理失败: {e}")
        
        print(f"\n🎉 共加载 {len(txt_files)} 个文件，{total_chunks} 个知识点")
        return total_chunks
    
    def split_by_sections(self, content: str, chapter_title: str) -> List[Dict]:
        """
        按章节标题智能切分文本
        
        Args:
            content: 原始文本内容
            chapter_title: 章节标题
            
        Returns:
            切分后的知识点列表
        """
        chunks = []
        
        # 匹配类似 "1.1 标题" 或 "## 1.1 标题" 的格式
        # 支持：1.1、1.1.1、第1节 等格式
        section_pattern = r'(?:^|\n)(?:#{0,2}\s*)?(\d+\.\d+(?:\.\d+)?\s+.+?)(?=\n(?:#{0,2}\s*)?\d+\.\d+(?:\.\d+)?\s+|\Z)'
        
        sections = re.split(section_pattern, content)
        
        # 如果切分失败，按段落切分
        if len(sections) <= 1:
            return self.split_by_paragraphs(content, chapter_title)
        
        # 处理切分结果
        current_section = ""
        for i, part in enumerate(sections):
            part = part.strip()
            if not part:
                continue
            
            # 检查是否是标题
            if re.match(r'^\d+\.\d+', part):
                current_section = part
            else:
                # 这是内容部分
                if current_section:
                    # 提取小节编号和标题
                    match = re.match(r'^(\d+\.\d+(?:\.\d+)?)\s+(.+)$', current_section)
                    if match:
                        section_id = match.group(1)
                        section_title = match.group(2)
                    else:
                        section_id = f"sec_{i}"
                        section_title = current_section
                    
                    # 创建知识点
                    chunk = {
                        "id": f"{chapter_title}_{section_id}",
                        "content": f"{section_title}\n\n{part}",
                        "metadata": {
                            "chapter": chapter_title,
                            "section_id": section_id,
                            "section_title": section_title,
                            "type": "知识点",
                            "source": chapter_title
                        }
                    }
                    chunks.append(chunk)
        
        # 如果没有切分出内容，按段落切分
        if not chunks:
            return self.split_by_paragraphs(content, chapter_title)
        
        return chunks
    
    def split_by_paragraphs(self, content: str, chapter_title: str) -> List[Dict]:
        """
        按段落切分（备用方案）
        
        Args:
            content: 原始文本内容
            chapter_title: 章节标题
            
        Returns:
            切分后的知识点列表
        """
        chunks = []
        
        # 按空行分割段落
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        for i, para in enumerate(paragraphs):
            # 限制每个chunk的长度（避免过长）
            if len(para) > 500:
                # 长段落按句子切分
                sentences = re.split(r'([。！？.!?]\s*)', para)
                current_chunk = ""
                
                for j in range(0, len(sentences), 2):
                    sentence = sentences[j]
                    if j + 1 < len(sentences):
                        sentence += sentences[j + 1]
                    
                    if len(current_chunk) + len(sentence) < 400:
                        current_chunk += sentence
                    else:
                        if current_chunk:
                            chunks.append({
                                "id": f"{chapter_title}_p{i}_s{j}",
                                "content": current_chunk,
                                "metadata": {
                                    "chapter": chapter_title,
                                    "section_id": f"p{i}",
                                    "type": "段落",
                                    "source": chapter_title
                                }
                            })
                        current_chunk = sentence
                
                if current_chunk:
                    chunks.append({
                        "id": f"{chapter_title}_p{i}",
                        "content": current_chunk,
                        "metadata": {
                            "chapter": chapter_title,
                            "section_id": f"p{i}",
                            "type": "段落",
                            "source": chapter_title
                        }
                    })
            else:
                chunks.append({
                    "id": f"{chapter_title}_p{i}",
                    "content": para,
                    "metadata": {
                        "chapter": chapter_title,
                        "section_id": f"p{i}",
                        "type": "段落",
                        "source": chapter_title
                    }
                })
        
        return chunks
    
    def add_chunks_to_collection(self, chunks: List[Dict]):
        """
        将知识点添加到向量数据库
        
        Args:
            chunks: 知识点列表
        """
        if not chunks:
            return
        
        # 准备数据
        ids = [chunk["id"] for chunk in chunks]
        documents = [chunk["content"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        
        # 生成向量
        embeddings = self.encoder.encode(documents).tolist()
        
        # 添加到集合
        self.collection.add(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query: str, n_results: int = 3, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """
        搜索相关知识
        
        Args:
            query: 查询文本
            n_results: 返回结果数量
            filter_dict: 过滤条件（如 {"chapter": "第一章"}）
            
        Returns:
            相关知识点列表
        """
        # 编码查询
        query_embedding = self.encoder.encode([query]).tolist()
        
        # 执行检索
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            where=filter_dict,  # 可选过滤
            include=["documents", "metadatas", "distances"]
        )
        
        # 格式化结果
        formatted_results = []
        for i in range(len(results["ids"][0])):
            formatted_results.append({
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "score": 1 - results["distances"][0][i]  # 转换为相似度分数
            })
        
        return formatted_results
    
    def get_stats(self) -> Dict:
        """获取知识库统计信息"""
        return {
            "total_documents": self.collection.count(),
            "collection_name": self.collection.name
        }
    
    def delete_collection(self):
        """删除整个集合（谨慎使用）"""
        try:
            self.client.delete_collection(self.collection.name)
            print(f"✅ 已删除集合: {self.collection.name}")
        except Exception as e:
            print(f"❌ 删除失败: {e}")


# 全局知识库实例（单例模式）
_kb_instance = None

def get_knowledge_base() -> KnowledgeBase:
    """获取知识库单例"""
    global _kb_instance
    if _kb_instance is None:
        _kb_instance = KnowledgeBase()
    return _kb_instance


def init_knowledge_base(docs_dir: str = "documents") -> KnowledgeBase:
    """
    初始化知识库并加载文档
    
    Args:
        docs_dir: 文档目录路径
        
    Returns:
        知识库实例
    """
    kb = get_knowledge_base()
    
    # 如果知识库为空，加载文档
    stats = kb.get_stats()
    if stats["total_documents"] == 0:
        print("🔄 知识库为空，开始加载文档...")
        kb.load_documents(docs_dir)
    else:
        print(f"✅ 知识库已有 {stats['total_documents']} 条记录")
    
    return kb

if __name__ == "__main__":
    # 初始化并加载文档
    kb = init_knowledge_base()
    
    # 显示统计
    stats = kb.get_stats()
    print(f"\n📊 知识库统计: {stats}")
    
    # 测试搜索
    print("\n🔍 测试搜索:")
    results = kb.search("什么是随机事件", n_results=2)
    for i, result in enumerate(results, 1):
        print(f"\n--- 结果 {i} (相似度: {result['score']:.2f}) ---")
        print(f"来源: {result['metadata']['chapter']}")
        print(f"内容: {result['content'][:100]}...")