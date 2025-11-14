"""
RAG搜索路由
使用ChromaDB进行向量检索
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import chromadb
import os
import sys
import hashlib
import urllib.parse

# 添加backend目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from cli import generate_text_embeddings

router = APIRouter()

# ChromaDB配置
CHROMADB_HOST = os.getenv("CHROMADB_HOST", "chromadb")
CHROMADB_PORT = int(os.getenv("CHROMADB_PORT", "8000"))

def generate_product_image_url(product_name: str) -> str:
    """
    为产品生成图片URL
    使用占位图服务，确保每个产品都有一致的图片
    """
    if not product_name:
        return "https://ui-avatars.com/api/?name=SK&size=200&background=6366f1&color=fff&bold=true"

    # 提取产品名的前两个单词的首字母
    words = product_name.split()
    initials = ''.join([word[0] for word in words[:2]]).upper()
    if not initials:
        initials = "SK"

    # 生成一个基于产品名的颜色（确保一致性）
    hash_obj = hashlib.md5(product_name.encode())
    hash_hex = hash_obj.hexdigest()
    bg_color = hash_hex[:6]

    # 使用ui-avatars.com生成占位图
    url = f"https://ui-avatars.com/api/?name={urllib.parse.quote(initials)}&size=200&background={bg_color}&color=fff&bold=true"
    return url

@router.get("/search")
async def search_products(
    q: str = Query(..., description="搜索查询"),
    top_k: int = Query(default=5, le=20, description="返回结果数量")
):
    """
    使用RAG进行产品搜索

    Parameters:
    - q: 搜索查询（例如: "moisturizer for dry skin"）
    - top_k: 返回结果数量（默认5，最多20）

    Returns:
    - results: 相关产品列表
    """
    try:
        # 连接ChromaDB
        client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
        collection = client.get_collection(name="char-split-collection")

        # 生成查询的embedding
        query_embedding = generate_text_embeddings([q], dimensionality=1536)[0]

        # 在ChromaDB中搜索
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        # 格式化结果并添加图片URL
        formatted_results = []
        for i in range(len(results['documents'][0])):
            metadata = results['metadatas'][0][i] if results['metadatas'] else {}
            product_name = metadata.get('book', 'Unknown Product')

            # 生成产品图片URL
            image_url = generate_product_image_url(product_name)

            formatted_results.append({
                'document': results['documents'][0][i],
                'metadata': metadata,
                'distance': results['distances'][0][i] if results['distances'] else None,
                'image_url': image_url,
                'product_name': product_name
            })

        return {
            "query": q,
            "total": len(formatted_results),
            "results": formatted_results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search error: {str(e)}"
        )
