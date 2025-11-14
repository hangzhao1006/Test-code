"""
图片分析路由
使用 GPT-4 Vision API 分析皮肤状况并推荐产品
"""
from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from typing import List, Optional, Dict
import base64
import os
import sys
import chromadb
from io import BytesIO

# 添加backend目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from cli import generate_text_embeddings

# OpenAI配置
try:
    from openai import OpenAI
    OPENAI_CLIENT = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    USE_OPENAI = True
except Exception as e:
    print(f"OpenAI not available: {e}")
    USE_OPENAI = False

# ChromaDB配置
CHROMADB_HOST = os.getenv("CHROMADB_HOST", "chromadb")
CHROMADB_PORT = int(os.getenv("CHROMADB_PORT", "8000"))

router = APIRouter()

class SkinAnalysisResponse(BaseModel):
    analysis: str
    skin_type: Optional[str] = None
    concerns: List[str] = []
    recommendations: List[str] = []
    recommended_products: List[Dict] = []

@router.post("/analyze-skin", response_model=SkinAnalysisResponse)
async def analyze_skin_image(
    image: UploadFile = File(...),
    additional_info: Optional[str] = Form(None)
):
    """
    分析皮肤图片并推荐产品

    Parameters:
    - image: 上传的皮肤照片
    - additional_info: 额外的信息（如：皮肤问题描述）

    Returns:
    - 皮肤分析结果和产品推荐
    """
    if not USE_OPENAI:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API is not configured"
        )

    try:
        # 读取图片内容
        image_bytes = await image.read()

        # 将图片转换为base64
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        # 使用GPT-4 Vision分析图片
        analysis_result = await analyze_with_gpt4_vision(
            base64_image=base64_image,
            additional_info=additional_info
        )

        # 根据分析结果从数据库检索相关产品
        recommended_products = await get_product_recommendations(analysis_result)

        return SkinAnalysisResponse(
            analysis=analysis_result['analysis'],
            skin_type=analysis_result.get('skin_type'),
            concerns=analysis_result.get('concerns', []),
            recommendations=analysis_result.get('recommendations', []),
            recommended_products=recommended_products
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing image: {str(e)}"
        )

async def analyze_with_gpt4_vision(base64_image: str, additional_info: Optional[str] = None) -> Dict:
    """
    使用GPT-4 Vision API分析皮肤状况

    Parameters:
    - base64_image: Base64编码的图片
    - additional_info: 额外信息

    Returns:
    - 分析结果字典
    """
    try:
        # 构建提示词
        prompt = """你是一位专业的皮肤分析师。请仔细分析这张皮肤照片，并提供详细的分析报告。

请按以下格式回答：

**肤质类型**: [干性/油性/混合性/敏感性/中性]

**主要问题**:
- [问题1]
- [问题2]
- [问题3]

**护肤建议**:
1. [建议1]
2. [建议2]
3. [建议3]

**产品关键词**: [用于搜索产品的关键词，用逗号分隔]

请用中文回答，专业且友好。"""

        if additional_info:
            prompt += f"\n\n用户补充信息: {additional_info}"

        # 调用GPT-4 Vision API
        response = OPENAI_CLIENT.chat.completions.create(
            model="gpt-4o-mini",  # 使用支持视觉的模型
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )

        analysis_text = response.choices[0].message.content

        # 解析分析结果
        result = parse_analysis_result(analysis_text)

        return result

    except Exception as e:
        print(f"Error in GPT-4 Vision analysis: {e}")
        raise

def parse_analysis_result(analysis_text: str) -> Dict:
    """
    解析GPT-4的分析结果

    Parameters:
    - analysis_text: GPT-4返回的文本

    Returns:
    - 结构化的分析结果
    """
    result = {
        'analysis': analysis_text,
        'skin_type': None,
        'concerns': [],
        'recommendations': [],
        'search_keywords': []
    }

    lines = analysis_text.split('\n')
    current_section = None

    for line in lines:
        line = line.strip()

        if '肤质类型' in line or 'Skin Type' in line:
            # 提取肤质类型
            if ':' in line:
                skin_type = line.split(':')[-1].strip()
                result['skin_type'] = skin_type

        elif '主要问题' in line or 'Main Concerns' in line:
            current_section = 'concerns'

        elif '护肤建议' in line or 'Recommendations' in line:
            current_section = 'recommendations'

        elif '产品关键词' in line or 'Product Keywords' in line:
            current_section = 'keywords'
            if ':' in line:
                keywords = line.split(':')[-1].strip()
                result['search_keywords'] = [k.strip() for k in keywords.split(',')]

        elif line.startswith('-') or line.startswith('•'):
            # 列表项
            item = line.lstrip('-•').strip()
            if current_section == 'concerns' and item:
                result['concerns'].append(item)

        elif line and line[0].isdigit() and '.' in line:
            # 数字列表项
            item = line.split('.', 1)[-1].strip()
            if current_section == 'recommendations' and item:
                result['recommendations'].append(item)

    return result

async def get_product_recommendations(analysis_result: Dict) -> List[Dict]:
    """
    根据分析结果从ChromaDB检索推荐产品

    Parameters:
    - analysis_result: 分析结果

    Returns:
    - 推荐产品列表
    """
    try:
        # 连接ChromaDB
        client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
        collection = client.get_collection(name="char-split-collection")

        # 构建搜索查询
        search_queries = []

        # 添加肤质相关查询
        if analysis_result.get('skin_type'):
            search_queries.append(f"{analysis_result['skin_type']} skin products")

        # 添加问题相关查询
        for concern in analysis_result.get('concerns', [])[:2]:  # 取前2个问题
            search_queries.append(concern)

        # 添加关键词查询
        for keyword in analysis_result.get('search_keywords', [])[:2]:  # 取前2个关键词
            search_queries.append(keyword)

        # 如果没有查询，使用默认查询
        if not search_queries:
            search_queries = ["facial moisturizer", "hydrating serum"]

        all_products = []
        seen_product_names = set()

        # 对每个查询进行搜索
        for query in search_queries[:3]:  # 最多使用3个查询
            query_embedding = generate_text_embeddings([query], dimensionality=1536)[0]

            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=3,  # 每个查询返回3个产品
                include=["documents", "metadatas", "distances"]
            )

            # 格式化结果
            for i in range(len(results['documents'][0])):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                product_name = metadata.get('product_name', metadata.get('book', ''))

                # 避免重复产品
                if product_name and product_name not in seen_product_names:
                    seen_product_names.add(product_name)

                    all_products.append({
                        'name': product_name,
                        'brand': metadata.get('brand', ''),
                        'category': metadata.get('category', ''),
                        'description': results['documents'][0][i][:200],
                        'amazon_url': metadata.get('amazon_url', ''),
                        'ewg_url': metadata.get('ewg_url', ''),
                        'relevance': round(1 - results['distances'][0][i], 3)
                    })

        # 按相关度排序，返回前5个
        all_products.sort(key=lambda x: x['relevance'], reverse=True)
        return all_products[:5]

    except Exception as e:
        print(f"Error getting product recommendations: {e}")
        return []
