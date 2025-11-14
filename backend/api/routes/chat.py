"""
对话路由
处理与 AI 的对话交互
集成OpenAI GPT + ChromaDB RAG
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid
from datetime import datetime
import os
import sys
import chromadb

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

# 请求模型
class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict] = None
    history: Optional[List[Dict]] = []

class ChatContext(BaseModel):
    analysis_id: Optional[str] = None
    skin_type: Optional[str] = None
    concerns: Optional[List[str]] = []
    chat_history: Optional[List[dict]] = []

# 响应模型
class ChatResponse(BaseModel):
    message_id: str
    response: str
    suggested_products: Optional[List[str]] = []
    follow_up_questions: Optional[List[str]] = []
    timestamp: str

@router.post("/", response_model=ChatResponse)
@router.post("/message", response_model=ChatResponse)
async def chat_with_ai(request: ChatMessage):
    """
    与 AI 对话 - 使用 OpenAI GPT + ChromaDB RAG

    Parameters:
    - message: 用户消息
    - context: 对话上下文
    - history: 对话历史

    Returns:
    - AI 回复（基于RAG检索的护肤品知识）
    - 推荐产品
    - 后续问题建议
    """
    try:
        message_id = str(uuid.uuid4())
        user_message = request.message

        # 1. 使用ChromaDB检索相关护肤品信息（RAG）
        relevant_context = await retrieve_skincare_context(user_message)

        # 2. 使用OpenAI GPT生成回复
        if USE_OPENAI and OPENAI_CLIENT:
            response_text = await generate_gpt_response(
                user_message=user_message,
                context=relevant_context,
                history=request.history or []
            )
        else:
            # 降级到规则响应
            response_text = generate_mock_response(user_message.lower(), request.context or {})

        # 3. 提取产品推荐
        suggested_products = extract_product_names(relevant_context)

        # 4. 生成后续问题
        follow_up_questions = [
            "您想了解这些产品的具体成分吗？",
            "需要我推荐其他类型的护肤品吗？",
            "您有其他肌肤问题需要咨询吗？"
        ]

        return ChatResponse(
            message_id=message_id,
            response=response_text,
            suggested_products=suggested_products[:3],
            follow_up_questions=follow_up_questions,
            timestamp=datetime.utcnow().isoformat()
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}"
        )

async def retrieve_skincare_context(user_message: str) -> List[Dict]:
    """
    从ChromaDB检索相关护肤品信息

    Parameters:
    - user_message: 用户消息

    Returns:
    - 相关产品信息列表
    """
    try:
        # 连接ChromaDB
        client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
        collection = client.get_collection(name="char-split-collection")

        # 生成查询的embedding
        query_embedding = generate_text_embeddings([user_message], dimensionality=1536)[0]

        # 在ChromaDB中搜索
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,  # 获取前5个最相关的结果
            include=["documents", "metadatas", "distances"]
        )

        # 格式化结果
        context = []
        for i in range(len(results['documents'][0])):
            context.append({
                'text': results['documents'][0][i],
                'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                'distance': results['distances'][0][i] if results['distances'] else None
            })

        return context

    except Exception as e:
        print(f"Error retrieving context from ChromaDB: {e}")
        return []

async def generate_gpt_response(user_message: str, context: List[Dict], history: List[Dict]) -> str:
    """
    使用OpenAI GPT生成回复

    Parameters:
    - user_message: 用户消息
    - context: ChromaDB检索的相关上下文
    - history: 对话历史

    Returns:
    - GPT生成的回复
    """
    try:
        # 构建系统提示词
        system_prompt = """你是一位专业的护肤顾问AI助手，拥有丰富的护肤品知识。你的任务是：

1. 基于EWG（Environmental Working Group）护肤品数据库的信息，为用户提供专业、准确的护肤建议
2. 根据用户的肤质、问题和需求，推荐合适的护肤品
3. 解释产品成分及其功效
4. 提供科学的护肤步骤和使用建议
5. 回答要友好、专业，用中文回答

重要原则：
- 只推荐数据库中有的产品
- 说明推荐理由（成分、功效等）
- 提醒可能的注意事项（如敏感成分、使用顺序等）
- 如果不确定，诚实告知用户"""

        # 构建上下文信息
        context_text = "\n\n相关护肤品信息：\n"
        for i, item in enumerate(context[:3], 1):  # 只使用前3个最相关的结果
            context_text += f"\n{i}. {item['text']}\n"
            if item.get('metadata'):
                metadata = item['metadata']
                if 'book' in metadata:
                    context_text += f"   来源: {metadata['book']}\n"

        # 构建消息历史
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        # 添加历史对话（最多保留最近5轮）
        for msg in history[-5:]:
            if isinstance(msg, dict):
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                if content:
                    messages.append({"role": role, "content": content})

        # 添加当前用户消息和上下文
        user_message_with_context = f"{user_message}\n{context_text}"
        messages.append({"role": "user", "content": user_message_with_context})

        # 调用OpenAI API
        response = OPENAI_CLIENT.chat.completions.create(
            model="gpt-4o-mini",  # 使用GPT-4o-mini，性价比高
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error generating GPT response: {e}")
        # 降级到模拟响应
        return "抱歉，AI服务暂时不可用。让我用基础知识为您解答..."

def extract_product_names(context: List[Dict]) -> List[str]:
    """
    从上下文中提取产品名称

    Parameters:
    - context: ChromaDB检索的相关上下文

    Returns:
    - 产品名称列表
    """
    products = []

    for item in context[:5]:  # 最多提取5个产品
        metadata = item.get('metadata', {})

        # 尝试从metadata中提取产品名
        if 'product_name' in metadata:
            products.append(metadata['product_name'])
        elif 'book' in metadata:
            # 如果book字段包含产品信息，提取它
            book = metadata['book']
            if book and book not in products:
                products.append(book)

        # 也可以尝试从文本中提取产品名（简单匹配）
        text = item.get('text', '')
        if text and len(products) < 5:
            # 提取前50个字符作为产品预览
            preview = text[:50].strip()
            if preview and preview not in products:
                products.append(preview)

    return products[:3]  # 返回最多3个产品

def generate_mock_response(message: str, context: dict) -> str:
    """生成模拟 AI 响应（后续替换为真实 LLM）"""

    skin_type = context.get("skin_type", "").lower()
    concerns = context.get("concerns", [])

    # 简单的关键词匹配
    if "洁面" in message or "cleanser" in message:
        if skin_type == "oily":
            return "对于油性肌肤，我推荐使用含有水杨酸的泡沫洁面产品。它能有效清洁毛孔，控制油脂分泌。每天早晚使用，注意不要过度清洁。"
        elif skin_type == "dry":
            return "干性肌肤建议使用温和的乳状洁面产品，含有神经酰胺和透明质酸的配方能在清洁的同时保持肌肤水分。避免使用含有皂基的洁面产品。"
        else:
            return "根据您的肤质，我建议使用温和的凝胶状洁面产品。它能平衡肌肤的水油状态，既能清洁T区的油脂，又不会让两颊过于干燥。"

    elif "爽肤水" in message or "toner" in message:
        return "爽肤水的选择要根据您的肌肤需求。如果您的肌肤偏油，可以选择含有金缕梅或茶树成分的清爽型爽肤水；如果偏干，建议选择保湿型爽肤水，含有透明质酸或甘油成分。"

    elif "精华" in message or "serum" in message:
        if "acne" in concerns or "痘" in message:
            return "针对痘痘问题，我推荐含有烟酰胺或水杨酸的精华液。烟酰胺能帮助调节皮脂分泌，减少炎症；水杨酸则能深入毛孔清洁。建议从低浓度开始使用。"
        elif "wrinkles" in concerns or "细纹" in message or "抗" in message:
            return "对于抗老需求，维A醇（Retinol）精华是黄金成分。它能促进胶原蛋白生成，改善细纹。初次使用建议从低浓度开始，并在晚上使用，白天务必做好防晒。"
        else:
            return "精华液是护肤中的重要步骤。根据您的肤质，我建议使用保湿精华，含有透明质酸、神经酰胺等成分能深层滋润肌肤。"

    elif "防晒" in message or "sunscreen" in message:
        return "防晒是护肤中最重要的步骤！建议选择 SPF 30 以上的广谱防晒产品。如果您的肌肤偏油，可以选择清爽型的化学防晒；如果敏感，物理防晒会更温和。记得每2-3小时补涂一次。"

    elif "顺序" in message or "步骤" in message or "routine" in message:
        return """正确的护肤顺序是：

早上：
1. 洁面
2. 爽肤水
3. 精华（如维C精华）
4. 乳液/面霜
5. 防晒（最重要！）

晚上：
1. 卸妆（如有化妆）
2. 洁面
3. 爽肤水
4. 精华（如维A醇精华）
5. 乳液/面霜

记住：从最轻薄的质地用到最厚重的质地。"""

    elif "预算" in message or "price" in message or "便宜" in message:
        return "护肤不一定要买贵的产品！很多平价品牌如 CeraVe、The Ordinary、The Inkey List 都有非常有效的产品。关键是选择适合自己肤质、含有有效成分的产品，并坚持使用。"

    elif "敏感" in message or "sensitive" in message:
        return "敏感肌肤需要特别呵护。建议选择无香料、无酒精、经过敏感肌测试的产品。避免使用含有刺激性成分如高浓度果酸、酒精的产品。建议先在耳后做过敏测试再全脸使用。"

    else:
        return f"我理解您对'{message}'的疑问。基于您的{skin_type}肤质，我可以为您提供个性化的护肤建议。请问您具体想了解洁面、保湿、还是其他护肤步骤呢？"

def extract_product_suggestions(message: str, context: dict) -> List[str]:
    """从消息中提取可能的产品推荐"""
    suggestions = []

    if "洁面" in message or "cleanser" in message:
        suggestions = ["prod_001", "prod_002"]
    elif "面霜" in message or "cream" in message or "保湿" in message:
        suggestions = ["prod_003"]

    return suggestions

def generate_follow_up_questions(message: str, context: dict) -> List[str]:
    """生成后续问题建议"""
    questions = [
        "您想了解具体的产品推荐吗？",
        "您的预算范围是多少呢？",
        "您还有其他肌肤问题想要改善吗？"
    ]

    # 根据消息内容动态生成
    if "洁面" in message:
        questions = [
            "您更喜欢泡沫型还是乳液型的洁面产品？",
            "您早晚都需要使用洁面产品吗？",
            "您想了解卸妆产品推荐吗？"
        ]
    elif "精华" in message:
        questions = [
            "您之前使用过维A醇产品吗？",
            "您更关注保湿、美白还是抗老？",
            "您想了解精华的正确使用顺序吗？"
        ]

    return questions[:3]  # 返回最多3个问题
